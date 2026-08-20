# Integrated Conformance

## Fricturn 2.0 extension

Integrated conformance also runs `scripts/run_v2_tests.py`. It verifies unsupported-fluency failure, source verification versus evidential standing, counterevidence preservation, rival interpretation, agent disagreement, productive refusal, bounded gate invalidation, append-only judgment and interpretation history, authorized epistemic return, and no-op return behavior. These checks do not alter the 13+1 skill count or routing vocabulary.

## Purpose

Integrated conformance tests whether Humanities Superpowers behaves as one research workflow rather than 13 core research skills plus 1 Level 3 router. It checks state transitions, handoffs, rollback targets, gate preservation, session continuity, and the alignment of examples, templates, schemas, and public documentation.

This phase does **not** claim that every AI harness will make identical judgments. The deterministic test suite verifies repository contracts and declared routing behavior. Cross-harness behavioral evaluation remains a separate empirical task.

## Conformance dimensions

### 1. Route completeness

Every scenario MUST begin with a declared research state and end with one of these decisions:

- `PROCEED`
- `PAUSE`
- `ROLLBACK`
- `RESEARCHER_DECISION_REQUIRED`
- `STOP`

### 2. Gate preservation

A failed gate MUST NOT be silently converted into success. A later step MAY resume only after the blocking issue has a recorded resolution or the claim has been narrowed so that the issue is no longer blocking.

### 3. Earliest-cause rollback

Rollback MUST target the earliest skill capable of repairing the causal defect. A citation problem caused by an unsupported central claim returns to argument planning, not merely citation formatting.

### 4. Provenance continuity

Researcher-supplied, verified, inferred, hypothetical, unknown, and disputed states MUST remain distinguishable across handoffs.

### 5. Session resumability

A suspended session MUST preserve:

- current state;
- completed skills and gate results;
- blocking issues;
- researcher decisions;
- next valid action;
- restrictions on completion claims.

### 6. Public-description fidelity

README claims MUST match implemented artifacts. The repository MUST NOT advertise guarantees, automated truth, automatic publication readiness, or behavioral parity across agent harnesses.

## Integrated test classes

1. **Clean forward path** — idea to a conditional submission gate.
2. **Scope rollback** — evidence cannot support the breadth of the claim.
3. **Argument rollback** — citation audit exposes a central unsupported inference.
4. **Researcher decision** — two defensible interpretations require authorial choice.
5. **Session resume** — work resumes without promoting unverified material.
6. **Adversarial stop** — fabricated citations or concealed AI authorship are requested.
7. **Submission failure** — unresolved central citations remain at deadline.
8. **Peer-review loop** — reviewer comments produce verified manuscript changes before response completion.

## Release criterion

Phase 3-F passes when:

- all 14 `SKILL.md` files (13 core research skills and 1 router) are represented in at least one integrated scenario;
- every routing decision appears in the suite;
- every substantive skill has at least one incoming or outgoing handoff;
- rollback, pause, researcher-decision, and stop paths are exercised;
- examples and templates conform to their declared formats;
- deterministic validation reports zero errors;
- unresolved behavioral questions are documented rather than hidden.
