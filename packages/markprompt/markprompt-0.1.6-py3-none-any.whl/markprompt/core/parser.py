"""
MarkPrompt template parser.
"""
import logging
import re
from typing import Dict, List, Optional, Tuple, Any

import frontmatter

from .models import PromptTemplate

logger = logging.getLogger(__name__)

DEFAULT_ROLES = {
    "system": "system\n---\n",
    "user": "user\n---\n",
    "assistant": "assistant\n---\n"
}

DEFAULT_PROVIDER = "openai"


class TemplateParser:
    """Parser for MarkPrompt templates."""

    def __init__(self):
        self._var_pattern = re.compile(r"{{([a-z_]+)}}")

    def parse(self, content: str) -> PromptTemplate:
        """Parse template content into a PromptTemplate object."""
        metadata, template_content = self._parse_frontmatter(content)

        roles = DEFAULT_ROLES.copy()
        if "roles" in metadata:
            roles.update(metadata["roles"])

        messages = self._parse_messages(template_content, roles)

        provider_config = None
        if "provider" in metadata:
            provider_config = metadata.get("provider")
        elif "generation_config" in metadata and "model" in metadata["generation_config"]:
            model = metadata["generation_config"]["model"]
            parsed_model = self._parse_model_string(model)
            
            if parsed_model["provider"] != model:     # 表示成功解析了 provider/model 格式
                metadata["generation_config"]["model"] = parsed_model["model"]
                provider_config = {"name": parsed_model["provider"]}

        template = PromptTemplate(
            metadata=metadata.get("metadata"),
            roles=roles,
            generation_config=metadata.get("generation_config", {}),
            input_variables=metadata.get("input_variables", {}),
            messages=messages,
            provider=provider_config
        )
        return template

    def _parse_model_string(self, model_string: str) -> Dict[str, str]:
        """Parse model string in format 'provider/model'."""
        if "/" in model_string:
            provider_name, model_name = model_string.split("/", 1)
            return {
                "provider": provider_name,
                "model": model_name
            }
        return {
            "provider": DEFAULT_PROVIDER,
            "model": model_string
        }

    def _parse_messages(self, content: str, roles: Dict[str, str]) -> List[Dict[str, str]]:
        """解析模板内容为消息列表，不替换变量。"""
        # 如果没有角色定义，则将所有内容视为系统消息
        if not roles:
            return [{"role": "system", "content": content.strip()}]

        case_insensitive_roles = {}
        for role, prefix in roles.items():
            role_name = prefix.split('\n')[0]
            case_insensitive_roles[role_name.lower()] = (role, prefix)

        messages = []
        current_pos = 0
        while current_pos < len(content):
            role_match = False
            matched_role = None
            matched_prefix = None

            is_line_start = current_pos == 0 or content[current_pos - 1] == '\n'

            if not is_line_start:
                current_pos += 1
                continue

            for role_name in case_insensitive_roles.keys():
                if current_pos + len(role_name) <= len(content):
                    possible_role = content[current_pos:current_pos + len(role_name)]

                    if possible_role.lower() == role_name.lower() and \
                        current_pos + len(role_name) + 5 <= len(content) and \
                        content[current_pos + len(role_name):current_pos + len(role_name) + 5] == '\n---\n':
                        original_role, prefix = case_insensitive_roles[role_name.lower()]
                        role_match = True
                        matched_role = original_role
                        matched_prefix = possible_role + '\n---\n'
                        break

            if not role_match:
                messages.append({"role": "system", "content": content.strip()})
                break

            start_pos = current_pos + len(matched_prefix)
            end_pos = len(content)

            for role_name in case_insensitive_roles.keys():
                remaining = content[start_pos:]
                search_pos = 0
                while search_pos < len(remaining):
                    next_pos = remaining.lower().find(role_name.lower(), search_pos)
                    if next_pos == -1:
                        break

                    is_line_start = next_pos == 0 or remaining[next_pos - 1] == '\n'

                    possible_role = remaining[next_pos:next_pos + len(role_name)]
                    if is_line_start and next_pos + len(role_name) + 5 <= len(remaining) and \
                        remaining[next_pos + len(role_name):next_pos + len(role_name) + 5] == '\n---\n' and \
                        possible_role.lower() == role_name.lower():
                        absolute_pos = start_pos + next_pos
                        if absolute_pos < end_pos:
                            end_pos = absolute_pos
                        break

                    search_pos = next_pos + 1

            message_content = content[start_pos:end_pos].strip()
            messages.append({
                "role": matched_role,
                "content": message_content
            })

            current_pos = end_pos

        return messages

    def render(self, template: PromptTemplate, input_values: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
        """根据输入变量渲染模板消息。"""
        variables = {}
        if template.input_variables:
            variables.update(template.input_variables)
        if input_values:
            variables.update(input_values)

        rendered_messages = []
        for message in template.messages:
            rendered_content = self._replace_variables(message["content"], variables)
            rendered_messages.append({
                "role": message["role"],
                "content": rendered_content
            })

        return rendered_messages

    def _replace_variables(self, content: str, variables: Dict[str, str]) -> str:
        """Replace variables in content with their Jinja2."""
        from jinja2 import Template, TemplateSyntaxError
        try:
            template = Template(content)
            return template.render(**variables)
        except TemplateSyntaxError as e:
            logger.warning(f"模板语法错误: {e}")
            return content

    def _parse_frontmatter(self, content: str) -> Tuple[dict, str]:
        """Parse frontmatter and content."""
        try:
            post = frontmatter.loads(content)
            if not post.metadata:
                raise ValueError("No metadata found in template")
            return post.metadata, post.content.strip()
        except Exception as e:
            raise ValueError(f"Invalid frontmatter: {e}")
