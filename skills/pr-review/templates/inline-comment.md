# Inline Comment Format

Keep each comment to one issue, anchored on the line that causes it.

~~~~
[HIGH] <one-line title>

<What the code does, in one sentence.>

Impact: <concrete failure scenario — inputs or state -> wrong outcome.>
Confidence: Confirmed / Likely

Suggested fix:
```<lang>
<minimal corrected snippet>
```
~~~~

Include the overall review assessment and verification limits separately from inline findings, following [SKILL.md](../SKILL.md#severity). An incomplete review must not imply approval.

## Rules

- One finding per comment. Do not stack unrelated points.
- Anchor on the changed line that *causes* the problem, not where it surfaces. For an unchanged caller broken by a changed contract, anchor to the contract change and cite the caller as supporting evidence.
- Lead with the severity label (`[CRITICAL]`, `[HIGH]`, `[MEDIUM]`, `[LOW]`, `[SUGGESTION]`) so the author can triage the thread list.
- Include a code suggestion when the fix is small and unambiguous; otherwise describe it.
- Only findings that survived the Phase 6 verification pass become comments.
- *Needs Verification* items are drafted as questions, not findings: *"I could not see where X is applied — is it handled elsewhere?"*
- Ask a question when you may be missing context; assert when you traced it.
- Omit praise-only inline comments; mention a useful engineering strength separately only if it adds information. Comments are drafts, not authorization to post.
