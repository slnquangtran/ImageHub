# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2025-02-02

### Added

- Initial release.

## [0.1.1] - 2026-02-12

### Added
- Palette-based theming with five swatches
- Palette persistence to config file at ~/.imagehub_config.json
  (Windows: %USERPROFILE%\\.imagehub_config.json)
- UI improvements: color-themed controls for better readability and accessibility

### Changed
- UI refinements to support theming and better readability
- Internal helpers for color palette management and dynamic theming

### Fixed
- Minor fixes in color palette persistence code

### How to test
- Run the app; switch swatches to apply different themes; restart the app and verify the selected palette persists via the config file
