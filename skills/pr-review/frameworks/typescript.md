# TypeScript Review

Applies to any TS codebase — Node, React, Vue, Angular, Deno. Pair with the framework file.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Type soundness](#type-soundness) · [Types are not validation](#types-are-not-validation) · [Modelling](#modelling) · [Async](#async) · [Interop and imports](#interop-and-imports) · [Errors](#errors) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

TypeScript with compiler version, strict flags, module resolution, emit target, runtime/transpiler, and lint configuration inspected locally. Numeric enum checks and narrowing evolve across compiler releases. Google-specific style is a separate opt-in, not a condition of TypeScript correctness.

This file supplies the local review guidance; links below are optional source attribution. Use local project evidence, and record unsupported version-dependent behavior as unverified.

## Type soundness
- `any` without a stated reason. Each one disables checking for everything it touches downstream.
- Assertions do not validate runtime shape. A double assertion bypasses compatibility checks; establish the invariant at the boundary before reporting a downstream access as safe or unsafe.
- Non-null assertions (`x!`) on values that can genuinely be null — a crash moved from compile time to runtime.
- Inspect suppressions for the actual error hidden and any justification. `@ts-expect-error` detects an unused suppression, but still hides all errors on its next line. Google-style restrictions apply only through the separate style opt-in; negative type tests may intentionally suppress errors.
- Inspect weakened compiler checks and resulting errors hidden by the change. A flag change alone does not determine severity: identify a concrete defect or a confirmed violation of an applicable required gate.
- Array/record index access typed as `T` rather than `T | undefined` when `noUncheckedIndexedAccess` is off — `arr[i]` and `map[key]` can both be undefined.

**Evidence and correction:** Trace the exact unsafe value and downstream dereference, not just an any/as token. A suppression may be a deliberate negative type test. Compile using the existing project settings when possible, and distinguish suppressed diagnostics from runtime failures.

## Types are not validation
- Types are erased at runtime. At untrusted boundaries (`JSON.parse`, responses, storage, env, messages), trace validation or a trusted producer contract before relying on the shape. Use existing validation tools; a new schema library is not mandatory at every boundary.
- `process.env.X` is `string | undefined`; a non-null assertion on it means the app boots and fails later.
- Compare generated clients with changed producer contracts and actual callers. Compatible additive changes or generated-on-build clients may need no tracked type edit; report a concrete stale assumption.

**Evidence and correction:** Find the trust boundary and established validation contract. Test a missing field, null, wrong type, and unexpected discriminant. Fix the missing validation or consumer assumption with existing tools; typing JSON.parse does not validate its result.

## Modelling
- Optional-field soup where a discriminated union belongs. If two of five fields are only valid together, encode that: `{kind: 'a', x} | {kind: 'b', y}`.
- `switch` over a union with no exhaustiveness guard. A `default: assertNever(x)` turns a future added variant into a compile error instead of silent fallthrough.
- Enums and string unions can both model variants. Numeric enum assignability depends on compiler version and whether a value is a literal or a broad number; do not claim every number literal is accepted. Validate external numeric values against allowed members when the runtime contract requires it. `const enum` policy belongs to opted-in style or the actual transpiler configuration.
- Fresh object literals receive extra excess-property checks; structural assignment can admit additional fields. Check satisfies/annotations/compiler settings and runtime serialization before treating structural compatibility as an unintended exposure.
- Unconstrained generics (`<T>` used as `any`), or generics with one call site that could be a plain parameter.
- Mutable shared types: prefer `readonly` arrays/props for data that must not be mutated by a consumer.

**Evidence and correction:** Test invalid combinations and actual consumer branches. A tagged union or readonly type is useful when it makes a violated invariant enforceable, but equivalent existing models are valid. Runtime enum values still need validation independently of compile-time assignability.

## Async
- Floating promises can leave rejections unhandled or results ignored. Follow the actual owner/catch path and respect configured no-floating-promises rules; intentional background work still needs lifecycle and error ownership.
- `async` functions passed where a void callback is expected — the rejection has nowhere to go.
- `Promise.all` rejects its result when one input rejects; it does not cancel other work. If every outcome must be recorded, use `allSettled` or explicit per-task handling; if work must stop, add an actual cancellation mechanism.
- Narrowing lost across `await` or a callback: a null check before `await` does not hold after it if the value is a mutable field.
- `try/catch` around `await` that catches and returns a default, hiding a real failure.

**Evidence and correction:** Observe both caller completion and background side effects when a promise fails. A void callback can discard an async rejection; add an owned catch/return path. Promise.all does not cancel siblings, so cleanup/idempotency must account for continued work.

## Interop and imports
- `import type` used for type-only imports where the project's `verbatimModuleSyntax`/`isolatedModules` setting requires it.
- Default vs named export inconsistency with the rest of the codebase.
- Deep imports into another module's internals rather than its public entry point.
- Module augmentation / `declare global` that widens a global type for the whole project.

**Evidence and correction:** Inspect output imports and the actual bundler/runtime before recommending syntax. Type-only imports should not create runtime dependencies; internal imports or global augmentations need a concrete compatibility/coupling impact rather than a naming preference.

## Errors
- `catch (e)` where `e` is `unknown` — check it is narrowed before `e.message` is read.
- Custom error classes without `instanceof` safety after transpilation to ES5.
- Throwing non-Error values (strings, objects), which lose stack traces.

**Evidence and correction:** Identify which errors callers match and how the runtime constructs their prototypes/stacks. Narrow unknown catch values or normalize them through the existing error boundary; verify an ES5 instanceof issue with the actual emitted code before claiming it.

## Worked example and counterexample

```ts
// Defect: assertion trusts an unvalidated boundary value.
const value = JSON.parse(raw) as { count: number };
const total = value.count + 1;
// Correction at this boundary using existing validation, or an explicit check:
const candidate: unknown = JSON.parse(raw);
if (typeof candidate !== 'object' || candidate === null ||
    !('count' in candidate) || typeof candidate.count !== 'number') {
  throw new Error('invalid count');
}
```

Handle parse failures using the project’s error contract. An intentional @ts-expect-error in a negative type test is not by itself a production bug or an adopted Google-style violation.

## Sources and maintenance

[TypeScript 5.0 enum changes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html); [TypeScript 5.4 assignability](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-4.html). Source checks: **2026-10-26**. Summarized in original wording for review; the linked manuals are not runtime dependencies.
