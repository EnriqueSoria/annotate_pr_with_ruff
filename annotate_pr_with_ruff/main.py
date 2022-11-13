#!/bin/python
import json
import os

from .changeutils import get_changed_files
from .github_utils import get_diff
from .github_utils import submit_review
from .ruff import ruff


def main():
    with open(os.environ["GITHUB_EVENT_PATH"]) as f:
        event_data = json.load(f)

    owner, repo = event_data["pull_request"]["head"]["repo"]["full_name"].split("/")
    pr_number = event_data["pull_request"]["number"]

    # Check which files have changed
    diff = get_diff(owner=owner, repo=repo, pr_number=pr_number)
    changed_files = get_changed_files(diff)

    # Get errors from ruff
    ruff_errors = ruff()

    # Filter only errors on lines that have been changed
    ruff_errors = [
        ruff_error
        for ruff_error in ruff_errors
        if ruff_error.line_number in changed_files.get(f"/{ruff_error.file}", {})
    ]

    submit_review(owner=owner, repo=repo, pr_number=pr_number, errors=ruff_errors)


if __name__ == "__main__":
    main()
