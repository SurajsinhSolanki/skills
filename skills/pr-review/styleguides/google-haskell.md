# Google Haskell Style Guide — Review Checklist

Source: [Google Haskell Style Guide](https://google.github.io/styleguide/haskellguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [To flag](#to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google Haskell style revision 1.01 snapshot; inspect GHC/base versions, extensions, generated declarations, build warnings, and formatter policy.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- 80 columns, 4-space indentation, no tabs, no trailing spaces. Layout rather than braces and semicolons.

**Application and exceptions:** Layout changes can change parsing, so preserve semantic grouping and use the configured formatter where available.

## To flag
- Identifiers with underscores (allowed only for unused bindings, `prop_`/`test_` names, and reserved-word escapes); plural module names; acronyms not camel-cased (`HttpResponse`).
- Modules normally use explicit export lists; generated Template Haskell exports can justify omitting the list. Verify an accidental public API before raising compatibility severity.
- Unqualified wholesale imports — use qualified imports or explicit import lists; imports not grouped (external, internal) and alphabetized.
- Language extensions enabled globally in the `.cabal` file, or controversial extensions without justification.
- Partial functions — `head`, `tail`, `fromJust`, `read`, `(!!)`, `minimum` — unless coverage is guaranteed right there. **(bug risk)**
- `error` used for anything but invariant violations. **(bug risk)**
- Top-level functions without type signatures.
- Exported items without Haddock comments.
- Code that does not compile under `-Wall -Werror`. **(bug risk)**
- Heavy point-free style; nested `if…then…else` where guards would do; `INLINE` pragmas without measurement.

**Application and exceptions:** Check explicit types, exports, qualified/import lists, and Haddock contracts together. Partial functions need a proven nonempty/valid input or total replacement. Template Haskell may justify generated exports or enabled extensions.

## Example and review decision

```haskell
-- Partial: crashes on [].
firstBad xs = head xs
-- Total contract for an optional first value.
firstGood :: [a] -> Maybe a
firstGood [] = Nothing
firstGood (x:_) = Just x
```

A caller-established nonempty invariant can make a partial operation intentional. Do not invent -Werror as a required gate if the project has not adopted it.
