"""Small deterministic helpers for Fricturn protocol conformance.

These functions do not automate scholarly judgment. They preserve existing gate
statuses while calculating current validity from explicit dependency references.
"""
from __future__ import annotations

from copy import deepcopy


def invalidate_dependent_gates(
    gates: list[dict], changed_refs: set[str], *, material_change: bool
) -> tuple[list[dict], list[str], list[str], list[str]]:
    """Return copied gates plus invalidated, recheck, and preserved names.

    A material change cannot safely preserve a gate whose dependency metadata is
    absent. Such a gate requires recheck rather than being assumed valid.
    """
    updated = deepcopy(gates)
    invalidated: list[str] = []
    recheck: list[str] = []
    preserved: list[str] = []
    for gate in updated:
        dependencies = set(gate.get("dependency_refs", []))
        if material_change and not dependencies:
            gate["validity"] = "REQUIRES_RECHECK"
            recheck.append(gate["gate"])
        elif material_change and dependencies.intersection(changed_refs):
            gate["validity"] = "INVALIDATED"
            invalidated.append(gate["gate"])
        else:
            gate.setdefault("validity", "VALID")
            preserved.append(gate["gate"])
    return updated, invalidated, recheck, preserved


def should_propose_epistemic_return(*, material_change: bool, new_knowledge: bool) -> bool:
    """A return requires both new knowledge and a material change."""
    return material_change and new_knowledge


def verification_transition_allowed(
    previous: str,
    proposed: str,
    *,
    verification_performed: bool,
) -> bool:
    """Reject silent promotion into a verified state.

    The helper deliberately does not impose a total order on epistemic states.
    It only enforces the invariant that verified states require an explicit act.
    """
    verified = {"verified-primary", "verified-secondary"}
    if proposed in verified and previous not in verified:
        return verification_performed
    return True


def trusted_authorization(record: dict, approval_events: dict[str, dict]) -> bool:
    """Bind an approval to a trusted event, actor, and proposal digest.

    ``approval_events`` must be supplied by the host's human-interaction layer;
    records being evaluated must never populate that mapping themselves.
    """
    event = approval_events.get(record.get("authorization_ref"))
    return bool(
        event
        and event.get("actor") == record.get("authorized_by")
        and event.get("proposal_digest") == record.get("proposal_digest")
        and event.get("human_confirmed") is True
    )


def trusted_verification(entry: dict, verification_events: dict[str, dict]) -> bool:
    """Bind verified standing to a host-supplied source-check event."""
    event = verification_events.get(entry.get("verification_event_ref"))
    return bool(
        event
        and event.get("checker") == entry.get("checked_by")
        and event.get("source_id") == entry.get("source_id")
        and event.get("source_digest") == entry.get("source_digest")
        and event.get("locator") == entry.get("locator")
        and event.get("verification_performed") is True
    )
