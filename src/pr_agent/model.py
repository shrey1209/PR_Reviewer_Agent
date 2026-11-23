from pydantic import BaseModel, computed_field

class FileChange(BaseModel):
    file_name: str
    changes: int
    status: str
    additions: int
    deletions: int
    diff: str | None = None

    @computed_field
    @property
    def total_changes(self) -> int:
        return self.additions + self.deletions

class PullRequest(BaseModel):
    number: int
    repo: str
    title: str
    url: str
    files: list[FileChange]
    description: str | None = None

    @computed_field
    @property
    def changed_files(self) -> int:
        return len(self.files)
