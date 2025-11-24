#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

# Remove dist directory to avoid symlink conflicts from previous builds
if [[ -d "dist" ]]; then
    echo "Removing existing dist directory..."
    rm -rf dist
fi

# Remove build directory to ensure clean build
if [[ -d "build" ]]; then
    echo "Removing existing build directory..."
    rm -rf build
fi

uv run --extra dev pyinstaller --clean --noconfirm ghost_files_finder.spec

echo "PyInstaller build complete. Dist output is located in $(realpath dist)."
