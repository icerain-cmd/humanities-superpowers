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

Three layers are recorded separately and must never be collapsed into one another:

| Layer | Field | Values | Meaning |
|---|---|---|---|
| Historical gate result | `status` | `PASS`, `CONDITIONAL PASS`, `FAIL` | What the gate recorded when it was evaluated. It is never rewritten by a later change. |
| Current validity | `validity` | `VALID`, `INVALIDATED`, `REQUIRES_RECHECK` | Whether that recorded result still applies to the current research objects. |
| Progression authorization | derived, not stored | eligible / not eligible | Whether the gate may be used as grounds for the next step. |

Invariants:

```text
PASS + VALID              -> may authorize progression
PASS + INVALIDATED        -> remains a valid historical record; cannot authorize progression
PASS + REQUIRES_RECHECK   -> remains a valid historical record; cannot authorize progression
FAIL + any validity       -> cannot authorize progression
```

`INVALIDATED` is a validity value, never a gate status. A historical `PASS` is never rewritten into `FAIL`.

When a dependency materially changes, an earlier `PASS` remains in history but may no longer authorize progression. Invalidation follows explicit dependency references rather than a universal downstream cascade. A gate that is `INVALIDATED` or `REQUIRES_RECHECK` must carry an `invalidation_reason`, and a gate whose dependency metadata is absent cannot be bounded at all, so it fails closed as `REQUIRES_RECHECK` with an explicitly empty dependency list rather than being assumed valid. Validity returns to `VALID` only after the affected gate is actually re-run; an agent cannot restore it by editing the record.

See [Core Specification 2.0](specification/v2/CORE_SPECIFICATION.md) for the normative statement.
