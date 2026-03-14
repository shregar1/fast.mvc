#!/usr/bin/env bash
#
# Create a public GitHub repo for each fastmvc_* package and push.
# Requires: GitHub CLI (gh) installed and logged in.
#
# Install gh: https://cli.github.com/
#   brew install gh   # macOS
#   gh auth login
#
# Usage: from repo root, run:
#   ./scripts/publish_packages_to_github.sh
# Or with a specific GitHub username:
#   GITHUB_USER=yourname ./scripts/publish_packages_to_github.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# Packages live in sibling directory fastmvc_packages (or in-repo packages/ for initial setup)
PACKAGES_DIR="${FASTMVC_PACKAGES_DIR:-$REPO_ROOT/../fastmvc_packages}"
if [ ! -d "$PACKAGES_DIR" ]; then
  PACKAGES_DIR="$REPO_ROOT/packages"
fi

# Optional: set your GitHub username (otherwise gh will use the authenticated user)
GITHUB_USER="${GITHUB_USER:-}"

if ! command -v gh &>/dev/null; then
  echo "GitHub CLI (gh) is not installed. Install it from https://cli.github.com/"
  echo "  macOS: brew install gh"
  echo "  Then: gh auth login"
  exit 1
fi

if ! gh auth status &>/dev/null; then
  echo "Not logged in to GitHub. Run: gh auth login"
  exit 1
fi

if [ -z "$GITHUB_USER" ]; then
  GITHUB_USER="$(gh api user --jq .login)"
  echo "Using GitHub user: $GITHUB_USER"
fi

for pkg in fastmvc_core fastmvc_dashboards fastmvc_channels fastmvc_notifications fastmvc_kafka fastmvc_webrtc; do
  dir="$PACKAGES_DIR/$pkg"
  if [ ! -d "$dir" ]; then
    echo "Skip $pkg (directory not found)"
    continue
  fi
  echo "--- $pkg ---"
  cd "$dir"

  # Ensure we're in a git repo
  if [ ! -d .git ]; then
    git init
  fi

  # Add and commit any new files (e.g. .gitignore)
  git add -A
  if git diff --staged --quiet 2>/dev/null && git diff --quiet 2>/dev/null; then
    echo "  Nothing to commit."
  else
    git commit -m "Add .gitignore and package files for publishing"
  fi

  # Create public repo on GitHub and push
  if git remote get-url origin &>/dev/null; then
    echo "  Remote origin already set. Pushing..."
    git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null || true
  else
    echo "  Creating GitHub repo $GITHUB_USER/$pkg (public) and pushing..."
    if gh repo create "$pkg" --public --source=. --remote=origin --push --description "FastMVC package: $pkg"; then
      :
    else
      echo "  Repo may already exist. Adding remote and pushing..."
      git remote add origin "https://github.com/$GITHUB_USER/$pkg.git" 2>/dev/null || true
      git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null || true
    fi
  fi

  echo "  Done: https://github.com/$GITHUB_USER/$pkg"
  echo ""
done

echo "All packages published to https://github.com/$GITHUB_USER/"
