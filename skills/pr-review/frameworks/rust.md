# Rust Review

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Panics — the main production risk](#panics--the-main-production-risk) · [Async](#async) · [Errors](#errors) · [Correctness and ownership](#correctness-and-ownership) · [`unsafe`](#unsafe) · [Serde and boundaries](#serde-and-boundaries) · [Tests](#tests) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Rust with Cargo edition, release profile, panic/overflow settings, target, async runtime, and Serde formats identified locally. Task cancellation and JoinHandle semantics are runtime-specific; examples of detached spawning assume Tokio-like behavior, not every executor.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Panics — the main production risk
- `unwrap()` / `expect()` in a request path, library, or long-running service. Compiles fine, kills the task or process at runtime. In a handler, check whether the framework catches it.
- Slice/HashMap indexing and split_at can panic on missing keys or invalid bounds. Check the preceding invariant; get/checked variants allow expected invalid input to become an explicit outcome.
- Integer overflow depends on compiler/profile overflow-check settings, not only debug versus release. Signed MIN/-1 division and zero divisors have separate checks. For input-dependent arithmetic, choose checked, saturating, or wrapping semantics matching the contract and verify the deployed profile.
- Division by zero, `as` casts that truncate (`u64 as u32`), and float-to-int casts that saturate.
- `unreachable!` / `todo!` / `unimplemented!` reachable from real input.
- `RefCell::borrow_mut` while already borrowed — runtime panic, not a compile error.
- `Mutex` poisoning: `.lock().unwrap()` propagates a panic from another thread.

**Evidence and correction:** Trace whether input can reach a panicking operation and what the host does with that panic. An invariant proven by prior checks or a test-only unwrap is different from an unchecked user index. Prefer checked access/arithmetic when failure is part of normal input.

## Async
- **A `std::sync::Mutex` guard held across an `.await` point** — holds a non-Send guard, deadlocks or fails to compile depending on shape. Use an async mutex, or drop the guard before awaiting.
- Blocking calls inside async: `std::fs`, `std::net`, `thread::sleep`, heavy CPU work, blocking DB drivers. Starves the executor. Use the async equivalent or `spawn_blocking`.
- Cancellation safety: any future can be dropped at an await point. State mutated before an await and committed after can be left half-applied — matters for `select!` branches and timeouts.
- Spawned tasks whose `JoinHandle` is dropped: the task runs detached and its panic is silently lost.
- Unbounded channels and unbounded task spawning from user input.
- Missing timeouts on outbound requests.

**Evidence and correction:** Locate every held guard and mutation at await points. Test cancellation between updates or a full bounded channel. Move blocking work to an owned compatible executor, and make partial operations recoverable; an async mutex is not automatically the best fix for every short critical section.

## Errors
- `unwrap_or_default()` hiding a real failure and substituting an empty value.
- Error APIs should preserve the information callers need. Typed public errors or contextual dynamic errors can both be appropriate; inspect downcasts/source chains and project conventions rather than mandating crates.
- `?` converting into an error type that discards context (no `#[from]` source, no `.context(...)`).
- `let _ = fallible();` discarding a `Result` — `#[must_use]` warns, but it can be silenced.
- Errors returned to a client carrying internal paths or SQL.

**Evidence and correction:** Follow Result conversion and client serialization. Preserve caller-relevant error identity/context and avoid returning internal details. An explicit ignored best-effort result can be valid; show the required action lost by the ignore.

## Correctness and ownership
- `clone()` in a hot path where a borrow would do — only report with a stated scale.
- `Arc<Mutex<T>>` where the lock is held across expensive work.
- Lock ordering inconsistent between call sites — deadlock.
- `mem::forget` / `ManuallyDrop` leaking a resource; `Drop` implementations that can panic.
- Shadowed variables changing meaning mid-function.
- Iterator chains that allocate per element (`collect` into a temporary just to iterate again).
- `String`/`Vec` capacity reallocated in a loop with a known size.

**Evidence and correction:** Inspect actual clone/allocate scale and lock acquisition order. A measured hot path or two concrete opposing lock orders supports a finding; a clone token or iterator style alone does not. Include destructors and error cleanup in lock reasoning.

## `unsafe`
- Verify the safety invariant for every unsafe operation: bounds, validity, aliasing, ownership, lifetime, and thread safety as applicable. Missing justification blocks verification when the invariant cannot be established; a missing comment alone has the severity of the project’s documentation rule, not presumed memory unsafety.
- Raw pointer arithmetic, `from_raw_parts`, `transmute`, and `get_unchecked` — verify bounds and lifetime reasoning.
- `unsafe impl Send/Sync` — justify why the type is actually thread-safe.

**Evidence and correction:** Write the safety invariant in terms of values, lifetimes, aliasing and ownership. Check every constructor/caller that must establish it. Fix the unsafe precondition or narrow the unsafe region; a comment cannot make an invalid pointer sound.

## Serde and boundaries
- `#[serde(deny_unknown_fields)]` considered for inbound payloads; silently ignoring unknown fields can mask a contract mismatch.
- `#[serde(default)]` filling a missing required field with a zero value.
- Numeric types that do not survive JSON (`u64` beyond 2^53) when the client is JavaScript.
- Untagged enums matching the wrong variant.

**Evidence and correction:** Test omitted/extra fields, numeric limits, and ambiguous variants against actual consumers. Unknown-field rejection is not universally desirable for forward-compatible protocols. JSON integer interoperability depends on the consumer representation.

## Tests
- `#[should_panic]` used as error handling rather than testing a genuine panic contract.
- `unwrap()` in tests is fine; in `src/` on a production path it is not — do not flag test code for it.

**Evidence and correction:** Review assertions against the intended contract. should_panic can validate a documented invariant failure; tests need not avoid unwrap merely because production paths must handle errors.

## Worked example and counterexample

```rust
// Defect if an arbitrary client index is accepted.
let item = items[index];
// Correction when absence is an expected input error.
let item = items.get(index).ok_or("index out of bounds")?;
```

This fragment assumes the enclosing function returns a compatible Result and uses a borrowed item. Choose a project error type; changing to unsafe get_unchecked is not an error-handling fix.

## Sources and maintenance

[Operator and overflow semantics](https://doc.rust-lang.org/reference/expressions/operator-expr.html). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
