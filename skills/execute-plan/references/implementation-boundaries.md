# Implementation boundaries and completion

## Apply relevant engineering requirements

| Concern | Inspect and implement within the selected task |
|---|---|
| Backend/business rules | Existing routing, validation, services, data access, errors and transactions. Follow the actual architecture; do not add controller/service/repository layers merely because a template lists them. |
| Frontend | Existing components, forms, routing, state, API clients, loading/error/empty states, accessibility and responsiveness. Reuse the current UI framework and design system. |
| API compatibility | Current consumers, request/response/error contracts, validation and authorization. Identify intentional breaking changes, migration/compatibility period and recovery where required. No incidental public-contract changes. |
| Data/migrations | Actual schema, constraints, indexes, records and migration conventions. Prefer a new migration over rewriting one potentially applied; honor an explicitly documented editable workflow. Preserve data and document ordering, backfill, partial failure and rollback/forward recovery. |
| Auth/security | Authentication, roles, ownership, resource-level access and tenant isolation at the relevant trust boundary. Test permitted and forbidden behavior; a hidden button is not server-side authorization. Protect secrets and sensitive logs. |
| Errors | Relevant invalid/missing/duplicate/forbidden input, timeout, external/DB failure, resource cleanup and partial completion. Follow existing error contracts and avoid disclosing internal secrets. Do not add unreachable defensive branches without a real boundary. |
| Integration | Existing clients, provider contracts, credentials, timeouts, retry eligibility and malformed responses. Preserve idempotency where required. Do not contact real users or production services as a local test. |
| Jobs/async | Actual producer/worker boundaries, retry/dead-letter behavior, duplicates, transactions, resource lifecycle and logs/metrics. Retry must not create unintended duplicate side effects. |
| Performance | Actual workload/requirements, queries, N+1 patterns, large loops, resource use and network requests. Measure requested targets; do not add speculative caches or services. |
| Operations/docs | Relevant config, environment variables, API docs, migration/service order, feature flags, monitoring and recovery instructions. Writing these artifacts is distinct from deploying or applying them to live systems. |

## Match evidence to criteria

Use existing tests at the useful level: unit for business rules; integration for
real boundaries/transactions; API for contracts/access; UI for interaction; E2E
for an important journey when applicable. Do not mandate every level for every
task. Tests should protect meaningful behavior and remain deterministic.

For each criterion, track the evidence and outcome. Example:

| Criterion | Evidence | Outcome |
|---|---|---|
| Blank name rejected without changing stored data | Focused behavior test ran | Verified |
| Existing valid names remain supported | Existing regression suite ran | Verified |
| Product owner manually approves copy | No approval supplied | Not verified; QA remains open |

This illustration does not establish actual project behavior. If the last row
is a required completion gate, do not mark the task done based on the first two.
If manual approval is optional, state that distinction instead of inventing a
blocker. Follow the project's actual acceptance requirements.

## Readiness and conflicts

- Read dependencies beyond labels: a task marked ready may rely on an unfinished
  schema or unavailable approved contract. Identify cycles and missing required
  inputs rather than starting an arbitrary different task.
- A missing renamed source file can be a harmless adaptation. An obsolete plan
  that asks to store plaintext passwords is a material conflict, not permission
  to weaken the current system. Report and seek the missing decision.
- A small helper necessary to the selected behavior can be in scope. Implementing
  a separate payment platform, auth system or another roadmap task is not an
  implicit prerequisite exception. Record the blocker.
- Preserve work already completed, user changes and stable task identifiers. Do
  not rewrite the roadmap's intent or format just because implementation differs
  from an old example path.

## Failure attribution and status

Record actual command, working-tree state and result. Compare against baseline
without resetting user work. Use disposable snapshots when an exact committed
comparison is necessary; do not mistake a dirty-tree result for committed-head
verification.

An unrelated existing test failure should be disclosed, not “fixed” by expanding
scope. Determine whether the project's completion gate applies to it. An introduced
failure or unverified required acceptance condition keeps the task incomplete.
Environment failures are not confirmed product regressions, but may prevent a
required criterion from being verified. State both facts.

Preserve the project's status vocabulary. If no formal vocabulary exists, use a
plain statement of completed, in progress, blocked or awaiting verification, with
evidence. A phase is complete only when every required task and phase criterion
is satisfied. Recommend the next unblocked task without automatically executing it.

## Source and applicability

Original adaptation of the maintainer's execution prompt under MIT, checked
**2026-10-27**. Applies to the selected task and actual project requirements;
does not mandate a framework, deployment model, report template or test quota.
