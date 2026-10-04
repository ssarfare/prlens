from litellm import completion
from litellm.exceptions import (
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    ServiceUnavailableError,
)
from pydantic import ValidationError

from prlens.review_models import ReviewResult


class LLMClient:
    """Model-agnostic LLM client backed by LiteLLM."""

    def __init__(self, model: str):
        self.model = model

    def complete(self, prompt: str) -> ReviewResult:
        try:
            response = completion(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "pr_review",
                        "strict": True,
                        "schema": ReviewResult.model_json_schema(),
                    },
                },
            )
        except AuthenticationError as error:
            raise RuntimeError(f"Authentication failed for model {self.model}.") from error
        except RateLimitError as error:
            raise RuntimeError(
                f"Rate limit reached for model {self.model}. Try again later."
            ) from error
        except ServiceUnavailableError as error:
            raise RuntimeError(
                f"Model {self.model} is temporarily unavailable. Try again later."
            ) from error
        except APIConnectionError as error:
            raise RuntimeError(
                f"Could not connect to the provider for model {self.model}."
            ) from error

        content = response.choices[0].message.content

        if not content:
            raise ValueError("LLM returned an empty response")

        try:
            return ReviewResult.model_validate_json(content)
        except ValidationError as error:
            raise ValueError("LLM response did not match review schema") from error
