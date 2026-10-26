# Reliability

## Error handling

- Are exceptions handled at a level that can actually do something about them?
- Is anything swallowed? An empty `catch {}` / bare `except: pass` needs a comment explaining why, or it is a finding.
- Are errors logged with context (ids, inputs, correlation id) rather than just the message?
- Are user-facing errors distinguishable from internal ones?
- Does a partial failure leave the system recoverable, or stuck in an intermediate state?

## Retries & idempotency

- Is the operation safe to run twice? Webhooks, queue consumers, and payment calls will be delivered twice eventually.
- Are retries bounded and backed off? Unbounded retry against a failing dependency is an amplification bug.
- Is there a dead-letter path, or do failures vanish?

## Background jobs

- What happens if the job is killed mid-run — on redeploy, on OOM?
- Is progress checkpointed for long jobs, or does a failure at 99% redo everything?
- Are job arguments serializable and version-tolerant across a deploy?
- Is there a timeout, so a hung job does not occupy a worker forever?

## Resource handling

- Files, connections, cursors, and locks released on every path including the error path.
- Concurrency limits on anything that fans out.

## Observability

- Will a production failure be visible? Log, metric, or alert.
- Are new failure modes distinguishable in logs from existing ones?
- Is logging at the right level — no per-row info logs, no silent errors at debug.
- No sensitive data in logs (see security checklist).
