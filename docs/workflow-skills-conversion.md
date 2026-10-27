# Workflow prompt conversion coverage

Converted **2026-10-27** with maintainer-confirmed MIT distribution. The five
source prompts remain external and unchanged; copies containing personal paths
are not distributed. The two existing skill packages retain their original bytes.
See [verification](verification.md) for executed checks and limitations.

## Resulting packages

| Source | Standalone entry | Conditional local guidance |
|---|---|---|
| `clean_prompt.md` | [production-cleanup](../skills/production-cleanup/SKILL.md) | [Audit categories and evidence](../skills/production-cleanup/references/audit-inventory.md) |
| `docs_prompt.md` | [codebase-diagrams](../skills/codebase-diagrams/SKILL.md) | [Diagram evidence, examples and compatibility](../skills/codebase-diagrams/references/diagram-guide.md) |
| `plan_prompt.md` | [implementation-planning](../skills/implementation-planning/SKILL.md) | [Roadmaps](../skills/implementation-planning/references/roadmap.md), [risk and acceptance](../skills/implementation-planning/references/risk-and-acceptance.md) |
| `test_prompt.md` | [feature-hardening](../skills/feature-hardening/SKILL.md) | [Scenario matrix and testing](../skills/feature-hardening/references/scenarios.md) |
| `work_on_plan.md` | [execute-plan](../skills/execute-plan/SKILL.md) | [Implementation and completion boundaries](../skills/execute-plan/references/implementation-boundaries.md) |

The entry points are authoritative for scope and workflow. References supply
conditional detail, not competing instructions. Each package includes MIT license
and notice files, and has no required dependency on another package. Technology
and repository conventions are detected locally. No automatic network lookup is
needed to apply the guidance.

## Coverage terminology

**Retained:** preserved intent with concise wording. **Improved:** corrected a
behavioral ambiguity, unsafe assumption or overclaim. **Consolidated:** merged
repeated instructions into their relevant workflow/reference. **Removed:** dropped
a mandate or scaffold that does not belong in a reusable skill; the reason follows.

## Production cleanup

| Original topic | Disposition and location/reason |
|---|---|
| Role, objective, core principles, final rule | Consolidated in purpose, authority, evidence and scoped outcome; no persona boilerplate. |
| Repository protection and discovery | Retained in baseline; inspect index/tree/untracked state, relevant project stack and operational entry points. |
| Validation baseline | Improved: safe existing commands, exact state/results, missing prerequisites and failure attribution; no automatic installs or production access. |
| Evidence inventory | Retained ID/category/location/impact/confidence/action/removal risk/checks, with compact reporting. |
| Approval for every destructive/behavior/security change | Improved: respect existing authorization; require a decision only outside scope or for material unresolved intent. |
| A: Demo/sample/placeholder functionality | Retained in inventory; distinguish legitimate sample products/tests/docs from accidental production artifacts. |
| B: Dead/obsolete code | Improved: dynamic/config/framework/generated usage and external public consumers prevent false removal. |
| C: Dependencies | Retained ecosystem-aware manifests/lockfiles, tooling, classifications and vulnerabilities; no incidental upgrades. Analyzer warnings are supporting evidence only. |
| D: Development code/access bypasses | Retained reachability and production config checks; no incidental auth redesign. |
| E: Logging/error handling | Retained useful operational logs, removal of temporary diagnostics, redaction and existing logging conventions. |
| F: Environment/configuration | Improved context-sensitive CORS/cookies/local URLs; configuration precedence and potentially exposed secrets. |
| G: Security review | Retained focused auth/ownership/tenant/input/redirect/injection/CSRF/token/error checks; no blanket security certification or live exploitation. |
| H: Flags/experiments/markers | Retained lifecycle and rollback checks; names, age, TODOs and flag defaults are not removal evidence. |
| I: Duplication/assets | Retained caller/contract checks and CSS/template/manifest/localization/generated references; broad refactoring remains separate. |
| J: Routes/APIs/integrations | Improved operational/public consumers; zero internal callers does not establish obsolescence. |
| K: Database/migrations/seeds | Retained history/data/initialization protection; distinguish preparing artifacts from applying changes. |
| L: Git hygiene/docs | Retained ignore/distribution checks, user-owned files and directly affected docs; no broad clean or history rewrite. |
| Safe implementation batches | Retained narrow changes, diff review and targeted verification; retain existing tests and user work. |
| Final checks/statuses | Improved PASS/FAIL/BLOCKED/NOT RUN with baseline attribution and dirty-tree versus committed-head distinction. |
| Eight mandatory report sections | Consolidated into relevant evidence, changes, checks, deferred work and limitations; empty sections removed. |
| READY FOR PRODUCTION / MINOR REVIEW / NOT READY | Removed as cleanup-wide verdicts; scoped completed/incomplete/blocked outcomes avoid unsupported release certification. |

## Codebase diagrams

| Original topic | Disposition and location/reason |
|---|---|
| Entire-codebase analysis | Improved scoped discovery first; a broad request still maps the system without blindly reading every file. |
| 1: System architecture | Retained component/protocol boundaries; distinguish source/configuration from observed running systems. |
| 2: User flow | Retained roles, success/failure decisions and differing flows, based on actual handlers/screens. |
| 3: Data flow | Retained transformations, validation, trust/persistence boundaries; no invented layers. |
| 4: Database/ER | Improved constraint/cardinality evidence and modeled/migrated/deployed schema distinction. |
| 5: Backend/API flow | Retained actual route, middleware, validation, permission and downstream order. |
| 6: Authentication/authorization | Retained actual login/token/session/refresh/logout/permission lifecycle; no real secrets in docs. |
| 7: Sequence | Improved actual async ordering and failure alternatives; no inferred delivery guarantees. |
| 8: Deployment/infrastructure | Improved configured versus deployed topology, infrastructure revision and runtime evidence limits. |
| 9: Jobs/async | Retained producers/workers/schedules/retries/transactions with evidence for guarantees. |
| 10: Module dependencies | Retained import/runtime/network distinctions and actual dependency direction. |
| Readability, explanations and consistent naming | Retained splitting by purpose, source paths/symbols and explanatory prose. |
| Unknowns and source traceability | Improved evidence state/revision and consequential unknowns; no unsupported architecture guesses. |
| Ten-file documentation structure | Improved adaptive existing structure, `docs/architecture/` fallback, applicable files only; inline requests remain inline. |
| Fixed six-section document template | Consolidated into purpose, diagram, source-backed explanation and relevant limits; omit empty repeated sections. |
| Mermaid validation (new) | Added local syntax versus render/readability versus source accuracy, host-version caveats and safe labels; missing tools are not a pass. |

## Implementation planning

| Original numbered topic | Disposition and location/reason |
|---|---|
| 1: Primary objective | Retained repository-grounded, implementation-ready planning, not implementation. |
| 2: Planning mode | Consolidated current/partial/completed/planned state in inspection and maintenance; cannot toggle host mode. |
| 3: New task input | Improved natural-language requirements; removed mandatory pasted NEW TASK block and placeholders. |
| 4: Repository analysis | Consolidated relevant application/data/infrastructure/tests/docs inspection; no mandatory whole-project inventory. |
| 5: Existing plan analysis | Retained matching phases/tasks/history/dependencies and avoiding duplicates. |
| 6: Task type | Retained useful classification without mandatory category fields. |
| 7: Verify before assuming | Retained current versus proposed versus unknown; no invented files/contracts. |
| 8: Impact | Consolidated affected components and risk-reference rows; include only applicable boundaries. |
| 9: Dependency analysis | Improved upstream/downstream/internal/external sequencing, cycles and genuine parallel work. |
| 10: Plan-change choices | Retained reuse/extend/add task/modify phase/new phase/discovery decision criteria. |
| 11: Global location | Improved adaptive existing format and inline default; docs/plan only a new persistent-roadmap fallback. |
| 12: Index requirements | Consolidated objective, links, order/dependencies/progress/decisions/traceability; no empty compulsory tables. |
| 13: Phase requirements | Retained objective/scope/prerequisites/tasks/completion and stable IDs; phases only when useful. |
| 14: Task structure | Consolidated outcome/current evidence/approach/dependencies/acceptance and applicable UI/API/data/permission/error concerns. |
| 15: Technical implementation | Retained verified/proposed architecture, contracts, data/business/async/observability details for complex tasks. |
| 16: Acceptance criteria | Improved observable outcomes and suitable verification; not vague robust/fast claims. |
| 17: Definition of done | Consolidated applicable implementation/testing/security/performance/docs/release requirements; distinguish acceptance and process gates. |
| 18: Risks | Retained concrete impact, mitigation and unresolved decisions; no mandatory large matrix. |
| 19: Discovery | Improved bounded investigation only for a material unknown that survives local inspection. |
| 20: Prioritization | Retained impact/business evidence; no invented priority. |
| 21: Effort | Retained no invented estimates; justified complexity or unknown/omitted field. |
| 22: Compatibility | Retained clients/data/flags/migration/rollout/recovery where needed. |
| 23: Security | Retained applicable trust/access/tenant/abuse/secrets/audit concerns; specialist review proportional to actual risk. |
| 24: Data integrity | Retained records/nullability/constraints/duplicates/backfill/partial failures/transactions/recovery. |
| 25: Avoid overengineering | Retained reuse and smallest justified extension; no gratuitous services or abstractions. |
| 26: Maintenance | Improved stable identifiers, preserved completed history and reasoned follow-ups; no incidental renumbering/format migration. |
| 27: Status rules | Improved existing vocabulary first; small fallback with optional review/QA/discovery states, evidence-based done. |
| 28: Final review | Consolidated readiness checks with material gaps explicit; unknowns do not automatically create discovery tasks. |
| 29: Output boundaries | Improved relevant planning artifacts only when requested; preserve inline requests and source code. |
| 30: Final response | Consolidated relevant plan changes/order/criteria/decisions/limits; no implementation or fixed empty sections. |

## Feature hardening

| Original topic | Disposition and location/reason |
|---|---|
| One feature/module | Retained; selection guided by request and repository, clarify materially different candidates. |
| Step 1: Understand feature | Retained flow/contracts/tests/side effects/dependencies and scoped baseline. |
| Step 2A: Happy path | Retained ordinary/min/max/combinations/repeated behavior as applicable scenarios. |
| Step 2B: Validation | Retained missing/null/blank/type/format/boundary/duplicate/reference/large inputs; Unicode rules follow the contract. |
| Step 2C: Business logic | Retained state transitions/conflicts/completed/deleted/forbidden/duplicate/concurrency/partial effects. |
| Step 2D: Database | Retained missing/duplicate/constraint/stale/related/transaction/timeout/connection/partial failure paths; mocks do not prove real rollback. |
| Step 2E: Authentication/authorization | Retained credential/role/ownership/tenant/privilege boundaries where applicable. |
| Step 2F: External services | Retained success/timeout/connection/4xx/5xx/malformed/empty/rate limit/unavailable/retry/duplicate behavior with safe boundaries. |
| Step 2G: Errors | Retained correct result/error/state/log/resource consequences; no forced HTTP concepts for libraries. |
| Step 2H: Edge cases | Retained data/boundary/Unicode/order/slow dependency/restart/retry/partial lifecycle scenarios based on risk. |
| Step 3: Write tests | Improved meaningful outcomes, isolated data/clocks/randomness/synchronization and existing tooling. |
| Step 4: Run/investigate | Improved implementation/test/baseline/environment/flake attribution and tests-only production boundary. |
| Step 5: Failure audit | Retained unhandled/swallowed errors, leak/rollback/log/retry/race consistency checks within scope. |
| Step 6: Test quality | Retained assertions, behavior, determinism, maintainability and regression protection; no arbitrary coverage quota. |
| Step 7: Report | Consolidated measured counts/scenarios/bugs/checks/gaps; omit unmeasured metrics and empty categories. |
| Important rules and HARDENED definition | Improved scoped completion; removed exhaustive universal “all failures handled” implication. Missing services are evidence limits. |
| Mandatory pre-implementation presentation | Improved brief progress update; no redundant permission pause after authorization. |

## Plan execution

| Original numbered topic | Disposition and location/reason |
|---|---|
| 1: Objective | Retained complete selected-task implementation, relevant tests/docs/config and intended behavior. |
| 2: Execution mode | Consolidated inspect/implement/verify/update with current state and existing work preservation. |
| 3: Selection | Improved explicit task first, then earliest ready/smallest logical item; dependencies validated even if status says ready. |
| 4: Read plan | Retained scope/prerequisites/criteria/risks/DoD; adaptive location and no required planning skill. |
| 5: Verify repo | Retained actual modules/contracts/tests and equivalent renamed paths; no duplicate infrastructure. |
| 6: Existing changes | Retained index/tree/untracked protection and material conflict handling. |
| 7: Implementation principles | Consolidated reuse/minimal scope/current architecture/security/data integrity. |
| 8: Process | Consolidated baseline, narrow change, meaningful tests, criteria review and truthful status update. |
| 9: Backend | Retained actual project layers/business/validation/auth/transaction/job/error/log conventions. |
| 10: Frontend | Retained existing routes/components/forms/state/clients/loading/error/accessibility/responsiveness; no framework replacement. |
| 11: Database | Retained new migrations, constraints/indexes/data preservation and compatibility/recovery; no live execution implied. |
| 12: API | Retained input/access/error contracts, consumers and intentional breaking-change migration/recovery. |
| 13: Auth | Retained server trust boundary, roles/ownership/tenant and permitted/forbidden tests. |
| 14: Errors | Retained applicable validation/missing/duplicate/forbidden/external/timeout/DB/job/partial failures. |
| 15: Integrations | Retained existing clients/timeouts/retries/idempotency/credential/log protection and provider discrepancies. |
| 16: Jobs/async | Retained queue/retry/duplicate/failure/dead-letter/transaction/lifecycle/monitoring concerns where present. |
| 17: Testing | Improved suitable unit/integration/API/UI/E2E choices rather than requiring every layer for every task. |
| 18: Acceptance verification | Retained criterion-level evidence; inspection cannot replace required runtime or human verification. |
| 19: Definition of done | Consolidated applicable implementation/tests/security/performance/docs gates, not every category universally. |
| 20: Quality | Consolidated narrow scope, actual contracts and meaningful regression risks; no broad cleanup. |
| 21: Performance | Retained actual workload/query/resource/measurement requirements; no premature optimization. |
| 22: Security | Retained relevant auth/access/tenant/input/secrets/injection/logging/rate concerns; report material unresolved risk. |
| 23: Plan conflicts | Improved minor adaptations versus separate missing prerequisites versus material requirement conflicts; no silent prerequisite scope expansion. |
| 24: Scope | Improved inherent necessary work versus separately planned dependencies; recommend optional work without executing it. |
| 25: Task status | Improved verification-dependent done, existing vocabulary and honest review/QA/blockers. |
| 26: Phase status | Retained all-required-tasks plus phase criteria; never done from one task. |
| 27: Documentation | Retained directly affected API/config/environment/data/operations/architecture/user behavior, no unnecessary docs. |
| 28: Migration/deployment | Retained ordering/data/backward compatibility/flags/service dependencies/recovery, separate artifact creation from deployment. |
| 29: Problems | Improved introduced/pre-existing/environment/unresolved attribution and relevance of required gates. |
| 30: Final verification | Retained actual safe commands and applicable criteria; dirty-tree results are not committed-head verification. |
| 31: Response | Consolidated task/changes/criteria/checks/status/limits/next recommendation; no auto-start of next task or empty sections. |
| 32: Critical rules | Consolidated in workflow; removed repeated slogans and task-ID/optional-instruction placeholders. |

## Source integrity

SHA-256 captured before conversion and compared after implementation. Only
filenames are recorded to avoid distributing personal filesystem paths.

| Source prompt | SHA-256 |
|---|---|
| `clean_prompt.md` | `e75592a7c2524f96d31139eac00a2b0e9840779937eb6e213f633a5d6723b436` |
| `docs_prompt.md` | `ca19e56e479b225c40bf636cb4817cd6d8f78fa419d10c5969089c9da6909ef8` |
| `plan_prompt.md` | `623f896d3831e62b7ff96ec9ea0dfed0b2581ba3ca694e1a260e892d94af404e` |
| `test_prompt.md` | `580e6e18714c5e697fbb23ad05e94efb51a91c6328a7515bfe82fd6dd3dcf5b3` |
| `work_on_plan.md` | `1a6a5a8a885a1e1ea03d1b54f1526581b9dbe84fd616d98edb4b494d2e6d801e` |

## Research incorporated

Original summaries checked **2026-10-27**; these are maintenance sources, not
online prerequisites or copied manuals. Tool-specific caveats apply only when
that tool/version is relevant; detect project tools and renderer versions locally.

- [Agent Skills authoring](https://agentskills.io/skill-creation/best-practices): focused scope, moderate detail, selective resources and execution feedback.
- [OpenAI skill evaluation](https://developers.openai.com/blog/eval-skills): trigger examples, independent executions and observable artifact/command evidence.
- [Knip issue investigation](https://knip.dev/guides/handling-issues): dynamic/generated/plugin/external-consumer analysis limits; optional ecosystem-specific tool.
- [Git clean](https://git-scm.com/docs/git-clean), [Git rm](https://git-scm.com/docs/git-rm): deletion/index effects; no broad cleanup or incidental staging.
- [Mermaid API](https://mermaid.js.org/config/usage.html), [syntax](https://mermaid.js.org/intro/syntax-reference.html), [architecture](https://mermaid.js.org/syntax/architecture.html): parsing versus rendering, established forms, architecture 11.1.0+; current docs 12.2.0.
- [GitHub diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams): destination Mermaid version can differ from local tools.
- [Google behavior testing](https://testing.googleblog.com/2013/08/testing-on-toilet-test-behavior-not.html), [pytest flakes](https://docs.pytest.org/en/stable/explanation/flaky.html): public outcomes and controlled state/synchronization; interaction assertions remain useful when interactions are the contract.

Future model, host, project and tooling changes can require maintenance. This
conversion does not promise that all later improvements are unnecessary.
