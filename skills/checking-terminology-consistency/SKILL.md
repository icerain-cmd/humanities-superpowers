---
name: checking-terminology-consistency
description: Use when a manuscript contains recurring concepts, translations, abbreviations, proper names, or near-synonyms whose meanings and forms must remain stable across the argument.
version: 2.0.0
language: en
license: MIT
---

# Checking Terminology Consistency

## Purpose

Control conceptual drift without flattening meaningful variation. This skill distinguishes harmless stylistic variation from changes that alter the argument's object, level of analysis, historical claim, translation, or normative force.

Humanities manuscripts often use several adjacent terms because sources use different vocabularies, translations vary, or a concept develops across sections. Consistency does not mean replacing every word with one preferred label. It means making every variation accountable.

## Contract

**Accepts** a manuscript, chapter set, terminology ledger, concept map, translation notes, style sheet, or reviewer comments about unclear terminology.

**Requires** the text to be checked and, for central concepts, provisional definitions or evidence of how the researcher intends the terms to differ.

**Produces** a normalized `TerminologyEntry` ledger, occurrence map, drift analysis, recommended actions, unresolved researcher decisions, and a terminology gate report.

**May produce** a translation table, capitalization and hyphenation sheet, abbreviation policy, proper-name authority list, or proposed definition revisions.

**Fails when** central terms have no recoverable meaning, two terms are used interchangeably despite incompatible definitions, a translation choice cannot be justified, or the requester asks the agent to hide conceptual inconsistency through stylistic editing.

**Guarantees** that each audited central term is linked to an explicit definition, distinction, status, and recommended treatment.

**Does not guarantee** that the chosen concept is philosophically correct, that one translation is universally authoritative, or that terminological uniformity will make the argument persuasive.

## When to use

Use after the central concepts have been provisionally defined, after merging chapters written at different times, after translation or multilingual research, before manuscript review, after renaming a key concept, or when reviewers report that several terms seem interchangeable.

Use it early enough that terminology changes can still propagate through the argument map, examples, headings, abstract, and keywords.

## Inputs required

Provide:

1. The manuscript or selected chapters.
2. A list of central and secondary terms, if available.
3. Definitions, concept-lineage notes, or source-language forms.
4. Target language and preferred transliteration or naming conventions.
5. Any journal style requirements affecting capitalization, italics, abbreviations, or translated titles.

If no definitions exist, the skill may create a provisional ledger but MUST mark entries requiring researcher definition.

## Procedure

### 1. Build the term inventory

Extract recurring concepts, technical terms, translated terms, proper names, abbreviations, hyphenated forms, capitalized labels, analytic categories, period names, and coined expressions. Rank them as central, supporting, source-specific, descriptive, or stylistic.

### 2. Establish canonical entries

For each central term record:

- canonical form;
- source-language form where relevant;
- definition in this manuscript;
- what the term includes;
- what it excludes;
- level of analysis;
- historical or disciplinary location;
- permitted variants;
- prohibited substitutions;
- first-definition location.

A canonical form is a manuscript decision, not a claim that other scholarship must use the same terminology.

### 3. Map occurrences and variants

Locate singular and plural forms, capitalization changes, abbreviations, translations, spelling variants, and near-synonyms. Record section and local context. Do not normalize before examining whether a variation is meaningful.

### 4. Classify variation

Assign each variation one category:

- exact synonym permitted by style;
- grammatical variation;
- source quotation that must remain unchanged;
- historical vocabulary requiring distinction;
- disciplinary vocabulary requiring explanation;
- translation variant;
- concept drift;
- scope drift;
- level-of-analysis shift;
- unresolved ambiguity.

For example, “platform,” “platform infrastructure,” and “platform capitalism” are not automatically interchangeable. Their relation must be stated.

### 5. Test definition stability

Compare every central occurrence with the canonical definition. Ask:

- Does the term name the same object?
- Is the same analytical scale being used?
- Has descriptive language become normative?
- Has a metaphor become an ontological claim?
- Has a local category become universal?
- Has a theorist's term been detached from its historical function?

Flag changes that alter inference or evidence requirements.

### 6. Test relational distinctions

Central concepts often depend on boundaries between adjacent terms. Create explicit contrast pairs such as:

```text
mediation / remediation
memory / storage
subject / position
influence / similarity
presence / authenticity
```

For each pair state whether the manuscript treats them as distinct, nested, overlapping, historically related, or interchangeable. Inconsistent relations are more serious than spelling variation.

### 7. Audit translations and proper names

Record original terms, transliteration system, published translation where used, and the researcher's chosen translation. Preserve quoted translations exactly. Where several translations are defensible, explain the manuscript's choice at first use rather than pretending universal consensus.

Check author names, titles, institutional names, dates, capitalization, diacritics, and romanization consistently.

### 8. Propose actions

Use one of the following actions for every flagged item:

- retain;
- normalize;
- define at first use;
- distinguish explicitly;
- replace;
- restrict to quotation;
- move to historical vocabulary note;
- request researcher decision.

Do not perform global replacement when context changes meaning.

### 9. Propagate approved changes

After the researcher approves a decision, update headings, abstract, keywords, tables, diagrams, argument maps, examples, and conclusion. Record the change in the ledger. A term renamed in prose but left unchanged in the research question creates a new inconsistency.

### 10. Issue the gate report

Return `PASS` when central terms are defined and their variations are either consistent or explicitly justified. Return `CONDITIONAL PASS` for non-blocking style inconsistencies or documented translation alternatives. Return `FAIL` when concept drift changes the argument, a central distinction collapses, or unresolved terminology makes claims ambiguous.

## Stop signals

Stop and request a researcher decision when:

- a coined term has multiple incompatible definitions;
- a translation choice affects the thesis;
- two adjacent concepts cannot be distinguished from the manuscript;
- normalization would alter a quotation or historical vocabulary;
- the same term shifts between object, method, and value judgment;
- the proposed replacement would broaden or narrow the claim;
- disciplinary specialists may reasonably dispute the translation.

## Completion criteria

Completion requires:

- a ledger for every central term;
- definitions and exclusions where needed;
- occurrence and variant mapping;
- explicit treatment of near-synonyms;
- translation and proper-name decisions;
- approved corrections propagated across the manuscript;
- unresolved decisions listed rather than hidden;
- a terminology gate supported by recorded evidence.

## Anti-fabrication rules

Do not invent original-language forms, etymologies, historical first uses, translator names, or authoritative consensus. Do not claim that two terms are equivalent because a dictionary offers overlapping glosses. Do not fabricate quotations to justify a definition. Do not silently attribute the researcher's coined distinction to an established scholar.

When the source-language text has not been consulted, label the form `researcher-supplied` or `unverified` as appropriate.

## Output format

Use `templates/terminology-ledger.md`. Include:

1. Canonical term.
2. Definition and exclusion.
3. Source-language form and translation status.
4. Permitted and prohibited variants.
5. Occurrence summary.
6. Drift type.
7. Recommended action.
8. Researcher decision.
9. Propagation status.

### Gate report

```text
Gate: Terminology Consistency
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill:
```

## Good invocation

> Audit how this manuscript uses “mediation,” “remediation,” and “platform mediation.” Preserve source quotations, identify level-of-analysis shifts, and require my decision where normalization would change the thesis.

## Bad invocation

> Replace every similar-looking term with one word so the paper appears consistent, even if the theorists use them differently.

The bad invocation confuses visual uniformity with conceptual consistency and MUST be rejected.

## Next skills

- `mapping-concept-lineage` when a distinction depends on historical derivation.
- `structuring-humanities-argument` when approved terms must be propagated.
- `reviewing-manuscript` for whole-manuscript evaluation.
- `verifying-before-submission` after terminology blockers are resolved.

## Friction triggers

Create semantic-drift friction when a term changes concept, scale, translation, historical function, or normative force; spelling variation alone is not friction.

## Friction checks

Compare each occurrence to the canonical ConceptRecord and distinguish harmless form variation from conceptual or translation instability.

## Judgment boundary

The agent may present translation and naming alternatives, but canonical adoption that affects the thesis requires an attributable researcher decision.

## Evidence ledger updates

Record sources used to justify definitions and translations with claim-specific standing. Dictionary overlap alone is `INSUFFICIENT` for conceptual identity.

## Interpretation history impact

When terminology changes an interpretation's frame, append a new interpretation version; do not retroactively normalize historical readings.

## Possible epistemic return

A new translation or conceptual distinction may reopen lineage, question, interpretation, or argument. Mechanical inconsistency repair remains rollback.

## Productive refusal

When no translation can be authorized, preserve alternatives, describe semantic stakes, give bounded wording, and request specialist or researcher judgment.

## Gate impact

Material ConceptRecord or translation change can invalidate terminology, interpretation, argument, citation-fit, review, and submission validity through explicit dependencies.

## Limitations

Terminology auditing cannot settle all interpretive disputes. Different disciplines and translations may support several defensible choices. The skill makes choices and uncertainties visible; final conceptual and translation responsibility remains with the researcher and, where needed, a language or field specialist.
