import requests
from pandasai.llm.base import LLM

class OpenRouterLLM(LLM):
    def __init__(self, api_key, model="deepseek/deepseek-coder:latest"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    @property
    def type(self) -> str:
        return "openrouter"

    def call(self, prompt: str, context: dict = None, **kwargs) -> str:
        prompt_str = str(prompt)
        messages = [{"role": "user", "content": prompt_str}]
        return self.chat(messages)

    def chat(self, messages, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",  # optional
            "X-Title": "LocalTestApp"           # optional
        }

        payload = {
            "model": self.model,
            "messages": messages
        }

        response = requests.post(self.base_url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"OpenRouter API Error: {response.status_code} - {response.text}")

        return response.json()["choices"][0]["message"]["content"]
#Which SKU generated the most revenue?