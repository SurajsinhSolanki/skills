# Production Thinking

Run these questions against every non-trivial change. Each one that has no answer in the code is a candidate finding.

## Failure
What happens if this fails halfway? Is state left consistent?

## Retry
What happens if the request, job, or webhook runs twice? Is the operation idempotent?

## Concurrency
What happens with simultaneous requests on the same row, file, or key? Is there a lock, a unique constraint, or an optimistic-concurrency check?

## Data
Can existing production data break this code? Nulls in newly-required columns, legacy enum values, rows written before the new invariant existed.

## Deployment
Can this deploy safely? Does old code run against the new schema during rollout, or new code against the old schema?

## Rollback
If this is reverted after an hour of traffic, does the data written in that hour still make sense?

## Blast radius
Who else calls the changed function or endpoint? What breaks if the contract shifted?

## Monitoring
When this fails in production at 3am, will anyone know? Is the failure logged with enough context to diagnose it?

## Limits
What happens at 10× the expected volume — rows, file size, concurrent users, payload length?
