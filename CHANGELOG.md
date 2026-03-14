# Changelog

Human-readable log of changes between versions. Follows the [Common Changelog style guide](https://common-changelog.org/).

## 0.1.0 - 2025-07-18

Initial commit to public `able-workflow-rule-copier` repository from `NEU-ABLE-LAB` private repository.

## 0.1.1 - 2026-03-14

### Changed

- **Breaking:** Require Snakemake v9.6.3+ for generated workflow-rule script tests because of `snakemake.io` API changes ([`51fcfbf`](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier-dev/commit/51fcfbf2d7194795b39f18696709859db64bf4eb)).

### Fixed

- Support both `snakemake.io.container` (Snakemake v9.17.0+) and `snakemake.io` fallback imports in generated test scaffolding, and use `ResourceList` for `Snakemake` resources ([`51fcfbf`](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier-dev/commit/51fcfbf2d7194795b39f18696709859db64bf4eb)).
- Switch to official PyPI `pytest-copie>=0.3.1` instead of a Git dependency for test tooling ([`51fcfbf`](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier-dev/commit/51fcfbf2d7194795b39f18696709859db64bf4eb)).
- Guard copier-based template tox collection by rejecting dirty template repositories and passing immutable `vcs_ref` values for deterministic copies ([`51fcfbf`](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier-dev/commit/51fcfbf2d7194795b39f18696709859db64bf4eb)).
- Update copier extension configuration and dependency naming to `copier_template_extensions` / `copier-template-extensions>=0.3.3` for compatibility with newer releases ([`51fcfbf`](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier-dev/commit/51fcfbf2d7194795b39f18696709859db64bf4eb)).
- Configure `git-revision-date-localized` with `locale: en` in MkDocs config ([`51fcfbf`](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier-dev/commit/51fcfbf2d7194795b39f18696709859db64bf4eb)).
- Replace Ruff `exclude` with `extend-exclude` to keep lint configuration compatible with current Ruff behavior ([`51fcfbf`](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier-dev/commit/51fcfbf2d7194795b39f18696709859db64bf4eb)).
