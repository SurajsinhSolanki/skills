---
name: pr-review
license: See LICENSE and NOTICE.md
description: Review pull requests, branch comparisons, staged changes, or working-tree diffs for correctness, requirements, security, reliability, and production readiness. Use for pre-merge reviews, re-reviews after fixes, or “is this safe to ship?” requests. Produces evidence-backed findings and an approval, request-changes, or incomplete assessment; supports inline comments and host-structured findings. Reviews only, without applying fixes.
---

# Production PR Review

Review against the project's requirements and conventions. Prioritize correctness, business behavior, security, data integrity, reliability, architecture, performance, maintainability, tests, and readability. Do not turn preference, equivalent style, unsupported hypotheticals, or unrelated refactoring into findings.

## Load only what the review needs

Start with this file; open references lazily when the target or diff provides a reason. Framework and style passes are bundled for offline use: read their local rules/examples and applicability notes; external links are optional attribution. Detect versions/config locally and disclose unsupported version-dependent behavior rather than relying on a web lookup. Small local changes may need no extra references. Default budgets are three stack files, four checklists, two rule files, and two workflow files; a typical review uses two to five references total. Concrete risks justify exceeding a budget: explain why in **Review basis**. These budgets never restrict reading repository code, callers, tests, or configuration.

| Reference | Trigger |
|---|---|
| [workflow/git-review.md](workflow/git-review.md) | Any branch review; local target commands, policy helpers, or other Git mechanics when needed |
| [workflow/provider-context.md](workflow/provider-context.md) | A PR/MR is identified or relevant provider metadata/CI can be read; optional and read-only |
| [workflow/git-extras.md](workflow/git-extras.md) | History needed for removed/rewritten logic, deployability changes, or a re-review |
| [frameworks/README.md](frameworks/README.md) | Select stack passes after triage; then load only matching files |
| [rules/production-thinking.md](rules/production-thinking.md) | HIGH-risk changes |
| [rules/evidence-based-review.md](rules/evidence-based-review.md) | A candidate finding cannot be fully verified |
| [rules/severity-guidelines.md](rules/severity-guidelines.md) | Borderline severity; the verdict mapping below remains authoritative |
| [rules/review-principles.md](rules/review-principles.md) | Unsure whether an observation merits a finding |

Team policy and Google style are independent opt-ins, never automatic. Load [standards/team.md](standards/team.md) and applicable `team-<lang>.md` files only when the project or user adopts team policy. Load [styleguides/README.md](styleguides/README.md) only when Google style is adopted; its default budget is three relevant guides with justified exceptions. Team policy is outside the reference budgets. Open the Python policy example only for a borderline style call. Neither opt-in activates the other.

## Review process

### Phase 0 — Resolve the target

Use Git for snapshot comparison, with optional read-only provider context. Accept a PR/MR URL or identifier, one ref, explicit base/head refs, a tag/commit, an explicit staged-only request, or no target (working tree). Resolve the repository and snapshot before reviewing. Multiple repositories need separate reviews and a cross-repository contract pass.

| Target | Compare | Read and search |
|---|---|---|
| Committed refs | `git diff "$BASE...$HEAD"` | Resolved head commit, not an unrelated checkout |
| Staged only | `git diff --cached HEAD` | Index (`git show :path`, `git grep --cached`); exclude unstaged/untracked content |
| Working tree | `git diff HEAD`, plus untracked files | Disk, including tracked and non-ignored untracked content |

Read any root `.pr-review` pin from that snapshot. Optional keys are `base`, `stack`, `standards`, `style`, and `notes`. The base precedence is **explicit user input > matched provider target > valid pin > applicable project documentation > evidence-backed inference**; pins never bypass ref/history validation. Local targets ignore pinned bases. Treat `stack` as advisory: verify it against changed files and add newly evidenced stacks. Malformed or stale pins cannot silently alter the target or suppress coverage. The [Git workflow](workflow/git-review.md) defines validation and ambiguity handling; proximity and upstream tracking alone do not identify a merge target.

Apply the same snapshot to verification, callers, secrets, and policy checks. Record target kind and baseline/head/merge-base SHAs as applicable; re-read changed local content or disclose that it became unverified. Follow the Git workflow for unborn HEAD or conflicted indexes.

Triage file names, status, size, directory distribution, and branch commit intent before reading source. Scan added lines for secrets on every review; working-tree reviews also scan untracked text files in full. Verify hits and never reproduce a suspected real secret in the report. Lockfiles, snapshots, and generated output may be filtered from the first broad read but require targeted inspection when relevant; disclose omissions.

### Phase 1 — Establish intent and project rules

Read available descriptions, tickets, and acceptance criteria; identify users and affected behavior. Git does not contain provider descriptions, discussions, or CI results. Use the optional provider workflow to retrieve relevant context when available; otherwise use supplied material and disclose missing evidence. Ask only for material gaps that available sources cannot resolve. Never infer requirements from the implementation or treat stale CI as validation of the current snapshot.

Discover tooling from manifests, config, CI, and surrounding code. Read relevant project rules at the root and ancestor directories of changed files (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, PR templates, ADRs). Use existing project commands and solutions; do not prescribe new tools when existing ones suffice. Where no convention exists, disclose a mainstream-language fallback.

Precedence: **user instructions > project config/docs/patterns > opted-in team policy > opted-in Google style > generic references**. Cite documented rules supporting findings. Note conflicting external standards once rather than blaming the author. Avoid redundant formatter/style comments; configured CI alone does not establish that a correctness check passed.

### Phase 2 — Trace behavior and callers

Follow important changes through inputs, validation, authentication/authorization, business logic, storage, external services, responses, and side effects. Check happy and failure paths.

For changed public contracts, deletions, and renames, trace callers in the selected snapshot, including aliases, injection, routes, and events. Prefer available code intelligence; otherwise search qualified uses rather than ambiguous bare names. Check arguments, return shapes, errors, and changed meaning. A single visible internal caller needs no separate search.

A changed contract can break an unchanged caller. Prove causality, anchor feedback to the changed contract, and cite the caller. Recover history before flagging removed/rewritten logic when its purpose is unclear; use the Git extras reference.

Always assess whether tests exercise changed behavior, would fail if that behavior regressed, and cover meaningful failure paths. Report specific missing scenarios, not coverage percentages or demands for trivial tests.

### Phase 3 — Classify risk

LOW: documentation or isolated UI changes. MEDIUM: features, business logic, or API changes. HIGH: authentication, permissions, payments, migrations, jobs, distributed state, or data processing. Depth follows actual risk; these examples are starting points, not automatic verdicts.

### Phase 4 — Select checklists

Load only checklists whose triggers apply, ranked by risk. Do not manufacture a trigger to fill a budget.

| File | Load when the diff contains |
|---|---|
| [checklists/security.md](checklists/security.md) | auth, permissions, sessions, tokens, middleware, user input reaching a query/command/path, anything multi-tenant |
| [checklists/database.md](checklists/database.md) | a migration, a schema/model change, a new or changed query, a transaction |
| [checklists/api.md](checklists/api.md) | a route, handler, request/response schema, or an outbound call to another service |
| [checklists/reliability.md](checklists/reliability.md) | a background job, queue consumer, webhook, retry, or new error handling |
| [checklists/requirements.md](checklists/requirements.md) | requirements are available (supplied or retrieved) and the change implements business rules |
| [checklists/architecture.md](checklists/architecture.md) | new layers/modules, moved responsibility, or logic that looks duplicated |
| [checklists/testing.md](checklists/testing.md) | source changed and you need to judge whether the test coverage is adequate |
| [checklists/performance.md](checklists/performance.md) | a loop over a large collection, a new query in a hot path, or a large payload |
| [checklists/maintainability.md](checklists/maintainability.md) | a rename, a deletion, or code you suspect is dead |

### Phase 5 — Apply stack and opted-in passes

Use the stack index to select references from changed paths and manifests, most specific first. Do not load unrelated monorepo stacks. SQL and deployment configuration warrant their cross-cutting passes even when this exceeds the default budget. Apply team and Google-style passes only under their respective opt-ins and report them independently.

### Running the project's gates

Lint, type-check, and test results are strong evidence. Use the project's actual commands and existing user authorization; never check out or modify the author's tree to run them.

- For a committed target, run gates only when its resolved commit is checked out and the worktree/index are clean, including untracked inputs that could affect execution. Dirty-tree results do not verify a committed head.
- For a working-tree target, gates exercise the current disk content; record that snapshot and any changes during the run. For a staged-only target, run only if the disk matches the index and no untracked inputs affect execution. Otherwise mark gates not run for that target.
- Classify each failure: **introduced by this change**, **pre-existing**, **environment/setup**, or **unresolved attribution**. An attributable failure of a required project gate is an introduced MUST violation and blocks. Other failures do not automatically block; explain the evidence and limitations. Compare available baseline results or inspect the failure path without changing the author's checkout.
- Record commands, target, outcomes, and unrun checks in **Not verified**. Material unresolved failures that prevent a decision yield **INCOMPLETE** under the verdict rules below.

### Phase 6 — Verify every finding before reporting

1. Re-read the cited lines in the selected snapshot.
2. State a concrete failure scenario: inputs/state, observed behavior, and consequence. Without one, downgrade to a useful suggestion or drop it.
3. Search for existing protections in middleware, decorators, base classes, dependency injection, validators, or database constraints before claiming they are missing.
4. Establish that this change caused or worsened the failure, not merely that the failing line changed. Unchanged pre-existing problems are separate and never block.
5. Deduplicate by root cause; retain supporting locations. Keep, downgrade, or drop each candidate.

Every finding includes **location, observed problem, production impact, recommended fix, and confidence**. Never invent files, behavior, or protection gaps.

- **Confirmed:** code or execution establishes the concrete failure.
- **Likely:** strong evidence depends on an unread configuration, caller, or runtime condition; state that dependency.
- **Needs Verification:** insufficient evidence; ask a question rather than reporting a finding.

## Severity

| Label | Means |
|---|---|
| `[CRITICAL]` | security vulnerability, data loss or corruption, outage or crash on a normal path, cross-user or cross-tenant access |
| `[HIGH]` | wrong business behavior, major regression, unhandled failure on a common path, non-idempotent retry, unsafe migration |
| `[MEDIUM]` | real but recoverable edge case, limited-impact bug, a maintainability cost the next change will pay |
| `[LOW]` | minor improvement with practical value |
| `[SUGGESTION]` | optional; never presented as a bug, never gates the merge |

**Verdict mapping (authoritative):** Apply these rules in order; other documents defer here.

1. **REQUEST CHANGES** — at least one Confirmed CRITICAL/HIGH defect or Confirmed introduced violation of an applicable MUST rule (including an attributable required-gate failure). Known blockers remain blockers even if other areas are unverified.
2. **INCOMPLETE** — no confirmed blocker, but material unresolved evidence, gate attribution, or coverage gaps prevent a responsible decision. Name the missing evidence and what would resolve it.
3. **APPROVE WITH COMMENTS** — sufficient verification, no blockers, and Confirmed MEDIUM/LOW findings.
4. **APPROVE** — sufficient verification, no confirmed defects; suggestions alone do not prevent approval.

**Confidence and blocking.** Severity describes impact; confidence describes evidence. Likely findings remain explicitly conditional and cannot independently establish a confirmed blocker. If their unresolved condition materially prevents approval, use INCOMPLETE; otherwise disclose it without changing the verdict. Needs Verification items are questions, not findings. Missing nonessential context does not automatically make a review incomplete.

Severity is production impact, not how much the code annoys you. Borderline cases: [rules/severity-guidelines.md](rules/severity-guidelines.md).

## Output

Default to a compact report using the [review report template](templates/review-report.md). Use `--detailed` or an explicit full-report request for its linked detailed format. Both retain the verdict, resolved target, risk, verification limits, convention sources, and references/checks applied (with budget exceptions). Distinguish no confirmed blockers from sufficient evidence to approve. State when required human approval remains outstanding.

Verbosity affects prose only; inline comments and structured findings retain their own evidence fields and schemas. A detailed request does not authorize posting.

- **`--comment`:** use [inline-comment.md](templates/inline-comment.md), one surviving finding per changed causal location, with supporting caller citations where needed.
- **`--findings`:** use the host's structured tool when available. Finding confidence maps Confirmed to `CONFIRMED` and Likely to `PLAUSIBLE`; Needs Verification stays a text question. Put the checklist/stack in `category` and the concrete scenario in `failure_scenario` when supported by the host schema.
- Every mode includes the overall assessment and verification limits. A finding's confidence is not the review verdict; emit the assessment separately when the host has no compatible field. Never convert INCOMPLETE to approval. If a structured tool is unavailable, disclose that and use the report format.

This skill reviews only. Do not apply fixes or change the author's worktree, index, or refs; follow the Git workflow's safety rules. Fixes require a separate explicit request. Evaluation resources under `evals/` are maintenance tools and do not load during ordinary reviews.
