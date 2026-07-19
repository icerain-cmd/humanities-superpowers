# Core Specification

## 1. Purpose

Humanities Superpowers is a structured workflow for AI-assisted humanities research. Its central design claim is that fluent language generation must be subordinated to explicit scholarly judgment.

A conforming implementation MUST make it harder—not easier—to pass an unsupported claim, fabricated citation, unstable concept, or unresolved objection as finished scholarship.

## 2. Design commitments

### 2.1 Research before prose

A skill MUST NOT treat polished prose as evidence that the underlying research object is complete. When a task begins with a broad topic, the workflow SHOULD stabilize the research question, scope, source state, and argument structure before stylistic work.

### 2.2 Unknown before invented

When required information is unavailable or unverified, a skill MUST represent it as `unknown`, `unverified`, or `researcher decision required`. It MUST NOT fill the gap with plausible details.

### 2.3 Evidence over confidence

A completion claim MUST point to observable artifacts: a question statement, scope boundary, argument map, source record, terminology ledger, objection log, revision trace, or gate report.

### 2.4 Human responsibility remains visible

The researcher remains responsible for source selection, interpretive judgment, ethical decisions, originality claims, and submission. A skill MUST identify decisions that require researcher approval.

### 2.5 Failure is a valid outcome

A gate MAY return `FAIL`. A failed gate is not a software malfunction when it accurately identifies a blocked scholarly condition.

## 3. Required execution cycle

Every core skill MUST implement the following abstract cycle:

1. **Intake** — identify supplied materials, constraints, and missing inputs.
2. **Classification** — distinguish research objects and verification states.
3. **Operation** — perform the skill-specific procedure.
4. **Challenge** — test for stop signals, counterevidence, and category errors.
5. **Record** — produce a structured output and unresolved-item list.
6. **Gate** — apply observable completion criteria.
7. **Handoff** — name the next appropriate skill or return to an earlier stage.

A skill MAY compress steps in presentation, but it MUST preserve their logical function.

## 4. Verification states

Every factual or bibliographic element that materially supports a scholarly claim MUST be assigned one of these states:

- `verified-primary`: checked against an authoritative primary source or the source itself;
- `verified-secondary`: checked against a reliable secondary source;
- `researcher-supplied`: supplied by the researcher but not independently checked by the agent;
- `inference`: reasoned from identified evidence;
- `hypothesis`: provisional explanation requiring testing;
- `unverified`: plausible but not checked;
- `unknown`: information not available;
- `disputed`: reliable sources or interpretations conflict.

A skill MUST NOT silently promote one state into a stronger state.

## 5. Gate statuses

Every quality gate MUST return exactly one status:

- `PASS` — all blocking criteria are met.
- `CONDITIONAL PASS` — no fatal blocker remains, but named researcher decisions or non-blocking risks remain.
- `FAIL` — at least one blocking criterion remains unmet.

The status MUST be accompanied by evidence checked, blockers, risks, required decisions, next action, and next skill.

## 6. Minimal scholarly units

The framework recognizes the following minimal units:

- research question;
- scope boundary;
- concept record;
- source record;
- claim;
- evidence item;
- interpretation;
- inference;
- argument node;
- objection;
- terminology entry;
- citation record;
- reviewer comment;
- revision action;
- gate report.

Their normative definitions appear in the Research Object Model.

## 7. Non-guarantees

No conforming skill guarantees:

- truth;
- originality;
- publication;
- complete literature coverage;
- correct interpretation of every source;
- compliance with every journal or institutional policy;
- elimination of hallucination.

A skill SHOULD state what risk it reduces and what it cannot establish.

## 8. Privacy and research integrity

A skill MUST warn before exposing confidential manuscripts, private peer-review material, personal data, embargoed archives, or restricted research materials to external systems. It MUST NOT claim that a workflow is private or secure without evidence about the deployment environment.

## 9. Compatibility

Harness-specific wrappers MAY differ, but the normative skill body MUST remain portable Markdown unless a platform requires additional metadata. Platform-specific files MUST NOT weaken anti-fabrication or gate requirements.

## 10. Versioning

Changes follow semantic intent:

- patch: clarification without changed obligations;
- minor: backward-compatible additions;
- major: changed required behavior or object schema.

Draft specifications use a prerelease suffix until all core skills pass contract conformance.
