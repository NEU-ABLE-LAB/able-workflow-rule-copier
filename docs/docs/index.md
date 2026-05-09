# ABLE Workflow Rule Copier

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)
[![codecov](https://codecov.io/gh/NEU-ABLE-LAB/able-workflow-rule-copier/graph/badge.svg?token=1K05YM2HIC)](https://codecov.io/gh/NEU-ABLE-LAB/able-workflow-rule-copier)
[![tox Main Tests](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier/actions/workflows/ci.yml/badge.svg)](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier/actions/workflows/ci.yml)

A [copier](https://copier.readthedocs.io/en/stable/) template for adding a Snakemake rule, its script, and the associated tests and docs inside an existing project.

This template assumes that you have already created an [`able-workflow-copier`]({{ able_workflow_copier_docs }}) project and may already have a [`able-workflow-module-copier`]({{ able_workflow_module_copier_docs }}) module and [`able-workflow-etl-copier`]({{ able_workflow_etl_copier_docs }}) ETL process.

## Start Here

1. If you want to add a new rule to an existing project, start with [Quick Reference](quick-reference/).
2. If you need the ecosystem-level rationale behind the template stack, go back to the main [`able-workflow-copier` Overview]({{ able_workflow_copier_docs }}/overview/).
3. If you are maintaining this template repository itself, use [Contributing](contributing/).

## What This Template Adds

- A new Snakemake rule declaration.
- The matching Python script scaffold.
- Unit and workflow-rule tests for the new rule.
- Maintainer-facing docs on how to update the generated rule scaffold.

## Template Ecosystem

- [`able-workflow-copier`]({{ able_workflow_copier_docs }})
- [`able-workflow-module-copier`]({{ able_workflow_module_copier_docs }})
- [`able-workflow-etl-copier`]({{ able_workflow_etl_copier_docs }})
- [`able-workflow-rule-copier`]({{ able_workflow_rule_copier_docs }})

Project users and project integrators should primarily use the generated project's documentation instead of this template repository.
