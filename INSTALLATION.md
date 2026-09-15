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
├── templates/          # runtime artifacts referenced by the skills
├── schemas/
└── .claude/
    └── skills/
        ├── using-humanities-superpowers/
        │   └── SKILL.md
        └── ...13 core skill directories...
```

Install from a local clone:

```bash
mkdir -p .claude/skills templates schemas vendor/obra-superpowers docs/specification/dual-core
cp -R /EXAMPLE/PATH/humanities-superpowers/skills/* .claude/skills/
cp -R /EXAMPLE/PATH/humanities-superpowers/templates/* templates/
cp -R /EXAMPLE/PATH/humanities-superpowers/schemas/* schemas/
cp -R /EXAMPLE/PATH/humanities-superpowers/vendor/obra-superpowers/* vendor/obra-superpowers/
cp -R /EXAMPLE/PATH/humanities-superpowers/docs/specification/dual-core/* docs/specification/dual-core/
# Never overwrite an existing instruction file.
if [ -e CLAUDE.md ]; then
  echo "CLAUDE.md already exists: append the Humanities Superpowers block instead (see 'Existing instruction files')."
else
  cp /EXAMPLE/PATH/humanities-superpowers/CLAUDE.md ./CLAUDE.md
fi
```

Skills and the router name the framework's `templates/`, `schemas/`, `vendor/obra-superpowers/`, and `docs/specification/dual-core/` artifacts by project-root-relative path, so those directories must be installed at the same relative locations. They are guidance text, schemas, a vendored third-party skill set, and its provenance record — not executable tooling.

For a user-level installation, copy the skill directories into the current Claude Code user skills directory. Consult the current Claude Code documentation before doing so; global paths can change. Keep `CLAUDE.md` in a project root when project-level routing rules are desired.

## OpenAI Codex

Use this project-local layout:

```text
project/
├── AGENTS.md
├── templates/          # runtime artifacts referenced by the skills
├── schemas/
└── .agents/
    └── skills/
        ├── using-humanities-superpowers/
        │   └── SKILL.md
        └── ...13 core skill directories...
```

Install from a local clone:

```bash
mkdir -p .agents/skills templates schemas vendor/obra-superpowers docs/specification/dual-core
cp -R /EXAMPLE/PATH/humanities-superpowers/skills/* .agents/skills/
cp -R /EXAMPLE/PATH/humanities-superpowers/templates/* templates/
cp -R /EXAMPLE/PATH/humanities-superpowers/schemas/* schemas/
cp -R /EXAMPLE/PATH/humanities-superpowers/vendor/obra-superpowers/* vendor/obra-superpowers/
cp -R /EXAMPLE/PATH/humanities-superpowers/docs/specification/dual-core/* docs/specification/dual-core/
# Never overwrite an existing instruction file.
if [ -e AGENTS.md ]; then
  echo "AGENTS.md already exists: append the Humanities Superpowers block instead (see 'Existing instruction files')."
else
  cp /EXAMPLE/PATH/humanities-superpowers/AGENTS.md ./AGENTS.md
fi
```

Skills and the router name the framework's `templates/`, `schemas/`, `vendor/obra-superpowers/`, and `docs/specification/dual-core/` artifacts by project-root-relative path, so those directories must be installed at the same relative locations.

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
├── templates/
├── schemas/
└── .cursor/
    └── rules/
        └── humanities-superpowers.mdc
```

```bash
mkdir -p skills templates schemas vendor/obra-superpowers docs/specification/dual-core .cursor/rules
cp -R /EXAMPLE/PATH/humanities-superpowers/skills/* skills/
cp -R /EXAMPLE/PATH/humanities-superpowers/templates/* templates/
cp -R /EXAMPLE/PATH/humanities-superpowers/schemas/* schemas/
cp -R /EXAMPLE/PATH/humanities-superpowers/vendor/obra-superpowers/* vendor/obra-superpowers/
cp -R /EXAMPLE/PATH/humanities-superpowers/docs/specification/dual-core/* docs/specification/dual-core/
cp /EXAMPLE/PATH/humanities-superpowers/.cursor/rules/humanities-superpowers.mdc .cursor/rules/
```

Copy the rule, the `skills/` directory, the vendored engineering core, and the artifacts the skills reference, then verify that your Cursor version loads the rule and can open the router. This route has not yet been independently verified in a target Cursor environment.

## Existing instruction files

`AGENTS.md` and `CLAUDE.md` are generic project-instruction names. A project may already contain one, and replacing it would destroy the researcher's own instructions. The install commands above therefore copy these files only when they are absent.

```text
no existing file -> create it from the framework
existing file    -> never overwrite
                 -> append only the Humanities Superpowers block
```

The framework's `AGENTS.md` and `CLAUDE.md` carry the same eight harness-neutral rules, so an existing file can be extended instead of replaced: add those rules after your own instructions, and adjust the router path to the layout you installed.

This release deliberately ships no automatic merge tool. Merge by hand and keep your own instructions first. Skill directories, by contrast, are framework-owned: copying the framework's skills over an earlier copy is the intended upgrade path, and only the two generic instruction files need the guard.

## Avoid nested installation

Copy the *contents* of the repository's `skills/`, `templates/`, `schemas/`, `vendor/obra-superpowers/`, and `docs/specification/dual-core/` directories into the target directories. Do not create `skills/skills/`, `templates/templates/`, `schemas/schemas/`, or `vendor/obra-superpowers/obra-superpowers/` accidentally. After installation, paths should end in `<skill-name>/SKILL.md`, not `skills/<skill-name>/skills/SKILL.md`.

`cp -R source/templates templates` copies the directory *into* an existing `templates/`. Create the target directory first and copy its contents, as the commands above do.

## Verify the installed files

For Claude Code, run:

```bash
find .claude/skills -type f -name SKILL.md | sort
find .claude/skills -type f -name SKILL.md | wc -l
```

For Codex, replace `.claude/skills` with `.agents/skills`. The expected result is 14 `SKILL.md` files: 13 core research skills and the `using-humanities-superpowers` router.

Then confirm that the artifacts the skills and the router reference are present in the project. Any missing path is reported as a line beginning with `MISSING`:

```bash
grep -rho '`\(templates\|schemas\|vendor\)/[A-Za-z0-9._/-]*`' .agents/skills | tr -d '`' | sort -u | while read -r artifact; do [ -e "$artifact" ] || echo "MISSING: $artifact"; done
```

Substitute `.claude/skills` or `skills` for `.agents/skills` when you installed one of the other layouts.

The installed project should contain the 14 Humanities skills, the vendored engineering core under `vendor/obra-superpowers/skills/`, its `PROVENANCE.json`, and the dual-core specification under `docs/specification/dual-core/`. The vendored files are an unmodified third-party import; edit them only in the upstream project, never in a installed project.

These verification commands, like the install commands above, need a POSIX shell (Linux, macOS, WSL, or Git Bash on Windows). On native Windows PowerShell, compare the names the skills reference against the files in `templates/` and `schemas/`, or run `python3 scripts/check_installation.py` from the framework clone inside WSL or Git Bash.

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
python3 scripts/check_installation.py
```

On Windows, use `python` instead of `python3` if that is the available launcher.

The worked example intentionally returns `FAIL` when its source set is unverified. That result must not be changed to make validation appear successful.

`validate_repository.py` proves the repository is internally consistent. `check_installation.py` proves something different: it executes the documented commands in throwaway projects and fails when an installed skill or instruction file points at a path the procedure never copies. Repository validation passing is not by itself installation validation.

## Direct repository use

You may keep the framework beside a research project and instruct an agent to read `skills/<name>/SKILL.md` directly. This is portable but provides less automatic discovery.

## Version caution

Agent installation paths and plugin formats can change. Recheck current official harness documentation before publishing installation claims or changing a user-level setup.
