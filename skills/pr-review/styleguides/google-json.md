# Google JSON Style Guide — Review Checklist

Source: [Google JSON Style Guide](https://google.github.io/styleguide/jsoncguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Load when the diff defines or changes a JSON **contract** — API request/response shapes, schemas, or fixtures standing in for them — not for incidental config files.

Contents: [Scope and offline use](#scope-and-offline-use) · [To flag](#to-flag) · [Envelope (only if the API uses it)](#envelope-only-if-the-api-uses-it) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google JSON contract policy (revision 0.9 snapshot), not a universal schema or incidental-config policy. Respect existing API envelopes and consumer compatibility.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## To flag
- Property names not `camelCase`, or using reserved JavaScript words.
- Arrays with singular names, or scalar properties with plural names.
- Google-style new enum contracts prefer descriptive strings. Neither strings nor numbers automatically makes an unknown future value safe; verify consumer handling before claiming a compatibility bug.
- Dates not RFC 3339 (`2007-11-06T16:34:41.000Z`); durations not ISO 8601. **(bug risk)**
- Arbitrary nesting that carries no meaning — flatten it.
- Comments in JSON.
- `null` or empty properties with no semantic meaning — consider omitting them.

**Application and exceptions:** Use double-quoted keys/strings and valid JSON without comments/trailing commas. camelCase is policy; object/map data keys may be externally defined. Null versus omission is a contract decision, not automatic cleanup.

## Envelope (only if the API uses it)
Google's guide defines reserved top-level properties (`apiVersion`, `data`, `error` with `code`/`message`/`errors[]`) and paging fields (`itemsPerPage`, `startIndex`, `nextLink`, and so on). Check them only in an API that has adopted that envelope; in any other API, follow its existing response shape.

**Application and exceptions:** Reserved envelope fields apply only when that envelope is adopted. Changing paging/error shapes requires checking existing consumers; adding a wrapper solely to match the guide is wrong.

## Example and review decision

```json
{"items":[{"userId":"u1","state":"ready"}],"nextLink":null}
```

This is one possible contract, not a required envelope. Explain allowed enum values, unknown-value handling, date/time units, and null/omission in a bundled schema or API contract. JSON has no imports or source-code comments.
