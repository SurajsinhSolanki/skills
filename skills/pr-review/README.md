# pr-review

A review-only skill for pull requests, branch comparisons, staged changes, and working-tree diffs. It checks correctness, requirements, security, data integrity, reliability, and production readiness against the project's own conventions, then gives an evidence-backed assessment.

## Usage

```text
/pr-review <branch>
```

| Target | Reviewed content |
|---|---|
| No target | Working tree against HEAD, including untracked files separately |
| PR/MR URL or identifier | Matched provider target and relevant metadata when accessible; Git-only fallback remains available |
| One branch, tag, or commit | That ref against the resolved base |
| Explicit base and head | Three-dot diff from the merge base to head |
| Explicit staged-only request | Index against HEAD; excludes unstaged and untracked changes |

Supply the ticket or acceptance criteria when available. The skill can read descriptions, discussions, and CI through an available connector or already authenticated CLI/API. It remains usable with Git and supplied context when provider access is unavailable. Missing material evidence can produce **INCOMPLETE**, rather than an unsupported approval.

The review never applies fixes or changes the author's checkout. Gates run only under the [target-matching and failure-attribution rules](SKILL.md#running-the-projects-gates). Existing failures and environment failures are not automatically attributed to the change.

## Project configuration

Place an optional `.pr-review` file at the project root:

```text
base: main
stack: python, sql
standards: team
style: google
notes: multi-tenant — every query must be scoped by org_id
```

Every key is optional. `base` supplies a default below the user’s explicit target and a matched provider target; it must resolve and have a usable merge base. Local reviews ignore it. `stack` is advisory: changed-file evidence adds missing passes and excludes irrelevant pinned stacks. Missing or ambiguous pinned bases require clarification rather than a silent fallback. The [Git workflow](workflow/git-review.md) defines target resolution, snapshot handling, and configuration errors. It groups identical ref aliases, supports multiple remotes, and treats graph proximity as a hint rather than proof. Reports identify the base-selection source and cached-ref freshness.

Team policy and Google style are separate opt-ins. Either can be adopted through the pin, project documentation, or an explicit review request; an omitted or `none` pin value does not opt in by itself. Follow the workflow’s precedence rules when other project documentation or user instructions apply. A Google-style-only review never activates team requirements for Dockerfiles, versioning, tests, or human approval.

The [team policy](standards/team.md) contains one team's rules and can be replaced for another team. [Google style guides](styleguides/README.md) apply only to relevant changed languages. Project conventions take precedence over both; the [skill entry point](SKILL.md) defines the full precedence and loading rules.

## Reference map

`SKILL.md` is the entry point and owns the review process, evidence requirements, gate policy, and verdict mapping. References load only when relevant; default budgets permit justified exceptions and never limit investigation of repository code.

| Resource | Purpose |
|---|---|
| [Git workflow](workflow/git-review.md) | Target resolution, diffs, triage, local snapshot helpers, and safe Git use |
| [Provider context](workflow/provider-context.md) | Optional read-only metadata, requirements, discussion, and SHA-matched CI evidence |
| [Git extras](workflow/git-extras.md) | History, deployability, and incremental re-review |
| [Stack index](frameworks/README.md) | Evidence-to-framework routing, including SQL/infra and generic fallback |
| [Checklists](checklists/) | Security, data, API, reliability, requirements, architecture, tests, performance, and maintainability; triggers live in SKILL.md |
| [Review rules](rules/) | Evidence and borderline judgment references |
| [Team policy](standards/team.md) | Opted-in team rules and language policy tables |
| [Style index](styleguides/README.md) | Opted-in Google style selection and application |
| [Report template](templates/review-report.md) | Default report structure and conditional sections |
| [Inline comments](templates/inline-comment.md) | Per-finding comments with causal line anchors |

## Optional provider access

Provider integration is capability-based and does not require a particular service or installed CLI. Prefer an available read-only connector; use an existing authenticated CLI/API only when needed. No installation, login, permission expansion, posting, review submission, CI retries, or merging is part of this skill.

The [provider workflow](workflow/provider-context.md) defines repository/fork identity, target precedence, pagination, stale or synthetic-merge CI, and access-failure fallback. Reports distinguish live reads, user-supplied evidence, and local cached refs. A matching provider head is required before claiming its CI verifies the reviewed snapshot.

## Offline review guidance

All 18 framework passes and 21 style guides contain local applicability notes, explanations, examples, exceptions, and source-check dates. Their web links are optional attribution; reviewing code against these files requires no web search. Read project versions/configuration first and report unknown version-dependent behavior as unverified. Shared policy and explicitly composed technology passes are bundled local files. The guides cover their listed PR-review topics rather than reproducing entire vendor manuals.

## Assessments and output

The authoritative [verdict mapping](SKILL.md#severity) defines **APPROVE**, **APPROVE WITH COMMENTS**, **REQUEST CHANGES**, and **INCOMPLETE**. Impact and verification confidence are separate. Findings must explain what fails, why the change caused it, and the smallest useful fix.

- Default: compact Markdown review with findings, snapshot context, verification, and limitations; no empty sections or repeated summaries.
- `--detailed` (or “give me a full report”): expanded prose using the [detailed template](templates/detailed-report.md), with the same evidence and verdict rules.
- `--comment`: paste-ready comments, one issue per comment.
- `--findings`: the host's structured findings tool when available; otherwise a disclosed Markdown fallback.

Compactness never reduces investigation depth or removes distinct verified findings. Every mode includes the overall assessment and verification limits. Structured finding confidence is not the overall verdict.

For a re-review, supply the previous review and recorded commit SHAs. The [re-review procedure](workflow/git-extras.md#re-review--after-the-author-pushes-changes) compares snapshots, separates base updates after rebases, and records earlier findings as fixed, partially fixed, not addressed, or rejected with a sound reason. Prior local disk/index state cannot be reconstructed from a baseline commit alone.

## Maintenance

- Add a stack pass in `frameworks/` and link its trigger from the stack index.
- Add a checklist only for a distinct review concern; update its trigger in SKILL.md.
- Change verdict policy in SKILL.md, then check reference and template consistency.
- Keep team policy and style-guide adoption independent.

Use the [evaluation fixtures and grading guide](evals/README.md) to check missed defects, false positives, target handling, and verdict consistency:

```bash
python3 evals/run.py
python3 -B -m unittest discover -s evals -p 'test_*.py'
```

The builder verifies thirty-two isolated review scenarios, including five with offline provider exports outside the skill folder. The grading tool summarizes actual reviews against an evaluator-only rubric. Fixture verification alone is not an agent evaluation, and normal PR reviews do not load these maintenance resources.
