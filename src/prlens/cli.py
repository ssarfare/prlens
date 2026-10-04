from urllib.parse import urlparse

import typer

from prlens.diff_parser import parse_diff
from prlens.github_client import GitHubClient

app = typer.Typer()


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
def review(pr_url: str):
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


@app.callback()
def main():
    """PRLens - AI-powered pull request reviewer."""
    pass


if __name__ == "__main__":
    app()
