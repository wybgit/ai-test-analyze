# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-07-02

### Added
- **Template Directory**: All user-configurable templates (`prompt`, `success_pattern`, `failed_pattern`) are now stored in a dedicated `templates` subdirectory within the user's config folder (`~/.config/ai-test-analyze/templates`).
- **Rich Failure Patterns**: The `failed_pattern.template` now supports more detailed error analysis guidance in addition to simple keywords.
- **Example Directory**: Included a comprehensive `example` directory with sample logs for out-of-the-box testing and demonstration.

### Changed
- **File Structure**: Reorganized the package to include a `templates` directory, which is now correctly included in the distribution thanks to `package_data` in `setup.py`.
- **Initialization Logic**: The tool now copies the default templates from the package to the user's configuration directory on first run, ensuring they are available for user modification.
- **Documentation**: The `README.md` has been significantly updated to use the new `example` directory for its primary usage tutorial, making it much easier for new users to get started.

## [0.2.0] - 2025-07-02

### Added
- Sub-command Interface (`run`, `config`).
- `config` command to display paths to all configuration files.
- Blacklist filtering for directories and files.
- Enhanced prompt templating with dynamic success/failure patterns.

### Changed
- Simplified Excel view by removing outline grouping.

## [0.1.0] - 2025-07-01

### Added
- Initial Release with core features like multi-threading, CSV/Excel reporting, dynamic columns, and breakpoint resume.

### Fixed
- Multiple path resolution and stream parsing bugs.
