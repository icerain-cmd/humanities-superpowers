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

## What 2.1.0 does not claim

| Track | Comparison | Result |
|---|---|---|
| Research | `CONTROL` versus `HSP` | Research effectiveness: `NOT_MEASURED` |
| Coding | `CONTROL_CODING` versus `ENGINEERING_CORE` | Coding effectiveness: `NOT_MEASURED` |

Both harnesses exist and pass their own self-tests, but no comparison run has been recorded. This release describes function, not measured effect: no coding-quality improvement, defect reduction, token saving, or research-quality improvement is claimed. See the [comparison harness](https://github.com/icerain-cmd/humanities-superpowers/blob/main/docs/evaluation/HSP_COMPARISON_HARNESS.md) and the [v2.1.0 release notes](https://github.com/icerain-cmd/humanities-superpowers/blob/main/docs/release/RELEASE_NOTES_v2.1.0.md).

Installation is unchanged in shape: see the [Installation Guide](installation.md). The [Fricturn 2.0](fricturn.md) research contract remains exactly as published.
