# Evidence Ledger Protocol

**Specification Version: 2.0.0**

## Core separation

`verification_state` asks whether the source or item was checked. `evidential_standing` asks what that item does for a particular claim. These fields MUST NOT be inferred from one another.

A real, verified article may still be insufficient:

```yaml
verification_state: verified-secondary
evidential_standing: INSUFFICIENT
```

## Evidential standing

- `SUPPORTS`: materially supports the claim within the stated scope;
- `QUALIFIES`: supports only a narrower or conditioned claim;
- `CONTRADICTS`: provides material counterevidence;
- `INSUFFICIENT`: does not establish the claim;
- `CONTEXT_ONLY`: supplies background without direct claim support;
- `DISPUTED`: standing cannot be resolved because reliable readings or sources conflict.

## Ledger rules

Every central claim SHOULD link all material supporting, qualifying, contradicting, and disputed evidence. Counterevidence MUST remain visible. Verification method, locator, limitations, checker, timestamp, and provenance MUST be recorded when known; absent information remains unknown.

A gate MUST NOT pass because supporting entries outnumber contradicting entries. It evaluates the consequence of each item, not a vote or score.

Verification states are not ranks that an agent may promote automatically. In particular, `researcher-supplied` MUST NOT become `verified-primary` or `verified-secondary` without an explicit verification act and recorded method, locator, checker, time, source digest, and host-supplied verification-event reference. Dedicated v2 ledger records enforce these fields conditionally for verified states; the host must match the event to the checker, source, digest, and locator.
