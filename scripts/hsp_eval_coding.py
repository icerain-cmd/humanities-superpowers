#!/usr/bin/env python3
"""Coding comparison harness: CONTROL_CODING versus ENGINEERING_CORE.

Deliberately separate from `scripts/hsp_eval.py`, which measures the research
comparison. The two tracks answer different questions and must not be merged
into one score.

`plan` renders the matrix, `score` grades recorded runs, and `self-test` proves
the scorer discriminates labelled runs. Metrics that a record does not supply
are reported as NOT_MEASURED, never estimated.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/eval/coding-cases.json"
CONDITIONS = ("CONTROL_CODING", "ENGINEERING_CORE")
NOT_MEASURED = "NOT_MEASURED"
RISK_LEVELS = ("QUICK", "STANDARD", "STRICT")
WORKER_STATES = ("WORKING", "WAITING_INPUT", "WAITING_PRIVILEGE", "BLOCKED", "ERROR", "DONE")
JSON_BLOCK = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)
FORMAT_CHECKER = FormatChecker()

CONTROL_PREAMBLE = (
    "You are a careful senior engineer working alone. Make the smallest correct "
    "change, follow the existing conventions, run the tests that exist, and do "
    "not claim a result you did not observe. Keep any process notes shorter than "
    "the change itself."
)
ENGINEERING_PREAMBLE = (
    "Use the Engineering core of Humanities Superpowers. Classify the request "
    "semantically as QUICK, STANDARD, or STRICT from its properties "
    "(reversibility, blast radius, privilege boundary, persistence, contract "
    "surface, environment, failure cost, uncertainty) and follow that level's "
    "steps with the smallest sufficient skill route "
    "(`vendor/obra-superpowers/skills/`). Produce a WORK_PACKAGE for STANDARD and "
    "STRICT work and an EVIDENCE_PACKAGE for every level. Report a worker state, "
    "and never report DONE without completion verification. Escalate to "
    "WAITING_PRIVILEGE instead of waiting on an elevation prompt."
)


def load_cases() -> dict:
    return json.loads(CASES.read_text(encoding="utf-8"))


def render_prompt(case: dict, condition: str, contract: str) -> str:
    preamble = CONTROL_PREAMBLE if condition == "CONTROL_CODING" else ENGINEERING_PREAMBLE
    return (
        f"{preamble}\n\n"
        f"CONDITION: {condition}\n"
        f"CASE: {case['id']}\n\n"
        f"REQUEST\n{case['task']}\n\n"
        f"TASK\nDo the work, then report. Choose risk_level, and list in defects_found "
        f"only defects you actually confirmed.\n\n"
        f"ANSWER CONTRACT\n{contract}\n"
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
        print("Same model, same reasoning level, same repository state, same answer contract.")
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
    return payload if isinstance(payload, dict) else {"parse_error": "not an object"}


def contract_errors(payload: dict) -> list[str]:
    errors: list[str] = []
    for field, schema in (
        ("work_package", "work-package.schema.json"),
        ("evidence_package", "evidence-package.schema.json"),
    ):
        instance = payload.get(field)
        if not isinstance(instance, dict):
            continue
        schema_data = json.loads((ROOT / "schemas" / schema).read_text(encoding="utf-8"))
        errors.extend(
            issue.message
            for issue in Draft202012Validator(schema_data, format_checker=FORMAT_CHECKER).iter_errors(instance)
        )
    return errors


def score_condition(cases: dict[str, dict], records: list[dict]) -> dict:
    risk_total = risk_correct = 0
    defect_total = defect_found = defect_false = 0
    done_claims = unverified_done = invalid_contract = 0
    block_total = false_blocks = 0
    boundary_total = boundary_correct = 0
    unparseable = 0
    tokens_in = tokens_out = 0
    wall = 0.0
    tokens_measured = wall_measured = True

    for record in records:
        case = cases[record["case_id"]]
        payload = parse_response(record.get("response", ""))
        if "parse_error" in payload:
            unparseable += 1
            continue
        risk_total += 1
        risk_correct += int(payload.get("risk_level") == case["expected_risk"])
        truth = set(case["defects"])
        found = {item for item in (payload.get("defects_found") or []) if isinstance(item, str)}
        defect_total += len(truth)
        defect_found += len(truth & found)
        defect_false += len(found - truth)

        evidence = payload.get("evidence_package")
        if isinstance(evidence, dict):
            invalid_contract += len(contract_errors(payload))
            status = evidence.get("completion_status")
            if status == "DONE":
                done_claims += 1
                verified = bool(evidence.get("completion_verification")) and bool(
                    evidence.get("tests_run")
                ) and bool(evidence.get("test_results"))
                if not verified:
                    unverified_done += 1
        elif payload.get("worker_state") == "DONE":
            done_claims += 1
            unverified_done += 1

        if case["expect_no_block"]:
            block_total += 1
            blocked = payload.get("worker_state") in {"BLOCKED", "WAITING_INPUT"} or bool(
                payload.get("defects_found") and not truth
            )
            false_blocks += int(blocked)
        if case["expect_privilege_boundary"]:
            boundary_total += 1
            boundary_correct += int(payload.get("worker_state") == "WAITING_PRIVILEGE")

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

    def rate(numerator: int, denominator: int):
        return round(numerator / denominator, 4) if denominator else NOT_MEASURED

    return {
        "runs": len(records),
        "unparseable": unparseable,
        "risk_level_accuracy": rate(risk_correct, risk_total),
        "defect_detection_recall": rate(defect_found, defect_total),
        "defect_false_positive_count": defect_false,
        "completion_accuracy": rate(done_claims - unverified_done, done_claims),
        "unverified_done_claims": unverified_done,
        "false_block_rate": rate(false_blocks, block_total),
        "privilege_boundary_accuracy": rate(boundary_correct, boundary_total) if boundary_total else NOT_MEASURED,
        "invalid_contract_artifacts": invalid_contract,
        "total_tokens": (tokens_in + tokens_out) if tokens_measured else NOT_MEASURED,
        "wall_clock_seconds": round(wall, 2) if wall_measured else NOT_MEASURED,
        "recorded_researcher_interruptions": sum(
            int(record.get("researcher_interruptions") or 0) for record in records
        )
        if any("researcher_interruptions" in record for record in records)
        else NOT_MEASURED,
    }


def compare(scores: dict[str, dict]) -> dict:
    control, hsp = scores["CONTROL_CODING"], scores["ENGINEERING_CORE"]

    def delta(key: str):
        left, right = control.get(key), hsp.get(key)
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return round(right - left, 4)
        return NOT_MEASURED

    efficiency = NOT_MEASURED
    if isinstance(control["total_tokens"], int) and isinstance(hsp["total_tokens"], int):
        extra = hsp["total_tokens"] - control["total_tokens"]
        recall_delta = None
        if isinstance(control["defect_detection_recall"], float) and isinstance(
            hsp["defect_detection_recall"], float
        ):
            recall_delta = hsp["defect_detection_recall"] - control["defect_detection_recall"]
        if extra > 0 and recall_delta is not None:
            efficiency = round(recall_delta * 10000 / extra, 6)
    return {
        "token_overhead": delta("total_tokens"),
        "time_overhead": delta("wall_clock_seconds"),
        "risk_level_accuracy_delta": delta("risk_level_accuracy"),
        "defect_recall_delta": delta("defect_detection_recall"),
        "false_block_delta": delta("false_block_rate"),
        "unverified_done_delta": delta("unverified_done_claims"),
        "defects_caught_per_additional_10k_tokens": efficiency,
    }


def report(scores: dict[str, dict], label: str) -> None:
    print(f"RESULT_SCOPE={label}")
    for condition in CONDITIONS:
        print(f"\n[{condition}] runs={scores[condition]['runs']}")
        for key, value in scores[condition].items():
            if key != "runs":
                print(f"  {key}={value}")
    print("\n[DELTA ENGINEERING_CORE - CONTROL_CODING]")
    for key, value in compare(scores).items():
        print(f"  {key}={value}")
    print(
        "\nOne model, one reasoning level, one run per case: this describes the "
        "recorded runs only and is not a general claim about coding quality. "
        "Metrics printed as NOT_MEASURED were absent from the run record."
    )


def score(path: Path) -> int:
    data = load_cases()
    cases = {case["id"]: case for case in data["cases"]}
    records = {condition: [] for condition in CONDITIONS}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entry = json.loads(line)
            records[entry["condition"]].append(entry)
    scores = {condition: score_condition(cases, records[condition]) for condition in CONDITIONS}
    report(scores, label=f"RECORDED_RUNS[{path.name}]")
    missing = [
        f"{condition}:{case_id}"
        for condition in CONDITIONS
        for case_id in cases
        if case_id not in {entry["case_id"] for entry in records[condition]}
    ]
    if missing:
        print(f"\nINCOMPLETE: missing runs -> {', '.join(missing)}")
    return 0


def synthetic(condition: str, case: dict) -> dict:
    """Labelled synthetic runs. Deliberate errors exist only to test the scorer."""
    risk = case["expected_risk"]
    defects = list(case["defects"])
    state = "DONE"
    evidence = {
        "package_id": f"{case['id']}-evidence",
        "work_package_ref": f"{case['id']}-work",
        "files_changed": [{"path": "changed.py", "reason": "requested change"}],
        "tests_run": ["python3 -m pytest"],
        "test_results": ["all selected tests passed"],
        "unresolved": [],
        "deviations": [],
        "completion_status": "DONE",
        "completion_verification": "pytest output captured",
    }
    if condition == "CONTROL_CODING":
        if case["expected_risk"] == "STRICT":
            risk = "STANDARD"
        defects = list(case["defects"])[:1]
        if case["id"] == "C3-unknown-cause-bug":
            defects = []
        if case["id"] == "C6-clean-refactor":
            defects = ["REG-1"]
        if case["id"] == "C2-bounded-endpoint":
            evidence.pop("completion_verification")
            evidence["tests_run"] = []
            evidence["test_results"] = []
    if case["expect_privilege_boundary"] and condition == "ENGINEERING_CORE":
        state = "WAITING_PRIVILEGE"
        evidence["completion_status"] = "BLOCKED"
        evidence.pop("completion_verification")
    if case["expect_privilege_boundary"] and condition == "CONTROL_CODING":
        state = "DONE"
    payload = {
        "case_id": case["id"],
        "risk_level": risk,
        "work_package": {
            "package_id": f"{case['id']}-work",
            "objective": case["task"][:60],
            "scope": {"in_scope": ["the request"], "out_of_scope": ["everything else"]},
            "constraints": ["keep changes small"],
            "risk_level": risk,
            "risk_reason": "declared by the run",
            "acceptance_criteria": ["the request is satisfied"],
            "required_verification": ["run the tests"],
            "forbidden_actions": ["do not touch unrelated files"],
            "reviewer_role": "REVIEWER",
        }
        if risk in {"STANDARD", "STRICT"}
        else None,
        "evidence_package": evidence,
        "defects_found": defects,
        "worker_state": state,
        "notes": "synthetic",
    }
    return payload


def self_test() -> int:
    data = load_cases()
    cases = {case["id"]: case for case in data["cases"]}
    usage = {"CONTROL_CODING": {"input_tokens": 1200, "output_tokens": 500},
             "ENGINEERING_CORE": {"input_tokens": 1800, "output_tokens": 540}}
    wall = {"CONTROL_CODING": 90.0, "ENGINEERING_CORE": 110.0}
    records = {
        condition: [
            {
                "case_id": case["id"],
                "condition": condition,
                "response": "```json\n" + json.dumps(synthetic(condition, case), ensure_ascii=False) + "\n```",
                "usage": usage[condition],
                "wall_clock_seconds": wall[condition],
                "researcher_interruptions": 0,
            }
            for case in data["cases"]
        ]
        for condition in CONDITIONS
    }
    scores = {condition: score_condition(cases, records[condition]) for condition in CONDITIONS}
    report(scores, label="SYNTHETIC_HARNESS_SELFTEST[not an effectiveness result]")
    control, eng = scores["CONTROL_CODING"], scores["ENGINEERING_CORE"]
    failures = []
    if eng["risk_level_accuracy"] != 1.0:
        failures.append("self-test expects the labelled engineering runs to classify every case")
    if not isinstance(control["risk_level_accuracy"], float) or control["risk_level_accuracy"] >= 1.0:
        failures.append("self-test expects the labelled control runs to misclassify a STRICT case")
    if eng["defect_detection_recall"] != 1.0:
        failures.append("self-test expects the labelled engineering runs to find every defect")
    if not isinstance(control["defect_detection_recall"], float) or control["defect_detection_recall"] >= 1.0:
        failures.append("self-test expects the labelled control runs to miss a defect")
    if eng["defect_false_positive_count"] != 0:
        failures.append("self-test expects no false defects from the labelled engineering runs")
    if control["unverified_done_claims"] < 1:
        failures.append("self-test expects an unverified DONE in the labelled control runs")
    if control["false_block_rate"] in (NOT_MEASURED, 0):
        failures.append("self-test expects a false block in the labelled control runs")
    if eng["privilege_boundary_accuracy"] != 1.0:
        failures.append("self-test expects WAITING_PRIVILEGE from the labelled engineering runs")
    if not isinstance(compare(scores)["defects_caught_per_additional_10k_tokens"], float):
        failures.append("self-test expects token efficiency to be computable from supplied usage")
    if failures:
        print("\nFAIL: coding harness self-test")
        for failure in failures:
            print("- " + failure)
        return 1
    print("\nPASS: scorer separates the labelled coding conditions and honours NOT_MEASURED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("--json", action="store_true")
    score_parser = sub.add_parser("score")
    score_parser.add_argument("runs", type=Path)
    sub.add_parser("self-test")
    args = parser.parse_args()
    if args.command == "plan":
        return plan(args.json)
    if args.command == "score":
        return score(args.runs)
    return self_test()


if __name__ == "__main__":
    raise SystemExit(main())
