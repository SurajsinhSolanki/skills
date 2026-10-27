# Risk-based scenarios and test quality

## Applicable scenario families

Use the feature contract and existing coverage to select scenarios. The matrix
is a menu, not a requirement to implement every case or artificial failure mode.

| Family | Relevant scenarios | Observable evidence |
|---|---|---|
| Success | Normal, minimal/maximal valid inputs, valid combinations, repeated operations | Correct result, persisted state and documented side effects. “No exception” alone is usually weak. |
| Validation | Missing/null/empty/whitespace, wrong type/format, boundary/negative/oversized values, invalid references, duplicates | Contractual error and no unintended state change. Unicode/normalization rules need actual requirements; do not assume all non-ASCII input is invalid. |
| Business/state | Invalid transitions, conflicts, completed/deleted/disabled resources, unauthorized business actions | Invariants remain true; explicit result or failure. Test idempotency only where the operation requires it. |
| Database | Not found, constraints, duplicate/stale/related records, timeout, transaction/connection failure, partial writes | Consistency, rollback/recovery where required, useful bounded errors. A mocked repository exception does not prove the real database transaction rolled back. |
| Authentication/authorization | Missing/expired credentials, forbidden roles, another owner/tenant, privilege escalation | Actual enforcement at the trust boundary and no data disclosure/side effects. Hiding UI is not a server access-control test. |
| External service | Success, timeout, connection failure, 4xx/5xx, malformed/empty response, rate limiting, unavailable service | Correct mapping, bounded retries, no duplicate effects; distinguish a contract stub from a live provider test. Do not retry every 4xx automatically. |
| Error handling | Expected errors, unexpected failures, logs, resource cleanup, partial processing | Safe result, appropriate status/shape, redacted diagnostics and data consistency. Do not demand HTTP status codes for a non-HTTP library. |
| Edge/lifecycle | Empty/large datasets, special characters, ordering, concurrent/retried requests, slow dependencies, restart/resume | Contractual boundaries, concurrency safety and recovery. Avoid speculative stress testing without an applicable requirement. |

Give important rows explicit statuses: covered by existing test, new test passing,
new test failing, inspected only, blocked/not run, or not applicable. Coverage of
one row at one level does not establish every path or real-service behavior.

## Behavior-focused example

Illustrative contract: a rejected update must leave the stored profile unchanged.

```python
def test_blank_name_preserves_existing_profile(profile_service, repository):
    user = repository.create(name="Ada")
    with raises(ValidationError):
        profile_service.rename(user.id, "   ")
    assert repository.get(user.id).name == "Ada"
```

Adapt `raises`, the error type and fixture interfaces to the actual framework.
This is not standalone executable code or a new API contract. Merely asserting
that a private validator was called would not establish the profile invariant.
Interaction assertions are appropriate when interaction itself matters, such as
preventing duplicate sends or ensuring an expensive backend is not contacted.

## Failure investigation

1. Reproduce with the recorded command and relevant state. Compare the baseline
   without discarding user changes; use disposable snapshots where helpful.
2. Classify a failure as implementation regression, pre-existing defect,
   test/expectation error, environment limitation, or unresolved/nondeterministic.
3. Correct a test only with evidence its expectation/setup is wrong. Correct
   implementation only within the authorized mode and selected feature.
4. Keep regression coverage and rerun affected checks. Record both first failure
   and subsequent outcomes; do not equate a successful retry with a resolved flake.

Flakes commonly involve shared state, order dependence, uncontrolled time/randomness,
threads, incomplete teardown, or missing synchronization. Prefer isolated resources,
injected clocks, seeded randomness where appropriate, and waiting for the actual
condition with a bound. A fixed sleep may hide a race and is not proof of completion.

## Safe and meaningful boundaries

- Use temporary databases/files and controlled service responses. Inspect commands
  and config before running tests that might call payment/email/cloud services.
- Exercise real behavior at the most suitable level. Unit mocks cannot establish
  DB constraints, browser accessibility, deployment configuration, or a provider's
  current behavior. Document those coverage limits.
- Do not install tools, introduce credentials, or connect to production to turn a
  blocked test into a pass. Continue available independent checks.
- Check test isolation, assertions, maintainability and whether the new test
  would fail for the relevant bug. Do not add tests that mirror a trivial
  implementation without protecting a meaningful contract.
- Runtime/coverage statistics need actual measurement and context. An isolated
  unit suite's 100% coverage does not establish whole-feature reliability.

## Sources and applicability

Original summaries checked **2026-10-27**. These principles apply across testing
frameworks; pytest details apply to projects actually using pytest. Existing
framework versions, project contracts and test conventions govern implementation.

- [Google: test behavior, not implementation](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html).
- [pytest: flaky tests](https://docs.pytest.org/en/stable/explanation/flaky.html).
