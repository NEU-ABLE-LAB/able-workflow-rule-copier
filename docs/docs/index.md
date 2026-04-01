# ABLE Workflow Rule Copier

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)
[![codecov](https://codecov.io/gh/NEU-ABLE-LAB/able-workflow-rule-copier/graph/badge.svg?token=1K05YM2HIC)](https://codecov.io/gh/NEU-ABLE-LAB/able-workflow-rule-copier)
[![tox Main Tests](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier/actions/workflows/ci.yml/badge.svg)](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier/actions/workflows/ci.yml)

A [copier](https://copier.readthedocs.io/en/stable/) template for generating a snakemake workflow rule that may use the project's python package.

This template assumes that you have already created an [`able-workflow-copier`]({{ able_workflow_copier_docs }}) project and have optionally created a [`able-workflow-module-copier`]({{ able_workflow_module_copier_docs }}) module and [`able-workflow-etl-copier`]({{ able_workflow_etl_copier_docs }}) ETL process.

## Overview of ABLE Workflow copier templates

- [`able-workflow-copier`]({{ able_workflow_copier_docs }})
- [`able-workflow-module-copier`]({{ able_workflow_module_copier_docs }})
- [`able-workflow-etl-copier`]({{ able_workflow_etl_copier_docs }})
- [`able-workflow-rule-copier`]({{ able_workflow_rule_copier_docs }})

## Who These Docs Are For

- **Template developers**: contributors maintaining `able-workflow-rule-copier`.
- **Project developers**: people applying this template to add a new workflow rule to an existing project.
- **Project users and project consumers**: people who only need to run or import a generated workflow should primarily use the generated project's documentation instead of this template repository.

## Contributing

### Environment configuration

See the environment configuration [`able-workflow-copier`](https://github.com/NEU-ABLE-LAB/able-workflow-copier).

1. Create a development environment with conda

   ```bash
   # Create the environment (or update and prune if it already exists)
   conda env update --name able-workflow-rule-copier --file environment-py312-dev.yaml --prune
   ```

   Alternatively, run the script `scripts/conda_update.sh`.

   Then activate

   ```bash
   conda activate able-workflow-rule-copier
   ```

   Configure `able-workflow-rule-copier` as the default python environment in the [Python Environments VSCode extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-python-envs).

2. Install pre-commit into the repo to run checks on every commit

   ```bash
   (able-workflow-rule-copier) pre-commit install
   ```
