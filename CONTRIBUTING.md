# Contributing

Contributions should make scholarly practice more explicit, testable, and accountable without pretending that interpretive judgment can be automated away.

## Before opening a pull request

1. Run `python3 scripts/validate_repository.py`.
2. Keep each skill focused on one reusable research operation.
3. Use the canonical metadata and section schema in `docs/SKILL_SCHEMA.md`.
4. Add or update a routing case in `tests/invocation-cases.yaml`.
5. Do not add invented bibliographic examples. Clearly label fictional or incomplete records.
6. Do not claim that a procedure guarantees truth, originality, acceptance, or citation accuracy.

## A strong skill contribution

A strong skill has a precise trigger, required inputs, a repeatable procedure, meaningful stop signals, observable completion criteria, anti-fabrication rules, and an output template. It also explains what the skill cannot establish.

## Pull request checklist

- [ ] The skill solves a recurring research problem.
- [ ] Its description states when it should be used.
- [ ] It has all required sections.
- [ ] It preserves uncertainty rather than filling gaps.
- [ ] It adds a good and bad invocation example.
- [ ] It includes at least one test-routing case.
- [ ] All internal links and metadata validate.

## Conduct

Be rigorous about arguments and generous toward contributors. Critique claims, methods, and evidence; do not attack persons or disciplines. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
