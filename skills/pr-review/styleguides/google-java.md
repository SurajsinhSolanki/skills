# Google Java Style Guide — Review Checklist

Source: [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [Imports](#imports) · [Naming](#naming) · [Javadoc](#javadoc) · [Programming practices to flag](#programming-practices-to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google Java policy; inspect supported language level and formatter. Records, generated bindings, and overriding APIs can impose names or documentation exceptions.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- Column limit 100 (package/import lines, URLs, and shell commands excepted).
- Block indentation +2 spaces; continuation lines at least +4.
- One statement per line. Braces on every `if`/`else`/`for`/`do`/`while`, even single-line bodies; K&R style.
- Tooling: `google-java-format` implements the formatting rules — if it runs in CI, skip formatting findings.

**Application and exceptions:** Formatter-owned whitespace needs no manual line-by-line findings. Preserve literals and URLs that legitimately exceed the column target.

## Imports
- No wildcard imports, static or otherwise.
- Static imports in one block, non-static in another, ASCII-sorted within each. No line-wrapping of imports.

**Application and exceptions:** Import group ordering is separate from runtime class loading; do not replace an import merely for personal preference.

## Naming
| Kind | Style |
|---|---|
| packages | all lowercase, no underscores |
| classes | `UpperCamelCase`; test classes end in `Test` |
| methods, fields, parameters, locals | `lowerCamelCase` |
| constants (static final, deeply immutable) | `UPPER_SNAKE_CASE` |
| type variables | single capital (`T`, `E2`) or name + `T` (`RequestT`) |

Acronyms are camel-cased as words: `XmlHttpRequest`, not `XMLHTTPRequest`. A local that is `final` is still `lowerCamelCase`.

**Application and exceptions:** An immutable static final constant differs from a mutable collection held in a final variable.

## Javadoc
- Required on every public and protected class and member, except self-explanatory members (simple getters) and overrides.
- Starts with a summary fragment. Block tags in order: `@param`, `@return`, `@throws`, `@deprecated`.

**Application and exceptions:** A useful Javadoc summary states caller-visible behavior, including null/error contracts; obvious overrides may inherit documentation.

## Programming practices to flag
- Missing `@Override` on an overriding method. **(bug risk)**
- A caught exception ignored with no comment explaining why. **(bug risk)**
- Static members referenced through an instance instead of the class name.
- Overriding `Object.finalize()`. **(bug risk)**

**Application and exceptions:** A missing @Override is a style/compiler-safety issue unless an actual unintended overload or broken contract is established.

## Example and review decision

```java
/** Returns the stable identifier used by callers. */
public String customerId() {
  return customerId;
}
```

If overriding an external method, preserve its name and add @Override; do not rename it to satisfy a naming preference.
