from __future__ import annotations
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []
REQUIRED_META = ["name", "description", "version", "language", "license"]
REQUIRED_SECTIONS = [
    "Purpose", "When to use", "Inputs required", "Procedure", "Stop signals",
    "Completion criteria", "Anti-fabrication rules", "Output format",
    "Good invocation", "Bad invocation", "Next skills", "Limitations"
]
EXPECTED_SKILLS = {
    "using-humanities-superpowers", "formulating-research-question",
    "scoping-argument-boundary", "mapping-concept-lineage",
    "conducting-literature-dialogue", "planning-humanities-argument",
    "performing-close-reading", "structuring-humanities-argument",
    "stress-testing-argument", "auditing-citations",
    "checking-terminology-consistency", "reviewing-manuscript",
    "responding-to-peer-review", "verifying-before-submission"
}
# Router is part of the 13-method set's orchestration layer; substantive set excludes router.
EXPECTED_SUBSTANTIVE_COUNT = 13
LEVEL2_FOUNDATION_SKILLS = {
    "formulating-research-question", "scoping-argument-boundary",
    "mapping-concept-lineage", "conducting-literature-dialogue"
}
LEVEL2_ARGUMENT_SKILLS = {
    "planning-humanities-argument", "performing-close-reading",
    "structuring-humanities-argument", "stress-testing-argument"
}
LEVEL2_VERIFICATION_SKILLS = {
    "auditing-citations", "checking-terminology-consistency",
    "reviewing-manuscript", "responding-to-peer-review",
    "verifying-before-submission"
}
LEVEL2_SKILLS = LEVEL2_FOUNDATION_SKILLS | LEVEL2_ARGUMENT_SKILLS | LEVEL2_VERIFICATION_SKILLS
LEVEL3_ROUTER = "using-humanities-superpowers"
CONTRACT_FIELDS = [
    "**Accepts**", "**Requires**", "**Produces**", "**May produce**",
    "**Fails when**", "**Guarantees**", "**Does not guarantee**"
]

def error(msg: str) -> None: ERRORS.append(msg)
def warning(msg: str) -> None: WARNINGS.append(msg)

def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    if not text.startswith("---\n"):
        error(f"{path}: missing YAML front matter")
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        error(f"{path}: unterminated front matter")
        return {}
    meta = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            error(f"{path}: invalid metadata line: {line}")
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"')
    return meta

def validate_skills() -> None:
    found = set()
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text, path.relative_to(ROOT))
        for key in REQUIRED_META:
            if not meta.get(key): error(f"{path.relative_to(ROOT)}: missing metadata {key}")
        name = meta.get("name", "")
        found.add(name)
        if name != path.parent.name: error(f"{path.relative_to(ROOT)}: name does not match directory")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name): error(f"{path.relative_to(ROOT)}: invalid kebab-case name")
        if not meta.get("description", "").startswith("Use when "): error(f"{path.relative_to(ROOT)}: description must start with 'Use when '")
        for section in REQUIRED_SECTIONS:
            if f"## {section}" not in text: error(f"{path.relative_to(ROOT)}: missing section {section}")
        if name in LEVEL2_SKILLS or name == LEVEL3_ROUTER:
            if "## Contract" not in text: error(f"{path.relative_to(ROOT)}: Level 2 skill missing Contract section")
            for field in CONTRACT_FIELDS:
                if field not in text: error(f"{path.relative_to(ROOT)}: Level 2 skill missing contract field {field}")
            if "## Gate report" not in text and "Gate report" not in text:
                error(f"{path.relative_to(ROOT)}: Level 2 skill missing gate-report output")
            minimum = 1800 if name == LEVEL3_ROUTER else 1100
            if len(text.split()) < minimum:
                warning(f"{path.relative_to(ROOT)}: conformance skill is shorter than {minimum:,} words")
        if "guarantee" in text.lower() and "does not guarantee" not in text.lower() and "cannot guarantee" not in text.lower():
            warning(f"{path.relative_to(ROOT)}: inspect guarantee language")
    if found != EXPECTED_SKILLS:
        error(f"skill set mismatch; missing={sorted(EXPECTED_SKILLS-found)} extra={sorted(found-EXPECTED_SKILLS)}")
    substantive = found - {"using-humanities-superpowers"}
    if len(substantive) != EXPECTED_SUBSTANTIVE_COUNT:
        error(f"expected {EXPECTED_SUBSTANTIVE_COUNT} substantive skills, found {len(substantive)}")

def validate_json() -> None:
    for path in [ROOT/'project.json', ROOT/'.codex-plugin/plugin.json', ROOT/'.claude-plugin/plugin.json', ROOT/'.cursor-plugin/plugin.json']:
        try: json.loads(path.read_text(encoding='utf-8'))
        except Exception as exc: error(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")

def validate_links() -> None:
    pattern = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
    for path in ROOT.rglob('*.md'):
        text=path.read_text(encoding='utf-8')
        for raw in pattern.findall(text):
            target=raw.split('#',1)[0]
            if not target: continue
            resolved=(path.parent/target).resolve()
            if not resolved.exists(): error(f"{path.relative_to(ROOT)}: broken link -> {raw}")

def validate_example() -> None:
    base=ROOT/'examples/concept-paper-example'
    required=['README.md','input/research-brief.md','output/research-question.md','output/scope-boundary.md','output/concept-lineage.md','output/argument-map.md','output/terminology-ledger.md','output/citation-audit.md','output/final-check.md']
    for rel in required:
        if not (base/rel).exists(): error(f"example missing {rel}")
    final=(base/'output/final-check.md').read_text(encoding='utf-8')
    if '`FAIL`' not in final:
        error('worked example must preserve its failing final gate')
    else:
        print('INTENTIONAL FAIL — OK: worked example correctly preserves an unresolved final gate')
    focused = [ROOT/'examples/argument-map-example/README.md', ROOT/'examples/terminology-audit-example/README.md']
    for path in focused:
        if not path.exists(): error(f'focused example missing {path.relative_to(ROOT)}')
    for asset in [ROOT/'assets/research-pipeline.svg', ROOT/'assets/skill-map.svg', ROOT/'assets/quality-gates.svg', ROOT/'assets/human-ai-collaboration.svg', ROOT/'assets/research-lifecycle.svg']:
        if not asset.exists(): error(f'visual asset missing {asset.relative_to(ROOT)}')

def validate_methodology() -> None:
    required = [
        ROOT/'MANIFESTO.md', ROOT/'docs/PHILOSOPHY.md', ROOT/'docs/DESIGN_PRINCIPLES.md',
        ROOT/'docs/ANTI_PATTERNS.md', ROOT/'docs/QUALITY_GATES.md',
        ROOT/'docs/white-paper/HUMANITIES_SUPERPOWERS_WHITE_PAPER.md'
    ]
    for path in required:
        if not path.exists(): error(f'methodology document missing {path.relative_to(ROOT)}')
    white = (ROOT/'docs/white-paper/HUMANITIES_SUPERPOWERS_WHITE_PAPER.md').read_text(encoding='utf-8')
    if len(white.split()) < 5000: warning('white paper is shorter than 5,000 words')
    for phrase in ['Research before prose', 'Unknown is better than fabricated', 'Completion must be demonstrated']:
        if phrase not in white: error(f'white paper missing core principle: {phrase}')

def validate_specification() -> None:
    required = [
        ROOT/'docs/specification/README.md',
        ROOT/'docs/specification/CORE_SPECIFICATION.md',
        ROOT/'docs/specification/SKILL_CONTRACT.md',
        ROOT/'docs/specification/RESEARCH_OBJECT_MODEL.md',
        ROOT/'docs/specification/RESEARCH_GRAMMAR.md',
        ROOT/'docs/specification/LANGUAGE_GUIDE.md',
        ROOT/'docs/specification/CONFORMANCE.md',
        ROOT/'docs/specification/EXTENSION_PROTOCOL.md',
        ROOT/'docs/specification/DECISION_RECORDS.md',
        ROOT/'templates/skill-contract.md',
        ROOT/'schemas/research-object.schema.json',
        ROOT/'schemas/gate-report.schema.json',
        ROOT/'tests/conformance/skills.yaml',
    ]
    for path in required:
        if not path.exists(): error(f'specification artifact missing {path.relative_to(ROOT)}')
    for path in [ROOT/'schemas/research-object.schema.json', ROOT/'schemas/gate-report.schema.json']:
        try:
            data=json.loads(path.read_text(encoding='utf-8'))
            if data.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
                error(f'{path.relative_to(ROOT)}: unexpected JSON Schema version')
        except Exception as exc:
            error(f'{path.relative_to(ROOT)}: invalid schema JSON: {exc}')
    core=(ROOT/'docs/specification/CORE_SPECIFICATION.md').read_text(encoding='utf-8')
    for phrase in ['Research before prose', 'Unknown before invented', 'Failure is a valid outcome']:
        if phrase not in core: error(f'core specification missing commitment: {phrase}')
    contract=(ROOT/'docs/specification/SKILL_CONTRACT.md').read_text(encoding='utf-8')
    for field in ['**Accepts**', '**Requires**', '**Produces**', '**Fails when**', '**Guarantees**', '**Does not guarantee**']:
        if field not in contract: error(f'skill contract specification missing field: {field}')
    grammar=(ROOT/'docs/specification/RESEARCH_GRAMMAR.md').read_text(encoding='utf-8')
    for prohibited in ['unknown -> verified', 'interpretation -> fact', 'polished prose -> completed argument']:
        if prohibited not in grammar: error(f'research grammar missing prohibited transformation: {prohibited}')
    cases = ROOT/'tests/conformance/phase3b-foundation-cases.yaml'
    if not cases.exists():
        error('Phase 3-B foundation conformance cases missing')
    else:
        case_text=cases.read_text(encoding='utf-8')
        for skill in LEVEL2_FOUNDATION_SKILLS:
            if f"  {skill}:" not in case_text: error(f'Phase 3-B cases missing skill: {skill}')
        for case_type in ['type: positive', 'type: negative', 'type: missing-input', 'type: adversarial', 'type: handoff']:
            if case_text.count(case_type) < 4: error(f'Phase 3-B cases need four instances of {case_type}')
    phase3c = ROOT/'tests/conformance/phase3c-argument-cases.yaml'
    if not phase3c.exists():
        error('Phase 3-C argument conformance cases missing')
    else:
        case_text=phase3c.read_text(encoding='utf-8')
        for skill in LEVEL2_ARGUMENT_SKILLS:
            if f"  {skill}:" not in case_text: error(f'Phase 3-C cases missing skill: {skill}')
        for case_type in ['type: positive', 'type: negative', 'type: missing-input', 'type: adversarial', 'type: handoff']:
            if case_text.count(case_type) < 4: error(f'Phase 3-C cases need four instances of {case_type}')
    phase3d = ROOT/'tests/conformance/phase3d-verification-cases.yaml'
    if not phase3d.exists():
        error('Phase 3-D verification conformance cases missing')
    else:
        case_text=phase3d.read_text(encoding='utf-8')
        for skill in LEVEL2_VERIFICATION_SKILLS:
            if f"  {skill}:" not in case_text: error(f'Phase 3-D cases missing skill: {skill}')
        for case_type in ['type: positive', 'type: negative', 'type: missing-input', 'type: adversarial', 'type: handoff']:
            if case_text.count(case_type) < 5: error(f'Phase 3-D cases need five instances of {case_type}')
    registry=(ROOT/'tests/conformance/skills.yaml').read_text(encoding='utf-8')
    for skill in LEVEL2_SKILLS:
        pattern=rf"- skill: {re.escape(skill)}\n    current_level: 2\n    target_level: 2"
        if not re.search(pattern, registry): error(f'conformance registry does not mark {skill} at Level 2')

    phase3e = ROOT/'tests/conformance/phase3e-router-cases.yaml'
    if not phase3e.exists():
        error('Phase 3-E router conformance cases missing')
    else:
        case_text=phase3e.read_text(encoding='utf-8')
        for case_type in ['type: positive', 'type: negative', 'type: ambiguous', 'type: missing-input', 'type: adversarial', 'type: rollback', 'type: researcher-decision', 'type: resume', 'type: handoff', 'type: end-to-end']:
            if case_type not in case_text: error(f'Phase 3-E router cases missing {case_type}')
        for decision in ['PROCEED', 'PAUSE', 'ROLLBACK', 'RESEARCHER_DECISION_REQUIRED', 'STOP']:
            if decision not in case_text: error(f'Phase 3-E router cases missing decision {decision}')
    router=(ROOT/'skills/using-humanities-superpowers/SKILL.md').read_text(encoding='utf-8')
    for state in ['IDEA', 'QUESTION', 'SCOPE', 'SOURCES', 'INTERPRETATION', 'ARGUMENT', 'STRUCTURE', 'REVIEW', 'REVISION', 'SUBMISSION', 'BLOCKED', 'UNKNOWN']:
        if f'`{state}`' not in router: error(f'router missing research state: {state}')
    for decision in ['PROCEED', 'PAUSE', 'ROLLBACK', 'RESEARCHER_DECISION_REQUIRED', 'STOP']:
        if decision not in router: error(f'router missing routing decision: {decision}')
    for artifact in [ROOT/'docs/orchestration/RESEARCH_STATE_MACHINE.md', ROOT/'docs/orchestration/ROUTING_AND_ROLLBACK.md', ROOT/'docs/orchestration/SESSION_MEMORY.md', ROOT/'templates/research-session.md', ROOT/'schemas/research-session.schema.json']:
        if not artifact.exists(): error(f'orchestration artifact missing {artifact.relative_to(ROOT)}')
    try:
        session_schema=json.loads((ROOT/'schemas/research-session.schema.json').read_text(encoding='utf-8'))
        if session_schema.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
            error('schemas/research-session.schema.json: unexpected JSON Schema version')
    except Exception as exc:
        error(f'schemas/research-session.schema.json: invalid schema JSON: {exc}')
    router_pattern=rf"- skill: {re.escape(LEVEL3_ROUTER)}\n    current_level: 3\n    target_level: 3"
    if not re.search(router_pattern, registry): error('conformance registry does not mark router at Level 3')


def validate_integration() -> None:
    required = [
        ROOT/'docs/integration/INTEGRATED_CONFORMANCE.md',
        ROOT/'docs/integration/TEST_COVERAGE.md',
        ROOT/'docs/integration/RELEASE_BLOCKERS.md',
        ROOT/'tests/integration/scenarios.json',
        ROOT/'scripts/run_integrated_tests.py',
        ROOT/'examples/end-to-end-research-session/README.md',
        ROOT/'examples/end-to-end-research-session/session-01.json',
        ROOT/'examples/end-to-end-research-session/gate-history.md',
        ROOT/'examples/end-to-end-research-session/handoff-trace.md',
    ]
    for path in required:
        if not path.exists(): error(f'integration artifact missing {path.relative_to(ROOT)}')
    try:
        data=json.loads((ROOT/'tests/integration/scenarios.json').read_text(encoding='utf-8'))
        scenarios=data.get('scenarios',[])
        if len(scenarios) < 8: error('integrated suite requires at least eight scenarios')
        all_text=json.dumps(data)
        for skill in EXPECTED_SKILLS:
            if skill not in all_text: error(f'integrated scenarios do not cover skill: {skill}')
        for decision in ['PROCEED','PAUSE','ROLLBACK','RESEARCHER_DECISION_REQUIRED','STOP']:
            if decision not in all_text: error(f'integrated scenarios do not cover decision: {decision}')
    except Exception as exc:
        error(f'tests/integration/scenarios.json: invalid JSON: {exc}')
    try:
        session=json.loads((ROOT/'examples/end-to-end-research-session/session-01.json').read_text(encoding='utf-8'))
        if session.get('routing_decision') != 'PAUSE': error('end-to-end example must preserve PAUSE decision')
        if not session.get('blocking_issues'): error('end-to-end example must preserve blocking issues')
    except Exception as exc:
        error(f'end-to-end session JSON invalid: {exc}')

def validate_placeholders() -> None:
    allowed={'project.json','CITATION.cff','LICENSE','CODE_OF_CONDUCT.md','SECURITY.md','plugin.json','README.md','README.ko.md'}
    token=re.compile(r'AUTHOR_[A-Z_]+|GITHUB_USERNAME|CONTACT_EMAIL')
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix in {'.md','.json','.cff',''}:
            matches=token.findall(path.read_text(encoding='utf-8',errors='ignore'))
            if matches and path.name not in allowed:
                error(f"{path.relative_to(ROOT)}: unexpected publication placeholder(s): {sorted(set(matches))}")

def main() -> int:
    validate_skills(); validate_json(); validate_links(); validate_example(); validate_methodology(); validate_specification(); validate_integration(); validate_placeholders()
    for msg in WARNINGS: print(f"WARNING: {msg}")
    for msg in ERRORS: print(f"ERROR: {msg}")
    if ERRORS:
        print(f"FAIL: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS: repository validation completed with 0 errors and {len(WARNINGS)} warning(s)")
    return 0
if __name__ == '__main__': raise SystemExit(main())
