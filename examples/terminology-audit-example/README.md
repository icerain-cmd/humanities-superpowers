# Terminology-audit example

This example demonstrates `checking-terminology-consistency` on a manuscript that alternates among related but non-identical terms.

## Input problem

The draft uses *mediation*, *intermediation*, *remediation*, and *platform mediation* as though they were interchangeable.

## Audit output

| Preferred term | Operational meaning | Exclude | Related terms | Action |
|---|---|---|---|---|
| mediation | A process through which form, access, or interpretation is shaped by a medium or institutional arrangement. | Simple transmission without transformation. | intermediation, remediation | Retain as the umbrella term. |
| platform mediation | Mediation performed through platform-specific ranking, interface, data, and governance arrangements. | All digital mediation. | algorithmic mediation | Use only where platform-specific mechanisms are demonstrated. |
| remediation | The refashioning of one medium within another medium. | Any form of mediation. | representation, adaptation | Reserve for explicitly intermedial cases. |
| intermediation | An intermediary actor or layer positioned between parties or processes. | General interpretive shaping. | brokerage, mediation | Replace unless an intermediary function is analytically central. |

## Consistency decisions

1. Replace generic uses of *intermediation* with *mediation*.
2. Keep *remediation* only where one medium refashions another.
3. Require a named platform mechanism before using *platform mediation*.
4. Record translation choices and exceptions in the terminology ledger.

## Stop signal

If the author cannot explain why two terms are distinct, the agent must not preserve both merely for stylistic variety.
