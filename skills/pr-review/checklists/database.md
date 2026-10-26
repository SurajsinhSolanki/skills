# Database & Data Integrity

## Queries

- Is the query correct — joins, filters, null handling, ordering determinism for pagination?
- Are the filtered/sorted columns indexed? Check the migration history, don't assume.
- **N+1** — a query inside a loop, or lazy-loaded relations iterated in a template/serializer.
- Unnecessary queries — refetching data already in memory; counting when existence is enough.
- Unbounded result sets — no `LIMIT` on a table that grows.
- `SELECT *` where the row is wide and only two columns are used.

## Transactions

- Are multi-write operations atomic, or can they leave half-written state?
- Does the transaction boundary cover the whole invariant, and only that?
- Are external calls (HTTP, queue publish, email) made *inside* a transaction where they cannot be rolled back?
- Is rollback behavior correct on exception — including in background jobs and nested calls?
- Is the transaction held open across slow I/O, holding locks?

## Migrations

- Is it safe to deploy while the old code is still running? (add-then-backfill-then-enforce, not rename-in-place)
- Adding a NOT NULL column without a default to a populated table will fail or lock.
- Does it take a lock that blocks writes on a large table?
- Is existing data valid under the new constraint? Is there a backfill, and is it batched?
- Is there a down migration, and does it lose data?
- Do enum/type changes match what the application code expects on both sides of the deploy?

## Concurrency & integrity

- Duplicate writes — is there a unique constraint, or only an application-level "check then insert" race?
- Read-modify-write on a counter or balance without a lock or atomic update.
- Are foreign keys and cascade rules correct? A cascade delete that removes audit history is a data-loss finding.
- Are soft-deleted rows filtered everywhere they should be?
- Are timestamps stored in UTC with a consistent type?
