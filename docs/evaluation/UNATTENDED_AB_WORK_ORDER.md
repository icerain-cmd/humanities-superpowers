# Unattended A/B work order

This document is the dispatchable form of the comparison described in
[HSP_COMPARISON_HARNESS.md](HSP_COMPARISON_HARNESS.md). It has two parts: a
mandatory preflight header that must be prepended to any long unattended run,
and the two comparison tracks with their exact commands.

The tracks are deliberately separate. The research track answers "does the
Humanities core help a scholar more than a strong generic instruction?" The
coding track answers "does the Engineering core help an implementer more than
the same implementer working unaided?" Merging their scores would hide which
core, if either, is worth its cost.

---

## Part 1 — Autonomous full-access mode: mandatory preflight

이 작업은 사람이 자리를 비운 상태에서 수행하는 무인 작업이다.

작업을 시작하기 전에 현재 에이전트 세션의 **실효 설정(effective settings)** 을
확인하라. 프롬프트에 "무인으로 진행하라"고 쓰여 있다는 사실은 full access의
증거가 아니다.

필수 조건:

```text
approval_policy = never
sandbox_mode    = danger-full-access
```

또는 현재 CLI 버전에서 위와 정확히 동등한 "승인 요청 없음 + 샌드박스 제한 없음"의
실효 설정이어야 한다.

1. 먼저 현재 세션의 실제 approval policy와 sandbox mode를 확인하라.
   설정 파일에 값이 있는지가 아니라 **이 세션에 실제로 적용된 값**을 확인한다.
   CLI 플래그는 설정 파일보다 우선순위가 높으므로, 둘 중 하나만 보고 판단하지 마라.

2. 다음 중 하나라도 아니면 본 작업을 시작하지 마라.

   ```text
   AUTONOMOUS_PREFLIGHT=FAIL
   ```

3. 설정이 다르다면:

   - 사용자에게 승인 요청을 반복하지 마라.
   - 현재 세션 안에서 안전하게 변경 가능한 공식 설정 방법이 있으면 적용 후 재확인한다.
   - 세션 재시작이 필요한 경우 임의로 현재 세션을 파괴하지 않는다.
   - `AUTONOMOUS_PREFLIGHT=FAIL`로 보고하고 중단한다.

4. preflight가 통과하면 다음을 명시적으로 기록한다.

   ```text
   AUTONOMOUS_PREFLIGHT=PASS
   APPROVAL_POLICY=never
   SANDBOX_MODE=danger-full-access
   INTERACTIVE_APPROVAL_EXPECTED=NO
   ```

세션 재시작이 필요한 설정 변경은 **다음 세션의 런처**에서 고정하는 것이 옳다.
가장 안전한 형태는 프로필 파일과 CLI 플래그 양쪽에 같은 값을 쓰는 것이다.

```text
# 프로필 파일 예시
approval_policy = "never"
sandbox_mode    = "danger-full-access"

# 런처 예시 (CLI 플래그가 최우선)
exec <agent-cli> --profile <unattended-profile> \
  --ask-for-approval never --sandbox danger-full-access "$@"
```

## Part 2 — Unattended execution rules

preflight PASS 이후에는 일반적인 승인 요청 때문에 작업을 멈추지 마라.
허용된 작업 범위 안에서 필요한 파일 읽기/쓰기, 코드 수정, 테스트 실행, lint/build,
`git status`/`git diff`, 작업용 branch commit, 로그 확인, 로컬 개발 서버 실행,
비파괴적 진단은 사용자에게 하나씩 승인받지 말고 계속 수행한다.

단, "승인하지 말라"는 것은 보안 경계를 우회하라는 뜻이 아니다. 다음은 approval
정책과 별개의 **외부 권한 경계**다.

- OS 관리자 권한 상승(UAC, sudo 비밀번호, Administrator/SYSTEM 경계)
- OS 자격증명 프롬프트, 외부 서비스 로그인/MFA
- 사람이 직접 승인해야 하는 보안 프롬프트

이런 경계를 만나면 승인창 앞에서 무한 대기하지 마라. 비대화형·사전 승인된 안전한
경로가 있는지 먼저 조사한다(이미 등록된 예약 작업, 기존 privileged helper, 기존
서비스, 이미 승인된 credential/session, 같은 목적의 비관리자 진단 방법). 안전한
기존 경로가 있으면 그것을 사용한다. 없다면:

```text
STATE=WAITING_PRIVILEGE
```

로 전환하고 다음을 기록한다 — 어떤 권한 경계인지, 왜 필요한지, 어디까지
완료했는지, 저장된 변경사항, 재개 지점과 재개 명령, 안전한 대안, rollback 방법.
그 뒤 승인창을 기다리며 `WORKING`이라고 표시하지 마라.

## Part 3 — No silent stall

프로세스가 살아 있다는 사실은 `WORKING`의 증거가 아니다. progress evidence는
다음 중 하나다: artifact 변경, 새로운 test/build 결과, 새로운 관찰 결과, 새로운
결정 기록, 명시적 state transition.

설정된 stall threshold 동안 progress evidence가 없으면 즉시 상태를 재평가하고
`WORKING`, `WAITING_INPUT`, `WAITING_PRIVILEGE`, `BLOCKED`, `ERROR`, `DONE` 중
하나로 표현한다. 이유를 알 수 없는데 진행되지 않으면 `BLOCKED`, 사용자 입력이
없어 진행 불가면 `WAITING_INPUT`, 권한 경계면 `WAITING_PRIVILEGE`다.
`DONE`은 반드시 completion verification evidence가 있어야 한다.

## Part 4 — Decision autonomy

사소한 구현 선택 때문에 사용자에게 묻지 마라. 저장소, 코드, 문서, 테스트에서
답을 찾을 수 있는 것은 먼저 스스로 조사한다. 여러 안전한 방법이 있으면 다음
우선순위로 고른다: 기존 architecture와 일치 → 최소 변경 → backward compatibility
→ reversible → testable. 중요한 결정이지만 기존 계약에서 합리적으로 결정할 수
있으면 그 기준으로 결정하고 기록한다.

`WAITING_INPUT`은 다음 경우에만 허용한다: 요구사항이 서로 모순됨, 사용자만 결정할
수 있는 제품/학술 판단, 되돌릴 수 없는 파괴적 작업, 법적·계정·결제 결정, 기존
계약만으로 선택할 수 없는 중대한 architecture fork.

---

## Part 5 — Track A: research comparison

```text
CONDITIONS:  CONTROL                 vs  HSP
FIXTURES:    tests/eval/cases.json   (T1 citation existence, T2 claim-source fit,
                                      T3 rival interpretation, T4 concept drift,
                                      T5 new evidence/return, T6 clean case)
```

```bash
python3 scripts/hsp_eval.py plan                 # render the 12 prompts
python3 scripts/hsp_eval.py score runs.jsonl     # score recorded runs
```

Both conditions must use the same model and the same reasoning level. `HSP`
receives the router plus the smallest sufficient Humanities skill set;
`CONTROL` receives one strong generic research instruction. Same material,
same allowed labels, same answer contract.

Record one JSONL line per run:

```json
{"case_id": "T1-citation-existence", "condition": "HSP", "response": "...",
 "usage": {"input_tokens": 0, "output_tokens": 0},
 "wall_clock_seconds": 0, "tool_calls": 0, "researcher_interruptions": 0}
```

## Part 6 — Track B: coding comparison

```text
CONDITIONS:  CONTROL_CODING          vs  ENGINEERING_CORE
FIXTURES:    tests/eval/coding-cases.json   (C1 localized UI, C2 bounded endpoint,
        C3 unknown-cause bug, C4 SYSTEM scheduled task, C5 public contract change,
        C6 clean refactor)
```

```bash
python3 scripts/hsp_eval_coding.py plan
python3 scripts/hsp_eval_coding.py score runs.jsonl
```

`ENGINEERING_CORE` receives the Dual-Core risk calibration, the smallest
sufficient engineering skill route, and the `WORK_PACKAGE`/`EVIDENCE_PACKAGE`
handoff. `CONTROL_CODING` receives one strong generic engineering instruction
with the same repository state and the same answer contract.

Reported metrics: risk-level accuracy, defect detection recall, defect false
positives, completion accuracy, unverified `DONE` claims, false block rate,
privilege-boundary accuracy, invalid contract artifacts, token overhead, time
overhead, interruptions, and defects caught per additional 10k tokens. The
scorer validates submitted `work_package`/`evidence_package` against the
Dual-Core schemas, so a run that skips the handoff contract is counted as a
contract failure rather than passing silently.

## Part 7 — Required final report

```text
AUTONOMOUS_PREFLIGHT=
APPROVAL_POLICY=
SANDBOX_MODE=

FINAL_STATE=            WORKING | WAITING_INPUT | WAITING_PRIVILEGE | BLOCKED | ERROR | DONE
STALL_OCCURRED=
PRIVILEGE_BOUNDARY_ENCOUNTERED=

FILES_CHANGED=
TESTS_RUN=
TEST_RESULTS=
COMMITS=
UNRESOLVED=
RESUME_POINT=

COMPLETION_VERIFICATION=
```

`AUTONOMOUS_PREFLIGHT`가 PASS가 아닌 상태에서 "무인 작업 완료"라고 보고하지 마라.
측정하지 않은 지표는 `NOT_MEASURED`로 남긴다. 합성 self-test 결과를 실제 효과로
보고하지 마라.
