# Google JavaScript Style Guide — Review Checklist

Source: [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [Declarations and modules](#declarations-and-modules) · [Naming](#naming) · [Documentation](#documentation) · [To flag](#to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google’s JavaScript guide is a legacy policy snapshot and is no longer updated upstream. Apply it to JavaScript only when opted in; do not require migrating the project to TypeScript.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- Column limit 80 (import/export lines and URLs excepted). 2-space indentation.
- Semicolons on every statement — never rely on automatic insertion. **(bug risk)**
- Braces on all control structures, K&R style. Single quotes for strings; template literals for interpolation and multi-line text.
- Trailing commas in multi-line array and object literals.

**Application and exceptions:** Semicolons and braces are style requirements here; a real automatic-semicolon-insertion failure needs an affected expression or return path.

## Declarations and modules
- `const` by default, `let` when reassigned, never `var`. One variable per declaration.
- ES modules or `goog.module`; **no default exports** — named exports only.

**Application and exceptions:** Keep module systems compatible with the project loader. Named exports are the policy; imports of third-party default exports remain possible.

## Naming
| Kind | Style |
|---|---|
| classes, interfaces, enums, typedefs | `UpperCamelCase` |
| methods, functions, fields, parameters, locals | `lowerCamelCase` |
| constants (deeply immutable), enum values | `CONSTANT_CASE` |

No single-letter parameter names on public methods.

**Application and exceptions:** Distinguish deeply immutable constants from mutable objects whose binding happens to be const.

## Documentation
- JSDoc on classes, fields, and methods; types in braces on `@param`/`@return`. `@override` on overriding methods.

**Application and exceptions:** JSDoc records the public contract; do not demand annotations already supplied by a generated interface or adopted tooling.

## To flag
- `==` / `!=` — use `===` / `!==` (`== null` to catch both null and undefined is the one allowed exception). **(bug risk)**
- `with`, `eval`, `new Function(string)`. **(bug risk)**
- Modifying built-in prototypes; `new String()`/`new Number()`/`new Boolean()` wrappers. **(bug risk)**
- Throwing anything other than an `Error` object. **(bug risk)**
- `for…in` over arrays, or over objects without an own-property check — use `for…of` / `Object.keys`. **(bug risk)**
- `switch` without a `default`, or fall-through without a comment. **(bug risk)**
- Fields not declared in the constructor; direct prototype manipulation; static-only container classes (export functions instead).
- Mixing quoted and unquoted keys in one object literal.

**Application and exceptions:** Loose-null equality is an explicit exception. Dynamic code loaders and compatibility polyfills need their documented exceptions; arbitrary eval of attacker text is a separate concrete risk.

## Example and review decision

```js
// Defect: a newline after return inserts a statement boundary.
function bad() { return
  {ok: true}; }
// Correction:
function good() { return {ok: true}; }
```

A semicolon preference without a semantic difference stays a style observation.
