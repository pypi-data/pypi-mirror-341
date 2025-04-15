---
metadata:
  name: translator
  version: 1.0.0
  description: A template for translating text to different languages
provider:
  name: openai
  base_url: http://localhost:10240
  path: /chat/completions
  api_key: sk-...
  timeout: 30
generation_config:
  model: "mlx-community/Qwen2.5-14B-Instruct-4bit"
  temperature: 0.3
  max_completion_tokens: 1000
input_variables:
  target_lang: English  # 默认语言
  tone: 专业        # 语气（正式/非正式）
---

system
---
You are an experienced and intelligent food recognition assistant with computer vision skills and a polite and practical nutrition assistant function. Your task is to analyze images or descriptions to identify all foods, packaged foods, or beverage items and accurately calculate their nutritional information.

user
---
500ml 牛奶，300ml咖啡
