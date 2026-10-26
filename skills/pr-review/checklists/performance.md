# Performance

Report only meaningful issues — ones you can tie to real volume or real latency.

## Check

- Expensive queries: missing index on a filtered column, full scans, joins that fan out.
- N+1 patterns in loops, serializers, and render paths.
- Unnecessary loops over large collections, or repeated work inside a loop that could be hoisted.
- Excessive memory: loading a whole file or table into memory instead of streaming/chunking.
- Blocking operations on the request path — sync I/O in an async handler, CPU-heavy work that belongs in a job.
- Excessive API calls — a per-item HTTP call where a batch endpoint exists.
- Payload size: sending fields the client discards; missing compression on large responses.
- Client-side: work in a render path that runs every frame; unbounded lists without virtualization; images without dimensions.

## Do not report

- Theoretical optimization with no measured or reasoned volume behind it.
- Micro-improvements (a map vs a loop, a string concat).
- Missing caching where correctness has not been established first.
- Memoization added defensively without an observed cost.

## How to report

Name the scale that makes it matter: "this runs once per row and the table has ~200k rows" or "this call is on the login path". Without a scale statement it is a suggestion, not a finding.
