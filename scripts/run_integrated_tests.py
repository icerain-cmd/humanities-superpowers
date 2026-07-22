from __future__ import annotations
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
ALLOWED_DECISIONS={"PROCEED","PAUSE","ROLLBACK","RESEARCHER_DECISION_REQUIRED","STOP"}
EXPECTED_SKILLS={p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')}
ROUTER='using-humanities-superpowers'

def main()->int:
    errors=[]
    core_skills=EXPECTED_SKILLS-{ROUTER}
    if len(EXPECTED_SKILLS)!=14 or len(core_skills)!=13 or ROUTER not in EXPECTED_SKILLS:
        errors.append('expected 14 SKILL.md files: 13 core research skills and 1 router')
    data=json.loads((ROOT/'tests/integration/scenarios.json').read_text(encoding='utf-8'))
    scenarios=data.get('scenarios',[])
    seen_skills=set(); seen_decisions=set(); total_steps=0
    ids=set()
    for s in scenarios:
        sid=s.get('id')
        if not sid or sid in ids: errors.append(f'invalid or duplicate scenario id: {sid}')
        ids.add(sid)
        steps=s.get('steps',[])
        if not steps: errors.append(f'{sid}: no steps')
        total_steps += len(steps)
        for item in steps:
            if not isinstance(item,list) or len(item)!=2:
                errors.append(f'{sid}: invalid step {item!r}'); continue
            skill,decision=item
            seen_skills.add(skill); seen_decisions.add(decision)
            if skill not in EXPECTED_SKILLS: errors.append(f'{sid}: unknown skill {skill}')
            if decision not in ALLOWED_DECISIONS: errors.append(f'{sid}: invalid decision {decision}')
        terminal=s.get('expected_terminal_decision')
        if terminal not in ALLOWED_DECISIONS: errors.append(f'{sid}: invalid terminal decision')
        if terminal not in {d for _,d in steps}: errors.append(f'{sid}: terminal decision not represented in steps')
        if terminal=='ROLLBACK' and not s.get('rollback_target'): errors.append(f'{sid}: rollback target missing')
        if s.get('rollback_target') and s['rollback_target'] not in EXPECTED_SKILLS: errors.append(f'{sid}: invalid rollback target')
    missing=EXPECTED_SKILLS-seen_skills
    if missing: errors.append(f'integrated scenarios miss skills: {sorted(missing)}')
    missing_decisions=ALLOWED_DECISIONS-seen_decisions
    if missing_decisions: errors.append(f'integrated scenarios miss decisions: {sorted(missing_decisions)}')
    example=ROOT/'examples/end-to-end-research-session/session-01.json'
    session=json.loads(example.read_text(encoding='utf-8'))
    for field in ['session_id','updated_at','requested_outcome','current_state','routing_decision','completed_skills','blocking_issues','researcher_decisions_required','next_valid_action','completion_claim_restrictions']:
        if field not in session: errors.append(f'end-to-end session missing {field}')
    if session.get('routing_decision')!='PAUSE': errors.append('end-to-end example must preserve PAUSE')
    if not session.get('blocking_issues'): errors.append('end-to-end example must preserve blocking issue')
    for item in session.get('completed_skills',[]):
        if 'gate_status' not in item: errors.append('completed skill missing gate_status')
    if not isinstance(session.get('next_valid_action'),dict): errors.append('next_valid_action must be an object')
    if errors:
        for e in errors: print('ERROR:',e)
        print(f'FAIL: {len(errors)} integrated conformance error(s)')
        return 1
    print(
        f'PASS: {len(scenarios)} integrated scenarios, {total_steps} steps, '
        f'{len(seen_skills)} SKILL.md files (13 core research skills + 1 router), '
        f'{len(seen_decisions)} decisions'
    )
    return 0
if __name__=='__main__': raise SystemExit(main())
