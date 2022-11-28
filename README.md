# Annotate pull requests with ruff

It runs `ruff` against pull requests changed lines, and creates a review comment with them.


## Configuration
```yaml
name: 'Dependency Review'
on: [pull_request]

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so that annotate_pr_with_ruff can access it.
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10' 
      - name: Install dependencies library
        run: |
          pip install ruff
        shell: bash
      - name: annotate_pr_with_ruff
        uses: EnriqueSoria/annotate_pr_with_ruff@c226a0b09f7e8ea7f148f29c129f89399b37f03d
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

For the installation of `ruff` there are two options possible:

 - Using [install-pinned](https://github.com/install-pinned/ruff), which is safer
```yaml
      - name: Install ruff from install-pinned action
        uses: install-pinned/ruff@66c987de12929f701b73e83c82edc36050ae55a0  # Specify a version
```

- Using pip without specifying a version, which will ensure you have always the same version
```yaml
      - name: Install ruff from pypi
        run: |
          pip install ruff
```

## Images
Here's an screenshot of what it can do:

![imagen](https://user-images.githubusercontent.com/7394684/201521001-9baafdb0-f4c0-4860-b5ad-1a97ec9abb7e.png)


## Credits
I've used [typilus/typilus-action](https://github.com/typilus/typilus-action) as a template for creating this action, which is MIT Licensed. 
