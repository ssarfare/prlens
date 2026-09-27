from prlens.github_client import GitHubClient


def test_get_pull_request(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url="https://api.github.com/repos/openai/openai-python/pulls/123",
        json={
            "title": "Test PR",
            "state": "open",
            "changed_files": 2,
            "user": {
                "login": "octocat"
            }
        },
        status_code=200,
    )

    client = GitHubClient()

    result = client.get_pull_request(
        owner="openai",
        repo="openai-python",
        pr_number=123,
    )

    assert result["title"] == "Test PR"
    assert result["state"] == "open"
    assert result["changed_files"] == 2
    assert result["user"]["login"] == "octocat"

def test_get_pull_request_diff(httpx_mock):
    expected_diff = """diff --git a/example.py b/example.py
                    index 1234567..7654321 100644
                    --- a/example.py
                    +++ b/example.py
                    @@ -1,2 +1,2 @@
                    -print("old")
                    +print("new")
                    """

    httpx_mock.add_response(
        method="GET",
        url="https://api.github.com/repos/openai/openai-python/pulls/123",
        headers={
            "Content-Type": "application/vnd.github.v3.diff"
        },
        text=expected_diff,
        status_code=200,
    )

    client = GitHubClient()

    result = client.get_pull_request_diff(
        owner="openai",
        repo="openai-python",
        pr_number=123,
    )

    assert result == expected_diff
