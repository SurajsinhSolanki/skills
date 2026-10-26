# Tests

## Required coverage for a change

- The main behavior described in the ticket.
- Invalid and boundary input — null, empty, too long, wrong type, out of range.
- Permission failures — unauthenticated, wrong owner, wrong tenant/role.
- Failure scenarios — dependency down, timeout, transaction rollback.
- Regression risk — the behavior most likely to break that the change touches.

## Quality

- Prefer behavior tests at a public seam over tests asserting internal calls.
- A mock-call assertion may verify an interaction contract, but it does not by itself prove the resulting user-visible behavior. Judge it against the behavior the test intends to cover.
- Are shared fixtures/factories used, or is setup copy-pasted?
- Are repeated cases parameterized rather than duplicated?
- Do the assertions actually fail when the behavior breaks? A test with no meaningful assertion is worse than none.
- Are snapshots minimal and reviewed, not blanket dumps?
- Is the test deterministic — no real clock, no real network, no ordering dependence between tests?

## Reporting gaps

Name the missing scenario and why it matters, not the count. "No test covers a second caller with the same idempotency key, which is the exact bug this PR fixes" beats "coverage is low".

Do not demand tests for trivial, well-typed pass-through code.
