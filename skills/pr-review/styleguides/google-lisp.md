# Google Common Lisp Style Guide — Review Checklist

Source: [Google Common Lisp Style Guide](https://google.github.io/styleguide/lispguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [To flag](#to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google Common Lisp style snapshot; inspect implementation, reader/package configuration, macro expansion environment, and generated code. This is Common Lisp, not Scheme or Clojure.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- 100-column lines, spaces only. Bodies indented 2 spaces. No space inside parentheses. One blank line between top-level forms.

**Application and exceptions:** Use indentation that reflects Lisp forms, not a mechanical two-space rule for every argument. Preserve string contents and reader syntax.

## To flag
- Names not lowercase-hyphenated; predicates without a `p` / `-p` suffix; globals without `*earmuffs*`; constants without `+plus-signs+`; package-name prefixes inside symbol names.
- Top-level functions, types, classes, variables, or macros without docstrings.
- Comment semicolons inconsistent with the convention (`;;;` top-level, `;;` within a form, `;` end of line).
- `::` access to another package's internal symbols outside tests; package nicknames.
- `error` without a specific condition type; calling `signal` directly; handling all conditions (type `t`). **(bug risk)**
- Assertions (`assert`, `check-type`) used to validate user input instead of internal invariants. **(bug risk)**
- Macros where a function would do; unhygienic macros (no `gensym`, arguments evaluated more than once). **(bug risk)**
- `eval`, `intern`, or `unintern` at runtime. **(bug risk)**
- `loop` where `dolist` or `dotimes` would do; mutating the iteration variable inside the body. **(bug risk)**

**Application and exceptions:** Inspect package exports, docstrings, conditions, and macro expansion. A macro intentionally introducing a binding differs from accidental capture; evaluate-once behavior matters when arguments have side effects.

## Example and review decision

```lisp
;; Counterexample: argument evaluated twice if TEST has side effects.
(defmacro twice (test) `(list ,test ,test))
;; Evaluate once when that is the intended macro contract.
(defmacro twice-once (test)
  (let ((value (gensym "VALUE")))
    `(let ((,value ,test)) (list ,value ,value))))
```

Document public forms, import only needed external symbols, and keep package internals private except documented tests/REPL use.
