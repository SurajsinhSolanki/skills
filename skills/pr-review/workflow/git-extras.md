# Git Extras — Situational Procedures

Load only on a trigger (see the end of `git-review.md`). Branch examples assume `$BASE` and `$HEAD` were resolved there. For local reviews, use that workflow’s target mapping/helpers for diffs and caller searches; history reads use the baseline commit, while changed content comes from the index or disk. The same safety rules apply: read-only commands only.

## History — recover the context the diff hides

A diff shows what changed, never why the old code was that way. Before flagging a removal or a rewrite:

```bash
git log --oneline -- <file>                       # this file's history
git log -L <start>,<end>:<file>                   # history of exactly these lines
git blame -L <start>,<end> $BASE -- <file>        # who wrote the old version, in which commit
git show <sha>                                    # that commit's message and full change
git log --oneline -S '<symbol>'                   # commits that added or removed a symbol
git log --oneline -G '<regex>'                    # commits whose diff matches a pattern
```

A guard clause deleted in this change was often added by a past bug fix. `git log -S` finds that commit in one call, which turns "why is this gone?" into a Confirmed regression finding with a citation.

Blast radius of a changed symbol:

```bash
git grep -n '<symbol>' -- '<glob>'                # current tree
git grep -n '<symbol>' $BASE -- '<glob>'          # as it was on the base
```

If the repo has a code-intelligence index available, prefer it — it resolves callers and dynamic dispatch that text search cannot.

## Deployability — can this ship safely

```bash
git diff --name-only $BASE...$HEAD -- '*migration*' '*migrate*' '*alembic*'
git diff $BASE...$HEAD -- '*example*env*' '*.env.example' '*config*sample*'
git diff --name-only $BASE...$HEAD -- '.github/**' '.gitlab-ci.yml' 'Jenkinsfile' 'Dockerfile*' '*.tf'
```

Mergeability is checked in `git-review.md` Step 3 whenever the branch is behind its base; it is not repeated here.

A new required setting added to a config example with no deployment note is a reliability finding: the service will start without it and fail later.

## Re-review — after the author pushes changes

A second round should review what changed since round one, not the whole branch again.

For committed reviews, record the base, merge-base, and head SHAs in the first report. Local index/disk content cannot be reconstructed from its baseline SHA: without a previously preserved snapshot, perform a fresh local review and reassess earlier findings. For committed snapshots:

```bash
git diff <old_head> <new_head> --        # differences between reviewed snapshots
git log --oneline <old_head>..<new_head>  # newly reachable commits, not necessarily new author work
```

If the branch was force-pushed (rebased, amended, squashed), `<old_head>` may no longer be reachable from the new head. It usually still exists locally:

```bash
git reflog <branch>                       # local record of where the branch pointed
git cat-file -t <old_head>                # does the object still exist?
```

After a rebase, amendment, or squash, the snapshot diff may include base updates. Record the old and new base/merge-base commits; compare their changes to separate integration updates from author edits. Where both series are available, `git range-diff <old_merge_base>..<old_head> <new_merge_base>..<new_head>` helps compare author commits. Always validate surviving and new findings against the current base-to-head PR diff and current target content. If attribution remains unclear, perform a full current review and disclose the limitation.

If the old sha is gone, fall back to a fresh `$BASE...$HEAD` review and say the incremental diff was unavailable.

Then, for each finding from round one:

- **Fixed** — confirm the fix is correct, and do not re-report it.
- **Partially fixed** — report what remains, referencing the original finding.
- **Not addressed** — restate it once, briefly. Do not escalate severity because it was ignored.
- **Rejected with a sound reason** — accept it and record the tradeoff. Repeating a rejected finding is noise.

New findings can arise from the fixes themselves — review the new code with the same bar, but do not re-litigate untouched code.
