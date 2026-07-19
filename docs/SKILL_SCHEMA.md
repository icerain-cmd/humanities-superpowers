# Canonical SKILL.md schema

Every core skill must use this YAML front matter:

```yaml
---
name: kebab-case-name
description: Use when ...
version: 1.0.0
language: en
license: MIT
---
```

Required sections, in order:

1. `# Skill title`
2. `## Purpose`
3. `## When to use`
4. `## Inputs required`
5. `## Procedure`
6. `## Stop signals`
7. `## Completion criteria`
8. `## Anti-fabrication rules`
9. `## Output format`
10. `## Good invocation`
11. `## Bad invocation`
12. `## Next skills`
13. `## Limitations`

Descriptions must state the triggering situation, not summarize the whole procedure. Completion criteria must be observable. Stop signals must produce an explicit unresolved-item report.


## Phase 3 contract extension

The canonical legacy schema remains valid during Phase 3-A. Phase 3-B adds a required `## Contract` section after `## Purpose`, as specified in [`specification/SKILL_CONTRACT.md`](specification/SKILL_CONTRACT.md). Core skills must reach Contract Conformance Level 2 before v1.0.
