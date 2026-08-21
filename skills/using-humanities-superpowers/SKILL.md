---
name: using-humanities-superpowers
description: Use when an agent must diagnose research state, select and sequence Humanities Superpowers skills, handle failed gates, and preserve a resumable humanities research workflow.
version: 2.0.0
language: en
license: MIT
---

# Using Humanities Superpowers

## Purpose

Act as the orchestration layer for Humanities Superpowers. Diagnose the current research state, select the smallest sufficient skill sequence, enforce dependencies, interpret gate results, and preserve a resumable record of unresolved work.

This skill is not a generic planner and not an autonomous paper-writing agent. It coordinates scholarly operations while keeping the researcher's decisions, source limits, and responsibility visible.

## When to use

Use this skill:

- at the beginning of a humanities research, manuscript, review, or submission task;
- when several substantive skills may apply;
- when the user asks for an end-to-end workflow;
- when the current research stage is unclear;
- after a gate returns `CONDITIONAL PASS` or `FAIL`;
- when work must resume from an earlier session;
- when a user asks whether a manuscript is ready, complete, publishable, or submission-ready;
- when the agent must decide whether to proceed, pause, roll back, or request a researcher decision.

Do not use this skill for a simple transformation that requires no scholarly diagnosis, such as converting a confirmed bibliography from one citation style to another, unless the request also asks for verification.

## Contract

**Accepts**

- a research request, manuscript task, reviewer task, or submission task;
- optional research materials, source records, previous gate reports, or a prior session record;
- optional explicit constraints such as discipline, corpus, venue, language, deadline, and desired output.

**Requires**

- a requested outcome or a sufficiently clear immediate task;
- enough information to classify the current state, or permission to mark the state as `UNKNOWN` and request the smallest missing input;
- preservation of provenance and verification states from supplied materials.

**Produces**

- a `ResearchState` diagnosis;
- a minimal ordered skill route;
- a prerequisite and input check;
- a routing decision: `PROCEED`, `PAUSE`, `ROLLBACK`, `RESEARCHER_DECISION_REQUIRED`, or `STOP`;
- a session record suitable for resuming work;
- a gate-aware handoff to the next valid skill;
- open friction, evidence conflict, judgment, gate-validity, and possible epistemic-return summaries.

**May produce**

- alternate routes when more than one method is defensible;
- a rollback plan;
- a list of deferred tasks;
- a request for disciplinary or ethical specialist review;
- a final workflow summary after an explicitly requested end-to-end run.

**Fails when**

- the user asks the system to fabricate sources, evidence, quotations, page numbers, archival facts, reviewer actions, or scholarly identity;
- the requested route would require inaccessible evidence and no bounded alternative is possible;
- a necessary researcher decision is replaced with an invented decision;
- a failed upstream gate is ignored to create the appearance of progress;
- submission readiness is requested without the materials required for a final gate.

**Guarantees**

- every selected skill is tied to an identified research need;
- known prerequisites and blocking failures are made visible;
- a failed gate does not silently advance the state;
- the route records where researcher judgment is required;
- the session record preserves current state, unresolved issues, and the next valid action.

**Does not guarantee**

- truth, originality, publication, disciplinary acceptance, or citation accuracy;
- that the selected route is the only defensible scholarly method;
- recovery from missing primary evidence;
- replacement of expert judgment, ethical review, or author responsibility.

## Inputs required

Collect or infer the following without inventing missing values:

1. **Requested outcome** — for example, formulate a question, interpret a passage, revise after review, audit citations, or verify a submission package.
2. **Available artifacts** — notes, corpus, primary text, images, bibliography, draft, reviewer reports, venue guidelines, previous gate reports, or session file.
3. **Current state** — one of the states defined below, or `UNKNOWN`.
4. **Constraints** — discipline, language, corpus, venue, deadline, word limit, ethical limits, privacy requirements, and access constraints.
5. **Researcher-controlled decisions** — theoretical commitment, acceptable scope, interpretation choice, response to reviewers, and final submission authorization.

When one of these is missing, request only the smallest input needed for the next valid step. Do not interrogate the user for information that is not yet necessary.

## Research state model

Use the following primary states:

- `IDEA` — a topic, intuition, problem, or phenomenon exists, but no defensible research question has been formulated.
- `QUESTION` — a research question exists, but scope or feasibility remains unresolved.
- `SCOPE` — boundaries and permissible claim scale are explicit.
- `SOURCES` — relevant materials are identified and their availability and verification states are recorded.
- `INTERPRETATION` — close readings or source analyses produce bounded interpretive claims.
- `ARGUMENT` — claims, evidence, warrants, qualifications, and objections form an explicit argument map.
- `STRUCTURE` — researcher-supplied material has been organized into a manuscript structure.
- `REVIEW` — the manuscript is being stress-tested or reviewed as a whole.
- `REVISION` — identified problems or peer-review comments are being converted into verified manuscript changes.
- `SUBMISSION` — the manuscript and submission package are undergoing final verification.
- `BLOCKED` — a required source, decision, permission, ethical clearance, or prerequisite is unavailable.
- `UNKNOWN` — the current state cannot yet be classified from supplied evidence.

A state label describes the present workflow condition. It does not certify quality. A manuscript can be in `SUBMISSION` state and still receive `FAIL`.

### Epistemic return is a transition record, not a quality state

Humanities inquiry often moves repeatedly between question, source, interpretation, and argument. Do not force this movement into a false one-way pipeline. Create an `EpistemicReturnRecord` whenever new knowledge materially changes an earlier object, while retaining the primary state that best describes the present artifact. Typical returns include:

```text
SOURCES → QUESTION
INTERPRETATION → QUESTION or SCOPE
ARGUMENT → INTERPRETATION
REVIEW → ARGUMENT, SCOPE, or SOURCES
```

Every epistemic return MUST record its trigger, target object and skill, invalidated and preserved gates, reopened artifacts, and required authorization. It is not a new routing decision: use `RESEARCHER_DECISION_REQUIRED` while approval is absent and `PROCEED` to an approved target. Iteration is not permission to bypass gates or erase provenance.

## Procedure

### 1. Intake

Restate the requested outcome in one sentence. Record supplied artifacts and constraints. Preserve distinctions among verified, researcher-supplied, inferred, unverified, unknown, and disputed information.

### 2. Classify the task

Classify the request as one or more of:

- question formation;
- scope design;
- concept lineage;
- literature dialogue;
- argument planning;
- close reading;
- argument structuring;
- argument stress testing;
- citation audit;
- terminology audit;
- manuscript review;
- peer-review response;
- submission verification;
- workflow orchestration only.

Do not infer that “write my paper” authorizes all tasks. Diagnose what scholarly objects and evidence already exist.

### 3. Diagnose current state

Use observable artifacts, not tone or user confidence.

Examples:

- A broad topic without a question is `IDEA`.
- A polished introduction with no explicit claim-evidence structure may still be `QUESTION`, `SCOPE`, or `STRUCTURE`, not `ARGUMENT`.
- Reviewer comments plus an unchanged draft indicate `REVISION`, with actions likely still `planned` rather than `verified`.
- A formatted manuscript with unresolved citations is `SUBMISSION` with a likely blocking gate.

If classification remains uncertain, use `UNKNOWN` and ask for the smallest discriminating artifact.

### 4. Check prerequisites

Before selecting skills, test whether each candidate skill's `Requires` conditions are satisfied.

Typical dependency rules:

- Scope requires a provisional question.
- Concept lineage requires named concepts and traceable sources or a clearly marked search task.
- Literature dialogue requires source records, not invented summaries.
- Close reading requires the actual object or a verifiable extract.
- Argument planning requires a question, scope, and some evidentiary path.
- Argument structuring requires researcher-supplied material or an approved argument map.
- Citation audit requires citation records and access sufficient to verify them.
- Peer-review response requires the actual comments and, for verified completion, the manuscript revision.
- Submission verification requires the final manuscript, required package components, and venue rules where applicable.

### 5. Select the smallest sufficient route

Choose only the skills necessary to reach the requested outcome from the diagnosed state.

Default dependency chain:

```text
IDEA
→ formulating-research-question
→ scoping-argument-boundary
→ mapping-concept-lineage and/or conducting-literature-dialogue
→ performing-close-reading as required by the materials
→ planning-humanities-argument
→ structuring-humanities-argument
→ stress-testing-argument
→ auditing-citations and checking-terminology-consistency
→ reviewing-manuscript
→ responding-to-peer-review when comments exist
→ verifying-before-submission
```

This is a dependency map, not a mandatory linear sequence. Skip a skill only when its required scholarly object already exists at sufficient quality and that status is evidenced.

### 6. Decide execution depth

- For a single, bounded request, route to one skill and stop after its gate report.
- For a multi-stage request, provide the full route but execute only the first valid step unless the user explicitly requests an end-to-end run.
- For an end-to-end run, stop at every blocking gate. Do not simulate later stages with invented inputs.
- For a resumed session, begin from the recorded next valid action, then confirm that referenced artifacts still exist and have not changed incompatibly.

### 7. Interpret gate results

Every substantive skill may return `PASS`, `CONDITIONAL PASS`, or `FAIL`.

#### PASS

Advance only when:

- the required output exists;
- no blocking issue remains for the next skill;
- provenance and researcher decisions are recorded.

#### CONDITIONAL PASS

Advance only if the next skill can operate without converting the condition into an unsupported claim. Carry the condition forward explicitly.

Examples:

- A provisional research question may advance to scope design while novelty remains unverified.
- A terminology ledger with one unresolved translation may allow argument planning but must block final submission.

#### FAIL

Do not advance to a dependent state. Choose one of:

- `ROLLBACK` to the earliest skill that can repair the failure;
- `PAUSE` while obtaining a missing source or decision;
- `RESEARCHER_DECISION_REQUIRED` when alternatives depend on authorial judgment;
- `STOP` for fabrication, ethical, legal, privacy, or irrecoverable access problems.

### 8. Rollback rules

Rollback must target the earliest causal defect, not the most recent document.

Examples:

- If an argument fails because the claim exceeds the corpus, roll back to `scoping-argument-boundary`, not merely `structuring-humanities-argument`.
- If a citation audit shows that a central source does not support the claim, roll back to `planning-humanities-argument` or `conducting-literature-dialogue`.
- If a reviewer exposes an undefined core concept, roll back to `mapping-concept-lineage` and `checking-terminology-consistency` before rewriting prose.
- If the submission gate finds hidden author metadata in a blinded file, remain in `SUBMISSION`; repair the package without reopening the argument.

Record the causal link between failed gate and rollback target.

### 8a. Distinguish rollback from epistemic return

Use `ROLLBACK` for defect repair: invalid citation, missing prerequisite, failed claim–source fit, or scope violation. When new evidence, a rival interpretation, or a revised concept materially changes an earlier premise, create an `EpistemicReturnRecord`. Name the target object and skill, preserve prior versions, and invalidate only gates that reference the changed dependency. New evidence that does not materially change an object is a ledger update or recheck, not an automatic return.

### 8b. Inspect friction and gate validity

Before routing, list open friction events, evidence conflicts, and gates whose validity is `INVALIDATED` or `REQUIRES_RECHECK`. A historical `PASS` with invalid validity cannot authorize progression. Do not harmonize conflict merely to restore a smooth route.

Apply the minimum-sufficient-record rule: create Fricturn objects only for material scholarly consequences, attributable decisions, or dependency validity. Do not create friction, judgment, or return records for spelling, formatting, stylistic preference, routine source addition, or harmless restatement alone. Prefer one narrowly targeted record over duplicated records across the route.

### 9. Researcher decision points

Return `RESEARCHER_DECISION_REQUIRED` when the system cannot legitimately choose among defensible alternatives, including:

- which interpretation the author will defend;
- whether to narrow the corpus or weaken the thesis;
- whether to concede or rebut a reviewer;
- which translation or technical term the author adopts;
- whether an ethical risk is acceptable under institutional rules;
- whether to submit despite disclosed non-blocking limitations.

Present the alternatives, consequences, and evidence. Do not select in the researcher's name.

### 10. Update the session record

After each routing decision or substantive gate, update a `research-session.md` or equivalent structured record containing:

- session identifier and timestamp;
- requested outcome;
- current state;
- completed skills and gate results;
- active artifacts and provenance;
- blocking issues;
- non-blocking risks;
- researcher decisions required;
- deferred tasks;
- next valid action;
- rollback history;
- completion claim restrictions;
- open and resolved friction references;
- judgment-log, evidence-ledger, and interpretation-history references;
- epistemic-return history, invalidated gates, and reopened objects.

The session record is workflow memory, not factual evidence. It must link to or name the underlying artifacts instead of replacing them.

### 11. Completion control

Do not use “complete,” “fully verified,” “citation-safe,” “submission-ready,” or equivalent language unless the relevant final gate has passed and the evidence checked is named.

A workflow may end successfully with `FAIL` when the correct outcome is to prevent an unsupported claim or unsafe submission.

## Routing matrix

| Observed need | Primary skill | Common prerequisite | Typical next skill |
|---|---|---|---|
| Broad topic, no arguable question | `formulating-research-question` | research interest or phenomenon | `scoping-argument-boundary` |
| Claim is too broad or corpus unclear | `scoping-argument-boundary` | provisional question | lineage, literature, or argument planning |
| Concept originality or inheritance is unclear | `mapping-concept-lineage` | named concept and sources/search boundary | literature dialogue or terminology audit |
| Sources are summarized as a list | `conducting-literature-dialogue` | source records | argument planning |
| Claims and evidence are not connected | `planning-humanities-argument` | question, scope, evidence path | close reading or structuring |
| Interpretation is asserted without textual/formal basis | `performing-close-reading` | primary object | argument planning |
| Notes and paragraphs exist but logic is hard to follow | `structuring-humanities-argument` | researcher material and argument map | stress testing |
| Thesis seems persuasive but unchallenged | `stress-testing-argument` | explicit argument | scope repair, argument repair, or review |
| References may be invented, incomplete, or mismatched | `auditing-citations` | citation records and access | manuscript review or submission gate |
| Core terms drift or translations conflict | `checking-terminology-consistency` | manuscript or terminology records | manuscript review |
| Whole manuscript needs prioritized diagnosis | `reviewing-manuscript` | manuscript and research purpose | revision or peer-review response |
| Reviewer comments need verified responses | `responding-to-peer-review` | comments and manuscript | manuscript review or final gate |
| Readiness or completion is claimed | `verifying-before-submission` | final package and requirements | submit, repair, or stop |

## Stop signals

Stop or pause immediately when:

- a required primary object, draft, reviewer report, venue guideline, or source is absent;
- the user asks for fabricated citations, quotations, page numbers, evidence, archival facts, or reviewer actions;
- a user asks the system to conceal AI authorship, impersonate a scholar, or manufacture a research history;
- a high-stakes legal, ethical, privacy, copyright, or human-subject issue requires qualified review;
- an upstream `FAIL` is being bypassed solely because of a deadline;
- the only available route would convert an inference into fact or an unknown into verified information;
- the requested output would violate a blind-review or privacy requirement.

When a stop signal occurs, return the reason, the blocked state, the missing or prohibited item, and the safest next action.

## Completion criteria

This orchestration skill is complete when:

- the requested outcome and current state are explicit;
- the smallest sufficient route is selected;
- every selected skill has satisfied prerequisites or is marked blocked;
- gate outcomes determine advance, conditional advance, rollback, pause, researcher decision, or stop;
- unresolved issues and completion restrictions remain visible;
- the session record identifies the next valid action;
- no later-stage artifact has been simulated from missing earlier-stage evidence.

Level 3 conformance additionally requires successful positive, negative, ambiguous, missing-input, adversarial, rollback, researcher-decision, resume, no-op, and end-to-end routing tests.

## Anti-fabrication rules

- Do not invent quotations, page numbers, publication facts, DOIs, archival identifiers, source contents, reviewer comments, revisions, or submission requirements.
- Do not treat researcher-supplied information as independently verified.
- Do not infer quality from fluent prose, formatting, confidence, file naming, or advanced workflow state.
- Do not manufacture a `PASS` to preserve momentum.
- Do not remove uncertainty labels during handoff.
- Do not convert `planned` revision actions into `completed` or `verified` actions without manuscript evidence.
- Do not use a session record as a substitute for the underlying source or manuscript.
- Preserve disagreement among sources and defensible alternative routes.

## Output format

Use this format before execution:

```md
## Workflow diagnosis

**Requested outcome:**
**Current state:**
**Available artifacts:**
**Missing prerequisites:**
**Constraints:**

## Routing decision

**Decision:** PROCEED | PAUSE | ROLLBACK | RESEARCHER_DECISION_REQUIRED | STOP
**Selected skills:**
**Sequence:**
**Reason for minimal route:**
**Conditions carried forward:**
**Completion claim restrictions:**

## Fricturn state

**Open frictions:**
**Evidence conflicts:**
**Researcher decisions required:**
**Gate validity:** VALID | INVALIDATED | REQUIRES_RECHECK
**Possible epistemic returns:**

## Next valid action

**Skill:**
**Required input:**
**Expected output:**
**Gate that controls handoff:**
```

After execution, append:

```md
## Orchestration gate report

**Gate:**
**Status:** PASS | CONDITIONAL PASS | FAIL
**Evidence checked:**
**Blocking issues:**
**Non-blocking risks:**
**Researcher decisions required:**
**Required next action:**
**Next skill or rollback target:**
**Session record updated:** yes | no
```

When a persistent file is appropriate, use `templates/research-session.md` and validate it against `schemas/research-session.schema.json` where tooling permits.

## Good invocation

> I have a provisional question, six verified sources, and notes from close readings. Diagnose my current research state and route me to the smallest workflow needed to build and stress-test the argument.

A valid response should classify the artifacts, avoid repeating completed stages, select argument planning followed by stress testing or structure as warranted, and carry any unresolved source conditions forward.

## Bad invocation

> Load every skill, invent whatever evidence is missing, write a publishable article, and mark it submission-ready today.

This request must not advance. It requires fabrication, ignores dependencies, and demands an unsupported completion claim.

## Next skills

The router may hand off to any substantive skill, but common first steps are:

- `formulating-research-question`
- `scoping-argument-boundary`
- `conducting-literature-dialogue`
- `planning-humanities-argument`
- `reviewing-manuscript`
- `responding-to-peer-review`
- `verifying-before-submission`

A failed gate may route backward to an earlier skill rather than forward to the next listed skill.

## Gate report

The orchestration gate evaluates routing integrity, not manuscript quality.

- `PASS` — state, prerequisites, route, and next action are explicit; no blocking dependency is bypassed.
- `CONDITIONAL PASS` — routing can proceed with named conditions that do not invalidate the next operation.
- `FAIL` — the route depends on fabrication, missing blocking evidence, an unresolved researcher decision, or a bypassed failed gate.

## Friction triggers

Trigger friction when a route would smooth over evidence conflict, rival interpretation, agent or researcher disagreement, unsupported promotion, or completion risk. Stylistic preference alone is not scholarly friction.

## Friction checks

For each event confirm a target object, trigger, material description, blocking status, categorical severity, required action, and resolution status. Preserve unresolved conflict in the session.

## Judgment boundary

Keep agent recommendations separate from `researcher_decision`. Only attributable human authorization may accept a scholarly choice or risk. Route defensible alternatives to `RESEARCHER_DECISION_REQUIRED`.

## Evidence ledger updates

Carry ledger references and distinguish `verification_state` from `evidential_standing`. A verified source may be `INSUFFICIENT` or `CONTRADICTS`; source counts do not decide a gate.

## Interpretation history impact

Append interpretation versions and preserve superseded readings. Agent-generated readings remain `PROPOSED` until researcher action.

## Possible epistemic return

Propose a bounded return when new knowledge materially changes an earlier object. Name invalidated and preserved gates, reopened artifacts, target skill, and authorization requirement. Do not mislabel defect repair as epistemic return.

## Productive refusal

When routing cannot proceed, state the reason, missing evidence, bounded work still possible, and next verification action. Do not manufacture a decision or completion state.

## Gate impact

Gate `status` remains `PASS`, `CONDITIONAL PASS`, or `FAIL`; current `validity` is tracked separately as `VALID`, `INVALIDATED`, or `REQUIRES_RECHECK`. Submission may not proceed on invalidated or unrechecked controlling gates.

## Limitations

The state machine is a coordination model, not a universal theory of humanities research. Real projects may be iterative, nonlinear, archival, practice-based, multilingual, collaborative, or discipline-specific. The router must therefore permit justified alternate routes while preserving explicit dependencies and gate evidence.

Session memory can preserve workflow context but cannot establish facts, verify sources, or replace the researcher's records. Different agent harnesses may implement persistence differently. The durable artifact is the explicit session record, not hidden model memory.
