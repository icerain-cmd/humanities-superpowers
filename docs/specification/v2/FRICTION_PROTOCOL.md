# Interpretive Friction Protocol

**Specification Version: 2.0.0**

## Definition

Interpretive Friction is a research brake that exposes uncertainty when a process would otherwise smooth conflicting evidence, concepts, interpretations, or judgments into premature closure.

## Trigger test

Create a friction event only when all three hold:

1. a named research object or transition is affected;
2. a material conflict, unsupported promotion, or completion risk is observable;
3. an action, decision, or recheck is required.

Do not create friction for wording preference, spelling, formatting, or a routine source addition alone. A defensible rival interpretation is not automatically blocking: record it only when it changes a claim, decision, gate, or required action.

When the trigger test is satisfied, create one event at the narrowest affected object or transition. Do not duplicate the same conflict across skills merely to increase traceability.

## Canonical types

`CLAIM_OVERREACH`, `CONCEPT_DRIFT`, `EVIDENCE_CONFLICT`, `RIVAL_INTERPRETATION`, `TRANSLATION_INSTABILITY`, `SOURCE_MISMATCH`, `INFERENCE_PROMOTION`, `AGENT_DISAGREEMENT`, `RESEARCHER_DISAGREEMENT`, and `COMPLETION_RISK`.

## Severity and blocking

Severity is `LOW`, `MEDIUM`, `HIGH`, or `BLOCKING`. It communicates scholarly consequence. `blocking` separately controls workflow: `true` prevents the dependent transition until resolved, accepted by an authorized researcher where acceptance is permitted, or converted into an approved epistemic return. `BLOCKING` severity therefore requires `blocking: true`; lower severity does not determine the boolean automatically.

## Resolution

Status is `OPEN`, `ACCEPTED_RISK`, `RESOLVED`, or `RETURN_TRIGGERED`. `ACCEPTED_RISK` requires an attributable researcher judgment and cannot override a gate's mandatory failure condition. `RETURN_TRIGGERED` links an `EpistemicReturnRecord`.

## Skill responsibility map

| Skill | Required friction responsibility |
|---|---|
| formulating-research-question | Premise friction |
| scoping-argument-boundary | Overreach friction |
| mapping-concept-lineage | Novelty and lineage friction |
| conducting-literature-dialogue | Consensus friction |
| planning-humanities-argument | Claim–evidence friction |
| performing-close-reading | Interpretive friction |
| structuring-humanities-argument | Rhetorical-smoothing friction |
| stress-testing-argument | Counterargument friction |
| auditing-citations | Citation and support friction |
| checking-terminology-consistency | Semantic-drift friction |
| reviewing-manuscript | Structural-coherence friction |
| responding-to-peer-review | Reviewer–author friction |
| verifying-before-submission | Completion friction |
