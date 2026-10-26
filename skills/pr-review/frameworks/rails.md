# Ruby on Rails Review

Contents: [Applicability and offline use](#applicability-and-offline-use) · [ActiveRecord](#activerecord) · [Transactions and callbacks](#transactions-and-callbacks) · [Controllers and security](#controllers-and-security) · [Migrations](#migrations) · [Jobs and caching](#jobs-and-caching) · [Ruby](#ruby) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Ruby on Rails/ActiveRecord and the actual job backend. Inspect Rails/Ruby versions, database adapter, Active Job versus raw Sidekiq invocation, transaction-enqueue options, and time-zone settings. Do not assume PostgreSQL DDL on another adapter.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## ActiveRecord
- **N+1**: `includes`/`preload`/`eager_load` missing where a loop or a serializer touches an association. Check views and JSON builders, not just controllers.
- `includes` vs `preload` vs `eager_load` — `includes` plus a `where` on the association silently switches to a join and can drop rows.
- `.count` (queries every call) vs `.size` vs `.length`; `.exists?` instead of `.present?` on a relation.
- `.all` / `.each` on a large table instead of `find_each`/`in_batches`.
- **SQL injection** via string interpolation: `where("name = '#{params[:q]}'")`, `order(params[:sort])`, `pluck(params[:col])`. Use bind parameters and an allowlist for column names.
- `update_column`/`update_columns`/`save(validate: false)`/`insert_all` skip validations and callbacks — sometimes intended, often a data-integrity bug.
- A new default_scope changes default relation behavior, but unscoped can bypass it. Check associations, explicit bypasses, and tenant invariants instead of assuming a scope protects every query.
- Missing DB-level constraint behind a `validates_uniqueness_of` — the validation races, only a unique index prevents duplicates.
- `dependent: :destroy` vs `:delete_all` — one runs callbacks, the other does not; both can remove data you wanted to keep.
- Enum defined with integer mapping — reordering the array changes the meaning of existing rows.

**Evidence and correction:** Inspect executed query shape, relationship cardinality, constraints, and serialization overrides. A new validation may still race without a unique constraint. Parameterize values and allowlist executable identifiers; measure repeated relation evaluation before prescribing a preload.

## Transactions and callbacks
- Side effects (emails, HTTP calls, job enqueues) inside a transaction — use `after_commit`, otherwise a rollback still sent the email, or the job runs before the row is visible.
- `after_save` vs `after_commit` confusion in a diff that adds a job enqueue.
- Callbacks doing business logic that belongs in a service object — flag when a callback chain becomes hard to follow or fires on unrelated updates.
- `raise ActiveRecord::Rollback` swallowed silently; a rescue inside a transaction block that prevents rollback.
- `lock!`/`with_lock` used for read-modify-write on counters and balances.

**Evidence and correction:** Trace save/callback/commit ordering and the queue adapter’s transaction behavior. Demonstrate an effect delivered after rollback or a worker observing an uncommitted row; use commit-safe dispatch or an outbox where delivery guarantees require one.

## Controllers and security
- Strong parameters must enforce the writable contract for the authenticated role. permit! is a candidate: trace whether privileged keys actually reach mass assignment. Administrative endpoints may intentionally accept fields forbidden to ordinary users.
- Authorization (Pundit `authorize`, CanCan `load_and_authorize_resource`) present on every action, not only the index. Verify scoping in `policy_scope`/`accessible_by`, otherwise `find(params[:id])` is an IDOR.
- `params[:id]` looked up on the global scope rather than through the current user's association.
- `skip_before_action :verify_authenticity_token` — needs a stated reason.
- Inspect model serialization overrides and serializer options before asserting that render json exposes a sensitive field. Narrow fields where the actual output exceeds the public contract.
- Mass responses without pagination.
- Strong `filter_parameter_logging` for passwords and tokens.

**Evidence and correction:** Test each action with another owner’s ID and extra privileged fields. Existing before_action/policy scopes can satisfy authorization. render json can be narrowed by serialization overrides; inspect actual output before asserting every column leaks.

## Migrations
- Determine the database/version and generated DDL before estimating lock/rewrite impact. PostgreSQL concurrent indexes have special transaction constraints; constant defaults can avoid rewrites on supported versions. Other adapters have different online-DDL mechanisms.
- `NOT NULL` added without a backfill in a prior deploy.
- Data migration inside a schema migration, using model classes that will change later — inline a minimal class or use raw SQL.
- Irreversible migration with no `down`.
- Index added in the migration but the query still not sargable.

**Evidence and correction:** Compare generated DDL, table scale, old/new app compatibility, and recovery. Concurrent-index requirements apply only to supporting adapters; a constant default is not inherently a rewrite on all database versions.

## Jobs and caching
- Raw Sidekiq arguments should be supported JSON values, commonly record IDs. Active Job supports records through GlobalID: verify later reloading, deletion handling, and whether the job needs current state or an immutable snapshot.
- Idempotency: jobs are retried, so double-charging, double-emailing, and double-inserting must be impossible.
- `retry_on`/`discard_on` configured; a job that raises forever with no dead-letter path.
- Long-running job with no batching or checkpoint.
- Cache keys that omit an input (user, locale, feature flag), so one user's fragment is served to another.
- `Rails.cache.fetch` without an expiry on data that changes.

**Evidence and correction:** Inspect serialized arguments and retries in the actual API. GlobalID records reload at execution; raw Sidekiq needs JSON-compatible arguments. Define deleted-record and repeated-delivery behavior, and key mutable caches by all inputs affecting the result.

## Ruby
- `Time.now`/`Date.today` instead of `Time.current`/`Date.current` — wrong timezone in a Rails app.
- `rescue => e` with no re-raise and no logging; `rescue Exception`.
- Symbol vs string keys on params and JSON.
- `method_missing`/`define_method` metaprogramming that defeats grep — flag when it hides business logic.
- Frozen string mutation; `<<` on a shared constant.

**Evidence and correction:** Check time-zone context, exception ownership, JSON key handling, and mutation of shared constants. Metaprogramming alone is not defective; trace its callers and cite the invariant it obscures or violates.

## Worked example and counterexample

```ruby
# Active Job: supported GlobalID argument, reloaded when performed.
NotifyJob.perform_later(account)
# Raw Sidekiq: pass JSON-compatible identity, reload explicitly in perform.
NotifyWorker.perform_async(account.id)
```

Both need a defined outcome if the record disappears before execution. For a job requiring the historical state, pass an explicit supported immutable snapshot instead of assuming GlobalID stores that state.

## Sources and maintenance

[Active Job serialization](https://guides.rubyonrails.org/active_job_basics.html). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
