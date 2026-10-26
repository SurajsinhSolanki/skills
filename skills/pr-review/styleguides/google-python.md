# Google Python Style Guide — Review Checklist

Source: [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [Naming](#naming) · [Imports](#imports) · [Docstrings and comments](#docstrings-and-comments) · [Language rules to flag](#language-rules-to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Python 3 Google-style policy; recognize generated code and project formatter/config exceptions. This is not the Pydantic model-default rule.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- Line limit 80 columns (long imports, URLs, and pylint-disable comments excepted). A team or repo setting overrides this.
- 4-space indentation, no tabs, no semicolons.
- Tooling Google names: `pylint` for linting, Black or Pyink for formatting, pytype for type checking.

**Application and exceptions:** Formatting exceptions apply to long paths/URLs and syntax where wrapping harms meaning; do not restyle formatter-owned output.

## Naming
| Kind | Style |
|---|---|
| modules, packages, functions, methods, variables | `lower_with_under` |
| classes, exceptions | `CapWords` |
| constants | `CAPS_WITH_UNDER` |
| internal (module- or class-private) | leading `_` |

Single-letter names only for counters, `e` in exception handlers, `f` for file handles, and private unconstrained type variables.

**Application and exceptions:** Keep acronym and public/private naming consistent without renaming external overrides merely to match a local preference.

## Imports
- Import modules and packages, not individual classes or functions (`typing`, `collections.abc`, and `typing_extensions` are exempt).
- Full package paths; no relative imports.
- Order: `__future__`, standard library, third-party, then local — one group each.

**Application and exceptions:** A qualified module import makes ownership visible; typing-related and documented interoperability exceptions remain valid.

## Docstrings and comments
- Triple double quotes. One-line summary ending in a period.
- Functions: `Args:`, `Returns:` (or `Yields:`), `Raises:` sections where applicable. Classes: `Attributes:` for public attributes.
- Logging calls take a pattern string plus arguments, never an f-string.

**Application and exceptions:** Document parameters, results, and raised errors that callers need; omit empty sections on trivial functions. Deferred logging avoids unnecessary formatting work.

## Language rules to flag
- Mutable default arguments — use `None` and create inside. **(bug risk)**
- Bare `except:` or `except Exception` without re-raising or a clear isolation point. **(bug risk)**
- `assert` used for runtime validation or control flow — asserts can be stripped. **(bug risk)**
- `try` blocks wider than the call that can fail, hiding unrelated errors. **(bug risk)**
- `== None` instead of `is None`; comparing to `True`/`False` with `==`. **(bug risk)**
- `if len(seq):` instead of `if seq:`; but compare integers to `0` explicitly so `None` is not confused with zero. **(bug risk)**
- String building with `+` in a loop — use `"".join(...)`.
- Mutable module-level state without a leading `_` and a reason.
- `staticmethod` where a module-level function would do.
- "Power features" (metaclasses, bytecode access, dynamic inheritance, `__del__`) without strong justification.
- Comprehensions with more than one `for` clause.
- Executable scripts without a `main()` and `if __name__ == "__main__":` guard.
- Type annotations encouraged on public APIs; `X | None` (or `Optional[X]`) for nullable values.

**Application and exceptions:** A bug-risk label calls for a concrete input/state and wrong result. Truthiness is valid for containers but may differ from None/zero checks; do not assign bug severity from syntax alone.

## Example and review decision

```python
# Shared function default: two callers can affect each other.
def collect_bad(item, items=[]):
    items.append(item)
    return items

# Fresh collection when the caller omits it.
def collect_good(item, items=None):
    items = [] if items is None else items
    items.append(item)
    return items
```

A mutable Pydantic v2 model default is a different mechanism; inspect the framework pass before claiming sharing.
