# Humanities Superpowers

[한국어](README.ko.md) · [Quick start](INSTALLATION.md) · [White paper](docs/white-paper/HUMANITIES_SUPERPOWERS_WHITE_PAPER.md) · [Manifesto](MANIFESTO.md) · [Examples](#worked-examples)

**Structured research skills and quality gates for humanities scholars using AI agents.**

> **Not an AI paper writer. A scholarly judgment scaffold.**

Humanities Superpowers helps researchers slow down the moments where fluent AI output is most dangerous: framing a question, defining concepts, connecting claims to evidence, testing objections, checking citations, and deciding whether a manuscript is ready to submit.

It supports scholarly judgment. It does not replace interpretation, source verification, ethics, or authorship.

<p align="center"><img src="assets/research-pipeline.svg" alt="Research pipeline from question to submission gate" width="100%"></p>

## Quick start

```bash
git clone https://github.com/icerain-cmd/humanities-superpowers.git
cd humanities-superpowers
python3 scripts/validate_repository.py
```

Copy `skills/` into your agent's skill directory, or follow [INSTALLATION.md](INSTALLATION.md).

Then ask:

> Use Humanities Superpowers to formulate a research question about artificial nature and platform aesthetics. Separate verified evidence, interpretation, inference, hypothesis, and unknowns. Do not invent sources.

For a complete workflow:

> Follow `workflows/write-a-paper.md`. Stop at every quality gate and report unresolved risks before proceeding.

## Why it exists

AI agents can produce polished academic prose before the underlying research has been verified. Humanities research requires a different discipline: conceptual lineage, close reading, argumentative restraint, traceable evidence, serious counterarguments, and explicit uncertainty.

The framework therefore organizes work around three commitments:

- **Research before prose**
- **Evidence over confidence**
- **Completion must be demonstrated**

Read the [methodology white paper](docs/white-paper/HUMANITIES_SUPERPOWERS_WHITE_PAPER.md), [project philosophy](docs/PHILOSOPHY.md), and [design principles](docs/DESIGN_PRINCIPLES.md).

## Thirteen research skills

<p align="center"><img src="assets/skill-map.svg" alt="Map of thirteen Humanities Superpowers skills" width="100%"></p>

| Research responsibility | Skill |
|---|---|
| Turn a topic into an arguable question | `formulating-research-question` |
| Define what the argument will and will not claim | `scoping-argument-boundary` |
| Trace a concept across thinkers and contexts | `mapping-concept-lineage` |
| Turn sources into a scholarly conversation, not a summary list | `conducting-literature-dialogue` |
| Build a claim–reason–evidence structure | `planning-humanities-argument` |
| Analyze passages, images, and media artifacts closely | `performing-close-reading` |
| Structure the researcher's argument without ghostwriting it | `structuring-humanities-argument` |
| Attack the argument before reviewers do | `stress-testing-argument` |
| Verify citation existence and claim–source fit | `auditing-citations` |
| Keep concepts and translations stable | `checking-terminology-consistency` |
| Simulate a rigorous manuscript review | `reviewing-manuscript` |
| Convert reviews into traceable revisions | `responding-to-peer-review` |
| Run a final PASS/FAIL submission gate | `verifying-before-submission` |

Each skill defines invocation conditions, required inputs, a procedure, stop signals, anti-fabrication rules, completion criteria, output records, and next steps.

## Research quality gates

<p align="center"><img src="assets/quality-gates.svg" alt="Eight research quality gates and their possible statuses" width="100%"></p>

A gate returns:

- `PASS` — no known blocking issue remains;
- `CONDITIONAL PASS` — recorded risks are explicitly accepted;
- `FAIL` — evidence, verification, or researcher judgment is still missing.

A failed gate is not a broken workflow. It is a refusal to hide unresolved scholarly risk. See [QUALITY_GATES.md](docs/QUALITY_GATES.md).

## Human–AI division of responsibility

<p align="center"><img src="assets/human-ai-collaboration.svg" alt="Researcher, shared, and AI responsibilities" width="100%"></p>

AI may organize, compare, test, and flag. The researcher remains responsible for significance, interpretation, source verification, ethics, conceptual commitments, disclosure, and final authorship.

## Worked examples

### End-to-end concept paper

[Artificial Nature and Platform Mediation](examples/concept-paper-example/README.md) runs from a research brief through question formation, scope, concept lineage, argument mapping, terminology control, citation audit, and final verification.

**The final gate intentionally returns `FAIL`.** No verified source set is supplied, so the framework refuses to label the project publication-ready. This is expected behavior.

### Focused examples

- [Argument-map example](examples/argument-map-example/README.md)
- [Terminology-audit example](examples/terminology-audit-example/README.md)

## What this project does not claim

Humanities Superpowers does not guarantee truth, originality, acceptance, or citation accuracy. It does not turn an AI agent into an autonomous scholar. It reduces avoidable risk by making assumptions, evidence, unresolved verification, and researcher decisions visible.

See [ANTI_PATTERNS.md](docs/ANTI_PATTERNS.md) for common failure modes.

## Supported environments

The repository provides manifests or copy-based installation routes for OpenAI Codex, Claude Code, Cursor, and agents capable of reading Markdown skills and project instructions. Product conventions change; compatibility does not imply marketplace endorsement. See [INSTALLATION.md](INSTALLATION.md).

## Origin and independence

Humanities Superpowers was inspired by Jesse Vincent's [`obra/superpowers`](https://github.com/obra/superpowers), which applies composable skills and systematic verification to coding agents. This project independently adapts that general design idea to humanities research.

It is not affiliated with, endorsed by, or maintained by Jesse Vincent, Prime Radiant, or the Superpowers project. See [ACKNOWLEDGMENTS.md](ACKNOWLEDGMENTS.md), [DIFFERENCES.md](DIFFERENCES.md), and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Author

**Lee Yong Wook** · Jeonju University  
GitHub: [`@icerain-cmd`](https://github.com/icerain-cmd) · [icerain@jj.ac.kr](mailto:icerain@jj.ac.kr)

## Contributing, citation, and license

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request. Citation metadata is provided in [CITATION.cff](CITATION.cff). Released under the [MIT License](LICENSE).


## Research orchestration

The Level 3 router diagnoses the current research state, selects the smallest valid skill route, and treats failed gates as reasons to pause or roll back—not as obstacles to hide. It can preserve a resumable session record without treating memory as evidence.

- [Research state machine](docs/orchestration/RESEARCH_STATE_MACHINE.md)
- [Routing and rollback](docs/orchestration/ROUTING_AND_ROLLBACK.md)
- [Session memory](docs/orchestration/SESSION_MEMORY.md)

## Documentation site

The repository includes a MkDocs Material site configured for GitHub Pages. After enabling **Settings → Pages → GitHub Actions**, pushes to `main` deploy the documentation automatically.

## Public release status

The v1.0.0 release notes and final publication checklist are available in [`docs/release/`](docs/release/).


## Social media launch kit

- [Social media launch kit](docs/social-media-kit/README.md)
