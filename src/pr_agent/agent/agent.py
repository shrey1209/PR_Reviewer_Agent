import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from pr_agent.model import OverallFinding, AgentOutput

class PrAgent:
    def __init__(self, model: str, pr_prompt: str):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model = init_chat_model(model)
        self.pr_prompt = pr_prompt
        self.agent = create_agent(
            model = self.model,
            system_prompt=self.pr_prompt,
            response_format= OverallFinding
    )

    def ask(self, pr: str) -> AgentOutput:
        response = self.agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": pr
                }
            ]
        })
        return AgentOutput(
            review=response["structured_response"],
            usage=response["messages"][-1].usage_metadata
        )
    