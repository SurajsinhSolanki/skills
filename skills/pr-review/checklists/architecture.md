# Architecture & Design

## Verify

- Responsibility is in the right layer: HTTP concerns in the router/controller, business rules in the service, data access in the repository.
- Existing patterns are reused rather than reinvented.
- Abstractions earn their keep — an interface with one implementation and no test double is usually premature.
- The design will survive the next likely requirement.

## Flag

- **Business logic in the wrong layer** — rules in a controller, HTTP status decisions in a repository, SQL in a view.
- **Layer bypass** — a router touching the DB session directly, a component calling `fetch` instead of the API layer.
- **Tight coupling** — a module reaching into another's internals; a change here forcing a change there for no domain reason.
- **Duplicated business logic** — the same rule expressed in two places will diverge. Name both locations.
- **Branching on type instead of registering behavior** — `if kind == "a" ... elif kind == "b"` where a registry or polymorphism exists.
- **God objects / god functions** — one unit doing validation, orchestration, persistence, and formatting.
- **Hardcoded values that belong in config** — URLs, limits, feature toggles, mappings the backend should own.
- **State duplicated across sources of truth** — the same fact stored in two places with no reconciliation.

## Judgement

Only flag design when you can name the concrete future cost. "This is not clean" is not a finding; "adding a third variant requires editing five files because the mapping is inlined, and the existing two already disagree" is.
