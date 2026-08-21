---
name: scoping-argument-boundary
description: Use when a research question is promising but its corpus, period, comparison, concepts, or claim size remain too broad or unstable for a defensible humanities argument.
version: 2.0.0
language: en
license: MIT
---

# Scoping an Argument Boundary

## Purpose

Convert a promising research question into a bounded inquiry by defining what the argument includes, excludes, compares, and refuses to claim. The skill prevents scale inflation and protects the manuscript from drifting between incompatible objects or levels of analysis.

## Contract

**Accepts**
- A `ResearchQuestion` record or clearly stated primary question.
- Candidate corpus, archive, period, geography, language, medium, or conceptual field.
- Known venue, deadline, length, and access constraints.

**Requires**
- A stable primary question.
- At least one candidate unit of analysis.
- Enough project context to identify feasible exclusions.

**Produces**
- One `ScopeBoundary` record.
- Inclusion and exclusion criteria.
- A bounded corpus statement.
- A claim ceiling defining the strongest claim the evidence could support.
- A scope gate report.

**May produce**
- Alternative narrow, moderate, and expansive scope options.
- A deferred-research list for valuable material excluded from the present project.

**Fails when**
- The primary question is still circular or indeterminate.
- The researcher refuses necessary exclusions.
- The proposed evidence cannot support the desired level of generalization.
- The project combines multiple independent studies without a governing relation.

**Guarantees**
- The output will make exclusions and claim limits explicit.
- Corpus boundaries and units of analysis will be recorded in a form usable by downstream skills.
- Excluded materials will not be treated as silently analyzed.

**Does not guarantee**
- That the selected scope is the most original or publishable one.
- That all included materials can be obtained or interpreted successfully.

## When to use

Use after a primary research question has been selected and before extensive literature accumulation or prose drafting. Use when a project contains too many theorists, periods, media, national contexts, or corpora; when the abstract promises more than the evidence can sustain; or when the unit of analysis shifts from text to discourse to society without explanation.

Do not use this skill to hide counterevidence by arbitrary exclusion. Exclusions must be methodologically defensible and disclosed.

## Inputs required

Collect:

1. Primary question and provisional hypothesis.
2. Candidate corpus or archive.
3. Temporal and geographic range.
4. Languages and media included.
5. Proposed comparison cases.
6. Practical constraints: access, length, deadline, expertise.
7. Desired claim level: local interpretation, bounded comparison, genealogy, or broader theoretical intervention.

## Procedure

### 1. Identify the current scale

List every object, period, concept, method, and comparison implied by the question. Mark where the project changes analytical level, such as moving from one novel to national culture or from one interface to “digital society.”

### 2. Define the primary unit of analysis

Choose the smallest unit capable of answering the question. Secondary units may be included only when their relation to the primary unit is explicit.

### 3. Build inclusion criteria

State positive rules for what belongs in the corpus. Good criteria are observable and repeatable: publication dates, genre, platform function, archival collection, language, institutional setting, or relevance to a defined motif.

### 4. Build exclusion criteria

State what is outside the project and why. Distinguish:

- **methodological exclusion:** not needed to answer the question;
- **practical exclusion:** unavailable, untranslated, or outside current competence;
- **deferred inclusion:** valuable for later research but too large for the current project.

### 5. Set the claim ceiling

Use the grammar:

```text
PermissibleClaim <= EvidenceCoverage + MethodCapacity + ScopeBoundary
```

A bounded corpus may support a strong interpretation of that corpus, but not a universal claim about all readers, all platforms, or an entire historical period.

### 6. Test comparison symmetry

For comparative work, verify that cases are compared at the same analytical level and through common criteria. If one case is represented by a single text and another by an entire national tradition, return `FAIL` or redesign the comparison.

### 7. Create three scope options when useful

- **Narrow:** strongest evidentiary control, smallest intervention.
- **Moderate:** balanced contribution and feasibility.
- **Expansive:** larger stakes, higher evidence burden and risk.

Recommend one option, but leave the final scholarly choice visible.

### 8. Register deferred material

Move excluded but relevant sources, concepts, or cases to a deferred-research list. Do not let them re-enter later prose without reopening the scope decision.

### 9. Issue the gate report

Return `PASS` when corpus, period, unit, exclusions, and claim ceiling are explicit. Return `CONDITIONAL PASS` when one non-blocking access or comparison issue remains. Return `FAIL` when the desired claim fundamentally exceeds the available evidence.

## Stop signals

Stop when:

- the researcher asks one article to cover several centuries, languages, or disciplines without a method of selection;
- the conclusion generalizes from one example to a population or era;
- exclusions appear designed to remove inconvenient evidence;
- the comparison lacks common criteria;
- the project’s central concept changes meaning across sections;
- the venue’s length makes the proposed evidence impossible to present responsibly.

## Completion criteria

- The primary and secondary units of analysis are explicit.
- Corpus inclusion and exclusion criteria are documented.
- Temporal, geographic, linguistic, and media boundaries are stated where relevant.
- The claim ceiling is written in one or two sentences.
- Comparison cases use common criteria.
- Deferred materials are recorded separately.
- The gate report identifies any unresolved access or representativeness risk.

## Anti-fabrication rules

- Do not claim representativeness without a stated sampling rationale.
- Do not describe excluded material as if it had been reviewed.
- Do not invent corpus completeness, archive access, translations, or dataset coverage.
- Do not turn practical convenience into a theoretical justification without disclosure.
- Do not erase counterexamples merely to preserve the hypothesis.

## Output format

```md
## Scope decision
Primary question:
Recommended scope: narrow | moderate | expansive

## Unit of analysis
Primary unit:
Secondary units:

## Corpus boundary
Included:
Excluded:
Deferred:

## Temporal, geographic, linguistic, and media limits

## Comparison design
Cases:
Common criteria:
Asymmetry risks:

## Claim ceiling
The strongest defensible claim is:
Claims this project will not make:

## Access and feasibility risks

## Gate report
Gate: Scope gate
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill: mapping-concept-lineage | conducting-literature-dialogue
```

## Good invocation

> Scope my article on platform mediation to 8,000 words. I have twelve museum interfaces from the Netherlands and South Korea, captured between 2023 and 2025. I need to know whether a cross-national comparison is defensible or whether I should narrow to one institutional function.

## Bad invocation

> Help me prove that all digital platforms have transformed human perception from the nineteenth century to today. I only have two screenshots, but make the scope sound ambitious.

The evidence cannot support the requested temporal and universal claim. The skill must return `FAIL` or propose a substantially narrower project.

## Next skills

- `mapping-concept-lineage` when the bounded project depends on contested or inherited concepts.
- `conducting-literature-dialogue` to map the scholarly conversation within the selected boundary.
- `planning-humanities-argument` only after the conceptual and literature foundations are adequate.

## Friction triggers

Create overreach friction when claim scale exceeds corpus, method, period, geography, language, or comparison symmetry.

## Friction checks

Test generalization against actual coverage and distinguish defensible exclusion from removal of counterevidence. Record a friction event when prose or ambition masks the mismatch.

## Judgment boundary

When both claim narrowing and corpus expansion are defensible, present costs and record the researcher's choice; do not select the author's ambition level.

## Evidence ledger updates

Link each major claim to covered, qualifying, contradicting, and missing evidence. A verified source outside the boundary may be `CONTEXT_ONLY`, not support.

## Interpretation history impact

Record when a scope decision limits the scale of an existing interpretation; do not rewrite its earlier version as though it had always been narrow.

## Possible epistemic return

Return to the research question when revised boundaries change the inquiry itself. New corpus evidence may reopen a prior scope record; ordinary overreach repair remains `ROLLBACK`.

## Productive refusal

When representativeness cannot be established, state actual coverage, unexamined range, the strongest bounded claim, and the sampling or corpus work required.

## Gate impact

Material scope change may invalidate source-coverage, argument, review, and submission validity. Bound invalidation to gates that reference the changed scope.

## Limitations

Scope decisions are interpretive and strategic, not mechanically optimal. A narrow project can still be shallow, and an expansive project can be justified when evidence, expertise, and format permit it. The researcher remains responsible for the final boundary.
