---
name: responding-to-peer-review
description: Use when authors must interpret real reviewer comments, decide how to revise a humanities manuscript, and produce a transparent point-by-point response grounded in actual changes.
version: 1.0.0
language: en
license: MIT
---

# Responding to Peer Review

## Purpose

Convert reviewer reports into a traceable revision process. This skill separates what the reviewer explicitly requested from what the author infers, classifies the scholarly issue behind each comment, and links every response to an actual manuscript change or a reasoned decision not to change.

The goal is neither automatic compliance nor rhetorical resistance. It is accountable revision.

## Contract

**Accepts** authentic reviewer or editor comments, the submitted manuscript, revision files, journal instructions, prior audit reports, and author decisions.

**Requires** the exact comments and enough manuscript context to locate the issue. A point-by-point response requires either completed revisions or an explicit planned-action status.

**Produces** normalized `ReviewerComment` and `RevisionAction` records, a comment classification, response strategy, manuscript change log, point-by-point response draft, unresolved conflicts, and a peer-review-response gate report.

**May produce** a revision plan, editor cover note, disagreement rationale, grouped response to overlapping comments, or requests for clarification.

**Fails when** comments are invented, reviewer identities or motives are guessed, claimed revisions do not exist, contradictory reviewer requests remain unresolved without an editor decision, or the author asks to conceal noncompliance.

**Guarantees** that each reviewer comment is accounted for and connected to a response status, manuscript location, and evidence of change or reasoned non-change.

**Does not guarantee** reviewer satisfaction, acceptance, correct interpretation of ambiguous comments, or resolution of conflicting editorial demands.

## When to use

Use after receiving formal reviewer or editor reports, during revision planning, while drafting the response letter, and before resubmission to verify that claimed changes are present.

Do not simulate peer review with this skill. Use `reviewing-manuscript` or `stress-testing-argument` for internal review. This skill requires real comments or clearly labeled hypothetical training material.

## Inputs required

Provide:

1. Full reviewer and editor comments, preserving numbering and wording.
2. The submitted manuscript and current revised version.
3. Journal instructions and deadline constraints.
4. Any editor prioritization among conflicting comments.
5. Author decisions, especially where revision would alter the thesis or exceed scope.
6. Existing citation, terminology, or manuscript review reports.

Redact personal data if necessary, but do not paraphrase away the substance of the comments before classification.

## Procedure

### 1. Preserve and identify each comment

Assign a stable ID such as `R1-C3`. Preserve the original wording. Separate bundled comments into sub-items while retaining their parent comment. Distinguish editor instructions from reviewer suggestions.

### 2. Classify the comment

Classify each item as one or more of:

- clarification;
- evidence request;
- citation or literature request;
- concept definition;
- scope challenge;
- argument objection;
- method concern;
- interpretation challenge;
- structural revision;
- terminology or translation;
- style or format;
- ethical or disclosure issue;
- misunderstanding caused by manuscript presentation;
- recommendation outside current scope.

This classification determines the appropriate skill and evidence needed.

### 3. Distinguish explicit request from inferred concern

Record:

- what the reviewer literally asks;
- the likely scholarly concern;
- confidence in that interpretation;
- whether clarification from the editor is needed.

Do not attribute hostility, ideology, incompetence, or hidden motives.

### 4. Assess validity and consequence

Evaluate the comment against the manuscript. Use one response strategy:

- accept and revise;
- accept in part and narrow;
- clarify without substantive change;
- disagree with evidence;
- defer as limitation;
- request editor clarification;
- mark outside scope with a bounded explanation.

“Reviewer is wrong” is not a sufficient strategy. A disagreement must identify the manuscript evidence, relevant source, scope, or methodological reason.

### 5. Plan revisions in dependency order

Some comments affect the thesis, scope, or terminology and therefore change responses to later comments. Build a revision sequence before editing. Route issues to appropriate skills:

```text
scope -> concepts -> evidence -> argument -> structure -> citations -> terminology -> style
```

Merge overlapping comments carefully, but answer each reviewer ID separately in the response letter.

### 6. Make or verify manuscript changes

For each action record:

- original location;
- revised location;
- old function or wording;
- new function or wording;
- reason for the change;
- evidence added or removed;
- status: planned, completed, verified, or blocked.

Do not say “revised as suggested” until the change is present in the current file.

### 7. Draft the response

A strong response normally contains:

1. Thanks or acknowledgement without excessive flattery.
2. A concise statement of the action or decision.
3. The reason where needed.
4. Exact manuscript location.
5. A brief quotation or summary of the revised text when useful.

Keep tone professional and specific. Avoid defensive biography, speculation about the reviewer, or claims that the change “fully resolves” the issue unless verified.

### 8. Handle disagreement transparently

When not following a recommendation:

- restate the concern fairly;
- identify shared ground;
- explain the manuscript's scope or method;
- provide evidence;
- state any compensating clarification or limitation added;
- invite editor guidance if the conflict is consequential.

A reasoned non-change is preferable to cosmetic compliance that damages the argument.

### 9. Reconcile the response letter and manuscript

Check every page, section, table, note, and reference cited in the response. Ensure numbering matches the revised file. Confirm that deleted passages are not still described as revised and that new sources appear in the bibliography.

### 10. Issue the gate report

Return `PASS` when every comment is accounted for, all claimed changes are verified, and no blocking conflict remains. Use `CONDITIONAL PASS` when an editor decision or specialist check remains but is explicitly documented. Return `FAIL` when comments are omitted, changes are falsely claimed, or central concerns remain unaddressed.

## Stop signals

Stop and request action when:

- the original comment is missing or paraphrased beyond recognition;
- reviewer requests conflict on the same issue and the editor has not prioritized them;
- a requested source cannot be accessed;
- compliance would require data, permissions, languages, or methods not available;
- the author asks to claim a revision that was not made;
- the response would disclose confidential or identifying information;
- the revision changes the thesis without researcher approval.

## Completion criteria

Completion requires:

- every comment has a stable ID and status;
- explicit request and inferred concern are distinguished;
- each response strategy is justified;
- claimed manuscript changes are verified at exact locations;
- citations and terminology affected by revision are reconciled;
- disagreements are evidence-based and respectful;
- unresolved editor decisions are explicit;
- the response gate follows from the record.

## Anti-fabrication rules

Do not invent reviewer comments, editorial preferences, page locations, revisions, sources, acceptance probabilities, or reviewer motives. Do not fabricate language such as “we have added extensive discussion” when only a sentence changed. Do not create supporting citations solely to appease a reviewer without checking relevance.

When the current manuscript file cannot be inspected, label actions `planned`, not `completed` or `verified`.

## Output format

Use `templates/reviewer-response.md`. For each comment include:

```text
Comment ID:
Original comment:
Issue classification:
Explicit request:
Inferred concern:
Response strategy:
Manuscript action:
Location:
Verification status:
Response text:
Remaining issue:
```

### Gate report

```text
Gate: Peer Review Response
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill:
```

## Good invocation

> Build a point-by-point response to these real reports. Preserve each comment, distinguish planned from verified changes, and flag the two conflicting requests for an editor decision.

## Bad invocation

> Invent a persuasive response saying we made all requested changes, even though the revised manuscript is not available.

The bad invocation requires false claims and MUST be refused.

## Next skills

- `scoping-argument-boundary` for scope conflicts.
- `stress-testing-argument` for substantive objections.
- `auditing-citations` for requested sources and quotation checks.
- `checking-terminology-consistency` after conceptual revisions.
- `verifying-before-submission` before resubmission.

## Limitations

Reviewer comments may be ambiguous, inconsistent, or based on disciplinary assumptions not fully stated. The skill cannot know reviewer intentions or guarantee acceptance. Editors retain authority over conflicting requests, and authors retain responsibility for intellectual decisions and accurate claims about revisions.
