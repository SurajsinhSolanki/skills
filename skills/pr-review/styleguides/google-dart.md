# Google Dart Style Guide — Review Checklist

Source: [Effective Dart: Style](https://dart.dev/effective-dart/style) (linked from Google's style guide index). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [Naming](#naming) · [Directives](#directives) · [Additional local conventions](#additional-local-conventions) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Effective Dart style with installed SDK language version and formatter configuration. Existing constant-name or generated-code conventions can override the default naming preference.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- `dart format` output is the standard — skip formatting findings if CI runs it. Lines up to 80 characters.
- Curly braces on all flow control, except a single-line `if` with no `else`.

**Application and exceptions:** dart format may use a configured page width; strings/URIs and semantic multiline text have exceptions. A style preference does not prove invalid syntax.

## Naming
| Kind | Style |
|---|---|
| classes, enums, typedefs, extensions, type parameters | `UpperCamelCase` |
| packages, directories, files, import prefixes | `lowercase_with_underscores` |
| members, variables, parameters, constants | `lowerCamelCase` (keep existing `SCREAMING_CAPS` only for consistency) |

- Acronyms over two letters capitalized as words (`HttpClient`); two-letter acronyms keep English capitals (`ID`, `UI`) except at the start of a `lowerCamelCase` name.
- No leading underscore on non-private names; no Hungarian prefixes. `_` for unused callback parameters.

**Application and exceptions:** Private names use _, while public constants normally use lowerCamelCase. Keep API spelling compatible.

## Directives
- Order: `dart:`, `package:`, relative imports, then exports — separate sections, alphabetical within each.

**Application and exceptions:** Group dart:, package:, relative imports and exports; do not change the actual import target solely to reorder it.

## Additional local conventions

Documentation and language conventions: /// comments describe public contracts; use effective nullability and supported async constructs. Do not rewrite generated imports or legacy constants without a changed-line policy reason.

## Example and review decision

```dart
import 'dart:async';

import 'package:app/model.dart';

/// Loads the current user, reporting failure through the returned Future.
Future<User> loadUser() => repository.load();
```

The imported model/repository are project context. This illustrates organization, not a required architecture.
