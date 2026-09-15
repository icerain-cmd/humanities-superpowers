# Risk Calibration Router

**Status: implemented and released in v2.1.0. The research core it routes to is unchanged.**

The second routing axis applies to `CODE` and `HYBRID` requests only. It decides
how much process the change justifies, so that a harmless edit is not buried in
ceremony and a dangerous one is not waved through.

| Level | Default steps |
|---|---|
| `QUICK` | inspect → modify → targeted verification |
| `STANDARD` | inspect → short plan → implement → test → regression → verification |
| `STRICT` | investigate → root cause or design → explicit plan → test strategy → implement → review → integration test → regression → evidence → completion |

## Classification is semantic

Do not classify by keyword. Grade the change on these properties and take the
highest level any property demands:

| Property | Raises the level when… |
|---|---|
| Reversibility | the change cannot be undone by reverting a commit |
| Blast radius | more than one component, project, machine, or user is affected |
| Privilege boundary | the change crosses into SYSTEM, admin, UAC, or another account |
| Persistence | data, schema, credentials, or backups are created, migrated, or destroyed |
| Contract surface | a public API, file format, CLI, plugin manifest, or installation path changes |
| Environment | production, a shared service, or other people's work depends on it |
| Failure cost | a wrong result is silent, or is discovered only later |
| Uncertainty | the agent cannot state why the change is safe |

`QUICK` is the default for localized, reversible, single-consumer edits. `STRICT`
is mandatory when the change touches any item below.

## Automatic STRICT triggers

- production systems or services others use;
- authentication or authorization;
- security-sensitive code, secrets, or credential handling;
- database migrations or schema changes;
- destructive data operations (delete, overwrite, truncate, bulk rename);
- deployment, release, or rollback paths;
- Windows SYSTEM, administrator, UAC, or service-account boundaries;
- networking, ports, firewalls, tunnels, or serving configuration;
- backup and restore paths;
- major refactors that move or rename broadly;
- public API or external contract changes;
- persistent infrastructure, schedulers, daemons, or startup tasks.

## Escalation and de-escalation

- If two levels both seem defensible, take the higher one and record which
  property forced it.
- A task may drop from `STRICT` to `STANDARD` only when the triggering property
  is verified absent, and that verification is recorded. "It looks fine" is not
  verification.
- Refusing to classify is not allowed. Every `CODE`/`HYBRID` request gets a
  level, and the level is stated before implementation begins.

## Anti-ceremony rules

These exist because a system that fails everything, or formalizes everything,
is a defective system:

- Do not classify every task `STRICT`. A repository that demands full ceremony
  for a spacing fix has converted risk management into ritual.
- Do not invent steps a level does not require. If a required step genuinely
  does not apply, record `NOT_APPLICABLE` with the reason instead of
  manufacturing work that produces no evidence.
- Do not re-run the full suite for a change whose blast radius is one function,
  when a targeted test plus the relevant regression subset is the honest
  evidence.
- Do not skip verification because a change is `QUICK`. `QUICK` reduces
  ceremony, never evidence.

## Relationship to verification

Every level ends with verification proportional to the level, and completion is
claimed only from observed output. This is the same rule the vendored
`verification-before-completion` skill states, and it is the rule the
[autonomous worker protocol](AUTONOMOUS_WORKER.md) enforces for unattended work.

## Worked examples

| Change | Level | Why |
|---|---|---|
| Fix a typo in a template | `QUICK` | reversible, one file, no consumer |
| Adjust dashboard spacing | `QUICK` | reversible, localized, visual check is the evidence |
| Add a bounded endpoint with tests | `STANDARD` | new behavior, contract surface is local |
| Fix a bug whose cause is unknown | `STANDARD` | root cause must be established before the fix |
| Edit a Windows scheduled task that starts a SYSTEM service | `STRICT` | privilege boundary, persistence, blast radius |
| Change the gate-report schema | `STRICT` | public contract, other artifacts depend on it |
| Rotate or rewrite stored credentials | `STRICT` | security, destructive, hard to reverse |
