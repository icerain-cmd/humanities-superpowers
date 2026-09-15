# Agent Orchestration Contract

**Status: implemented, unreleased.**

Work is described by role, never by model name. A profile maps roles onto
models; the contracts below stay valid when that mapping changes.

## Roles

| Role | Responsibility | Must not |
|---|---|---|
| `PLANNER` / `ARCHITECT` | Define the objective, scope, constraints, risk level, acceptance criteria, and required verification | implement the change it planned, or declare its own plan verified |
| `IMPLEMENTER` | Execute the work package and produce the evidence package | approve its own work, weaken acceptance criteria, or claim completion without observed output |
| `REVIEWER` | Check the evidence package against the acceptance criteria and the diff | accept a summary in place of evidence |
| `ESCALATION_REVIEWER` | Decide when review is contested, when risk is `STRICT`, or when attempts are exhausted | silently overrule a reviewer without recording the reason |

Separation of duties mirrors the humanities rule that an agent recommendation
is not a researcher decision: the producer of work is not the approver of work.

## Operating profile (replaceable)

The mapping below is the current configuration, not part of the architecture.
Any role may be filled by any capable model.

| Role | Current assignment |
|---|---|
| `PLANNER`, `REVIEWER` | Sol Medium |
| `IMPLEMENTER` (implementation, debugging, test execution) | DeepSeek |
| `ESCALATION_REVIEWER` | Sol High |

Escalate to `ESCALATION_REVIEWER` when: the risk level is `STRICT` and the
change is complete; the reviewer and implementer disagree on a finding;
destructive or irreversible operations are proposed; or the attempt limit is
reached without a verified result.

## WORK_PACKAGE

The handoff from planner to implementer. It must be self-contained: an
implementer that has to ask what was meant has received an incomplete package.

| Field | Requirement |
|---|---|
| `objective` | one sentence stating the outcome |
| `scope` | what is in scope, and explicitly what is out of scope |
| `constraints` | environment, compatibility, and non-negotiables |
| `risk_level` | `QUICK`, `STANDARD`, or `STRICT`, with the property that set it |
| `acceptance_criteria` | verifiable statements, not intentions |
| `required_verification` | the commands or checks that must be run, and their expected result |
| `forbidden_actions` | what the implementer must not do |

Optional: `references`, `deadline`, `prior_attempts`, `reviewer_role`.

## EVIDENCE_PACKAGE

The handoff from implementer to reviewer. It reports what was observed, not
what was intended.

| Field | Requirement |
|---|---|
| `files_changed` | every changed path, with the reason |
| `tests_run` | exact commands |
| `test_results` | observed output or exit status, not a paraphrase |
| `unresolved` | every open item, including ones believed minor |
| `deviations` | where the implementation differed from the work package, and why |
| `completion_status` | `DONE`, `PARTIAL`, `BLOCKED`, or `ERROR`, consistent with the worker states |

An `EVIDENCE_PACKAGE` with `completion_status: DONE` and no observed test
output is invalid. A reviewer that approves it is recorded as a review failure.

## Rules

1. No implementation begins without a `WORK_PACKAGE` at `STANDARD` or above.
   `QUICK` work may record the package inline in the same message as the change.
2. No review begins without an `EVIDENCE_PACKAGE`.
3. `STRICT` work requires review by a different role than the one that
   implemented it.
4. Deviations are recorded, never silently absorbed.
5. Model names appear only in the profile table, never in the deterministic
   schemas or validators.
