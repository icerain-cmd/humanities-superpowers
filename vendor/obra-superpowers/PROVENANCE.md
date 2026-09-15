# Vendored upstream: obra/superpowers

This directory is a partial, unmodified import of a third-party skills
library. Nothing under `vendor/` is authored by Humanities Superpowers and
nothing under `vendor/` may be edited in place.

| Field | Value |
|---|---|
| Upstream repository | <https://github.com/obra/superpowers> |
| Upstream version | 6.3.0 |
| Upstream commit | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` |
| Commit date | 2026-08-12 |
| License | MIT (`LICENSE` in this directory) |
| Copyright | Copyright (c) 2025 Jesse Vincent |
| Imported | 2026-09-15 |
| Import method | `git archive <commit> -- <selected paths> \| tar -x` |

Machine-readable provenance, per-skill tree hashes, and the exclusion reasons
are in [`PROVENANCE.json`](PROVENANCE.json). `scripts/run_dual_core_tests.py`
recomputes those hashes and fails if any vendored byte changes.

## Imported skills (10 of 14)

| Skill | Files | Why it is in the engineering core |
|---|---:|---|
| `writing-plans` | 2 | Turns an approved design into bite-sized, testable tasks |
| `executing-plans` | 1 | Executes a plan task by task with checkpoints |
| `test-driven-development` | 2 | Test first, watch it fail, then implement |
| `systematic-debugging` | 11 | Root cause before fix; symptom patches are treated as failure |
| `verification-before-completion` | 1 | Evidence before completion claims |
| `requesting-code-review` | 2 | Review request with the context a reviewer needs |
| `receiving-code-review` | 1 | Evaluate review feedback on technical grounds, not deference |
| `dispatching-parallel-agents` | 1 | Independent workstreams without shared state |
| `using-git-worktrees` | 1 | Isolated working trees for parallel branches |
| `finishing-a-development-branch` | 1 | Merge, verify, and clean up a finished branch |

## Excluded skills and reasons

| Skill | Reason |
|---|---|
| `using-superpowers` | Upstream's own router. This repository ships its own dual-core router; a second router would create competing entry points and encourage loading every skill. |
| `brainstorming` | Ships a Node HTTP server and browser visual companion (`scripts/server.cjs`, `start-server.sh`, `stop-server.sh`, `frame-template.html`) plus an upstream three-path router. That is a runtime dependency outside this repository's Python/shell footprint and duplicates the domain/risk routing defined here. |
| `writing-skills` | Skill-authoring methodology. This repository already owns its skill contract (`docs/SKILL_SCHEMA.md`, `docs/specification/SKILL_CONTRACT.md`). |
| `subagent-driven-development` | Ships a second orchestration contract (bash scripts plus a `.superpowers/sdd` workspace) parallel to the role-based `WORK_PACKAGE`/`EVIDENCE_PACKAGE` handoff in `docs/specification/dual-core/AGENT_ORCHESTRATION.md`. Two orchestration contracts violate the minimum-sufficient-record rule; `dispatching-parallel-agents` covers the parallelism need. |

## Update procedure

1. Fetch the upstream repository and choose the target tag or commit.
2. Diff the candidate commit against the recorded commit for every imported skill.
3. Re-run the import with `git archive <new-commit> -- <selected paths> LICENSE | tar -x`.
4. Recompute per-skill `tree_sha256` and `aggregate_sha256` with the definition in `PROVENANCE.json`, and update `version`, `commit`, `commit_date`, and `imported_at`.
5. Record newly excluded or newly included skills with a reason.
6. Run `python3 scripts/run_dual_core_tests.py` and the full validation set.
7. Update `THIRD_PARTY_NOTICES.md` if the license or attribution changes.

## Boundary rule

Upstream teaches software-engineering practice. Humanities Superpowers teaches
scholarly judgment. The two cores are kept in separate trees so that an
upstream update can never silently rewrite a Humanities skill, and so that a
Humanities revision can never be mistaken for an upstream contribution.
