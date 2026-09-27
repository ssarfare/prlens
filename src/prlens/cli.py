from urllib.parse import urlparse

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


@app.callback()
def main():
    """PRLens - AI-powered pull request reviewer."""
    pass


if __name__ == "__main__":
    app()


