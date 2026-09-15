# Autonomous Worker Protocol

**Status: implemented and released in v2.1.0. The research core it routes to is unchanged.**

This contract exists for unattended work: DeepSeek-style implementers, Codex
workers, schedulers, and any run whose human supervisor is not watching. It
defines the states a worker must be able to report, how a silent stall is
detected, and what a notification interface may contain. It does not implement
a notification channel.

## States

| State | Meaning | Required evidence |
|---|---|---|
| `WORKING` | Progress is being made toward the objective | at least one `progress_evidence` entry newer than the stall threshold |
| `WAITING_INPUT` | A specific question is blocking progress | the question, what it blocks, and the smallest artifact that would answer it |
| `WAITING_PRIVILEGE` | The next step needs a boundary the agent cannot cross | the boundary (`UAC`, `SYSTEM`, `administrator`, `service account`, `external credential`), the exact action, and the rollback plan |
| `BLOCKED` | No available path reaches the objective | the obstruction, what was tried, and what would unblock it |
| `ERROR` | The last attempt failed | the failing command or check, its observed output, and the attempt count |
| `DONE` | The objective is achieved and verified | a completion verification record with observed output |

## Two rules that prevent the common lies

1. **A live process is not `WORKING`.** A worker that has produced no new
   evidence inside its stall threshold is stalled regardless of CPU, log
   activity, or process uptime.
2. **A finished process is not `DONE`.** `DONE` requires a completion
   verification record. Exit code 0, a written summary, or an optimistic
   message is not verification. If verification has not run, the state is
   `WORKING`, `ERROR`, or `BLOCKED` — never `DONE`.

## Stall detection

Each state report carries `last_progress_at`. Progress means one of:

- a new or changed artifact on disk;
- new observed command or test output;
- a recorded decision that removes a candidate path;
- a state transition.

The stall threshold is per-task and stated in the report. When
`now - last_progress_at` exceeds it, the worker MUST re-evaluate and re-report
its state rather than continue silently. Re-evaluation chooses the most
specific truthful state:

| Observation | Next state |
|---|---|
| A question is outstanding and unanswered | `WAITING_INPUT` |
| A permission or elevation prompt is outstanding | `WAITING_PRIVILEGE` |
| Every attempted path is exhausted | `BLOCKED` |
| The same failure recurred the attempt limit | `ERROR` |
| Work is genuinely proceeding | `WORKING` |

A worker that cannot distinguish these cases reports `BLOCKED`, because
"unknown why nothing is happening" is itself a blocker.

## Privilege boundary

`WAITING_PRIVILEGE` is not a generic failure. It names the boundary explicitly,
because an unattended worker cannot interact with a UAC consent prompt, a
Windows SYSTEM-owned resource, or an interactive credential request.

Required fields: `privilege_boundary`, `requested_action`, `blocked_since`,
`rollback_plan`, and whether the action is reversible. The worker MUST NOT
attempt to bypass the boundary by changing ownership, disabling controls, or
elevating through an unrelated path.

## Notification interface

Notification is an interface, not an implementation. A worker emits events; a
host adapter decides whether to deliver them (for example through an existing
Hermes or Telegram bridge). This repository adds no messaging service.

Event kinds:

| Kind | When |
|---|---|
| `STATE_CHANGED` | any state transition, including to and from `DONE` |
| `STALL_DETECTED` | the stall threshold passed |
| `PRIVILEGE_REQUIRED` | entering `WAITING_PRIVILEGE` |
| `INPUT_REQUIRED` | entering `WAITING_INPUT` |
| `ERROR_RECORDED` | entering `ERROR` |
| `COMPLETION_VERIFIED` | `DONE` with its verification record |

Every event carries the worker id, task reference, state, timestamp, the reason
string, and references to the `WORK_PACKAGE` and `EVIDENCE_PACKAGE`. Message
payloads MUST NOT contain credentials, secrets, private source text, or
unpublished manuscript content.

## Adapter boundary

A host adapter receives events and is responsible for delivery, retries,
deduplication, and rate limiting. The worker must behave identically when no
adapter is attached: events are written to the state record and nothing else
happens. Delivery failure is never a worker state change.

See [Agent orchestration](AGENT_ORCHESTRATION.md) for the handoff packages this
record references, and [Risk calibration](RISK_ROUTER.md) for how `STRICT`
changes affect completion evidence.
