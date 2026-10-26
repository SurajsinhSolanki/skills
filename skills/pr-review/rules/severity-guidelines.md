# Severity Classification

`SKILL.md` carries the short version of this scale and the verdict mapping. This file is for borderline cases.

## [CRITICAL] — blocking when Confirmed

- security vulnerability (authn bypass, authz gap, injection, secret exposure)
- data corruption or data loss
- production outage or crash on a normal path
- severe authorization failure (cross-tenant or cross-user access)

## [HIGH] — blocking when Confirmed

- incorrect business behavior against the stated requirement
- major regression in existing functionality
- serious reliability issue (unhandled failure on a common path, non-idempotent retry)
- migration that is unsafe to deploy

## [MEDIUM] — important, usually non-blocking

- a real edge case that will occur in production but is recoverable
- maintainability risk that will cost the next change (duplicated business logic, wrong layer)
- limited-impact bug on an uncommon path

## [LOW]

- minor improvement with practical value: naming that misleads, a missing log line, a dead branch

## [SUGGESTION]

Optional improvement. Never present a suggestion as a bug, and never let suggestions gate a merge.

## Verdict mapping

[SKILL.md](../SKILL.md#severity) is authoritative for severity-to-verdict decisions, confidence, required-gate failures, and INCOMPLETE reviews. Do not infer blocking from severity alone without verifying causality and confidence.

Severity reflects production impact, not how much the code annoys you.
