#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / 'MANIFEST.json'
PROJECT_VERSION = json.loads((ROOT / 'project.json').read_text(encoding='utf-8'))['version']
TEXT_EXTENSIONS = {'.md', '.yml', '.yaml', '.json', '.toml', '.txt', '.py', '.cff', '.mdc', '.sh', '.svg', '.xml', '.html', '.css', '.js'}

# The release contract this validator locks. A release promotion must update
# these pins deliberately; nothing else in the repository may drift silently.
RELEASE_VERSION = '2.1.0'
RELEASE_DATE = '2026-09-15'
VENDOR_REPOSITORY = 'https://github.com/obra/superpowers'
VENDOR_VERSION = '6.3.0'
VENDOR_COMMIT = 'b36e0829c6d0140e93cfef2ca599b1b07d4a7797'
VENDOR_SKILLS = 10
HUMANITIES_SKILLS = 14
WORKER_STATES = ('WORKING', 'WAITING_INPUT', 'WAITING_PRIVILEGE', 'BLOCKED', 'ERROR', 'DONE')
# Files that state what this release does. Effect claims are checked here.
CLAIM_FILES = [
    'README.md', 'README.ko.md', 'CHANGELOG.md',
    'docs/release/RELEASE_NOTES_v2.1.0.md', 'site/docs/dual-core.md',
    'docs/evaluation/EFFECTIVENESS_AND_OPERATING_POLICY.md',
    'docs/evaluation/TOOL_USE_BENCHMARK.md',
]
UNMEASURED_CLAIMS = [
    r'(?i)\bimproves?\s+coding\s+quality\b',
    r'(?i)\breduces?\s+defects?\b',
    r'(?i)\bsaves?\s+tokens?\b',
    r'(?i)\bproven\s+(?:coding|research)\s+quality\b',
    r'(?i)\bmeasured\s+improvement\b',
]
SECRET_PATTERNS = [
    r'sk-[A-Za-z0-9]{20,}',
    r'ghp_[A-Za-z0-9]{20,}',
    r'github_pat_[A-Za-z0-9_]{20,}',
    r'AKIA[0-9A-Z]{16}',
    r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
    r'xox[baprs]-[A-Za-z0-9-]{10,}',
    r'(?i)(?:api[_-]?key|client_secret|access_token|password)\s*[:=]\s*["\'][A-Za-z0-9/_+.-]{16,}["\']',
]
LOCAL_PATH_PATTERNS = [
    r'/(?:home|Users|mnt|srv|opt)/[^\s`)\]"\']*',
    r'[A-Za-z]:\\Users\\[^\s`)\]"\']*',
]
# Documented, intentional placeholders in INSTALLATION.md and its checker.
ALLOWED_PATH_LITERALS = ('/EXAMPLE/PATH', '/path/to/')

REQUIRED = [
    'mkdocs.yml', 'site/requirements.txt', 'requirements-validation.txt', '.github/workflows/pages.yml',
    '.github/pull_request_template.md', '.github/ISSUE_TEMPLATE/bug_report.yml',
    '.github/ISSUE_TEMPLATE/skill_proposal.yml',
    '.github/ISSUE_TEMPLATE/test_report.yml',
    '.github/ISSUE_TEMPLATE/methodological_criticism.yml',
    '.github/ISSUE_TEMPLATE/installation_problem.yml',
    'docs/release/RELEASE_NOTES_v1.0.0.md',
    'docs/release/RELEASE_NOTES_v2.0.0.md',
    'docs/release/RELEASE_NOTES_v2.1.0.md',
    'docs/release/PUBLIC_RELEASE_CHECKLIST.md', 'site/docs/index.md',
    'site/docs/quick-start.md', 'site/docs/skills.md', 'LICENSE',
    'CITATION.cff', 'README.md', 'README.ko.md', 'INSTALLATION.md',
    'MANIFEST.json',
]
ROUTER = 'using-humanities-superpowers'


def vendored_tree_hash(directory: Path) -> str:
    """Recompute one vendored skill tree hash with the documented definition."""
    digest = hashlib.sha256()
    for path in sorted(p for p in directory.rglob('*') if p.is_file()):
        relative = path.relative_to(directory).as_posix()
        digest.update(f'{relative}\0{hashlib.sha256(path.read_bytes()).hexdigest()}\n'.encode('utf-8'))
    return digest.hexdigest()


def text_release_files() -> list[Path]:
    return [
        path for path in release_files()
        if path.suffix.lower() in TEXT_EXTENSIONS or path.name in {'.gitignore', '.gitattributes'}
    ]


def validate_release_version(errors: list[str]) -> None:
    """The project release version is a pinned release decision, not a side effect."""
    if PROJECT_VERSION != RELEASE_VERSION:
        errors.append(f'project.json version is {PROJECT_VERSION}, expected release {RELEASE_VERSION}')
    for rel in ['project.json', 'MANIFEST.json', '.codex-plugin/plugin.json',
                '.claude-plugin/plugin.json', '.cursor-plugin/plugin.json']:
        try:
            data = json.loads((ROOT / rel).read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'{rel}: unreadable version source: {exc}')
            continue
        if data.get('version') != RELEASE_VERSION:
            errors.append(f'{rel} version is {data.get("version")!r}, expected {RELEASE_VERSION!r}')
    skill_versions = {
        path.relative_to(ROOT).as_posix(): match.group(1)
        for path in sorted((ROOT / 'skills').glob('*/SKILL.md'))
        if (match := re.search(r'^version:\s*([^\s]+)', path.read_text(encoding='utf-8'), re.MULTILINE))
    }
    wrong = {rel: version for rel, version in skill_versions.items() if version != RELEASE_VERSION}
    if wrong:
        errors.append(f'skill metadata not at release {RELEASE_VERSION}: {sorted(wrong.items())}')
    citation = (ROOT / 'CITATION.cff').read_text(encoding='utf-8')
    if f'version: {RELEASE_VERSION}' not in citation:
        errors.append(f'CITATION.cff does not declare version: {RELEASE_VERSION}')
    if f'date-released: {RELEASE_DATE}' not in citation:
        errors.append(f'CITATION.cff does not declare date-released: {RELEASE_DATE}')


def validate_release_documents(errors: list[str]) -> None:
    changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
    heading = f'## [{RELEASE_VERSION}] - {RELEASE_DATE}'
    if heading not in changelog:
        errors.append(f'CHANGELOG.md is missing the release heading {heading!r}')
    if '## [Unreleased]' in changelog:
        errors.append('CHANGELOG.md still carries an [Unreleased] section after the release promotion')
    notes = (ROOT / 'docs/release/RELEASE_NOTES_v2.1.0.md').read_text(encoding='utf-8')
    if not notes.startswith(f'# Humanities Superpowers v{RELEASE_VERSION} '):
        errors.append('v2.1.0 release notes do not open with their release identity')
    for token in ['NOT_MEASURED', 'RESEARCH', 'CODE', 'HYBRID', 'QUICK', 'STANDARD', 'STRICT']:
        if token not in notes:
            errors.append(f'v2.1.0 release notes are missing {token}')
    for rel in ['README.md', 'README.ko.md']:
        text = (ROOT / rel).read_text(encoding='utf-8')
        if RELEASE_VERSION not in text:
            errors.append(f'{rel} never names the release version {RELEASE_VERSION}')
        # The public statement is no longer "nothing was measured": an
        # evaluation exists. The README must therefore carry its conclusion and
        # the default policy, and must link the document that records both.
        if 'EXPERIMENTAL_ONLY' not in text:
            errors.append(f'{rel} does not state the evaluated status of the research core')
        if 'OFF' not in text:
            errors.append(f'{rel} does not state the default policy')
        if 'docs/evaluation/EFFECTIVENESS_AND_OPERATING_POLICY.md' not in text:
            errors.append(f'{rel} does not link the effectiveness and operating policy')


def validate_vendor_provenance(errors: list[str]) -> None:
    vendor = ROOT / 'vendor/obra-superpowers'
    try:
        provenance = json.loads((vendor / 'PROVENANCE.json').read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'vendor/obra-superpowers/PROVENANCE.json: unreadable: {exc}')
        return
    upstream = provenance.get('upstream', {})
    for field, expected in [
        ('repository', VENDOR_REPOSITORY), ('version', VENDOR_VERSION), ('commit', VENDOR_COMMIT),
    ]:
        if upstream.get(field) != expected:
            errors.append(
                f'vendored provenance {field} is {upstream.get(field)!r}, expected {expected!r}'
            )
    if 'MIT' not in str(upstream.get('license', '')):
        errors.append('vendored provenance does not record the upstream MIT license')
    imported = provenance.get('imported', {})
    if len(imported) != VENDOR_SKILLS:
        errors.append(f'vendored provenance records {len(imported)} skills, expected {VENDOR_SKILLS}')
    digest = hashlib.sha256()
    for name in sorted(imported):
        directory = vendor / 'skills' / name
        if not directory.is_dir():
            errors.append(f'vendored skill directory missing: {name}')
            continue
        actual = vendored_tree_hash(directory)
        if actual != imported[name].get('tree_sha256'):
            errors.append(f'vendored skill changed since import: {name}')
        digest.update(f'{name}\0{actual}\n'.encode('utf-8'))
    if digest.hexdigest() != provenance.get('aggregate_sha256'):
        errors.append('vendored aggregate hash does not match the recorded import')
    license_hash = hashlib.sha256((vendor / 'LICENSE').read_bytes()).hexdigest()
    if license_hash != provenance.get('license_sha256'):
        errors.append('vendored upstream LICENSE is not byte-identical to the recorded import')
    for item in provenance.get('excluded', []):
        if not item.get('reason'):
            errors.append(f"vendored exclusion without a reason: {item.get('skill')}")
    notices = (ROOT / 'THIRD_PARTY_NOTICES.md').read_text(encoding='utf-8')
    for token in [VENDOR_REPOSITORY, VENDOR_VERSION, VENDOR_COMMIT, 'PROVENANCE.json']:
        if token not in notices:
            errors.append(f'THIRD_PARTY_NOTICES.md is missing {token}')


def validate_release_hygiene(errors: list[str]) -> None:
    """Local artifacts, secrets, local paths, and unmeasured claims stay out."""
    for path in release_files():
        if path.suffix.lower() in {'.orig', '.rej'} or path.name.endswith(('.orig', '.rej')):
            errors.append(f'local merge artifact tracked in the release: {path.relative_to(ROOT)}')
    for pattern in LOCAL_PATH_PATTERNS:
        compiled = re.compile(pattern)
        for path in text_release_files():
            for number, line in enumerate(path.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
                for found in compiled.finditer(line):
                    if found.group(0).startswith(ALLOWED_PATH_LITERALS):
                        continue
                    errors.append(
                        f'{path.relative_to(ROOT)}:{number}: absolute local path in public release '
                        f'({found.group(0)!r})'
                    )
    for pattern in SECRET_PATTERNS:
        compiled = re.compile(pattern)
        for path in text_release_files():
            match = compiled.search(path.read_text(encoding='utf-8', errors='ignore'))
            if match:
                errors.append(f'{path.relative_to(ROOT)}: possible secret material ({pattern})')
    for rel in CLAIM_FILES:
        text = (ROOT / rel).read_text(encoding='utf-8')
        for pattern in UNMEASURED_CLAIMS:
            if re.search(pattern, text):
                errors.append(f'{rel}: claims an effect that was not measured ({pattern})')
    for rel in ['CHANGELOG.md', 'docs/release/RELEASE_NOTES_v2.1.0.md']:
        if 'NOT_MEASURED' not in (ROOT / rel).read_text(encoding='utf-8'):
            errors.append(f'{rel}: records no unmeasured-effect statement')


def validate_install_and_contract_inventory(errors: list[str]) -> None:
    installation = (ROOT / 'INSTALLATION.md').read_text(encoding='utf-8')
    for token in ['vendor/obra-superpowers', 'docs/specification/dual-core', '14 `SKILL.md` files']:
        if token not in installation:
            errors.append(f'INSTALLATION.md does not document {token}')
    worker = (ROOT / 'docs/specification/dual-core/AUTONOMOUS_WORKER.md').read_text(encoding='utf-8')
    for state in WORKER_STATES:
        if f'`{state}`' not in worker:
            errors.append(f'AUTONOMOUS_WORKER.md does not define the {state} state')
    for phrase in ['does not implement', 'adds no messaging service']:
        if phrase not in worker:
            errors.append(f'AUTONOMOUS_WORKER.md does not separate the contract from a runtime: {phrase}')
    if len(sorted((ROOT / 'skills').glob('*/SKILL.md'))) != HUMANITIES_SKILLS:
        errors.append(f'expected {HUMANITIES_SKILLS} Humanities SKILL.md files')


def release_files() -> list[Path]:
    """Return Git-visible release inputs, excluding ignored local artifacts."""
    result = subprocess.run(
        ['git', 'ls-files', '--cached', '-z'],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    files: list[Path] = []
    for raw in result.stdout.decode('utf-8').split('\0'):
        if not raw:
            continue
        path = ROOT / raw
        if path == MANIFEST_PATH or path.name == 'VALIDATION_REPORT.txt':
            continue
        if path.is_symlink():
            raise ValueError(f'release inventory refuses symlink: {raw}')
        if not path.is_file():
            raise ValueError(f'release inventory path is not a regular file: {raw}')
        files.append(path)
    files.sort()
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
        'version': PROJECT_VERSION,
        'file_count': len(files),
        'files': files,
    }


def update_manifest() -> int:
    payload = json.dumps(manifest_data(), ensure_ascii=False, indent=2) + '\n'
    descriptor, temporary = tempfile.mkstemp(prefix='.MANIFEST.', suffix='.tmp', dir=ROOT)
    try:
        with os.fdopen(descriptor, 'wb') as handle:
            handle.write(payload.encode('utf-8'))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, MANIFEST_PATH)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    print(f'UPDATED: MANIFEST.json ({len(manifest_data()["files"])} files)')
    return 0


def main() -> int:
    errors: list[str] = []

    validate_release_version(errors)
    validate_release_documents(errors)
    validate_vendor_provenance(errors)
    validate_release_hygiene(errors)
    validate_install_and_contract_inventory(errors)

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
        ROOT / '.github/ISSUE_TEMPLATE/test_report.yml',
        ROOT / '.github/ISSUE_TEMPLATE/methodological_criticism.yml',
        ROOT / '.github/ISSUE_TEMPLATE/installation_problem.yml',
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
        elif match.group(1) != PROJECT_VERSION:
            errors.append(f'skill version is not {PROJECT_VERSION}: {skill_file.relative_to(ROOT)} ({match.group(1)})')

    for path in [
        ROOT / 'project.json', ROOT / '.codex-plugin/plugin.json',
        ROOT / '.claude-plugin/plugin.json', ROOT / '.cursor-plugin/plugin.json',
    ]:
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            if data.get('version') != PROJECT_VERSION:
                errors.append(f'version is not {PROJECT_VERSION}: {path.relative_to(ROOT)}')
        except Exception as exc:
            errors.append(f'invalid json {path.relative_to(ROOT)}: {exc}')

    citation = (ROOT / 'CITATION.cff').read_text(encoding='utf-8')
    for value in [f'version: {PROJECT_VERSION}', 'family-names: "Lee"', 'given-names: "Yong Wook"', 'license: MIT']:
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
        if listed_manifest.get('version') != PROJECT_VERSION:
            errors.append(f'MANIFEST.json version is not {PROJECT_VERSION}')
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
