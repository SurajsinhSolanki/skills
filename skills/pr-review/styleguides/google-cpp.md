# Google C++ Style Guide — Review Checklist

Source: [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [Headers](#headers) · [Naming](#naming) · [To flag](#to-flag) · [Additional local conventions](#additional-local-conventions) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google C++ policy; inspect the project’s C++ standard, exception/RTTI policy, ownership conventions, generated headers, and formatter settings.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- 80-column lines, 2-space indentation. Tooling: `clang-format` (Google style) and `cpplint` — skip what CI enforces.

**Application and exceptions:** Apply formatting through existing tooling; long literals and generated output can have explicit exceptions.

## Headers
- Self-contained headers with `#define` guards named `<PROJECT>_<PATH>_<FILE>_H_`.
- Include order: related header, C system, C++ standard library, other libraries, project headers — blank line between groups.
- Prefer `#include` over forward declarations.

**Application and exceptions:** Compile a header in its intended include environment before asserting a missing dependency. An include guard protects repeated inclusion; it does not prove self-contained declarations.

## Naming
| Kind | Style |
|---|---|
| files | `lower_with_under.cc` / `.h` |
| types, functions | `PascalCase` |
| variables | `snake_case`; class data members `snake_case_` |
| constants, enumerators | `kPascalCase` |
| namespaces | `lowercase` |
| macros | `UPPER_WITH_UNDER` |

**Application and exceptions:** Keep public/interop spellings compatible. Struct fields and class members have different naming conventions.

## To flag
- `using namespace` directives; inline namespaces.
- Static or global objects that are not trivially destructible. **(bug risk)**
- Namespace/class-scope `thread_local` not constant-initialized. **(bug risk)**
- Single-argument constructors and conversion operators not `explicit`. **(bug risk)**
- Copy/move semantics left implicit on a class where they matter — declare or delete them. **(bug risk)**
- Overrides without `override` or `final`. **(bug risk)**
- Non-private data members on classes with invariants; `struct` used for anything but passive data.
- User-defined literals (`operator""`).
- Raw owning pointers — use `std::unique_ptr`; `std::shared_ptr` only with a reason. **(bug risk)**
- C-style casts (other than to `void`). **(bug risk)**
- RTTI outside tests where a virtual method or visitor would do.
- Output parameters where a return value would do.
- Functions much longer than about 40 lines without a reason.
- **Exceptions:** Google's own code does not use C++ exceptions. Apply this only if the repo follows the same policy; in an exception-using codebase, follow the repo.

**Application and exceptions:** Review ownership, lifetime, initialization, and conversions behind bug-risk labels. An intentional borrowed pointer or ABI namespace is different from unsafe ownership; a function-length heuristic alone does not establish a defect.

## Additional local conventions

API documentation: explain ownership, lifetime, preconditions and failure behavior for non-obvious public declarations. Includes provide dependencies; do not duplicate declarations simply to avoid reading a bundled header.

## Example and review decision

```cpp
// Ownership is explicit; a borrowed pointer can still be appropriate elsewhere.
auto item = std::make_unique<Item>();
// Prevent an accidental implicit conversion when that is the intended API.
class ItemId { public: explicit ItemId(int value) : value_(value) {};
 private: int value_; };
```

Use syntax supported by the configured standard and preserve exception-using project conventions.
