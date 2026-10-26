# Next.js Review (App Router)

Read alongside `react.md` and `typescript.md`.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [The server/client boundary — the highest-risk area](#the-serverclient-boundary--the-highest-risk-area) · [Server Actions](#server-actions) · [Caching and rendering](#caching-and-rendering) · [Middleware](#middleware) · [Correctness](#correctness) · [Config](#config) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Next.js App Router. Read next/package version, route segment config, cacheComponents, runtime, and deployment adapter. Distinguish Next 14, Next 15, and Next 16 Cache Components; do not infer Pages Router behavior from this file.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## The server/client boundary — the highest-risk area
- Trace client-boundary imports, environment access, and serialized props to actual exposed values. `NEXT_PUBLIC_*` values are intended for browser exposure; non-public environment variables are not automatically inlined into client bundles. Server code can still leak secrets through literals or serialized data. Use `server-only` for modules whose imports must fail across the boundary, and confirm an exposed secret before assigning severity.
- `import 'server-only'` / `'client-only'` guards on modules that must not cross the boundary.
- Props passed from a server to a client component are serialized and visible in the HTML payload. Check for tokens, internal ids, and full user records.
- A server component that becomes a client component in this diff (`'use client'` added) pulls its whole import graph client-side — re-check for secrets and bundle size.

**Evidence and correction:** Inspect the client entry’s transitive imports and the actual rendered/serialized fields. A browser bundle or payload containing a real credential is evidence; a module name or non-public env access alone is not. Keep private work in a server-only module or narrow the returned fields.

## Server Actions
- **A Server Action is a public HTTP endpoint.** It needs its own authentication and authorization check inside the action body; being defined next to a protected page proves nothing.
- Input must be validated in the action — the client can post anything.
- `redirect()` and `notFound()` work by throwing. Calling them inside `try/catch` swallows the control flow; the catch must rethrow or the call must move out.
- After mutations, trace the cache and UI refresh path. Revalidate affected cached data when needed; uncached data, an explicit client update, or another invalidation mechanism may already satisfy the contract.
- Action closures can carry values through a client round trip; encryption is not a substitute for minimizing sensitive capture or checking authorization. Distinguish encrypted closure transport from values directly returned or rendered.

**Evidence and correction:** Treat an action invocation as hostile input regardless of its page. Trace authentication, object ownership, validation, writes, redirects, and failure handling. Verify whether stale views use cached data before prescribing revalidation. Keep action-returned errors free of secrets.

## Caching and rendering
Next.js caching defaults surprise people; treat every change here as behavior change.

- Identify version and cache mode first: Next 14 commonly caches eligible server `fetch` requests; Next 15 changes `fetch` and GET-handler defaults to uncached; Next 16 can enable Cache Components. Explicit cache options, wrappers, route configuration, and deployment behavior still matter. Missing `no-store` alone proves no leak; demonstrate a shared cache returning another user’s data before reporting cross-user exposure.
- Route handlers (`GET`) may be statically cached unless opted out. Check `dynamic`, `revalidate`, `fetchCache` exports.
- Cached results need identity-complete keys/arguments, including user/tenant when applicable. `cacheTag` labels entries for invalidation; it does not itself define the result’s identity. Inspect the cache wrapper or `use cache` arguments and closure inputs.
- Request APIs affect rendering according to the selected cache model. With Cache Components, keep request-specific reads outside shared cached scopes and pass required values explicitly. Do not apply legacy route-segment rules blindly across versions.
- `generateStaticParams` with `dynamicParams: false` returns 404 for anything unlisted.
- Compare application and upstream cache lifetimes; frequent revalidation can still return upstream-stale data. Report only when the resulting staleness or repeated work violates a concrete requirement.

**Evidence and correction:** Write down the result identity, cache layer, lifetime, and invalidation path. Compare two callers with different tenant/user arguments. Shared public data can be cached; personalized cached output must distinguish identities. Unknown version/configuration means the default is unverified, not a confirmed leak.

## Middleware
- Runs on every matched request, so the `matcher` is a security control: a path that fails to match is a path with no middleware auth. Check the matcher against the routes it is supposed to protect, including `/api` and nested segments.
- Middleware auth alone is not enough — server components and actions must still check, since they can be reached in ways middleware may not cover.
- Inspect the actual Node/Edge runtime and deployment adapter. Edge code cannot assume Node-only APIs; limits and driver support vary. Newer projects may use `proxy` rather than legacy middleware conventions.

**Evidence and correction:** Check matcher exclusions and direct entry paths against server authorization. Runtime availability must come from the actual adapter/build configuration; test the excluded route or unsupported API rather than assuming every middleware file runs at Edge.

## Correctness
- Hydration mismatches from non-deterministic render: `Date.now()`, `Math.random()`, locale/timezone formatting, `window` checks.
- `loading.tsx` / Suspense boundaries present so a slow segment does not block the whole page; `error.tsx` per route segment.
- `next/image`: `sizes`/`fill` correctness, remote patterns configured, layout shift.
- `next/font` used rather than a runtime stylesheet request.
- Parallel/intercepting routes: verify the default slot exists, or navigation breaks.
- Metadata: `generateMetadata` async errors, and titles that leak internal ids.

**Evidence and correction:** Compare server-rendered output with the first browser render and test direct navigation plus client navigation for parallel slots. Suspense/error boundaries, images, fonts, and metadata choices merit findings only when a concrete broken experience or applicable policy is shown.

## Config
- `next.config` changes to `rewrites`, `redirects`, `headers` — verify CSP and auth-relevant headers are not weakened, and that a redirect cannot be made open by user input.
- `experimental` flags turned on in a production config.

**Evidence and correction:** Follow rewrite/redirect destinations and header merge behavior. A user-controlled destination or weakened security header needs an execution path. Experimental options require a version/configuration check, not an automatic rejection.

## Worked example and counterexample

```ts
// Personal data cached without identifying the caller: unsafe if both use this entry.
const cached = unstable_cache(() => db.profile(currentUserId), ['profile']);
// Make identity an explicit argument of the cached function.
const cachedByUser = unstable_cache((id: string) => db.profile(id), ['profile']);
await cachedByUser(authenticatedUser.id);
```

Authenticate/authorize before using the ID; cache identity is not authorization. With `use cache`, likewise pass request-derived identity explicitly. A public fetch in Next 15 without `no-store` is not by itself a finding.

## Sources and maintenance

[Next 15 defaults](https://nextjs.org/docs/15/app/guides/upgrading/version-15); [Cache Components](https://nextjs.org/docs/app/api-reference/directives/use-cache); [Previous cache model](https://nextjs.org/docs/app/guides/caching-without-cache-components). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
