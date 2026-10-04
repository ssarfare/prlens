from unittest.mock import MagicMock, patch

import pytest

import prlens.llm_client as llm_client_module
from prlens.llm_client import LLMClient


@patch("prlens.llm_client.completion")
def test_complete_returns_structured_review(mock_completion):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = """
    {
      "overall_status": "NEEDS_ATTENTION",
      "summary": "Adds API key support.",
      "findings": [
        {
          "severity": "MEDIUM",
          "category": "testing",
          "file": "example.py",
          "line": 10,
          "description": "Missing test coverage.",
          "recommendation": "Add a unit test."
        }
      ],
      "testing_gaps": ["API key propagation"]
    }
    """

    mock_completion.return_value = mock_response

    client = LLMClient(model="gemini/test-model")

    result = client.complete("Review this diff")

    assert result.overall_status == "NEEDS_ATTENTION"
    assert result.summary == "Adds API key support."
    assert len(result.findings) == 1
    assert result.findings[0].severity == "MEDIUM"

    mock_completion.assert_called_once()

    call_kwargs = mock_completion.call_args.kwargs

    assert call_kwargs["model"] == "gemini/test-model"
    assert call_kwargs["messages"] == [
        {
            "role": "user",
            "content": "Review this diff",
        }
    ]

    assert call_kwargs["response_format"]["type"] == "json_schema"
    assert call_kwargs["response_format"]["json_schema"]["name"] == "pr_review"


@patch("prlens.llm_client.completion")
def test_complete_rejects_empty_response(mock_completion):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = None

    mock_completion.return_value = mock_response

    client = LLMClient(model="gemini/test-model")

    with pytest.raises(ValueError, match="LLM returned an empty response"):
        client.complete("Review this diff")


@patch("prlens.llm_client.completion")
def test_complete_rejects_invalid_schema(mock_completion):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = """
    {
      "overall_status": "INVALID",
      "summary": "Bad schema",
      "findings": [],
      "testing_gaps": []
    }
    """

    mock_completion.return_value = mock_response

    client = LLMClient(model="gemini/test-model")

    with pytest.raises(
        ValueError,
        match="LLM response did not match review schema",
    ):
        client.complete("Review this diff")


@patch("prlens.llm_client.completion")
def test_complete_handles_authentication_error(mock_completion, monkeypatch):
    class FakeAuthenticationError(Exception):
        pass

    monkeypatch.setattr(
        llm_client_module,
        "AuthenticationError",
        FakeAuthenticationError,
    )

    mock_completion.side_effect = FakeAuthenticationError("Invalid API key")

    client = LLMClient(model="gemini/test-model")

    with pytest.raises(
        RuntimeError,
        match="Authentication failed for model gemini/test-model",
    ):
        client.complete("Review this diff")


@patch("prlens.llm_client.completion")
def test_complete_handles_rate_limit_error(mock_completion, monkeypatch):
    class FakeRateLimitError(Exception):
        pass

    monkeypatch.setattr(
        llm_client_module,
        "RateLimitError",
        FakeRateLimitError,
    )

    mock_completion.side_effect = FakeRateLimitError("Rate limit exceeded")

    client = LLMClient(model="gemini/test-model")

    with pytest.raises(
        RuntimeError,
        match="Rate limit reached for model gemini/test-model",
    ):
        client.complete("Review this diff")


@patch("prlens.llm_client.completion")
def test_complete_handles_service_unavailable(mock_completion, monkeypatch):
    class FakeServiceUnavailableError(Exception):
        pass

    monkeypatch.setattr(
        llm_client_module,
        "ServiceUnavailableError",
        FakeServiceUnavailableError,
    )

    mock_completion.side_effect = FakeServiceUnavailableError("Service unavailable")

    client = LLMClient(model="gemini/test-model")

    with pytest.raises(
        RuntimeError,
        match="Model gemini/test-model is temporarily unavailable",
    ):
        client.complete("Review this diff")


@patch("prlens.llm_client.completion")
def test_complete_handles_connection_error(mock_completion, monkeypatch):
    class FakeAPIConnectionError(Exception):
        pass

    monkeypatch.setattr(
        llm_client_module,
        "APIConnectionError",
        FakeAPIConnectionError,
    )

    mock_completion.side_effect = FakeAPIConnectionError("Connection failed")

    client = LLMClient(model="gemini/test-model")

    with pytest.raises(
        RuntimeError,
        match="Could not connect to the provider for model gemini/test-model",
    ):
        client.complete("Review this diff")
