# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Richer duration primitives: `PositiveDuration`, `NonNegativeDuration`, `Milliseconds`, and `DurationRange`
- Serialization helpers for seconds, milliseconds, `timedelta`, and ISO 8601 output
- Optional integration helpers for FastAPI, Taskiq-style tasks, FastStream-style headers, Pydantic AI budgets, and Pydantic Graph timeout guards
- Integration examples and docs for service configuration, async infrastructure, and agent workflows

## [0.1.0] - 2026-07-08

### Added

- Initial duration parsing API
- Pydantic v2 integration
- Formatting helpers
- Custom exception hierarchy
- PyPI-ready packaging
- CI validation
- Release workflow using PyPI Trusted Publishing

[Unreleased]: https://github.com/dillon-barendt/duratypes/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/dillon-barendt/duratypes/releases/tag/v0.1.0
