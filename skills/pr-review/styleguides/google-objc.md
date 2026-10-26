# Google Objective-C Style Guide — Review Checklist

Source: [Google Objective-C Style Guide](https://google.github.io/styleguide/objcguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [Naming](#naming) · [To flag](#to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google Objective-C/Objective-C++ style; inspect ARC versus manual ownership, SDK availability, nullability, and any C++ language mode.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- Column limit 100 (Objective-C++ files may follow the 80-column C++ limit). 2-space indentation, continuations +4.

**Application and exceptions:** Objective-C++ may adopt the project’s C++ width. Do not rewrite generated API declarations for whitespace.

## Naming
- Classes `CapitalCase`; shared code uses a 3+ letter prefix. Category methods use a lowercase prefix and underscore (`gtm_doThing`).
- Methods `lowerCamelCase`, reading as a sentence. Instance variables `_name`. File-scope constants `kName`. Non-static functions prefixed.
- File names match the class; `.h`, `.m`, `.mm`.

**Application and exceptions:** Preserve SDK selectors and superclass overrides. Prefixes protect shared public symbols; scoped local names need not repeat the class.

## To flag
- `@throw` — return errors instead; catch only around third-party code that throws. **(bug risk)**
- Delegates, targets, and data sources not `weak`; blocks retaining `self` in a cycle. **(bug risk)**
- Retained NSString/immutable collection contracts should copy potentially mutable inputs. Synthesized copy setters can help; a mutable collection property may instead need mutableCopy in a custom accessor. Blindly copying NSMutableArray with copy produces an immutable instance. **(bug risk)**
- Comparing `BOOL` to `YES`, or converting integers to `BOOL` by cast. **(bug risk)**
- Messaging `self` in `init`/`dealloc`; missing designated-initializer overrides in subclasses. **(bug risk)**
- Missing nullability annotations on new public API.
- Dot syntax for non-property methods.
- `+new`, used or overridden.
- Static variables declared in headers.
- `#include` for Objective-C headers (use `#import`), or importing individual framework headers instead of the umbrella header.
- Unsigned integers outside system-interface matching; `long`/`NSInteger` in fixed-size APIs (use `int32_t`/`int64_t`). **(bug risk)**
- Missing Doxygen-style declaration comments on non-trivial public interfaces.

**Application and exceptions:** Inspect retained ownership and accessors, not just property keywords. copy on a mutable collection produces an immutable copy; use mutableCopy when mutation is part of the actual contract.

## Example and review decision

```objc
@property(nonatomic, copy) NSString *name;
// For a custom initializer, direct ivar assignment bypasses a synthesized setter:
_name = [name copy];
```

Document non-obvious ownership/nullability on declarations. Keep imports in dependency order, using framework umbrellas where the project adopts them.
