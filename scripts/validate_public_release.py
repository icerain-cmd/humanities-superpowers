#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys, yaml
root=Path(__file__).resolve().parents[1]
errors=[]
required=[
'mkdocs.yml','site/requirements.txt','.github/workflows/pages.yml','.github/pull_request_template.md',
'.github/ISSUE_TEMPLATE/bug_report.yml','.github/ISSUE_TEMPLATE/skill_proposal.yml',
'docs/release/RELEASE_NOTES_v1.0.0.md','docs/release/PUBLIC_RELEASE_CHECKLIST.md',
'site/docs/index.md','site/docs/quick-start.md','site/docs/skills.md','MANIFEST.json'
]
for f in required:
    if not (root/f).exists(): errors.append(f'missing: {f}')
text_ext={'.md','.yml','.yaml','.json','.toml','.txt','.py','.cff','.mdc'}
for f in root.rglob('*'):
    if f.is_file() and f.suffix.lower() in text_ext and f.name!='MANIFEST.json' and 'scripts' not in f.parts:
        txt=f.read_text(errors='ignore')
        for token in ['GITHUB_USERNAME','AUTHOR_NAME','AFFILIATION','email@example.com','maintainer replaces this placeholder','1.0.0-draft.1','0.9.0-preview']:
            if token in txt: errors.append(f'placeholder or stale release token {token!r}: {f.relative_to(root)}')
for f in [root/'.github/ISSUE_TEMPLATE/bug_report.yml',root/'.github/ISSUE_TEMPLATE/skill_proposal.yml',root/'.github/workflows/pages.yml',root/'mkdocs.yml']:
    try: yaml.safe_load(f.read_text())
    except Exception as e: errors.append(f'invalid yaml {f.relative_to(root)}: {e}')
for skill_file in sorted((root/'skills').glob('*/SKILL.md')):
    match=re.search(r'^version:\s*([^\s]+)', skill_file.read_text(), re.MULTILINE)
    if not match:
        errors.append(f'missing skill version: {skill_file.relative_to(root)}')
    elif match.group(1)!='1.0.0':
        errors.append(f'skill version is not 1.0.0: {skill_file.relative_to(root)} ({match.group(1)})')
for f in [root/'project.json',root/'.codex-plugin/plugin.json',root/'.claude-plugin/plugin.json',root/'.cursor-plugin/plugin.json']:
    try:
        data=json.loads(f.read_text())
        if data.get('version')!='1.0.0': errors.append(f'version is not 1.0.0: {f.relative_to(root)}')
    except Exception as e: errors.append(f'invalid json {f.relative_to(root)}: {e}')
manifest_path=root/'MANIFEST.json'
if manifest_path.exists():
    try:
        manifest=json.loads(manifest_path.read_text())
        listed={x['path']:x for x in manifest['files']}
        actual=[]
        for f in sorted(root.rglob('*')):
            if f.is_file() and f!=manifest_path and f.name!='VALIDATION_REPORT.txt' and '.git' not in f.parts and 'site-build' not in f.parts:
                rel=f.relative_to(root).as_posix(); actual.append(rel)
                h=hashlib.sha256(f.read_bytes()).hexdigest()
                item=listed.get(rel)
                if not item: errors.append(f'manifest missing file: {rel}')
                elif item.get('sha256')!=h or item.get('bytes')!=f.stat().st_size: errors.append(f'manifest mismatch: {rel}')
        extra=sorted(set(listed)-set(actual))
        for rel in extra: errors.append(f'manifest lists absent file: {rel}')
        if manifest.get('file_count')!=len(actual): errors.append(f'manifest file_count {manifest.get("file_count")} != {len(actual)}')
    except Exception as e: errors.append(f'invalid MANIFEST.json: {e}')
if errors:
    print('FAIL: public release validation')
    print('\n'.join('- '+e for e in errors)); sys.exit(1)
print('PASS: public release versions, placeholders, metadata, and manifest')
