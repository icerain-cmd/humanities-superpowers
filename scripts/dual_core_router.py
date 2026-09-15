#!/usr/bin/env python3
"""Reference implementation of the Dual-Core routing contract.

`docs/specification/dual-core/*.md` is normative. This module is the executable
reference used by `scripts/run_dual_core_tests.py`, so the routing rules can be
regression-tested instead of only read.

Classification is property-based, not keyword-based. Callers describe a task by
its reversibility, blast radius, privilege boundary, persistence, contract
surface, environment, failure cost, and uncertainty; the router derives the
level from those properties.
"""
from __future__ import annotations

DOMAINS = ("RESEARCH", "CODE", "HYBRID")
RISK_LEVELS = ("QUICK", "STANDARD", "STRICT")

#: Properties that force STRICT on their own.
STRICT_TRIGGERS = frozenset(
    {
        "production",
        "authentication",
        "authorization",
        "security",
        "credential_handling",
        "database_migration",
        "destructive_data_operation",
        "deployment",
        "privilege_boundary",
        "networking",
        "backup_restore",
        "major_refactor",
        "public_contract",
        "persistent_infrastructure",
    }
)

PRIVILEGE_BOUNDARIES = frozenset(
    {"UAC", "SYSTEM", "ADMINISTRATOR", "SERVICE_ACCOUNT", "EXTERNAL_CREDENTIAL"}
)
#: Contract surfaces that force STRICT. An internal-only surface raises the
#: level to STANDARD but does not make a change dangerous on its own.
STRICT_CONTRACT_SURFACES = frozenset(
    {"public_api", "file_format", "cli", "plugin_manifest", "installation_path", "schema"}
)
LOCAL_ENVIRONMENTS = frozenset({"local", "development"})
LOCAL_BLAST_RADII = frozenset({"single_file", "single_symbol"})

#: Base engineering routes per level. Additions are explicit, never implied.
ENGINEERING_BASE_ROUTES = {
    "QUICK": [],
    "STANDARD": ["test-driven-development", "verification-before-completion"],
    "STRICT": [
        "writing-plans",
        "test-driven-development",
        "requesting-code-review",
        "verification-before-completion",
    ],
}


def classify_domain(task: dict) -> str:
    """Return the domain of a task.

    ``produces`` is the artifact that must end up correct. ``scholarly_dependency``
    marks software whose correctness depends on scholarly requirements;
    ``software_dependency`` marks scholarship whose correctness depends on
    software the agent changes.
    """
    produces = task.get("produces")
    scholarly_dependency = bool(task.get("scholarly_dependency"))
    software_dependency = bool(task.get("software_dependency"))
    if produces == "scholarly" and not software_dependency:
        return "RESEARCH"
    if produces == "software" and not scholarly_dependency:
        return "CODE"
    if produces in {"scholarly", "software"}:
        return "HYBRID"
    raise ValueError(f"unclassifiable task: produces={produces!r}")


def classify_risk(task: dict) -> tuple[str, list[str]]:
    """Return ``(level, reasons)`` for a CODE or HYBRID task.

    Any single STRICT property is sufficient. Otherwise a task is QUICK only if
    it is reversible, localized, non-persistent, contract-free, local, and
    unambiguous; everything else is STANDARD.
    """
    strict_reasons: list[str] = []
    for trigger in sorted(set(task.get("strict_triggers") or [])):
        if trigger in STRICT_TRIGGERS:
            strict_reasons.append(f"trigger:{trigger}")
    boundary = task.get("privilege_boundary")
    if boundary in PRIVILEGE_BOUNDARIES:
        strict_reasons.append(f"privilege_boundary:{boundary}")
    if task.get("destructive") is True:
        strict_reasons.append("destructive_data_operation")
    persistence = task.get("persistence")
    if persistence and persistence != "none":
        strict_reasons.append(f"persistence:{persistence}")
    contract = task.get("contract_surface")
    if contract in STRICT_CONTRACT_SURFACES:
        strict_reasons.append(f"contract_surface:{contract}")
    environment = task.get("environment")
    if environment and environment not in LOCAL_ENVIRONMENTS:
        strict_reasons.append(f"environment:{environment}")
    if task.get("reversible") is False:
        strict_reasons.append("irreversible")
    if strict_reasons:
        return "STRICT", strict_reasons

    standard_reasons: list[str] = []
    if contract and contract != "none" and contract not in STRICT_CONTRACT_SURFACES:
        standard_reasons.append(f"contract_surface:{contract}")
    if task.get("blast_radius") not in LOCAL_BLAST_RADII:
        standard_reasons.append(f"blast_radius:{task.get('blast_radius')}")
    if environment not in LOCAL_ENVIRONMENTS:
        standard_reasons.append(f"environment:{environment}")
    if task.get("uncertainty") != "low":
        standard_reasons.append(f"uncertainty:{task.get('uncertainty')}")
    if task.get("reversible") is not True:
        standard_reasons.append("reversibility_unknown")
    if task.get("failure_cost") == "silent":
        standard_reasons.append("failure_cost:silent")
    if standard_reasons:
        return "STANDARD", standard_reasons
    return "QUICK", ["localized, reversible, non-persistent, local edit"]


def select_engineering_route(level: str, task: dict) -> list[str]:
    """Return the smallest sufficient engineering skill route for a level."""
    if level not in ENGINEERING_BASE_ROUTES:
        raise ValueError(f"unknown risk level: {level!r}")
    route = list(ENGINEERING_BASE_ROUTES[level])
    if task.get("unknown_cause") and level != "QUICK":
        route.insert(0, "systematic-debugging")
    if task.get("multi_step") and "writing-plans" not in route:
        route.insert(0, "writing-plans")
    if task.get("parallel"):
        route.append("dispatching-parallel-agents")
    return route


def route(task: dict) -> dict:
    """Return the full routing decision for a task descriptor."""
    domain = classify_domain(task)
    decision = {
        "task_id": task.get("id"),
        "domain": domain,
        "risk_level": None,
        "risk_reasons": [],
        "engineering_skills": [],
        "humanities_skills": [],
    }
    if domain == "RESEARCH":
        decision["humanities_skills"] = list(task.get("research_checks") or [])
        return decision
    level, reasons = classify_risk(task)
    decision["risk_level"] = level
    decision["risk_reasons"] = reasons
    decision["engineering_skills"] = select_engineering_route(level, task)
    if domain == "HYBRID":
        decision["humanities_skills"] = list(task.get("research_checks") or [])
    return decision
