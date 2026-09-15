#!/usr/bin/env python3
"""Controlled comparison harness: CONTROL versus HSP.

This harness does not measure research quality by itself. It defines a
reproducible comparison so that a human or an agent harness can run the same
task set twice -- once with a strong generic research instruction and once
with the Humanities Superpowers router plus the smallest sufficient skill set
-- and then score the recorded responses with deterministic rules.

Three things are deliberately separated:

* ``plan``      renders the exact task/condition matrix and prompts;
* ``score``     scores *recorded* responses against the fixtures and reports
                measured metrics, using ``NOT_MEASURED`` for anything the
                record does not contain;
* ``self-test`` checks the scorer itself with labelled synthetic responses.
                Its output is labelled ``SYNTHETIC_HARNESS_SELFTEST`` and is
                not evidence about research performance.

No result is ever fabricated: a metric is reported only when a response record
supplies the data, and every reported number carries the sample size.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/eval/cases.json"
CONDITIONS = ("CONTROL", "HSP")
NOT_MEASURED = "NOT_MEASURED"
JSON_BLOCK = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)

CONTROL_PREAMBLE = (
    "You are a meticulous research assistant working for a humanities scholar. "
    "Verify before asserting, prefer primary sources, preserve uncertainty, "
    "never invent sources or page numbers, and separate evidence you checked "
    "from evidence you did not. Keep any process record shorter than the answer."
)
HSP_PREAMBLE = (
    "Use Humanities Superpowers. Route first with `using-humanities-superpowers`, "
    "then load the smallest sufficient skill set: `auditing-citations` for "
    "citation existence and metadata, `planning-humanities-argument` for "
    "claim-source fit, `performing-close-reading` for rival interpretation, "
    "`checking-terminology-consistency` for concept drift, and "
    "`verifying-before-submission` for completion and return decisions. "
    "Preserve unresolved conflict instead of harmonizing it, never invent "
    "sources, keep recorded gate status separate from current validity, and "
    "record only the friction a material consequence requires."
)


def load_cases() -> dict:
    return json.loads(CASES.read_text(encoding="utf-8"))


def render_prompt(case: dict, condition: str, contract: str) -> str:
    preamble = CONTROL_PREAMBLE if condition == "CONTROL" else HSP_PREAMBLE
    labels = ", ".join(case["labels"])
    return (
        f"{preamble}\n\n"
        f"CONDITION: {condition}\n"
        f"CASE: {case['id']} ({case['type']})\n\n"
        f"MATERIAL\n{case['material']}\n\n"
        f"TASK\nLabel each item id listed in the material. Allowed labels: {labels}.\n"
        f"Set decision_required to true only when a human choice is genuinely required.\n\n"
        f"ANSWER CONTRACT\n{contract}\n"
    )


def plan(as_json: bool) -> int:
    data = load_cases()
    contract = data["answer_contract"]
    matrix = [
        {
            "case_id": case["id"],
            "type": case["type"],
            "condition": condition,
            "prompt": render_prompt(case, condition, contract),
        }
        for condition in CONDITIONS
        for case in data["cases"]
    ]
    if as_json:
        print(json.dumps({"matrix": matrix}, ensure_ascii=False, indent=2))
    else:
        print(f"{len(matrix)} runs ({len(data['cases'])} cases x {len(CONDITIONS)} conditions)")
        print("Same model, same reasoning level, same material, same answer contract.")
        for entry in matrix:
            print("\n" + "=" * 72)
            print(entry["prompt"])
    return 0


def parse_response(response: str) -> dict:
    blocks = JSON_BLOCK.findall(response or "")
    if not blocks:
        return {"parse_error": "no json block"}
    try:
        payload = json.loads(blocks[-1])
    except json.JSONDecodeError as exc:
        return {"parse_error": f"invalid json: {exc.msg}"}
    if not isinstance(payload, dict):
        return {"parse_error": "json block is not an object"}
    return payload


def score_condition(cases: dict[str, dict], records: list[dict]) -> dict:
    defect_items = 0
    detected = 0
    exact = 0
    non_defect_items = 0
    false_positives = 0
    fit_total = fit_correct = 0
    false_blocks = 0
    clean_cases = 0
    over_requests = 0
    unparseable = 0
    tokens_in = tokens_out = 0
    wall = 0.0
    tool_calls = 0
    tokens_measured = wall_measured = True

    for record in records:
        case = cases[record["case_id"]]
        defect_labels = set(case["defect_labels"])
        truth = {item["id"]: item["label"] for item in case["ground_truth"]}
        payload = parse_response(record.get("response", ""))
        if "parse_error" in payload:
            unparseable += 1
            detected += 0
            if case["type"] == "clean_case":
                clean_cases += 1
                false_blocks += 1
            continue
        predicted = {
            item.get("id"): item.get("label")
            for item in payload.get("items", [])
            if isinstance(item, dict)
        }
        flags = payload.get("flags") or []

        for item_id, expected in truth.items():
            got = predicted.get(item_id)
            if expected in defect_labels:
                defect_items += 1
                if got in defect_labels:
                    detected += 1
                if got == expected:
                    exact += 1
            else:
                non_defect_items += 1
                if got in defect_labels:
                    false_positives += 1
            if case["type"] == "claim_source_fit":
                fit_total += 1
                fit_correct += int(got == expected)

        if case["type"] == "clean_case":
            clean_cases += 1
            blocked = bool(flags) or payload.get("decision_required") is True
            blocked = blocked or any(label in defect_labels for label in predicted.values())
            false_blocks += int(blocked)
        if case.get("expected_decision_required") is False and payload.get("decision_required") is True:
            over_requests += 1

        usage = record.get("usage") or {}
        if "input_tokens" in usage and "output_tokens" in usage:
            tokens_in += int(usage["input_tokens"])
            tokens_out += int(usage["output_tokens"])
        else:
            tokens_measured = False
        if record.get("wall_clock_seconds") is not None:
            wall += float(record["wall_clock_seconds"])
        else:
            wall_measured = False
        tool_calls += int(record.get("tool_calls") or 0)

    def rate(numerator: int, denominator: int):
        return round(numerator / denominator, 4) if denominator else NOT_MEASURED

    return {
        "runs": len(records),
        "unparseable": unparseable,
        "defect_recall": rate(detected, defect_items),
        "defect_recall_exact": rate(exact, defect_items),
        "false_positive_rate": rate(false_positives, non_defect_items),
        "false_block_rate": rate(false_blocks, clean_cases),
        "citation_fit_accuracy": rate(fit_correct, fit_total),
        "researcher_interruption_over_requests": over_requests,
        "recorded_researcher_interruptions": sum(
            int(record.get("researcher_interruptions") or 0) for record in records
        )
        if any("researcher_interruptions" in record for record in records)
        else NOT_MEASURED,
        "tool_calls": tool_calls if any("tool_calls" in record for record in records) else NOT_MEASURED,
        "input_tokens": tokens_in if tokens_measured else NOT_MEASURED,
        "output_tokens": tokens_out if tokens_measured else NOT_MEASURED,
        "total_tokens": (tokens_in + tokens_out) if tokens_measured else NOT_MEASURED,
        "wall_clock_seconds": round(wall, 2) if wall_measured else NOT_MEASURED,
    }


def compare(scores: dict[str, dict]) -> dict:
    control, hsp = scores["CONTROL"], scores["HSP"]

    def delta(key: str):
        left, right = control.get(key), hsp.get(key)
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return round(right - left, 4)
        return NOT_MEASURED

    efficiency = NOT_MEASURED
    if isinstance(control["total_tokens"], int) and isinstance(hsp["total_tokens"], int):
        extra = hsp["total_tokens"] - control["total_tokens"]
        caught = None
        if isinstance(control["defect_recall"], float) and isinstance(hsp["defect_recall"], float):
            caught = (hsp["defect_recall"] - control["defect_recall"])
        if extra > 0 and caught is not None:
            efficiency = round(caught * 10000 / extra, 6)
    return {
        "token_overhead": delta("total_tokens"),
        "time_overhead": delta("wall_clock_seconds"),
        "researcher_interruption_delta": delta("researcher_interruption_over_requests"),
        "defect_recall_delta": delta("defect_recall"),
        "defects_caught_per_additional_10k_tokens": efficiency,
    }


def report(scores: dict[str, dict], label: str) -> None:
    print(f"RESULT_SCOPE={label}")
    for condition in CONDITIONS:
        metrics = scores[condition]
        print(f"\n[{condition}] runs={metrics['runs']}")
        for key in (
            "defect_recall",
            "defect_recall_exact",
            "false_positive_rate",
            "false_block_rate",
            "citation_fit_accuracy",
            "researcher_interruption_over_requests",
            "recorded_researcher_interruptions",
            "tool_calls",
            "input_tokens",
            "output_tokens",
            "total_tokens",
            "wall_clock_seconds",
            "unparseable",
        ):
            print(f"  {key}={metrics[key]}")
    print("\n[DELTA HSP - CONTROL]")
    for key, value in compare(scores).items():
        print(f"  {key}={value}")
    print(
        "\nA scored run describes the recorded responses only: one model, one "
        "reasoning level, one run per case. It is not a general claim about "
        "research quality, and any metric reported as NOT_MEASURED was absent "
        "from the response record."
    )


def read_records(path: Path) -> dict[str, list[dict]]:
    records: dict[str, list[dict]] = {condition: [] for condition in CONDITIONS}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        condition = entry.get("condition")
        if condition not in records:
            raise SystemExit(f"unknown condition in {path}: {condition!r}")
        records[condition].append(entry)
    return records


def score(path: Path) -> int:
    data = load_cases()
    cases = {case["id"]: case for case in data["cases"]}
    records = read_records(path)
    missing = [
        f"{condition}:{case_id}"
        for condition in CONDITIONS
        for case_id in cases
        if case_id not in {entry["case_id"] for entry in records[condition]}
    ]
    scores = {condition: score_condition(cases, records[condition]) for condition in CONDITIONS}
    report(scores, label=f"RECORDED_RESPONSES[{path.name}]")
    if missing:
        print(f"\nINCOMPLETE: missing runs -> {', '.join(missing)}")
    return 0


def synthetic(condition: str, case: dict) -> dict:
    """Build labelled synthetic responses. Deliberate defects exist only to test the scorer."""
    defect_labels = set(case["defect_labels"])
    benign = [label for label in case["labels"] if label not in defect_labels]
    missed = False
    items = []
    for item in case["ground_truth"]:
        label = item["label"]
        if condition == "CONTROL" and not missed and label in defect_labels:
            label = benign[0]
            missed = True
        items.append({"id": item["id"], "label": label})
    decision = bool(case.get("expected_decision_required", False))
    flags = []
    if condition == "CONTROL" and case["type"] == "clean_case":
        decision = True
        flags = ["unresolved verification"]
        items = [{"id": item["id"], "label": "DEFECT"} for item in case["ground_truth"]]
    return {"case_id": case["id"], "items": items, "decision_required": decision, "flags": flags}


def self_test() -> int:
    data = load_cases()
    cases = {case["id"]: case for case in data["cases"]}
    # Synthetic usage only: the condition preamble and skill loading cost more
    # input than the generic instruction. These numbers are labels for the
    # scorer test and are never reported as an effectiveness result.
    usage = {
        "CONTROL": {"input_tokens": 900, "output_tokens": 300},
        "HSP": {"input_tokens": 1400, "output_tokens": 320},
    }
    wall = {"CONTROL": 12.0, "HSP": 14.0}
    records = {
        condition: [
            {
                "case_id": case["id"],
                "condition": condition,
                "response": "```json\n" + json.dumps(synthetic(condition, case), ensure_ascii=False) + "\n```",
                "usage": usage[condition],
                "wall_clock_seconds": wall[condition],
                "tool_calls": 2,
                "researcher_interruptions": 0,
            }
            for case in data["cases"]
        ]
        for condition in CONDITIONS
    }
    scores = {condition: score_condition(cases, records[condition]) for condition in CONDITIONS}
    report(scores, label="SYNTHETIC_HARNESS_SELFTEST[not an effectiveness result]")
    control, hsp = scores["CONTROL"], scores["HSP"]
    failures = []
    if not isinstance(hsp["defect_recall"], float) or hsp["defect_recall"] != 1.0:
        failures.append("self-test expects the labelled HSP responses to catch every defect")
    if not isinstance(control["defect_recall"], float) or control["defect_recall"] >= 1.0:
        failures.append("self-test expects the labelled CONTROL responses to miss a defect")
    if control["false_block_rate"] in (NOT_MEASURED, 0):
        failures.append("self-test expects the labelled CONTROL responses to false-block the clean case")
    if hsp["false_block_rate"] != 0:
        failures.append("self-test expects the labelled HSP responses not to false-block")
    if hsp["citation_fit_accuracy"] != 1.0:
        failures.append("self-test expects exact claim-source labels from the labelled HSP responses")
    if not isinstance(compare(scores)["defects_caught_per_additional_10k_tokens"], float):
        failures.append("self-test expects token efficiency to be computable from supplied usage")
    if failures:
        print("\nFAIL: harness self-test")
        for failure in failures:
            print("- " + failure)
        return 1
    print("\nPASS: scorer distinguishes the labelled conditions and marks absent data NOT_MEASURED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan_parser = sub.add_parser("plan", help="render the task/condition matrix")
    plan_parser.add_argument("--json", action="store_true")
    score_parser = sub.add_parser("score", help="score recorded responses (JSONL)")
    score_parser.add_argument("responses", type=Path)
    sub.add_parser("self-test", help="verify the scorer with labelled synthetic responses")
    args = parser.parse_args()
    if args.command == "plan":
        return plan(args.json)
    if args.command == "score":
        return score(args.responses)
    return self_test()


if __name__ == "__main__":
    raise SystemExit(main())
