from typing import Literal

from pydantic import BaseModel

Severity = Literal["HIGH", "MEDIUM", "LOW"]

OverallStatus = Literal[
    "LOOKS_GOOD",
    "NEEDS_ATTENTION",
    "CHANGES_REQUIRED",
]

Category = Literal[
    "correctness",
    "performance",
    "concurrency",
    "security",
    "error-handling",
    "testing",
    "maintainability",
]


class Finding(BaseModel):
    severity: Severity
    category: Category
    file: str
    line: int | None = None
    description: str
    recommendation: str


class ReviewResult(BaseModel):
    overall_status: OverallStatus
    summary: str
    findings: list[Finding]
    testing_gaps: list[str]
