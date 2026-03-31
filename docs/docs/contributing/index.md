# Contributing to ABLE Workflow Rule Copier

## Tests

The test environments are managed with `tox`.

### Validating template generation

This template is to be run in a project that was created with [`able-workflow-copier`]({{ able_workflow_copier_docs }}). To test rendering, this repository uses the parent template from the git submodule at `submodules/able-workflow-copier`.

!!! note "Initializing and updating parent template submodules"

    Initialize submodules before running template tests:

    ```bash
    git submodule update --init --recursive
    ```

    To pull the latest submodule commits recorded by the current branch:

    ```bash
    git submodule sync --recursive
    git submodule update --init --recursive
    ```

Example Copier answers are provided in the `answers/` directory. The following command runs the tests for these examples:

    ```bash
    tox run -e py312-template-generate
    ```
