
from pathlib import Path

class GetSystemPrompt:
    def __init__(self, prompt_path: Path):
        self.prompt_path = prompt_path

    def get_prompt(self) -> str:
        return self.prompt_path.read_text(encoding="utf-8")