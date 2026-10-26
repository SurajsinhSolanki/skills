# Java / Kotlin Review (Spring Boot · JPA / Hibernate)

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Transactions — proxy semantics are the classic trap](#transactions--proxy-semantics-are-the-classic-trap) · [JPA / Hibernate](#jpa--hibernate) · [Spring web and security](#spring-web-and-security) · [Concurrency and state](#concurrency-and-state) · [General](#general) · [Kotlin specifics](#kotlin-specifics) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Java/Kotlin services using Spring transactions/security and JPA/Hibernate. Inspect Spring version, proxy versus AspectJ mode, transaction manager, ORM provider, Kotlin plugins, and database adapter. An annotation alone does not establish active advice.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Transactions — proxy semantics are the classic trap
- In Spring proxy mode, self-invocation bypasses transactional advice. Method eligibility depends on interface/class proxying and visibility; AspectJ weaving behaves differently. Inspect the actual bean call path and proxy mode before claiming the transaction is absent.
- Default rollback normally covers RuntimeException/Error; explicit rollback rules or newer global rollback configuration can change this. Inspect local annotations and transaction configuration before treating a checked exception as committed.
- `readOnly = true` on a method that writes.
- Propagation: `REQUIRES_NEW` inside an outer transaction creates a second connection and can deadlock against it.
- External calls (HTTP, queue publish, email) inside a transaction cannot be rolled back and hold the connection open. Move them to `TransactionSynchronization` / after-commit.
- Transaction spanning a long loop, holding locks for its duration.

**Evidence and correction:** Find the actual bean invocation path and transaction boundaries. Test an exception after a write and observe whether it commits. Fix the proxy crossing, rollback rule, or transaction scope rather than moving methods only for appearance; external effects need commit-safe delivery when rollback matters.

## JPA / Hibernate
- **N+1**: lazy collections touched in a loop, a mapper, or a serializer. Look for `@OneToMany` accessed after the service returns.
- `LazyInitializationException` — an entity returned past the transaction boundary and touched in the controller or view.
- `FetchType.EAGER` on a collection: every query drags the graph along.
- Entities serialized directly to JSON — leaks the schema, drags lazy proxies, and couples the API to the DB. Use DTOs.
- `equals`/`hashCode` on an entity using a generated id: before persist the id is null, so the object changes identity inside a `HashSet`.
- `CascadeType.REMOVE` / `orphanRemoval = true` — verify the delete is intended and cannot take unrelated history with it.
- `save()` in a loop instead of a batch; `saveAll` without batch size configured is still row-by-row.
- Missing `@Version` where two requests can update the same row (lost update).
- Derived query methods that generate surprising SQL; check the actual query for anything non-trivial.
- Inspect production schema-management settings and rollout policy. Automatic destructive schema updates may be unsafe, but a setting alone is not a blocker without an applicable MUST rule or a concrete introduced risk.

**Evidence and correction:** Read generated SQL and serialization paths. Demonstrate N+1 at realistic row count, mutation races, or unintended cascade deletes. Eager fetching, DTOs, version columns, and batch settings are choices whose necessity depends on a caller/data invariant.

## Spring web and security
- Missing `@Valid` on a `@RequestBody`, so bean-validation annotations never run.
- Request DTOs that include fields the client must not set (`id`, `role`, `ownerId`) — overposting.
- Trace authorization across exposed entry points. Controller, service, and method policies can be valid; require an extra service check when another caller bypasses the existing boundary or the project mandates it.
- `SecurityFilterChain` rule order: a broad `permitAll` before a specific `authenticated` matcher opens everything after it.
- CSRF disabled without a stated reason for a cookie-authenticated app.
- Actuator endpoints exposed (`/actuator/env`, `/heapdump`) — CRITICAL if reachable unauthenticated.
- `@ControllerAdvice` mapping exceptions so stack traces and SQL never reach the client.
- CORS configured with `allowedOrigins("*")` plus credentials.

**Evidence and correction:** Trace filter-chain matcher order, fallback policies, validation activation, and field binding. Reproduce wrong-owner/anonymous access or an exposed sensitive actuator endpoint; authentication alone does not establish object authorization.

## Concurrency and state
- **Singleton beans holding request state in fields.** Spring beans are singletons by default; an instance field mutated per request is a cross-request data leak.
- Non-thread-safe members shared across requests: `SimpleDateFormat`, `Calendar`, non-concurrent collections, `StringBuilder` fields.
- `@Async` on a self-invoked method (same proxy problem) and `@Async` without a configured executor — the default may be unbounded or single-threaded.
- `CompletableFuture` chains without an explicit executor, silently on the common pool.
- Mutable static state.

**Evidence and correction:** Locate mutable singleton fields and executor ownership. Test overlapping requests/cancellations, and separate immutable shared config from request-scoped state. An @Async annotation still needs a proxied call and appropriate executor/error handling.

## General
- Resources closed with try-with-resources: streams, JDBC, HTTP clients.
- `Optional` used as a field or parameter type rather than a return value; `.get()` without a presence check.
- `@Value` scattered where `@ConfigurationProperties` gives one validated object.
- Exceptions swallowed (`catch (Exception e) {}`) or logged and rethrown twice.
- Logging: parameterized (`log.info("x {}", v)`), never string concatenation; no secrets or full request bodies.
- `RestTemplate`/`WebClient` without connect and read timeouts — a hung dependency exhausts the thread pool.

**Evidence and correction:** Check resource closure, Optional presence, time/culture choices, and configuration conversion on actual boundary values. Prefer existing config patterns; API style by itself is non-blocking unless adopted as a MUST.

## Kotlin specifics
- Platform types from Java APIs are implicitly nullable; `!!` reintroduces NPEs.
- `data class` as a JPA entity: `equals`/`hashCode`/`copy` conflict with proxying and identity; entities need a no-arg constructor and open members.
- `lateinit` fields accessed before initialization.
- Coroutines: blocking calls (`Thread.sleep`, JDBC) inside a coroutine without `Dispatchers.IO`; `GlobalScope` leaking work past the request; structured concurrency and cancellation respected.

**Evidence and correction:** Identify Hibernate bytecode/proxy requirements and Kotlin compiler plugins before flagging final classes. Check initialized lifecycle and structured coroutine ownership; blocking I/O needs an appropriate dispatcher or framework integration.

## Worked example and counterexample

```java
// Proxy mode: this call does not cross a transactional proxy.
public void run() { this.write(); }
@Transactional public void write() { /* database work */ }
// Place the transaction on the externally invoked run method,
// or invoke a transactional method on a separately proxied bean.
```

The correction depends on the intended atomic unit. AspectJ weaving or an existing outer transaction can invalidate the assumed missing-transaction finding.

## Sources and maintenance

[Transactional configuration](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
