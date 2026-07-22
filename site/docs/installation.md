# Installation

Humanities Superpowers contains 13 core research skills and 1 Level 3 router. Project-local installation is recommended for a first test because it is isolated, reviewable, and easy to remove. User-level installation makes the skills available across projects but depends on the current conventions of each agent harness.

## Verification status

Tested:

- Claude Code
- OpenAI Codex

Installation guidance provided, but not yet independently verified:

- Cursor

Other Markdown-capable agents may use the skills manually, but compatibility is not guaranteed.

## Claude Code

```text
project/
├── CLAUDE.md
└── .claude/
    └── skills/
        ├── using-humanities-superpowers/
        │   └── SKILL.md
        └── ...13 core skill directories...
```

```bash
mkdir -p .claude/skills
cp -R /EXAMPLE/PATH/humanities-superpowers/skills/* .claude/skills/
cp /EXAMPLE/PATH/humanities-superpowers/CLAUDE.md ./CLAUDE.md
```

For a user-level installation, consult the current Claude Code documentation before copying the skills into its user directory.

## OpenAI Codex

```text
project/
├── AGENTS.md
└── .agents/
    └── skills/
        ├── using-humanities-superpowers/
        │   └── SKILL.md
        └── ...13 core skill directories...
```

```bash
mkdir -p .agents/skills
cp -R /EXAMPLE/PATH/humanities-superpowers/skills/* .agents/skills/
cp /EXAMPLE/PATH/humanities-superpowers/AGENTS.md ./AGENTS.md
```

Codex reads `AGENTS.md` for project-level instructions. Use the current Codex documentation before changing a user-level setup.

## Cursor

The repository provides `.cursor/rules/humanities-superpowers.mdc`. That rule refers to `skills/using-humanities-superpowers/SKILL.md`, so copy both the rule and the repository's `skills/` directory into the project. Then verify that your Cursor version loads the rule and can open the router. This route has not yet been independently verified in a target Cursor environment.

## Avoid nested installation

Copy the *contents* of the repository's `skills/` directory into the harness skill directory. Do not create `skills/skills/`. Paths should end in `<skill-name>/SKILL.md`.

## Verify the installed files

```bash
find .claude/skills -type f -name SKILL.md | sort
find .claude/skills -type f -name SKILL.md | wc -l
```

For Codex, replace `.claude/skills` with `.agents/skills`. Expect 14 `SKILL.md` files: 13 core research skills and the `using-humanities-superpowers` router.

PowerShell users can run:

```powershell
(Get-ChildItem .agents/skills -Recurse -Filter SKILL.md).Count
```

## First run

```text
Use Humanities Superpowers to diagnose the current research state.
Do not invent missing sources. Return a routing decision and gate result.
```

## Safe read-only pilot

Keep the only copy of a manuscript outside the agent's write area:

```text
pilot/
├── original/   # unchanged source copy
├── working/    # disposable working copy
└── output/     # gate reports and proposed revisions
```

Tell the agent that `original/` is read-only.

## Validate the framework clone

```bash
python3 scripts/validate_repository.py
python3 scripts/run_integrated_tests.py
python3 scripts/validate_public_release.py
```

On Windows, use `python` instead of `python3` if that is the available launcher.

The worked example intentionally returns `FAIL` when its source set is unverified. Do not change that result to make validation appear successful.

## Direct repository use

You may keep the framework beside a research project and instruct an agent to read `skills/<name>/SKILL.md` directly. This is portable but provides less automatic discovery.
