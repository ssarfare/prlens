from urllib.parse import urlparse

import typer

from prlens.diff_parser import parse_diff
from prlens.github_client import GitHubClient
from prlens.llm_client import LLMClient
from prlens.prompt_builder import build_review_prompt
from prlens.token_estimator import estimate_input_tokens

app = typer.Typer()

STATUS_ICONS = {
    "LOOKS_GOOD": "✅",
    "NEEDS_ATTENTION": "⚠️",
    "CHANGES_REQUIRED": "❌",
}

SEVERITY_ICONS = {
    "HIGH": "🔴",
    "MEDIUM": "🟠",
    "LOW": "🟡",
}


def parse_pr_url(url: str) -> tuple[str, str, int]:
    parsed = urlparse(url.strip())

    if parsed.netloc != "github.com":
        raise ValueError("Invalid GitHub PR URL")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 4 or parts[2] != "pull":
        raise ValueError("Invalid GitHub PR URL")

    owner = parts[0]
    repo = parts[1]

    try:
        pr_number = int(parts[3])
    except ValueError:
        raise ValueError("Invalid GitHub PR number") from None

    return owner, repo, pr_number


@app.command()
def review(
    pr_url: str,
    model: str = typer.Option(
        ...,
        "--model",
        "-m",
        help="LLM model to use, for example anthropic/claude-sonnet",
    ),
):
    owner, repo, pr_number = parse_pr_url(pr_url)

    client = GitHubClient()
    pull_request = client.get_pull_request(owner, repo, pr_number)

    typer.echo(f"Title: {pull_request['title']}")
    typer.echo(f"Author: {pull_request['user']['login']}")
    typer.echo(f"State: {pull_request['state']}")
    typer.echo(f"Changed files: {pull_request['changed_files']}")

    # Fetch PR diff
    diff = client.get_pull_request_diff(
        owner,
        repo,
        pr_number,
    )

    changed_files = parse_diff(diff)
    typer.echo()
    typer.echo(f"Changed files parsed: {len(changed_files)}")

    for changed_file in changed_files:
        typer.echo(f"- {changed_file.path} ({len(changed_file.sections)} diff section(s))")

    prompt = build_review_prompt(changed_files)

    input_tokens = estimate_input_tokens(
        model=model,
        prompt=prompt,
    )

    typer.echo()
    typer.echo(f"Model: {model}")
    typer.echo(f"Estimated input tokens: {input_tokens:,}")

    if not typer.confirm("Continue with review?"):
        raise typer.Abort()

    client = LLMClient(model=model)

    try:
        result = client.complete(prompt)
    except (RuntimeError, ValueError) as error:
        typer.echo()
        typer.echo(f"Review failed: {error}", err=True)
        raise typer.Exit(code=1) from None

    status_icon = STATUS_ICONS[result.overall_status]

    typer.echo()
    typer.echo(f"{status_icon} {result.overall_status.replace('_', ' ')}")

    typer.echo()
    typer.echo("Summary")
    typer.echo("-------")
    typer.echo(result.summary)

    if result.findings:
        typer.echo()
        typer.echo("Findings")
        typer.echo("--------")

        for finding in result.findings:
            severity_icon = SEVERITY_ICONS[finding.severity]

            location = finding.file

            if finding.line is not None:
                location = f"{location}:{finding.line}"

            typer.echo()
            typer.echo(f"{severity_icon} {finding.severity} | {finding.category} | {location}")
            typer.echo(finding.description)
            typer.echo(f"💡 {finding.recommendation}")

    if result.testing_gaps:
        typer.echo()
        typer.echo("🧪 Testing Gaps")
        typer.echo("---------------")

        for gap in result.testing_gaps:
            typer.echo(f"- {gap}")


@app.callback()
def main():
    """PRLens - AI-powered pull request reviewer."""
    pass


if __name__ == "__main__":
    app()
