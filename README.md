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
      - uses: actions/checkout@v2
      - name: PR annotator with ruff
        uses: EnriqueSoria/annotate_pr_with_ruff@vX.X.X  # <-- Choose a release version
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Images
Here's an screenshot of what it can do:

![imagen](https://user-images.githubusercontent.com/7394684/201521001-9baafdb0-f4c0-4860-b5ad-1a97ec9abb7e.png)


## Credits
I've used [typilus/typilus-action](https://github.com/typilus/typilus-action) as a template for creating this action, which is MIT Licensed. 
