# Risk and acceptance planning

Use relevant concerns to make a task executable. This is not a requirement to
add security, database, deployment or performance work to every request.

| Concern | Establish locally | Specify in the plan |
|---|---|---|
| Backend/business logic | Existing routes, validators, domain rules, transactions, errors and reusable services | Intended behavior, affected boundaries, failure outcomes and meaningful tests. Do not invent a new architecture layer. |
| Frontend | Current components, routing, API clients, state, permissions and project design conventions | Relevant user flow, loading/error/empty states, accessibility and responsive behavior. Do not introduce a design system for a minor feature. |
| API/compatibility | Existing request/response/error contracts, clients, versions and external consumers | Explicit proposed changes; compatibility/migration period when needed; errors and consumer regression tests. |
| Authentication/authorization | Actual auth model, roles, ownership and tenant boundaries | Server-side checks where applicable, positive and forbidden access tests; no reliance solely on hidden UI. Flag required specialist review when the risk warrants it. |
| Data integrity | Schema, constraints, nullability, duplicates, references, indexes and migration conventions | Compatibility, backfill, transaction/partial failure behavior, migration ordering, rollback or forward recovery. Historical applied migrations are not disposable cleanup. |
| External integration | Client contract, credentials source, provider guarantees and existing test doubles | Timeouts, retry eligibility, malformed responses, rate limits, idempotency and safe verification. Mark unverified provider behavior; do not require live production credentials for tests. |
| Async/queues | Producer/consumer behavior, retry/dead-letter configuration and transactions | Duplicate delivery, out-of-order/partial processing, job recovery, side-effect idempotency and relevant observability. Avoid inventing exactly-once guarantees. |
| Security/privacy | Reachability, input trust, access controls, sensitive fields and applicable requirements | Concrete abuse/failure cases and handling of logs/secrets/audit events. Avoid copying a generic mandatory security checklist into unrelated tasks. |
| Performance | Actual queries, data volume, N+1 risk, resource use and measurable requirements | Appropriate measurement and workload, success threshold grounded in a requirement, resource cleanup and regression checks. No speculative caching or services. |
| Deployment/operations | Actual build/runtime config, environments, service dependencies, flags and runbooks | Relevant ordering, compatibility, configuration, monitoring and recovery steps. A planned deployment does not authorize executing it. |

## Observable acceptance

Weak: “The API is robust.”

Stronger, when consistent with the product contract: “A duplicate submission with
the same idempotency key returns the original result and creates no second payment.”
Define the observable response and side-effect assertions. Do not invent
idempotency as a new product requirement for an unrelated read-only endpoint.

For a performance task, define a representative workload and a justified target;
when neither is known, plan measurement first. “Fast” alone is not verifiable.

For compatibility-sensitive work, state which old inputs/clients/data remain
supported and how the changed behavior will be introduced. Recovery may require
a forward fix or restore procedure; not every data migration is reversibly undone.

Separate executed evidence from planned verification. If tests or infrastructure
cannot be inspected, record that limit and which decision depends on it. Do not
create a passing verification record in advance.

## Source and applicability

Original adaptation of the maintainer's planning prompt under MIT, checked
**2026-10-27**. Applies according to the project's actual architecture and
requirements; no particular framework, security standard or deployment tool is
mandated by this reference.
