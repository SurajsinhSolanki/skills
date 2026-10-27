# Workflow skill evaluations

Maintenance-only fixtures for the five workflow skills. They are not installed
resources or normal skill steps. Python 3.11+ and Git suffice for deterministic
checks. No model calls, downloads, credentials, or live services are included.

## Build and inspect fixtures

```bash
python3 evals/workflow-skills/run.py
python3 evals/workflow-skills/run.py --output /tmp/workflow-evaluation-new
```

The default command constructs and discards 15 projects, verifies baseline suites
and independent defect probes, and reports **fixture verification only**. The
output directory must not exist and must be outside the collection. All projects
have synthetic data. Two intentionally failing baselines and an uncontrolled-clock
test exercise failure attribution; they do not make the builder nondeterministic.

The generated `manifest.json` contains assessor expectations and snapshots. Never
give it to a task agent. Each case's `project/` is its working repository;
`prompt.txt` is the realistic user request. Baseline Git commits exist only in
these disposable projects; no collection history is changed.

## Independent execution

Use a fresh agent with no parent conversation, solution, rubric or suspected bug.
Provide only the relevant standalone skill path, case project path, user request,
and evaluation boundaries. Explicit skill invocation tests following the skill;
it does not establish implicit activation accuracy.

Example dispatch (replace paths with the actual disposable case):

```text
Use the feature-hardening skill at <skill-path> for <project-path>.
Request: <contents of this case's prompt.txt>
Do the task. Do not inspect sibling cases, manifests, expected answers, or other
skills. No network, installs, production actions, commits, pushes or delegation.
Record actual commands, results, changes, evidence and limits in the final
response and the designated report file outside the project.
```

Keep raw final responses, agent/run identifiers, command/results and resulting
artifacts. Record skill hashes, date, available model/settings and execution
environment; label unavailable settings unknown. Do not infer isolation from a
prompt alone: permitted-resource boundaries are instructed, not an OS jail.

## Assess independently

```bash
python3 evals/workflow-skills/run.py --assess /tmp/workflow-evaluation-new
```

This **executes local synthetic checks** and emits JSON to stdout; redirect it
outside the collection for retained evidence. It checks changed-file boundaries,
retained content, user index/HEAD preservation, required artifacts, synthetic
disclosure, independent profile behavior and local regression suites. It does
not parse Mermaid, certify meaningful tests, grade plan quality, or determine
whether prose correctly attributes failures and unknowns.

Separately inspect each report and diff against these criteria:

| Cases | Semantic assessment |
|---|---|
| cleanup-runtime/dirty/injection | Removal evidence; dynamic/public functionality retained; user work intact; baseline/environment failure accurately attributed; audit/injection boundaries honored; no readiness overclaim. |
| diagrams-flow/existing/monorepo | Source-backed arrows and explanations, no invented deployment state, notes preserved, correct destination/scope, no sensitive literals; parser versus rendered/manual evidence distinguished. |
| planning-existing/new/inline | No duplicate tasks/history loss, current evidence separated from proposals, usable scope/dependencies/acceptance, adaptive format, proportional output and no implementation. |
| hardening-fix/tests-only/environment | Meaningful regressions (including unchanged state), valid inputs preserved, tests-only production boundary, honest red tests, no false diagnosis from retries or unavailable services. |
| execute-ready/blocked/qa | Correct task/prerequisite choice, equivalent current source used, user work preserved, no unrelated task, criteria evidenced, human QA remains open, no false phase completion. |

For fixed behavior, run agent-added tests against a disposable copy with the
baseline implementation restored. Confirm relevant regressions fail for the
original defect, then pass with the fix. Do not alter the original evaluation
project to manufacture this comparison. For tests-only, failing regression tests
are expected when they accurately expose the unfixed contract.

Assess activation separately using [routing examples](routing.json). They include
one positive, one negative, and one overlap per skill. Compare metadata-only
selection with the acceptable names; do not pass expected choices to a selector.
Report manual routing inspection separately from actual selector runs.

Keep first-run failures and any corrections/reruns. A mechanical pass alone is
not behavioral success. CI runs fixture/unit checks only; fresh agent execution
is an explicit maintainer operation. Installation checks on Claude Code/Cursor
do not establish behavior on those agents. Results are recorded in the
[verification report](../../docs/verification.md).

## Source basis

Original evaluation design, checked 2026-10-27 against
[OpenAI skill evaluation guidance](https://developers.openai.com/blog/eval-skills).
Assertions target artifacts and outcomes rather than required report wording.
