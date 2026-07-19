from pathlib import Path
import json, sys

root=Path(__file__).resolve().parents[1]
if len(sys.argv)!=5:
    print('Usage: python3 scripts/prepare_release.py "Full Name" "GitHubUsername" "email" "Family|Given"')
    raise SystemExit(2)
name, username, email, split=sys.argv[1:]
family,given=split.split('|',1)
repls={'Lee Yong Wook':name,'icerain-cmd':username,'icerain@jj.ac.kr':email,'Lee':family,'Yong Wook':given}
for path in root.rglob('*'):
    if path.is_file() and '.git' not in path.parts:
        try: text=path.read_text(encoding='utf-8')
        except UnicodeDecodeError: continue
        new=text
        for a,b in repls.items(): new=new.replace(a,b)
        if new!=text: path.write_text(new,encoding='utf-8')
print('Updated publication metadata. Run: python3 scripts/validate_repository.py')
