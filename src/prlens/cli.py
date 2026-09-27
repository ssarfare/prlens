from urllib.parse import urlparse
from prlens.github_client import GitHubClient


import typer

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
        raise ValueError("Invalid GitHub PR number")

    return owner, repo, pr_number


@app.command()
def review(pr_url: str):
    owner, repo, pr_number = parse_pr_url(pr_url)

    typer.echo(f"Owner: {owner}")
    typer.echo(f"Repository: {repo}")
    typer.echo(f"PR: {pr_number}")

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

    typer.echo(f"Diff size: {len(diff)} characters")



@app.callback()
def main():
    """PRLens - AI-powered pull request reviewer."""
    pass


if __name__ == "__main__":
    app()


