from enum import Enum
from pydantic import BaseModel, Field, computed_field
from typing import Literal

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

class Severity(Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"

class AgentFinding(BaseModel):
    file_path: str
    line_number: int | None = None
    title: str
    review_comment: str
    evidence: str
    trigger_condition: str
    impact: str
    suggested_fix: str | None = None
    suggested_test: str | None = None
    confidence: Literal["HIGH", "MEDIUM", "LOW"]
    severity: Severity = Field(
        description=(
            "How bad the problem is. "
            "P0: exploitable security flaw, severe data loss, or widespread production outage. "
            "P1: major functional defect, significant security risk, or serious production regression. "
            "P2: reproducible defect, important reliability issue, or meaningful maintainability risk. "
            "P3: minor improvement with limited operational impact."
        )
    )
    category: Literal[
        "CORRECTNESS",
        "SECURITY",
        "PERFORMANCE",
        "ARCHITECTURE",
        "RELIABILITY",
        "MAINTAINABILITY",
        "TESTING",
        "CICD"
    ]

class OverallFinding(BaseModel):
    pr_overview: str
    findings: list[AgentFinding]
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    recommendation: Literal["APPROVE", "REQUEST_CHANGES", "NEEDS_CONTEXT"]
    review_limitations: list[str] | None = None

class AgentOutput(BaseModel):
    review: OverallFinding
    usage: dict | None = None
