import os
from langchain.chat_models import init_chat_model
from pr_agent.model import AgentOutput

class PrAgent:
    def __init__(self, model: str, pr_prompt: str):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = init_chat_model(model)
        self.pr_prompt = pr_prompt

    def ask(self, pr: str) -> AgentOutput:
        response = self.model.invoke([
            {
                "role": "system",
                "content": self.pr_prompt
            },
            {
                "role": "user",
                "content": pr
            }
        ])
        output = AgentOutput(
            review=response.text,
            usage=response.usage_metadata
        )
        return output
    