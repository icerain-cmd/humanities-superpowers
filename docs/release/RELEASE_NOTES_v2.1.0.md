# Humanities Superpowers v2.1.0 — Dual-Core

Released 2026-09-15.

Humanities Superpowers v2.1.0 promotes the verified Dual-Core work into a release. It is not a new research feature: the Humanities/Fricturn research core keeps its 13 core skills, its router semantics, its verification states, its gate statuses, its validity rules, and its human authorization boundary.

## What v2.1.0 contains

One router, two cores, and an explicit boundary between them.

```text
                  Router
                     |
        -----------------------------
        |             |             |
     RESEARCH       CODE        HYBRID
        |             |             |
   Humanities   Engineering    Both cores
      Core          Core
```

## Added

- **Dual-Core architecture** — a research core and an engineering core reached through one router, with an explicit domain boundary.
- **Engineering core** — ten selected `obra/superpowers` 6.3.0 skills, vendored byte-identically with per-skill hashes, import commit, license, and a documented reason for every excluded skill.
- **`RESEARCH` / `CODE` / `HYBRID` routing** — semantic classification by the artifact that must be correct, not by keywords.
- **`QUICK` / `STANDARD` / `STRICT` risk routing** — applied to code and hybrid work, derived from reversibility, blast radius, privilege boundary, persistence, contract surface, environment, failure cost, and uncertainty.
- **Autonomous Worker state contract** — `WORKING`, `WAITING_INPUT`, `WAITING_PRIVILEGE`, `BLOCKED`, `ERROR`, `DONE`, where a live process is not `WORKING` and a terminated process is not `DONE`.
- **`WORK_PACKAGE` / `EVIDENCE_PACKAGE`** — handoff records between role-based `PLANNER`, `IMPLEMENTER`, `REVIEWER`, and `ESCALATION_REVIEWER` assignments, with model names confined to a replaceable operating profile.
- **Coding evaluation harness** — `scripts/hsp_eval_coding.py` and `tests/eval/coding-cases.json` for the separate `CONTROL_CODING` versus `ENGINEERING_CORE` comparison.

## Preserved

- The 13 core research skill bodies are unchanged from the audited tip (`2a452b6`); only the release-metadata `version:` line changed, from `2.0.0` to `2.1.0`.
- Gate status, current validity, and progression authorization stay separate properties, and invalidation remains bounded by dependency references.
- Epistemic return, citation verification, productive refusal, terminology control, and human judgment authority are unchanged.
- Installation safety: an existing `AGENTS.md` or `CLAUDE.md` is never overwritten, and `skills/skills/` is never created.
- `vendor/obra-superpowers/**` is byte-identical to upstream commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`.

## Not claimed

- **Coding effectiveness: `NOT_MEASURED`.** No `CONTROL_CODING` versus `ENGINEERING_CORE` run has been recorded, so this release claims no coding-quality improvement, no defect reduction, and no token saving.
- **Research effectiveness: `NOT_MEASURED`.** No `CONTROL` versus `HSP` run has been recorded, so this release claims no research-quality improvement.
- **Runtime notification: not implemented.** The worker state contract is a contract. No Telegram, Hermes, or other notification runtime ships with this release.
- Passing repository, installation, and conformance checks demonstrate internal consistency. They are not evidence of benefit.

## Version scope

v2.1.0 is the project release version. It is not the Fricturn protocol version: the v2 specification documents remain at `Specification Version: 2.0.0`, schema identifiers are unchanged, and `schema_version` values in protocol records are unchanged.

## Provenance

| Field | Value |
|---|---|
| Upstream repository | `https://github.com/obra/superpowers` |
| Upstream version | `6.3.0` |
| Upstream commit | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` |
| Upstream license | MIT, Copyright (c) 2025 Jesse Vincent |
| Imported skills | 10 of 14 |
| Record | `vendor/obra-superpowers/PROVENANCE.json` |

The vendored files are unmodified. `scripts/run_dual_core_tests.py` recomputes the recorded hashes and fails if any vendored byte changes.

## Validation

The release candidate passed repository validation, integrated tests, v2 conformance tests, dual-core routing and provenance tests, public-release validation, installation smoke tests for the documented Codex and Claude Code layouts, Cursor layout checks, both evaluation self-tests, and a strict documentation build. Manifest hashes were regenerated from the release tree.
