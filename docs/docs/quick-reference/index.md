# Quick Reference

??? note "Audience: Project Developers"

    This section is for project developers applying `able-workflow-rule-copier` to an existing workflow project.
    If you are maintaining the template itself, use this repository's contributing documentation instead.

Apply this Copier template to an existing [`able-workflow-copier`]({{ able_workflow_copier_docs }}) project (i.e., `./`) to create a new Snakemake rule with the following commands:

```bash
copier copy --trust {{ able_workflow_rule_copier_repo }}.git ./
```

{% raw %}

If this template has been updated and you would like to apply those updates to your project, run the following command replacing `{{ rule_name }}` with the rule you would like to update. You can see all the Copier templates that have been applied to your project in the `./copier-answers/` directory. (DO NOT EDIT THESE FILES.)

```bash
copier update --trust --answers-file ".copier-answers/rule-{{ rule_name }}.yml" ./
```

{% endraw %}
