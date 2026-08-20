#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from fricturn_protocol import (
    invalidate_dependent_gates,
    should_propose_epistemic_return,
    trusted_authorization,
    trusted_verification,
    verification_transition_allowed,
)

ROOT = Path(__file__).resolve().parents[1]
FORMAT_CHECKER = FormatChecker()


def require_format_dependencies() -> None:
    if "date-time" not in FORMAT_CHECKER.checkers:
        raise RuntimeError(
            "date-time validation is unavailable; install requirements-validation.txt"
        )


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate(schema_name: str, instance: dict, errors: list[str], label: str) -> None:
    schema = load(f"schemas/{schema_name}")
    issues = sorted(
        Draft202012Validator(schema, format_checker=FORMAT_CHECKER).iter_errors(instance),
        key=lambda item: list(item.path),
    )
    errors.extend(f"{label}: {issue.message}" for issue in issues)


def main() -> int:
    require_format_dependencies()
    errors: list[str] = []
    friction = {item["id"]: item for item in load("tests/friction/cases.json")["cases"]}
    judgment = {item["id"]: item for item in load("tests/judgment/cases.json")["cases"]}
    returns = {item["id"]: item for item in load("tests/return/cases.json")["cases"]}
    regression = {item["id"]: item for item in load("tests/regression/cases.json")["cases"]}

    for case in friction.values():
        validate("friction-event.schema.json", case["friction"], errors, case["id"])
    validate("evidence-ledger.schema.json", regression["verified-but-irrelevant"]["ledger"], errors, "verified-but-irrelevant")
    validate("judgment-record.schema.json", judgment["researcher-decision-preservation"]["record"], errors, "researcher-decision-preservation")
    for record in judgment["researcher-reopens-own-decision"]["records"]:
        validate("judgment-record.schema.json", record, errors, record["decision_id"])
    validate("epistemic-return.schema.json", returns["epistemic-return"]["record"], errors, "epistemic-return")
    for record in regression["interpretation-overwrite"]["history"]:
        validate("interpretation-history.schema.json", record, errors, record["interpretation_id"])

    if friction["fluent-but-unsupported"].get("gate_status") != "FAIL":
        errors.append("fluent unsupported prose must FAIL")
    if "CONTRADICTS" not in friction["counterevidence"].get("ledger_standings", []):
        errors.append("counterevidence must remain in the ledger")
    if friction["rival-interpretation"].get("routing_decision") != "RESEARCHER_DECISION_REQUIRED":
        errors.append("rival interpretation requires researcher decision")
    if friction["agent-disagreement"]["friction"].get("friction_type") != "AGENT_DISAGREEMENT":
        errors.append("agent disagreement must create friction")
    accepted = judgment["researcher-decision-preservation"]["record"]
    if accepted["researcher_decision"] != "B" or accepted["agent_recommendations"][0]["recommendation"] != "A":
        errors.append("researcher decision must not be overwritten by agent recommendation")
    reopened = judgment["researcher-reopens-own-decision"]["records"]
    if reopened[1].get("supersedes") != reopened[0].get("decision_id"):
        errors.append("reopened judgment history must preserve supersession")
    history = regression["interpretation-overwrite"]["history"]
    if len(history) != 2 or history[1].get("supersedes") != history[0].get("interpretation_id"):
        errors.append("interpretation history must append rather than overwrite")
    concept_gates = [
        {"gate": "Terminology gate", "status": "PASS", "validity": "VALID", "dependency_refs": ["concept:C3"]},
        {"gate": "Argument gate", "status": "PASS", "validity": "VALID", "dependency_refs": ["concept:C3"]},
        {"gate": "Interpretation gate", "status": "CONDITIONAL PASS", "validity": "VALID", "dependency_refs": ["concept:C3"]},
        {"gate": "Citation-fit gate", "status": "PASS", "validity": "VALID", "dependency_refs": ["concept:C3", "source:S2"]},
        {"gate": "Unrelated source gate", "status": "PASS", "validity": "VALID", "dependency_refs": ["source:S9"]},
    ]
    updated, invalidated, recheck, preserved = invalidate_dependent_gates(concept_gates, {"concept:C3"}, material_change=True)
    if invalidated != ["Terminology gate", "Argument gate", "Interpretation gate", "Citation-fit gate"] or preserved != ["Unrelated source gate"]:
        errors.append("concept changes must invalidate all and only concept-dependent gates")
    if recheck:
        errors.append("complete concept dependencies must not produce an unbounded recheck")
    if updated[1]["status"] != "PASS" or updated[1]["validity"] != "INVALIDATED":
        errors.append("gate invalidation must preserve historical status and change validity")
    claim_gates = [
        {"gate": "Evidence support gate", "status": "PASS", "validity": "VALID", "dependency_refs": ["claim:C7"]},
        {"gate": "Citation gate", "status": "PASS", "validity": "VALID", "dependency_refs": ["claim:C7"]},
        {"gate": "Argument review gate", "status": "PASS", "validity": "VALID", "dependency_refs": ["claim:C7"]},
        {"gate": "Submission gate", "status": "PASS", "validity": "VALID", "dependency_refs": ["claim:C7", "scope:B1"]},
        {"gate": "Terminology gate", "status": "PASS", "validity": "VALID", "dependency_refs": ["concept:C8"]},
    ]
    _, claim_invalidated, claim_recheck, claim_preserved = invalidate_dependent_gates(claim_gates, {"claim:C7"}, material_change=True)
    if claim_invalidated != ["Evidence support gate", "Citation gate", "Argument review gate", "Submission gate"] or claim_preserved != ["Terminology gate"]:
        errors.append("claim changes must invalidate all and only claim-dependent gates")
    if claim_recheck:
        errors.append("complete claim dependencies must not produce an unbounded recheck")
    formatting, formatting_invalidated, formatting_recheck, formatting_preserved = invalidate_dependent_gates(
        concept_gates, {"concept:C3"}, material_change=False
    )
    if formatting_invalidated or formatting_recheck or formatting_preserved != [gate["gate"] for gate in concept_gates]:
        errors.append("formatting-only changes must preserve every gate")
    if any(gate["validity"] != "VALID" for gate in formatting):
        errors.append("formatting-only changes must not alter gate validity")
    incomplete_gate = [{"gate": "Legacy submission gate", "status": "PASS"}]
    incomplete, incomplete_invalidated, incomplete_recheck, incomplete_preserved = invalidate_dependent_gates(
        incomplete_gate, {"claim:C7"}, material_change=True
    )
    if incomplete_invalidated or incomplete_preserved or incomplete_recheck != ["Legacy submission gate"]:
        errors.append("missing dependency metadata after material change must require recheck")
    if incomplete[0].get("validity") != "REQUIRES_RECHECK":
        errors.append("missing dependency metadata must fail closed as REQUIRES_RECHECK")
    if should_propose_epistemic_return(material_change=False, new_knowledge=True):
        errors.append("non-material evidence must not force epistemic return")
    if not should_propose_epistemic_return(material_change=True, new_knowledge=True):
        errors.append("material new knowledge must permit epistemic-return proposal")
    if returns["no-op-return"].get("return_record") is not None:
        errors.append("non-material evidence must not force epistemic return")
    if regression["gate-regression"].get("previous_status") != "PASS" or regression["gate-regression"].get("current_validity") != "INVALIDATED":
        errors.append("changed dependencies must invalidate prior PASS validity")
    refusal = regression["productive-refusal"]["result"]
    for field in ("checked_range", "unverified_range", "required_verification", "permitted_wording"):
        if not refusal.get(field):
            errors.append(f"productive refusal missing {field}")
    unauthorized = dict(accepted)
    unauthorized.pop("authorized_by")
    schema = load("schemas/judgment-record.schema.json")
    if not list(Draft202012Validator(schema, format_checker=FORMAT_CHECKER).iter_errors(unauthorized)):
        errors.append("ACCEPTED judgment without human authorization must be invalid")
    recommendation_only = dict(accepted)
    for field in ("researcher_decision", "rationale", "authorized_by", "decided_at"):
        recommendation_only.pop(field, None)
    if not list(Draft202012Validator(schema, format_checker=FORMAT_CHECKER).iter_errors(recommendation_only)):
        errors.append("agent recommendation alone must not become ACCEPTED")
    malformed_time = dict(accepted)
    malformed_time["decided_at"] = "not-a-timestamp"
    if not list(Draft202012Validator(schema, format_checker=FORMAT_CHECKER).iter_errors(malformed_time)):
        errors.append("accepted judgment must use a valid date-time")
    forged_authorization = dict(accepted)
    forged_authorization["authorized_by"] = "agent:A"
    if not list(Draft202012Validator(schema, format_checker=FORMAT_CHECKER).iter_errors(forged_authorization)):
        errors.append("an agent identifier must not authorize a researcher decision")
    trusted_approvals = {
        accepted["authorization_ref"]: {
            "actor": accepted["authorized_by"],
            "proposal_digest": accepted["proposal_digest"],
            "human_confirmed": True,
        }
    }
    if not trusted_authorization(accepted, trusted_approvals):
        errors.append("matching external human approval must authorize the decision")
    forged_approvals = {
        accepted["authorization_ref"]: {
            "actor": "researcher:forged",
            "proposal_digest": accepted["proposal_digest"],
            "human_confirmed": True,
        }
    }
    if trusted_authorization(accepted, forged_approvals):
        errors.append("self-asserted or mismatched approval must not authorize a decision")
    interpretation_schema = load("schemas/interpretation-history.schema.json")
    unauthorized_interpretation = dict(history[0])
    unauthorized_interpretation["researcher_status"] = "ACCEPTED"
    unauthorized_interpretation.pop("authorized_by", None)
    if not list(Draft202012Validator(interpretation_schema, format_checker=FORMAT_CHECKER).iter_errors(unauthorized_interpretation)):
        errors.append("AI interpretation without human authorization must remain PROPOSED")
    orphaned_interpretation = dict(history[1])
    orphaned_interpretation.pop("supersedes", None)
    if not list(Draft202012Validator(interpretation_schema, format_checker=FORMAT_CHECKER).iter_errors(orphaned_interpretation)):
        errors.append("interpretation version 2 must preserve its predecessor reference")
    orphaned_reopen = dict(reopened[0])
    orphaned_reopen.pop("supersedes", None)
    if not list(Draft202012Validator(schema, format_checker=FORMAT_CHECKER).iter_errors(orphaned_reopen)):
        errors.append("reopened judgment must preserve its predecessor reference")
    gate_schema = load("schemas/gate-report-v2.schema.json")
    invalid_gate_status = {
        "schema_version": "2.0",
        "gate": "Argument gate",
        "status": "INVALIDATED",
        "evidence_checked": [],
        "blocking_issues": [],
        "non_blocking_risks": [],
        "researcher_decisions_required": [],
        "required_next_action": "Recheck",
        "next_skill": None,
    }
    if not list(Draft202012Validator(gate_schema, format_checker=FORMAT_CHECKER).iter_errors(invalid_gate_status)):
        errors.append("INVALIDATED must be validity, never a gate status")
    versionless_empty_pass = {
        "gate": "Submission",
        "status": "PASS",
        "evidence_checked": [],
        "blocking_issues": [],
        "non_blocking_risks": [],
        "researcher_decisions_required": [],
        "required_next_action": "",
        "next_skill": None,
    }
    if not list(Draft202012Validator(gate_schema, format_checker=FORMAT_CHECKER).iter_errors(versionless_empty_pass)):
        errors.append("versionless evidence-free PASS must not satisfy the full v2 gate profile")
    valid_v2_gate = {
        "schema_version": "2.0",
        "gate": "Argument gate",
        "status": "PASS",
        "validity": "VALID",
        "dependency_refs": ["claim:C7"],
        "evidence_checked": ["ledger:L7"],
        "blocking_issues": [],
        "non_blocking_risks": [],
        "researcher_decisions_required": [],
        "required_next_action": "Proceed to review.",
        "next_skill": "reviewing-manuscript",
    }
    if list(Draft202012Validator(gate_schema, format_checker=FORMAT_CHECKER).iter_errors(valid_v2_gate)):
        errors.append("complete versioned v2 gate report must validate")
    if verification_transition_allowed(
        "researcher-supplied", "verified-primary", verification_performed=False
    ):
        errors.append("researcher-supplied evidence must not be promoted without verification")
    if not verification_transition_allowed(
        "researcher-supplied", "verified-primary", verification_performed=True
    ):
        errors.append("an explicit verification act must permit a recorded verified transition")
    ledger_schema = load("schemas/evidence-ledger.schema.json")
    provenance_free_verified = dict(regression["verified-but-irrelevant"]["ledger"])
    for field in ("verification_method", "locator", "checked_at", "checked_by"):
        provenance_free_verified.pop(field, None)
    if not list(Draft202012Validator(ledger_schema, format_checker=FORMAT_CHECKER).iter_errors(provenance_free_verified)):
        errors.append("verified evidence without verification provenance must be invalid")
    verified_entry = regression["verified-but-irrelevant"]["ledger"]
    trusted_checks = {
        verified_entry["verification_event_ref"]: {
            "checker": verified_entry["checked_by"],
            "source_id": verified_entry["source_id"],
            "source_digest": verified_entry["source_digest"],
            "locator": verified_entry["locator"],
            "verification_performed": True,
        }
    }
    if not trusted_verification(verified_entry, trusted_checks):
        errors.append("matching external source-check event must establish verification")
    if trusted_verification(verified_entry, {}):
        errors.append("self-asserted verification metadata must not establish verification")

    example_entries = load("examples/conflicting-evidence-example/evidence-ledger.json")
    for index, entry in enumerate(example_entries, start=1):
        validate("evidence-ledger.schema.json", entry, errors, f"conflicting-example-L{index}")
    validate("epistemic-return.schema.json", load("examples/epistemic-return-example/return-record.json"), errors, "return-example")
    validate("judgment-record.schema.json", load("examples/epistemic-return-example/judgment-record.json"), errors, "return-judgment-example")
    for record in load("examples/judgment-history-example/judgments.json"):
        validate("judgment-record.schema.json", record, errors, f"judgment-example-{record['decision_id']}")
    for record in load("examples/rival-interpretation-example/interpretations.json"):
        validate("interpretation-history.schema.json", record, errors, f"interpretation-example-{record['interpretation_id']}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAIL: {len(errors)} v2 conformance error(s)")
        return 1
    print("PASS: 12 Fricturn cases plus negative boundaries; schemas, judgment authority, bounded gate invalidation, verification transitions, and epistemic return")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
