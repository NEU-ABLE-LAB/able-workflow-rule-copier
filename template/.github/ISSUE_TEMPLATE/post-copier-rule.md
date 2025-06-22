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

1. [ ] `workflow/rules/{{ smk_file_name }}`
   1. [ ] Specify `input:` directives as needed.
   2. [ ] Specify `output:` directives as needed.
   3. [ ] Specify `params:` directives as needed.
   4. [ ] Specify `wildcards:` directives as needed.
2. [ ] `workflow/scripts/rule_*/{{ rule_name }}.py`
   1. [ ] Assign the desired snakemake directives (e.g., `input` to variables.
   2. [ ] Fill in the rule logic within main().
3. [ ] `tests/workflow/rules/test_{{ rule_name }}.py`: Add dummy data so that rule integration tests work.
4. [ ] `test/workflow/scripts/rule_*/test_{{ rule_name }}.py`
   1. [ ] Update the `SimpleNamespace()` parameters of `_fake_snakemake()` with dummy values for the expected inputs of the function under test.
   2. [ ] Replace the dummy `test_main_runs()` test with a more thorough test of the script under test.
5. [ ] Update `workflow/Snakefile` to include the new smk file `workflow/rules/{{ smk_file_name }}`
6. [ ] Update documentation on how to use rule or expected output. This should be automatically extracted from rule docstring.

### Optional

- [ ] Run the `logs_to_watch` rule and update the `"logViewer.watch"` section of `.vscode/settings.json` with the results found in `logs/rules/logs_to_watch.log`.
