# ABLE Workflow Rule copier template documentation

## Overview

The documentation for this project uses [MkDocs](https://www.mkdocs.org/) and the
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

The documentation source files are located in the `docs/docs/` directory.

The navigation structure is specified with
[`literate-nav`](https://pypi.org/project/mkdocs-literate-nav/) in the
`SUMMARY.md` file within the `docs/docs/` directory and each subdirectory.

/// note

    This documentation *can* be served as a stand alone site, but is intended to be included in the main [`able-workflow-copier`](https://github.com/NEU-ABLE-LAB/able-workflow-copier-dev) documentation via a gitsubmodule and a symlink to this project's `docs/docs/` directory.

## Building the documentation locally

    ```bash
    mkdocs build  --config-file docs/mkdocs.yml
    ```

    The assumes that you have already set up the development environment.
    See the main `README.md` file for instructions.

## Serving the documentation locally

    ```bash`
    mkdocs serve --config-file docs/mkdocs.yml
    ```

## More information

For more information on developing the documentation, see the
`docs/contributing/docs.md` file or the equivalent in the hosted documentation.
