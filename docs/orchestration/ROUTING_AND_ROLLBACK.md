# Routing and Rollback Protocol

## Minimal routing

The router selects the smallest set of skills that can produce the requested scholarly object from the current state. It must not load every skill by default.

## Dependency examples

- Research question before scope.
- Scope before corpus-wide claims.
- Primary object before close reading.
- Source record before literature dialogue or citation verification.
- Argument map before prose restructuring when logic is disputed.
- Actual manuscript changes before a reviewer response is marked complete.
- Final package before submission verification.

## Decision values

- `PROCEED` — run the next valid skill.
- `PAUSE` — obtain a missing source, guideline, permission, or artifact.
- `ROLLBACK` — return to the earliest skill able to repair a causal defect.
- `RESEARCHER_DECISION_REQUIRED` — present defensible alternatives and consequences.
- `STOP` — fabrication, unsafe handling, or an irrecoverable requirement prevents execution.

## Conditions may travel forward

A condition can be carried forward when it does not invalidate the next operation. For example, provisional originality status does not prevent scope design. It does prevent a final novelty claim.

Conditions must include:

- origin gate;
- affected object or claim;
- allowed downstream operations;
- blocked claims or transitions;
- required resolution point.

## No false progress

The following are prohibited:

- advancing because a deadline is near;
- rewriting prose to conceal an evidentiary gap;
- deleting an unresolved marker without solving the issue;
- treating `planned` revision as `verified` revision;
- treating a remembered summary as a verified source;
- issuing a final `PASS` from workflow state alone.
