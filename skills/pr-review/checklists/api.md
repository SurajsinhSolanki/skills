# API & Integration

## Contracts

- Is every request field validated — type, range, length, enum membership, required vs optional?
- Is the response shape backwards compatible? Removing or renaming a field, or narrowing a type, breaks existing clients.
- Are new fields optional for existing clients?
- Is pagination stable and bounded (max page size, deterministic ordering)?
- Does the route name, method, and status match existing conventions in this codebase?

## Errors

- Correct status codes: 400 vs 401 vs 403 vs 404 vs 409 vs 422 vs 500. A 200 with `{"error": ...}` is a finding.
- Error messages are safe — no stack traces, SQL, internal paths, or existence oracles ("no such user" vs "invalid credentials").
- Validation errors identify the offending field.

## External services

- Is there a timeout on every outbound call? A missing timeout is a reliability finding, not a nit.
- Retry strategy: bounded, backed off, and only on retryable errors.
- Idempotency: if the caller retries, does the remote side duplicate the effect? Is an idempotency key sent?
- Fallback: what does the caller see when the dependency is down — a hang, a 500, or a degraded response?
- Are responses validated before use, or trusted blindly?
- Is the failure logged with enough context to correlate (request id, resource id)?

## Compatibility

- Existing clients on the old version — mobile apps, cached bundles, third-party integrations.
- Versioning: does this change belong behind a new version rather than mutating the current one?
