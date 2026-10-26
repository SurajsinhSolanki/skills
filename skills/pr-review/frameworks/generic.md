# Framework-Independent Review

Use this when the stack has no dedicated file, or alongside one.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Trace the layers](#trace-the-layers) · [Universal smells](#universal-smells) · [Language-agnostic correctness](#language-agnostic-correctness) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Fallback for a language/stack without a dedicated pass, or cross-boundary checks alongside one. Establish language/runtime, data model, concurrency, and project conventions locally. This file does not prescribe a service/repository architecture.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Trace the layers
```
Entry point (controller / route / handler / CLI / consumer)
    ↓
Validation & authorization
    ↓
Service / business logic
    ↓
Repository / data access
    ↓
Models / entities
    ↓
Database & external systems
```

Treat these as possible responsibilities, not a mandatory architecture. At each existing boundary, check ownership, invariants, and errors. A small CLI may combine several responsibilities safely; require a new layer only when an adopted rule or concrete defect calls for it.

**Evidence and correction:** Trace the changed input through the boundaries the project actually has. At each one, identify the precondition, representation, owner, and error result. Fix the earliest causal contract violation, citing later callers as evidence; a missing abstract layer is not itself a defect.

## Universal smells
- Business rules or data access duplicated across entry points with inconsistent invariants.
- Multiple owners applying incompatible transactions or authorization.
- Entity serialization exposing fields outside the intended transport contract.
- Configuration read via ad-hoc environment lookups scattered through the code instead of one settings object.
- Global mutable state.
- Silent type coercion at a boundary.
- Errors converted to `null`/`false` and then not checked.

**Evidence and correction:** For each candidate smell, show an observable consequence: two authorization paths disagree, mutable global state mixes identities, or a swallowed error becomes success. Consolidate only the duplicated invariant needed to fix that result; preserve legitimate cached/snapshot/config ownership.

## Language-agnostic correctness
- Integer/float boundaries, division by zero, money as float.
- Timezone and DST handling; naive vs aware datetimes.
- String encoding at I/O boundaries.
- Mutable default arguments / shared mutable defaults.
- Comparison of floats or of objects by identity.
- Iteration over a collection while mutating it.

**Evidence and correction:** Use boundary values with the actual language semantics: overflow versus arbitrary-precision arithmetic, decimal versus binary rounding requirements, ambiguous local timestamps, invalid encodings, aliases, and concurrent mutation. Recommend the project’s existing safe representation and error contract.

## Worked example and counterexample

```python
# Defect: failed parsing is silently turned into a successful zero count.
try:
    count = int(raw)
except ValueError:
    count = 0
# Correction when invalid input must be rejected: return a validation error
# from the existing boundary instead of substituting a valid business value.
```

A documented default-on-invalid contract can make the original code intentional. Evidence needs the requirement or a downstream failure, not a dislike of fallback values.

## Sources and maintenance

[Python default semantics example](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
