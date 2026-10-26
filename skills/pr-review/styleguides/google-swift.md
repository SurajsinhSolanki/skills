# Google Swift Style Guide — Review Checklist

Source: [Google Swift Style Guide](https://google.github.io/swift/) (Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [Naming](#naming) · [To flag](#to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google Swift style snapshot; inspect Swift language mode, concurrency checking, minimum OS, formatter, and imported Objective-C API naming.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- Column limit 100. 2-space indentation. No semicolons; one statement per line.
- K&R braces. Trailing commas in multi-line array and dictionary literals.
- Imports: whole modules preferred; grouped (modules, individual declarations, `@testable`), sorted, one blank line between groups.
- Tooling: `swift-format` — skip what CI enforces.

**Application and exceptions:** Use configured formatting and import groups; @testable imports belong to tests, not production access-control bypass.

## Naming
- Types `UpperCamelCase`; functions, variables, and global constants `lowerCamelCase` — no `k` prefix, no `SCREAMING_SNAKE`.
- Acronyms keep uniform case (`URLSession`, `htmlBody`).
- Static properties not suffixed with the type name (`UIColor.red`, not `redColor`).
- Delegate methods take the source object first.

**Application and exceptions:** Follow Swift API readability at the call site. Imported Objective-C/acronym spellings can be intentional exceptions.

## To flag
- Force unwrap (`!`) outside tests without a comment explaining why it cannot fail. **(bug risk)**
- `try!` outside tests and unmistakable programmer-error cases. **(bug risk)**
- Force casts (`as!`) without a comment on the invariant. **(bug risk)**
- Implicitly unwrapped optionals outside UI outlets, lifecycle-initialized properties, and test fixtures. **(bug risk)**
- Sentinel values (`-1`, `""`) instead of optionals; return codes instead of `throws` for multiple failure states. **(bug risk)**
- Deep `if` nesting where `guard` gives an early exit.
- A `case` containing only `fallthrough` — combine the patterns.
- Masking arithmetic (`&+`) outside modular arithmetic or documented hot paths. **(bug risk)**
- Access modifiers on an `extension` itself, or explicit modifiers equal to the default.
- Multiple variables per `let`/`var`; `Array<T>`/`Optional<T>` instead of `[T]`/`T?`.
- Horizontal alignment of code except for tabular data; playground literals in production code.
- Missing `///` doc comments on `public`/`open` declarations; `/** */` block doc comments.
- Several unrelated top-level types in one file.

**Application and exceptions:** Force operations need an invariant: a documented test fixture differs from untrusted input. Optional/error modeling is a policy choice until a reachable trap, lost failure, or violated contract is shown.

## Example and review decision

```swift
// Defect if input is not known to contain an integer.
let count = Int(text)!
// Correction for expected invalid input:
guard let count = Int(text) else { throw ParseError.invalidCount }
```

This fragment assumes a throwing function and existing ParseError. Keep public /// documentation aligned with the failure contract.
