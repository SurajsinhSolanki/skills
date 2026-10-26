# Django Review (Django · DRF)

Contents: [Applicability and offline use](#applicability-and-offline-use) · [ORM](#orm) · [Migrations](#migrations) · [DRF and security](#drf-and-security) · [Views, transactions, signals](#views-transactions-signals) · [Settings and files](#settings-and-files) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Django ORM and DRF with the installed database backend. Confirm Django/DRF versions, ATOMIC_REQUESTS, permission defaults, and serializer overrides. Locking and concurrent-index notes are backend-specific, especially PostgreSQL versus SQLite.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## ORM
- **N+1**: `select_related` (FK, one query join) and `prefetch_related` (M2M/reverse, second query) missing where a loop, template, or serializer walks a relation.
- Querysets are lazy: a `filter` in a loop issues a query per iteration. `.exists()` over `.count()` over `len()`.
- `.iterator()` / `Paginator` for large result sets instead of loading everything.
- `only()`/`defer()` misuse causing extra queries on deferred attribute access.
- Evaluating `select_for_update()` in autocommit raises `TransactionManagementError` on backends supporting row locks; SQLite ignores the locking clause. Django `TestCase` can mask the missing transaction because it wraps the test. Verify backend and active transaction, using `TransactionTestCase` where appropriate.
- `F()` expressions for atomic increments instead of read-then-write.
- `get_or_create`/`update_or_create` race without a unique constraint behind it.
- Bulk operations bypass Model.save and model save signals. Field defaults/pre_save behavior differs between bulk insert and update; inspect generated values rather than asserting all auto_now fields are always skipped.
- Raw SQL via `.raw()`, `.extra()`, `RawSQL` with interpolated input — injection. `annotate` with user-supplied field names.
- Missing `db_index` on a field the new query filters or orders by; missing `unique_together`/`UniqueConstraint`.

**Evidence and correction:** Follow queryset evaluation through serializers/templates and measure query count for multiple rows. exists/count/materialization each have valid uses depending on whether results are later consumed. Check actual constraints and backend transaction behavior before recommending locks or indexes.

## Migrations
- `AddField` non-null without a default, or a default that rewrites the whole table.
- `RunPython` without a reverse function, or a data migration that loads every row into memory.
- Data migration referencing the live model class instead of `apps.get_model`.
- Index creation on a large table without `AddIndexConcurrently` (Postgres) and `atomic = False`.
- Two migration leaves needing a merge.
- Migration and code deployed together where the code requires the column immediately — check the rollout order.

**Evidence and correction:** Inspect historical model access, reverse behavior, table size, and application compatibility across deploy order. A deliberately irreversible cleanup can be valid with an accepted recovery plan; absence of a down function alone does not prove data loss.

## DRF and security
- DRF generic detail views call object checks through `get_object()`; custom overrides must preserve them. List views do not automatically check every object: scope querysets. Creation needs view/serializer/perform_create enforcement. A global allow-all versus authenticated permission is not itself ownership enforcement; trace the actual policy before claiming IDOR.
- `DEFAULT_PERMISSION_CLASSES` — if it is `AllowAny`, every view without an explicit class is public. Check the settings, not the view.
- `fields = '__all__'` expands the serializer’s model-field surface; inspect actual output, field overrides and read-only settings. Flag a privileged field only when the new request/response path exposes or writes it without the required policy.
- Field-specific validation uses `validate_<field>`; cross-field validation belongs in `validate(self, attrs)` or an equivalent service invariant. Confirm the save path validates before writing.
- Filtering/ordering backends accepting arbitrary field names — allowlist them.
- Pagination configured, otherwise a list endpoint returns the table.
- `SessionAuthentication` for a cookie-based SPA requires CSRF; token auth in a cookie without `HttpOnly`.
- Throttling on auth and expensive endpoints.

**Evidence and correction:** Test list, retrieve, create, and update separately with another owner’s ID. Check custom get_object overrides and queryset scoping. Inspect actual writable/output serializer fields: __all__ can be intentionally read-only and does not alone prove privilege escalation.

## Views, transactions, signals
- `transaction.atomic` around multi-write operations; `transaction.on_commit` for emails, jobs, and webhooks so a rollback does not fire them.
- `ATOMIC_REQUESTS` interaction — if enabled, the whole view is one transaction and external calls sit inside it.
- Trace signal registration, sender, raw fixture loads, historical migration models, and bulk paths separately. Report an unintended or missing effect on an actual path; using a signal rather than a service is not inherently wrong.
- Custom middleware order, and middleware storing request state on `self` (the instance is reused across requests — a cross-request leak).
- `get_object_or_404` used rather than an unguarded `.get()` that raises a 500.

**Evidence and correction:** Trace both commit and rollback, including on_commit callbacks and middleware ordering. Signals may intentionally enforce invariants; report duplicate/unexpected effects with a concrete save path. Verify not-found handling at the request boundary before calling .get() a 500.

## Settings and files
- `DEBUG = True`, a hardcoded `SECRET_KEY`, or `ALLOWED_HOSTS = ['*']` reaching a non-local settings module.
- `CORS_ALLOW_ALL_ORIGINS`, `CSRF_TRUSTED_ORIGINS` widened.
- `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS` weakened.
- `USE_TZ` and naive datetimes: `datetime.now()` instead of `django.utils.timezone.now()`.
- Uploads: extension/content-type/size validated, filename sanitized, stored outside the web root, never served by Django in production.
- Templates: `|safe` and `mark_safe` with user data; `{% autoescape off %}`.
- Cache keys including user/tenant identity; per-user data cached under a shared key.
- New setting added with no entry in the env example, so the deploy boots without it.

**Evidence and correction:** Identify production settings selection, reverse proxy behavior, upload storage and cache identity. A development fixture SECRET_KEY or wildcard host with validated upstream routing is different from an exposed production secret or untrusted host path.

## Worked example and counterexample

```python
# Custom DRF detail lookup must keep both scoping and object checks.
def get_object(self):
    obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
    self.check_object_permissions(self.request, obj)
    return obj
```

A supporting database evaluates select_for_update inside a real transaction; SQLite cannot validate row-lock behavior. Use an appropriate backend/test transaction when assessing a concurrency fix.

## Sources and maintenance

[Queryset locking](https://docs.djangoproject.com/en/4.0/ref/models/querysets/#select-for-update); [DRF permissions](https://www.django-rest-framework.org/api-guide/permissions/); [Generic views](https://www.django-rest-framework.org/api-guide/generic-views/). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
