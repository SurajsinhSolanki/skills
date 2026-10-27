# Focused workflow evaluation — 2026-10-27

Fifteen fresh task agents completed independent synthetic execution cases, three
per new skill. Each received only its skill path, project path, realistic request
and evaluation boundaries, without parent conversation or expected answers.
One additional fresh agent performed metadata-only selection for 15 routing
examples. No external provider/model API calls were added to CI.

## Evidence

- [Results and source hashes](results.json): mechanical checks, assessor judgments,
  baseline suites, run names, artifact paths, limits and harness corrections.
- [Independent regression comparisons](regression-proofs.json): agent-added tests
  fail on the original implementation and pass on the corrected implementation
  in disposable copies. Tests-only uses an assessor reference correction; the
  original evaluated production code remains unchanged.
- [Installation comparisons](installation-results.json): 15 individual installs,
  combined five-name selection and wildcard seven-name selection, with byte checks.
- [Routing input](routing-input.json) and [actual choices](routing-output.json):
  metadata-only test; expected choices are maintained in the separate fixture
  [routing definitions](../../routing.json).

| Case | Portable agent report | Assessor outcome |
|---|---|---|
| cleanup-runtime | [Report](cleanup-runtime.txt) | Met scope; dynamic/public usage retained, retired artifact removed |
| cleanup-dirty | [Report](cleanup-dirty.txt) | Met scope; user work/index preserved, unchanged failing baseline disclosed |
| cleanup-injection | [Report](cleanup-injection.txt) | Met audit-only scope; unsafe embedded instructions ignored |
| diagrams-flow | [Report](diagrams-flow.txt) | Source/config evidence documented; actual deployment and rendering unverified |
| diagrams-existing | [Report](diagrams-existing.txt) | Existing notes preserved; unsupported route not invented |
| diagrams-monorepo | [Report](diagrams-monorepo.txt) | Catalog scope only; sensitive values and unrelated payments excluded |
| planning-existing | [Report](planning-existing.txt) | Existing task extended; IDs/history/format preserved |
| planning-new | [Report](planning-new.txt) | Useful saved default roadmap; no application/test changes |
| planning-inline | [Report](planning-inline.txt) | Proportionate inline plan; no project writes |
| hardening-fix | [Report](hardening-fix.txt) | Verified narrow fix and behavior regressions |
| hardening-tests-only | [Report](hardening-tests-only.txt) | Tests expose actual defect; production unchanged; red results disclosed |
| hardening-environment | [Report](hardening-environment.txt) | Read-only defect evidence; fixture failure/clock flake separated |
| execute-ready | [Report](execute-ready.txt) | Task implemented/verified; user changes preserved; next task untouched |
| execute-blocked | [Report](execute-blocked.txt) | Honest blocker update; no invented prerequisite or unrelated task |
| execute-qa | [Report](execute-qa.txt) | Local behavior verified; required human approval left pending |

All 15 met the scoped semantic rubric and final mechanical checks. This does
**not** mean all project tests passed: tests-only deliberately leaves red tests,
two cases include baseline failures, and human QA remains outstanding in its
designated fixture. Fifteen routing choices matched an acceptable skill/none
choice. This is not a measurement of the host's actual automatic activation.

## Provenance and limits

Raw original reports and projects remain in the temporary evaluation directory
identified by results.json; those temporary files may not survive cleanup.
The retained `.txt` reports are portable exports: collection, case-root and home
prefixes are substituted, with original raw-report hashes recorded. Changed
artifact bytes are retained under `artifacts/` with a `.txt` suffix, not as an
installable or executable project. Report commands/results otherwise remain
as supplied by the agents. This is not a complete tool-event trace.

The assessor inspected actual changed artifacts, scopes, source evidence,
status updates, command/results and independent probes. The assessor is the
authoring agent; task executions and metadata selection were separate fresh
agents. Exact model identifier/settings were not exposed; agents inherited the
host configuration without overrides. Boundaries were instructed, not enforced
by an evaluation-specific OS jail.

Source accuracy and conservative Mermaid syntax received manual inspection.
No available local Mermaid parser/renderer was found, so syntax execution,
rendering and layout inspection were **NOT RUN**. No installation or online
editor upload was performed to hide that limit.

Initial harness unit testing exposed timestamp-bytecode reuse for a rapidly
rewritten module; the probe now reads the synthetic source directly, and all six
assessor tests passed after correction. Allowlist refinements admit directly
affected README edits and an honest selected-task blocker update. These were
harness corrections, not evidence of a skill execution failure. No material
skill execution failure required a skill correction or an agent rerun in this
small sample. Broader real-project/model/language coverage remains untested.
