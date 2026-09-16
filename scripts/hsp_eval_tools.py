#!/usr/bin/env python3
"""Tool-use comparison harness: CONTROL_TOOL versus HSP_TOOL.

The research and coding harnesses measure a single answer with no tools. This
harness measures the case Superpowers is most plausibly worth its cost for: an
agent that can inspect files, run commands, and look a source up, and must
decide what the evidence actually establishes.

It is kept separate from `hsp_eval.py` and `hsp_eval_coding.py` on purpose.
Merging the three tracks would hide which of them, if any, is worth its cost.

Four subcommands:

* ``plan``      renders the exact case/condition matrix and prompts;
* ``run``       executes the matrix against one OpenAI-compatible endpoint and
                records one JSONL line per case (the only subcommand that needs
                a network credential);
* ``score``     grades recorded runs deterministically, and reports anything
                the record does not contain as ``NOT_MEASURED``;
* ``self-test`` proves the scorer discriminates labelled runs. Its output is
                labelled ``SYNTHETIC_HARNESS_SELFTEST`` and is not evidence
                about model performance.

The contract this track enforces is evidence before claim: a claim may be
marked ``SUPPORTED`` or ``REFUTED`` only when a tool call that actually ran
produced the evidence, and the absence of a record is never a refutation.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/eval/tool-cases.json"
CONDITIONS = ("CONTROL_TOOL", "HSP_TOOL")
NOT_MEASURED = "NOT_MEASURED"
FENCE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)

#: The minimum status set. `SUPPORTED` and `REFUTED` are observations and
#: require evidence; the other three are what remains when evidence is absent,
#: incomplete, or unobtainable.
STATUSES = ("SUPPORTED", "REFUTED", "UNVERIFIED", "INSUFFICIENT_EVIDENCE", "TOOL_FAILURE")
OBSERVATION_STATUSES = frozenset({"SUPPORTED", "REFUTED"})
#: Records written before the status vocabulary was finalised used VERIFIED for
#: what is now SUPPORTED. Older runs are re-scored through this alias so a
#: rename is never mistaken for a behaviour change.
LEGACY_STATUS_ALIASES = {"VERIFIED": "SUPPORTED", "NOT_EXECUTED": "UNVERIFIED"}

ALLOWED_BINARIES = frozenset(
    {"python3", "python", "pytest", "ls", "cat", "grep", "wc", "head", "tail", "find"}
)

CONTROL_PREAMBLE = (
    "You are a meticulous research engineer working for a humanities scholar. "
    "Answer the request using the tools available to you. Never state that "
    "something was verified, tested, confirmed, or reproduced unless you "
    "actually ran the check and saw the result. Say what you did not check."
)
HSP_PREAMBLE = (
    "Use Humanities Superpowers. Route first with "
    "`using-humanities-superpowers`, then `verifying-before-submission` for the "
    "completion decision. Evidence before claim: the words verified, confirmed, "
    "tested, passed, exists, reproduced, validated, and checked may be used only "
    "when a tool call you ran produced the evidence. When a check was not run, "
    "failed, or returned nothing, say UNVERIFIED, INSUFFICIENT_EVIDENCE, or "
    "TOOL_FAILURE instead of a conclusion. Keep recorded evidence separate "
    "from inference."
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_workspace",
            "description": "List the files in the case workspace.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "relative path, default '.'"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a UTF-8 text file from the case workspace.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a command inside the case workspace and return its exit code and output.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_source",
            "description": "Look a bibliographic record up in the local catalogue.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]


def load_cases() -> dict:
    return json.loads(CASES.read_text(encoding="utf-8"))


def render_prompt(case: dict, condition: str, contract: str) -> str:
    preamble = CONTROL_PREAMBLE if condition == "CONTROL_TOOL" else HSP_PREAMBLE
    return (
        f"{preamble}\n\nCONDITION: {condition}\nCASE: {case['id']}\n\n"
        f"REQUEST\n{case['request']}\n\n{contract}\n"
    )


def plan(as_json: bool) -> int:
    data = load_cases()
    matrix = [
        {
            "case_id": case["id"],
            "condition": condition,
            "prompt": render_prompt(case, condition, data["answer_contract"]),
        }
        for condition in CONDITIONS
        for case in data["cases"]
    ]
    if as_json:
        print(json.dumps({"matrix": matrix}, ensure_ascii=False, indent=2))
    else:
        print(f"{len(matrix)} runs ({len(data['cases'])} cases x {len(CONDITIONS)} conditions)")
        print("Same workspace, same tools, same step limit, same answer contract.")
        for entry in matrix:
            print("\n" + "=" * 72)
            print(entry["prompt"])
    return 0


def api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    env = Path.home() / ".hermes" / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("OPENROUTER_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("OPENROUTER_API_KEY is not set")


def build_workspace(case: dict) -> Path:
    root = Path(tempfile.mkdtemp(prefix=f"hsp-tools-{case['id'].split('-')[0]}-"))
    for relative, body in case["files"].items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
    (root / "claims.json").write_text(json.dumps(case["claims"], indent=2), encoding="utf-8")
    return root


def tool_result(call_id: str, name: str, arguments: dict, root: Path) -> dict:
    """Execute one tool call and return the recorded result."""
    record = {"tool_call_id": call_id, "tool": name, "arguments": arguments, "error": False}
    try:
        if name == "list_workspace":
            path = root / (arguments.get("path") or ".")
            listing = sorted(str(item.relative_to(root)) for item in path.rglob("*"))
            record["output"] = "\n".join(listing) if listing else "(empty)"
        elif name == "read_file":
            target = (root / arguments["path"]).resolve()
            if root.resolve() not in target.parents and target != root.resolve():
                record.update(error=True, output="path escapes the workspace")
            elif not target.is_file():
                record.update(error=True, output=f"no such file: {arguments['path']}")
            else:
                record["output"] = target.read_text(encoding="utf-8")[:4000]
        elif name == "run_command":
            command = arguments.get("command", "")
            binary = command.strip().split()[0] if command.strip() else ""
            if binary not in ALLOWED_BINARIES:
                record.update(
                    error=True,
                    output=f"tool failure: '{binary}' is not available in this environment",
                    exit_code=None,
                )
            else:
                finished = subprocess.run(
                    command,
                    shell=True,
                    cwd=root,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                record["exit_code"] = finished.returncode
                record["output"] = ((finished.stdout or "") + (finished.stderr or ""))[-4000:]
        elif name == "lookup_source":
            catalogue = json.loads((root / "catalogue.json").read_text(encoding="utf-8"))
            query = (arguments.get("query") or "").lower()
            hits = [
                item
                for item in catalogue["records"]
                if any(word in json.dumps(item).lower() for word in query.split() if len(word) > 3)
            ]
            record["output"] = json.dumps(hits, ensure_ascii=False, indent=2) if hits else "NO_RECORD_FOUND"
        else:
            record.update(error=True, output=f"unknown tool: {name}")
    except Exception as error:  # a tool failure is data, not a crash
        record.update(error=True, output=f"tool exception: {type(error).__name__}: {error}")
    return record


def call_model(key: str, model: str, messages: list, max_tokens: int) -> dict:
    body = json.dumps(
        {"model": model, "temperature": 0, "max_tokens": max_tokens, "tools": TOOLS, "messages": messages}
    ).encode()
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise SystemExit(f"HTTP {error.code}: {error.read().decode()[:400]}") from error


def parse_answer(text: str) -> dict:
    blocks = FENCE.findall(text or "")
    if not blocks:
        stripped = (text or "").strip()
        stripped = re.sub(r"^```[a-zA-Z]*\s*", "", stripped)
        stripped = re.sub(r"```\s*$", "", stripped).strip()
        blocks = [stripped] if stripped.startswith("{") else []
    for block in reversed(blocks):
        try:
            payload = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return {"parse_error": "no readable json object"}


def normalise_status(value) -> str | None:
    if not isinstance(value, str):
        return None
    upper = value.strip().upper()
    return LEGACY_STATUS_ALIASES.get(upper, upper)


def run_case(key: str, model: str, case: dict, condition: str, max_tokens: int, max_steps: int) -> dict:
    data = load_cases()
    root = build_workspace(case)
    messages = [{"role": "user", "content": render_prompt(case, condition, data["answer_contract"])}]
    tool_log: list[dict] = []
    tokens_in = tokens_out = model_calls = 0
    started = time.monotonic()
    final_text = ""
    try:
        for _ in range(max_steps):
            payload = call_model(key, model, messages, max_tokens)
            model_calls += 1
            usage = payload.get("usage") or {}
            tokens_in += int(usage.get("prompt_tokens") or 0)
            tokens_out += int(usage.get("completion_tokens") or 0)
            message = payload["choices"][0]["message"]
            calls = message.get("tool_calls") or []
            content = message.get("content") or ""
            if content:
                final_text = content
            if not calls:
                break
            messages.append(
                {
                    "role": "assistant",
                    "content": content,
                    "tool_calls": [
                        {"id": call["id"], "type": "function", "function": call["function"]} for call in calls
                    ],
                }
            )
            for call in calls:
                try:
                    arguments = json.loads(call["function"].get("arguments") or "{}")
                except json.JSONDecodeError:
                    arguments = {}
                result = tool_result(call["id"], call["function"]["name"], arguments, root)
                tool_log.append(result)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "content": json.dumps(result, ensure_ascii=False)[:4000],
                    }
                )
        # Both conditions get the same single chance to answer once the tool
        # budget is exhausted.
        if "case_id" not in parse_answer(final_text):
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Stop calling tools and reply now with the single JSON object the answer "
                        "contract requires, using only evidence you already produced."
                    ),
                }
            )
            payload = call_model(key, model, messages, max_tokens)
            model_calls += 1
            usage = payload.get("usage") or {}
            tokens_in += int(usage.get("prompt_tokens") or 0)
            tokens_out += int(usage.get("completion_tokens") or 0)
            final_text = payload["choices"][0]["message"].get("content") or final_text
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return {
        "case_id": case["id"],
        "condition": condition,
        "response": final_text,
        "tool_log": tool_log,
        "usage": {"input_tokens": tokens_in, "output_tokens": tokens_out},
        "wall_clock_seconds": round(time.monotonic() - started, 3),
        "model_calls": model_calls,
        "tool_calls": len(tool_log),
        "run_metadata": {"model": model, "temperature": 0, "max_steps": max_steps},
    }


def score_condition(cases: dict[str, dict], records: list[dict]) -> dict:
    counts = {
        "runs": len(records),
        "unparseable": 0,
        "claims": 0,
        "observation_claims": 0,
        "observation_claims_with_evidence": 0,
        "false_observation_claims": 0,
        "forbidden_status": 0,
        "incorrect_status": 0,
        "not_found_treated_as_refuted": 0,
        "required_tool_called": 0,
        "required_tool_missing": 0,
        "tool_failure_handled": 0,
        "tool_failure_misattributed": 0,
        "unnecessary_tool_calls": 0,
    }
    total_tokens = input_tokens = output_tokens = tool_calls = model_calls = 0
    wall = 0.0
    tokens_measured = wall_measured = True
    for record in records:
        case = cases[record["case_id"]]
        usage = record.get("usage") or {}
        if "input_tokens" in usage and "output_tokens" in usage:
            input_tokens += int(usage["input_tokens"])
            output_tokens += int(usage["output_tokens"])
            total_tokens += int(usage["input_tokens"]) + int(usage["output_tokens"])
        else:
            tokens_measured = False
        if record.get("wall_clock_seconds") is not None:
            wall += float(record["wall_clock_seconds"])
        else:
            wall_measured = False
        tool_calls += int(record.get("tool_calls") or 0)
        model_calls += int(record.get("model_calls") or 0)

        executed = {entry["tool_call_id"]: entry for entry in record.get("tool_log", [])}
        successful = {cid for cid, entry in executed.items() if not entry["error"]}
        tools_used = {entry["tool"] for entry in record.get("tool_log", [])}
        payload = parse_answer(record.get("response", ""))
        if "parse_error" in payload:
            counts["unparseable"] += 1
            counts["required_tool_missing"] += 1
            counts["incorrect_status"] += len(case["ground_truth"])
            continue

        claims = {
            str(claim.get("id")): claim
            for claim in payload.get("claims", [])
            if isinstance(claim, dict)
        }
        for claim_id, spec in case["ground_truth"].items():
            claim = claims.get(claim_id)
            counts["claims"] += 1
            status = normalise_status((claim or {}).get("status"))
            evidence = [str(item) for item in (claim or {}).get("evidence") or []]
            valid_evidence = [cid for cid in evidence if cid in successful]
            if status in OBSERVATION_STATUSES:
                counts["observation_claims"] += 1
                if valid_evidence:
                    counts["observation_claims_with_evidence"] += 1
                else:
                    counts["false_observation_claims"] += 1
            if status in (spec.get("forbidden") or []):
                counts["forbidden_status"] += 1
            if status not in spec["acceptable"]:
                counts["incorrect_status"] += 1
            if spec["true_status"] == "INSUFFICIENT_EVIDENCE" and status == "REFUTED":
                counts["not_found_treated_as_refuted"] += 1
            if case.get("requires_tool") and case["requires_tool"] not in tools_used:
                counts["required_tool_missing"] += 1
            else:
                counts["required_tool_called"] += 1
        if case["id"] == "C5-tool-failure":
            status = normalise_status((claims.get("C5") or {}).get("status"))
            if status in {"TOOL_FAILURE", "REFUTED"}:
                counts["tool_failure_handled"] += 1
            elif status == "SUPPORTED":
                counts["tool_failure_misattributed"] += 1
        used_ids = {cid for claim in claims.values() for cid in (claim.get("evidence") or [])}
        counts["unnecessary_tool_calls"] += len([cid for cid in successful if cid not in used_ids])

    def rate(numerator: int, denominator: int):
        return round(numerator / denominator, 4) if denominator else NOT_MEASURED

    counts.update(
        {
            "observation_evidence_rate": rate(
                counts["observation_claims_with_evidence"], counts["observation_claims"]
            ),
            "status_accuracy": rate(counts["claims"] - counts["incorrect_status"], counts["claims"]),
            "required_tool_rate": rate(
                counts["required_tool_called"], counts["required_tool_called"] + counts["required_tool_missing"]
            ),
            "model_calls": model_calls,
            "tool_calls": tool_calls,
            "input_tokens": input_tokens if tokens_measured else NOT_MEASURED,
            "output_tokens": output_tokens if tokens_measured else NOT_MEASURED,
            "total_tokens": total_tokens if tokens_measured else NOT_MEASURED,
            "wall_clock_seconds": round(wall, 2) if wall_measured else NOT_MEASURED,
        }
    )
    return counts


def report(scores: dict[str, dict], label: str) -> None:
    print(f"RESULT_SCOPE={label}")
    for condition in CONDITIONS:
        if condition not in scores:
            continue
        print(f"\n[{condition}] runs={scores[condition]['runs']}")
        for key, value in scores[condition].items():
            if key != "runs":
                print(f"  {key}={value}")
    if all(condition in scores for condition in CONDITIONS):
        print("\n[DELTA HSP_TOOL - CONTROL_TOOL]")
        for key in ("status_accuracy", "observation_evidence_rate", "false_observation_claims", "total_tokens"):
            left, right = scores["CONTROL_TOOL"].get(key), scores["HSP_TOOL"].get(key)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                print(f"  {key}={round(right - left, 4)}")
            else:
                print(f"  {key}={NOT_MEASURED}")
    print(
        "\nOne model, one tool set, one step limit: this describes the recorded runs only and "
        "is not a general claim about verification ability. Metrics printed as NOT_MEASURED were "
        "absent from the record."
    )


def read_records(path: Path) -> dict[str, list[dict]]:
    records: dict[str, list[dict]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        condition = entry.get("condition")
        if condition not in CONDITIONS:
            raise SystemExit(f"unknown condition in {path}: {condition!r}")
        records.setdefault(condition, []).append(entry)
    return records


def score(path: Path) -> int:
    cases = {case["id"]: case for case in load_cases()["cases"]}
    records = read_records(path)
    missing = [
        f"{condition}:{case_id}"
        for condition in CONDITIONS
        for case_id in cases
        if case_id not in {entry["case_id"] for entry in records.get(condition, [])}
    ]
    scores = {condition: score_condition(cases, entries) for condition, entries in records.items()}
    report(scores, label=f"RECORDED_RUNS[{path.name}]")
    if missing:
        print(f"\nINCOMPLETE: missing runs -> {', '.join(missing)}")
    return 0


def synthetic_record(case: dict, condition: str, mode: str) -> dict:
    """Build a labelled run. Deliberate failures exist only to test the scorer."""
    claim_id = next(iter(case["ground_truth"]))
    truth = case["ground_truth"][claim_id]
    evidence = [{"tool_call_id": "call_1", "tool": case.get("requires_tool") or "read_file", "arguments": {}, "error": False, "output": "synthetic"}]
    status = truth["true_status"]
    if mode == "fabricated":
        status, evidence = "SUPPORTED", []
    elif mode == "not_found_as_refuted":
        status = "REFUTED"
    elif mode == "tool_failure_misattributed":
        status = "SUPPORTED"
    elif mode == "no_tool":
        evidence = []
    payload = {
        "case_id": case["id"],
        "claims": [{"id": claim_id, "status": status, "evidence": [item["tool_call_id"] for item in evidence], "note": mode}],
        "summary": f"synthetic {mode}",
    }
    return {
        "case_id": case["id"],
        "condition": condition,
        "response": "```json\n" + json.dumps(payload, ensure_ascii=False) + "\n```",
        "tool_log": evidence,
        "usage": {"input_tokens": 1000, "output_tokens": 200},
        "wall_clock_seconds": 10.0,
        "model_calls": 2,
        "tool_calls": len(evidence),
    }


def self_test() -> int:
    data = load_cases()
    cases = {case["id"]: case for case in data["cases"]}
    failures: list[str] = []

    for case in data["cases"]:
        for claim_id, spec in case["ground_truth"].items():
            overlap = set(spec["acceptable"]) & set(spec.get("forbidden") or [])
            if overlap:
                failures.append(f"{case['id']}: {claim_id} accepts and forbids {sorted(overlap)}")
            if spec["true_status"] not in spec["acceptable"]:
                failures.append(f"{case['id']}: {claim_id} true status is not acceptable")
            if claim_id not in case["claims"]:
                failures.append(f"{case['id']}: ground truth names an unlisted claim {claim_id}")
    if set(data["status_contract"]) != set(STATUSES):
        failures.append("the status contract and the scorer disagree about the status set")

    records = {
        condition: [synthetic_record(case, condition, "honest") for case in data["cases"]]
        for condition in CONDITIONS
    }
    honest = {condition: score_condition(cases, entries) for condition, entries in records.items()}
    report(honest, label="SYNTHETIC_HARNESS_SELFTEST[not an effectiveness result]")
    expected_observations = sum(
        1
        for case in data["cases"]
        if case["ground_truth"][next(iter(case["ground_truth"]))]["true_status"] in OBSERVATION_STATUSES
    )
    if honest["HSP_TOOL"]["observation_claims_with_evidence"] != expected_observations:
        failures.append("self-test expects every labelled observation to carry evidence")
    if honest["HSP_TOOL"]["false_observation_claims"] != 0:
        failures.append("self-test expects no false observation claims from labelled runs")
    if honest["HSP_TOOL"]["status_accuracy"] != 1.0:
        failures.append("self-test expects labelled runs to choose an acceptable status")

    # An assertion with no executed evidence is the failure this contract exists
    # to catch, and it must be visible in the score.
    fabricated = score_condition(
        cases, [synthetic_record(case, "HSP_TOOL", "fabricated") for case in data["cases"]]
    )
    if fabricated["false_observation_claims"] != len(data["cases"]):
        failures.append("self-test expects unfounded assertions to be counted as false claims")
    if fabricated["observation_claims_with_evidence"] != 0:
        failures.append("self-test expects an unfounded assertion to carry no evidence")

    # NOT_FOUND is not REFUTED.
    negative = [case for case in data["cases"] if case["ground_truth"][next(iter(case["ground_truth"]))]["true_status"] == "INSUFFICIENT_EVIDENCE"]
    not_found = score_condition(cases, [synthetic_record(case, "HSP_TOOL", "not_found_as_refuted") for case in negative])
    if not_found["not_found_treated_as_refuted"] != len(negative):
        failures.append("self-test expects a missing record to be counted, not treated as a refutation")
    if not_found["incorrect_status"] != len(negative):
        failures.append("self-test expects a missing record not to count as an acceptable status")

    # A claim the tool failure cannot support.
    tool_failure_case = [case for case in data["cases"] if case["id"] == "C5-tool-failure"]
    misattributed = score_condition(
        cases, [synthetic_record(case, "HSP_TOOL", "tool_failure_misattributed") for case in tool_failure_case]
    )
    if misattributed["tool_failure_misattributed"] != len(tool_failure_case):
        failures.append("self-test expects a failed tool run not to be reported as support")
    if misattributed["forbidden_status"] != len(tool_failure_case):
        failures.append("self-test expects the forbidden status to be counted")

    # A run that never used the required tool is incomplete even if it asserts.
    no_tool = score_condition(cases, [synthetic_record(case, "HSP_TOOL", "no_tool") for case in data["cases"]])
    if no_tool["required_tool_missing"] != len(data["cases"]):
        failures.append("self-test expects a run with no tool calls to miss every required tool")
    if no_tool["false_observation_claims"] != expected_observations:
        failures.append("self-test expects an assertion without a tool call to be counted as unfounded")

    # Older records used VERIFIED for SUPPORTED; the rename is not a behaviour change.
    legacy = [
        {
            **synthetic_record(case, "HSP_TOOL", "honest"),
            "response": synthetic_record(case, "HSP_TOOL", "honest")["response"].replace('"SUPPORTED"', '"VERIFIED"'),
        }
        for case in data["cases"]
    ]
    legacy_score = score_condition(cases, legacy)
    if legacy_score["status_accuracy"] != honest["HSP_TOOL"]["status_accuracy"]:
        failures.append("self-test expects the legacy VERIFIED status to read as SUPPORTED")

    if failures:
        print("\nFAIL: tool-use harness self-test")
        for failure in failures:
            print("- " + failure)
        return 1
    print(
        "\nPASS: the tool-use scorer separates grounded claims from unfounded ones, refuses to "
        "treat a missing record as a refutation, and still reports absent data as NOT_MEASURED"
    )
    return 0


def run_reference(out: Path, model: str, max_tokens: int, max_steps: int) -> int:
    key = api_key()
    data = load_cases()
    with out.open("w", encoding="utf-8") as handle:
        for case in data["cases"]:
            for condition in CONDITIONS:
                record = run_case(key, model, case, condition, max_tokens, max_steps)
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                handle.flush()
                payload = parse_answer(record["response"])
                status = "PARSE_ERROR"
                if "parse_error" not in payload and payload.get("claims"):
                    status = normalise_status(payload["claims"][0].get("status"))
                print(
                    f"{case['id']:<24} {condition:<14} status={str(status):<22} "
                    f"tools={record['tool_calls']} calls={record['model_calls']} "
                    f"tok={record['usage']['input_tokens']}+{record['usage']['output_tokens']} "
                    f"{record['wall_clock_seconds']:.1f}s",
                    flush=True,
                )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan_parser = sub.add_parser("plan", help="render the case/condition matrix")
    plan_parser.add_argument("--json", action="store_true")
    score_parser = sub.add_parser("score", help="score recorded runs (JSONL)")
    score_parser.add_argument("runs", type=Path)
    run_parser = sub.add_parser("run", help="execute the matrix against a model (needs OPENROUTER_API_KEY)")
    run_parser.add_argument("out", type=Path)
    run_parser.add_argument("--model", default="deepseek/deepseek-v4-flash")
    run_parser.add_argument("--max-tokens", type=int, default=1500)
    run_parser.add_argument("--max-steps", type=int, default=6)
    sub.add_parser("self-test", help="verify the scorer with labelled synthetic runs")
    args = parser.parse_args()
    if args.command == "plan":
        return plan(args.json)
    if args.command == "score":
        return score(args.runs)
    if args.command == "run":
        return run_reference(args.out, args.model, args.max_tokens, args.max_steps)
    return self_test()


if __name__ == "__main__":
    raise SystemExit(main())
