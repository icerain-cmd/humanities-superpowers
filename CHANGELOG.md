# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Fixed

- Reconciled the gate contract: `schemas/gate-report-v2.schema.json` and `schemas/gate-report.schema.json` no longer force `status: PASS` to imply `validity: VALID`, so the official invalidation helper output validates. Historical status, current validity, and progression authorization are now separate and explicitly documented.
- Required an `invalidation_reason` for `INVALIDATED` and `REQUIRES_RECHECK` gates, and allowed an explicitly empty `dependency_refs` list only for `REQUIRES_RECHECK`, where dependency metadata is absent and invalidation cannot be bounded.
- Recorded `invalidation_reason` in `invalidate_dependent_gates()` output and added `progression_authorized()` and `gate_validity_restoration_allowed()` so progression authorization is derived rather than stored.
- Made the documented project-local installs coherent: `templates/` and `schemas/` are now copied alongside the skills, the instruction files name every documented router path, and an existing `AGENTS.md` or `CLAUDE.md` is never overwritten.

### Added

- `tests/regression/gate-validity-cases.json` and an end-to-end contract check in `scripts/run_v2_tests.py` that feed invalidation output into both gate-report profiles and then into the progression rule, covering normal PASS, material dependency change, absent dependency metadata, formatting-only change, and recheck restoration.
- `scripts/check_installation.py`, which executes the documented install commands in throwaway Codex, Claude Code, and Cursor projects and fails when an installed skill or instruction file refers to a path the procedure never copies. It is part of the validation workflow.
- `tests/eval/cases.json`, `scripts/hsp_eval.py`, and [the comparison harness guide](docs/evaluation/HSP_COMPARISON_HARNESS.md) for a reproducible CONTROL-versus-HSP comparison on six task types, with deterministic scoring, a clean case for false blocks, and `NOT_MEASURED` for any metric the response record does not contain. No effectiveness result is recorded by this release.

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
