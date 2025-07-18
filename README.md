# ABLE Workflow rules Copier

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)

A [copier](https://copier.readthedocs.io/en/stable/) template for generating a snakemake workflow rule that may use the project's python package.

This template assumes that you have already created an [`able-workflow-copier`](https://github.com/NEU-ABLE-LAB/able-workflow-copier) project and have optionally created a [`able-workflow-module-copier`](https://github.com/NEU-ABLE-LAB/able-workflow-module-copier) module and [`able-workflow-etl-copier`](https://github.com/NEU-ABLE-LAB/able-workflow-etl-copier) ETL process.

## Overview of ABLE Workflow copier templates

- [`able-workflow-copier`](https://github.com/NEU-ABLE-LAB/able-workflow-copier)
- [`able-workflow-module-copier`](https://github.com/NEU-ABLE-LAB/able-workflow-module-copier)
- [`able-workflow-etl-copier`](https://github.com/NEU-ABLE-LAB/able-workflow-etl-copier)
- [`able-workflow-rule-rule-copier`](https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier)

## Quick-Start

This assumes you are already working within a project created by [`able-workflow-copier`](https://github.com/NEU-ABLE-LAB/able-workflow-copier).

### Configure Conda Environment

Use the conda environment already created to copy the project template.

### Generate a rule with the template

```bash
copier copy --trust https://github.com/NEU-ABLE-LAB/able-workflow-rule-copier.git ./
```
