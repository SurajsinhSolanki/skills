# Review-skill evaluation

These fixtures evaluate decisions, not wording or report length. They are maintenance tools: normal PR reviews must not load them. They require Python 3 and Git, use no external Python packages, and do not contact a network.

## Build and verify the fixtures

From the skill directory:

```bash
python3 evals/run.py
```

The command creates a fresh temporary suite, commits synthetic repositories, and checks observable conditions such as passing/failing consumers and distinct index/disk content. Alternatively, use `--output /tmp/my-review-evaluation`; the destination must not exist and must be outside this skill. It never modifies an existing repository. Keep the printed output path for grading or remove that generated directory when finished.

Generated files:

- `repos/case-NN/`: independent Git repositories with the relevant commits and local state.
- `inputs/case-NN.json`: synthetic supplied provider exports for provider cases; reviewer-visible, outside the reviewed repository, with no account/network access needed.
- `cases.json`: reviewer prompts and target metadata, with no expected verdicts.
- `expected.json`: evaluator-only verdicts, required behaviors, prohibited behaviors, and ground-truth evidence. Do not give this to the reviewing agent.

| Case | What it checks |
|---|---|
| 01 | Clean documentation change; no fabricated defects |
| 02 | Changed API breaks an unchanged caller |
| 03 | Known baseline gate failure does not block unrelated documentation |
| 04 | Introduced required-gate failure blocks |
| 05 | Staged review excludes unstaged and untracked defects |
| 06 | Working-tree review includes untracked callers and deduplicates failures |
| 07 | Lockfile-only regression is inspected |
| 08 | Rewritten branch fixes an earlier defect; base updates are separated |
| 09 | Google-style opt-in does not activate team policy |
| 10 | Missing external identity-contract evidence yields INCOMPLETE |
| 11 | Explicit user base overrides a different pinned default |
| 12 | Missing pinned base requires clarification, not silent fallback |
| 13 | Closer merge base does not prove intended integration target |
| 14 | Python stack pin does not suppress newly introduced SQL review |
| 15 | Same-SHA aliases across remotes are one comparison |
| 16 | Named head uses its own pin, not the unrelated checkout's pin |
| 17 | Matched provider target overrides a project pin |
| 18 | Old green CI does not verify the new head |
| 19 | Partial discussion export is disclosed, not treated as complete |
| 20 | Unavailable optional provider access preserves local review fallback |
| 21 | Unavailable fork head cannot be replaced with a same-named local branch |
| 22 | Requested detailed report preserves finding evidence and verification |
| 23 | Compact team-policy reporting preserves exceptions and human-approval limits |
| 24 | Vue 3.5 direct script-setup props destructuring is valid |
| 25 | Vue 3.4 default compilation still loses destructured primitive tracking |
| 26 | Pydantic v2 unhashable model defaults are independent |
| 27 | Ordinary Python function mutable default really shares state |
| 28 | Next 15 public fetch needs no blanket no-store requirement |
| 29 | Identity-omitting cache key causes a concrete cross-user result |
| 30 | Intentional TypeScript negative type test without Google opt-in |
| 31 | Opted-in TypeScript export style is non-blocking, not a runtime bug |
| 32 | Project-approved inline handler query is not a layering defect |

Cases 01, 02, and 10 also grade compact reporting: no padding, complete finding evidence, and explicit unresolved material gaps. Formatting is graded semantically, not by exact word counts or section titles.

Fixture checks passing means the scenarios were built correctly. It does **not** mean an agent using the skill passed the evaluation.

## Run a blind review

1. Record the skill revision or content hash, model, settings, and run date alongside the results.
2. Start a fresh review context for each case. Supply the skill location and only that case's `prompt` from `cases.json`. Do not include this catalog, the generator source, prior reviews, or expected answers. Do not expose the entire suite directory as task context; scope access to that case’s repository and its supplied input file (when present) where the harness supports it.
3. Save the raw review outside the fixture repository. Do not allow the reviewer to fix files or change its target. Run gates only as authorized in the prompt.
4. Have a separate evaluator compare the raw review with `expected.json`. Grade equivalent reasoning as correct; do not require exact prose. A minor severity difference is acceptable when impact, confidence, and blocking behavior are correct. Evaluate cited locations and causal reasoning, not just keywords.
5. For comparisons, use the same fixture inputs/model/settings and repeat across fresh contexts. Report variation, not just the best run. For mutable local cases, rebuild before reuse if a run altered their state.

Cases 24–32 explicitly prohibit web search, provider calls, and dependency installation. Source-grounded framework cases identify their validation method; building their manifests does not execute Vue, Next, Pydantic, or TypeScript. The reviewer receives local version/configuration evidence and bundled guidance.

The Git unit tests also verify branch/tag ambiguity, equivalent remote aliases, already-contained heads, unrelated histories, shallow clones, and multiple merge bases. These verify Git mechanics, not whether an agent follows the policy.

The builder's case numbers and directory layout are stable; commit SHAs and temporary paths vary. The re-review prompt legitimately includes the previous finding because it is user context for a second-round review.

## Grade and summarize

Create a JSON array with one entry per case. Criterion indices refer to zero-based positions in the case's `required` and `forbidden` arrays:

```json
[
  {
    "id": "case-01",
    "actual_verdict": "APPROVE",
    "satisfied_required": [0],
    "violated_forbidden": [],
    "false_positives": [],
    "evidence": "review-01.md: verdict approves; no invented findings"
  }
]
```

This is a one-case illustration; a real grade file must include all thirty-two cases. List every unsupported finding in `false_positives`, with a short explanation. Useful optional suggestions are not automatically false positives. A missing required behavior is left out of `satisfied_required`; the scorer counts it as missed. Supply report excerpts or citations in `evidence` for auditability.

```bash
python3 evals/score.py /tmp/my-review-evaluation/expected.json /tmp/grades.json
python3 -B -m unittest discover -s evals -p 'test_*.py'
```

The scorer reports verdict accuracy, missed required criteria, false-positive count, and per-case pass/fail. A case passes only with the correct verdict, all required behaviors, no prohibited behaviors, and no false positives. Missing/duplicate cases or invalid criterion indices are rejected. Exit status is 0 for an all-pass suite, 1 for scored failures, and 2 for invalid input.

The provider cases use synthetic exports as supplied evidence. They do not test real authentication, pagination APIs, connector schemas, or live CI services.

This is human-graded semantic evaluation, not an automated prose judge. Required-criterion counts include review behaviors as well as defects, so do not label that metric “bug recall.” The suite is a focused regression baseline, not comprehensive coverage of every language, security issue, or review mode. Mixed-stack budget handling, environment-only failures, generated contracts, structured-output host integration, and framework-runtime behavior outside installed tools are candidates for future expansion.

## Offline guide validation

Run `python3 -B -m unittest discover -s evals -p 'test_*.py'` for the full local checks. The offline-example tests execute code from bundled guides for Python defaults, JavaScript return/newline behavior, SQL NULL exclusions, quoted Bash arguments, and checked Rust indexing when installed. Pydantic v2 is tested only if already installed; a skip is not a pass for its runtime behavior. No dependency is downloaded. Vue/Next/compiler-specific cases remain source-grounded until exercised in an environment with their exact dependencies.

The [offline-guidance audit](offline-guidance-audit.md) records every original topic’s disposition, source provenance, corrections, and execution limitations. It is a maintenance artifact and is not loaded during ordinary reviews.
