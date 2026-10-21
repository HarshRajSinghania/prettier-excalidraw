# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned
- `fix.py`: re-measure text width/height and re-centre bound labels after a font
  size snap.
- `build.py`: warn when an icon is shrunk below 65 % of its box; optional second
  (right-aligned) region title.
- Description optimisation for more reliable triggering.

## [0.1.0] - 2026-10-22

### Added
- `SKILL.md` with generate / restyle / check workflows and the reasoning behind
  each style rule, including a gap-filling step for under-specified prompts.
- `scripts/build.py`: JSON spec to `.excalidraw`, handling bound labels, elbowed
  bound arrows, embedded icons, same-side arrow loops and z-order.
- `scripts/lint.py`: 14 style rules including hidden arrows, child-before-parent
  z-order, icon sizing and misleading store placement.
- `scripts/fix.py`: mechanical fixes for font, size, roughness, fills, corners,
  arrowheads and z-order without moving anything.
- `scripts/preview.py`: SVG preview with exact text widths and a `--square` mode
  for quick-look thumbnails.
- Style guide and spec format references; five worked examples with specs.
- Eval set (3 cases) and grader; CI running the unit tests.
