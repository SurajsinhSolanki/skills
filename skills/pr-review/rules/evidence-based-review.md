# Evidence-Based Review

A finding must be supported by one of:

- code evidence (the lines that create the problem)
- an execution path (how input reaches the defect)
- architecture context (a documented pattern or contract the change violates)

Never report "might break" without explaining why.

## Confidence labels

Attach one to every finding that is not trivially verifiable.

**Confirmed** — The code clearly creates the problem. You can name the inputs and the wrong outcome.

**Likely** — Strong evidence exists, but it depends on a call site, config value, or runtime condition you could not read.

**Needs Verification** — Insufficient context. Say what you would need to check, and ask.

## Anti-hallucination rules

- Quote or cite the exact line you are reviewing. If you cannot cite it, you cannot report it.
- Do not assert that a function, migration, index, env var, or test exists unless you read it.
- Do not assume a framework applies protection (CSRF, mass-assignment guards, parameterized queries) — verify it in this codebase.
- If a claim depends on code outside the diff, read that code. If unavailable, use Likely only when other evidence is strong and the dependency is explicit; otherwise ask a Needs Verification question. Never label the missing evidence Confirmed.
- Establish causality, not just changed-line membership: a changed callee can break an unchanged caller. Cite both and anchor inline feedback to the causal change.
- Distinguish "the diff does not show X" from "X is missing". Unchanged code may already handle it.

## Failure-scenario test

Before writing a finding, state it as: *given these inputs / this state → this wrong output or crash.* If you cannot fill that in concretely, it is not a finding — it is at most a suggestion.
