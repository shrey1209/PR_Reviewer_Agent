from pydantic import BaseModel

class FileChange(BaseModel):
    file_name: str
    changes: int
    status: str
    additions: int
    deletions: int
    diff: str | None = None

class PullRequest(BaseModel):
    number: int
    repo: str
    title: str
    url: str
    changed_files: int
    files: list[FileChange]