# Quick Start

## Clone

```bash
git clone https://github.com/icerain-cmd/humanities-superpowers.git
cd humanities-superpowers
```

## Ask your agent

Install the framework using the tested project layout in the [Installation Guide](installation.md), then ask:

```text
Use Humanities Superpowers to turn my broad topic about platform interfaces
and cultural memory into a precise research question. Do not invent sources.
```

The orchestrator should diagnose the current research state, select the smallest sufficient skill path, and return a gate result.

## Expected behavior

A valid result includes:

- the current research state;
- the selected skill;
- missing inputs;
- a structured output;
- `PASS`, `CONDITIONAL PASS`, or `FAIL`;
- the next valid action;
- any researcher decision that cannot be delegated.

## Validate the repository

```bash
python3 scripts/validate_repository.py
python3 scripts/run_integrated_tests.py
python3 scripts/validate_public_release.py
```

On Windows, use `python` instead of `python3` if that is the available launcher.
