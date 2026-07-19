# Research Session Memory

Humanities Superpowers uses an explicit session artifact rather than relying on opaque model memory.

## What the session record does

It records workflow context:

- requested outcome;
- current state;
- completed skills and gate results;
- artifacts and provenance;
- blocking issues and conditions;
- researcher decisions;
- rollback history;
- next valid action.

## What it does not do

A session record does not:

- verify a source;
- preserve the full contents of a primary object;
- replace a manuscript, bibliography, or audit;
- prove that an earlier gate remains valid after artifacts change;
- authorize the agent to make an authorial decision.

## Resume protocol

When resuming:

1. read the session record;
2. confirm that referenced artifacts are available;
3. identify artifacts modified since the last gate;
4. invalidate any gate whose evidence has materially changed;
5. begin from the next valid action or recalculate the route.

## Privacy

Do not place confidential reviewer identities, personal data, embargoed materials, or sensitive human-subject information in a session record unless the researcher has an approved secure workflow.
