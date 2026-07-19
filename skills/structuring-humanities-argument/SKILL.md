---
name: structuring-humanities-argument
description: Use when a researcher has an approved argument map, source-grounded notes, interpretations, and draft passages that need organization and logical repair without delegating the original scholarly contribution to the agent.
version: 1.0.0
language: en
license: MIT
---

# Structuring a Humanities Argument

## Purpose

Organize researcher-provided intellectual material into a coherent section or manuscript while preserving provenance, uncertainty, and authorial responsibility. This skill repairs sequence, paragraph function, transitions, redundancy, and missing warrants; it is not a ghostwriting license.

## Contract

**Accepts**
- An approved argument map or thesis-and-claims structure.
- Researcher-authored notes, draft passages, definitions, interpretations, and verified evidence.
- Genre, audience, length, and stylistic constraints.

**Requires**
- A researcher-approved thesis or central claim.
- Enough evidence and interpretation to support the requested unit.
- Clear separation, where possible, among source language, researcher language, and agent-proposed connective language.

**Produces**
- A structured outline, paragraph plan, or revised draft based on supplied material.
- Inline provenance and gap markers.
- A provenance note describing transformations.
- A structuring gate report.

**May produce**
- Alternative sequences with trade-offs.
- A list of surplus or misplaced material.
- `FAIL` when the requested contribution would need to be invented.

**Fails when**
- No thesis or argument map has been approved.
- The evidence base is too thin for the requested prose.
- The agent cannot distinguish quotation, paraphrase, and researcher-authored claim.
- The request asks the agent to invent the scholar’s original theory, interpretation, or personal voice.

**Guarantees**
- New factual and bibliographic claims will not be introduced without explicit support.
- Missing warrants and author decisions will remain marked.
- The provenance note will distinguish reordering, compression, paraphrase, and newly proposed connective language.

**Does not guarantee**
- Originality, stylistic excellence, publication readiness, or authentic representation of the researcher’s voice.
- That structurally coherent prose is substantively correct.

## When to use

Use after `planning-humanities-argument` and source-grounded analysis. Use when notes are rich but unordered, when paragraphs lack functions, when transitions conceal logical gaps, or when revisions require moving, compressing, or splitting material.

Do not use from a title alone. Do not ask this skill to simulate a personal voice, hide AI involvement, invent a theoretical contribution, or create citations to support missing claims.

## Inputs required

Collect:

1. Approved thesis and claim map.
2. Target unit: paragraph, subsection, chapter, article, response letter.
3. Researcher-authored notes and passages.
4. Verified evidence and citation records.
5. Definitions and terminology ledger.
6. Audience, venue, length, and citation style.
7. Permissions concerning paraphrase and line editing.

Identify each input’s provenance before restructuring.

## Procedure

### 1. Inventory and label materials

Classify supplied items as claim, evidence, quotation, paraphrase, observation, interpretation, inference, context, transition, or unresolved note. Mark uncertain provenance immediately.

### 2. Align with the argument map

Assign each item to a claim and section function. Place unmatched material in `Surplus / unresolved placement` rather than forcing it into the draft.

### 3. Build paragraph contracts

For each paragraph define:

```text
Function
+ Claim
+ Evidence
+ Analysis
+ Warrant
+ Link forward
```

Not every paragraph needs all elements, but every paragraph needs a declared function and relation to the argument.

### 4. Separate connective work from substantive judgment

The agent may propose order, signposting, compression, and explicit warrants already latent in supplied material. When a transition requires a new substantive claim, insert `[AUTHOR DECISION REQUIRED]` rather than supplying it as fact.

### 5. Repair sequence

Order paragraphs by inferential need: definition before application, observation before interpretation, evidence before generalization, objection before qualified conclusion. Preserve deliberate nonlinear form only when its epistemic purpose is stated.

### 6. Control repetition

Distinguish productive recurrence from redundancy. Consolidate repeated definitions and claims, but preserve repeated textual features when repetition is itself evidence.

### 7. Mark gaps visibly

Use:
- `[EVIDENCE NEEDED]`
- `[WARRANT NEEDED]`
- `[CONTEXT VERIFICATION NEEDED]`
- `[AUTHOR DECISION REQUIRED]`
- `[TERMINOLOGY DECISION REQUIRED]`
- `[CITATION VERIFICATION NEEDED]`

Markers must not be silently removed during polishing.

### 8. Preserve epistemic status

Do not upgrade hypothesis to conclusion, interpretation to fact, or researcher-supplied context to verified history. Retain disagreement and qualification.

### 9. Produce provenance notes

For each substantial block record whether it was retained, reordered, compressed, lightly edited, paraphrased from supplied text, or newly proposed as connective language. Do not claim exact authorship attribution when collaboration is entangled; state the limits.

### 10. Run paragraph-function audit

Check for evidence dumps, theory-name paragraphs, unearned conclusions, delayed definitions, and transitions that merely announce topic changes. Verify that each paragraph advances, qualifies, supports, or tests a claim.

### 11. Issue the gate report

Return `PASS` only when the requested unit is structurally coherent and no blocking authorship or evidence gap remains. Return `CONDITIONAL PASS` when visible non-blocking markers remain. Return `FAIL` when original contribution or evidence would need invention.

## Stop signals

Stop when:
- the user asks for a “complete original paper” from a title or abstract;
- source and researcher language are mixed without attribution;
- the only way to connect sections is to invent a claim;
- a requested rewrite would suppress uncertainty or disagreement;
- a personal style imitation is requested to conceal provenance;
- unsupported citations are required to make prose appear complete.

## Completion criteria

Complete only when:
- each paragraph or section has an argumentative function;
- material is aligned with the argument map;
- no unsupported factual or bibliographic claims were added;
- all missing decisions and warrants are visibly marked;
- terminology is stable or flagged;
- provenance transformations are documented;
- the gate report records residual risks and next action.

## Anti-fabrication rules

- Do not invent original contribution, interpretation, evidence, or citations.
- Do not imitate a living researcher’s voice to obscure authorship.
- Do not erase unresolved markers for fluency.
- Do not merge contradictory sources into false consensus.
- Do not present agent-proposed connective language as verified scholarship.
- Do not infer permissions to rewrite quoted or archival material.

## Output format

```md
## Structural plan
Target unit:
Primary function:
Claims advanced:

## Revised structure or draft
[Use provenance and gap markers inline.]

## Surplus / unresolved placement

## Provenance note
Retained:
Reordered:
Compressed:
Paraphrased from supplied material:
Agent-proposed connective language:
Limits of attribution:

## Gate report
Gate: Argument-structuring gate
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill: stress-testing-argument
```

## Good invocation

> Reorganize these researcher-written notes and verified passages according to the approved argument map. Mark missing warrants and distinguish all newly proposed connective language.

## Bad invocation

> Write my original theoretical contribution in my personal style from this title and make the citations look complete.

The bad invocation delegates authorship and requests deceptive completion.

## Next skills

- `stress-testing-argument` to expose structural and substantive vulnerabilities.
- `checking-terminology-consistency` after the sequence stabilizes.
- `reviewing-manuscript` for whole-manuscript evaluation.

## Limitations

The boundary between legitimate structuring assistance and substantive co-authorship varies by institution, venue, and research culture. Researchers must follow applicable disclosure and authorship policies. Provenance notes improve transparency but cannot reconstruct every micro-level contribution with certainty.
