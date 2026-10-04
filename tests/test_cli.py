from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from prlens.cli import app, parse_pr_url
from prlens.review_models import Finding, ReviewResult

runner = CliRunner()


def test_parse_valid_pr_url():
    owner, repo, pr_number = parse_pr_url("https://github.com/openai/openai-python/pull/123")

    assert owner == "openai"
    assert repo == "openai-python"
    assert pr_number == 123


def test_parse_pr_url_with_trailing_slash():
    owner, repo, pr_number = parse_pr_url("https://github.com/openai/openai-python/pull/123/")

    assert owner == "openai"
    assert repo == "openai-python"
    assert pr_number == 123


def test_reject_non_github_url():
    with pytest.raises(ValueError):
        parse_pr_url("https://example.com/openai/openai-python/pull/123")


def test_reject_github_issue_url():
    with pytest.raises(ValueError):
        parse_pr_url("https://github.com/openai/openai-python/issues/123")


def test_parse_rejects_invalid_pr_number():
    with pytest.raises(
        ValueError,
        match="Invalid GitHub PR number",
    ):
        parse_pr_url("https://github.com/openai/openai-python/pull/not-a-number")


@patch("prlens.cli.estimate_input_tokens", return_value=500)
@patch("prlens.cli.build_review_prompt", return_value="Review this diff")
@patch("prlens.cli.parse_diff", return_value=[])
@patch("prlens.cli.GitHubClient")
@patch("prlens.cli.LLMClient")
def test_review_renders_structured_findings(
    mock_llm_client,
    mock_github_client,
    mock_parse_diff,
    mock_build_review_prompt,
    mock_estimate_input_tokens,
):
    github_client = mock_github_client.return_value

    github_client.get_pull_request.return_value = {
        "title": "Test PR",
        "user": {"login": "test-user"},
        "state": "open",
        "changed_files": 1,
    }

    github_client.get_pull_request_diff.return_value = "diff"

    mock_llm_client.return_value.complete.return_value = ReviewResult(
        overall_status="NEEDS_ATTENTION",
        summary="The pull request needs attention.",
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

    result = runner.invoke(
        app,
        [
            "review",
            "https://github.com/test/repo/pull/1",
            "--model",
            "gemini/test-model",
        ],
        input="y\n",
    )

    assert result.exit_code == 0
    assert "NEEDS ATTENTION" in result.output
    assert "The pull request needs attention." in result.output
    assert "MEDIUM" in result.output
    assert "testing" in result.output
    assert "example.py:10" in result.output
    assert "Missing test coverage." in result.output
    assert "Add a unit test." in result.output
    assert "Testing Gaps" in result.output
    assert "API key propagation" in result.output


@patch("prlens.cli.estimate_input_tokens", return_value=500)
@patch("prlens.cli.build_review_prompt", return_value="Review this diff")
@patch("prlens.cli.parse_diff", return_value=[])
@patch("prlens.cli.GitHubClient")
@patch("prlens.cli.LLMClient")
def test_review_renders_finding_without_line_number(
    mock_llm_client,
    mock_github_client,
    mock_parse_diff,
    mock_build_review_prompt,
    mock_estimate_input_tokens,
):
    github_client = mock_github_client.return_value

    github_client.get_pull_request.return_value = {
        "title": "Test PR",
        "user": {"login": "test-user"},
        "state": "open",
        "changed_files": 1,
    }

    github_client.get_pull_request_diff.return_value = "diff"

    mock_llm_client.return_value.complete.return_value = ReviewResult(
        overall_status="NEEDS_ATTENTION",
        summary="Review summary.",
        findings=[
            Finding(
                severity="MEDIUM",
                category="correctness",
                file="example.py",
                line=None,
                description="Concrete correctness issue.",
                recommendation="Fix the issue.",
            )
        ],
        testing_gaps=[],
    )

    result = runner.invoke(
        app,
        [
            "review",
            "https://github.com/test/repo/pull/1",
            "--model",
            "gemini/test-model",
        ],
        input="y\n",
    )

    assert result.exit_code == 0
    assert "example.py" in result.output
    assert "example.py:" not in result.output


@patch("prlens.cli.estimate_input_tokens", return_value=500)
@patch("prlens.cli.build_review_prompt", return_value="Review this diff")
@patch("prlens.cli.parse_diff", return_value=[])
@patch("prlens.cli.GitHubClient")
@patch("prlens.cli.LLMClient")
def test_review_renders_clean_result(
    mock_llm_client,
    mock_github_client,
    mock_parse_diff,
    mock_build_review_prompt,
    mock_estimate_input_tokens,
):
    github_client = mock_github_client.return_value

    github_client.get_pull_request.return_value = {
        "title": "Test PR",
        "user": {"login": "test-user"},
        "state": "open",
        "changed_files": 1,
    }

    github_client.get_pull_request_diff.return_value = "diff"

    mock_llm_client.return_value.complete.return_value = ReviewResult(
        overall_status="LOOKS_GOOD",
        summary="Looks good — no critical or important issues found.",
        findings=[],
        testing_gaps=[],
    )

    result = runner.invoke(
        app,
        [
            "review",
            "https://github.com/test/repo/pull/1",
            "--model",
            "gemini/test-model",
        ],
        input="y\n",
    )

    assert result.exit_code == 0
    assert "LOOKS GOOD" in result.output
    assert "no critical or important issues found" in result.output
    assert "Findings" not in result.output
    assert "Testing Gaps" not in result.output


@patch("prlens.cli.estimate_input_tokens", return_value=500)
@patch("prlens.cli.build_review_prompt", return_value="Review this diff")
@patch("prlens.cli.parse_diff", return_value=[])
@patch("prlens.cli.GitHubClient")
@patch("prlens.cli.LLMClient")
def test_review_cancel_does_not_call_model(
    mock_llm_client,
    mock_github_client,
    mock_parse_diff,
    mock_build_review_prompt,
    mock_estimate_input_tokens,
):
    github_client = mock_github_client.return_value

    github_client.get_pull_request.return_value = {
        "title": "Test PR",
        "user": {"login": "test-user"},
        "state": "open",
        "changed_files": 1,
    }

    github_client.get_pull_request_diff.return_value = "diff"

    result = runner.invoke(
        app,
        [
            "review",
            "https://github.com/test/repo/pull/1",
            "--model",
            "gemini/test-model",
        ],
        input="n\n",
    )

    assert result.exit_code != 0
    mock_llm_client.return_value.complete.assert_not_called()


@patch("prlens.cli.estimate_input_tokens", return_value=500)
@patch("prlens.cli.build_review_prompt", return_value="Review this diff")
@patch("prlens.cli.parse_diff", return_value=[])
@patch("prlens.cli.GitHubClient")
@patch("prlens.cli.LLMClient")
def test_review_handles_model_failure(
    mock_llm_client,
    mock_github_client,
    mock_parse_diff,
    mock_build_review_prompt,
    mock_estimate_input_tokens,
):
    github_client = mock_github_client.return_value

    github_client.get_pull_request.return_value = {
        "title": "Test PR",
        "user": {"login": "test-user"},
        "state": "open",
        "changed_files": 1,
    }

    github_client.get_pull_request_diff.return_value = "diff"

    mock_llm_client.return_value.complete.side_effect = RuntimeError(
        "Model gemini/test-model is temporarily unavailable."
    )

    result = runner.invoke(
        app,
        [
            "review",
            "https://github.com/test/repo/pull/1",
            "--model",
            "gemini/test-model",
        ],
        input="y\n",
    )

    assert result.exit_code == 1
    assert "Review failed: Model gemini/test-model is temporarily unavailable." in result.output


def test_review_requires_model():
    result = runner.invoke(
        app,
        [
            "review",
            "https://github.com/test/repo/pull/1",
        ],
    )

    assert result.exit_code != 0
    assert "model" in result.output.lower()
