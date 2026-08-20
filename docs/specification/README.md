# Humanities Superpowers Research Specification v1.0

**Status:** v1.0 normative specification
**Specification version:** 1.0.0  
**Project version:** 1.0.0

This specification defines the common language, contracts, research objects, quality gates, and conformance requirements used by Humanities Superpowers skills.

It exists for one reason: a repository of individually useful prompts is not yet a method. A method requires shared objects, explicit transitions, observable outputs, declared failure conditions, and stable rules for uncertainty.

## Normative documents

1. [Core specification](CORE_SPECIFICATION.md)
2. [Skill contract specification](SKILL_CONTRACT.md)
3. [Research object model](RESEARCH_OBJECT_MODEL.md)
4. [Research grammar](RESEARCH_GRAMMAR.md)
5. [Language and terminology guide](LANGUAGE_GUIDE.md)
6. [Conformance and testing](CONFORMANCE.md)
7. [Extension protocol](EXTENSION_PROTOCOL.md)
8. [Decision records](DECISION_RECORDS.md)

## Normative vocabulary

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are to be interpreted as requirement levels within this project. They are used to make skill behavior auditable, not to imitate legal certainty.

## Scope

The specification governs:

- skill metadata and document structure;
- declared inputs and outputs;
- the representation of claims, evidence, interpretations, and uncertainty;
- stop conditions and quality-gate outcomes;
- transitions between skills;
- researcher decisions that cannot be delegated;
- repository-level validation and contribution requirements.

It does not define a universal method for all humanities disciplines. A conforming skill may add discipline-specific procedures, but it may not weaken the core safeguards.

## Conformance levels

- **Document conformant:** metadata and required sections are valid.
- **Contract conformant:** inputs, outputs, failures, and non-guarantees are explicit.
- **Workflow conformant:** outputs can be consumed by named next skills.
- **Evidence conformant:** uncertainty and source verification states are preserved.
- **Release conformant:** automated checks pass and unresolved blockers are disclosed.

All 13 core research skills conform to Level 2, and the `using-humanities-superpowers` router conforms to Level 3.

## Version 2 extension

[Humanities Superpowers 2.0 — Fricturn](v2/README.md) extends this v1 base with interpretive friction, traceable scholarly judgment, evidential standing, gate validity, and epistemic return. The v1 vocabulary and objects remain backward compatible.
