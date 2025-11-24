# Ghost Files Finder

Desktop app for exploring files that match rclone filter rules. Built with PySide6 and managed with `uv`.

**Author:** Rich Lewis (@RichLewis007)

## Features

### Core Functionality

- **Scan & Match**: Load rclone filter lists and scan a chosen root directory for matches
- **Interactive Results**: Results pane highlights matched files with rule metadata and color-coded rule matching
- **Rule Filtering**: Multi-select rule filters in sidebar to show only files matching specific rules
- **Search**: Real-time text search across visible results with immediate filtering

### File Management

- **Context Actions**: Right-click context menu to open matches in Finder/File Explorer or delete files safely to Trash
- **Export**: Export results in multiple formats (CSV, JSON, JSONL, or plain text) with options for visible-only or full results
- **Batch Operations**: Select multiple files for deletion with confirmation dialogs

### User Interface

- **Scan Progress Dialog**: Modal dialog showing detailed scan progress with file counts, size of matches, elapsed time, and long path support
- **Pause/Resume**: Pause and resume scans while preserving progress
- **Column Sorting**: Sort by Name, Full Path, Size, or Modified date with case-insensitive options
- **Settings Dialog**: Configure debug logging, UI sounds, and completion sounds
- **Persistent Settings**: Remembers last-used root directory and filter file paths

### Performance & Reliability

- **Optimized Performance**: Handles large datasets with thousands of files and deeply nested directories (500+ children per node)
- **Background Processing**: Non-blocking scan operations with progress updates
- **Smart Text Elision**: Status bar and dialogs handle long file paths without causing window resizing issues

## Architecture Highlights

- **Single-responsibility threads**: UI stays on the main thread; scanning, deletion, and export run on worker threads with Qt signals for progress/cancellation.
- **Tree model built for scale**: `PathTreeModel` batches inserts and avoids costly full-column auto-resize; `TreeFilterProxyModel` handles rule filters and case-insensitive sorting.
- **First-match-wins rules**: `MatchEngine` applies rclone-style globs to root-relative POSIX paths, recording both the first matching rule and all secondary matches.
- **Persistent settings**: `SettingsStore` wraps `QSettings` + `platformdirs` to remember geometry, recent roots/filter files, export defaults, and sound preferences.

## Development

1. Install uv: <https://github.com/astral-sh/uv>
1. Sync dependencies (including dev extras):
   ```
   uv sync --extra dev
   ```
1. Enable git hooks:
   ```
   uv run --extra dev pre-commit install
   ```
1. Run quality checks:
   ```
   uv run --extra dev nox
   ```
1. Launch the app in dev mode:
   ```
   uv run ghost-files-finder
   ```

## Tests

Run a test to detect all types of files and folders listed in the rclone filter file:

```
uv run --extra dev pytest tests/integration/test_scanner_finds_excluded_patterns.py
```

## Status

Core scanning workflow, rule loading, and results interactions are in place.
Performance optimizations ensure smooth operation with large datasets (nodes with 500+ children).
