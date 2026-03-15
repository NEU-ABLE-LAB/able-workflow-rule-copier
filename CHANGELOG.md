# Changelog

Human-readable log of changes between versions. Follows the [Common Changelog style guide](https://common-changelog.org/).

## 0.1.1 - 2026-03-14

### Changed

- **Breaking:** Require Snakemake v9.6.3+ for generated workflow-rule script tests because of `snakemake.io` API changes.
- Docs are not hosted on github pages instead of thisismikekane.com domain.

### Fixed

- Support both `snakemake.io.container` (Snakemake v9.17.0+) and `snakemake.io` fallback imports in generated test scaffolding, and use `ResourceList` for `Snakemake` resources.
- Switch to official PyPI `pytest-copie>=0.3.1` instead of a Git dependency for test tooling.
- Guard copier-based template tox collection by rejecting dirty template repositories and passing immutable `vcs_ref` values for deterministic copies.
- Update copier extension configuration and dependency naming to `copier_template_extensions` / `copier-template-extensions>=0.3.3` for compatibility with newer releases.
- Configure `git-revision-date-localized` with `locale: en` in MkDocs config.
- Replace Ruff `exclude` with `extend-exclude` to keep lint configuration compatible with current Ruff behavior.

## 0.1.0 - 2025-07-18

Initial commit to public `able-workflow-rule-copier` repository from `NEU-ABLE-LAB` private repository.
