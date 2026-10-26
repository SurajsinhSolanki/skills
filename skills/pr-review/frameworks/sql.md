# SQL Review

Applies to hand-written SQL, raw fragments inside an ORM, views, and migrations. Pair with `checklists/database.md`.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Correctness before performance](#correctness-before-performance) · [Pagination](#pagination) · [Indexes and sargability](#indexes-and-sargability) · [Transactions and concurrency](#transactions-and-concurrency) · [DDL and migrations](#ddl-and-migrations) · [Data modelling](#data-modelling) · [Evidence](#evidence) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

SQL queries, ORM fragments, views, and migrations. Identify engine/version, column types/collation, constraints, isolation, data distribution, and execution-plan source. PostgreSQL-specific commands below are labeled; do not apply them to MySQL, SQL Server, or SQLite blindly.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Correctness before performance
- If a NOT IN subquery contains NULL, an unmatched comparison can become UNKNOWN and be filtered out. An empty subquery and matching values have different results. Test nullable inputs; use correlated NOT EXISTS or explicit null handling when that expresses the intended exclusion.
- `= NULL` / `<> NULL` never match — `IS NULL` / `IS NOT NULL`.
- `LEFT JOIN` followed by a `WHERE` on the right-hand table silently becomes an inner join. The predicate belongs in the `ON` clause.
- **Join fan-out**: joining a one-to-many duplicates left-side rows, which then inflates `SUM`/`COUNT`. Aggregate in a subquery or use `DISTINCT` deliberately, knowing it also masks genuine duplicates.
- Missing join condition producing a cross product.
- `COUNT(col)` skips NULLs; `COUNT(*)` does not.
- Aggregates with a `WHERE` that should have been `HAVING`, or vice versa.
- UNION removes duplicates while UNION ALL preserves them; the engine can use hashing or sorting. Verify intended multiplicity and the actual plan before claiming either a result bug or a sort cost.
- Ordering assumed without an `ORDER BY`; `GROUP BY` does not guarantee order.
- Integer division truncating, and money stored or computed as float.
- Implicit type coercion in a comparison changing which rows match.
- `LIMIT` without `ORDER BY` returns an arbitrary row.

**Evidence and correction:** Construct a tiny dataset containing NULL, duplicate children, unmatched parents, zero, and empty input. Compare expected rows and aggregates before discussing speed. Changing an outer join filter to ON is correct only when unmatched rows should survive; sometimes exclusion is intentional.

## Pagination
- `OFFSET n` scans and discards n rows — degrades linearly. Keyset/seek pagination (`WHERE (sort_key, id) > (:k, :id)`) for anything deep.
- **The `ORDER BY` must be a total order.** Sorting on a non-unique column means rows can appear on two pages or none. Add the primary key as a tiebreaker.

**Evidence and correction:** Choose a deterministic tie-breaker and define behavior while rows change between pages. Keyset pagination can avoid deep offsets but requires compatible ordering and cursor validation; offset is reasonable for small bounded administrative datasets.

## Indexes and sargability
- A predicate wrapped in a function (`WHERE lower(email) = ...`, `WHERE date(created_at) = ...`) cannot use a plain index — needs an expression index or a range rewrite.
- Implicit casts (`WHERE varchar_col = 123`) disable the index.
- `LIKE '%term'` with a leading wildcard cannot use a b-tree index.
- Leading columns usually make a multicolumn B-tree more selective, but other-column predicates can still use the index, including skip-scan optimizations on supporting engines/versions. Inspect the actual plan and distribution instead of asserting it is unusable.
- Sort and filter both served, or the sort spills to disk.
- `OR` across different columns often defeats a single index — consider a rewrite or a union.
- Index added in the diff but unused by the query as written; or a redundant index duplicating an existing prefix.

**Evidence and correction:** Use the actual engine’s planner and representative distribution. Casts/functions/collations can affect usable indexes, but expression indexes and optimizer transformations vary. Recommend a rewrite/index only after identifying a relevant scan, sort, or row-estimate problem.

## Transactions and concurrency
- Read-modify-write without `SELECT ... FOR UPDATE` or an atomic expression — lost update.
- Isolation level assumptions: at read-committed, two reads in one transaction can differ.
- Deadlocks from inconsistent lock ordering across code paths; the fix is a consistent order, not a retry loop alone.
- Long transactions holding locks across application logic or external calls.
- Advisory locks acquired and never released on the error path.
- PostgreSQL ON CONFLICT requires an eligible arbiter for the chosen conflict target. MERGE follows its engine-specific join/action rules and is not universally equivalent to ON CONFLICT. Check concurrent insert semantics and constraints separately.

**Evidence and correction:** Enumerate competing transactions and the invariant they can violate. Atomic updates, row locks, optimistic checks, or serializable isolation can all be valid. Keep external I/O outside critical locks when possible; retry transactions only with safe side-effect handling.

## DDL and migrations
- Locks: adding a column with a volatile default, changing a type, or adding a `NOT NULL` constraint rewrites and locks the table on most engines.
- On PostgreSQL, ordinary CREATE INDEX blocks writers; CONCURRENTLY allows writes with its own waits/failure modes and cannot run in a transaction block. Other engines have different online-index syntax and locking. Choose from the actual engine/version and deployment window.
- PostgreSQL supports NOT VALID for eligible CHECK/foreign-key constraints, not every constraint kind; later validation still takes locks. Verify eligible DDL, old-row semantics, and lock duration before recommending staged validation.
- Dropping or renaming a column while the old application version is still running.
- Enum/type changes: adding a value is usually safe, reordering or removing is not.
- Cascade rules: `ON DELETE CASCADE` that reaches audit or history tables is data loss.
- Backfills batched with a bound and a sleep, not one statement over the whole table.

**Evidence and correction:** Determine lock acquisition, table rewrite, old-row validation, and overlapping application versions. PostgreSQL CONCURRENTLY and NOT VALID are targeted tools with eligibility limits, not universal migration syntax. Inspect the recovery plan for partial/failed DDL.

## Data modelling
- `timestamptz` vs `timestamp` — storing local time without a zone is unrecoverable ambiguity.
- Nullable columns that encode two meanings ("unset" and "explicitly empty").
- Soft-delete flags with no partial index and no consistent filter, so deleted rows leak into some queries.
- Case sensitivity and collation on a column used for uniqueness of emails or usernames.
- Missing `NOT NULL` and missing foreign keys where the application assumes both.

**Evidence and correction:** Test null/empty distinctions, deletion scope, and normalized uniqueness values. Timestamp storage needs a domain decision: an instant differs from a local recurring appointment. A soft-delete index is a performance choice; consistently excluding deleted rows is a correctness contract.

## Evidence
For any performance claim, cite `EXPLAIN` (or `EXPLAIN ANALYZE`) output or the row-count scale that makes it matter. A guess about the plan is a Needs Verification note, not a finding.

**Evidence and correction:** Use supplied plans or an authorized read-only EXPLAIN. EXPLAIN ANALYZE executes the statement; do not run it on production writes as part of a review. Missing plan evidence is a limitation, not permission to claim a guessed index strategy.

## Worked example and counterexample

```sql
-- A NULL inside blocked makes unmatched NOT IN comparisons UNKNOWN.
SELECT id FROM users WHERE id NOT IN (SELECT user_id FROM blocked);
-- Correction when the contract is “exclude matching IDs”.
SELECT u.id FROM users AS u
WHERE NOT EXISTS (SELECT 1 FROM blocked AS b WHERE b.user_id = u.id);
```

Use fixtures with a NULL blocked.user_id to establish the difference; do not change nullable-key semantics without checking the intended result.

## Sources and maintenance

[NULL subqueries](https://www.postgresql.org/docs/current/functions-subquery.html); [Index creation](https://www.postgresql.org/docs/current/sql-createindex.html); [Multicolumn indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
