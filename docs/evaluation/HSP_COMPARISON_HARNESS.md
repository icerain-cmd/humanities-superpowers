# Controlled comparison harness: CONTROL versus HSP

**Status: the harness exists and has been run.** A controlled comparison was
recorded on 2026-09-16 with one model, six fixtures, and two repetitions per
condition. The measured result does not support enabling the framework by
default: the difference over the control appeared on one fixture and one
repetition, did not reproduce, and cost the same in tokens. The numbers, the
stability analysis, and the resulting operating policy are recorded in
[EFFECTIVENESS_AND_OPERATING_POLICY.md](EFFECTIVENESS_AND_OPERATING_POLICY.md).

Repository validation passes, and that says nothing about whether the framework
helps a scholar find more real defects. This harness exists so that claim can be
tested instead of assumed.

## What is compared

| Condition | What the model receives |
|---|---|
| `CONTROL` | One strong generic research instruction with the same materials and the same answer contract |
| `HSP` | The same task, preceded by the router and the smallest sufficient skill set (citation audit, argument planning, close reading, terminology consistency, submission verification) |

Both conditions receive identical material, identical allowed labels, and an
identical answer contract. The comparison requires the same model and the same
reasoning level in both conditions; a run that changes the model or the
reasoning level measures the model, not the framework.

## Task set

Fixtures live in [`tests/eval/cases.json`](../../tests/eval/cases.json).

| Case | Type | Measures |
|---|---|---|
| `T1-citation-existence` | citation existence | fabricated-citation and metadata-error detection, false positives on real references |
| `T2-claim-source-fit` | claim–source fit | accuracy across `SUPPORTS`, `QUALIFIES`, `CONTEXT_ONLY`, `CONTRADICTS`, `INSUFFICIENT` |
| `T3-rival-interpretation` | rival interpretation | whether both readings survive, or are collapsed into one |
| `T4-concept-drift` | concept drift | drift detection and false alarms on stable segments |
| `T5-new-evidence` | epistemic return | bounded invalidation (affected gates only) and return-versus-rollback classification |
| `T6-clean-case` | clean case | false blocks and unnecessary researcher interruptions on a set with no defect |

`T6` exists specifically to penalize a system that buys safety by failing
everything: a framework that raises avoidable friction on a clean case is
recorded as a cost, not as caution.

## How to run

```bash
# 1. Render the exact matrix to run (6 cases x 2 conditions).
python3 scripts/hsp_eval.py plan

# 2. Run each prompt in your agent harness with the same model and reasoning
#    level, then save one JSONL record per run:
#    {"case_id","condition","response","usage":{"input_tokens","output_tokens"},
#     "wall_clock_seconds","tool_calls","researcher_interruptions"}
python3 scripts/hsp_eval.py score responses.jsonl

# 3. Verify the scorer itself (synthetic labels, never an effectiveness result).
python3 scripts/hsp_eval.py self-test
```

`score` reports a metric only when the record contains the data for it.
Anything absent is printed as `NOT_MEASURED`; missing runs are listed as
`INCOMPLETE` rather than silently averaged.

## Metrics

| Metric | Definition |
|---|---|
| defect recall | share of ground-truth defect items labelled as any defect |
| defect recall (exact) | share labelled with the exact expected defect label |
| false-positive rate | share of non-defect items labelled as a defect |
| false-block rate | share of clean cases blocked by a flag, a defect label, or an unnecessary decision request |
| citation-fit accuracy | exact label agreement on `T2-claim-source-fit` |
| researcher-interruption over-requests | decision requests on cases whose ground truth says no decision is required |
| token overhead | `HSP.total_tokens - CONTROL.total_tokens` |
| time overhead | `HSP.wall_clock_seconds - CONTROL.wall_clock_seconds` |
| defects caught per additional 10k tokens | recall delta scaled by the extra tokens, only when both are measured |

## What this harness does not establish

- It does not establish that the framework improves real research outcomes.
  The fixture set is small, author-written, and labelled by the author.
- Ground-truth labels, especially which references are real, must be confirmed
  against a catalogue by the researcher before scores are interpreted.
- A single run per case is not a distribution. Repeated runs and inter-model
  comparison are out of scope for the current harness.
- Token and time accounting depend on the host harness reporting usage.
  When it does not, those metrics stay `NOT_MEASURED` by design.

## Reporting rule

A scored run may be described only as: what was measured, on which fixtures,
with which model and reasoning level, at which sample size, and what remained
unmeasured. Effectiveness claims that go beyond a recorded run are not
supported by this repository. With six fixtures and two repetitions, describe
differences as observed, unstable, or insufficient evidence — never as proven,
superior, or production ready.

For the dispatch form of this comparison — the mandatory unattended preflight
header, the unattended execution rules, and the separate coding track — see
[UNATTENDED_AB_WORK_ORDER.md](UNATTENDED_AB_WORK_ORDER.md).

For the tool-use comparison, which measures the same question when the agent can
actually inspect files, run commands, and look a source up, see
[TOOL_USE_BENCHMARK.md](TOOL_USE_BENCHMARK.md).
