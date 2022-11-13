import os
from typing import Sequence

import requests

from .ruff import RuffError
from .ruff import run_cli


def get_diff(owner: str, repo: str, pr_number: int) -> str:
    return run_cli(
        "gh",
        "pr",
        "diff",
        str(pr_number),
        "--repo",
        f"{owner}/{repo}",
    ).strip()


def get_last_commit(owner: str, repo: str, pr_number: int) -> str:
    return run_cli(
        "gh",
        "pr",
        "view",
        str(pr_number),
        "--repo",
        f"{owner}/{repo}",
        "--json",
        "commits",
        "--jq",
        ".commits[].oid",
    ).strip()


def submit_review(owner: str, repo: str, pr_number: int, review_message:str, errors: Sequence[RuffError]):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews"

    body = dict(
        commit_id=get_last_commit(owner, repo, pr_number),
        body=review_message,
        event="COMMENT",
        comments=[
            {
                "path": error.file,
                "position": error.line_number,
                "body": error.message,
            }
            for error in errors
        ],
    )
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    }
    response = requests.post(
        url=url,
        headers=headers,
        json=body,
    )
    print(f">>> post({url}, headers={headers}, body={body})")
    print(response.status_code, response.json())
