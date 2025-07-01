# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-07-01

### Added
- **Initial Release**
- Core functionality to analyze log files or directories via a CLI.
- Configuration via `config.json` for API settings.
- Whitelisting for directories and log files using wildcards.
- Automatic creation of default config file in user's home directory (`~/.config/ai-test-analyze`).
- Generation of a CSV report with analysis results.
- Sample log files and directories for testing.
- Separation of the LLM prompt into a `prompt.template` file.
- Progress bar (`tqdm`) to visualize analysis progress.
- Incremental writing to the report file for robustness.
- Breakpoint resume capability using `--resume` flag.
- `--debug` mode to include LLM I/O in the report.
- Hierarchical directory columns (Root, Sub Dir 1, Sub Dir 2) in the report.
- Optional report generation in `.xlsx` format with `--format xlsx`.
- Rich formatting for Excel reports, including color-coding, auto-width, and frozen panes.
- Real-time data transfer rate display (`KB/s`) on the progress bar.
- Extraction of LLM "reasoning_content" in debug mode.
- **Multi-threaded concurrent analysis** using `--threads` parameter (default: 8).
- `.gitignore` file for version control hygiene.
- `requirements.txt` for dependency management.
- This `CHANGELOG.md` file.
- `build.sh` script for easy packaging.

### Fixed
- Fixed a critical path resolution bug causing "File not found" errors.
- Resolved `_csv.Error: field larger than field limit` in debug mode by increasing the limit.
- Fixed a `TypeError` from `None` values in the LLM stream by adding a `None` check.
- Corrected a flawed stream-processing logic to ensure complete LLM responses are parsed.
