# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2025-07-02

### Added
- **Fast Path Analysis**: Introduced `fast_success_regex` and `fast_failure_regex` in `config.json`. If a log matches these patterns, it is immediately classified without sending it to the LLM, significantly speeding up the process and reducing costs.

### Changed
- The core `analyze_log` function now performs the regex pre-check before falling back to LLM analysis.

## [0.5.0] - 2025-07-02

### Added
- An `Extracted Log Content` column in the report.
- Periodic saving for Excel reports to prevent data loss.
- Advanced issue classification prompt to distinguish between environmental issues and software defects.

## [0.4.0] - 2025-07-02

### Added
- Intelligent Log Reading (last 8KB).
- Exception Pattern Matching with `exception_pattern.template`.

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