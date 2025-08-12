# Changelog
All notable changes to this project will be documented in this file.

This project follows a simplified version of [Keep a Changelog](https://keepachangelog.com/) and uses semver-style tags (e.g., `v0.9.0-beta`).

## [Unreleased]
### Added
- (placeholder) Add items scheduled for the next beta here.

### Changed
- (placeholder)

### Fixed
- (placeholder)

---

## [0.9.0-beta] - 2025-08-12
### Added
- **CLI**: `init`, `labels`, `--once`, `--daemon`, `--dry-run`.
- **Rules engine**: `rules.yaml` with `whitelist`, `blacklist`, `always_star`.
- **Backoff**: resilient Gmail API calls with exponential retry.
- **Logging**: stdout + rotating file `gsa.log`.
- **Caching**: SQLite DB of processed message IDs to prevent reprocessing.
- **Label name→ID** resolution at startup.
- **Docs**: Quick Start, install-from-source, configuration guide.

### Changed
- Standardized `.env` keys: `LABEL_ID_REVIEW`, `POLL_INTERVAL`, `GMAIL_POLL_CACHE`, `GSA_LOG_LEVEL`.

### Fixed
- CLI daemon mode startup visibility (startup and per-cycle logs).

[Unreleased]: https://github.com/oberon01/gmail-sentiment-analyzer/compare/v0.9.0-beta...HEAD
[0.9.0-beta]: https://github.com/oberon01/gmail-sentiment-analyzer/releases/tag/v0.9.0-beta
