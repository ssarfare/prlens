import pytest

from prlens.cli import parse_pr_url


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
