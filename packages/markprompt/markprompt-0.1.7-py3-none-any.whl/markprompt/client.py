"""
MarkPrompt client implementation.
"""
import inspect
import os
from pathlib import Path
from typing import Dict, Optional, Union, List, Callable, Any

from openai import OpenAI

from .core import TemplateParser
from .core.logger import setup_logger, message_logger, DynamicLogger, format_tool_calls
from .core.tools import ToolHandler

logger = setup_logger(__name__)


class MarkPromptClient:
    """Client for generating responses using MarkPrompt templates."""

    def __init__(self, template_dir: Union[str, Path] = '.', client: Optional[OpenAI] = None):
        """Initialize the client.
        
        Args:
            template_dir: Directory containing prompt templates. Can be a string or Path object.
            client: Optional OpenAI client instance. If not provided, a default OpenAI client will be used.
        """
        if isinstance(template_dir, str):
            # 处理 ~ 开头的路径
            if template_dir.startswith("~"):
                template_dir = os.path.expanduser(template_dir)

            # 如果是相对路径，从调用者的文件位置开始查找
            if not os.path.isabs(template_dir):
                caller_frame = inspect.stack()[1]
                caller_file = caller_frame.filename
                caller_dir = os.path.dirname(os.path.abspath(caller_file))
                template_dir = os.path.join(caller_dir, template_dir)

            template_dir = Path(template_dir)

        if not template_dir.is_dir():
            raise ValueError(f"Template directory not found: {template_dir}")

        self.template_dir = template_dir
        self.client = client if client else OpenAI()
        self.parser = TemplateParser()

    def _create_client_from_provider(self, provider_config: Dict[str, Any]) -> OpenAI:
        """根据提供商配置创建 OpenAI 客户端。
        
        Args:
            provider_config: 提供商配置字典
            
        Returns:
            初始化好的 OpenAI 客户端
        """
        openai_params = [
            "api_key", "base_url", "timeout", "max_retries", 
            "default_headers", "default_query", "organization",
            "project_id", "api_version"
        ]
        
        client_kwargs = {}
        for key, value in provider_config.items():
            if key in openai_params:
                client_kwargs[key] = value
            
        return OpenAI(**client_kwargs)

    def _choose_chat_completion_method(self, client, params):
        """根据参数选择合适的 OpenAI API 调用方法
        
        Args:
            client: OpenAI 客户端实例
            params: API 调用参数
            
        Returns:
            Tuple[Callable, bool]: 包含选择的方法和是否为 parse 方法的标志
        """
        # 检查是否使用了 response_format 参数且是 BaseModel 类型
        response_format = params.get('response_format')
        use_parse_method = response_format is not None and hasattr(response_format, '__class__') and getattr(response_format.__class__, '__name__', '') == 'BaseModel'
        
        if use_parse_method:
            # 当提供了 BaseModel 类型的 response_format 时使用 beta.chat.completions.parse()
            return client.beta.chat.completions.parse, True
        else:
            # 正常情况使用普通的 chat.completions.create()
            return client.chat.completions.create, False

    def _generate_with_tools(self, messages, tools: List[Callable], verbose: bool = False, client=None, **params):
        tool_handler = ToolHandler(tools=tools, verbose=verbose)
        openai_tools = tool_handler.convert_tools_to_openai_format()
        client_to_use = client if client is not None else self.client

        with DynamicLogger() as alogger:
            # 获取适合的 API 调用方法
            chat_completion_method, _ = self._choose_chat_completion_method(client_to_use, params)
            
            # 使用工具必须使用 chat.completions.create 方法
            response = chat_completion_method(
                messages=messages,
                tools=openai_tools,
                **params
            )

            if response.choices[0].message.tool_calls is None:
                panel_content = response.choices[0].message.content
                alogger.log(panel_content)
                return response

            if verbose:
                content = format_tool_calls(response.choices[0].message.tool_calls)
                alogger.log(content)

            tool_results = tool_handler.execute_tool_calls(
                response.choices[0].message.tool_calls
            )

            if tool_results:
                try:
                    new_messages = messages.copy()
                    new_messages.append({
                        "role": "assistant",
                        "tool_calls": response.choices[0].message.tool_calls
                    })
                    new_messages.extend(tool_results)
                    
                    # 第二次调用也获取适合的方法 (但工具调用后不使用parse方法)
                    chat_completion_method, _ = self._choose_chat_completion_method(client_to_use, params)
                    second_response = chat_completion_method(
                        messages=new_messages,
                        **params
                    )

                    if verbose:
                        alogger.log("\n\n")
                        panel_content = second_response.choices[0].message.content
                        alogger.log(panel_content)
                    return second_response
                except Exception as e:
                    if verbose:
                        print(f"{str(e)}")
                        logger.error(f"二次请求失败: {str(e)}")
                        panel_content += f"\n\n生成失败: {str(e)}"
                        logger.error(f"二次请求失败: {panel_content}")
                    return response

    def generate(
        self,
        template_name: str,
        user_input: str,
        input_variables: Optional[Dict[str, str]] = None,
        verbose: bool = False,
        tools: Optional[List[Callable]] = None,
        **override_params
    ):
        """Generate a response using the specified template.
        
        Args:
            template_name: Name of the template file (without .md extension)
            user_input: User input content
            input_variables: Optional template variables
            verbose: Optional flag to enable verbose logging
            tools: Optional list of functions to be converted to OpenAI tools/function calling
            **override_params: Parameters to override template's generate_config,
                             including 'stream' for streaming output,
                             or 'response_format' to use beta.chat.completions.parse()
            
        Returns:
            If override_params contains stream=True, returns a streaming response iterator
            Otherwise, returns the complete response
        """
        template_path = self.template_dir / f"{template_name}.md"
        if not template_path.exists():
            raise ValueError(f"Template not found: {template_name}")

        with open(template_path, "r", encoding="utf-8") as f:
            template = self.parser.parse(f.read())

        # 默认使用已初始化的客户端
        client = self.client
        
        # 如果模板中定义了 provider 配置，创建临时客户端实例
        if template.provider:
            try:
                temp_client = self._create_client_from_provider(template.provider)
                client = temp_client
                if verbose:
                    logger.info(f"Using template-specific provider: {template.provider.get('name', 'unknown')}")
            except Exception as e:
                logger.error(f"创建模板特定客户端失败: {str(e)}，使用默认客户端")

        input_values = input_variables or {}
        input_values["user_input"] = user_input

        messages = self.parser.render(template, input_values)
        if messages[-1]['role'] != 'user':
            messages.append({"role": "user", "content": user_input})

        if verbose:
            message_logger.log_messages(messages)

        params = {k: v for k, v in template.generation_config.items() if v is not None}
        params.update(override_params)

        if tools:
            return self._generate_with_tools(messages, tools, verbose, client=client, **params)
        else:
            # 获取适合的 API 调用方法
            chat_completion_method, _ = self._choose_chat_completion_method(client, params)
            
            # 使用选择的方法调用 API
            response = chat_completion_method(
                messages=messages,
                **params
            )

            if params.get('stream'):
                return response

            if verbose:
                if hasattr(response, 'choices') and hasattr(response.choices[0], 'message'):
                    message = response.choices[0].message
                    message_logger.log_message(message.__dict__)

            return response
