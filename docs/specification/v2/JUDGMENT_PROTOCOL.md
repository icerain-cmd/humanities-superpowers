# Traceable Scholarly Judgment Protocol

**Specification Version: 2.0.0**

## Authority boundary

Agent recommendation is advisory. Researcher decision is authoritative only when `authorized_by` identifies a human researcher, `authorization_ref` links a trusted human-interaction event outside the agent-authored record, `proposal_digest` binds that event to the exact proposal, and the record contains a decision and rationale. Missing authorization is not implicit approval. Schema validation checks the record shape; the host system MUST verify that the referenced event belongs to the session researcher and MUST NOT let an agent mint its own approval event.

## Lifecycle

`PROVISIONAL`, `ACCEPTED`, `REOPENED`, and `SUPERSEDED` are judgment statuses. An agent may create a recommendation and a `PROVISIONAL` record without a decision. It MUST NOT create `ACCEPTED` without `researcher_decision`, `authorized_by`, and `decided_at`.

Reopening preserves history:

```text
D1: ACCEPTED
new evidence
D1: REOPENED
D2: PROVISIONAL or ACCEPTED; supersedes D1
```

## Required visibility

The record distinguishes alternatives, evidence considered, interpretations considered, counterarguments considered, agent recommendations, researcher decision, and rationale. If the researcher selects B after an agent recommends A, B remains the decision and A remains recommendation history.

## Productive refusal

When no responsible decision can be made, return the current verified range, missing evidence, unresolved alternatives, bounded language presently permitted, and next verification action. Do not invent an authorization or convert indecision into acceptance.
