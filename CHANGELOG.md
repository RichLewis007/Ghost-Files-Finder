# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fixed status bar window resizing issue when displaying long file paths during scanning
  - Implemented text elision ('to omit something') in status bar using QFontMetrics to truncate long paths dynamically
  - Added path truncation helper to limit path length before display (shows beginning and end with ellipsis)
  - Status bar now properly handles window resize events and re-elides text accordingly
  - Prevents unexpected window expansion when scanning files in deeply nested directories
- Improved scanning dialog processing events more frequently during recursive child processing, especially for nodes with 500+ children
- Added "please wait while processing" message during scan completion
- Corrected scanning dialog title/label text and ensured it wraps long source paths cleanly
- Fixed README references to the local specifications and performance notes

## [1.0.0] - 2025-11-13

### Added

- File and folder size tracking for matched items during scanning
- Size of matches display in scanning dialog and app footer with proper formatting (\<1 MB, KB, MB, TB, etc.)
- Column sorting by clicking column headers with custom sorting for Size (numeric) and Modified (chronological) columns
- Case-insensitive sorting for Name and Full Path columns
- About dialog showing on app launch with version, copyright, and license information
- macOS system menu "About Ghost Files Finder" and "Quit Ghost Files Finder" items that appear in the macOS menu bar following macOS standards
- MIT License file added to project root
- UI Sounds checkbox in results pane footer to mute/unmute all application sounds
- Version information (1.0.0) and copyright (2025 Rich Lewis) in About dialog

### Changed

- Updated application version from 0.1.0 to 1.0.0
- Improved About dialog positioning to appear on the same screen as main window
- Enhanced macOS process name setting for better dock/task switcher integration

### Fixed

- Fixed index validation errors in proxy model sorting to prevent Qt warnings
- Fixed multi-monitor positioning for About dialog and main window to launch on the last-used monitor
- Fixed case-insensitive sorting implementation for Name and Full Path columns using Qt's built-in `setSortCaseSensitivity`
- Improved About dialog timing to show after main window is fully visible

## [0.14.0] - 2025-11-12

### Added

- Time elapsed display in scanning dialog with minutes/seconds format when exceeding 59 seconds
- Pause/Resume functionality for scans that preserves scan progress
- Introduced a QtMultimedia-backed sound manager with bundled tones to provide pleasant audio feedback for toolbar and scan dialog buttons

## [0.13.0] - 2025-11-11

### Added

- Scan progress dialog now mirrors the main badge image, switches to a "scan complete" badge when finished, uses Feather play/pause/close icons, formats large numbers with thousand separators, and stays open until closed by the user

## [0.12.0] - 2025-11-10

### Added

- macOS builds now show "Ghost Files Finder" as the app name and use a bundled window icon
- Toolbar now presents icon buttons with text labels for scan, source root, rules file, delete, export, and quit actions using bundled Feather SVGs
- Added helper script `scripts/copy_feather_icons.sh` to sync Feather SVG assets into the project resources
- Added PyInstaller configuration (`ghost_files_finder.spec`) and helper script to produce distributable builds

### Changed

- Updated app metadata and configuration directories to use the "Ghost Files Finder" identity and credit Rich Lewis as the author

## [0.11.0] - 2025-11-09

### Added

- "Select Root…" action lets users change the scan directory from the toolbar or File menu
- Modal scanning dialog mirrors footer progress (long-path friendly), now owns the Scan / Pause / Cancel controls, and stays larger to accommodate long paths
- Selecting a source folder or rules file no longer triggers an automatic scan; the Scan button activates once both selections are made

### Changed

- Removed Pause and Cancel toolbar actions in favour of dialog-hosted controls for scanning
- Startup no longer triggers an immediate scan; the user initiates scanning explicitly

## [0.10.0] - 2025-11-08

### Added

- Double-click rename updates files on disk while keeping highlights and summary counts in sync

## [0.9.0] - 2025-11-07

### Added

- Clicking a rule highlights its row and colors matching results in the tree with the rule's tint

## [0.8.0] - 2025-11-06

### Added

- When no rule checkboxes are active the full source tree is shown; unchecking "Select all" clears the result list
- Clearing the search field immediately re-runs the filter so visible results reset without extra clicks

## [0.7.0] - 2025-11-05

### Added

- "Open…" action validates and loads rclone filter files, replacing rules and triggering a rescan

### Changed

- Replaced module/class/function docstrings with block comments to standardise documentation style project-wide

## [0.6.0] - 2025-11-04

### Added

- Folder rows render in bold, their full paths include a trailing slash, and the context menu explains that folders cannot be deleted

## [0.5.0] - 2025-11-03

### Added

- File context menu now offers "Open in Finder/File Explorer" with OS-specific handling

## [0.4.0] - 2025-11-02

### Added

- Selecting rules in the sidebar now immediately filters results, with multi-select supported

## [0.3.0] - 2025-11-01

### Added

- Results pane promoted to a dedicated "Results" panel that fills the window beneath the search bar
- Results footer now shows live file/folder totals plus highlighted counts, and the tree exposes "Expand all" / "Collapse all" controls

## [0.2.0] - 2025-10-30

### Added

- Added File ▸ Quit command (also on the toolbar) with confirmation dialog before closing the app

### Changed

- `create-samples.py` now relies solely on the shared fixture helper; manual extras were removed to avoid divergence

## [0.1.9] - 2025-10-28

### Added

- Export dialog supporting lines, CSV, JSON, and JSONL formats for visible or full results

### Changed

- Removed the `**/Icon?` filter rule and its Icon sample data from fixtures and tests

## [0.1.8] - 2025-10-25

### Added

- Tri-state "Select all" control for rule filters plus type-safe PySide6 integrations

## [0.1.7] - 2025-10-22

### Added

- Delete workflow with confirmation dialog and asynchronous Trash worker

## [0.1.6] - 2025-10-20

### Added

- Persistent settings for last-used root/filter paths and default export format

## [0.1.5] - 2025-10-18

### Added

- Main window wiring for live scans, status-bar progress updates, and safe thread teardown

## [0.1.4] - 2025-10-15

### Added

- Background filesystem `ScanWorker` with progress, cancellation, and real tree population

## [0.1.3] - 2025-10-12

### Added

- Expanded pre-commit tooling (ruff, mdformat, JSON formatters) and hardened project ignore list

## [0.1.2] - 2025-10-05

### Fixed

- **Performance**: Fixed application freezing when processing large datasets with many nested directories
  - Implemented incremental node processing with frequent UI updates during tree model population
  - Optimized recursive child processing with chunked processing (25-50 items) and event loop updates
  - Improved column resizing to avoid expensive `resizeColumnToContents()` operations for large datasets
  - Added detailed debug logging for performance bottleneck identification
  - Application now handles nodes with 500+ children without UI freezing

## [0.1.1] - 2025-09-25

### Added

- Settings dialog for configuring debug logging, UI sounds, and completion sounds

## [0.1.0] - 2025-09-15

### Added

- uv-managed project scaffold with PySide6 application entry point and CLI harness
- Core matching engine implementing rclone-style glob rules with unit tests
- GUI skeleton: main window, rules sidebar, tree view with search modes, status bar
- Initial developer tooling (pytest, nox, ruff, mypy) and documentation bootstrap

## [0.0.9] - 2025-09-10

### Added

- Basic file operations and context menu framework

## [0.0.8] - 2025-09-05

### Added

- Export functionality foundation

## [0.0.7] - 2025-09-01

### Added

- File system integration and path handling

## [0.0.6] - 2025-08-25

### Added

- Tree view component with basic display capabilities

## [0.0.5] - 2025-08-20

### Added

- Rules panel sidebar component

## [0.0.4] - 2025-08-15

### Added

- Search bar component with filtering capabilities

## [0.0.3] - 2025-08-10

### Added

- Core matching engine with rclone-style glob pattern support

## [0.0.2] - 2025-08-05

### Added

- Project structure and build configuration
- Basic PySide6 application framework

## [0.0.1] - 2025-08-01

### Added

- Initial project setup with uv package manager
- Repository structure and basic configuration files

[0.0.1]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.0.1
[0.0.2]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.0.2
[0.0.3]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.0.3
[0.0.4]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.0.4
[0.0.5]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.0.5
[0.0.6]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.0.6
[0.0.7]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.0.7
[0.0.8]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.0.8
[0.0.9]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.0.9
[0.1.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.1.0
[0.1.1]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.1.1
[0.1.2]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.1.2
[0.1.3]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.1.3
[0.1.4]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.1.4
[0.1.5]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.1.5
[0.1.6]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.1.6
[0.1.7]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.1.7
[0.1.8]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.1.8
[0.1.9]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.1.9
[0.10.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.10.0
[0.11.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.11.0
[0.12.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.12.0
[0.13.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.13.0
[0.14.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.14.0
[0.2.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.2.0
[0.3.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.3.0
[0.4.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.4.0
[0.5.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.5.0
[0.6.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.6.0
[0.7.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.7.0
[0.8.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.8.0
[0.9.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v0.9.0
[1.0.0]: https://github.com/richlewis007/ghost-files-finder/releases/tag/v1.0.0
[unreleased]: https://github.com/richlewis007/ghost-files-finder/compare/v1.0.0...HEAD
