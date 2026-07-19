# Public Release Checklist

This checklist separates checks completed in the release archive from operations that require a live GitHub repository or an installed agent harness. A checked item records evidence available in this archive; it does not claim that external hosting settings have already been configured.

## Archive checks completed

- [x] Author name, affiliation, email, and GitHub username are populated.
- [x] MIT license text is present.
- [x] Acknowledgments, differences, and third-party notices are present.
- [x] No unpublished manuscript, reviewer identity, personal address, API key, access token, or private key was detected by the release validator.
- [x] Text, JSON, YAML, workflow, and metadata placeholders covered by the validator are absent.
- [x] Project, plugin, specification, and conformance versions are aligned to `1.0.0`.
- [x] `MANIFEST.json` was regenerated from the current release tree.
- [x] `python3 scripts/validate_repository.py` passes.
- [x] `python3 scripts/run_integrated_tests.py` passes.
- [x] `python3 scripts/validate_public_release.py` passes.
- [x] `mkdocs build --strict` passes in the release environment.

## Live-repository checks still required

- [x] Create or update the GitHub repository and push the release candidate.
- [x] Inspect README and internal links in GitHub's rendered view.
- [x] Confirm that Git history contains no sensitive files.
- [x] Run the GitHub Pages workflow and inspect the deployed site.

- [x] Create a GitHub Release with the v1.0.0 tag, release notes, and the signed release archive.
- [ ] Test Cursor rule loading in the target environment.
- [ ] Set repository description and topics.
- [ ] Enable Issues and Discussions as intended.
- [ ] Configure Pages to use GitHub Actions.
- [ ] Configure branch protection after the first push.
- [ ] Create and publish Release `v1.0.0` from `docs/release/RELEASE_NOTES_v1.0.0.md`.
