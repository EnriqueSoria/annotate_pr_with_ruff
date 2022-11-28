import logging

from ruff_utils import run_cli

logger = logging.getLogger(__name__)


def get_diff(owner: str, repo: str, pr_number: int) -> str:
    return run_cli(
        "gh",
        "pr",
        "diff",
        str(pr_number),
        "--repo",
        f"{owner}/{repo}",
        "--color",
        "never"
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