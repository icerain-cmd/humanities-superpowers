# Installation

Humanities Superpowers is a repository of Agent Skills and supporting project instructions. Installation differs by agent harness.

## Claude Code

Claude Code discovers project skills from:

```text
.claude/skills/<skill-name>/SKILL.md
```

For a project-local installation:

```bash
mkdir -p .claude/skills
cp -R /path/to/humanities-superpowers/skills/* .claude/skills/
```

For a user-level installation, copy the skills into your Claude skills directory according to the current Claude Code documentation. Keep `CLAUDE.md` in the project root when project-level routing rules are desired.

## Codex

Codex discovers repository skills under:

```text
.agents/skills/<skill-name>/SKILL.md
```

Install them into a research repository:

```bash
mkdir -p .agents/skills
cp -R /path/to/humanities-superpowers/skills/* .agents/skills/
cp /path/to/humanities-superpowers/AGENTS.md ./AGENTS.md
```

Codex reads `AGENTS.md` before work and uses it for project-level instructions.

## Cursor

The repository includes a project rule at:

```text
.cursor/rules/humanities-superpowers.mdc
```

Copy the rule and skills into the target project. Cursor compatibility may depend on the current agent and rules implementation; verify loading in the version you use.

## Direct repository use

You may also clone the repository beside a research project and instruct an agent to read the relevant `skills/<name>/SKILL.md`. This is portable but provides less automatic discovery.

## Verification after installation

Ask the agent:

```text
Use Humanities Superpowers to diagnose the current research state.
Do not invent missing sources. Return a routing decision and gate result.
```

A valid installation should make the orchestrator visible and should preserve missing inputs instead of fabricating them.

## Version caution

Agent harness installation paths and plugin formats can change. Before publishing a release, compare this guide against the current official Claude Code, Codex, and Cursor documentation.
