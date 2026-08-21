# Judgment History

The agent recommends A, but the researcher selects B. The record keeps A under `agent_recommendations` and B under `researcher_decision`; it never rewrites recommendation as authority.

After new evidence, D1 becomes `REOPENED`. D2 is appended and links `supersedes: D1`. The history shows what changed, why, and who authorized it. An absent `authorized_by` would leave the decision provisional.
