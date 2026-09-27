import httpx

GITHUB_API_URL = "https://api.github.com"


class GitHubClient:
    def get_pull_request(
        self,
        owner: str,
        repo: str,
        pr_number: int,
    ) -> dict:
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}"

        response = httpx.get(url)
        response.raise_for_status()

        return response.json()

    def get_pull_request_diff(
        self,
        owner: str,
        repo: str,
        pr_number: int,
    ) -> str:
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}"

        response = httpx.get(
            url,
            headers={"Accept": "application/vnd.github.v3.diff"},
        )

        response.raise_for_status()

        return response.text
