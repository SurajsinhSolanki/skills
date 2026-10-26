# Team Standards — Review Policy

One team's rules, packaged as an **opt-in** review policy. They apply only when a project opts in — `standards: team` in its `.pr-review` file, its own docs adopting these guidelines, or the user asking for them in the review. Without an opt-in, none of this file applies: the skill reviews against the project's own conventions only.

Language-specific rules live in sibling files (`team-python.md`) and load only when the project opted in and that language is in the diff.

This file turns the team guidelines into things a reviewer can verify from git. Provider-only rules (approvals, releases, project boards) need evidence from the [optional provider workflow](../workflow/provider-context.md) or supplied context; they cannot be verified from Git alone and must never be guessed.

To adopt this skill for another team, replace the files in `standards/`. Nothing else in the skill refers to these specific rules.

**Style:** if the team's projects follow Google style, opt in to that separately with `style: google`. Where both are on, team rules here override Google where they differ — for example, Python lines may run to 120 columns instead of Google's 80.

Use the target-aware helpers in [../workflow/git-review.md](../workflow/git-review.md#step-7--reviewing-local-targets) for file, diff, and search checks below. Also inspect untracked files for working-tree reviews. Commit-history checks apply only to committed branch reviews; mark them n/a for local targets. Follow the workflow's special handling for unborn HEAD/conflicted index.

## How to run this pass

Work through this file, plus the language file for each language in the diff (e.g. [team-python.md](team-python.md)). They hold the git commands for each check: branch name, commit messages, version bump, Dockerfile and hadolint, Python style, docstrings, unit and end-to-end tests.

- **MUST** rules (tests required, Dockerfile present, correct version bump) are `[HIGH]` and block the merge.
- **SHOULD** rules (style, naming, commit hygiene) are `[LOW]`, grouped one finding per rule, and never block. Skip any rule a configured linter already enforces in CI.
- Rules that live on the hosting provider (peer approval, releases, project board) are verified only with relevant provider/supplied evidence; otherwise mark *not verified from git-only context*.

Team findings go through Phase 6 like any other, and each one names the rule it comes from. MUST violations block only when Confirmed and introduced by the change; uncertainty follows the authoritative verdict rules in SKILL.md.

## Precedence

When rules disagree, apply them in this order:

1. The user's explicit instruction for this review.
2. The repo's own enforced config and documented rules — linter/formatter config, `CLAUDE.md`, `CONTRIBUTING.md`, CI.
3. These team standards.
4. The Google style guides (`styleguides/`).
5. The generic checklists and framework files.

A conflict between (2) and (3) — for example the repo's linter sets a different line length than the team rule — is **not the author's fault**. Follow the repo, and record the discrepancy once in the team-policy results as a note for the team, not as a finding.

## MUST vs SHOULD

| Kind | Severity | Effect |
|---|---|---|
| **MUST** — required by the team | `[HIGH]` | **REQUEST CHANGES** (see the verdict mapping in `SKILL.md`) |
| **SHOULD** — style and hygiene | `[LOW]` | never blocks; **one grouped finding per rule**, listing up to five locations and "and N more" |
| **Encouraged** | `[SUGGESTION]` | optional |

Every team finding names the rule it comes from, e.g. *"Team rule: unit tests required for new behavior."*

Style rules that a configured linter or formatter already enforces in CI are **not reported per line** — the tool will catch them, and repeating them is noise. Report only what no tool enforces.

## Git workflow (GitHub Flow)

### Branch name — SHOULD

Descriptive of the change: `add-user-authentication`, not `fix1`, `test`, `temp`, `wip`, `my-branch`, a bare ticket number, or a person's name. Type prefixes (`feature/`, `bugfix/`) are fine — the rule is about being descriptive.

```bash
git branch --show-current          # or the head ref you were given
```

### Commits — SHOULD

Frequent, small, and with messages that say **what changed and why**.

```bash
git log --format='%h %s' --no-merges $BASE..$HEAD
git log --shortstat --format='%h' --no-merges $BASE..$HEAD | grep -v '^$' | paste - -
```

Flag, as one grouped `[LOW]` finding:

- Subjects that say nothing about the change: `fix`, `update`, `changes`, `wip`, `misc`, `update test file`, `change in X`. A conventional-commit prefix alone (`feat: change in sso`) does not make a message clear.
- Duplicate subjects across commits.
- One commit mixing unrelated concerns, or a very large commit (roughly 500+ changed lines) that could have been split. A large but cohesive commit is not automatically wrong.

If the team squash-merges, the PR title becomes the commit message — weigh commit granularity less, and the PR title more.

### Pull request — SHOULD / process

- **Title**: descriptive and clear. The title is not in git; check supplied or retrieved metadata, otherwise mark *not verified*.
- **Target**: GitHub Flow merges into `main`. If the resolved base is a different branch, check whether the repo documents that flow (CI triggers, `CONTRIBUTING.md`). If it does, note the discrepancy once in the policy results and do not flag the author.
- **Description**: should summarize the change, the reason, and how it was tested. Check supplied or retrieved metadata.

### Review approval — process

Every change needs approval from **another team member** before merge. Record existing approval evidence only when supplied or retrieved for this PR, noting dismissed or stale approvals and unknown applicability. **This automated review does not satisfy that requirement.** Say so in the *Final Assessment*. Never recommend merging on the strength of this review alone.

### Deployment — out of scope

"Deploy soon after merge" happens after the review. Out of scope.

## Versioning — MUST when a version changes

Semantic Versioning `MAJOR.MINOR.PATCH`: MAJOR for incompatible API changes, MINOR for backwards-compatible features, PATCH for backwards-compatible fixes.

```bash
review_diff -- pyproject.toml setup.cfg setup.py package.json VERSION \
  '**/__init__.py' '**/_version.py' | grep -E '^[-+].*(version|__version__)'
```

- **No version change**: fine — releases may be cut separately. But if the change is **breaking** (removed or renamed public function, endpoint, CLI flag, config key, or changed response shape), ask in *Questions for the Author* whether the next release is planned as MAJOR.
- **Bump smaller than the change requires** (a breaking change shipped as MINOR or PATCH): `[HIGH]`, MUST — consumers break on an upgrade they were told is safe.
- **Bump larger than needed** (MAJOR for a fix): `[LOW]`.
- **Release notes / releases**: use relevant supplied/provider evidence when available; otherwise not verified from Git alone.

## Docker

### Dockerfile present — MUST

Every repository must contain a Dockerfile.

```bash
review_files | grep -i '^Dockerfile'      # candidate paths; check disk existence for working reviews
review_diff --name-status | grep -i 'Dockerfile' # changed or deleted here?
```

- The change **deletes** the Dockerfile: `[HIGH]`, MUST.
- The repo had no Dockerfile before this change: *Pre-existing*, not the author's fault. Note it in the policy results.

### hadolint — when a Dockerfile changed

`hadolint` reads from stdin, so it can lint the selected snapshot without checking anything out. Use that snapshot’s hadolint configuration as well; do not silently apply a different checkout’s config. If matching configuration cannot be supplied without modifying the checkout, mark the check not run for this target. With matching inputs, that makes it read-only and allowed without asking:

```bash
command -v hadolint && review_read Dockerfile | hadolint -
```

- Errors on lines this change added: `[MEDIUM]`. Warnings: `[LOW]`, grouped. If hadolint is an applicable required project gate and the change caused its failure, apply the required-gate MUST rule in SKILL.md instead. Environment or pre-existing failures do not establish a blocker.
- Not installed: say *hadolint not run* in the policy results and review by hand against the practices below. Do not download or pull an image to run it without asking.

Practices to check by hand: pinned base image versions, minimal layers, cache-friendly instruction order, small images (multi-stage), non-root user, no secrets baked in. Security-relevant problems (secrets, root plus host mounts) take their severity from `frameworks/infra.md`, not from this file.

## Provider-only evidence

Use supplied or retrieved evidence for the following process facts when relevant to opted-in policy; otherwise mark *not verified*. Do not expand a code review into a project-management audit:

- approval by another team member
- GitHub Releases being up to date
- the repo being linked to the team's GitHub Project, and the issue's Kanban column and assignee
- deployment after merge

## Team Standards table (detailed mode)

When this file is opted in, evaluate the applicable rules below. Compact reports summarize coverage, rule-specific failures, and unverified items; detailed reports include this table. Rows that do not apply are `n/a`. Add language-specific rows only for policies loaded.

| Area | Rule | Status | Notes |
|---|---|---|---|
| Branch name | descriptive | pass / fail | |
| Commits | small, clear messages | pass / fail | |
| PR title | descriptive | pass / fail / not verified | |
| Target branch | PR into `main` | pass / note | repo-documented flow if different |
| Versioning | SemVer bump matches change | pass / fail / n/a | |
| Dockerfile | present | pass / fail / pre-existing gap | |
| hadolint | clean | pass / N issues / not run | |
| Peer approval | another team member | verified existing approval / not verified | This automated review never supplies human approval. |
| Project board / releases | linked, current | verified / not verified / n/a | Cite relevant supplied/provider evidence. |

Confirmed introduced MUST violations also appear as findings with full evidence in either format. A policy summary or table does not replace the finding.
