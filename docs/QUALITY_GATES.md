# Research quality gates

A quality gate is a documented decision point that can stop the workflow.

## Status values

- `PASS`: no known blocking issue remains.
- `CONDITIONAL PASS`: non-blocking risks are documented and accepted by the researcher.
- `FAIL`: one or more blocking issues remain.

## Required gate record

```text
Gate:
Status:
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill:
```

## Gate sequence

1. Question gate
2. Scope gate
3. Source gate
4. Concept gate
5. Argument gate
6. Stress-test gate
7. Citation gate
8. Submission gate

A failed gate is expected when required evidence is absent. It must never be silently converted into a pass.

## Gate validity in Fricturn

Historical gate status remains `PASS`, `CONDITIONAL PASS`, or `FAIL`. Fricturn records current validity separately as `VALID`, `INVALIDATED`, or `REQUIRES_RECHECK`. When a dependency materially changes, an earlier `PASS` remains in history but may no longer authorize progression. Invalidation follows explicit dependency references rather than a universal downstream cascade.
