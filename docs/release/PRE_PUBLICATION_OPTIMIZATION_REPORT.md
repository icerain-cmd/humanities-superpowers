# Pre-Publication Optimization Report

## 1. Executive verdict

**READY WITH MINOR MANUAL ACTIONS**

No unresolved methodology, integrity, link, secret, or deterministic-validation blocker remains in the local repository. `mkdocs build --strict` passes in an isolated environment created from `site/requirements.txt`. The public Pages site and a successful deployment for the starting `main` commit were independently observed; the pull-request workflow now reruns the full validation set, including MkDocs, before merge.

## 2. Baseline state

- Branch: `chore/pre-publication-polish`
- Starting commit: `9dfe112` (`Update release checklist: mark live-repository checks as completed`)
- Existing release tag: `v1.0.0` at `262e1c6`; it was not moved or modified.
- Starting repository status: clean after a fresh clone of the public repository.
- Baseline validation:
  - `validate_repository.py` failed under the Windows default console encoding and passed only in forced UTF-8 mode.
  - `run_integrated_tests.py` passed 8 scenarios and 33 steps.
  - `validate_public_release.py` failed under the Windows default file encoding. In forced UTF-8 mode, it still failed because CRLF checkout conversion invalidated manifest hashes and two tracked paths differed only by case.
  - `mkdocs build --strict` was unavailable because MkDocs was not installed.

## 3. Issues found

### Blocking

- The public-release validator was not reproducible on the current Windows checkout.
- `site/docs/DIFFERENCES.md` and `site/docs/differences.md` were identical tracked files that collided on case-insensitive filesystems, leaving the working tree one file short of the manifest.

### Major

- README compatibility language did not distinguish tested installations from guidance-only compatibility.
- The Korean README lacked the same compatibility, responsibility, and contribution details as the English README.
- The installation guide did not show complete project-local layouts, guard against `skills/skills/` nesting, verify all 14 `SKILL.md` files, or describe a read-only pilot.
- The public checklist simultaneously described the v1.0.0 GitHub Release as completed and not completed.

### Moderate

- References to 13 research skills, 14 skills, and the orchestrator did not consistently distinguish 13 core research skills from 1 Level 3 router.
- Public social copy described Cursor beside tested harnesses without consistently preserving its unverified status.
- A tracked release-candidate validation log was stale after the public v1.0.0 Release.
- The specification index still labeled v1.0.0 a Phase 3-A draft.

### Minor

- The repository had no LF policy to protect manifest reproducibility across Git configurations.
- The validator checked link existence but not path-case mismatches on case-insensitive systems.

## 4. Changes made

- `README.md`, `README.ko.md`: moved verification status near the Quick Start; stated the project boundary, tested harnesses, Cursor limitation, and the 13-core-plus-router structure; restored semantic parity.
- `INSTALLATION.md`, `site/docs/installation.md`, `site/docs/quick-start.md`: added complete Claude Code and Codex layouts, guidance-only Cursor layout, project-versus-user scope, nesting warnings, file-count checks, a minimal prompt, a read-only pilot layout, and all three validation commands.
- `CHANGELOG.md`, `ROADMAP.md`, `docs/release/RELEASE_NOTES_v1.0.0.md`, `docs/white-paper/HUMANITIES_SUPERPOWERS_WHITE_PAPER.md`, `docs/integration/INTEGRATED_CONFORMANCE.md`, `docs/integration/TEST_COVERAGE.md`, `docs/specification/README.md`, `assets/skill-map.svg`, `site/docs/skills.md`: standardized the distinction between 13 core research skills and 1 Level 3 router.
- `docs/social-media-kit/*`, `site/docs/release/*`: distinguished tested Claude Code and OpenAI Codex routes from unverified Cursor guidance and updated the post-release launch sequence.
- `docs/integration/RELEASE_BLOCKERS.md`, `docs/release/PUBLIC_RELEASE_CHECKLIST.md`: reconciled the documents with the public GitHub state observed on 2026-07-22.
- `scripts/validate_repository.py`: made console output Windows-safe, added public-document checks, and added case-sensitive local-link validation.
- `scripts/run_integrated_tests.py`: made the 14-file result explicit as 13 core research skills plus 1 router.
- `scripts/validate_public_release.py`: made all text decoding explicit UTF-8, added count and compatibility checks, normalized text bytes to the repository LF policy, detected path collisions, and added deterministic manifest regeneration.
- `.github/workflows/validate.yml`: expanded the existing `validate` job to run all three validators and `mkdocs build --strict`.
- `.gitattributes`: established LF text normalization while preserving common binary formats.
- `site/docs/DIFFERENCES.md`: removed the case-colliding duplicate; `site/docs/differences.md` remains canonical.
- `VALIDATION_REPORT.txt`: removed the stale release-candidate log.
- `MANIFEST.json`: regenerated after the final release tree was assembled.

No core skill procedure, router state, schema contract, workflow decision, or intentional example failure was changed.

## 5. Claims and compatibility audit

Tested:

- Claude Code: installation and full pilot reported complete in the supplied release evidence.
- OpenAI Codex: installation and validation complete, including this audit environment.

Unverified:

- Cursor: a rule and installation layout are provided, but target-environment loading was not independently verified.
- Other Markdown-capable agents: manual use may be possible; compatibility is not guaranteed.

Risk-language matches were reviewed in context. Remaining occurrences are negative claims, forbidden examples, submission gates, or narrow procedural contracts. The public descriptions do not claim truth, hallucination prevention, guaranteed citation accuracy, automated peer review, publication readiness, or replacement of scholarly judgment.

## 6. Documentation consistency

- README and README.ko now carry equivalent identity, limitation, compatibility, skill/router, quality-gate, attribution, author, license, installation, and intentional-`FAIL` messages.
- Installation guidance uses the actual project-local discovery paths for Claude Code and Codex and the repository's rule-relative layout for Cursor.
- The release checklist no longer duplicates or contradicts the v1.0.0 Release state.
- The repository contains 14 `SKILL.md` files: 13 core research skills and the `using-humanities-superpowers` Level 3 router.
- `obra/superpowers` remains described as inspiration, independently adapted, and not affiliated or endorsed.

A new Claude Code case study was not added. The external pilot directory may contain unpublished working material, and this audit did not establish a publishable, consent-cleared excerpt. Avoiding accidental disclosure takes priority over adding a launch asset; a sanitized case study can be prepared later.

## 7. Validation results

- `python scripts/validate_repository.py`: **PASS**; intentional example `FAIL` preserved.
- `python scripts/run_integrated_tests.py`: **PASS**; 8 scenarios, 33 steps, 14 `SKILL.md` files, 5 decisions.
- `python scripts/validate_public_release.py`: **PASS** after final manifest regeneration.
- `mkdocs build --strict`: **PASS** using the pinned dependencies in `site/requirements.txt`.
- Local link and path-case checks: **PASS** through `validate_repository.py`.
- `git diff --check`: **PASS**.
- `git fsck --no-reflogs --full`: **PASS**.
- Working-tree and reachable-history secret scans: **PASS**; no matching credentials or private-key material.
- Local-path, archive, and large-file scan: **PASS**.

The current public repository page, documentation URL, and v1.0.0 Release page returned HTTP 200 during the audit. The public Actions history showed a successful documentation deployment for the starting `main` commit, and the changed documentation builds successfully in the local isolated environment.

## 8. Remaining manual GitHub actions

- Description: already matches `Structured research skills and quality gates for humanities scholars using AI agents.`
- Topics: the 10 recommended topics are set: `humanities`, `digital-humanities`, `research-methodology`, `ai-agents`, `agent-skills`, `scholarly-writing`, `citation-verification`, `close-reading`, `claude-code`, and `openai-codex`.
- Issues: enabled.
- Discussions: enabled.
- Pages: the homepage points to the public documentation site; the current site and prior deployment are verified. The updated PR check runs a strict documentation build before merge, and the Pages workflow will redeploy after merge to `main`.
- Release: published v1.0.0 verified. Do not rewrite it or move its tag.
- Branch protection: `main` requires the `validate` status check, linear history, and resolved conversations. Force pushes and deletion are disabled.
- Cursor: independently verify rule and skill loading or retain the unverified-guidance label.

## 9. Release recommendation

**Prepare v1.0.1.**

The existing v1.0.0 tag points to an earlier commit, and this audit fixes more than prose: it removes a cross-platform path collision and repairs Windows release validation. Publish these changes as a patch after CI and rendered-document review. Do not force-move `v1.0.0`.

## 10. Exact public announcement status

Safe claims:

- Humanities Superpowers provides 13 core research skills and 1 Level 3 router for AI-assisted humanities research.
- It uses explicit quality gates and preserves unresolved evidence and intentional failure states.
- Claude Code and OpenAI Codex installations have been tested.
- Cursor installation guidance is available but has not yet been independently verified.
- The framework supports scholarly judgment and citation auditing without replacing researcher verification or authorship.

Claims to avoid:

- that the framework prevents hallucinations or guarantees truth or citation accuracy;
- that it automatically makes manuscripts publication-ready;
- that it automates or replaces peer review;
- that all agent harnesses behave identically;
- that Cursor loading has been verified before a target-environment test is completed.
