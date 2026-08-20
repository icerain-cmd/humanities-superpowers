---
name: formulating-research-question
description: Use when a humanities researcher has a broad topic, intuition, corpus, or problem but does not yet have a precise, contestable, and researchable question.
version: 2.0.0
language: en
license: MIT
---

# Formulating a Research Question

## Purpose

Transform a broad topic or dissatisfaction into a contestable research question with an explicit object, unresolved tension, stakes, and feasible evidentiary path. This skill supports scholarly judgment; it does not manufacture novelty or decide what the researcher ought to value.

## Contract

**Accepts**
- A topic, corpus, archive, concept, event, medium, practice, or preliminary observation.
- Notes describing what seems puzzling, inadequate, contradictory, or underexplained.
- Optional disciplinary, temporal, linguistic, geographic, or institutional constraints.

**Requires**
- At least one identifiable research object or candidate corpus.
- At least one unresolved tension stated without assuming its answer.
- Enough information to distinguish the topic from the research problem.

**Produces**
- One `ResearchQuestion` record for the selected primary question.
- Up to two subordinate questions.
- A short research-problem statement.
- A list of evidence classes required to answer the question.
- A provisional hypothesis explicitly marked `hypothesis`.

**May produce**
- Two or three alternative question formulations with trade-offs.
- A `FAIL` or `CONDITIONAL PASS` gate report when the object, tension, or evidence path remains unclear.

**Fails when**
- The requested question presupposes the conclusion.
- The object or corpus cannot be identified.
- The question requires inaccessible evidence and no narrower formulation is possible.
- The request asks the agent to declare novelty without a literature check.

**Guarantees**
- The selected question will explicitly name its object, unresolved relation, and expected evidence path.
- Unresolved elements will remain visible rather than being silently invented.
- The output will distinguish question, hypothesis, and conclusion.

**Does not guarantee**
- Originality, disciplinary significance, publication value, or a successful final answer.
- That the listed evidence actually exists or will support the hypothesis.

## When to use

Use this skill at the beginning of a paper, chapter, thesis, grant concept, or major revision. Use it when the researcher has many notes but no governing problem, when the current “question” is a topic label, or when the manuscript appears to know its conclusion before inquiry begins.

Do not use it merely to generate fashionable titles, inflate significance, or reverse-engineer a question around a predetermined claim. Route those cases to clarification or return `FAIL`.

## Inputs required

Collect the following before drafting a question:

1. **Research object:** what text, archive, discourse, practice, event, platform, institution, or concept is being examined?
2. **Observed feature:** what is actually noticed in or about the object?
3. **Unresolved tension:** what contradiction, absence, instability, or interpretive difficulty remains?
4. **Stakes:** why would resolving this tension matter to a scholarly conversation?
5. **Evidence access:** what materials can realistically be consulted?
6. **Constraints:** discipline, language, chronology, word limit, deadline, or venue.

If one of the first three inputs is missing, do not guess it. Ask for it or produce an unresolved-items report.

## Procedure

### 1. Separate topic from problem

Rewrite the user’s topic as a neutral noun phrase. Then state the unresolved problem as a full sentence. A topic such as “platform aesthetics” is not yet a problem. A problem appears only when an observed feature and an unresolved tension are connected.

Use the grammar:

```text
ResearchProblem = Observation + Unresolved Tension + Stakes
```

### 2. Identify the unit of analysis

Specify whether the inquiry concerns a text, motif, interface, archive, historical episode, concept, discourse, reception pattern, institutional practice, or relation among these. Avoid shifting units mid-question.

### 3. Generate question families

Draft at least three candidates when enough input exists:

- **Interpretive:** How should a difficult feature or relation be understood?
- **Explanatory-genealogical:** How did a concept, form, or discourse acquire its present configuration?
- **Critical-comparative:** What becomes visible when two positions, corpora, or media forms are placed in a bounded comparison?

Do not force all three if the object clearly supports only one.

### 4. Test answerability

For each candidate, ask:

- Can the question be answered with identifiable materials?
- Is the answer non-obvious and contestable?
- Could evidence require revision of the initial hypothesis?
- Is the scale appropriate for the venue and deadline?
- Does the wording avoid evaluative slogans such as “bad,” “revolutionary,” or “destroyed” unless these are objects of analysis?

### 5. Detect conclusion smuggling

Mark and revise formulations that contain their preferred answer. For example, “How does platform capitalism destroy authentic experience?” already treats destruction and authenticity as settled. Reframe the relation as an open problem.

### 6. Select and register

Select one primary question. Record:

- object
- unresolved relation
- scope cues
- evidence classes
- stakes
- verification state

Assign `verification_state: researcher-supplied` unless relevant claims have been independently checked.

### 7. Draft a provisional hypothesis

Only after the question is stable, state a provisional answer. Label it `hypothesis`. Add at least one condition under which the hypothesis would need revision.

### 8. Revisit the question after exploratory source work

Treat question formation as iterative rather than final. After an initial source, corpus, archive, or concept exploration, compare the provisional question with what the materials actually make visible. Record whether the object, tension, scale, vocabulary, or evidence path has changed. When exploratory materials expose a different problem, route back to this skill instead of forcing the original question to survive.

A revised question MUST preserve a change note:

```text
Original question
→ exploratory finding
→ reason for revision
→ revised question
```

Do not describe this return as failure. In humanities inquiry, revision after reading is often evidence that the question has become more precise.

### 9. Issue the gate report

Return `PASS` only when object, tension, stakes, and evidence path are explicit. Return `CONDITIONAL PASS` when the question is usable but one non-blocking scope or terminology decision remains. Return `FAIL` when the question is circular, inaccessible, or too indeterminate to hand off.

## Stop signals

Stop and preserve uncertainty when:

- the user asks for a “groundbreaking” question without a corpus or literature context;
- the question embeds an unverified historical claim;
- the key concept has no stable working definition;
- the intended evidence is unavailable, private, untranslated, or outside the project’s capacity;
- the requested scale would require multiple independent studies;
- the researcher rejects every formulation that does not already prove the preferred conclusion.

When a stop signal occurs, produce `Unresolved items` and `Researcher decision required`. Do not repair the gap by inventing a source, consensus, or historical premise.

## Completion criteria

The skill is complete only when:

- the primary question contains an identifiable object and analytical relation;
- the unresolved tension is not merely a topic label;
- the answer could plausibly be contested;
- the evidence classes are named;
- the scale is feasible under stated constraints;
- the provisional hypothesis is marked as revisable;
- the gate report records blocking and non-blocking issues;
- the next skill can accept the produced object without reconstructing missing context.

## Anti-fabrication rules

- Do not declare a question original without a completed literature dialogue.
- Do not invent gaps in scholarship.
- Do not convert the researcher’s intuition into a verified disciplinary fact.
- Do not invent quotations, publication facts, page numbers, DOI values, archival identifiers, or source contents.
- Do not imply that a source exists merely because a plausible title can be generated.
- Preserve disagreement and uncertainty.
- Use `unknown` when the relevant fact has not been checked.

## Output format

```md
## Research problem
Observation:
Unresolved tension:
Stakes:

## Candidate questions
### Candidate A
Question:
Type:
Strength:
Risk:
Evidence required:

## Selected primary question
Question:
Object:
Analytical relation:
Verification state:

## Sub-questions
1.
2.

## Provisional hypothesis
Status: hypothesis
Statement:
Revision condition:

## Unresolved items

## Gate report
Gate: Research-question gate
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill: scoping-argument-boundary
```

## Good invocation

> Use this skill to turn my topic “platform aesthetics” and my notes on artificial nature into three candidate research questions. My corpus is a set of museum platform interfaces from 2023–2025. Explain the trade-offs and select one question only if the evidence path is feasible.

This invocation supplies an object, a provisional tension, a bounded corpus, and a request for transparent selection.

## Bad invocation

> Give me a groundbreaking research question that proves platforms have destroyed nature. Make it sound publishable and say nobody has studied it.

This request presupposes a conclusion, asks for unsupported novelty, and provides no bounded object. The correct outcome is clarification or `FAIL`, not an impressive-sounding question.

## Next skills

- `scoping-argument-boundary` to delimit corpus, period, comparison, and excluded claims.
- `mapping-concept-lineage` when key terms require genealogy and differentiation.
- `conducting-literature-dialogue` before any originality claim is accepted.

## Friction triggers

Create premise friction when a preferred answer is embedded in the question, an unverified premise controls the inquiry, or new material undermines the question's object or tension.

## Friction checks

Compare the premise, evidence path, and revision conditions with exploratory findings. Record `CLAIM_OVERREACH`, `INFERENCE_PROMOTION`, or `EVIDENCE_CONFLICT` only when the issue materially affects answerability.

## Judgment boundary

The agent may present question alternatives and consequences; the researcher selects the governing question and stakes. Preserve recommendations separately from the authorized decision.

## Evidence ledger updates

Register evidence classes and any source tied to a premise. Verification state does not determine whether that source supports the premise.

## Interpretation history impact

When a new reading changes the question, link the accepted or proposed interpretation version rather than replacing the earlier rationale.

## Possible epistemic return

This skill is a primary return target when new sources or interpretations materially alter an earlier question. Preserve Q1, create Q2 with `supersedes`, and identify affected scope, argument, and submission gates.

## Productive refusal

If originality, first use, or a premise cannot be established, report the checked range, missing search, bounded wording currently permitted, and next verification action.

## Gate impact

Premise friction that makes the question circular or unsupported forces `FAIL`. A materially revised question marks dependent gates `INVALIDATED` or `REQUIRES_RECHECK` without changing their historical status.

## Limitations

A well-formed question can still be unimportant, derivative, ethically unsuitable, or impossible to answer with the eventual evidence. Question quality must be reassessed after literature review, close reading, and argument stress testing.
