# Research Object Model

## 1. Purpose

The object model provides a shared vocabulary for skills. It does not force humanities research into a database metaphor; it makes handoffs and omissions visible.

Every object has four common fields:

```yaml
id: stable-local-identifier
status: draft | active | superseded | blocked | accepted
verification_state: verified-primary | verified-secondary | researcher-supplied | inference | hypothesis | unverified | unknown | disputed
provenance: source, researcher, skill, or transformation record
```

## 2. ResearchQuestion

Represents the inquiry that organizes a project.

Required fields:

- `question_text`
- `object`
- `problem_or_tension`
- `analytical_relation`
- `answerability_note`
- `required_evidence`

Optional fields:

- subordinate questions;
- provisional hypothesis;
- disciplinary audience;
- significance claim.

Invalid state: a question that contains its preferred answer as an unquestioned premise.

## 3. ScopeBoundary

Defines what the argument includes and excludes.

Required fields:

- corpus or object range;
- time range;
- geographic or linguistic range where relevant;
- analytical level;
- excluded claims;
- practical constraints.

A scope boundary MUST distinguish deliberate exclusion from accidental omission.

## 4. ConceptRecord

Represents a concept used analytically.

Required fields:

- preferred term;
- working definition;
- lineage or source context;
- inclusion conditions;
- exclusion conditions;
- nearest competing terms;
- current role in argument.

A coined concept MUST include a necessity test: what explanatory work cannot be done adequately by an existing term?

## 5. SourceRecord

Represents a source without assuming that it has been read or verified.

Required fields:

- bibliographic description;
- source type;
- access state;
- verification state;
- relevance note;
- claims it is being used to support.

Optional fields:

- direct quotations;
- page or location references;
- methodological limitations;
- disagreement with other sources.

## 6. Claim

A contestable proposition advanced by the researcher.

Required fields:

- claim text;
- claim type: descriptive, interpretive, explanatory, evaluative, methodological, or normative;
- scope;
- support status;
- dependency list;
- counterconditions.

Claims MUST NOT be confused with topics, quotations, or rhetorical transitions.

## 7. EvidenceItem

A piece of material used to support, qualify, or challenge a claim.

Required fields:

- evidence description;
- source record reference;
- location where applicable;
- evidentiary role;
- verification state;
- limitations.

## 8. Interpretation

A reasoned account of what a text, artifact, practice, or event means within an analytical frame.

Required fields:

- object interpreted;
- observed features;
- interpretive move;
- conceptual frame;
- alternative reading;
- evidentiary limits.

An interpretation is not upgraded to fact merely because it is persuasive.

## 9. Inference

A conclusion drawn from identified premises.

Required fields:

- premises;
- inference rule or reasoning explanation;
- conclusion;
- defeaters;
- confidence note.

## 10. ArgumentNode

A unit in an argument map.

Types:

- thesis;
- supporting claim;
- reason;
- evidence need;
- warrant;
- objection;
- reply;
- limitation;
- implication.

Every node SHOULD declare dependencies and whether it is blocking.

## 11. Objection

A challenge that could weaken or defeat a claim.

Required fields:

- target claim;
- strongest formulation;
- objection type;
- evidence needed to assess it;
- current response status;
- consequence if sustained.

## 12. TerminologyEntry

Required fields:

- preferred term;
- definition;
- permitted variants;
- prohibited or deprecated variants;
- distinction from neighboring terms;
- first-definition location;
- known drift risks.

## 13. CitationRecord

Required fields:

- source record reference;
- claim supported;
- citation function;
- bibliographic verification;
- locator verification;
- quotation verification if relevant;
- status and unresolved issue.

Bibliographic existence and claim support are separate checks.

## 14. ReviewerComment

Required fields:

- comment text;
- source or reviewer identifier;
- issue category;
- severity;
- affected manuscript location;
- interpretation of requested change;
- ambiguity note.

## 15. RevisionAction

Required fields:

- reviewer comment or self-review source;
- action type;
- manuscript location;
- before/after summary;
- rationale;
- verification required;
- status.

## 16. GateReport

Required fields:

- gate name;
- status;
- evidence checked;
- blocking issues;
- non-blocking risks;
- researcher decisions required;
- required next action;
- next skill.

## 17. Provenance rule

Transformations MUST preserve provenance. When an agent reformulates a researcher-supplied claim, the result MUST remain traceable to the original note and marked as a transformation rather than an independently sourced claim.
