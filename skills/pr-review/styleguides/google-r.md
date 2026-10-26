# Google R Style Guide — Review Checklist

Source: [Google R Style Guide](https://google.github.io/styleguide/Rguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Google's R guide is the tidyverse style guide plus the changes below. Formatting is enforced with `styler` — skip what it enforces.

Contents: [Scope and offline use](#scope-and-offline-use) · [To flag](#to-flag) · [Additional local conventions](#additional-local-conventions) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google R style extensions plus a local summary of the referenced tidyverse basics. Inspect R version, package namespace, and project styler/lintr configuration.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## To flag
- Function names not `BigCamelCase`; private functions not starting with a dot (`.Helper()`).
- `attach()`. **(bug risk)**
- Right-hand assignment (`… -> x`) — use `x <- …`.
- Relying on implicit return — use explicit `return()`.
- External functions called without `package::` qualification (infix operators, rlang pronouns, and base packages such as stats, utils, and methods are exempt). **(bug risk: masking)**
- Roxygen `@import` of whole packages — use `@importFrom`.
- A package without a `packagename-package.R` documentation file.

**Application and exceptions:** Use BigCamelCase functions and .PrivateHelper for Google policy; other data names can use descriptive snake_case. Document exported functions with roxygen, explicit parameters/results, and narrow @importFrom directives.

## Additional local conventions

Locally available base rules: use two-space indentation, spaces around assignment/operators, spaces after commas, <- for assignment, and braces for multiline control flow. Prefer readable names and short lines (about 80 columns, with literals/URLs exempt). Group library imports deliberately; package code should declare dependencies and qualify or narrowly import non-base functions. Do not let attach() silently change lookup of columns/functions.

Optional baseline attribution: [Tidyverse syntax](https://style.tidyverse.org/syntax.html). The relevant baseline is included above.

## Example and review decision

```r
# Explicit qualification prevents an attached package changing the selected function.
KeepRows <- function(data) {
  return(dplyr::filter(data, enabled))
}
```

A project without dplyr should use its existing tools; this example is not a dependency recommendation.
