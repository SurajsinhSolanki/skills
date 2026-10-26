# Maintainability

Only raise these when they will cost the next change. Style preference is not a finding.

## Check

- **Naming** — does the name describe what it does now? A misleading name is worse than a vague one.
- **Comments** — short and meaningful. Missing "why" on a non-obvious decision is a finding; a wall of narration is also a finding.
- **Dead code** — unreachable branches, unused exports, commented-out blocks, feature flags that no longer flip.
- **Magic values** — unexplained numbers and strings, especially duplicated ones.
- **Function size and nesting** — deep nesting that hides the happy path; early returns usually fix it.
- **Duplication** — the same rule in two places. Duplicated *shape* is fine; duplicated *decision* is not.
- **Typing** — unjustified `any` / `Any`, silenced type errors, casts that hide a real mismatch.
- **Error-prone signatures** — three consecutive booleans, positional args that are easy to swap.
- **Docs** — does this change invalidate a README, an env example, or an API doc that lives in the repo?
- **Consistency** — does the change match the conventions of the files around it?

## Rename completeness

If the PR renames something, verify the rename landed everywhere: imports, tests, fixtures, stories, styles, docs, migrations, and string references.
