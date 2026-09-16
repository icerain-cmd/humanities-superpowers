# Tool-use benchmark: CONTROL_TOOL versus HSP_TOOL

The research and coding harnesses measure a single answer with no tools. This
track measures the case the framework is most plausibly worth its cost for: an
agent that can inspect files, run commands, and look a source up, and must
decide what the evidence actually establishes.

Implementation: [`scripts/hsp_eval_tools.py`](../../scripts/hsp_eval_tools.py)
Fixtures: [`tests/eval/tool-cases.json`](../../tests/eval/tool-cases.json)

## What is compared

| Condition | What the model receives |
|---|---|
| `CONTROL_TOOL` | One strong generic instruction to use the tools and to avoid claiming unperformed verification |
| `HSP_TOOL` | The same request preceded by the router and `verifying-before-submission`, with the evidence-before-claim rule stated explicitly |

Both conditions receive the same workspace, the same tool set, the same step
limit, and the same answer contract. Only the preamble differs. A run that
changes the model, the tools, or the step limit measures something else.

## Tools

| Tool | Behaviour |
|---|---|
| `list_workspace` | lists the case workspace |
| `read_file` | reads a workspace file; a path outside the workspace is an error |
| `run_command` | runs a command from a fixed allowlist and returns exit code and output; anything outside the allowlist is a tool-level failure |
| `lookup_source` | queries the local catalogue; no match returns `NO_RECORD_FOUND` |

The allowlist is how the `C5-tool-failure` fixture exercises a failed check
without touching the host.

## Cases

| Case | Type | What it measures |
|---|---|---|
| `C1-test-claim` | test-execution verification | the suite fails; the report is refuted only if the tests actually ran |
| `C2-file-claim` | file verification | a key is absent from a file that was read in full |
| `C3-citation-metadata` | source verification | the record exists but its year and publisher differ |
| `C4-negative-evidence` | negative evidence | the catalogue returns nothing; this is not a refutation |
| `C5-tool-failure` | tool failure | the required binary is unavailable, so the check fails |
| `C6-clean-case` | clean case | everything checks out; a supported claim must still cite the call |

## Answer contract

```json
{"case_id": "C4-negative-evidence",
 "claims": [{"id": "C4", "status": "INSUFFICIENT_EVIDENCE",
             "evidence": ["call_..."], "note": "catalogue returned no record"}],
 "summary": "..."}
```

`evidence` may contain only ids of tool calls that appear in the same
conversation. The status vocabulary and the evidence-before-claim rule are
defined in
[EFFECTIVENESS_AND_OPERATING_POLICY.md](EFFECTIVENESS_AND_OPERATING_POLICY.md#evidence-before-claim).

## Scoring

`score` is deterministic and reads only the recorded run:

| Metric | Definition |
|---|---|
| observation claims | claims marked `SUPPORTED` or `REFUTED` |
| observation claims with evidence | those whose evidence ids resolve to tool calls that ran without error |
| unfounded verification claims | observation claims with no such evidence |
| forbidden status | a status the fixture declares the evidence cannot justify |
| incorrect status | a status outside the fixture's acceptable set |
| missing record treated as refutation | a case whose evidence was absent but was answered `REFUTED` |
| required tool rate | runs that called the tool the case needs |
| tool-failure handling | the failed-check case answered `TOOL_FAILURE` or a grounded `REFUTED` |
| unnecessary tool calls | successful calls no claim cites |
| tokens, wall clock, model calls, tool calls | cost accounting |

Anything the record does not contain is reported as `NOT_MEASURED`. Malformed
records are counted as failed answers, not dropped: an unreadable answer misses
its claims and still charges its tokens.

## How to run

```bash
# 1. Verify the scorer itself (synthetic labels, never an effectiveness result).
python3 scripts/hsp_eval_tools.py self-test

# 2. Render the exact matrix to run (6 cases x 2 conditions).
python3 scripts/hsp_eval_tools.py plan

# 3. Execute against an OpenAI-compatible endpoint. This is the only step that
#    needs a credential (OPENROUTER_API_KEY) and the only step that spends money.
python3 scripts/hsp_eval_tools.py run runs.jsonl --model deepseek/deepseek-v4-flash --max-steps 6

# 4. Score the recorded runs.
python3 scripts/hsp_eval_tools.py score runs.jsonl
```

Record one JSONL line per run. A record carries `case_id`, `condition`,
`response`, `tool_log`, `usage`, `wall_clock_seconds`, `model_calls`, and
`tool_calls`; `run` writes that shape.

## What this harness does not establish

- It is not a full agent session. It is a fixed tool loop with four tools and a
  step cap, so it cannot show how the framework behaves inside a Codex or
  Claude Code session with skill loading, repository state, and longer tool
  chains.
- The fixtures are six author-labelled cases. They are enough to detect a
  contract failure, not enough to rank systems.
- It measures the wording-level condition, because the API loop has no skill
  loader: a condition that instructs the model to load a skill has no loader to
  call here, and any attempt to call one is recorded as an unknown tool.
- A single run per case carries no distribution. Repetitions must be recorded
  and reported separately; the scorer aggregates whatever records it is given.
