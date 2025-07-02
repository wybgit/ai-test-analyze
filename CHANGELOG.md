# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-07-02

### Added
- **Intelligent Log Reading**: The tool now analyzes only the last 8KB of each log file, focusing on the most relevant information where errors typically occur.
- **Exception Pattern Matching**: Introduced a new `exception_pattern.template` to define benign error messages that should not be treated as failures, making the analysis more nuanced.

### Changed
- The main prompt template (`prompt.template`) has been updated to include the new exception pattern logic.
- The initialization process now also creates the `exception_pattern.template` in the user's configuration directory.

## [0.3.0] - 2025-07-02

### Added
- A dedicated `templates` directory for all user-configurable templates.
- An `example` directory with sample logs for out-of-the-box testing.
- Richer content for the `failed_pattern.template`.

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