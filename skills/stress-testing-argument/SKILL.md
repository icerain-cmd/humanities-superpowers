---
name: stress-testing-argument
description: Use when a thesis, concept, interpretation, or manuscript needs disciplined adversarial testing against counterexamples, rival explanations, category errors, scale violations, false novelty, and unresolved ethical risks.
version: 1.0.0
language: en
license: MIT
---

# Stress-Testing an Argument

## Purpose

Identify the strongest informed objections to an argument, rank their severity, and specify repairs without reducing the thesis to a trivial claim. The skill challenges evidence, warrants, concepts, scope, method, ethics, and novelty while preserving fair representation.

## Contract

**Accepts**
- A thesis, enabling claims, argument map, evidence inventory, and scope boundary.
- Optional rival theories, disciplinary criteria, reviewer comments, or venue expectations.

**Requires**
- A sufficiently explicit argument to reconstruct charitably.
- Access to the evidence and warrants being tested.
- Separation between verified criticism and hypothetical reviewer concerns.

**Produces**
- A steelmanned argument summary.
- Ranked `Objection` records.
- Alternative explanations and counterexamples.
- Recommended responses: rebut, concede, narrow, redesign, or defer.
- A stress-test gate report.

**May produce**
- A revised thesis or scope boundary for researcher approval.
- A fatal-flaw report.
- `FAIL` when the argument cannot survive without abandoning its central contribution.

**Fails when**
- The argument or evidence is unavailable.
- Critique would depend on invented sources, consensus, or reviewer preferences.
- The user requests abuse, humiliation, or predetermined rejection rather than analysis.
- Ethical or legal issues require specialist review beyond the skill’s competence.

**Guarantees**
- The argument will be represented in its strongest fair form before criticism.
- Objections will identify a target claim, reasoning, severity, and repair path.
- Residual risks will remain visible.

**Does not guarantee**
- Reviewer acceptance, truth, novelty, or freedom from all objections.
- That the proposed repair preserves every ambition of the original thesis.

## When to use

Use after an argument map exists, before submission, during major revision, or when a new concept appears to explain too much. Use when evidence may support rival accounts, when a local interpretation expands into a historical or ontological claim, or when novelty depends on an uncertain genealogy.

Do not use as performative hostility. “Reviewer #2” theater that rewards harshness over accuracy is an anti-pattern.

## Inputs required

Collect:

1. Thesis and enabling claims.
2. Argument map with warrants.
3. Evidence and citation status.
4. Scope boundary.
5. Concept definitions and lineage.
6. Known alternatives and negative cases.
7. Ethical, political, or disciplinary constraints.

If the source base is missing, critique only the formal structure and mark evidentiary judgment `unknown`.

## Procedure

### 1. Steelman the argument

Restate the thesis, claim sequence, evidence, and stakes in the strongest form the supplied materials permit. Ask for researcher confirmation when reconstruction changes emphasis.

### 2. Obtain steelman confirmation

Present the reconstruction to the researcher before adversarial testing. Ask whether it is the strongest version the researcher is prepared to defend and identify any omitted qualification, evidence, or conceptual commitment. Do not proceed as though silence were approval.

When interactive confirmation is unavailable, mark the reconstruction `researcher confirmation required` and limit subsequent objections to provisional status. An agent-generated steelman is not evidence that the author's strongest argument has been captured.

### 3. Prioritize objection dimensions

Choose objection dimensions according to the argument type rather than treating every category as equally important.

- interpretive argument: prioritize object fidelity, warrants, rival readings, and scale;
- historical or genealogical argument: prioritize chronology, transmission evidence, archive coverage, and alternative causal accounts;
- conceptual argument: prioritize definition, boundary, category error, internal consistency, and counterexample;
- comparative argument: prioritize comparability, asymmetry, selection criteria, and translation;
- normative argument: prioritize stated values, affected parties, feasibility, and ethical consequences.

Record why the selected dimensions receive priority.

### 4. Build an objection matrix

Test at least these dimensions:

- evidence adequacy;
- warrant validity;
- concept definition;
- category and level consistency;
- scope and representativeness;
- historical or genealogical support;
- rival explanation;
- counterexample and negative case;
- normative assumption;
- ethical or political consequence;
- false or inflated novelty.

### 5. Test inferential transformations

Look for prohibited movement:

```text
interpretation → fact
correlation → causation
local reading → universal claim
similarity → influence
source mention → source support
new term → new concept
```

### 6. Generate serious alternatives

Construct explanations that account for the same evidence with fewer assumptions or different causal levels. State what additional evidence would discriminate among them.

### 7. Search for counterexamples

Identify cases inside and outside the corpus that would weaken the claim. Do not invent cases; use supplied or verified examples, or mark candidates as `to verify`.

### 8. Audit scope

Compare every major conclusion with the scope boundary. Flag movement across text, corpus, medium, period, geography, institution, or ontology without an explicit bridge.

### 9. Audit concepts

Check equivocation, circular definition, excessive extension, hidden normativity, and collapse of neighboring terms. A concept that explains every outcome is not discriminating enough.

### 10. Rank severity

Use:
- **Fatal:** central thesis cannot stand under current evidence or logic.
- **Major:** substantial revision, new evidence, or re-scoping required.
- **Moderate:** argument remains viable but a section or qualification is needed.
- **Minor:** clarity, terminology, or presentation issue with limited substantive effect.

Also estimate likelihood that an informed reviewer would raise the issue, while marking this as inference rather than fact.

### 11. Select response strategy

For each objection recommend:
- rebut;
- concede;
- narrow;
- redesign;
- defer as limitation;
- seek specialist review.

Do not recommend rhetorical evasion.

### 12. Re-test the repaired thesis

When a repair is proposed, test whether it becomes trivial, circular, or inconsistent with the original question. Record what intellectual cost the repair imposes.

### 13. Issue the gate report

Return `PASS` only when no fatal or unresolved major objection remains. Return `CONDITIONAL PASS` when manageable major risks require named revisions. Return `FAIL` when the central contribution collapses or evidence is fundamentally insufficient.

## Stop signals

Stop when:
- criticism requires sources not available and cannot be framed hypothetically;
- the task becomes ideological endorsement or rejection rather than analysis;
- the user demands proof that the work is worthless or unquestionably original;
- legal, clinical, community safety, or research ethics questions require experts;
- the only viable repair abandons the research question entirely.

## Completion criteria

Complete only when:
- the steelman is accurate and fair;
- each objection targets a specific claim or inference;
- at least one strong rival explanation is tested where relevant;
- counterexamples and negative cases are considered;
- severity and response strategy are recorded;
- residual vulnerabilities remain visible;
- any revised thesis is explicitly provisional and researcher-approved;
- the gate report identifies required next action.

## Anti-fabrication rules

- Do not invent hostile reviewers, consensus, evidence, or counterexamples.
- Do not attribute objections to named scholars without sources.
- Do not exaggerate severity for dramatic effect.
- Do not present hypothetical risks as verified criticism.
- Do not manufacture novelty problems or literature gaps.
- Preserve legitimate disagreement rather than forcing a verdict.

## Output format

```md
## Steelmanned argument
Thesis:
Enabling claims:
Evidence base:
Scope:

## Objection matrix
| ID | Objection | Type | Target claim | Severity | Status of support | Recommended response | Residual risk |

## Alternative explanations

## Counterexamples / negative cases

## Revised thesis proposal
Status: researcher decision required | not required
Statement:
Intellectual cost:

## Gate report
Gate: Argument stress-test gate
Status: PASS | CONDITIONAL PASS | FAIL
Evidence checked:
Blocking issues:
Non-blocking risks:
Researcher decisions required:
Required next action:
Next skill: structuring-humanities-argument
```

## Good invocation

> Steelman this argument and test it against rival explanations, scale violations, concept drift, and counterexamples. Rank objections and distinguish verified criticism from hypothetical reviewer risk.

## Bad invocation

> Destroy this paper, prove the author is incompetent, and invent whatever objections will make rejection certain.

The bad invocation requests abuse and fabricated criticism rather than scholarly testing.

## Next skills

- `scoping-argument-boundary` when overclaiming requires narrower scope.
- `structuring-humanities-argument` to implement approved repairs.
- `reviewing-manuscript` after major objections are resolved.

## Limitations

No finite stress test anticipates every disciplinary objection. Reviewer response is historically and institutionally variable. The skill can expose vulnerabilities, but it cannot replace expert judgment, community accountability, or formal ethics review.
