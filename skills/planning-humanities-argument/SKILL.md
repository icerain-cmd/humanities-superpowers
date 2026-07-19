---
name: planning-humanities-argument
description: Use when a research question, scope boundary, and source base exist but the manuscript still needs a defensible sequence of claims, warrants, evidence, objections, and section functions.
version: 1.0.0
language: en
license: MIT
---

# Planning a Humanities Argument

## Purpose

Convert a research question and bounded source base into an explicit argument architecture. The skill makes inferential dependencies visible before prose hides them. It does not manufacture a thesis, create evidence, or convert thematic organization into argument by tone alone.

## Contract

**Accepts**
- A `ResearchQuestion`, `ScopeBoundary`, provisional thesis, source inventory, and notes.
- Optional venue constraints, word limit, disciplinary expectations, and section drafts.

**Requires**
- A research question that can be answered propositionally.
- A provisional thesis supplied or approved by the researcher.
- At least one identifiable evidence class for every major claim.
- A declared scope boundary.

**Produces**
- One argument map composed of `Claim`, `EvidenceItem`, `Inference`, `ArgumentNode`, and `Objection` records.
- A dependency-ordered section plan.
- An evidence-gap register.
- An argument-planning gate report.

**May produce**
- Alternative architectures when more than one defensible sequence exists.
- `CONDITIONAL PASS` when the structure is usable but evidence or warrants remain incomplete.
- `FAIL` when the thesis cannot be decomposed into supportable claims.

**Fails when**
- The thesis is only a topic, slogan, moral preference, or conclusion copied from the prompt.
- A major claim lacks both evidence and a feasible evidence plan.
- Section order depends on concepts not yet defined or claims not yet established.
- The requested architecture requires invented evidence or literature consensus.

**Guarantees**
- Every major claim is paired with an explicit warrant and evidence status.
- Section order reflects argumentative dependency rather than topic sequence alone.
- Missing inferential work remains visible.

**Does not guarantee**
- That the thesis is true, original, significant, or publishable.
- That planned evidence will ultimately support the claim.
- That a complete map will yield persuasive prose without further scholarly judgment.

## When to use

Use after the research question and scope have stabilized and before substantial drafting. Use during revision when a manuscript contains strong passages but no clear inferential progression, when the conclusion introduces claims not earned earlier, or when sections merely accumulate theorists, themes, or examples.

Do not use this skill to generate an argument from a title alone. Do not treat a table of contents as an argument map. If the researcher has not yet chosen a provisional thesis, route back to `formulating-research-question` or request a researcher decision.

## Inputs required

Collect:

1. Primary research question.
2. Scope boundary and exclusions.
3. Provisional thesis, marked `hypothesis` or `researcher-supplied`.
4. Source and evidence inventory with verification states.
5. Key concepts and working definitions.
6. Venue, length, audience, and deadline.
7. Known objections or rival explanations.

If the thesis or scope is missing, stop. If evidence is incomplete but identifiable, continue with explicit gap markers.

## Procedure

### 1. Normalize the thesis

Rewrite the provisional thesis as one contestable proposition without changing its meaning. Separate descriptive, interpretive, causal, genealogical, and normative components. A single sentence that contains several claim types may need to become a claim cluster.

### 2. Derive enabling claims

Ask what must be established before the thesis can be accepted. Create three to five enabling claims where possible. Each must perform necessary work; a section that can disappear without affecting the conclusion is probably contextual, redundant, or misplaced.

### 3. Build claim records

For each claim record:

```text
Claim
+ Evidence
+ Warrant
+ Qualification
+ Objection
+ Consequence
```

Distinguish direct evidence from contextual support and theoretical framing. Do not allow a theory name to stand in for a warrant.

### 4. Classify inferential movement

Mark transitions as definition, distinction, interpretation, comparison, genealogy, explanation, evaluation, or implication. This prevents silent movement from local observation to historical generalization or from interpretation to causal explanation.

### 5. Create the dependency graph

Order claims by logical dependence. Definitions precede applications; local readings precede broader implications; source-supported historical claims precede genealogical conclusions. Circular dependencies must be exposed rather than disguised through section headings.

### 6. Assign section functions

Give every section one primary argumentative function, such as defining a concept, establishing a historical transformation, interpreting a corpus, testing a rival account, or deriving implications. A section may contain context, but context must serve its function.

### 7. Audit evidence distribution

Check whether one source or example is asked to support incompatible propositions. Mark overused evidence, unsupported claims, and claims supported only by secondary summaries when primary evidence is required.

### 8. Place objections

Attach objections to the claims they threaten. Do not postpone every objection to a final limitations section. Rank each objection as fatal, major, or minor and indicate whether the planned response is rebuttal, concession, narrowing, or redesign.

### 9. Budget space

Allocate words according to inferential burden, not enthusiasm. Claims that introduce new concepts, contest established readings, or depend on difficult evidence receive more space than descriptive background.

### 10. Run removal and reversal tests

For each section, ask what fails if it is removed. Then test whether reversing two adjacent sections creates circularity or premature claims. Record sections whose function remains uncertain.

### 11. Issue the gate report

Return `PASS` only when the thesis, enabling claims, warrants, evidence path, objections, and dependencies are explicit. Return `CONDITIONAL PASS` for non-blocking evidence gaps. Return `FAIL` when the map is decorative rather than inferential.

## Stop signals

Stop when:
- the thesis changes meaning across notes;
- the same evidence is used to prove mutually incompatible claims;
- a claim relies on a concept defined only after its application;
- the evidence path depends on unavailable materials;
- the researcher requests “a persuasive outline” while refusing to state a claim;
- the structure would conceal a fatal objection rather than address it.

Record `Researcher decision required` rather than choosing a substantive thesis on the researcher’s behalf.

## Completion criteria

Complete only when:
- the thesis answers the primary question;
- every major claim has a warrant and evidence status;
- claims are dependency-ordered;
- section functions are non-duplicative;
- major objections are attached to target claims;
- evidence gaps are explicit;
- the final implication does not exceed the scope boundary;
- the gate report identifies the next skill.

## Anti-fabrication rules

- Do not invent evidence to fill a clean-looking map.
- Do not convert a theorist’s name into a warrant.
- Do not mark researcher-supplied claims as verified.
- Do not infer consensus from a small source set.
- Do not label a thesis original before literature dialogue and lineage checks.
- Preserve contradictory evidence and unresolved dependencies.

## Output format

```md
## Thesis
Statement:
Claim types:
Verification state:

## Argument map
### Claim C1
Function:
Depends on:
Evidence:
Warrant:
Qualification:
Strongest objection:
Response:
Status:

## Section architecture
| Section | Primary function | Claims advanced | Evidence used | Dependency | Word budget |

## Evidence gaps

## Unresolved items

## Gate report
Gate: Argument-planning gate
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill: performing-close-reading
```

## Good invocation

> Use my approved research question, scope statement, verified source notes, and provisional thesis to create a dependency-ordered argument map. Mark every missing warrant and do not invent evidence.

## Bad invocation

> Make a persuasive five-part argument proving that AI has changed humanity forever. Use whatever evidence sounds right.

The bad invocation supplies an inflated conclusion, no bounded corpus, and permission to fabricate support.

## Next skills

- `performing-close-reading` to generate accountable object-level evidence.
- `structuring-humanities-argument` to organize researcher-authored material around the map.
- `stress-testing-argument` to challenge the architecture before drafting.

## Limitations

Argument maps clarify dependencies but cannot settle interpretive disputes or determine disciplinary value. Some humanities arguments are deliberately recursive, fragmentary, or essayistic; such forms still require a defensible account of how their sequence produces knowledge.
