# Research Object Model 2.0

**Specification Version: 2.0.0**

The v1 objects remain valid. Fricturn adds five versionable research objects without overwriting their predecessors.

## Common optional versioning fields

`version`, `created_at`, `updated_at`, `derived_from`, `supersedes`, `triggered_by`, `validation_refs`, and `last_gate_status` are optional in the backward-compatible base schema and required where a v2 conformance profile says so. `supersedes` preserves history; it never licenses deletion of the older object.

## EvidenceLedgerEntry

Connects a claim and evidence item while keeping source verification separate from evidential function. It records `verification_state`, `evidential_standing`, method, locator, limitations, counterevidence, checker, time, and provenance.

## JudgmentRecord

Records a decision point, alternatives, evidence, interpretations, counterarguments, agent recommendations, researcher decision, rationale, authorization actor and external approval-event reference, status, time, and supersession. Agent proposals may exist without a researcher decision. Only an authorized researcher decision may be `ACCEPTED`; the host verifies the approval event outside the self-authored record.

## InterpretationVersion

Preserves observed features, interpretive move, frame, rival readings, limits, trigger, reason for change, derivation, supersession, and researcher status. An AI-generated interpretation begins as `PROPOSED`.

## FrictionEvent

Records a material obstacle to premature closure: type, target, trigger, description, blocking flag, categorical severity, required action, and resolution status. Resolution may preserve an accepted risk; it need not erase disagreement.

## EpistemicReturnRecord

Records a knowledge-driven reopening: trigger, source and target states, target object and skill, new evidence or interpretation, affected gate validity, preserved gates, artifacts reopened, required researcher decision, and return status.

## Provenance and history rule

New interpretations and decisions MUST append history. `I2.supersedes = I1` and `D2.supersedes = D1`; I1 and D1 remain inspectable. A changed record MUST identify what changed, why, what triggered it, and which validation references require reconsideration.
