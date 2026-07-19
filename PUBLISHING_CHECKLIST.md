# Publishing checklist

## Required identity replacement

Run:

```bash
python3 scripts/prepare_release.py "Your Full Name" "GitHubUsername" "icerain@jj.ac.kr" "FamilyName|GivenName"
```

Then review:

- [ ] `project.json`
- [ ] `CITATION.cff`
- [ ] `LICENSE`
- [ ] plugin manifests
- [ ] contact details in `SECURITY.md` and `CODE_OF_CONDUCT.md`

## Repository checks

- [ ] `python3 scripts/validate_repository.py` passes.
- [ ] All links render on GitHub.
- [ ] The example intentionally ends in `FAIL` because citations are unresolved.
- [ ] No private research files, credentials, or personal data are present.
- [ ] GitHub repository description and topics are set.
- [ ] First release is tagged `v1.0.0`.

## Suggested GitHub description

> Structured research skills and quality gates for humanities scholars using AI agents.

## Suggested topics

`humanities` `research-methodology` `ai-agents` `scholarly-writing` `agent-skills` `close-reading` `citation-verification` `claude-code` `codex` `cursor`
