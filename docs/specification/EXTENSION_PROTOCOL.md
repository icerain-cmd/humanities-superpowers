# Extension Protocol

## 1. Purpose

The extension protocol allows contributors to propose new skills without turning the repository into an uncurated prompt collection.

## 2. Admission test

A proposed skill MUST answer:

1. What recurring scholarly decision does it support?
2. Why is that decision not already covered by an existing skill?
3. What research objects does it accept and produce?
4. What failure conditions must it preserve?
5. How can its completion criteria be observed?
6. What discipline-specific assumptions does it make?

A proposal that only changes tone, formatting, or subject matter SHOULD be an example or profile, not a new core skill.

## 3. Skill classes

- **Core:** broadly applicable and required for the canonical workflow.
- **Discipline profile:** adapts a core skill for a field without weakening safeguards.
- **Workflow skill:** coordinates existing skills.
- **Utility:** performs formatting or file operations but does not make scholarly judgments.
- **Experimental:** promising but not yet validated across cases.

## 4. Naming

Names MUST use an action-oriented gerund phrase in kebab case, such as `mapping-concept-lineage`. Names SHOULD identify the scholarly operation rather than a desired outcome like `writing-a-great-paper`.

## 5. Required proposal artifacts

- completed skill contract;
- at least four invocation tests;
- one missing-input failure example;
- one adversarial example;
- one output artifact;
- compatibility note;
- known limitations;
- license declaration.

## 6. Core promotion

An extension may become core only after:

- use in at least two distinct humanities contexts;
- no unresolved overlap with an existing skill;
- Level 4 conformance;
- documentation and maintenance commitment;
- maintainer review.

## 7. Deprecation

Deprecated skills MUST name a replacement or explain why the operation is no longer supported. Removal requires a major version unless the skill is explicitly experimental.
