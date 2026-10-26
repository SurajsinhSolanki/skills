# .NET Review (ASP.NET Core · EF Core)

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Async correctness](#async-correctness) · [EF Core](#ef-core) · [Dependency injection](#dependency-injection) · [Web pipeline and security](#web-pipeline-and-security) · [Language and runtime](#language-and-runtime) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

C#/.NET, ASP.NET Core, and EF Core. Inspect target framework, nullable settings, EF provider/version, DI registrations, and host lifecycle. Legacy ASP.NET synchronization contexts and older EF client evaluation differ from modern ASP.NET Core.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Async correctness
- **`async void`** anywhere but an event handler — exceptions cannot be caught and crash the process.
- `.Result` / `.Wait()` / `.GetAwaiter().GetResult()` on an async call — deadlock risk and thread-pool starvation under load.
- `CancellationToken` accepted by the action but not passed down to EF Core and HTTP calls, so a cancelled request keeps working.
- Unowned background work may outlive the request while using disposed scoped services, lose failures, or be killed at process shutdown. Use an owned background service/queue when work must survive requests; Task.Run is not automatically cancelled at request end.
- `Task` returned without `await` inside a `using` block: the scope disposes before completion.
- Sync-over-async in a middleware or filter.

**Evidence and correction:** Follow completion, disposal, cancellation, and exception ownership through each Task. Show a disposed service access, unobserved failure, or blocked pool under meaningful load; a Task.Run does not automatically end with its request. Await inside the owning scope or hand work to an owned service.

## EF Core
- **N+1** from lazy loading or from projecting inside a loop; use `Include`/`ThenInclude` or a projection.
- Missing `AsNoTracking()` on read-only queries — tracking overhead and accidental updates on `SaveChanges`.
- `SaveChanges` inside a loop instead of one call.
- Client-side evaluation: a `Where` the provider cannot translate silently pulls the table into memory in older versions, or throws in newer ones. Check for method calls on entities inside predicates.
- `IQueryable` leaked out of the repository and enumerated after the context is disposed.
- **DbContext lifetime**: it is scoped and not thread-safe. Captured by a singleton (captive dependency), used across parallel tasks, or injected into a background service without creating a scope — all bugs.
- Missing concurrency token (`[Timestamp]`/`IsConcurrencyToken`) where two requests can update the same row.
- `ExecuteSqlRaw` with interpolated input — use `FromSqlInterpolated` or parameters.
- Migrations reviewed by hand; `EnsureCreated` in anything but a test.
- Tracked entity mutated then not saved, or saved twice.

**Evidence and correction:** Locate the context instance and query execution points. Concurrent tasks using one DbContext are unsafe even if their queries look independent. Fix with sequential awaits or separate scoped contexts. Measure tracking/query overhead before making AsNoTracking or batching requirements.

## Dependency injection
- Lifetime mismatch: a singleton depending on a scoped service. This is the most common .NET production bug after async misuse.
- `IServiceProvider` injected and resolved manually (service locator) instead of constructor injection.
- Frequent client/handler creation can exhaust sockets; a long-lived client with configured pooled-connection lifetime is also valid. Inspect actual handler reuse and DNS-refresh requirements before requiring IHttpClientFactory.
- Inspect who creates and disposes IDisposable instances. Container-resolved transients are tracked for disposal; resolving many from a root scope can retain them too long. Manually constructed instances need an explicit owner.

**Evidence and correction:** Compare service lifetimes and disposal ownership. Captive scoped services are distinct from a validated singleton holding a reusable thread-safe client. Avoid disposing container-owned instances manually; use the established lifetime/factory pattern.

## Web pipeline and security
- **Middleware order**: `UseAuthentication` before `UseAuthorization`; `UseCors` before them; `UseRouting`/`UseEndpoints` placement. Reordering changes security behavior silently.
- `[Authorize]` missing on a new controller/action, or `[AllowAnonymous]` added; for minimal APIs, `RequireAuthorization()` on the endpoint or group.
- Role-based and policy-based authorization are both supported. Confirm that server endpoints enforce the intended roles/ownership; a UI-only check does not provide server authorization.
- Overposting: binding directly to an EF entity lets a client set `Id`, `Role`, or `OwnerId`. Use a request DTO.
- Model validation result actually checked (`ModelState.IsValid`) when not using automatic validation.
- Exception handler middleware in place; `UseDeveloperExceptionPage` gated to development.
- Antiforgery on cookie-authenticated form posts.
- Data-protection keys persisted, otherwise cookies and tokens invalidate on restart or across instances.
- Secrets from configuration providers, never literals; user-secrets/Key Vault rather than `appsettings.json`.

**Evidence and correction:** Inspect effective endpoint/global policies and middleware registration, including minimal API groups. Authorization can be provided by a fallback policy; missing one attribute is not proof of public exposure. Test an anonymous and wrong-owner call.

## Language and runtime
- Nullable reference types enabled and not silenced with `!`.
- `IEnumerable` enumerated multiple times, re-running the query each time; materialize with `ToList()` once.
- LINQ deferred execution captured over a mutating variable.
- `struct` vs `class` copies; `DateTime` vs `DateTimeOffset` and `DateTime.Now` vs `UtcNow`.
- `string` concatenation in a loop; culture-sensitive comparison where ordinal is meant (`StringComparison.OrdinalIgnoreCase`).
- `lock` on a public or boxed object; `async` inside a `lock` (not allowed — needs `SemaphoreSlim`).
- Logging via `ILogger` with structured placeholders, not interpolation.

**Evidence and correction:** Check actual enumeration count, culture/time semantics, lock ownership, and structured logger behavior. Show a changed result or measured cost. Nullable warnings and logging style follow the project’s enforced configuration.

## Worked example and counterexample

```csharp
// Defect: same context used concurrently.
await Task.WhenAll(db.Users.ToListAsync(ct), db.Orders.ToListAsync(ct));
// Correction when parallelism is unnecessary.
var users = await db.Users.ToListAsync(ct);
var orders = await db.Orders.ToListAsync(ct);
```

Use separate context scopes if parallel database operations are required. Merely moving both calls to Task.Run does not make a DbContext thread-safe.

## Sources and maintenance

[EF context ownership](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
