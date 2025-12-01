#!/usr/bin/env bash

# Recreate the virtual environment and set up pre-commit hooks
# (One use case: if you delete the .venv directory, you can run this script to recreate it.)
#
# What this does:
# - Removes .venv - Deletes the old virtual environment
# - Recreates with uv sync --extra dev - Creates a new virtual environment and installs:
#   - All project dependencies (PySide6, etc.)
#   - All dev dependencies (pytest, ruff, mypy, pre-commit, etc.)
# - Installs pre-commit hooks - Sets up git hooks so pre-commit runs automatically on commits
# After running this, your virtual environment will be recreated and pre-commit will be configured. The hooks will run automatically when you commit.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Removing existing virtual environment..."
rm -rf .venv

echo "Creating new virtual environment with dependencies..."
uv sync --extra dev

echo "Installing pre-commit hooks..."
uv run --extra dev pre-commit install

echo ""
echo "Setup complete! Virtual environment recreated and pre-commit hooks installed."
echo ""
echo "You can now:"
echo "  - Run the app: uv run ghost-files-finder"
echo "  - Run tests: uv run --extra dev pytest"
echo "  - Run checks: uv run --extra dev nox"
