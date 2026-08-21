# Epistemic Return Protocol

**Specification Version: 2.0.0**

## Distinction from rollback

`ROLLBACK` repairs a defect: missing prerequisite, invalid citation, scope violation, or failed claim–source fit. `Epistemic Return` reopens inquiry because new evidence, interpretation, theory, definition, or researcher judgment changes what can responsibly be asked or claimed.

An epistemic return is an object and transition record, not a new router decision or research state. The router uses the existing decision vocabulary: it normally returns `RESEARCHER_DECISION_REQUIRED` for a proposed return, then `PROCEED` to the approved target; a defect remains `ROLLBACK`.

## Materiality test

A return requires a documented reason that changes an earlier object's premise, scope, interpretation, dependency, or permitted claim. New evidence that merely confirms an existing decision produces a ledger update and possible recheck, not an automatic return.

A spelling, formatting, stylistic, or provenance-neutral wording change is not material knowledge and MUST NOT invalidate gates or produce a return record.

## Gate invalidation

Gate status and current validity are separate:

```text
status: PASS | CONDITIONAL PASS | FAIL
validity: VALID | INVALIDATED | REQUIRES_RECHECK
```

Full v2 workflows validate gate outputs against `schemas/gate-report-v2.schema.json`, which requires `schema_version: 2.0`, nonempty evidence and dependency references, and current validity. The backward-compatible base schema alone does not certify v2 progression.

Invalidation MUST be bounded by dependency references. Typical candidates are:

- ResearchQuestion → scope, literature route, argument, submission;
- ScopeBoundary → source coverage, argument, review, submission;
- ConceptRecord → terminology, argument, interpretation, citation fit;
- Claim → evidence ledger, citation, argument review, submission;
- EvidenceItem → claim support, argument, citation, submission;
- Interpretation → argument, structure, review.

The return record MUST name invalidated and preserved gates. It MUST NOT invalidate every downstream gate merely because one object changed.

## Execution

1. Record the trigger and changed knowledge.
2. Compare the new material with the existing object.
3. Propose a bounded target object and skill.
4. Identify dependent gates and preserved work.
5. Obtain researcher authorization when scholarly choice is involved.
6. Mark the record `APPROVED`, then `EXECUTED` only after reopening occurs.
7. Re-run affected gates and mark `RESOLVED` only when evidence exists.

`APPROVED`, `EXECUTED`, and `RESOLVED` records require an `authorization_ref` to a trusted human-interaction event and a `proposal_digest` that binds approval to the exact return proposal. A self-authored identifier is not authorization; the host must verify the event, actor, and digest outside JSON Schema validation.
