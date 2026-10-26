# Google C# Style Guide — Review Checklist

Source: [C# at Google Style Guide](https://google.github.io/styleguide/csharpguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [Naming](#naming) · [Organization](#organization) · [To flag](#to-flag) · [Additional local conventions](#additional-local-conventions) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google C# policy, which differs from common Microsoft formatting defaults. Inspect target language version, .editorconfig, nullability, and generated bindings.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- Column limit 100, 2-space indentation, no tabs; continuations +4.
- No line break before an opening brace; braces even when optional. One statement and one assignment per line.

**Application and exceptions:** Two-space same-line braces belong to this opt-in policy; the repository’s enforced formatter wins.

## Naming
| Kind | Style |
|---|---|
| classes, methods, enums, namespaces, public fields and properties | `PascalCase` |
| locals, parameters | `camelCase` |
| private, protected, internal fields and properties | `_camelCase` |
| interfaces | `I` prefix |
| files, directories | `PascalCase`, file named after its main class |

Acronyms as words: `MyRpc`, not `MyRPC`.

**Application and exceptions:** Match access-level naming, including _camelCase non-public fields. Public API casing does not force changing a third-party interface.

## Organization
- Modifier order: `public protected internal private new abstract virtual override sealed static readonly extern unsafe volatile async`.
- `using` directives alphabetical, `System` first.
- Member order: nested types, static/const/readonly fields, fields and properties, constructors, methods — by access level within each group.

**Application and exceptions:** Follow the listed order only where no project formatter or stronger convention specifies it; ordering does not establish runtime safety.

## To flag
- Values that could be `const` but are not (or `readonly` when `const` is impossible).
- Mutable collection types on inputs — accept `IReadOnlyList`/`IReadOnlyCollection`/`IEnumerable`.
- Structs used for anything but small value-like types.
- Non-trivial (more than ~2 statements) or reused lambdas — make them named methods.
- `ref` parameters, or `out` not placed last.
- Extension methods on types whose source the project owns.
- `Tuple<>` in APIs where a named class would be clearer.
- Repeated string concatenation in loops — `StringBuilder`.
- Removing from a collection while iterating it — `RemoveAll` or rebuild. **(bug risk)**
- Delegate invocation without a null check — `handler?.Invoke()`. **(bug risk)**
- Bare `bool` arguments at call sites — use named arguments, enums, or an options type.
- `var` hiding a non-obvious type, especially numeric types.

**Application and exceptions:** Choose input interfaces by the capabilities actually needed. A nullable delegate or modified collection is a bug only on a reachable invocation/iteration path.

## Additional local conventions

Documentation: use XML documentation on non-obvious public contracts, including nullability and thrown exceptions. Keep using directives grouped and ordered as above; aliases can be valid for interop or ambiguity.

## Example and review decision

```csharp
// Preserve null-safe event invocation when there may be no subscribers.
Changed?.Invoke(this, EventArgs.Empty);
// A read-only input contract need not expose mutation.
int CountItems(IReadOnlyCollection<Item> items) { return items.Count; }
```

IEnumerable is useful for one-pass lazy input; do not materialize it solely to match the example.
