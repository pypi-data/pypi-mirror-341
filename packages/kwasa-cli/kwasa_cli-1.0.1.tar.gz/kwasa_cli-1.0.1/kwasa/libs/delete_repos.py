import requests
from dotenv import load_dotenv
import os

load_dotenv()


token = os.environ.get("")

username = os.environ.get("")


def delete_repositories(repos: list[str] | str = []) -> None:
    api_url = "https://api.github.com/repos/{}/{}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    if isinstance(repos, list):
        for repo in repos_to_delete:
            delete_repo(api_url, repo, headers)
    else:
        delete_repo(api_url, repo, headers)


def delete_repo(api_url: str, repo: str, headers: dict[str, str]) -> None:
    repo_url = api_url.format(username, repo)
    response = requests.delete(repo_url, headers=headers)

    if response.status_code == 204:
        print(f"Successfully deleted: {repo}")
    else:
        print(f"Failed to delete {repo}. Status code: {response.status_code}")
        print(response.json())


if __name__ == "__main__":
    repos_to_delete = [
        "example",
    ]
    delete_repositories(repos_to_delete)
