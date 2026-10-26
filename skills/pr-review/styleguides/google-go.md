# Google Go Style Guide — Review Checklist

Source: [Google Go Style Guide (Decisions)](https://google.github.io/styleguide/go/decisions) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [Naming](#naming) · [Comments](#comments) · [Imports](#imports) · [Errors — to flag](#errors--to-flag) · [Language — to flag](#language--to-flag) · [Tests](#tests) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google Go policy; inspect module language/toolchain versions and project gofmt/lint setup. Google policy choices such as test helpers are not universal Go requirements.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- `gofmt` output is required — skip formatting findings if CI runs it.
- No fixed line limit for code or comments. Wrap for readable semantic units rather than a numerical quota; avoid arbitrary splits of function signatures.

**Application and exceptions:** Use gofmt for layout; readability rather than a hard comment width controls wrapping.

## Naming
- `MixedCaps` everywhere, constants included — never `MAX_SIZE` or `kMaxSize`.
- Initialisms keep one case: `XMLAPI` / `xmlAPI`, never `XmlApi`.
- Package names lowercase, no underscores; avoid `util`, `common`, `helpers`.
- Receivers one or two letters, consistent across a type's methods.
- No `Get` prefix on getters. Name length proportional to scope; drop type words (`users`, not `userSlice`).
- No stutter between package and symbol (`widget.New`, not `widget.NewWidget`).

**Application and exceptions:** Scope affects name length. Generated bindings, operating-system interfaces, and black-box _test packages have naming exceptions.

## Comments
- Every exported name has a doc comment that starts with the name and is a full sentence.

**Application and exceptions:** Exported comments explain the contract, not just repeat the signature. Mention concurrency/lifetime limitations callers depend on.

## Imports
- Groups: standard library, then everything else (protos and side-effect imports may get their own groups).
- No dot imports. Blank (`_`) imports only in `main` packages and tests.

**Application and exceptions:** Side-effect imports require an understood initialization effect; adopted generated/framework integrations may justify an exception.

## Errors — to flag
- `error` not the last return value; exported functions returning a concrete error type instead of `error`. **(bug risk)**
- Errors discarded with `_` without a comment. **(bug risk)**
- In-band error values (`-1`, `""`) instead of an extra return. **(bug risk)**
- Error strings capitalized or ending in punctuation.
- Normal path in an `else` after an error check — return early and keep the happy path unindented.

**Application and exceptions:** Style of error text is distinct from lost error handling; cite the failing caller before treating an error-API shape as a bug.

## Language — to flag
- `panic` for ordinary errors; outside `main`/init, return an `error`. **(bug risk)**
- Goroutines without a clear exit condition or `context.Context` cancellation. **(bug risk)**
- Interfaces defined on the producer side, or large interfaces — define small interfaces where they are consumed; return concrete types.
- Pointer vs value receivers mixed inconsistently; types containing a `sync.Mutex` with value receivers. **(bug risk)**
- Generics added before there are two real uses.
- Redundant `break` at the end of a `case`.
- Asynchronous APIs where a synchronous one would let the caller choose concurrency.
- Type aliases outside package migrations.

**Application and exceptions:** Small consumer interfaces and synchronous APIs are defaults, not proof that every producer interface, alias, or first-use generic is wrong.

## Tests
- No assertion libraries — use `cmp.Diff` / `cmp.Equal` and plain `if` checks.
- Failure messages name the function and inputs, got before want: `Foo(%v) = %v, want %v`.
- `t.Error` to keep going; `t.Fatal` only when later checks would be meaningless.

**Application and exceptions:** Use the project’s adopted comparison/assertion tools. Worker goroutines should report back to the test goroutine for Fatal/FailNow.

## Example and review decision

```go
// Function and its exported contract use the same name.
// ParseID validates text and returns an identifier or an error.
func ParseID(text string) (ID, error) { return parseID(text) }
```

This is a declaration fragment with existing ID/parseID definitions, not a standalone runnable program.
