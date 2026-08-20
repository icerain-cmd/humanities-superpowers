---
name: conducting-literature-dialogue
description: Use when a humanities researcher needs to transform verified sources into a structured scholarly conversation rather than a chronological list of summaries.
version: 2.0.0
language: en
license: MIT
---

# Conducting a Literature Dialogue

## Purpose

Organize sources around agreements, disagreements, methods, blind spots, and unresolved questions so that the literature review becomes an argument about a scholarly conversation. The skill supports positioning; it does not simulate reading sources that have not been supplied or verified.

## Contract

**Accepts**
- A bounded research question and scope.
- `SourceRecord` entries, bibliographic records, notes, excerpts, or verified summaries.
- Optional concept-lineage records and provisional claims.

**Requires**
- At least two usable sources for comparison.
- Clear provenance for each source description.
- Enough source content to identify a claim, method, object, or limitation.

**Produces**
- A literature-dialogue map organized by problem or position.
- Source-role assignments.
- Agreement, disagreement, and unresolved-question records.
- A bounded gap statement or a declaration that no gap has yet been established.
- A literature gate report.

**May produce**
- A search-needs list.
- Competing maps based on method, chronology, concept, or disciplinary tradition.
- A recommendation to postpone originality claims.

**Fails when**
- Sources are represented only by titles or unverified generated summaries.
- The user asks for a comprehensive review without a search corpus or scope.
- The proposed gap is merely “few studies exist” without evidence.
- Disagreement among sources cannot be reconstructed from available material.

**Guarantees**
- Every source role will be linked to supplied or verified material.
- Summary, interpretation, and inference will be distinguished.
- A gap will not be asserted unless the reviewed scope supports it.

**Does not guarantee**
- Exhaustiveness, systematic-review completeness, or originality.
- That the most important source has been found.
- That a scholarly disagreement is resolvable.

## When to use

Use after the research question and scope are stable enough to guide source selection. Use when a literature review reads as “Scholar A says…, Scholar B says…,” when the manuscript accumulates citations without defining positions, or when the researcher needs to identify where a new argument enters an existing debate.

Do not use this skill to generate citations from memory or to create an appearance of comprehensive coverage.

## Inputs required

For each source, provide as much of the following as possible:

- verified bibliographic record;
- source type and publication status;
- relevant passages or researcher notes;
- central claim;
- object or corpus;
- method or interpretive frame;
- evidence used;
- limitations or unresolved points;
- provenance and verification state.

Also provide the primary research question and current scope boundary.

## Procedure

### 1. Register source status

Create or review a `SourceRecord` for each item. Distinguish:

- directly read and verified;
- verified bibliographic record with partial reading;
- researcher-supplied notes;
- secondary report of another source;
- unverified lead.

Do not allow an unverified lead to function as established support.

### 2. Extract source positions

For each source, record:

- problem addressed;
- central claim;
- method;
- object and scope;
- evidence;
- key concept;
- limitation;
- relevance to the project.

Keep direct quotation separate from paraphrase and interpretation.

### 3. Cluster by scholarly problem

Group sources by the question they answer, not merely by publication date or author. Possible clusters include competing definitions, historical explanations, methodological divisions, interpretive schools, normative disputes, or different scales of analysis.

### 4. Assign source roles

A source may function as:

- foundation;
- definition;
- predecessor;
- method model;
- supporting evidence;
- counterposition;
- complication;
- contextual background;
- unresolved lead.

A prestigious name is not itself a role.

### 5. Reconstruct relations

Use explicit relation labels:

```text
A supports B on X but differs on Y.
C rejects A's causal explanation while retaining its object.
D changes the unit of analysis and therefore cannot be treated as a direct contradiction.
```

Distinguish genuine disagreement from different questions or scales.

### 6. Identify the unresolved space

A defensible gap may be:

- an unresolved contradiction;
- an untested assumption;
- an object omitted within a bounded conversation;
- a scale mismatch;
- a concept used inconsistently;
- a method unable to address a documented feature.

“Few studies exist” is insufficient without a documented search scope and relevance criterion.

### 7. Position the project

State whether the project extends, revises, combines, challenges, or reframes existing positions. Specify what it does not claim. The position must follow from the mapped dialogue, not from promotional language.

### 8. Generate search needs

List missing primary sources, counterpositions, recent work, language traditions, or empirical materials. Mark each as blocking or non-blocking.

### 9. Issue the gate report

Return `PASS` when major source roles and relations are grounded and the project position is bounded. Return `CONDITIONAL PASS` when a non-blocking cluster or recent source remains to be checked. Return `FAIL` when the map relies on unverified summaries, fabricates a gap, or lacks enough source content to establish dialogue.

## Stop signals

- A source is cited from memory without a verifiable record.
- The user requests “the latest scholarship” without web or database verification.
- The literature map excludes obvious counterpositions solely because they weaken the hypothesis.
- A gap claim is based on a handful of convenient sources.
- Secondary citations are presented as direct engagement with the primary source.
- The review claims comprehensiveness without a reproducible search strategy.

## Completion criteria

- Every included source has provenance and verification status.
- Sources are grouped by scholarly problem or position.
- Agreements and disagreements are expressed as specific relations.
- Different scales or questions are not mistaken for contradiction.
- The project’s position is explicit and bounded.
- Any gap claim states the reviewed scope and evidence.
- Missing searches and counterpositions are recorded.
- The gate report supports handoff to argument planning or requests further research.

## Anti-fabrication rules

- Do not invent sources, titles, quotations, abstracts, page numbers, DOI values, publication dates, or author positions.
- Do not claim to have read a source when only metadata or a secondary summary is available.
- Do not manufacture consensus, controversy, or neglect.
- Do not use citation quantity as evidence of representativeness.
- Do not upgrade a plausible inference about a source into a verified claim.

## Output format

```md
## Review scope
Research question:
Corpus searched or supplied:
Coverage limits:

## Source-status table
| Source | Provenance | Verification state | Role |

## Scholarly conversation
### Problem or position A
Sources:
Shared claim:
Differences:
Methods:
Unresolved issue:

## Relation map

## Project position
This project extends/revises/challenges/reframes:
It contributes:
It does not claim:

## Gap assessment
Status: established | provisional | not established
Reviewed scope:
Evidence:

## Search needs
Blocking:
Non-blocking:

## Gate report
Gate: Literature-dialogue gate
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill: planning-humanities-argument | mapping-concept-lineage
```

## Good invocation

> Build a literature dialogue from the eight articles and two book chapters I supplied. Group them by how they define platform mediation, distinguish direct reading from my notes, and state whether a gap is actually established within this corpus.

## Bad invocation

> Write a comprehensive literature review on AI and humanities with thirty real citations. I have not provided sources, so use plausible ones and say the field ignores my idea.

The request requires fabricated sources and an unsupported gap claim. The skill must return `FAIL` and identify the evidence required.

## Next skills

- `mapping-concept-lineage` when disagreement turns on unstable or translated concepts.
- `planning-humanities-argument` when the conversation and project position are sufficiently grounded.
- `auditing-citations` when source claims and bibliographic records need independent verification.

## Friction triggers

Create consensus friction when disagreement clusters, incompatible scales, counterpositions, or unverified summaries are flattened into a unified field account.

## Friction checks

Preserve specific agreements and disagreements, test whether apparent conflict addresses the same question, and flag excluded counterevidence or unsupported gap claims.

## Judgment boundary

The agent may map defensible positions but must not choose the project's final alignment or manufacture consensus. Strategic positioning requires researcher authorization.

## Evidence ledger updates

Assign each source a claim-specific standing, including `QUALIFIES`, `CONTRADICTS`, `INSUFFICIENT`, and `CONTEXT_ONLY`; verification alone never means support.

## Interpretation history impact

When the literature changes a source interpretation or project position, append the new version and preserve the earlier map.

## Possible epistemic return

New scholarship that materially changes the premise or concept may reopen question, scope, or lineage. A missing required source is repair-oriented rollback or pause, not epistemic return.

## Productive refusal

If consensus, neglect, comprehensiveness, or a gap cannot be established, state the reviewed corpus, coverage limits, bounded finding, and search needed.

## Gate impact

Unresolved central conflict may force `FAIL` or a researcher decision. Material source-role changes require rechecking argument and submission gates that depend on them.

## Limitations

This skill is not a systematic-review engine and cannot establish database completeness unless a reproducible search protocol and results are supplied. Humanities conversations may remain plural, incommensurable, or historically discontinuous; the map should preserve those conditions rather than force consensus.
