# Laravel / PHP Review

Pair with `sql.md` when the diff contains raw queries.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Request path](#request-path) · [Eloquent & data](#eloquent--data) · [Migrations](#migrations) · [Jobs, events, and mail](#jobs-events-and-mail) · [Output & security](#output--security) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Laravel/PHP with installed framework, queue driver, PHP version, middleware groups, and config-cache setup. Queue model reloading and after-commit dispatch depend on framework/connection/job options; use their local configuration.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Request path
- Verify validation runs before side effects. Form Requests and inline `$request->validate()` are both supported; require one organization only when the project adopts it or duplication causes divergent validation.
- Authorization via Policies/Gates and enforced (`authorize()`, `can` middleware) — not just hidden in the UI.
- Route model binding scoped to the owner/tenant, otherwise it is an IDOR.
- Follow adopted controller/service boundaries; report a concrete responsibility or consistency problem instead of requiring a service/action for every endpoint.

**Evidence and correction:** Trace validation and authorization before the controller writes or dispatches work. Form Requests, inline validation, policies, and middleware can all enforce the rule. Test another tenant’s bound model ID; fix the missing scope/check instead of mandating an action/service class.

## Eloquent & data
- N+1: eager load with `with()`; check Blade loops and API resources for lazy relations.
- Mass assignment: `$fillable`/`$guarded` correct; never `Model::create($request->all())` on a model with privileged columns.
- Query scopes applied for tenant/soft-delete filtering everywhere, including raw queries and joins.
- `DB::raw` / `whereRaw` with interpolated input is SQL injection.
- Transactions wrap multi-write operations; `DB::transaction` closure returns are handled and external calls are outside it.
- Chunking (`chunkById`) for large iterations instead of `all()`.

**Evidence and correction:** Inspect accepted fields, global scopes, raw fragments, query counts, and transaction rollback. Demonstrate a privileged writable attribute or user input interpolated into executable SQL. Bind values and allowlist identifiers; an ORM call is not automatically safe.

## Migrations
- Safe to run against production volume; no blocking alter on a large table.
- Column additions nullable-or-defaulted; backfill separate and batched.
- `down()` present and non-destructive where possible.

**Evidence and correction:** Read generated database operations against the actual adapter/version and deploy overlap. Establish data size, lock behavior, backfill strategy, and recovery. An intentionally irreversible migration needs an accepted recovery path rather than a pretend reversible down method.

## Jobs, events, and mail
- Jobs are idempotent and have `$tries`/`$backoff`/`$timeout` set.
- Serialized models are re-fetched at run time (`SerializesModels`) — deleted rows must be handled.
- Bound request latency according to the endpoint contract. Use queues for work allowed to complete later; synchronous work can be correct when the response must include its result.
- Events/listeners not creating hidden ordering dependencies.

**Evidence and correction:** Identify when dispatch occurs relative to commit and what the worker reloads. A missing/deleted record and a duplicate delivery are separate cases. Choose after-commit delivery and idempotency where needed; configured connection defaults may already supply retry settings.

## Output & security
- Blade `{{ }}` escapes; `{!! !!}` with dynamic content is XSS.
- API Resources control the response shape so model columns cannot leak.
- CSRF middleware not excluded for convenience.
- Config via `config()` with cached-config safety, not `env()` outside config files.

**Evidence and correction:** Trace the actual response template/resource and configuration cache. Sanitized trusted raw HTML can be valid; unsanitized attacker input is the exploit. Use config values at runtime when env reads would fail after cached deployment.

## Worked example and counterexample

```php
// Defect: worker can observe a row before its transaction commits.
DB::transaction(function () use ($invoice) {
    $invoice->save();
    SendInvoice::dispatch($invoice);
});
// Correction when dispatch is not already configured after commit:
SendInvoice::dispatch($invoice)->afterCommit();
```

Put the corrected dispatch in the transaction at the same point as the original. Verify the queue connection’s after_commit default first; model deletion before execution still needs a defined outcome.

## Sources and maintenance

[Queue serialization and commit timing](https://laravel.com/framework/docs/12.x/queues). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
