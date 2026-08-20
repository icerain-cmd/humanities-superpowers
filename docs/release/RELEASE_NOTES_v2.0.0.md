# Humanities Superpowers v2.0.0 — Fricturn

**Status: draft release notes. v2.0.0 has not been tagged, pushed, or publicly released by this implementation task.**

Fricturn extends the v1 scholarly judgment scaffold without changing its 13 core skills, one router, verification-state vocabulary, gate statuses, or routing decisions.

## Added

- Interpretive friction as a traceable research event.
- Claim-specific evidential standing distinct from source verification.
- Append-only judgment and interpretation histories.
- Epistemic return for knowledge-driven reopening of earlier objects.
- Bounded gate invalidation through explicit dependency references.
- Productive refusal records that preserve checked range and next verification.
- Twelve deterministic v2 conformance cases, explicit negative boundary checks, and four synthetic examples.

## Compatibility

v1 research objects and sessions remain valid because the extended base fields are optional. Dedicated v2 schemas enforce stronger object-level rules. Gate status remains `PASS`, `CONDITIONAL PASS`, or `FAIL`; validity is a separate property.

## Validation

Release preparation requires repository validation, integrated tests, v2 conformance tests, public-release validation, JSON/YAML parsing, link checks, and manifest regeneration. No tag, push, release, or merge is performed by the implementation task.
