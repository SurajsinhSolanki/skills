# Requirements & Business Logic

## Verify

- Does the implementation actually solve the ticket, or only the part that was easy?
- Is every acceptance criterion implemented? List them and mark each.
- Are the business rules correct — thresholds, rounding, precedence, units, timezones?
- Are edge workflows handled, not just the demo path?

## Look for

- **Missing states** — what happens between "started" and "done"? Cancelled, expired, partially complete, retried.
- **Incorrect assumptions** — "there is always exactly one", "the list is never empty", "the user always has a tenant".
- **Wrong calculations** — off-by-one, percentage vs fraction, inclusive vs exclusive ranges, float money.
- **Incomplete workflows** — the record is created but never cleaned up; the flag is set but nothing reads it.
- **Silent scope creep** — behavior changed that the ticket never asked for.
- **Unstated defaults** — a new required field defaulted to a value nobody agreed on.

## Questions worth asking the author

- What happens to records created before this change?
- Which acceptance criterion covers <behavior you cannot find>?
- Is this rule the same for every tenant, region, and customer tier?
