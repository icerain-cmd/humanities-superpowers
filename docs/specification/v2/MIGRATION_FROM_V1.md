# Migration from v1

**Specification Version: 2.0.0**

## Compatibility policy

v1 research objects, sessions, gate reports, and examples remain valid. New fields in extended base schemas are optional. Full v2 artifacts use the five dedicated research-object schemas plus `gate-report-v2.schema.json` and conformance fixtures. An unversioned base GateReport is legacy-compatible input; it MUST NOT authorize v2 progression until converted to the full v2 profile.

The 13 core skills and one router retain their names and invocation roles. The router retains `PROCEED`, `PAUSE`, `ROLLBACK`, `RESEARCHER_DECISION_REQUIRED`, and `STOP`. Gate status retains `PASS`, `CONDITIONAL PASS`, and `FAIL`.

## Semantic migrations

- Existing `ITERATIVE_RETURN` descriptions migrate to an `EpistemicReturnRecord`; no new primary state is introduced.
- Gate records may add `validity`, dependency references, and invalidation reasons without altering their historical status.
- Evidence items may be connected through `EvidenceLedgerEntry`; verification status never implies support.
- Interpretations and decisions become append-only histories linked with `supersedes`.
- AI recommendations remain distinct from human authorization.

## Full v2 conformance

A full v2 workflow records material friction, supports bounded gate invalidation, preserves counterevidence and rival readings, produces productive refusal when judgment is unsupported, and can execute an authorized epistemic return without deleting prior objects.
