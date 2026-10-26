# Google TypeScript Style Guide — Review Checklist

Source: [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Load together with `google-javascript.md` only if the diff also has plain `.js`; for `.ts` this file is enough.

Contents: [Scope and offline use](#scope-and-offline-use) · [Naming](#naming) · [Modules](#modules) · [Types — to flag](#types--to-flag) · [Classes](#classes) · [Other rules to flag](#other-rules-to-flag) · [Additional local conventions](#additional-local-conventions) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google TypeScript policy snapshot; inspect compiler/module settings and required framework exports. Negative type tests have a narrow @ts-expect-error exception.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Naming
| Kind | Style |
|---|---|
| classes, interfaces, types, enums, decorators, type parameters | `UpperCamelCase` |
| variables, parameters, functions, methods, properties | `lowerCamelCase` |
| global constants, enum values | `CONSTANT_CASE` |

Acronyms as words (`loadHttpUrl`). No leading or trailing underscores.

**Application and exceptions:** Preserve external API spelling and framework contracts; naming changes are policy issues, not inherently runtime defects.

## Modules
- No default exports. No `namespace` (except for external interop). No mutable exports — export a getter instead.
- `import type` for type-only imports. No static-only container classes.

**Application and exceptions:** Named exports aid consistent imports; a framework-mandated default export or external declaration can override this policy through the project rules.

## Types — to flag
- `any` — use `unknown` or a specific type; a suppression needs a comment. **(bug risk)**
- Type assertions without a comment explaining why they are safe; angle-bracket assertions (use `as`). **(bug risk)**
- Non-null assertions (`!`) without justification. **(bug risk)**
- `@ts-ignore`, `@ts-expect-error`, `@ts-nocheck` — disallowed outside tests. **(bug risk)**
- `const enum` (plain `enum` is fine); coercing enum values with `!!`/`Boolean()` — compare explicitly.
- Wrapper types `String`/`Number`/`Boolean`; the `{}` type — use `unknown`, `object`, or `Record<…>`.
- Optional `?` and a required `T | undefined` property express different presence contracts, especially with exactOptionalPropertyTypes. Use the form matching the contract; prefer interface for object shapes only as the adopted style allows.

**Application and exceptions:** Assertions erase checks rather than validating data. Optional and required-but-undefined fields differ; inspect the producer and exactOptionalPropertyTypes before rewriting one into the other.

## Classes
- Fields not reassigned after construction marked `readonly`; parameter properties to cut boilerplate.
- TypeScript visibility modifiers instead of `#private` fields. Never bypass visibility with `obj['private']`.

**Application and exceptions:** Readonly protects reassignment of the field, not deep immutability. Parameter properties can express simple constructor assignment without changing runtime validation.

## Other rules to flag
- `var`, `Array()`/`Object()` constructors, `debugger`, `with`, `eval`, `new Function(string)`. **(bug risk)**
- `==`/`!=` except `== null`. **(bug risk)**
- Throwing non-`Error` values; catch variables not treated as `unknown`; empty `catch` without a comment. **(bug risk)**
- `for…in` without own-property filtering. **(bug risk)**
- `this` inside function declarations/expressions (outside explicit rebinding) — use arrow functions.
- Control statements without braces; `switch` without `default`.
- JSDoc (`/** */`) for implementation comments — use `//`.

Tooling: `gts` packages Google's TypeScript lint and format setup. Strict compiler settings are expected.

**Application and exceptions:** Control-flow, catch, and iteration rules need the actual value path before bug severity. Existing compiler/lint enforcement handles mechanical violations.

## Additional local conventions

Formatting and documentation: keep the project’s formatter (commonly two-space indentation and semicolon-terminated statements); use JSDoc for public API contracts and ordinary comments for implementation rationale. Do not invent a TypeScript line limit absent adopted config.

## Example and review decision

```ts
// Policy-compliant named export and interface.
export interface Profile { readonly id: string; }
export function profileId(profile: Profile): string { return profile.id; }
```

This policy does not ban a default export required by Next.js or a documented negative type test under the project’s stronger rules.
