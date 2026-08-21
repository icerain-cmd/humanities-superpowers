# Installation

> Paths beginning with `/EXAMPLE/PATH` are illustrative. Do not copy them literally without replacing the source path.

Humanities Superpowers contains 13 core research skills and 1 Level 3 router. Project-local installation is recommended for a first test because it is isolated, reviewable, and easy to remove. User-level installation makes the skills available across projects but depends on the current conventions of each agent harness.

## Verification status

Tested:

- Claude Code
- OpenAI Codex

Installation guidance provided, but not yet independently verified:

- Cursor

Other Markdown-capable agents may use the skills manually, but compatibility is not guaranteed.

## Claude Code

Use this project-local layout:

```text
project/
├── CLAUDE.md
└── .claude/
    └── skills/
        ├── using-humanities-superpowers/
        │   └── SKILL.md
        └── ...13 core skill directories...
```

Install from a local clone:

```bash
mkdir -p .claude/skills
cp -R /EXAMPLE/PATH/humanities-superpowers/skills/* .claude/skills/
cp /EXAMPLE/PATH/humanities-superpowers/CLAUDE.md ./CLAUDE.md
```

For a user-level installation, copy the skill directories into the current Claude Code user skills directory. Consult the current Claude Code documentation before doing so; global paths can change. Keep `CLAUDE.md` in a project root when project-level routing rules are desired.

## OpenAI Codex

Use this project-local layout:

```text
project/
├── AGENTS.md
└── .agents/
    └── skills/
        ├── using-humanities-superpowers/
        │   └── SKILL.md
        └── ...13 core skill directories...
```

Install from a local clone:

```bash
mkdir -p .agents/skills
cp -R /EXAMPLE/PATH/humanities-superpowers/skills/* .agents/skills/
cp /EXAMPLE/PATH/humanities-superpowers/AGENTS.md ./AGENTS.md
```

Codex reads `AGENTS.md` for project-level instructions. For a user-level installation, use the current Codex user-skills location rather than guessing a global path.

## Cursor

The repository provides this rule:

```text
.cursor/rules/humanities-superpowers.mdc
```

The rule refers to `skills/using-humanities-superpowers/SKILL.md`, so the guidance-only project layout is:

```text
project/
├── skills/
│   ├── using-humanities-superpowers/
│   │   └── SKILL.md
│   └── ...13 core skill directories...
└── .cursor/
    └── rules/
        └── humanities-superpowers.mdc
```

Copy the rule and `skills/` directory into the target project, then verify that your Cursor version loads the rule and can open the router. This route has not yet been independently verified in a target Cursor environment.

## Avoid nested installation

Copy the *contents* of the repository's `skills/` directory into the harness skill directory. Do not create `skills/skills/` accidentally. After installation, paths should end in `<skill-name>/SKILL.md`, not `skills/<skill-name>/skills/SKILL.md`.

## Verify the installed files

For Claude Code, run:

```bash
find .claude/skills -type f -name SKILL.md | sort
find .claude/skills -type f -name SKILL.md | wc -l
```

For Codex, replace `.claude/skills` with `.agents/skills`. The expected result is 14 `SKILL.md` files: 13 core research skills and the `using-humanities-superpowers` router.

PowerShell users can count them with:

```powershell
(Get-ChildItem .agents/skills -Recurse -Filter SKILL.md).Count
```

## First run

Use a minimal prompt that requires the router to expose uncertainty:

```text
Use Humanities Superpowers to diagnose the current research state.
Do not invent missing sources. Return a routing decision and gate result.
```

A valid installation should make `using-humanities-superpowers` visible and preserve missing inputs instead of fabricating them.

## Safe read-only pilot

Do not begin with the only copy of a manuscript. Keep the source unchanged and write agent outputs elsewhere:

```text
pilot/
├── original/   # unchanged source copy
├── working/    # disposable working copy
└── output/     # gate reports and proposed revisions
```

Tell the agent that `original/` is read-only and that every proposed change must go to `working/` or `output/`.

## Validate the framework clone

Run the repository checks from the Humanities Superpowers clone:

```bash
python3 -m pip install -r requirements-validation.txt
python3 scripts/validate_repository.py
python3 scripts/run_integrated_tests.py
python3 scripts/validate_public_release.py
```

On Windows, use `python` instead of `python3` if that is the available launcher.

The worked example intentionally returns `FAIL` when its source set is unverified. That result must not be changed to make validation appear successful.

## Direct repository use

You may keep the framework beside a research project and instruct an agent to read `skills/<name>/SKILL.md` directly. This is portable but provides less automatic discovery.

## Version caution

Agent installation paths and plugin formats can change. Recheck current official harness documentation before publishing installation claims or changing a user-level setup.
