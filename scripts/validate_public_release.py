#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / 'MANIFEST.json'
TEXT_EXTENSIONS = {'.md', '.yml', '.yaml', '.json', '.toml', '.txt', '.py', '.cff', '.mdc', '.sh', '.svg', '.xml', '.html', '.css', '.js'}
REQUIRED = [
    'mkdocs.yml', 'site/requirements.txt', '.github/workflows/pages.yml',
    '.github/pull_request_template.md', '.github/ISSUE_TEMPLATE/bug_report.yml',
    '.github/ISSUE_TEMPLATE/skill_proposal.yml',
    'docs/release/RELEASE_NOTES_v1.0.0.md',
    'docs/release/PUBLIC_RELEASE_CHECKLIST.md', 'site/docs/index.md',
    'site/docs/quick-start.md', 'site/docs/skills.md', 'LICENSE',
    'CITATION.cff', 'README.md', 'README.ko.md', 'INSTALLATION.md',
    'MANIFEST.json',
]
ROUTER = 'using-humanities-superpowers'


def release_files() -> list[Path]:
    files = []
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or path == MANIFEST_PATH:
            continue
        if '.git' in path.parts or 'site-build' in path.parts:
            continue
        if path.name == 'VALIDATION_REPORT.txt':
            continue
        files.append(path)
    return files


def canonical_bytes(path: Path) -> bytes:
    """Return release bytes with Git's required LF policy applied to text files."""
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_EXTENSIONS or path.name in {'.gitignore', '.gitattributes', 'LICENSE'}:
        data = data.replace(b'\r\n', b'\n')
    return data


def manifest_data() -> dict:
    files = []
    for path in release_files():
        data = canonical_bytes(path)
        files.append({
            'path': path.relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(data).hexdigest(),
            'bytes': len(data),
        })
    return {
        'name': 'humanities-superpowers',
        'version': '1.0.0',
        'file_count': len(files),
        'files': files,
    }


def update_manifest() -> int:
    payload = json.dumps(manifest_data(), ensure_ascii=False, indent=2) + '\n'
    MANIFEST_PATH.write_bytes(payload.encode('utf-8'))
    print(f'UPDATED: MANIFEST.json ({len(manifest_data()["files"])} files)')
    return 0


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f'missing: {rel}')

    seen: dict[str, str] = {}
    for path in release_files():
        rel = path.relative_to(ROOT).as_posix()
        folded = rel.casefold()
        if folded in seen and seen[folded] != rel:
            errors.append(f'case-colliding paths: {seen[folded]} and {rel}')
        seen[folded] = rel

    for path in release_files():
        if path.suffix.lower() not in TEXT_EXTENSIONS or 'scripts' in path.parts:
            continue
        text = path.read_text(encoding='utf-8', errors='strict')
        for token in [
            'GITHUB_USERNAME', 'AUTHOR_NAME', 'AFFILIATION',
            'email@example.com', 'maintainer replaces this placeholder',
            '1.0.0-draft.1', '0.9.0-preview',
        ]:
            if token in text:
                errors.append(f'placeholder or stale release token {token!r}: {path.relative_to(ROOT)}')

    for path in [
        ROOT / '.github/ISSUE_TEMPLATE/bug_report.yml',
        ROOT / '.github/ISSUE_TEMPLATE/skill_proposal.yml',
        ROOT / '.github/workflows/pages.yml', ROOT / 'mkdocs.yml',
    ]:
        try:
            yaml.safe_load(path.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'invalid yaml {path.relative_to(ROOT)}: {exc}')

    skill_files = sorted((ROOT / 'skills').glob('*/SKILL.md'))
    names = {path.parent.name for path in skill_files}
    core_names = names - {ROUTER}
    if len(skill_files) != 14 or len(core_names) != 13 or ROUTER not in names:
        errors.append(
            f'expected 14 SKILL.md files (13 core research skills and 1 router); '
            f'found {len(skill_files)} files, {len(core_names)} core skills, router={ROUTER in names}'
        )
    for skill_file in skill_files:
        text = skill_file.read_text(encoding='utf-8')
        match = re.search(r'^version:\s*([^\s]+)', text, re.MULTILINE)
        if not match:
            errors.append(f'missing skill version: {skill_file.relative_to(ROOT)}')
        elif match.group(1) != '1.0.0':
            errors.append(f'skill version is not 1.0.0: {skill_file.relative_to(ROOT)} ({match.group(1)})')

    for path in [
        ROOT / 'project.json', ROOT / '.codex-plugin/plugin.json',
        ROOT / '.claude-plugin/plugin.json', ROOT / '.cursor-plugin/plugin.json',
    ]:
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            if data.get('version') != '1.0.0':
                errors.append(f'version is not 1.0.0: {path.relative_to(ROOT)}')
        except Exception as exc:
            errors.append(f'invalid json {path.relative_to(ROOT)}: {exc}')

    citation = (ROOT / 'CITATION.cff').read_text(encoding='utf-8')
    for value in ['version: 1.0.0', 'family-names: "Lee"', 'given-names: "Yong Wook"', 'license: MIT']:
        if value not in citation:
            errors.append(f'CITATION.cff missing expected metadata: {value}')

    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    readme_ko = (ROOT / 'README.ko.md').read_text(encoding='utf-8')
    installation = (ROOT / 'INSTALLATION.md').read_text(encoding='utf-8')
    public_phrases = [
        (readme, '13 core research skills + 1 Level 3 router', 'README.md'),
        (readme, '**Tested:** Claude Code and OpenAI Codex.', 'README.md'),
        (readme, 'not yet independently verified:** Cursor.', 'README.md'),
        (readme_ko, '13개 핵심 연구 스킬 + 1개 Level 3 라우터', 'README.ko.md'),
        (readme_ko, '독립적인 로딩 검증은 미완료:** Cursor.', 'README.ko.md'),
        (installation, 'Do not create `skills/skills/`', 'INSTALLATION.md'),
    ]
    for text, phrase, rel in public_phrases:
        if phrase not in text:
            errors.append(f'{rel} missing required public-release wording: {phrase}')

    try:
        listed_manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
        expected_manifest = manifest_data()
        listed = {item['path']: item for item in listed_manifest['files']}
        expected = {item['path']: item for item in expected_manifest['files']}
        for rel, item in expected.items():
            if rel not in listed:
                errors.append(f'manifest missing file: {rel}')
            elif listed[rel].get('sha256') != item['sha256'] or listed[rel].get('bytes') != item['bytes']:
                errors.append(f'manifest mismatch: {rel}')
        for rel in sorted(set(listed) - set(expected)):
            errors.append(f'manifest lists absent file: {rel}')
        if listed_manifest.get('file_count') != expected_manifest['file_count']:
            errors.append(
                f'manifest file_count {listed_manifest.get("file_count")} '
                f'!= {expected_manifest["file_count"]}'
            )
        if listed_manifest.get('version') != '1.0.0':
            errors.append('MANIFEST.json version is not 1.0.0')
    except Exception as exc:
        errors.append(f'invalid MANIFEST.json: {exc}')

    if errors:
        print('FAIL: public release validation')
        print('\n'.join('- ' + error for error in errors))
        return 1
    print('PASS: public release versions, counts, compatibility wording, metadata, and manifest')
    return 0


if __name__ == '__main__':
    if sys.argv[1:] == ['--update-manifest']:
        raise SystemExit(update_manifest())
    if sys.argv[1:]:
        print('Usage: python3 scripts/validate_public_release.py [--update-manifest]')
        raise SystemExit(2)
    raise SystemExit(main())
