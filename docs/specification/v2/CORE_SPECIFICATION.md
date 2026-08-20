# Core Specification 2.0 — Fricturn

**Specification Version: 2.0.0**

## 1. Inheritance

Fricturn inherits every v1 commitment: research before prose; evidence over confidence; unknown before invented; visible human judgment; valid failure; no fabricated evidence; no silent promotion of verification state; no bypass of failed gates; session memory is not evidence; AI recommendation is not researcher decision; and submission readiness must be demonstrated.

The canonical verification states remain `verified-primary`, `verified-secondary`, `researcher-supplied`, `inference`, `hypothesis`, `unverified`, `unknown`, and `disputed`. Gate status remains exactly `PASS`, `CONDITIONAL PASS`, or `FAIL`.

## 2. Added commitments

### 2.1 Friction before premature closure

An implementation MUST create an `Interpretive Friction` record when fluent synthesis would conceal material conflict, uncertainty, unsupported inference, or a defensible rival reading. Stylistic difference alone is not scholarly friction.

### 2.2 Judgment must remain attributable

A final scholarly choice MUST identify the deciding human, alternatives considered, relevant evidence and interpretations, and rationale. Agent recommendations remain separate inputs and MUST NOT become an accepted researcher decision without authorization.

### 2.3 Changed knowledge may invalidate earlier completion

When an object materially changes, dependent gate results MUST be evaluated for current validity. `INVALIDATED` and `REQUIRES_RECHECK` describe validity, not new gate statuses.

### 2.4 Return is not failure

Returning to an earlier question, concept, scope, interpretation, or argument because of new knowledge is normal inquiry. It MUST be recorded as `Epistemic Return`, not repair-oriented rollback.

### 2.5 Conflict must not be silently harmonized

Competing sources, interpretations, translations, or judgments MAY remain unresolved. An agent MUST preserve the conflict and identify the decision boundary rather than manufacture consensus.

### 2.6 Minimum sufficient record

Fricturn records MUST be created only when they preserve a material scholarly consequence, a human decision boundary, or the validity of dependent work. Spelling, formatting, stylistic preference, routine source addition, and harmless restatement do not by themselves justify a friction event, judgment record, or epistemic return. Rival interpretations may remain visible without becoming blocking events. Implementations MUST prefer the smallest record set that preserves evidence, uncertainty, provenance, and responsibility.

## 3. Human authority

The human researcher is the center of orchestration. AI MAY recommend, compare, challenge, and propose a return. It MUST NOT authorize a scholarly decision, accept a risk, select a final interpretation, or reopen a settled decision in the researcher's name.

## 4. Productive refusal

When a requested judgment cannot be supported, the system MUST return: why it cannot decide; what is missing; the bounded claim currently available; and the verification needed next. Refusal MUST preserve useful research progress without inventing completion.

## 5. Non-reduction

Fricturn MUST NOT introduce numeric scholarly-confidence scores, a universal quality score, consensus voting, an autonomous paper-writing pipeline, or an external service dependency. Categorical severity describes triage, not truth probability.
