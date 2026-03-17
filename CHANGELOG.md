# Changelog

Human-readable log of changes between versions. Follows the [Common Changelog style guide](https://common-changelog.org/).

## v0.1.2 - 2026-03-15

### Changed

- Reworked docs publishing in `.github/workflows/docs-pages.yml` so pushes/manual runs deploy `dev`, releases deploy the tagged version, and `mike set-default` runs only for releases. (#30)
- Updated `.github/workflows/pr.yml` to use public `NEU-ABLE-LAB/able-workflow-copier@v0.1.1`, added workflow concurrency controls, and removed private-token dependent nested-clone/Codecov steps. (#30)
- Enforced uniformity of scripts and tests across `able-workflow*-copier` repos
- `sandbox_examples_generate` is now module `scripts.sandbox_examples_generate` instead of script

### Added

- Added `.github/workflows/main.yml` to run tox on `main` (Python 3.11/3.12), generate coverage/test-result reports, and upload to Codecov when a token is available. (#30)
- Added Codecov and `tox Main Tests` workflow badges to `README.md` and `docs/docs/index.md`. (#30)
- Refactored `copie_helpers.py` functions into their own file.

### Removed

- Duplicate `tox` install in `pr.yml`

### Fixed

- Removed stray `-dev` suffix references by switching `scripts/pull_able_workflow_copier.py` to the public `able-workflow-copier` repository and sandbox path naming. (#30)
- Constrained MkDocs to `<2` in both `pyproject.toml` and `environment-py312-dev.yaml` for compatibility. (#30)
- Corrected the ABLE Workflow docs navigation link in `docs/docs/SUMMARY.md` to point to `/latest/overview/`. (#30)
- Use an explicit `env.CODECOV_TOKEN` guard and token wiring for both Codecov upload steps in `.github/workflows/main.yml` to avoid secret-resolution failures. (#30)

## v0.1.1 - 2026-03-14

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

## v0.1.0 - 2025-07-18

Initial commit to public `able-workflow-rule-copier` repository from `NEU-ABLE-LAB` private repository.
