# Python Review

Covers FastAPI, Flask, SQLAlchemy 2 (async), and Pydantic v2, plus general Python. For Django/DRF use `django.md` instead. Skip any section the project does not use.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Layering](#layering) · [FastAPI](#fastapi) · [Async](#async) · [SQLAlchemy 2 (async)](#sqlalchemy-2-async) · [Pydantic v2](#pydantic-v2) · [General Python](#general-python) · [Before approving](#before-approving) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Python 3; inspect pyproject/lockfiles and the actual web framework. SQLAlchemy notes target 2.x async APIs and Pydantic notes target v2. Do not apply those APIs to older dependencies; Flask does not inherit FastAPI dependency or response-model behavior.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Layering
- Follow documented boundaries for handlers, business logic, and data access. Direct session access in a small handler is not inherently defective. Report misplaced responsibility only when it violates an adopted rule or creates a concrete problem such as divergent authorization or transaction handling.
- Repeated derived business values should have one authoritative definition where duplication causes inconsistent results.

**Evidence and correction:** Compare handlers implementing the same invariant. A useful finding names the differing rule and the input producing inconsistent results; the fix may be one local helper rather than a new service/repository layer.

## FastAPI
- Trace dependency scopes for sessions, auth, and services. `Depends()` can manage request-scoped resources; immutable configuration or thread-safe singleton clients are valid when their lifetime is intentional.
- Every mutating endpoint enforces ownership/permission. Verify the dependency actually runs on that route.
- Verify response filtering through a response model, return annotation, or explicit safe serialization. Flag sensitive fields that actually reach a response, not the absence of one decorator option.
- Correct `HTTPException` status codes; no returning error dicts with 200.
- `BackgroundTasks` used for work that must not block the response — but not for work that must not be lost.
- Rate limiting applied on expensive or auth-adjacent routes where the project does so elsewhere.
- Streaming/file responses close their handles.

**Evidence and correction:** Trace the mounted route and dependency chain through serialization. Test a forbidden owner and a response containing a privileged field; fix the actual authorization/filtering seam. Built-in error/validation responses and explicit Response objects need separate inspection.

## Async
- No blocking calls in an `async def` path: sync DB drivers, `requests`, `time.sleep`, heavy CPU work, sync file I/O. Use the async client or offload to a thread.
- A coroutine object must be awaited, scheduled as an owned task, or otherwise consumed. Missing await can leave work unexecuted; deliberate scheduling is valid when lifecycle and errors are owned.
- Trace shared mutable invariants across interleavings. Task confinement, atomic operations, or synchronization may preserve them; a lock is necessary only when the actual invariant needs it.
- `asyncio.gather` results include exceptions when `return_exceptions=True` — verify they are inspected.

**Evidence and correction:** Locate the event loop and resource owner. A synchronous library inside a synchronous worker is valid; the same blocking call on the event-loop path can stall concurrent requests. Bound offloading and preserve cancellation; a lock is unnecessary for immutable state.

## SQLAlchemy 2 (async)
- Session scope: one per request, committed/rolled back exactly once, not passed into background tasks that outlive it.
- Lazy loading on an async session raises or triggers a hidden IO — check for `selectinload`/`joinedload` on relations that get accessed.
- N+1: relations touched in a loop or serializer.
- `flush()` vs `commit()` used deliberately; nested transactions/savepoints correct.
- Bulk operations bypass ORM events — confirm that is intended.
- Raw SQL uses bound parameters, never f-strings.
- Migrations (Alembic or equivalent): autogenerate output reviewed by hand, downgrade present, safe against existing rows, no table-locking op on a large table.

**Evidence and correction:** Check session creation, commit/rollback, closure, and all tasks using it. An AsyncSession is mutable transaction state and should not be shared across concurrent tasks. Preload needed relationships or use supported explicit async access instead of assuming all lazy reads are safe.

## Pydantic v2
- Fields are required unless genuinely optional; `Optional[X]` without a default is still required.
- Validators use v2 syntax (`field_validator`/`model_validator`) consistently.
- Ordinary Python function defaults are shared between calls. Pydantic v2 instead deep-copies unhashable model defaults per instance: `items: list[int] = []` is not by itself shared-state leakage. A factory is useful for computed defaults or clarity; inspect custom/hashable objects and validators before asserting sharing.
- Request and response models are distinct — don't reuse the DB-shaped model as the request body (mass-assignment risk).
- `model_config` strictness matches the project's convention (extra fields forbidden vs ignored).

**Evidence and correction:** Inspect validation and serialization separately: nullable is not the same as omittable. Test omitted, null, and extra fields using the installed model version. Defaults may need validation enabled; a factory is not a substitute for authorization or a correct public field set.

## General Python
- Config lives in one settings object, not scattered `os.getenv()` calls.
- Deferred logging arguments avoid eagerly formatting disabled messages. Report expensive formatting only with relevant frequency/cost; formatting style follows project policy.
- Bare `except:` or `except Exception: pass` — needs a stated reason.
- Mutable default arguments.
- `Any` without justification; `# type: ignore` without a reason comment.
- Resources (files, clients) closed via context managers.
- Check user-derived paths against the allowed root after normalization, including symlink behavior where relevant. `pathlib` and `os.path` are both valid; neither automatically prevents traversal.

**Evidence and correction:** Trace exception handlers and resources on early returns. Reproduce malformed config/path input or a repeated default-argument call before reporting leakage. Naming, logging syntax, and pathlib adoption are policy preferences unless an actual failure or measured cost follows.

## Before approving
Use the project's declared lint/type/test commands under [Running the project's gates](../SKILL.md#running-the-projects-gates). That section governs snapshot matching, authorization, failure attribution, and reporting; a failed command alone does not establish an introduced blocker.

**Evidence and correction:** Use existing project commands and report whether the selected snapshot was actually executed; dependency absence is a verification limit, not evidence of a code defect.

## Worked example and counterexample

```python
# Defect: ordinary function default persists across calls.
def add_bad(value, items=[]):
    items.append(value)
    return items

# Correction when each call needs a fresh collection.
def add_good(value, items=None):
    items = [] if items is None else items
    items.append(value)
    return items
```

Pydantic v2 counterexample: `class M(BaseModel): items: list[int] = []` deep-copies this unhashable model default per instance; do not transfer the function-default finding to it.

## Sources and maintenance

[Python defaults](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values); [Pydantic fields](https://pydantic.dev/docs/validation/latest/concepts/fields/); [SQLAlchemy async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html); [FastAPI responses](https://fastapi.tiangolo.com/tutorial/response-model/). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
