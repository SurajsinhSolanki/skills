# Saved roadmap maintenance

## Adapt before creating

Use the supplied plan path or the project's existing roadmap. A single-file
roadmap, issue-oriented task list, or another naming convention is valid. Do not
impose `docs/plan/` or move files merely to match this example. Never create saved
files for an inline-only planning request.

Before updating, identify matching requirements and tasks, current status,
completed history, dependencies and relevant user edits. A matching task may
already cover the request; report it rather than generating a duplicate. Extend
an unfinished task when the same acceptance boundary naturally applies. If new
work follows a completed task, preserve completion history and add a follow-up.

## Default for a new persistent roadmap

When persistence is requested and no project convention exists:

```text
docs/plan/
  README.md
  phase-1.md
```

Add further phases only for meaningful stages or prerequisites. The index needs
a short objective, phase/task links, execution order/dependencies, progress and
material open decisions. Add requirement-to-task mapping when multiple
requirements make traceability useful. Do not create separate empty tables.

A phase needs its objective, boundaries, prerequisites, tasks, and applicable
completion criteria. Use stable IDs such as `P1-T001`; allocate an unused ID and
never renumber or reuse old IDs to close gaps. A moved task can keep its ID and
record its new phase. Preserve cancelled or superseded history with a brief reason.

## Minimal task template

Adapt headings to the project. Omit irrelevant fields; proposed file names are
proposals until implementation exists.

```markdown
### P1-T001 — Reject an empty display name
Status: Ready
Depends on: None

Current evidence: `src/profile.py::update_name` accepts an empty string;
the documented profile contract requires a nonblank name.

Outcome: Reject empty or whitespace-only names without changing the old name.
Approach: Extend the existing validator and its public-behavior tests.
Scope: Profile name validation; no new profile fields or password changes.

Acceptance:
- Valid names keep the documented normalization behavior.
- Empty/whitespace names produce the existing validation error type.
- Rejection leaves the stored name unchanged.

Verification: Run the focused validator tests and existing profile tests.
```

The example is illustrative, not evidence of any actual repository behavior.
Complex tasks can add UI/API/data flow, proposed contracts, failure handling,
security, migration/rollout/recovery, risks and observability. Do not require all
of them for a small task. Distinguish acceptance (observable outcome) from process
checks such as documentation review or obtaining an approval.

## Status and dependencies

- Preserve existing vocabulary and define its meaning if unclear. For a new plan,
  use `Not started`, `Ready`, `In progress`, `Blocked`, and `Done`; add `Discovery`,
  `In review`, `QA`, `Deferred`, or `Cancelled` only when useful.
- `Ready` means scope, essential decisions and prerequisites permit implementation.
  A dependency cycle, missing permission, or unresolved essential contract blocks
  the dependent task; do not hide it under optimistic status.
- `Done` requires evidence for acceptance and the applicable definition of done.
  Code inspection alone cannot satisfy a required runtime test or human QA gate.
- A phase becomes done only after all required tasks and phase criteria are met.
  Do not infer whole-phase completion from a newly finished task.
- Explain a changed approach and update affected links/dependencies. Do not erase
  why a prior approach was rejected or mark old tests as having run again.

## Priorities and discovery

Use the project's priority vocabulary. Establish urgency from impact, exposure,
business requirements or blocked work; do not manufacture deadlines or estimates.
If unknown, state that priority/estimate needs a decision, or omit the field.

A discovery task is appropriate when a material unknown survives reasonable local
inspection. Define a specific question, bounded investigation, options and
decision criteria, responsible decision-maker when known, and an acceptance
artifact. Do not promise the eventual design before that evidence exists.

## Source and applicability

Original adaptation of the maintainer's planning prompt under MIT, checked
**2026-10-27**. This is a format fallback, not a framework or standards mandate.
