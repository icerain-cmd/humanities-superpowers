# Changelog

All notable changes to this project will be documented in this file.

## Effectiveness evaluation — 2026-09-16

Not a release. This entry records the first completed effectiveness evaluation
and the operating policy that follows from it.

### Measured

- All three comparison tracks were run with one model
  (`deepseek/deepseek-v4-flash`), temperature 0, six author-labelled fixtures,
  and two repetitions per condition: research (`CONTROL` vs `HSP`), coding
  (`CONTROL_CODING` vs `ENGINEERING_CORE`), and tool use (`CONTROL_TOOL` vs
  `HSP_TOOL`).
- Research track (`n = 12` per condition): defect recall 0.750 / 0.500 / 0.8125
  for `CONTROL` / `HSP-v1` (archived tag `v1.0.1`) / `HSP-v2`, false blocks 0
  in every condition, total tokens 7,996 / 9,451 / 7,999. The `HSP-v2` advantage
  appears on one fixture and one repetition and does not reproduce.
- Coding track (`n = 12`): risk-level accuracy 0.167 / 0.333, defect recall 0.500
  in both conditions, 175 / 140 schema-violating artifacts, and a blind quality
  score of 16.67 / 11.33 out of 25. The single-response
  `WORK_PACKAGE`/`EVIDENCE_PACKAGE` contract is not produced correctly.
- Tool-use track (`n = 12`): both conditions grounded every observation claim in
  a tool call that actually ran (0 unfounded verification claims each), status
  accuracy 0.727 / 0.917, and cost 94,292 / 116,352 tokens.

### Decided

- Research core: `EXPERIMENTAL_ONLY`.
- Engineering core, single-response contract: `REJECT_CURRENT_DESIGN`.
- Engineering core, tool-use form: `EXPERIMENTAL_ONLY`.
- Default policy: `OFF`. Enable selectively where external evidence decides the
  answer.
- The earlier +90.3% token comparison stays recorded as
  `HISTORICAL / NON-REPRODUCIBLE BENCHMARK`; its raw runs, prompt corpus, model
  parameters, and token accounting are not preserved, and it is not merged with
  the current numbers.

### Added

- `docs/evaluation/EFFECTIVENESS_AND_OPERATING_POLICY.md`: the public conclusion,
  the operating policy, the benchmark distinction, and the evidence-before-claim
  rule.
- `docs/evaluation/TOOL_USE_BENCHMARK.md` and `scripts/hsp_eval_tools.py` with
  `tests/eval/tool-cases.json`: a reproducible tool-use comparison, its dataset,
  its deterministic scorer, and a self-test.

### Fixed

- The comparison scorers no longer mis-score a correct answer: identifiers are
  compared by content, an answer without the fenced wrapper is still read, an
  unreadable answer is counted as a miss and still charged, and a defect report
  written in a fixture-declared wording counts as that defect.

## [2.1.0] - 2026-09-15

Version 2.1.0, **Dual-Core**, places a vendored engineering core beside the
unchanged Humanities/Fricturn research protocol. It is a release promotion of
already-verified work, not a new research feature: no comparison run was
executed for this release, so no effectiveness result is recorded.

### Added

- Dual-Core architecture: one router, two cores, and an explicit boundary between scholarship and software.
- An Engineering core built from selected `obra/superpowers` 6.3.0 skills, vendored byte-identically with recorded provenance, per-skill hashes, and documented exclusions.
- `RESEARCH`/`CODE`/`HYBRID` domain routing, so a citation review, a spacing fix, and a fix to the citation verifier itself are routed differently.
- `QUICK`/`STANDARD`/`STRICT` risk calibration for `CODE` and `HYBRID` work, derived from properties (reversibility, blast radius, privilege boundary, persistence, contract surface, environment, failure cost, uncertainty) rather than keywords.
- An Autonomous Worker state contract (`WORKING`, `WAITING_INPUT`, `WAITING_PRIVILEGE`, `BLOCKED`, `ERROR`, `DONE`) in which a live process is not `WORKING` and a terminated process is not `DONE`.
- `WORK_PACKAGE`/`EVIDENCE_PACKAGE` handoff schemas and role-based orchestration (`PLANNER`, `IMPLEMENTER`, `REVIEWER`, `ESCALATION_REVIEWER`) with model names kept in a replaceable operating profile.
- `tests/eval/coding-cases.json` and `scripts/hsp_eval_coding.py`, keeping the coding comparison (`CONTROL_CODING` versus `ENGINEERING_CORE`) separate from the research comparison.

### Fixed

- Reconciled the gate contract: `schemas/gate-report-v2.schema.json` and `schemas/gate-report.schema.json` no longer force `status: PASS` to imply `validity: VALID`, so the official invalidation helper output validates. Historical status, current validity, and progression authorization are now separate and explicitly documented.
- Required an `invalidation_reason` for `INVALIDATED` and `REQUIRES_RECHECK` gates, and allowed an explicitly empty `dependency_refs` list only for `REQUIRES_RECHECK`, where dependency metadata is absent and invalidation cannot be bounded.
- Recorded `invalidation_reason` in `invalidate_dependent_gates()` output and added `progression_authorized()` and `gate_validity_restoration_allowed()` so progression authorization is derived rather than stored.
- Made the documented project-local installs coherent: `templates/` and `schemas/` are now copied alongside the skills, the instruction files name every documented router path, and an existing `AGENTS.md` or `CLAUDE.md` is never overwritten.

### Added

- `tests/regression/gate-validity-cases.json` and an end-to-end contract check in `scripts/run_v2_tests.py` that feed invalidation output into both gate-report profiles and then into the progression rule, covering normal PASS, material dependency change, absent dependency metadata, formatting-only change, and recheck restoration.
- `scripts/check_installation.py`, which executes the documented install commands in throwaway Codex, Claude Code, and Cursor projects and fails when an installed skill or instruction file refers to a path the procedure never copies. It is part of the validation workflow.
- `tests/eval/cases.json`, `scripts/hsp_eval.py`, and [the comparison harness guide](docs/evaluation/HSP_COMPARISON_HARNESS.md) for a reproducible CONTROL-versus-HSP comparison on six task types, with deterministic scoring, a clean case for false blocks, and `NOT_MEASURED` for any metric the response record does not contain. No effectiveness result is recorded by this release.
- Dual-Core: a vendored, unmodified import of ten `obra/superpowers` 6.3.0 engineering skills with `PROVENANCE.json` hashes and documented exclusions, a `RESEARCH`/`CODE`/`HYBRID` domain axis, `QUICK`/`STANDARD`/`STRICT` property-based risk calibration, an autonomous worker state contract, and role-based orchestration handoffs with `WORK_PACKAGE`/`EVIDENCE_PACKAGE` schemas.
- `scripts/run_dual_core_tests.py` and `tests/dual-core/cases.json`, covering domain and risk routing, privilege-boundary escalation, smallest-sufficient routes, rejected completion without verification, worker-state representation, provenance integrity, model-agnostic contracts, and unchanged Humanities regression.
- `tests/eval/coding-cases.json` and `scripts/hsp_eval_coding.py` for the separate `CONTROL_CODING` versus `ENGINEERING_CORE` comparison, scoring risk-level accuracy, defect recall and false positives, completion accuracy, unverified `DONE` claims, false blocks, privilege-boundary state, contract validity, and token/time overhead. It is kept separate from the research comparison on purpose.
- `docs/evaluation/UNATTENDED_AB_WORK_ORDER.md`, the dispatch form of both comparisons: a mandatory unattended preflight header (effective approval policy and sandbox mode must be verified, not assumed), unattended execution rules, the no-silent-stall state contract, decision-autonomy rules, the two tracks, and the required final report.

### Changed

- Public wording now separates design intent from measured effect: the README states that no comparison run has been recorded and that repository validation is not evidence of research benefit.
- `docs/integration/TEST_COVERAGE.md` documents the gate-contract, installation, and evaluation checks and lists research benefit as an unmeasured target.
- The installation guide copies the vendored engineering core and the dual-core specification, and the router names both the research and engineering cores. The 14 Humanities skills, their gates, and their validity rules are unchanged. This release therefore ships as v2.1.0; the Fricturn protocol specification itself stays at `Specification Version: 2.0.0`.

### Preserved

- The existing Humanities/Fricturn research core: the 13 core research skills and the router are byte-identical to the audited tip, and no research semantics changed.
- Gate status, current validity, and progression authorization remain separate properties, and gate invalidation stays bounded by dependency references.
- Epistemic return, citation verification, productive refusal, and human judgment authority are unchanged.
- Installation safety: an existing `AGENTS.md` or `CLAUDE.md` is never overwritten, and `skills/skills/` is never created.
- `vendor/obra-superpowers/**` is byte-identical to the recorded upstream commit.

### Not claimed

- No claim of improved coding quality, reduced defects, or saved tokens. `CODING_EFFECTIVENESS=NOT_MEASURED`, because no `CONTROL_CODING` versus `ENGINEERING_CORE` run has been recorded.
- No claim of improved research quality. `RESEARCH_EFFECTIVENESS=NOT_MEASURED`, because no `CONTROL` versus `HSP` run has been recorded.
- No claim of autonomous runtime notification: the worker state contract is a contract, and no notification runtime is implemented.
- Passing repository, installation, and conformance checks demonstrate internal consistency, not benefit.

## [2.0.0] - 2026-08-21

### Added

- Humanities Superpowers 2.0 Fricturn normative specification and Humanities Engineering methodology.
- Schemas for evidence ledgers, judgment records, interpretation histories, friction events, and epistemic returns.
- Gate-validity and versioning extensions that remain compatible with v1 session and object samples.
- Twelve deterministic conformance cases for unsupported fluency, source mismatch, counterevidence, rival interpretation, productive refusal, agent disagreement, gate invalidation, researcher decisions, append-only history, and no-op returns.
- Four synthetic worked examples for conflict, rival readings, epistemic return, and judgment history.

### Changed

- Extended the Level 3 router and all 13 core skills with friction, judgment, evidence-ledger, history, productive-refusal, epistemic-return, and gate-impact behavior.
- Preserved the existing 13+1 skill structure, verification states, gate statuses, routing decisions, anti-fabrication rules, and human authorization boundary.

## [1.0.0] - 2026-07-19

### Added

- 13 core research skills with a shared contract, gate report, and handoff structure.
- One Level 3 router with explicit state transitions, pause, rollback, stop, and researcher-decision behavior.
- Research Specification v1.0, including the research object model, research grammar, language guide, conformance levels, and extension protocol.
- Quality gates using `PASS`, `CONDITIONAL PASS`, and `FAIL`.
- Research session memory, machine-readable JSON Schemas, deterministic conformance cases, and integrated workflow scenarios.
- End-to-end examples that preserve unresolved evidence and intentional failure rather than declaring false completion.
- English and Korean documentation, a methodology white paper, citation audit, installation guides, and social launch materials.
- GitHub Pages configuration, issue templates, pull request template, release checklist, and public-release validation.
- Claude Code, Codex, and Cursor installation metadata or copy-based installation instructions.
- MIT license, acknowledgments, differences from `obra/superpowers`, and third-party notices.

### Changed during release-candidate review

- Added iterative research-question revision after source exploration.
- Added medium-specific close-reading dimensions for visual, cinematic, interface, performative, architectural, and material objects.
- Added an explicit hermeneutic part-whole iteration protocol.
- Added researcher confirmation and argument-type prioritization to steelman stress testing.
- Distinguished conceptual lineage tracing from Foucauldian genealogy.
- Added a verified white-paper citation audit and corrected canonical citation metadata.
- Made intentional example failure visible in repository validation output.
- Normalized all package, plugin, citation, and skill versions to `1.0.0`.
- Regenerated the release manifest and normalized the public archive root directory.
