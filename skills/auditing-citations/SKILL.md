---
name: auditing-citations
description: Use when citations, quotations, page numbers, bibliography entries, or source-supported claims must be checked for existence, metadata accuracy, textual fidelity, and claim–source fit.
version: 1.0.0
language: en
license: MIT
---

# Auditing Citations

## Purpose

Audit the evidentiary chain between a manuscript and its sources. This skill does not beautify a bibliography or infer missing publication details. It creates a traceable record showing what was checked, against which source, with what result, and what remains unresolved.

Citation accuracy has at least two distinct dimensions. **Bibliographic verification** asks whether the cited object exists and whether author, title, date, edition, journal, volume, issue, pages, DOI, archival identifier, and translator information are accurate. **Claim–source verification** asks whether the cited passage actually supports the sentence, interpretation, historical statement, or quotation to which it is attached. A record can pass the first test and fail the second.

## Contract

**Accepts** a manuscript, notes, bibliography, citation export, quotation list, source files, authoritative catalogue records, or a prior `CitationRecord` set.

**Requires** the text containing the citations and enough source access to distinguish checked items from inaccessible ones. Direct quotations require the exact edition or a clearly identified equivalent edition.

**Produces** normalized `CitationRecord` objects, an itemized audit table, discrepancy notes, submission-blocking issues, and a citation gate report.

**May produce** a corrected bibliography proposal, a source-access request list, duplicate-record map, or a list of claims that need weaker wording or different evidence.

**Fails when** the cited source cannot be identified, a quotation cannot be located, an edition or pagination conflict prevents reliable matching, or the requester asks the agent to invent or conceal missing details.

**Guarantees** that every audited item receives an explicit status and that inaccessible or mismatched items are not silently represented as verified.

**Does not guarantee** that inaccessible sources are accurate, that the bibliography is exhaustive, that a verified source makes the manuscript's interpretation correct, or that a journal will accept the citation style.

## When to use

Use this skill before submission, after AI-assisted drafting, after importing references from a manager, when direct quotations have been translated or paraphrased, when a reviewer questions a source, or whenever references were assembled from secondary mentions rather than primary consultation.

Do not wait until the final day when the manuscript contains many direct quotations. Citation auditing is most reliable when repeated after major drafting rounds and again at the submission gate.

## Inputs required

At minimum provide:

1. The manuscript or the passages containing citations.
2. The bibliography or reference list, if one exists.
3. Accessible source texts, scans, database records, or stable catalogue metadata.
4. The target citation style or journal instructions, if format is in scope.
5. A statement of which editions, translations, or archival versions the researcher actually used.

When any input is missing, record it as a limitation. Do not treat a citation string as evidence that the underlying work was consulted.

## Procedure

### 1. Create the audit inventory

Extract every in-text citation, footnote, endnote, direct quotation, epigraph, translated passage, data attribution, archival reference, URL, DOI, and bibliography entry. Assign a stable `CitationRecord` ID. Reconcile obvious duplicates without deleting provenance.

### 2. Classify citation function

Label what each citation is being asked to do:

- identify a source;
- support a factual statement;
- support an interpretive claim;
- establish a concept's lineage;
- document a direct quotation;
- provide background or further reading;
- support a methodological choice.

A source used only as background MUST NOT be reported as direct proof of a contested claim.

### 3. Verify bibliographic identity

Check author or editor, title, container title, publication year, edition, translator, volume, issue, page range, publisher, DOI, URL, archive, collection, and item number as relevant. Prefer the source itself, publisher metadata, DOI registry, library catalogue, or archival finding aid over copied citations from unrelated webpages.

Record discrepancies exactly. If two legitimate editions differ, preserve both identities and identify the edition used in the manuscript.

### 4. Verify direct quotations

Compare wording, spelling, punctuation, ellipses, brackets, emphasis, and surrounding context. Confirm page, paragraph, section, timestamp, image number, folio, or stable location. For translations, distinguish:

- published translation quoted directly;
- researcher's translation;
- AI-assisted draft translation requiring human review.

Do not silently modernize or improve quoted language.

### 5. Verify claim–source fit

Read enough surrounding context to determine whether the source supports the attached claim. Classify fit as:

- direct support;
- qualified support;
- contextual relevance only;
- support for a narrower claim;
- contradiction;
- unable to determine.

A shared keyword is not sufficient support. A citation to a theorist's name does not validate every later use of that theorist.

### 6. Check citation placement and scope

Determine whether a citation applies to one sentence, several sentences, or a whole paragraph. Flag ambiguous citation placement, citation clusters where no source is mapped to a specific claim, and paragraph-final citations that appear to support more than they actually do.

### 7. Reconcile bibliography and manuscript

Identify cited-but-unlisted works, listed-but-uncited works, duplicate identities, inconsistent author names, year suffix errors, broken cross-references, missing translators, and mismatched titles. Formatting corrections come after identity is secure.

### 8. Assign verification state

Use only explicit states:

- `verified-primary`
- `verified-secondary`
- `researcher-supplied`
- `inference`
- `unverified`
- `unknown`
- `disputed`

Do not use “verified” when only a search snippet or another bibliography was checked.

### 9. Determine blocking status

Submission-blocking issues include fabricated or absent sources, unverifiable direct quotations, materially wrong page numbers, citations that contradict the attached claim, and unresolved identity conflicts affecting the argument. Minor punctuation differences in a citation style are normally non-blocking.

### 10. Issue the gate report

Return `PASS` only when every citation has a status and no blocking item remains. Use `CONDITIONAL PASS` when non-blocking format issues or clearly listed access limitations remain. Return `FAIL` when any central quotation, evidentiary citation, or bibliographic identity is unverified or contradicted.

## Stop signals

Stop and request researcher action when:

- the source is inaccessible and no authoritative record is available;
- the manuscript cites a work that cannot be located;
- quotation wording materially differs from the source;
- edition or translation identity is unclear;
- a page number belongs to another edition;
- a source supports only a narrower claim than the manuscript makes;
- a secondary citation is presented as direct consultation;
- the requester asks for plausible missing details.

Do not “repair” these problems through guessing.

## Completion criteria

The skill is complete only when:

- every citation and bibliography item has a stable record;
- every direct quotation has a checked location or unresolved flag;
- every claim-bearing citation has a claim–source-fit status;
- bibliography and in-text references reconcile;
- discrepancies are separated into blocking and non-blocking groups;
- researcher decisions are identified;
- the final gate follows the documented evidence.

## Anti-fabrication rules

Never invent an author, title, page, DOI, issue number, archive identifier, quotation, or source content. Never use search-result snippets as substitutes for reading the relevant passage. Never convert a likely match into a verified identity. Never hide a failed citation by deleting it without reporting the affected claim. Never translate a quotation and present it as an established published translation unless that translation was checked.

When source access is partial, say exactly what was checked. “Metadata verified; passage not checked” is preferable to a polished but false assurance.

## Output format

Use `templates/citation-audit.md` and include:

1. Audit scope and source-access statement.
2. Citation inventory with record IDs.
3. Bibliographic verification result.
4. Quotation or passage verification result.
5. Claim–source-fit result.
6. Required correction.
7. Blocking status.
8. Counts by verification state.

### Gate report

```text
Gate: Citation Audit
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill:
```

## Good invocation

> Audit all citations and direct quotations in this manuscript against the supplied PDFs. Distinguish metadata verification from claim–source fit and fail the gate if a central quotation cannot be checked.

## Bad invocation

> Make the references look complete, supply plausible page numbers, and do not tell the reviewer which sources I could not access.

The bad invocation requests concealment and fabrication. The skill MUST refuse it and preserve the unresolved state.

## Next skills

- `checking-terminology-consistency` when translated names or concepts vary.
- `responding-to-peer-review` when the audit addresses reviewer concerns.
- `verifying-before-submission` after all blocking citation issues are resolved.
- `structuring-humanities-argument` when a claim must be narrowed after source mismatch.

## Limitations

An audit is bounded by source access, edition identity, language competence, and the quality of authoritative metadata. It can establish that a passage exists and is represented accurately; it cannot decide by itself whether a complex interpretation is persuasive. Specialist review may be required for rare languages, manuscripts, archival conventions, legal restrictions, or contested editions.
