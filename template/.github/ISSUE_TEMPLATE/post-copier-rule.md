---
name: Post-copier rule development
about: This is a template for for issues to address after running the able-workflow-rule-copier template.
title: "post-copier rule"
labels:
  - workflow
  - tests
---

This issue is for tracking the development of a rule that was copied from the `able-workflow-rule-copier` template.

## Next steps

### Required

1. [ ] `workflow/scripts/rule_*/{{ rule_name }}.py`
   1. [ ] Assign the desired snakemake directives (e.g., `input` to variables.
   2. [ ] Fill in the rule logic within main().
2. [ ] `workflow/rules/{{ smk_file_name }}`
   1. [ ] Specify `input:` directives as needed.
   2. [ ] Specify `output:` directives as needed.
   3. [ ] Specify `params:` directives as needed.
   4. [ ] Specify `wildcards:` directives as needed.
   5. [ ] If the rule uses a `conda:` environment, make sure to reference the appropriate entry in `config["CONDA"]["ENVS"]["<ENV_NAME>"]`
3. [ ] `test/workflow/scripts/rule_*/test_{{ rule_name }}.py`
   1. [ ] Update the `SimpleNamespace()` parameters of `_fake_snakemake()` with dummy values for the expected inputs of the function under test.
   2. [ ] Replace the dummy `test_main_runs()` test with a more thorough test of the script under test.
4. [ ] Update documentation on how to use rule or expected output.
5. [ ] Add dummy data to `tests/workflow/rules/test_{{ rule_name }}.py` so that rule integration tests work.

### Optional

- [ ] Run the `logs_to_watch` rule and update the `"logViewer.watch"` section of `.vscode/settings.json` with the results found in `logs/rules/logs_to_watch.log`.
