# Test Coverage Report

## Fricturn cases

The v2 deterministic suite contains twelve cases across `tests/friction`, `tests/judgment`, `tests/return`, and `tests/regression`. The existing eight integrated scenarios and all v1 conformance fixtures remain active.

## Scope

The repository contains three layers of deterministic tests.

| Layer | Purpose | Cases |
|---|---|---:|
| Invocation | Basic trigger examples | repository-defined |
| Skill conformance | Positive, negative, missing-input, adversarial, and handoff behavior | 65 |
| Integrated conformance | State transitions, rollback, session resume, and end-to-end paths | 8 scenarios / 33 steps |

## Skill coverage

All 14 `SKILL.md` files—13 core research skills and 1 Level 3 router—are exercised by the integrated suite.

| Skill | Integrated scenarios |
|---|---|
| using-humanities-superpowers | all scenarios |
| formulating-research-question | clean-forward, session-resume |
| scoping-argument-boundary | clean-forward, scope-rollback |
| mapping-concept-lineage | clean-forward, researcher-decision |
| conducting-literature-dialogue | clean-forward, argument-rollback |
| planning-humanities-argument | clean-forward, argument-rollback |
| performing-close-reading | clean-forward, researcher-decision |
| structuring-humanities-argument | clean-forward, peer-review-loop |
| stress-testing-argument | clean-forward, scope-rollback |
| auditing-citations | clean-forward, argument-rollback, submission-failure |
| checking-terminology-consistency | clean-forward, peer-review-loop |
| reviewing-manuscript | clean-forward, peer-review-loop |
| responding-to-peer-review | peer-review-loop |
| verifying-before-submission | clean-forward, submission-failure |

## Routing-decision coverage

- `PROCEED`: covered
- `PAUSE`: covered
- `ROLLBACK`: covered
- `RESEARCHER_DECISION_REQUIRED`: covered
- `STOP`: covered

## Known limits

The suite verifies declared behavior and artifact consistency. It does not yet measure:

- inter-model agreement;
- discipline-specific validity;
- citation retrieval accuracy in live environments;
- whether a particular harness follows every instruction;
- user learning outcomes;
- publication outcomes.

These are empirical evaluation targets for the post-v1.0 roadmap.
