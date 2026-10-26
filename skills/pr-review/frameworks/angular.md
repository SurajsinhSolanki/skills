# Angular Review

Pair with `typescript.md`.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Subscriptions and RxJS — the top defect source](#subscriptions-and-rxjs--the-top-defect-source) · [Change detection](#change-detection) · [DI and services](#di-and-services) · [HTTP](#http) · [Forms](#forms) · [Routing and security](#routing-and-security) · [Consistency](#consistency) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Angular with RxJS; inspect Angular/RxJS versions, standalone versus NgModule setup, signals, and zone/zoneless configuration. takeUntilDestroyed is available in Angular 16+; use the project’s compatible lifecycle mechanism.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Subscriptions and RxJS — the top defect source
- Long-lived subscriptions need ownership and teardown. Finite streams such as a normal completed HttpClient request do not create a permanent subscription leak merely because no destroy operator exists; still consider cancellation, callbacks after destruction, and changed retry behavior.
- Prefer the `async` pipe over manual subscribe; a component that subscribes and assigns to a field usually should not.
- Nested `subscribe` inside `subscribe` — a race and a leak. `switchMap` (cancel previous), `concatMap` (queue), `mergeMap` (parallel), `exhaustMap` (ignore while busy). Picking the wrong one is a real bug: `mergeMap` on a save button allows out-of-order writes; `switchMap` on a save cancels a write that already reached the server.
- `shareReplay` retention depends on configuration, source completion, and subscriber lifetime. Inspect whether an infinite upstream remains subscribed after all consumers leave; choose ref-counting or explicit lifecycle management when that ownership is required.
- `Subject` used where `BehaviorSubject` semantics are needed (late subscribers get nothing).
- Errors in a stream terminate it — an HTTP error inside a `switchMap` without `catchError` kills the outer stream permanently.
- `combineLatest` emits only after every source has emitted once.

**Evidence and correction:** Trace source completion and ownership before claiming a leak. Demonstrate duplicate side effects after destroy/navigation or an orphaned infinite upstream. Choose flattening operators for the intended ordering; unsubscription does not undo a server write already accepted.

## Change detection
- OnPush can miss in-place input changes when no notification marks the view for checking; events, signals, and explicit marking can also trigger checks. Reproduce the stale view before asserting every mutation is invisible.
- Mutating an array in place (`push`) with `OnPush` or with `trackBy` by index.
- `markForCheck`/`detectChanges` sprinkled to force rendering — usually a symptom of a mutation bug.
- Functions or getters called from a template run on every change-detection cycle; anything expensive there is a performance finding.
- `*ngFor` without `trackBy` on a list that is replaced by a new array — full DOM rebuild.
- Signals (v16+): mixing signals and manual change detection inconsistently; `effect()` used for data derivation where `computed()` belongs; writes inside an `effect` causing loops.

**Evidence and correction:** Test an input change originating outside local events and confirm how the view is notified. Signals and zoneless scheduling change trigger assumptions. Require stable item identity when preservation of DOM/component state matters, not merely because an array instance changed.

## DI and services
- Service state in a `providedIn: 'root'` singleton that holds per-user or per-route data, not cleared on logout or navigation.
- Provider declared at the wrong level (component vs module vs root), yielding either an unexpected shared instance or an unexpected fresh one.
- Injecting a service into a component only to pass it through — pass data, not the service.

**Evidence and correction:** Locate provider registration and consumer lifetime. Reproduce stale identity data after logout or a duplicated state owner after navigation. Correct the scope/reset path; do not ban singleton services or pass-through injection categorically.

## HTTP
- No `catchError` and no user-visible error path.
- No timeout on calls that can hang; no retry policy, or retry on non-idempotent requests.
- Interceptor order matters — an auth interceptor added after an error interceptor changes behavior. Check the array order, not just the presence.
- Interceptors attaching tokens to *every* outbound request, including third-party hosts.

**Evidence and correction:** Inspect effective interceptor order and destination allowlists. Test an unauthorized host, a timeout, and a failed retry. Retry a write only with idempotency or a contract proving duplicate execution is safe.

## Forms
- Reactive vs template-driven mixed in one feature.
- Validators present but errors never displayed; `updateOn: 'blur'` vs default; async validators without debounce hammering the server.
- `disabled` set via the template on a reactive control (Angular warns and ignores it).
- `patchValue` vs `setValue` semantics when the shape is partial.
- Double submit not guarded.

**Evidence and correction:** Compare form model, template, and user-visible errors. Test a partial patch, disabled-control submission, and a double click. Mixing form styles is a finding only when values/validation diverge or an adopted rule forbids it.

## Routing and security
- **Route guards are client-side only.** `canActivate` is UX, never authorization — the server must enforce it. A PR that adds a guard and calls the feature "secured" is a finding.
- The router uses the first emitted guard value and unsubscribes; completion is not required. A guard that never emits can leave navigation waiting. Check redirect/false behavior and errors as well.
- Trust-bypass calls disable framework sanitization for a security context. Trace the input and actual sink; attacker-controlled unsanitized HTML/URLs can be exploitable, while reviewed trusted content can be intentional.
- Lazy-loaded routes: verify the module/component actually splits and that guards apply to the lazy route.
- Query/route params are strings — check parsing before numeric use.

**Evidence and correction:** Call the underlying endpoint without the UI guard. Guards need a first result, not completion; a never-emitting source is the waiting case. Verify actual sanitizer bypass provenance and route-param conversion.

## Consistency
- Standalone components vs NgModules mixed inconsistently within a feature.
- `strictTemplates` weakened in `tsconfig`.
- `zone.js` `runOutsideAngular` used without a matching `run()` to re-enter.

**Evidence and correction:** Check local migration/configuration intent. Standalone and NgModule interoperability or runOutsideAngular can be valid; demonstrate missing view updates or policy violations instead of treating mixed APIs as defects.

## Worked example and counterexample

```ts
// An infinite source owned by a component needs lifetime control.
this.events.pipe(takeUntilDestroyed(this.destroyRef)).subscribe(handleEvent);
// A finite one-shot stream can complete normally without leaking a subscription.
this.http.get('/api/item').subscribe(handleItem);
```

The second example still needs error handling and may need cancellation after destroy. A guard `of(true)` is valid: the first value permits navigation even if another stream type would remain open.

## Sources and maintenance

[Lifecycle teardown](https://angular.dev/api/core/rxjs-interop/takeUntilDestroyed); [Guard return semantics](https://angular.dev/guide/routing/route-guards). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
