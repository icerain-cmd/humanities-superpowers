---
name: mapping-concept-lineage
description: Use when a humanities argument depends on a concept whose history, competing definitions, translations, or boundaries must be reconstructed before the concept can support new claims.
version: 1.0.0
language: en
license: MIT
---

# Mapping a Concept Lineage

## Purpose

Reconstruct how a concept is named, transformed, contested, translated, and operationalized across relevant sources. The skill prevents theory-name accumulation, anachronism, and the presentation of a relabeled inherited concept as wholly original.

## Contract

**Accepts**
- One focal concept or term.
- A bounded research question and scope.
- Researcher-supplied sources, definitions, notes, or candidate predecessors.

**Requires**
- A working description of how the concept functions in the present project.
- At least one verified or researcher-supplied source associated with the concept.
- A declared language and disciplinary context where translation matters.

**Produces**
- A set of `ConceptRecord` entries.
- A lineage map showing inheritance, modification, rejection, and unresolved ambiguity.
- A boundary statement distinguishing the focal concept from adjacent terms.
- A novelty-status statement limited to what has actually been checked.
- A concept-lineage gate report.

**May produce**
- Competing lineage models.
- A translation ledger.
- A recommendation to rename, narrow, merge, or abandon the focal concept.

**Fails when**
- No source text or reliable definition is available for central predecessors.
- The proposed lineage is based only on name resemblance.
- Chronology or translation is invented.
- The researcher demands an originality claim before literature verification.

**Guarantees**
- Each lineage relation will be labeled as verified, supported, inferred, disputed, or unknown.
- Similarity, influence, inheritance, and direct citation will not be treated as equivalent.
- Concept boundaries and unresolved translation issues will remain visible.

**Does not guarantee**
- A complete intellectual history.
- Direct influence between thinkers unless documentary evidence supports it.
- That a newly coined term is original or useful.

## When to use

Use when a manuscript introduces a new concept, combines theorists from different traditions, translates key terms, or relies on a familiar term whose meaning shifts across periods. Use before presenting a concept as an intervention and before building an argument that depends on stable terminology.

Do not use the skill as a decorative genealogy that lists prestigious names without showing conceptual operations.

## Inputs required

1. Focal concept and working definition.
2. Function of the concept in the current argument.
3. Candidate predecessors, rivals, or adjacent terms.
4. Relevant source passages or verified bibliographic records where available.
5. Original-language terms and translations where relevant.
6. Scope boundary: which traditions, periods, and disciplines are included or excluded.

## Procedure

### 1. Register the focal concept

Create a `ConceptRecord` containing preferred term, variants, working definition, analytical function, provenance, and verification state. Separate the term’s name from the operation it performs in the argument.

### 2. Identify candidate relations

For each predecessor or adjacent concept, classify the proposed relation:

- direct citation or explicit inheritance;
- conceptual modification;
- critical rejection;
- functional analogy;
- lexical similarity only;
- possible but unverified relation.

Never collapse these categories into “influence.”

### 3. Establish chronology and source status

Verify publication order, editions, translations, and direct references where available. If not verified, mark them `unverified` or `unknown`. Do not infer historical transmission solely from conceptual resemblance.

### 4. Compare conceptual dimensions

For each concept, record:

- object addressed;
- problem solved;
- ontological or epistemological commitments;
- unit of analysis;
- mechanism or relation;
- normative stakes;
- exclusions;
- typical evidence.

### 5. Track translation risk

Record original term, translation variants, translator or edition when known, and semantic loss or drift. A translated English label must not erase distinctions present in the source language.

### 6. Build the lineage map

Represent relations with explicit labels such as:

```text
A --explicitly revised by--> B
A --functionally analogous to--> C
D --translation overlap, relation disputed--> E
```

Avoid a simple arrow when the relation is uncertain.

### 7. Test the focal concept’s necessity

Ask:

- Does the concept identify a phenomenon not adequately captured by existing terms?
- Is the difference substantive or merely lexical?
- Does the concept have stable inclusion and exclusion rules?
- Can it guide interpretation or only rename an intuition?
- What evidence would show that the concept is misapplied?

### 8. Bound the novelty claim

Use one of the following statuses:

- `not assessed`
- `terminological variation`
- `bounded modification`
- `new synthesis`
- `potentially novel, literature check incomplete`
- `novelty claim supported within reviewed scope`

Do not use “first” or “unprecedented” without a documented search and clear scope.

### 9. Issue the gate report

Return `PASS` when the focal concept has a clear function, differentiated neighbors, traceable sources, and bounded novelty status. Return `CONDITIONAL PASS` when one translation or predecessor relation remains unresolved but does not invalidate use. Return `FAIL` when the concept is indistinguishable from an existing term, historically unsupported, or internally unstable.

## Stop signals

- The lineage consists only of famous names.
- Direct influence is claimed without citation or archival evidence.
- A translated term is treated as identical across languages and periods.
- The focal concept changes definition to fit each example.
- The researcher asks the agent to “prove” originality.
- A central source is known only through an uncited summary.

## Completion criteria

- The focal `ConceptRecord` has a working definition and analytical function.
- At least two adjacent or predecessor concepts are compared when relevant.
- Every lineage edge has a relation label and verification state.
- Translation variants are recorded where applicable.
- Inclusion and exclusion boundaries are explicit.
- The novelty statement is proportional to the reviewed evidence.
- The next skill can use the concept without reconstructing its basic history.

## Anti-fabrication rules

- Do not invent quotations, terms in original languages, page numbers, editions, translators, or publication chronology.
- Do not state that one thinker influenced another without evidence.
- Do not fabricate scholarly consensus or neglect known disputes.
- Do not convert etymology into conceptual history without intermediate evidence.
- Do not label a renamed familiar idea “new” merely because the wording differs.

## Output format

```md
## Focal concept
Preferred term:
Variants:
Working definition:
Analytical function:
Verification state:

## Concept records
### Concept A
Source status:
Definition:
Problem addressed:
Relation to focal concept:
Relation status:

## Translation ledger
Original term:
Variants:
Risk of semantic drift:

## Lineage map

## Boundary statement
Included uses:
Excluded uses:
Adjacent concepts:

## Novelty status
Status:
Evidence reviewed:
Claim permitted:
Claim not permitted:

## Unresolved relations

## Gate report
Gate: Concept-lineage gate
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill: conducting-literature-dialogue
```

## Good invocation

> Map the lineage of “remediation” for my article. I have verified passages from Bolter and Grusin and notes on mediation in Benjamin and Manovich. Distinguish direct inheritance from functional analogy, and do not claim influence unless the sources support it.

## Bad invocation

> Connect Benjamin, Foucault, Deleuze, Haraway, and Manovich into a single lineage proving my new concept is completely original. Fill in any missing links.

The request demands fabricated continuity and unsupported novelty. The correct response is to reject the missing links and return a limited or failing map.

## Next skills

- `conducting-literature-dialogue` to position the stabilized concept within current scholarship.
- `checking-terminology-consistency` when the manuscript already uses multiple variants.
- `planning-humanities-argument` after conceptual boundaries and literature positions are sufficiently clear.

## Limitations

Conceptual lineages are selective reconstructions shaped by the research question. They cannot establish exhaustive intellectual history, unconscious influence, or reception across all languages and disciplines. Absence from the map is not proof of irrelevance.

This skill performs **conceptual lineage tracing**, not Foucauldian genealogy. It does not by itself reconstruct the historical conditions of emergence of a discourse, dispositifs of power/knowledge, institutional formation, subjectivation, or discontinuities in an archive. A project making those claims requires an explicitly stated archaeological or genealogical method and evidence appropriate to it.
