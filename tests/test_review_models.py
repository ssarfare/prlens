import pytest
from pydantic import ValidationError

from prlens.review_models import Finding, ReviewResult


def test_review_result():
    review = ReviewResult(
        overall_status="NEEDS_ATTENTION",
        summary="Adds API key support.",
        findings=[
            Finding(
                severity="MEDIUM",
                category="testing",
                file="example.py",
                line=10,
                description="Missing test coverage.",
                recommendation="Add a unit test.",
            )
        ],
        testing_gaps=["API key propagation"],
    )

    assert review.overall_status == "NEEDS_ATTENTION"
    assert review.summary == "Adds API key support."
    assert review.findings[0].severity == "MEDIUM"
    assert review.findings[0].category == "testing"
    assert review.testing_gaps == ["API key propagation"]


def test_rejects_invalid_severity():
    with pytest.raises(ValidationError):
        Finding(
            severity="CRITICAL",
            category="testing",
            file="example.py",
            description="Issue",
            recommendation="Fix it",
        )


def test_rejects_invalid_status():
    with pytest.raises(ValidationError):
        ReviewResult(
            overall_status="MAYBE",
            summary="Invalid",
            findings=[],
            testing_gaps=[],
        )


def test_rejects_invalid_category():
    with pytest.raises(ValidationError):
        Finding(
            severity="LOW",
            category="style",
            file="example.py",
            description="Issue",
            recommendation="Fix it",
        )
