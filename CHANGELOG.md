# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

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
