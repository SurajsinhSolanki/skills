# Node.js Review (Express · NestJS · Fastify · Koa)

Pair with `typescript.md` for a TS codebase.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Request path](#request-path) · [Async & errors](#async--errors) · [Performance & event loop](#performance--event-loop) · [Data & security](#data--security) · [Operational](#operational) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Node.js server paths using the installed Express, NestJS, Fastify, or Koa version. Error forwarding differs between Express 4 and 5; body/query coercion may be provided by framework validation pipes/plugins. Identify ESM/CJS and supported runtime APIs.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Request path
- Validation runs on every route (zod / class-validator / Joi) — not only in the client.
- Auth middleware is actually applied to the new route; check the router mount, not the intent.
- Ownership/tenant checks on every mutating handler.
- Body size limits and file-upload limits configured.
- Route/query/body values depend on parser, validation, and coercion configuration. Test strings, repeated query arrays, nested objects, null, and missing values before using them as numbers or booleans.

**Evidence and correction:** Trace router mounting, auth/validation, size limits, and normalized input. Test array/object query values and invalid numeric conversion, not only numeric-looking strings. Existing global middleware or pipes may enforce the rule outside the changed handler.

## Async & errors
- Promise rejections need an owner: await/return them to a handler or attach intentional error handling. A floating promise may become an unhandled rejection rather than a silently swallowed error.
- Async errors reach the error middleware — in Express 4, an async handler that throws needs a wrapper or `next(err)`.
- No `process.exit` or unhandled `throw` in a request path.
- `unhandledRejection` / `uncaughtException` behavior not weakened.
- Callback-style APIs not mixed with promises in the same flow.

**Evidence and correction:** Follow the promise returned to the framework. Express 5 forwards returned rejections automatically; Express 4 usually needs an explicit wrapper/next path. Callback errors and detached promises still need ownership. Fix the missing error path without reporting redundant wrappers as required.

## Performance & event loop
- No sync I/O (`fs.readFileSync`, `crypto.pbkdf2Sync`) on the request path.
- CPU-heavy work offloaded to a worker or a job.
- Streams used for large payloads instead of buffering entire files.
- No unbounded in-memory caches or arrays that grow per request.

**Evidence and correction:** Find the actual event-loop blocking operation or unbounded retained resource and estimate request size/concurrency. Streams need backpressure and error cleanup; a small bounded buffer or startup-only synchronous read is not automatically a production issue.

## Data & security
- Parameterized queries / ORM bindings; no template-literal SQL.
- NoSQL injection: object values reaching a Mongo query operator position.
- Prototype pollution: merging untrusted objects, `Object.assign` on user input.
- Secrets from config/env, never literals; `.env` not committed.
- Helmet/CORS/rate-limit configured to match the project's existing posture.
- Inspect new dependency provenance, runtime compatibility, lockfile changes, and adopted dependency policy. Do not invent an additional approval requirement.

**Evidence and correction:** Distinguish bound values from executable identifiers and data objects from operator-bearing query objects. Trace accepted keys through the actual database/client API. A generic merge operation is not prototype pollution without the relevant setter/path behavior.

## Operational
- Timeouts on every outbound HTTP call (`AbortSignal.timeout` or client option).
- Graceful shutdown: in-flight requests drained, DB pool and consumers closed.
- Structured logging with correlation ids; no `console.log` if the project uses a logger.

**Evidence and correction:** Check deadline propagation, in-flight drain, consumer termination, and logging redaction. An upstream timeout may already bound the operation; verify its scope. New dependencies follow existing project approval policy rather than an invented user gate.

## Worked example and counterexample

```js
// Express 4: explicitly forward a rejected async operation.
app.get('/item', (req, res, next) => {
  load().then(item => res.json(item)).catch(next);
});
// Express 5 also supports returning an async handler directly.
app.get('/item', async (req, res) => res.json(await load()));
```

Use one route implementation appropriate to the installed major version; these are alternatives, not two handlers to register together.

## Sources and maintenance

[Express 5 errors](https://expressjs.com/en/5x/guide/error-handling/). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
