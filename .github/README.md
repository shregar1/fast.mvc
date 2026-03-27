# `.github`

## What this folder does

The **`.github`** directory holds **GitHub-specific automation** for this repository: **workflow** definitions (CI/CD), issue and pull request **templates**, and optional **CODEOWNERS** or **dependabot** configuration.

It does **not** ship with your Python package to PyPI; it only affects **behavior on GitHub** when you push code or open issues/PRs.

## Typical contents

| Item | Purpose |
|------|---------|
| `workflows/` | YAML pipelines: tests, lint, release, security scans |
| `ISSUE_TEMPLATE/` | Structured bug reports and feature requests |
| `pull_request_template.md` | Default PR description checklist (if present) |

## Practices

1. Keep workflows **fast** and **cached** where possible.  
2. **Pin** action versions (`uses: actions/checkout@v4`) for reproducibility.  
3. Align workflow **Python version** with `pyproject.toml` / production.  
4. Document any **secrets** required in repo settings (never commit secrets).
