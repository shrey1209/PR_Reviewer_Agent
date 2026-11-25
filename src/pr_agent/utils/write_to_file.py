from pathlib import Path

class FileWriter:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def write(self, content: str) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(content)