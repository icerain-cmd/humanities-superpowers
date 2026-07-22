# Recommended Launch Sequence

## Before the next public announcement

1. Run all repository validators and inspect the final diff.
2. Confirm that README images and documentation links render correctly.
3. Retain Claude Code and OpenAI Codex as tested environments.
4. Test Cursor loading, or keep the not-independently-verified label.
5. Replace `[REPOSITORY_URL]` and `[PAGES_URL]` in the launch copy.
6. If releasing fixes, create a new patch release without moving the existing `v1.0.0` tag.

## Launch day

1. Publish the main Korean announcement.
2. Publish the main English announcement within the same day.
3. Post the short version to link-oriented social platforms.
4. Share the academic-community version with relevant research groups.
5. Pin the repository and the main announcement on the author's profile.

## Days 2–7

1. Publish one post explaining the intentional `FAIL` example.
2. Publish one image showing the research pipeline or quality gates.
3. Share the graduate-student version.
4. Open GitHub Discussions if early users need a lower-friction feedback channel.
5. Respond to issues without promising unsupported compatibility.

## Weeks 2–4

1. Summarize real installation and use feedback.
2. Label confirmed issues separately from feature requests.
3. Publish a short follow-up describing what changed and what remains unverified.
4. Prepare `v1.0.1` only for confirmed documentation, installation, or validation fixes.

## Messaging rules

Do not claim that the framework:

- prevents hallucinations
- guarantees accurate citations
- produces publication-ready manuscripts
- automates peer review
- replaces scholarly expertise

Prefer:

- reduces the risk of fabricated citations
- forces explicit checks before a claim is accepted
- preserves unresolved uncertainty
- supports scholarly judgment rather than replacing it
