# Conformance and Testing

## 1. Purpose

Conformance checks whether a skill follows the shared method. It does not certify the truth of a research outcome.

## 2. Levels

### Level 0 — Parseable

- YAML front matter parses.
- `name`, `description`, `version`, `language`, and `license` exist.
- Directory name matches skill name.

### Level 1 — Document conformant

- all canonical sections exist in order;
- triggering description begins with a use condition;
- output format is explicit;
- good and bad invocations are present.

### Level 2 — Contract conformant

- Contract section exists;
- accepts, requires, produces, fails when, guarantees, and non-guarantees are present;
- outputs map to research object types;
- stop signals map to blockers or unresolved items.

### Level 3 — Workflow conformant

- next-skill transitions declare conditions;
- input/output compatibility is testable;
- verification states survive handoff;
- loops back to earlier skills are explained.

### Level 4 — Evidence conformant

- fabricated bibliographic details are prohibited;
- source existence and claim support are separate checks;
- unknown and disputed states are preserved;
- examples include at least one responsible failure path.

### Level 5 — Release conformant

- repository validator passes;
- invocation tests pass;
- links and JSON metadata validate;
- no release placeholders remain;
- changes are documented.

## 3. Required test categories

1. **Positive invocation:** clear task triggers the correct skill.
2. **Negative invocation:** unrelated task does not trigger the skill.
3. **Ambiguous invocation:** router asks for or infers the minimum clarification.
4. **Missing-input test:** skill returns unresolved items rather than fabricating.
5. **Adversarial test:** user requests proof, novelty inflation, or invented citations.
6. **Handoff test:** output satisfies the next skill’s required input.
7. **Failure-path test:** at least one example ends in a justified FAIL.
8. **Terminology test:** required status vocabulary is used consistently.

## 4. Conformance manifest

Each migrated skill SHOULD include an entry in `tests/conformance/skills.yaml`:

```yaml
- skill: auditing-citations
  level: 2
  tests:
    positive: true
    negative: true
    missing_input: true
    adversarial: true
    handoff: false
  notes: "Workflow handoff test pending."
```

## 5. Validator behavior

The repository validator MUST distinguish errors from warnings.

- **Error:** release-blocking nonconformance.
- **Warning:** declared migration gap or recommended improvement.

During Phase 3-A, legacy core skills may remain Level 1. Phase 3-B release is blocked until all 13 core skills reach Level 2 and the router reaches Level 3.

## 6. Human evaluation

Automated tests cannot assess interpretive quality fully. Each core skill SHOULD receive at least two human walkthroughs using different disciplines or corpora before v1.0.

Reviewers SHOULD examine:

- whether the procedure exposes rather than conceals uncertainty;
- whether output improves scholarly decisions;
- whether the skill over-structures interpretive work;
- whether stop signals are appropriately sensitive;
- whether the agent adds unsourced claims.
