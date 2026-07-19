---
name: verifying-before-submission
description: Use when a humanities manuscript is about to be submitted or resubmitted and requires a final evidence-based gate covering argument, citations, terminology, files, author information, venue requirements, and disclosure.
version: 1.0.0
language: en
license: MIT
---

# Verifying Before Submission

## Purpose

Provide the final release gate for a manuscript package. This skill does not repeat every earlier method in full. It verifies that required audits were performed, that their blocking issues were resolved, that the submitted files correspond to the reviewed version, and that no unsupported claim of readiness is made.

A polished PDF is not evidence of scholarly readiness. Submission readiness is a package-level state supported by traceable checks.

## Contract

**Accepts** the final manuscript package, target venue instructions, author and funding information, prior gate reports, revision letter, supplementary files, declarations, and submission metadata.

**Requires** the exact files intended for submission, current venue requirements, and evidence from citation, terminology, manuscript, and peer-review gates where applicable.

**Produces** a package inventory, requirement matrix, unresolved-risk register, privacy and metadata check, final `GateReport`, and a precise `PASS`, `CONDITIONAL PASS`, or `FAIL` decision.

**May produce** a submission checklist, filename corrections, missing-document list, anonymization actions, or a release manifest with checksums.

**Fails when** central gate reports are absent, a blocking issue remains, the submitted file differs from the reviewed file, venue requirements cannot be checked, required declarations are missing, or the requester asks for readiness despite unresolved evidence.

**Guarantees** that the readiness decision is tied to documented checks and that unresolved blocking issues prevent a `PASS`.

**Does not guarantee** acceptance, legal compliance in every jurisdiction, factual truth beyond completed audits, successful file upload, or compatibility with an unknown submission system.

## When to use

Use immediately before first submission, revised submission, accepted-manuscript delivery, conference upload, book-chapter handoff, repository deposit, or any claim that a manuscript is “submission-ready.”

Run it again whenever the manuscript changes after the gate. Even a small edit can alter page numbers, citations, anonymization, word count, figures, or response-letter references.

## Inputs required

Provide:

1. Exact final manuscript file and all supplementary files.
2. Current venue author instructions or verified requirement summary.
3. Author names, affiliations, ORCID information, corresponding-author details, and anonymization status.
4. Abstract, keywords, title, running title, and word count where required.
5. Citation audit, terminology audit, manuscript review, and peer-review-response reports as applicable.
6. Funding, conflict-of-interest, ethics, data, AI-use, copyright, permission, and acknowledgments statements.
7. Figures, tables, captions, accessibility text, permissions, and source files where required.
8. A declaration of which file version is authoritative.

If the venue instructions are not available or current, the venue-compliance portion cannot pass.

## Procedure

### 1. Freeze and inventory the package

List every intended file with filename, role, version, modification date, and checksum where possible. Identify the authoritative manuscript. Exclude working notes, tracked-change files, personal data, hidden drafts, and unrelated attachments unless required.

### 2. Verify prior quality gates

Check the latest status and evidence for:

- research question and scope;
- argument and close reading;
- citation audit;
- terminology consistency;
- manuscript review;
- peer-review response for resubmission.

A prior `PASS` is invalidated if the relevant content changed afterward. Record which checks must be rerun.

### 3. Verify venue requirements

Create a requirement matrix covering format, genre, length, language, file type, title page, abstract, keywords, headings, notes, references, figures, tables, supplementary material, anonymization, declarations, and submission-system fields.

Use current official instructions. Do not infer requirements from another journal, an old author template, or a third-party blog.

### 4. Verify manuscript identity and integrity

Check title, author order, affiliations, corresponding author, ORCID, funding, acknowledgments, and version consistency. Ensure abstract, keywords, headings, tables, figures, appendices, notes, and references belong to the same manuscript version.

Confirm that response-letter page and line references match the final revised file.

### 5. Verify anonymization and privacy

For blinded review, inspect title page, manuscript text, acknowledgments, self-citations, file properties, comments, tracked changes, embedded paths, image metadata, supplementary files, repository links, and filenames. Do not remove information required by the venue; follow its blinding policy.

Check that personal, confidential, student, participant, peer-review, or archival data are not exposed improperly.

### 6. Verify citations and permissions

Confirm that no blocking citation issue remains and that revisions did not create new orphan references. Check permissions or fair-use documentation for images, tables, long quotations, translated material, archival reproductions, and third-party content as required.

This skill records permission status; it does not provide legal advice.

### 7. Verify declarations and responsible AI disclosure

Check required statements for funding, conflicts, ethics, consent, data availability, author contributions, originality, prior publication, preprints, and AI assistance. The disclosure must reflect actual use and the venue's policy. Do not invent compliance or conceal prohibited use.

### 8. Verify technical presentation

Inspect page numbers, line numbers, fonts, margins, headings, cross-references, table and figure numbering, captions, alternative text where required, equation and symbol rendering, hyperlinks, bibliography formatting, and file opening. Check that no placeholder, comment, broken field, or unresolved marker remains.

Search explicitly for markers such as:

```text
TODO
TBD
[CITATION NEEDED]
[AUTHOR DECISION REQUIRED]
XXX
placeholder
```

Do not remove an unresolved marker merely to pass the gate; resolve or report it.

### 9. Conduct package-difference check

Compare the final package with the version that passed prior review. Record post-review changes. If substantive claims, quotations, citations, terminology, or structure changed, route back to the relevant skill before deciding readiness.

### 10. Classify remaining issues

Use:

- **blocking**: prevents valid submission or makes a material scholarly or ethical claim unreliable;
- **non-blocking**: does not invalidate submission but should be corrected or disclosed;
- **researcher decision required**: cannot be decided procedurally;
- **external authority required**: editor, rights holder, ethics office, legal counsel, or specialist must decide.

### 11. Issue the final gate

Return `PASS` only when all mandatory requirements within scope are evidenced, no blocking issue remains, and the exact package has been checked. `CONDITIONAL PASS` is allowed only when the package may proceed under a clearly stated external condition that does not invalidate the current scholarly claims. Return `FAIL` for missing audits, unresolved citations, false revision claims, privacy exposure, missing declarations, requirement mismatch, or version inconsistency.

## Stop signals

Stop and fail or request action when:

- the exact final files are not available;
- official venue requirements cannot be verified;
- the manuscript changed after its last relevant audit;
- a central citation or quotation remains unverified;
- required author, ethics, funding, permission, or AI-use information is unknown;
- anonymization conflicts with venue policy;
- response-letter claims do not match the manuscript;
- hidden metadata exposes identities or confidential information;
- the requester asks for a `PASS` despite a blocker.

## Completion criteria

Completion requires:

- a frozen package inventory;
- a current venue-requirement matrix;
- verified prior gate statuses;
- author, anonymity, privacy, and declaration checks;
- citation, terminology, figure, table, permission, and metadata status;
- no unresolved placeholders;
- package/version consistency;
- explicit blocking and non-blocking lists;
- a final status supported by evidence.

## Anti-fabrication rules

Do not claim compliance with instructions that were not checked. Do not invent ethics approval, permission, funding, author consent, ORCID, word count, AI disclosure, or rights status. Do not report a file as inspected when only its filename is known. Do not turn missing information into “not applicable” without researcher confirmation.

A `FAIL` is correct when evidence is missing. The purpose of this skill is not to make every package pass.

## Output format

Use `templates/submission-gate.md` and include:

1. Authoritative package inventory.
2. Venue requirement matrix.
3. Prior gate status table.
4. Scholarly-content checks.
5. Citation and terminology checks.
6. Author, privacy, anonymization, and metadata checks.
7. Ethics, funding, permission, and AI disclosure checks.
8. Technical file checks.
9. Blocking and non-blocking issue registers.
10. Required next actions.

### Gate report

```text
Gate: Submission Verification
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
External authority required:
Required next action:
Verified package identifier:
Next skill:
```

## Good invocation

> Verify the exact files in this submission folder against the current journal instructions and prior audit reports. Fail the gate if the manuscript changed after citation audit or if any required disclosure is unknown.

## Bad invocation

> Mark this submission ready now. I do not have the final files or journal instructions, but the prose looks polished.

The bad invocation mistakes appearance for verified readiness and MUST receive `FAIL`.

## Next skills

- `auditing-citations` when references changed or remain unresolved.
- `checking-terminology-consistency` after late conceptual edits.
- `reviewing-manuscript` after substantive changes.
- `responding-to-peer-review` for mismatch between revision letter and manuscript.
- `using-humanities-superpowers` to route any failed gate.

## Limitations

Submission systems, policies, legal requirements, and ethical rules vary and can change. This skill depends on current official instructions and accurate researcher-supplied information. It cannot provide legal advice, guarantee upload success, or guarantee editorial acceptance. The final author remains responsible for every submitted file and declaration.
