import os
from langchain.chat_models import init_chat_model

class PrAgent:
    def __init__(self, model: str, system_prompt: str):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = init_chat_model(model)
        self.system_prompt = system_prompt

    def ask(self, pr: str) -> str:
        return self.model.invoke([
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": pr
            }
        ]).text
    