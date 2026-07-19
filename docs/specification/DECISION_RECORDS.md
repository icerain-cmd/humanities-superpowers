# Specification Decision Records

## SDR-001 — Use research objects without reducing interpretation to data

**Decision:** Define a minimal object model for handoffs, provenance, and validation.

**Reason:** Skills need stable interfaces. The model records methodological state; it does not claim that interpretation is computationally reducible.

**Consequence:** Contributors must name inputs and outputs but may retain discipline-specific prose and methods.

## SDR-002 — Separate verification from truth

**Decision:** Use verification states that describe what has been checked.

**Reason:** An agent can document verification activity but cannot guarantee truth.

**Consequence:** `verified` must always imply a traceable check, not confidence.

## SDR-003 — Permit FAIL as a successful execution

**Decision:** A gate may complete successfully while returning FAIL.

**Reason:** Blocking unsupported scholarship is a core function.

**Consequence:** Technical success and scholarly readiness are distinct.

## SDR-004 — Preserve researcher-supplied provenance

**Decision:** Researcher-provided information is not automatically source-verified.

**Reason:** This prevents accidental laundering of notes into citations.

**Consequence:** Skills must retain provenance through transformations.

## SDR-005 — Do not make prose generation a core skill

**Decision:** Core skills structure and test research rather than autonomously authoring a paper.

**Reason:** The project supports judgment and argument, not replacement authorship.

**Consequence:** `structuring-humanities-argument` may reorganize researcher material but must mark substantive additions.

## SDR-006 — Keep the core small

**Decision:** Maintain 13 core scholarly skills plus one router for v1.0.

**Reason:** Coverage is less important than coherence and testability.

**Consequence:** New proposals default to profiles or experimental extensions.
