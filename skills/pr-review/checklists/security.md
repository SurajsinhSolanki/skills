# Security

Treat every item as required for HIGH-risk changes.

## Authentication

- Is the endpoint / route / job authenticated at all? Check the actual dependency or middleware, not the assumption.
- Can auth be bypassed — an unauthenticated variant of the route, a debug flag, a health path with real capability?
- Are tokens/sessions validated for expiry, signature, and audience?

## Authorization

- **IDOR** — is the resource fetched by ID and then returned without checking the caller owns it?
- **Missing ownership checks on writes** — updates and deletes need the same check as reads, and more.
- **Tenant isolation** — is the tenant/org/workspace scope applied in the query itself, or filtered in memory after fetching everything?
- **Privilege escalation** — can a user set their own role, owner_id, or permission fields through the request body?
- Is the authorization decision made server-side, not inferred from a client-supplied flag?

## Input

- SQL injection — string-built queries, raw fragments, dynamic ORDER BY / table names.
- XSS — unescaped rendering, `dangerouslySetInnerHTML`, `v-html`, template auto-escaping disabled.
- Command / path injection — user input reaching a shell, a file path, or a filename.
- Unsafe parsing — deserialization of untrusted data, XML external entities, zip/archive extraction paths, unbounded uploads.
- SSRF — user-supplied URLs fetched server-side.
- Is validation server-side, or only in the UI?

## Data

- Secrets in code, fixtures, or committed env files.
- Sensitive values in logs — tokens, passwords, PII, full request bodies.
- Over-fetching in responses — internal IDs, other users' fields, stack traces.
- Personal data leaving its intended boundary (analytics, third-party APIs, error trackers).

## Web

- CSRF protection on state-changing form/cookie-authenticated endpoints.
- Cookie flags: `HttpOnly`, `Secure`, `SameSite`.
- CORS: is the allowed origin list actually restrictive, or `*` with credentials?
- Redirects: open-redirect via a user-supplied `next` parameter.
- Rate limiting on auth, upload, and expensive endpoints.

## Reporting

Cite the exact line and the attack path: who sends what, and what they get that they should not. A security finding without a path is a Needs Verification note, not a CRITICAL.
