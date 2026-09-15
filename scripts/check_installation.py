#!/usr/bin/env python3
"""Install smoke test for the documented project-local procedures.

The repository validator proves the *repository* is internally consistent.
This check verifies the *installed* result instead: it executes the fenced
commands published in INSTALLATION.md inside a throwaway project directory and
asserts that every path the installed skills and instruction files refer to
actually exists there. A repository that passes validation can still install
into a project whose skills point at directories that were never copied.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLATION = ROOT / "INSTALLATION.md"
SOURCE_PLACEHOLDER = "/EXAMPLE/PATH/humanities-superpowers"
EXPECTED_SKILLS = 14

# Section heading -> (skill directory, instruction file, extra pre-existing files)
HARNESSES = {
    "OpenAI Codex": {
        "skills": Path(".agents/skills"),
        "instruction": Path("AGENTS.md"),
        "protect": [Path("AGENTS.md")],
    },
    "Claude Code": {
        "skills": Path(".claude/skills"),
        "instruction": Path("CLAUDE.md"),
        "protect": [Path("CLAUDE.md")],
    },
    "Cursor": {
        "skills": Path("skills"),
        "instruction": Path(".cursor/rules/humanities-superpowers.mdc"),
        "protect": [],
    },
}

SENTINEL = "PRE-EXISTING PROJECT INSTRUCTIONS - MUST SURVIVE INSTALL"
ARTIFACT_REFERENCE = re.compile(r"`((?:templates|schemas)/[A-Za-z0-9._/-]+)`")
SKILL_REFERENCE = re.compile(r"`?((?:\.agents/skills|\.claude/skills|skills)/[a-z0-9-]+/SKILL\.md)`?")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")


def section(text: str, heading: str) -> str:
    start = text.find(f"## {heading}")
    if start < 0:
        raise SystemExit(f"INSTALLATION.md is missing the '## {heading}' section")
    rest = text[start + len(heading) + 3 :]
    end = rest.find("\n## ")
    return rest if end < 0 else rest[:end]


def documented_commands(heading: str) -> list[str]:
    body = section(INSTALLATION.read_text(encoding="utf-8"), heading)
    blocks = re.findall(r"```bash\n(.*?)```", body, re.DOTALL)
    return [block.replace(SOURCE_PLACEHOLDER, str(ROOT)) for block in blocks]


def populated_before_run(project: Path, protect: list[Path]) -> dict[Path, str]:
    originals: dict[Path, str] = {}
    for relative in protect:
        target = project / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative.suffix == ".md" and relative.name in {"AGENTS.md", "CLAUDE.md"}:
            content = f"{SENTINEL}\n"
        elif relative.suffix == ".md":
            content = "# Existing project guidance\n\nKeep me.\n"
        else:
            content = "---\ndescription: pre-existing project rule\n---\n\nKeep me.\n"
        target.write_text(content, encoding="utf-8")
        originals[relative] = content
    return originals


def run_documented_install(name: str, project: Path, errors: list[str]) -> bool:
    blocks = documented_commands(name)
    if not blocks:
        errors.append(f"[{name}] publishes no runnable install command to verify")
        return False
    for block in blocks:
        result = subprocess.run(
            ["bash", "-e", "-c", block],
            cwd=project,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            detail = (result.stderr or result.stdout).strip().splitlines()[:1]
            errors.append(f"[{name}] documented install command failed: {detail}")
            return False
    return True


def check_fresh_project(name: str, spec: dict, errors: list[str]) -> None:
    """A clean project must receive every path the installed artifacts refer to."""
    project = Path(tempfile.mkdtemp(prefix=f"hsp-fresh-{name.split()[0].lower()}-"))
    try:
        if not run_documented_install(name, project, errors):
            return

        skill_dir = project / spec["skills"]
        installed = sorted(skill_dir.glob("*/SKILL.md"))
        if len(installed) != EXPECTED_SKILLS:
            errors.append(f"[{name}] expected {EXPECTED_SKILLS} installed SKILL.md files, found {len(installed)}")
        router = skill_dir / "using-humanities-superpowers" / "SKILL.md"
        if not router.is_file():
            errors.append(f"[{name}] router not found at {spec['skills']}/using-humanities-superpowers/SKILL.md")
        if (project / "skills" / "skills").exists():
            errors.append(f"[{name}] nested skills/skills directory created")

        for skill in installed:
            text = skill.read_text(encoding="utf-8")
            for raw in ARTIFACT_REFERENCE.findall(text):
                if not (project / raw).exists():
                    errors.append(
                        f"[{name}] {skill.relative_to(project)} refers to {raw}, "
                        f"which the documented install never copies"
                    )
            for raw in MARKDOWN_LINK.findall(text):
                target = raw.split("#", 1)[0].strip("<>")
                if not target or not (skill.parent / target).exists():
                    errors.append(f"[{name}] {skill.relative_to(project)}: broken relative link -> {raw}")

        instruction = spec["instruction"]
        if instruction:
            path = project / instruction
            if not path.is_file():
                errors.append(f"[{name}] instruction file {instruction} was not installed")
            else:
                text = path.read_text(encoding="utf-8")
                named = {Path(raw) for raw in SKILL_REFERENCE.findall(text)}
                harness_router = spec["skills"] / "using-humanities-superpowers" / "SKILL.md"
                if not named:
                    errors.append(f"[{name}] {instruction} never names a router path")
                elif harness_router not in named:
                    errors.append(
                        f"[{name}] {instruction} does not name this layout's router path ({harness_router})"
                    )
                elif not (project / harness_router).is_file():
                    errors.append(
                        f"[{name}] {instruction} names {harness_router}, which the install never created"
                    )
    finally:
        shutil.rmtree(project, ignore_errors=True)


def check_existing_instruction_files(name: str, spec: dict, errors: list[str]) -> None:
    """A project that already has instruction files must not have them destroyed."""
    if not spec["protect"]:
        return
    project = Path(tempfile.mkdtemp(prefix=f"hsp-existing-{name.split()[0].lower()}-"))
    try:
        originals = populated_before_run(project, spec["protect"])
        if not run_documented_install(name, project, errors):
            return
        for relative, content in originals.items():
            path = project / relative
            if not path.is_file():
                errors.append(f"[{name}] documented install removed pre-existing {relative}")
            elif path.read_text(encoding="utf-8") != content:
                errors.append(
                    f"[{name}] documented install overwrote pre-existing {relative} "
                    f"instead of instructing a merge"
                )
    finally:
        shutil.rmtree(project, ignore_errors=True)


def main() -> int:
    errors: list[str] = []
    for name, spec in HARNESSES.items():
        check_fresh_project(name, spec, errors)
        check_existing_instruction_files(name, spec, errors)
    if errors:
        print("FAIL: install smoke test")
        for error in errors:
            print("- " + error)
        return 1
    print(
        "PASS: documented project-local installs reproduce 14 skills, resolvable "
        "template/schema references, a router path that exists, and pre-existing "
        "instruction files left intact"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
