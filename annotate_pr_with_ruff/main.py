import json
import os

print(f"{os.environ['GITHUB_EVENT_PATH']=}")

from changeutils import get_changed_files
from github_utils import get_diff
from ruff_utils import ruff

print("imports finished")

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

    print(f"::set-output name=num_errors::{len(ruff_errors)}")

    # Submit review
    for ruff_error in ruff_errors:
        print(
            f"::error file={ruff_error.file},line={ruff_error.line_number}::{ruff_error.message}"
        )


if __name__ == "__main__":
    main()
