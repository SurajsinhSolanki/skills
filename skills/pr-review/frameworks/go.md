# Go Review

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Errors](#errors) · [Goroutines and context](#goroutines-and-context) · [Data races](#data-races) · [Slices, maps, interfaces](#slices-maps-interfaces) · [Resources and stdlib](#resources-and-stdlib) · [Testing](#testing) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Go modules; read the go directive, toolchain, build tags, race settings, and GODEBUG. Loop-variable behavior changes with Go 1.22 language semantics; timer behavior changes with Go 1.23 semantics and compatibility overrides.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Errors
- **Ignored errors.** `_ = doThing()`, or a returned error not checked. Every one is a silent failure path.
- Errors wrapped with `%w` so `errors.Is`/`errors.As` still work downstream; `%v` breaks the chain.
- Sentinel errors compared with `==` where the error may be wrapped — use `errors.Is`.
- Error strings that leak internals to a client, or that get logged and returned (double reporting).
- `panic` in library or request code. A panic in a handler takes down the goroutine and, without recovery, the process.
- Named returns plus `defer` mutating them — subtle and often unintended.

**Evidence and correction:** Trace every error to its caller and user-facing outcome. An intentionally ignored cleanup error can be acceptable; a lost write error is not. Preserve error identity only where callers inspect it, and distinguish handler recovery from process-wide panic behavior.

## Goroutines and context
- **Goroutine leaks**: a goroutine started with no way to stop, blocked forever on a channel send/receive, or spawned per request with no bound.
- `context.Context` not propagated into DB and HTTP calls, so cancellation and deadlines do nothing.
- `context.Background()` used inside a request path instead of the request's context.
- No timeout anywhere on an outbound call.
- `sync.WaitGroup`: `Add` after `Wait`, `Done` not deferred, or the WaitGroup copied instead of passed by pointer.
- `errgroup` without a bounded limit where the fan-out is user-controlled.
- Unbuffered channel writes with no reader — deadlock. Closing a channel from the receiving side, or closing twice — panic.
- Repeated `time.After` calls allocate timers; unreferenced channel timers become collectible under Go 1.23 timer semantics. Inspect the main module’s go version and `GODEBUG=asynctimerchan` overrides before reporting legacy retention. Allocations can still matter when measured.

**Evidence and correction:** Identify who starts, cancels, and joins each goroutine. A blocked send after its receiver exits is a reproducible leak. Propagate request context or a deliberate detached-work lifetime; bound fan-out according to the actual workload.

## Data races
- Shared maps written concurrently — a runtime fatal error, not a recoverable one.
- A mutex copied by value (embedding a `sync.Mutex` in a struct then passing the struct by value).
- Mutex held across a blocking call or an I/O operation.
- Per-iteration variables declared by loops follow Go 1.22 semantics when enabled for the package/module. An existing variable assigned using `=` is still shared. Check the go directive, build constraints, and declaration shape before reporting capture bugs.
- `sync/atomic` mixed with plain reads of the same variable.
- Writes to a struct field from a goroutine with no synchronization, "because it's just a bool".

**Evidence and correction:** Inspect declarations as well as compiler version: := loop declarations can be per-iteration while assignment to an outer variable still shares it. Reproduce race/aliasing with relevant concurrent paths; do not report a safe post-join read as a race.

## Slices, maps, interfaces
- `append` aliasing: appending to a sub-slice can overwrite the parent's backing array. Copy when the parent must not change.
- A small sub-slice retaining a large backing array, preventing collection.
- `nil` map written to — panic. Reading a nil map is fine, which hides the bug in tests.
- **A nil pointer stored in an interface is not `nil`.** `err != nil` is true for a typed nil, a classic source of false error paths.
- Map iteration order assumed stable.
- Struct comparison including unexported or floating-point fields.

**Evidence and correction:** Check slice capacity and ownership, nil-interface construction, and map initialization with small boundary inputs. A retained backing array is a performance concern only with relevant size/lifetime; a nil map write or typed-nil error can be a concrete defect.

## Resources and stdlib
- `defer resp.Body.Close()` present and after the error check; `defer` inside a loop accumulating until function exit.
- `defer` argument evaluation happens immediately — `defer log(time.Since(start))` captures the wrong value.
- `database/sql`: `rows.Close()` deferred, **`rows.Err()` checked after the loop** (skipping it hides truncated results), `QueryContext` over `Query`, and connection-pool limits set.
- `http.Client` with no `Timeout` and `http.Server` with no `ReadHeaderTimeout`/`WriteTimeout` — both are DoS exposure.
- `io.ReadAll` on an untrusted body without `http.MaxBytesReader`.
- JSON: unexported fields silently skipped; `omitempty` drops legitimate zero values (`false`, `0`, `""`), which is a contract bug for booleans and counts.
- `time.Time` compared with `==` rather than `.Equal` (monotonic clock and location).
- Integer division and conversion truncation; `strconv` errors ignored.

**Evidence and correction:** Follow the early error branch before deferring resource closure, then iteration errors and close ownership. Defaults for HTTP timeout or omitempty matter only when an actual unbounded wait or lost zero-value contract exists.

## Testing
- `t.Parallel()` with shared state or a captured loop variable across subtests.
- Table tests that skip the failing-case rows.
- `t.Fatal`/`FailNow` must run in the test goroutine; a worker calling it exits only that worker. Signal a result/error back to the test goroutine, which can fail and stop the test deliberately.

**Evidence and correction:** Keep fatal test control in the test goroutine and return worker results through channels or joins. Existing table tests may cover the changed behavior without new files.

## Worked example and counterexample

```go
// Typed nil pointer inside an error interface is not a nil interface.
func bad() error { var e *os.PathError; return e }
func good() error { return nil }
```

For callbacks in `for _, item := range items`, inspect module language semantics. If instead the loop assigns an outer `item` using `=`, capture a local copy when each callback must retain its own value.

## Sources and maintenance

[Loop variables](https://go.dev/blog/loopvar-preview); [Timer changes](https://go.dev/wiki/Go123Timer). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
