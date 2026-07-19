# Research State Machine

This document specifies the orchestration model used by `using-humanities-superpowers`.

## Purpose

The state machine prevents fluent output from being mistaken for completed research. States describe which scholarly objects currently exist and which operation is valid next. They do not certify truth or quality.

## States

| State | Minimum observable condition | Common blocking condition |
|---|---|---|
| `IDEA` | Topic, intuition, phenomenon, or problem is recorded | No arguable research question |
| `QUESTION` | A provisional research question exists | Scope, feasibility, or hidden conclusion unresolved |
| `SCOPE` | Inclusion, exclusion, corpus, and claim scale are explicit | Necessary materials unavailable |
| `SOURCES` | Source records and verification states exist | Central evidence absent or unverified |
| `INTERPRETATION` | Bounded readings connect observable features to interpretive moves | Primary object absent or alternative reading ignored |
| `ARGUMENT` | Claims, evidence, warrants, qualifications, and objections are mapped | Central warrant or evidence path missing |
| `STRUCTURE` | Researcher material is organized by argumentative function | Prose conceals unresolved argument gaps |
| `REVIEW` | Manuscript or argument is under systematic challenge | Review lacks manuscript, scope, or evidence context |
| `REVISION` | Problems or reviewer comments have revision actions | Planned actions are falsely reported as completed |
| `SUBMISSION` | Final manuscript and package are being verified | Citation, privacy, package, or venue requirement fails |
| `BLOCKED` | A required item or decision prevents valid progression | Source, permission, ethics review, or author decision absent |
| `UNKNOWN` | Evidence is insufficient to classify the state | No discriminating artifact supplied |

## Transition rule

A transition is valid only when:

1. the current state's required object exists;
2. the selected skill's prerequisites are satisfied;
3. the controlling gate is not `FAIL`;
4. carried conditions remain explicitly represented;
5. no researcher-controlled decision has been silently automated.

## Normal transitions

```text
IDEA → QUESTION → SCOPE → SOURCES
SOURCES → INTERPRETATION and/or ARGUMENT
INTERPRETATION → ARGUMENT
ARGUMENT → STRUCTURE → REVIEW → REVISION → SUBMISSION
```

The path is intentionally nonlinear. A source discovery may return a project from `ARGUMENT` to `SCOPE`; a reviewer may return it from `REVISION` to `CONCEPT LINEAGE`; a submission audit may stay within `SUBMISSION` while repairing file metadata.

## Gate-driven actions

| Gate status | Default orchestration action |
|---|---|
| `PASS` | Advance if the next skill's prerequisites are satisfied |
| `CONDITIONAL PASS` | Advance only with named conditions and no invalid conversion |
| `FAIL` | Roll back, pause, request researcher decision, or stop |

## Rollback principle

Rollback targets the earliest causal defect, not the latest visible symptom.

- Unsupported generalization → scope.
- Unsupported central claim → literature dialogue, close reading, or argument planning.
- Concept drift → concept lineage and terminology audit.
- Unverified citation → citation audit; if central support collapses, argument planning.
- Reviewer request requiring a new corpus → researcher decision and scope.
- Hidden author identity in blinded files → submission package repair only.

## Completion semantics

`SUBMISSION` is a workflow state. `PASS` is a gate result. They are not synonyms.

A project may end with:

- `SUBMISSION + PASS`: the named checks passed for the inspected package;
- `SUBMISSION + CONDITIONAL PASS`: non-blocking conditions remain and are disclosed;
- `SUBMISSION + FAIL`: submission should not proceed until blocking defects are repaired.

No state authorizes claims of truth, originality, or publication success.
