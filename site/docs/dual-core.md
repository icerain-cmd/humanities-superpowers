# Dual-Core 2.1

Humanities Superpowers 2.1.0 ships two cores behind one router. The research core is unchanged; a vendored engineering core is added beside it.

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

## The two cores

- **Humanities (research)** — 13 core research skills plus the router: questions, concepts, close reading, citation audit, gates, epistemic return. This is the Fricturn protocol, and its specification version is unchanged at `2.0.0`.
- **Engineering (code)** — ten selected skills from [`obra/superpowers`](https://github.com/obra/superpowers) 6.3.0, vendored unmodified under `vendor/obra-superpowers/` with per-skill hashes, the import commit, and the reason for every excluded skill.

## Two axes

**Domain.** `RESEARCH` when the artifact that must be correct is scholarship, `CODE` when it is software or configuration, `HYBRID` when the correctness of one depends on the other. Classification is semantic, not lexical: "review" and "verify" appear in both cores.

**Risk.** `QUICK`, `STANDARD`, or `STRICT` for code and hybrid work, derived from properties rather than keywords — reversibility, blast radius, privilege boundary, persistence, contract surface, environment, failure cost, and uncertainty.

## Unattended work

Unattended work reports one of `WORKING`, `WAITING_INPUT`, `WAITING_PRIVILEGE`, `BLOCKED`, `ERROR`, or `DONE`. A live process is not `WORKING`, a terminated process is not `DONE`, and `DONE` requires a completion verification record. Handoffs use a `WORK_PACKAGE` and an `EVIDENCE_PACKAGE` between role-based `PLANNER`, `IMPLEMENTER`, `REVIEWER`, and `ESCALATION_REVIEWER` assignments.

## What 2.1.0 does not claim, and what the evaluation found

An effectiveness evaluation has been conducted — one model, six author-labelled fixtures, two repetitions per condition, in three separate tracks. It does not support enabling HSP-v2 by default.

| Core | Status after the evaluation |
|---|---|
| Research core | `EXPERIMENTAL_ONLY` — the difference over control appeared on one fixture and one repetition and did not reproduce |
| Engineering core, single-response contract | `REJECT_CURRENT_DESIGN` — the one-shot work/evidence contract was not produced correctly |
| Engineering core, tool-use form | `EXPERIMENTAL_ONLY` — verification claims were grounded in real tool evidence, but the advantage was narrow and cost more |

**Default policy: `OFF`.** Enable it selectively where external evidence decides the answer. This release describes function, not measured effect: no coding-quality improvement, defect reduction, token saving, or research-quality improvement is claimed. See the [effectiveness and operating policy](https://github.com/icerain-cmd/humanities-superpowers/blob/main/docs/evaluation/EFFECTIVENESS_AND_OPERATING_POLICY.md), the [comparison harness](https://github.com/icerain-cmd/humanities-superpowers/blob/main/docs/evaluation/HSP_COMPARISON_HARNESS.md), the [tool-use benchmark](https://github.com/icerain-cmd/humanities-superpowers/blob/main/docs/evaluation/TOOL_USE_BENCHMARK.md), and the [v2.1.0 release notes](https://github.com/icerain-cmd/humanities-superpowers/blob/main/docs/release/RELEASE_NOTES_v2.1.0.md).

Installation is unchanged in shape: see the [Installation Guide](installation.md). The [Fricturn 2.0](fricturn.md) research contract remains exactly as published.
