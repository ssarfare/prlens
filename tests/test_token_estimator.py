from unittest.mock import patch

from prlens.token_estimator import estimate_input_tokens


@patch("prlens.token_estimator.token_counter")
def test_estimate_input_tokens(mock_token_counter):
    mock_token_counter.return_value = 1234

    result = estimate_input_tokens(
        model="anthropic/test-model",
        prompt="Review this diff",
    )

    assert result == 1234

    mock_token_counter.assert_called_once_with(
        model="anthropic/test-model",
        messages=[
            {
                "role": "user",
                "content": "Review this diff",
            }
        ],
    )
