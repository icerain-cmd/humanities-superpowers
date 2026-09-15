#!/usr/bin/env python3
"""Dual-Core routing, contract, and provenance checks.

Covers: RESEARCH/CODE/HYBRID routing, QUICK/STANDARD/STRICT calibration,
privilege-boundary escalation, the smallest-sufficient-route rule, completion
verification, worker-state representation, model-agnostic contracts, vendored
provenance integrity, and unchanged Humanities regression.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from dual_core_router import (  # noqa: E402
    DOMAINS,
    ENGINEERING_BASE_ROUTES,
    RISK_LEVELS,
    route,
)

VENDOR = ROOT / "vendor/obra-superpowers"
PROVENANCE = VENDOR / "PROVENANCE.json"
FORMAT_CHECKER = FormatChecker()
HUMANITIES_SKILLS = {
    "using-humanities-superpowers",
    "formulating-research-question",
    "scoping-argument-boundary",
    "mapping-concept-lineage",
    "conducting-literature-dialogue",
    "planning-humanities-argument",
    "performing-close-reading",
    "structuring-humanities-argument",
    "stress-testing-argument",
    "auditing-citations",
    "checking-terminology-consistency",
    "reviewing-manuscript",
    "responding-to-peer-review",
    "verifying-before-submission",
}
MODEL_TOKENS = ("gpt", "claude", "deepseek", "sonnet", "opus", "gemini", "llama", "qwen")


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate(
    schema_name: str, instance: dict, errors: list[str], label: str, *, expect_valid: bool = True
) -> bool:
    schema = load(f"schemas/{schema_name}")
    issues = sorted(
        Draft202012Validator(schema, format_checker=FORMAT_CHECKER).iter_errors(instance),
        key=lambda item: list(item.path),
    )
    if expect_valid:
        errors.extend(f"{label}: {issue.message}" for issue in issues)
    elif not issues:
        errors.append(f"{label}: expected the schema to reject this artifact")
    return not issues


def tree_hash(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(
        (item for item in directory.rglob("*") if item.is_file()),
        key=lambda item: item.relative_to(directory).as_posix(),
    ):
        relative = path.relative_to(directory).as_posix()
        digest.update(f"{relative}\0{hashlib.sha256(path.read_bytes()).hexdigest()}\n".encode())
    return digest.hexdigest()


def check_provenance(errors: list[str]) -> set[str]:
    """The vendored tree must match the recorded upstream hashes."""
    if not PROVENANCE.is_file():
        errors.append("vendored provenance file missing: vendor/obra-superpowers/PROVENANCE.json")
        return set()
    data = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    for field in ("repository", "version", "commit", "commit_date", "license", "copyright", "imported_at"):
        if not data.get("upstream", {}).get(field):
            errors.append(f"vendored provenance is missing upstream.{field}")
    if "update procedure" not in PROVENANCE.with_suffix(".md").read_text(encoding="utf-8").lower():
        errors.append("vendored provenance does not document an update procedure")
    imported = data.get("imported", {})
    aggregate = hashlib.sha256()
    for name in sorted(imported):
        directory = VENDOR / "skills" / name
        if not directory.is_dir():
            errors.append(f"vendored skill missing: {name}")
            continue
        actual = tree_hash(directory)
        if actual != imported[name]["tree_sha256"]:
            errors.append(f"vendored skill changed since import: {name}")
        count = sum(1 for item in directory.rglob("*") if item.is_file())
        if count != imported[name]["files"]:
            errors.append(f"vendored skill file count changed: {name}")
        aggregate.update(f"{name}\0{actual}\n".encode())
    if aggregate.hexdigest() != data.get("aggregate_sha256"):
        errors.append("vendored aggregate hash does not match the recorded import")
    license_hash = hashlib.sha256((VENDOR / "LICENSE").read_bytes()).hexdigest()
    if license_hash != data.get("license_sha256"):
        errors.append("vendored LICENSE changed since import")

    on_disk = {item.name for item in (VENDOR / "skills").iterdir() if item.is_dir()}
    if on_disk != set(imported):
        errors.append(f"vendored skill set mismatch: on disk={sorted(on_disk)}")
    excluded = {item["skill"] for item in data.get("excluded", [])}
    if not excluded:
        errors.append("vendored provenance records no exclusions")
    for item in data.get("excluded", []):
        if not item.get("reason"):
            errors.append(f"exclusion without a reason: {item.get('skill')}")
    if on_disk & excluded:
        errors.append(f"a skill is both imported and excluded: {sorted(on_disk & excluded)}")
    return on_disk


def check_imported_skill_paths(imported: set[str], errors: list[str]) -> None:
    router = (ROOT / "skills/using-humanities-superpowers/SKILL.md").read_text(encoding="utf-8")
    for name in sorted(imported):
        if name not in router:
            errors.append(f"router never names the imported engineering skill {name}")
        if not (VENDOR / "skills" / name / "SKILL.md").is_file():
            errors.append(f"imported engineering skill has no SKILL.md: {name}")
    for name in sorted(HUMANITIES_SKILLS):
        if name not in router:
            errors.append(f"router never names the humanities skill {name}")


def check_routes(imported: set[str], errors: list[str]) -> None:
    cases = load("tests/dual-core/cases.json")["cases"]
    seen_domains: set[str] = set()
    seen_levels: set[str] = set()
    for case in cases:
        decision = route(case["task"])
        expected = case["expect"]
        label = case["id"]
        seen_domains.add(decision["domain"])
        if decision["risk_level"]:
            seen_levels.add(decision["risk_level"])
        for key in ("domain", "risk_level", "engineering_skills", "humanities_skills"):
            if decision[key] != expected[key]:
                errors.append(f"{label}: {key} {decision[key]!r} != {expected[key]!r}")
        for name in decision["engineering_skills"]:
            if name not in imported:
                errors.append(f"{label}: route names an unvendored engineering skill: {name}")
        for name in decision["humanities_skills"]:
            if name not in HUMANITIES_SKILLS:
                errors.append(f"{label}: route names an unknown humanities skill: {name}")
        if decision["domain"] == "RESEARCH" and decision["engineering_skills"]:
            errors.append(f"{label}: research work must not load the engineering core")
        if decision["domain"] == "CODE" and decision["humanities_skills"]:
            errors.append(f"{label}: code work must not load the humanities core")
        if decision["domain"] == "HYBRID" and not (
            decision["engineering_skills"] and decision["humanities_skills"]
        ):
            errors.append(f"{label}: hybrid work must name both the engineering fix and the research check")

    for domain in DOMAINS:
        if domain not in seen_domains:
            errors.append(f"no case exercises the {domain} domain")
    for level in RISK_LEVELS:
        if level not in seen_levels:
            errors.append(f"no case exercises the {level} risk level")

    # Smallest sufficient route: no case may load a full core.
    for case in cases:
        decision = route(case["task"])
        if len(decision["engineering_skills"]) >= len(imported):
            errors.append(f"{case['id']}: route loads the entire engineering core")
        if len(decision["humanities_skills"]) >= len(HUMANITIES_SKILLS):
            errors.append(f"{case['id']}: route loads the entire humanities core")
        level = decision["risk_level"]
        if level and len(decision["engineering_skills"]) < len(ENGINEERING_BASE_ROUTES[level]):
            errors.append(f"{case['id']}: route is smaller than the level's required base route")

    # Unclassifiable work must fail loudly rather than silently defaulting.
    try:
        route({"id": "unclassifiable", "produces": "neither"})
    except ValueError:
        pass
    else:
        errors.append("an unclassifiable task must be rejected, not defaulted")


def check_completion_evidence(errors: list[str]) -> None:
    base = {
        "package_id": "E-1",
        "work_package_ref": "W-1",
        "files_changed": [{"path": "a.py", "reason": "fix"}],
        "tests_run": ["python3 -m pytest tests"],
        "test_results": ["12 passed"],
        "unresolved": [],
        "deviations": [],
        "completion_status": "DONE",
        "completion_verification": "pytest output captured in the run log",
    }
    if not validate("evidence-package.schema.json", base, errors, "I-verified-done"):
        errors.append("I: a verified DONE evidence package must validate")
    unverified = dict(base)
    unverified.pop("completion_verification")
    unverified["tests_run"] = []
    unverified["test_results"] = []
    validate("evidence-package.schema.json", unverified, errors, "I-unverified-done", expect_valid=False)
    partial = dict(base)
    partial["completion_status"] = "PARTIAL"
    partial.pop("completion_verification")
    partial["tests_run"] = []
    partial["test_results"] = []
    if not validate("evidence-package.schema.json", partial, errors, "I-partial"):
        errors.append("I: an unverified PARTIAL package must remain valid so honest reporting is possible")


def check_worker_state(errors: list[str]) -> None:
    base = {
        "worker_id": "worker-1",
        "task_ref": "W-1",
        "state": "WORKING",
        "since": "2026-09-15T00:00:00Z",
        "last_progress_at": "2026-09-15T00:05:00Z",
        "stall_threshold_seconds": 900,
        "attempt_count": 0,
        "progress_evidence": ["tests/test_a.py changed"],
    }
    if not validate("worker-state.schema.json", base, errors, "J-working"):
        errors.append("J: a WORKING state with fresh progress evidence must validate")
    stalled = dict(base)
    stalled.pop("progress_evidence")
    validate("worker-state.schema.json", stalled, errors, "J-working-no-evidence", expect_valid=False)

    privilege = dict(base)
    privilege.update(
        {
            "state": "WAITING_PRIVILEGE",
            "privilege_boundary": "SYSTEM",
            "requested_action": "register a SYSTEM-owned scheduled task",
            "rollback_plan": "unregister the task and restore the exported XML",
        }
    )
    if not validate("worker-state.schema.json", privilege, errors, "J-waiting-privilege"):
        errors.append("J: a documented WAITING_PRIVILEGE state must validate")
    for missing in ("privilege_boundary", "requested_action", "rollback_plan"):
        incomplete = dict(privilege)
        incomplete.pop(missing)
        validate(
            "worker-state.schema.json",
            incomplete,
            errors,
            f"J-privilege-without-{missing}",
            expect_valid=False,
        )

    done = dict(base)
    done["state"] = "DONE"
    validate("worker-state.schema.json", done, errors, "J-done-without-verification", expect_valid=False)
    done["completion_verification_ref"] = "run:2026-09-15T00:10Z"
    if not validate("worker-state.schema.json", done, errors, "J-done-verified"):
        errors.append("J: a verified DONE state must validate")

    blocked = dict(base)
    blocked["state"] = "BLOCKED"
    validate("worker-state.schema.json", blocked, errors, "J-blocked-without-reason", expect_valid=False)


def check_work_package(errors: list[str]) -> None:
    base = {
        "package_id": "W-1",
        "objective": "Fix the citation verifier's support classification",
        "domain": "HYBRID",
        "scope": {"in_scope": ["verifier"], "out_of_scope": ["UI"]},
        "constraints": ["no network"],
        "risk_level": "STRICT",
        "risk_reason": "contract_surface:schema",
        "acceptance_criteria": ["the wrong label is no longer produced"],
        "required_verification": ["run the verifier tests"],
        "forbidden_actions": ["do not change the gate schema"],
        "reviewer_role": "REVIEWER",
    }
    if not validate("work-package.schema.json", base, errors, "W-strict"):
        errors.append("a STRICT work package with a named reviewer must validate")
    for missing in ("acceptance_criteria", "required_verification", "forbidden_actions"):
        incomplete = dict(base)
        incomplete.pop(missing)
        validate(
            "work-package.schema.json", incomplete, errors, f"W-without-{missing}", expect_valid=False
        )
    unclassified = dict(base)
    unclassified["risk_level"] = "STANDARD"
    unclassified.pop("risk_reason")
    validate(
        "work-package.schema.json",
        unclassified,
        errors,
        "W-standard-without-reason",
        expect_valid=False,
    )


def check_model_agnostic(errors: list[str]) -> None:
    for path in sorted((ROOT / "schemas").glob("*.schema.json")):
        text = path.read_text(encoding="utf-8").lower()
        for token in MODEL_TOKENS:
            if token in text:
                errors.append(f"schema hard-codes a model name ({token}): {path.name}")
        if re.search(r"\bsol\b", text):
            errors.append(f"schema hard-codes a model name (sol): {path.name}")
    # The routing implementation must stay model-agnostic. This test file is
    # excluded because it has to contain the tokens it searches for.
    for path in [ROOT / "scripts/dual_core_router.py"]:
        text = path.read_text(encoding="utf-8").lower()
        for token in MODEL_TOKENS:
            if token in text:
                errors.append(f"routing code hard-codes a model name ({token}): {path.name}")


def check_documentation(errors: list[str]) -> None:
    required = {
        "DUAL_CORE_ROUTER.md": ["RESEARCH", "CODE", "HYBRID", "smallest sufficient"],
        "RISK_ROUTER.md": ["QUICK", "STANDARD", "STRICT", "SYSTEM"],
        "AUTONOMOUS_WORKER.md": ["WAITING_PRIVILEGE", "DONE", "stall"],
        "AGENT_ORCHESTRATION.md": ["WORK_PACKAGE", "EVIDENCE_PACKAGE", "ESCALATION_REVIEWER"],
    }
    base = ROOT / "docs/specification/dual-core"
    for name, phrases in required.items():
        path = base / name
        if not path.is_file():
            errors.append(f"dual-core specification missing: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{name} does not define {phrase}")
    orchestration = (base / "AGENT_ORCHESTRATION.md").read_text(encoding="utf-8")
    if "not part of the architecture" not in orchestration:
        errors.append("the operating profile must be marked replaceable, not architectural")


def check_humanities_regression(errors: list[str]) -> None:
    found = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    if found != HUMANITIES_SKILLS:
        errors.append(f"humanities skill set changed: missing={sorted(HUMANITIES_SKILLS - found)} extra={sorted(found - HUMANITIES_SKILLS)}")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/run_v2_tests.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        errors.append("humanities v2 conformance regressed: " + (result.stdout + result.stderr).strip())


def main() -> int:
    errors: list[str] = []
    imported = check_provenance(errors)
    check_imported_skill_paths(imported, errors)
    check_routes(imported, errors)
    check_completion_evidence(errors)
    check_worker_state(errors)
    check_work_package(errors)
    check_model_agnostic(errors)
    check_documentation(errors)
    check_humanities_regression(errors)
    if errors:
        print("FAIL: dual-core checks")
        for error in errors:
            print("- " + error)
        return 1
    print(
        f"PASS: dual-core routing ({len(DOMAINS)} domains, {len(RISK_LEVELS)} levels), "
        f"{len(imported)} vendored engineering skills with matching provenance, "
        "completion-verification and worker-state contracts, model-agnostic schemas, "
        "and unchanged humanities regression"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
