from litellm import token_counter


def estimate_input_tokens(
    model: str,
    prompt: str,
) -> int:
    return token_counter(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
