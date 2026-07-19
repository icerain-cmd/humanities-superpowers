# Skill Contract Specification

## 1. Contract purpose

A skill contract makes the relationship between skills explicit. It states what a skill accepts, what it produces, when it must stop, and what it does not guarantee.

Every core skill in Phase 3-B MUST include a `## Contract` section immediately after `## Purpose`.

## 2. Required contract fields

```md
## Contract

**Accepts**
- Research objects or files the skill may consume.

**Requires**
- Minimum information without which the skill cannot proceed responsibly.

**Produces**
- Named artifacts and their required fields.

**May produce**
- Optional artifacts or diagnostic reports.

**Fails when**
- Blocking conditions that force a FAIL or unresolved-item return.

**Guarantees**
- Narrow procedural guarantees that the skill can actually enforce.

**Does not guarantee**
- Truth, originality, publication, completeness, or other outcomes outside the procedure.
```

## 3. Contract rules

### 3.1 Accepts versus requires

`Accepts` describes compatible input types. `Requires` describes the minimum valid subset. A skill MUST NOT pretend to execute fully when required inputs are absent.

### 3.2 Outputs must be inspectable

Each produced artifact MUST have a stable name and observable fields. “A better argument” is not a valid output description. `argument-map.md` with claims, reasons, evidence needs, objections, and dependencies is valid.

### 3.3 Failure conditions must be scholarly

Failure conditions SHOULD represent missing evidence, unstable concepts, inaccessible corpora, circular reasoning, unresolved objections, or incompatible constraints. They MUST NOT be limited to technical errors.

### 3.4 Guarantees must be narrow

Permitted guarantee:

> Guarantees that every citation record is assigned an explicit verification state.

Forbidden guarantee:

> Guarantees that all citations are accurate.

### 3.5 Handoffs

A contract MUST name the objects made available to the next skill. The `Next skills` section MUST explain the condition for each transition.

## 4. Standard execution record

Every completed skill SHOULD be able to emit this record:

```yaml
skill: formulating-research-question
skill_version: 1.0.0
run_status: PASS | CONDITIONAL_PASS | FAIL
inputs:
  - type: research_brief
    location: input/research-brief.md
outputs:
  - type: research_question
    location: output/research-question.md
verification_summary:
  verified: 0
  researcher_supplied: 3
  inference: 2
  unverified: 1
blocking_issues: []
researcher_decisions_required: []
next_skill: scoping-argument-boundary
```

## 5. Contract compatibility

A downstream skill is compatible when:

- its required input type is produced by the upstream skill;
- required fields are present;
- verification states are not discarded;
- unresolved blockers are not silently removed.

## 6. Contract template

See [`templates/skill-contract.md`](../../templates/skill-contract.md).
