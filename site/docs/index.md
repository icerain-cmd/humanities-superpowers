# Humanities Superpowers

**Not an AI paper writer. A scholarly judgment scaffold.**

Humanities Superpowers is a set of structured research skills, research contracts, and quality gates for scholars using AI agents.

It is designed to reduce the risk that fluent AI output is mistaken for verified scholarship. It does not replace the researcher. It makes research decisions, missing evidence, unresolved objections, citation status, and submission blockers more visible.

The repository contains 13 core research skills and 1 Level 3 router. Claude Code and OpenAI Codex have been tested; Cursor installation guidance is provided but has not yet been independently verified.

## What it changes

Most AI writing workflows move forward continuously:

```text
prompt → prose → polish → submit
```

Humanities Superpowers uses a different logic:

```text
question → scope → sources → interpretation → argument
         → stress test → citation audit → review → submission gate
```

A failed gate is not hidden. The workflow pauses, requests a researcher decision, or rolls back to the earliest stage that caused the problem.

## Core promise

The framework does **not** promise truth, originality, publication, or error-free citations. It instead makes a narrower and observable discipline explicit:

- unknown information remains marked as unknown;
- claims are not silently widened beyond available evidence;
- interpretation is not relabeled as fact;
- citation existence and claim support are checked separately;
- submission readiness cannot be declared while blocking issues remain.

## Start here

1. Read the [Quick Start](quick-start.md).
2. Install the skills for your agent using the [Installation Guide](installation.md).
3. Try the [end-to-end example](examples.md).
4. Read the [methodology](methodology.md) before adapting or contributing skills.
