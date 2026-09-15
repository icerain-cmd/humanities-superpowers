# Dual-Core Router

**Status: implemented and released in v2.1.0. The research core it routes to is unchanged.**

Humanities Superpowers keeps its research protocol intact and adds a second,
vendored engineering core. One router decides which core a request needs, in
what order, and how much process the risk justifies.

## The two cores

| Core | Location | Purpose |
|---|---|---|
| Humanities (Research) | `skills/` (14 skills, incl. this router) | Scholarly judgment: questions, concepts, interpretation, citation verification, gates, epistemic return |
| Engineering (Code) | [`vendor/obra-superpowers/skills/`](../../../vendor/obra-superpowers/PROVENANCE.md) | Software practice: planning, TDD, systematic debugging, review, parallel dispatch, branch completion |

The engineering core is vendored unmodified and path-referenced. It is not
registered as a second plugin, so no competing router and no second skill
namespace exists. Provenance, hashes, and exclusions are recorded in
`vendor/obra-superpowers/PROVENANCE.json`.

## Domain axis

Classify every request on one axis before selecting skills.

| Domain | Signal | Route |
|---|---|---|
| `RESEARCH` | The deliverable is scholarly text, interpretation, a source claim, a citation record, or a research decision | Humanities core only |
| `CODE` | The deliverable is working software, configuration, or infrastructure whose consumers are programs or operators | Engineering core only |
| `HYBRID` | The deliverable is software whose correctness depends on scholarly requirements, or scholarship whose correctness depends on software the agent changed | Both cores, smallest sufficient combination |

Classification is semantic, not lexical. The words "review", "structure", or
"verify" appear in both cores; the question is what artifact must be correct
at the end.

### Examples

| Request | Domain | Smallest sufficient route |
|---|---|---|
| Review whether these citations support the claim | `RESEARCH` | `auditing-citations` |
| Fix CSS spacing in a dashboard header | `CODE` | localized edit plus targeted visual check |
| Fix the citation verifier that checks whether sources support a claim | `HYBRID` | `test-driven-development` → the fix → `auditing-citations` on the verifier's own output |
| Build a new dashboard panel | `CODE` | `writing-plans` → `test-driven-development` → `requesting-code-review` |
| Write the methods section describing how the verifier works | `RESEARCH` | `planning-humanities-argument` (the software is an object of description, not a deliverable to change) |

## Smallest sufficient route

The router selects the fewest skills that can reach the requested outcome, and
stops when that outcome is reached.

Rules:

1. Load the router first, then only the skills on the chosen route.
2. Never load both cores "for safety". Loading the other core without a
   concrete artifact that needs it is a routing failure, not diligence.
3. Within the engineering core, pick the subset the task needs. A localized
   edit does not need the full planning → TDD → review chain.
4. Within the humanities core, the existing gate and progression rules are
   unchanged and remain authoritative.

## HYBRID rule: code changes can invalidate research claims

When a change alters how research artifacts are produced — citation checking,
evidence extraction, terminology tables, concept dictionaries, schema
validation, or gate automation — the router must treat that change as a
possible material dependency change in the Fricturn sense.

Concretely:

1. Perform the engineering route (`QUICK`, `STANDARD`, or `STRICT`).
2. Determine whether the change can alter any recorded claim, citation record,
   evidence standing, or gate result.
3. If it can, re-run the affected humanities check and mark affected gates
   `INVALIDATED` or `REQUIRES_RECHECK` rather than leaving them `VALID`.
4. If it cannot, record why, so the decision is auditable.

A code change is never allowed to silently keep a research gate `VALID`.

## Division of records

| Record | Owner |
|---|---|
| Gate report, friction event, evidence ledger, epistemic return, judgment record | Humanities core |
| `WORK_PACKAGE`, `EVIDENCE_PACKAGE`, worker state | Shared orchestration layer |

Engineering work does not manufacture humanities gate reports, and humanities
work does not manufacture engineering test evidence. `HYBRID` runs produce
both, side by side.

## Failure modes this router must avoid

- Routing every request to the engineering core because it "also has process".
- Routing every request to the humanities core, including ordinary code edits.
- Treating `HYBRID` as an excuse to run both cores end to end.
- Loading all 24+ skills, or loading a core's skills "just in case".

See [Risk calibration](RISK_ROUTER.md) for the second axis, and
[Agent orchestration](AGENT_ORCHESTRATION.md) for handoff contracts.
