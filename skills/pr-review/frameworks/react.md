# React / TypeScript Review

Written for a modern React app with a server-state library (TanStack Query, SWR, RTK Query) and a client-state store (Zustand, Redux, Jotai). Pair with `typescript.md`, and with `nextjs.md` for an App Router project. Skip any section the project does not use.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [State boundaries](#state-boundaries) · [Hooks & rendering](#hooks--rendering) · [Components](#components) · [Quality gates](#quality-gates) · [TypeScript](#typescript) · [Before approving](#before-approving) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

React function components and Hooks; inspect React version, compiler/lint settings, router, and installed data libraries. The special use API belongs to React 19+. Server components and framework caches need their matching framework pass.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## State boundaries
- Follow the project’s state ownership. Duplicated server data becomes a finding when updates diverge or stale state affects behavior; an intentional editable draft or snapshot is valid.
- Server data copied into `useState` on mount goes stale — flag it unless the copy is an intentional editable draft.
- Query keys include every input the query depends on, or the cache serves the wrong data.
- Mutations invalidate or update the right keys; optimistic updates roll back on error.
- Cache lifetime is deliberate — stale data shown after a mutation is a correctness bug, not a cosmetic one.
- `enabled` guards on queries that need a param that may be undefined.

**Evidence and correction:** Identify the authoritative owner of each value and the mutation/refetch path. Test switching users/filters and a failed optimistic update. Fix the key, rollback, or synchronization responsible for stale data; do not require a new store library.

## Hooks & rendering
- Effects have correct dependencies; no lying dependency arrays.
- No effect that only derives state from props — compute during render.
- Cleanup returned from effects that subscribe, time out, or open connections.
- Ordinary Hooks require stable call order. React 19’s `use` API has specific conditional/loop allowances; do not generalize those to `useState` or `useEffect`. Check the installed React/compiler version.
- Stable keys in lists — never the array index for reorderable data.
- Memoization only where a real cost exists; unnecessary `useMemo`/`useCallback` is noise.
- Event handlers not recreated in a way that breaks a memoized child's contract.
- Async work in effects is cancelled or ignored after unmount.

**Evidence and correction:** Read dependencies, captured values, setup and cleanup together. Development Strict Mode can intentionally repeat setup/cleanup; duplicate setup is a defect only when observable resources or state are left inconsistent. Re-run with changing inputs to establish a race.

## Components
- Follow project naming and module boundaries; multiple related components per file are valid. Custom Hooks use the `use` prefix so tooling and callers recognize their contract.
- Reuse existing UI primitives rather than adding a parallel implementation.
- Verify required props and defaults express real states. Pass-through props at several levels are not a defect without concrete complexity or a documented boundary rule.
- Different UI patterns stay separate components — do not fuse them behind a `variant` flag that branches heavily.
- Values the server owns (options, permissions, availability, limits) are fetched, never hardcoded in the client.

**Evidence and correction:** Judge boundaries by caller contracts and actual maintenance burden. A related local helper component or variant can be appropriate. Check optional props for undefined behavior and server-controlled decisions against the real API, rather than enforcing a file or prop-depth quota.

## Quality gates
- Loading, error, and empty states all handled — not just the success path.
- Route-level error boundaries present for new routes.
- Accessibility: labels tied to inputs, keyboard reachable controls, focus management on dialogs, `aria-*` where role is not implicit, no click-only handlers on non-interactive elements.
- Trace HTML provenance into `dangerouslySetInnerHTML`; untrusted unsanitized HTML is a vulnerability. Trusted or correctly sanitized HTML is a valid use; verify the sanitizer and its configuration.
- Forms: validation errors announced, submit disabled or guarded against double submit.
- If the project has an i18n layer, user-facing strings go through it rather than being inlined.

**Evidence and correction:** Exercise slow, empty, failed, repeated-submit, keyboard, and focus-return paths. A library may supply a boundary or dialog behavior outside the diff; verify it before requiring another one. For HTML sinks, demonstrate that untrusted input reaches an unsanitized sink.

## TypeScript
- No unjustified `any`, no `as` casts that paper over a real mismatch, no `@ts-expect-error` without a reason.
- Discriminated unions rather than optional-field soup for variant data.
- API response types match the backend contract — verify against the endpoint, not against hope.

**Evidence and correction:** Compare types with actual producer/consumer behavior. An intentional assertion at a validated boundary is not the same as assuming an untrusted response is valid. Use the existing error variant or narrowing strategy to restore the contract.

## Before approving
Use the project's declared lint/type/test commands under [Running the project's gates](../SKILL.md#running-the-projects-gates). That section governs snapshot matching, authorization, failure attribution, and reporting; a failed command alone does not establish an introduced blocker.

**Evidence and correction:** CI configuration is not a result; use the shared gate rules to determine what was actually checked.

## Worked example and counterexample

```jsx
// Race-prone: an older request can overwrite a newer selection.
useEffect(() => { load(id).then(setRecord); }, [id]);

// Ignore obsolete completions; add AbortController if load supports it.
useEffect(() => {
  let ignore = false;
  load(id).then(record => { if (!ignore) setRecord(record); });
  return () => { ignore = true; };
}, [id]);
```

Handle rejection in the real component. This example addresses ordering, not the full loading/error UI.

## Sources and maintenance

[Effect synchronization](https://react.dev/learn/synchronizing-with-effects). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
