# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-07-02

### Added
- **Enhanced Analysis Context**: The report now includes a new `Extracted Log Content` column, showing the exact log snippet that was analyzed.
- **Periodic Saving**: For Excel reports, the file is now saved periodically during long runs (every 100 items), providing better protection against data loss from interruptions.
- **Advanced Issue Classification**: The prompt now guides the LLM to classify failures as either **Environmental Issues** or **Software Defects**, leading to more actionable insights.

### Changed
- The `analyze_log` function now returns the extracted log content along with other analysis data.
- The main processing loop in `handle_run` has been updated to implement periodic saving for Excel files.

## [0.4.0] - 2025-07-02

### Added
- Intelligent Log Reading (last 8KB).
- Exception Pattern Matching with `exception_pattern.template`.

### Changed
- Updated main prompt to use exception patterns.

## [0.3.0] - 2025-07-02

### Added
- A dedicated `templates` directory for all user-configurable templates.
- An `example` directory with sample logs for out-of-the-box testing.

### Changed
- Reorganized the package to correctly include the `templates` directory in the distribution.
- Updated the `README.md` with a comprehensive tutorial using the `example` directory.

## [0.2.0] - 2025-07-02

### Added
- Sub-command Interface (`run`, `config`).
- `config` command to display paths to all configuration files.
- Blacklist filtering for directories and files.

### Changed
- Simplified Excel view by removing outline grouping.

## [0.1.0] - 2025-07-01

### Added
- Initial Release with core features like multi-threading, CSV/Excel reporting, dynamic columns, and breakpoint resume.

### Fixed
- Multiple path resolution and stream parsing bugs.
