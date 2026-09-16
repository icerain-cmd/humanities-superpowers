# Effectiveness evaluation and operating policy

**Status: an effectiveness evaluation has been conducted. This document records
what was measured, what it does and does not support, and the resulting default
policy.**

The evaluation was run on 2026-09-16 with the repository's own comparison
harnesses. Three tracks were measured, each with one model
(`deepseek/deepseek-v4-flash`), temperature 0, six author-labelled cases, and
two repetitions per condition:

| Track | Condition A | Condition B | Tools |
|---|---|---|---|
| A — research | `CONTROL` | `HSP` | none |
| B — coding | `CONTROL_CODING` | `ENGINEERING_CORE` | none |
| C — tool use | `CONTROL_TOOL` | `HSP_TOOL` | file read, command run, source lookup |

## Required public conclusion

Effectiveness evaluation has been conducted. Current evidence does not support
enabling HSP-v2 by default. The research core showed limited and unstable gains
over control. In tool-use evaluation, verification claims were grounded in
actual tool evidence, but the observed advantage over control was narrow and
incurred additional token and latency cost. HSP-v2 therefore remains
experimental and selectively applicable.

### Product status

| Core | Status | What the status means |
|---|---|---|
| Research core | `EXPERIMENTAL_ONLY` | The measured difference appears on one fixture and one repetition, does not reproduce, and costs the same as the control |
| Engineering core, single-response contract | `REJECT_CURRENT_DESIGN` | The one-shot `WORK_PACKAGE`/`EVIDENCE_PACKAGE` contract is not produced correctly and invites unfounded verification narration |
| Engineering core, tool-use form | `EXPERIMENTAL_ONLY` | Grounded verification behaviour is sound in both conditions; the advantage is narrow and costs more |

## Default policy

**Default: `OFF`.**

Enable it selectively, for work where external evidence decides the answer:

- citation and source verification;
- file, configuration, or artifact verification;
- test-execution verification;
- work where deciding to withhold a conclusion when evidence is missing matters
  more than producing a conclusion.

Not justified as a default:

- general writing;
- general coding;
- simple questions;
- work where evidence verification is not the point.

When it is enabled, expect additional tokens and latency in tool-using work:
the measured tool-use comparison cost roughly a quarter more tokens and a third
more wall-clock time than the control.

## Evidence before claim

This is a design principle of the project, not a claim about outcomes.

A response may use *verified*, *tested*, *confirmed*, *passed*, *reproduced*,
*validated*, or *checked* only when evidence for that specific statement exists.
Evidence means a tool call, an executed command, an exit code, test output, a
source result, or an inspected artifact — something that was actually produced.
Inference is not evidence.

When evidence is missing, incomplete, or unobtainable, the response must say so
using the vocabulary below instead of a conclusion.

| Status | Meaning |
|---|---|
| `SUPPORTED` | the evidence that was produced supports the claim |
| `REFUTED` | the evidence that was produced contradicts the claim |
| `UNVERIFIED` | no check was run, or the check was not sufficient |
| `INSUFFICIENT_EVIDENCE` | a check ran but produced neither support nor refutation |
| `TOOL_FAILURE` | the tool needed for the check failed |

**A missing record is not a refutation.** A lookup that returns nothing, a file
that is not in the workspace, or an empty catalogue supports
`INSUFFICIENT_EVIDENCE` or `UNVERIFIED`; it does not support `REFUTED`. This
distinction is enforced by the tool-use harness.

## Benchmark status

Two different things are called "the benchmark". They are not comparable.

### HISTORICAL / NON-REPRODUCIBLE BENCHMARK

An earlier comparison reported roughly 4.8M control tokens against 9.2M
framework tokens (+90.3%) and a blind quality score moving from 22.33 to 19.67
out of 25. Its raw runs, prompt corpus, model parameters, and token accounting
are not preserved anywhere in this repository or on the research share. Nothing
here confirms it, reproduces it, or disproves it, and it must not be merged with
the numbers below.

### CURRENT HARNESS BENCHMARK

Measured on 2026-09-16 with the harnesses in this repository. Research track,
`n = 12` per condition:

| Metric | `CONTROL` | `HSP-v1` (archived tag v1.0.1) | `HSP-v2` |
|---|---:|---:|---:|
| defect recall | 0.750 | 0.500 | 0.8125 |
| false positives | 1 | 0 | 0 |
| false blocks | 0 | 0 | 0 |
| total tokens | 7,996 | 9,451 (+18.2%) | 7,999 (+0.04%) |
| wall clock | 129.5 s | 108.7 s | 84.0 s |
| blind quality (out of 25) | 13.92 | 13.50 | 16.17 |

The `HSP-v1` column is the routing text of the archived tag `v1.0.1`
(`b709e0a`) measured under the current harness. It is a reconstruction of a
configuration, not a reproduction of the historical benchmark above.

Stability, which is the reason the research core stays experimental:

- the `HSP-v2` advantage over `CONTROL` appears in one repetition out of two,
  and only on one fixture type (`T5`, bounded invalidation);
- excluding that fixture, `CONTROL` and `HSP-v2` score identically (12/12);
- the token difference changes sign between repetitions (−26% / +65%);
- the blind quality ordering changes sign depending on whether responses are
  judged pairwise or one at a time, so it is not a usable discriminator at this
  sample size.

Tool-use track, `n = 12` per condition:

| Metric | `CONTROL_TOOL` | `HSP_TOOL` |
|---|---:|---:|
| observation claims with executed evidence | 11 / 11 | 11 / 11 |
| unfounded verification claims | 0 | 0 |
| status accuracy | 0.727 | 0.917 |
| missing record treated as refutation | 2 | 1 |
| total tokens | 94,292 | 116,352 (+23.4%) |
| wall clock | 308.0 s | 408.0 s (+32%) |

The tool-use result is the one positive finding, and it is narrow: when tools
were available, neither condition narrated verification it had not performed,
and the framework condition was more likely to withhold a conclusion when the
evidence was absent. It paid roughly a quarter more tokens for that.

## What this evaluation does not establish

- It does not establish a general research benefit, a coding benefit, or a
  token economy in either direction.
- It does not establish that one condition is better. Six author-labelled
  fixtures with two repetitions cannot support that claim.
- It does not measure tool-using agent harnesses as they are actually used: the
  tool-use track runs a fixed tool loop, not a full Codex or Claude Code
  session.
- It does not validate the historical benchmark above, and it is not evidence
  that the historical benchmark was mistaken.

## Reproducing the evaluation

```bash
# research track (CONTROL vs HSP; add --conditions HSP_V1 for the v1 condition)
python3 scripts/hsp_eval.py plan
python3 scripts/hsp_eval.py score recorded-runs.jsonl

# coding track
python3 scripts/hsp_eval_coding.py plan
python3 scripts/hsp_eval_coding.py score recorded-runs.jsonl

# tool-use track
python3 scripts/hsp_eval_tools.py self-test
python3 scripts/hsp_eval_tools.py run runs.jsonl        # needs OPENROUTER_API_KEY
python3 scripts/hsp_eval_tools.py score runs.jsonl
```

Each harness separates `plan`, `run`, and `score`, reports anything the record
does not contain as `NOT_MEASURED`, and keeps the research, coding, and
tool-use tracks apart on purpose.
