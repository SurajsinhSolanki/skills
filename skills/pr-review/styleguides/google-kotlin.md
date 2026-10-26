# Google Kotlin Style Guide — Review Checklist

Source: [Android Kotlin Style Guide](https://developer.android.com/kotlin/style-guide) (linked from Google's style guide index). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [Imports](#imports) · [Naming](#naming) · [KDoc](#kdoc) · [To flag](#to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Android Kotlin style snapshot; inspect Kotlin/Compose versions, compiler target, formatter, and framework override contracts.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- Column limit 100 (package/import lines, URLs, and shell commands excepted).
- 4-space indentation; continuation lines +4. No semicolons; one statement per line.
- K&R braces. A one-line `if`/`else` used as an expression may omit braces.
- Tooling: `ktfmt --google-style` or `ktlint` — if one runs in CI, skip formatting findings.

**Application and exceptions:** The column target permits package/import/URL exceptions. Existing ktfmt/ktlint configuration decides mechanically enforced whitespace.

## Imports
- No wildcard imports. One ASCII-sorted list, never line-wrapped.

**Application and exceptions:** Keep one sorted import list. Aliases are legitimate when they disambiguate otherwise colliding names.

## Naming
| Kind | Style |
|---|---|
| packages | lowercase, no underscores |
| classes, types | `PascalCase`; tests end in `Test` |
| functions | `camelCase` (underscores allowed only in test names); `@Composable` functions returning `Unit` are `PascalCase` |
| `const val` and deeply immutable top-level/object vals | `UPPER_SNAKE_CASE` |
| other properties, parameters, locals | `camelCase` |
| backing properties | `_camelCase` |
| type variables | `T`, `T2`, or name + `T` |

Acronyms camel-cased as words: `XmlHttpRequest`, `newCustomerId`.

**Application and exceptions:** Compose naming applies to Unit-returning composables, not every function carrying a composable type.

## KDoc
- Required on every public type and every public or protected member, except obvious ones and overrides.
- Summary fragment first; tag order `@constructor`, `@receiver`, `@param`, `@property`, `@return`, `@throws`, `@see`.

**Application and exceptions:** KDoc should describe caller-visible behavior; avoid empty tags and preserve inherited documentation for straightforward overrides.

## To flag
- Public library API relying on an inferred return or property type — make it explicit.
- Several unrelated top-level declarations in one file; file name not matching its single top-level class.
- Single-expression functions may use an expression body, including readable wrapped expressions. Use braces for multiline if/else branches as required; do not confuse a wrapped function expression with an unbraced conditional.

**Application and exceptions:** An expression body spanning lines is not inherently wrong; judge readability and the current project formatter rather than banning it categorically.

## Example and review decision

```kotlin
/** Returns the selected account, or null when no selection exists. */
fun selectedAccount(): Account? = selection.current
```

Explicit public return types stabilize the contract; do not infer that every multiline expression body causes a defect.
