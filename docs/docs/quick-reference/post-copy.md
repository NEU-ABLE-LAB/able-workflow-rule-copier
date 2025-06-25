---
render_macros: false
---

# Post-Copy Checklist

This to-do list will be rendered to `logs/post-copier-todos/rule-{{ rule_name }}.md`

{%
    include-markdown "../../../template/logs/post-copier-todos/rule-{{ rule_name }}.md.jinja"
    heading-offset=1
%}
