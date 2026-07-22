# Public Release Checklist

Checked 2026-07-22 against local commit `9dfe112` and the public GitHub repository. A checked item has direct local or public evidence. `[-]` means the item could not be independently verified in this environment; it is not a completion mark.

## Repository checks

- [x] Author name, affiliation, email, and GitHub username are populated.
- [x] MIT license text is present.
- [x] Acknowledgments, differences, and third-party notices preserve the project's inspiration, independent adaptation, and non-affiliation statements.
- [x] Project, plugin, specification, conformance, citation, and skill versions are aligned to `1.0.0`.
- [x] The worked example preserves its intentional final `FAIL`.
- [x] `MANIFEST.json` was regenerated from the final pre-publication tree.
- [x] All three Python validators pass after the pre-publication changes.
- [x] `mkdocs build --strict` passes in an isolated environment using `site/requirements.txt`.
- [x] Final secret, local-path, large-file, and Git object checks pass after the pre-publication changes.

## Agent-harness verification

- [x] Claude Code installation and full pilot completed.
- [x] OpenAI Codex installation and validation completed.
- [ ] Cursor rule and skill loading have not been independently verified in a target Cursor environment.
- [-] Other Markdown-capable agents may read the skills manually, but compatibility is not guaranteed.

## Public GitHub state

- [x] The repository is public and `main` is the default branch.
- [x] The repository description is `Structured research skills and quality gates for humanities scholars using AI agents.`
- [x] The 10 recommended repository topics are set.
- [x] Issues are enabled.
- [x] Discussions are enabled.
- [x] The repository page and rendered README return HTTP 200.
- [x] The documentation site at `https://icerain-cmd.github.io/humanities-superpowers/` returns HTTP 200, and the public Actions history contains a successful deployment for `main`.
- [x] GitHub Release `v1.0.0` exists and is published, not draft or prerelease.
- [x] `main` branch protection requires the `validate` check, linear history, and conversation resolution; force pushes and branch deletion are disabled.

## Before the next announcement or patch release

- [ ] Review and publish the pre-publication changes without moving the existing `v1.0.0` tag.
- [x] Set the recommended repository topics.
- [x] Enable Discussions and protect `main` with the repository validation check.
- [ ] Independently test Cursor loading or continue to label it as unverified guidance.
- [ ] If these changes are released as a patch, prepare `v1.0.1` notes and a new release artifact rather than rewriting the existing `v1.0.0` Release.
