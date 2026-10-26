# Vue Review (Vue 3 / Composition API / Nuxt)

Pair with `typescript.md`.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Reactivity — where most Vue bugs live](#reactivity--where-most-vue-bugs-live) · [Composables and lifecycle](#composables-and-lifecycle) · [Template](#template) · [State (Pinia / Vuex)](#state-pinia--vuex) · [SSR / Nuxt](#ssr--nuxt) · [Quality](#quality) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Vue 3 Composition API; inspect matching vue/compiler-sfc versions and Nuxt/Pinia versions. The Vue 3.5 defineProps transform applies within script setup, not arbitrary object destructuring. Vue 2 and Options API code need locally verified equivalents.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Reactivity — where most Vue bugs live
- Destructuring a primitive from an ordinary reactive object loses tracked access. In Vue 3.5+, variables destructured directly from `defineProps()` in the same `<script setup>` block are compiler-rewritten and remain reactive when accessed there. Vue 3.4 and earlier lack that default transform. This exception does not apply to arbitrary `reactive()` objects or passing a current value to another function.
- `ref` vs `reactive` consistency; `.value` forgotten in script (silent wrong behavior) or wrongly written in template.
- Replacing a `reactive` object wholesale (`state = {...}`) breaks the proxy link; mutate properties or use a `ref`.
- Props mutated directly — Vue warns, but a mutated object prop mutates the parent's state silently.
- `computed` with side effects (fetching, mutating, logging) — computeds must be pure and can run more than once.
- `watch` on a getter vs a ref: watching `props.obj.x` needs a getter function, otherwise it never fires.
- `deep: true` watchers on large objects are a real cost; `immediate: true` changes first-run semantics.
- `watchEffect` tracks reactive accesses made synchronously on each execution. Conditional dependencies can change on later runs; accesses after the first `await` are not tracked by the initial synchronous run.
- Watchers that start intervals, listeners, or requests need cleanup via the `onCleanup` argument or `onScopeDispose`.

**Evidence and correction:** Identify whether code is compiler-transformed script setup or ordinary JavaScript. Change a prop after mount and observe the derived value. Preserve tracked property access with a getter/ref where needed; do not demand toRefs for a supported transform.

## Composables and lifecycle
- Lifecycle registration and injection require an active component context. Async `<script setup>` has compiler-supported context restoration; plain async callbacks may not. A condition/loop is not inherently invalid as with React Hooks: inspect which APIs the composable uses and when it runs.
- `onUnmounted`/`onScopeDispose` cleanup for listeners, timers, observers, and subscriptions.
- Module-scope state in a composable is a singleton shared by every component instance — sometimes intended, often an accidental cross-component leak.
- `nextTick` used to paper over an ordering bug rather than fixing the dependency.

**Evidence and correction:** Inspect the APIs a composable calls, its registration time, and the owner that disposes resources. A utility with no lifecycle dependency can run outside setup. Fix missing ownership/cleanup, not the mere presence of an await or conditional.

## Template
- `v-html` with untrusted unsanitized content is XSS. Verify input provenance and sanitization rather than treating every dynamic HTML value as unsafe.
- `v-for` with `v-if` on the same element: `v-if` evaluates first and cannot see the loop variable — filter in a computed instead.
- `:key` present and stable; never the array index for reorderable or filtered lists.
- `v-model` on a prop, or a custom `v-model` whose `update:` event name does not match.
- Event listeners on components without `emits` declared, so they land as native attrs via `inheritAttrs`.
- Expensive expressions inline in the template re-evaluate on every render — move to `computed`.

**Evidence and correction:** Check directive precedence, keyed identity, event fallthrough, and HTML trust with a real input/state change. Browser warnings can guide inspection but are not a substitute for the failing path. Prefer a filtered computed collection when v-if needs the loop item.

## State (Pinia / Vuex)
- Pinia `state` must be a function returning fresh state; a shared object leaks between instances and, on SSR, between requests.
- Server data cached in a store with no invalidation, shown stale after a mutation.
- Actions that mutate other stores in a cycle.
- `storeToRefs` used when destructuring, otherwise reactivity is lost.

**Evidence and correction:** Trace store creation per app/request and cache invalidation on user changes. An intentional app singleton is fine; server-side request data in a module singleton can cross users. Preserve reactivity when extracting store state, but leave actions as functions.

## SSR / Nuxt
- **Module-level mutable state on the server is shared across every request** — a user's data can be served to another user. Treat any singleton holding request data as CRITICAL.
- `useState`/`useAsyncData` keys must be unique and must include user/tenant identity where the data is per-user.
- `useAsyncData`/`useFetch` — check `server`, `lazy`, `watch`, and that errors are surfaced rather than silently empty.
- Browser-only APIs (`window`, `document`, `localStorage`) accessed during SSR — must be guarded or moved into `onMounted`/`<ClientOnly>`.
- Server routes in `server/api` are public endpoints: they need their own auth and validation.
- Runtime config: private keys must not be in the `public` block.
- Hydration mismatch from dates, random values, or locale formatting.

**Evidence and correction:** Compare requests for two identities and initial hydration against browser navigation. Scope private runtime config and caches to their real lifetime. Do not key identical public data per user unnecessarily; do not expose private fields in serialized state.

## Quality
- Loading, error, and empty states handled — not just success.
- Accessibility: labels bound to inputs, focus trapped in dialogs, keyboard-reachable custom controls.
- `defineProps` with types and required flags rather than implicit defaults.

**Evidence and correction:** Check form errors and keyboard/focus behavior, using the project’s UI components before requiring new ones.

## Worked example and counterexample

```ts
// Vue 3.5+ script setup: valid reactive access to a destructured prop.
const { userId } = defineProps<{ userId: string }>();
watch(() => userId, reload); // getter preserves a tracked source
// watch(userId, reload) passes the current string instead: not a source.
```

Ordinary `const { count } = reactive({ count: 0 })` still extracts a primitive; use `state.count` or a ref when later updates must be observed.

## Sources and maintenance

[Props and 3.5 destructuring](https://vuejs.org/guide/components/props.html#reactive-props-destructure); [Watchers](https://vuejs.org/guide/essentials/watchers.html). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
