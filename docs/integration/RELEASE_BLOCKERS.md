# Release Blockers

For Fricturn 2.0, release is blocked if any new schema fails Draft 2020-12 parsing, any of the 14 skills lacks its friction contract, gate status vocabulary changes, agent recommendation can become an accepted decision without human authorization, a prior `PASS` remains valid after a materially changed dependency, or the v2 conformance runner fails.

## Methodology and integration status

No deterministic methodology or integration blocker remains in the conformance suite.

## Public-release operations that remain outside the archive

These are hosting and live-environment checks, not claims that the archive has already completed them:

The public repository, rendered README, Pages site, Issues setting, and published `v1.0.0` Release were independently observed on 2026-07-22. The remaining external actions are:

1. Test rule and skill loading in an actual Cursor environment; until then, retain the unverified-guidance label.
2. Add repository topics.
3. Decide whether Discussions and branch protection should be enabled.
4. Publish subsequent fixes without moving or rewriting the existing `v1.0.0` tag and Release.

## Explicit non-blocking limitations

- Cross-harness behavioral equivalence has not been demonstrated.
- The framework reduces risk; it does not guarantee factual or citation accuracy.
- The worked end-to-end example uses bounded illustrative material and is not evidence of publication effectiveness.
- Discipline profiles beyond general humanities methodology are not included in v1.0.
