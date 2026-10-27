# Agent Skills

A collection of independently installable AI coding-agent skills in the
[Agent Skills format](https://agentskills.io/specification). The collection
contains seven independently installable skills. New skills belong in separate
directories under `skills/`.

`pr-review` provides evidence-based, read-only code review with bundled offline
framework guidance. Its 18 framework passes, 21 style guides, and review modes
remain together in one installable package. Load references selectively.

`design-psychology-rules` provides 49 rules for usable, accessible, discoverable,
and ethical interfaces, with evidence-aware design reviews and bundled guidance.

Five focused workflow skills cover conservative cleanup, Mermaid documentation,
implementation planning, feature hardening, and execution of a selected plan task.
Each works independently with bundled offline guidance and explicit scope.

## Install

From your target project, with Node.js 22.20 or newer:

```bash
npx skills add SurajsinhSolanki/skills
npx skills add SurajsinhSolanki/skills --skill pr-review
npx skills add SurajsinhSolanki/skills --skill design-psychology-rules
npx skills add SurajsinhSolanki/skills --skill implementation-planning --skill execute-plan
npx skills add SurajsinhSolanki/skills --list
npx skills add SurajsinhSolanki/skills --skill '*'
```

The official CLI documents Claude Code, Codex, Cursor, and other agents.
[Compatibility](docs/compatibility.md) distinguishes installation checks from
agent behavior tests. See [installation](docs/installation.md) for local use,
agent selection, multiple skills, scope, and troubleshooting.

## Available skills

<!-- SKILLS:START -->
| Skill | Description | Installation |
|---|---|---|
| [codebase-diagrams](skills/codebase-diagrams/SKILL.md) | Create or update Mermaid architecture, user/data/API flows, sequence, database, deployment, and module diagrams grounded in repository evidence. Use for visual technical documentation of an existing system or selected workflow; not UI mockups, implementation planning, or a mandatory full-codebase knowledge bundle. | `npx skills add SurajsinhSolanki/skills --skill codebase-diagrams` |
| [design-psychology-rules](skills/design-psychology-rules/SKILL.md) | Design, build, or critique user-facing interfaces using psychology-informed usability, accessibility, discoverability, and ethical-design checks. Use for screens, product flows, mockups, and pre-ship UX reviews; not unrelated backend changes or general code review. | `npx skills add SurajsinhSolanki/skills --skill design-psychology-rules` |
| [execute-plan](skills/execute-plan/SKILL.md) | Implement a selected ready task from an existing project plan, verify its acceptance criteria, and update task status with evidence. Use when asked to execute a plan task or take the next unblocked roadmap item; not planning-only requests, automatic whole-roadmap execution, or unrelated cleanup. | `npx skills add SurajsinhSolanki/skills --skill execute-plan` |
| [feature-hardening](skills/feature-hardening/SKILL.md) | Harden one selected feature with risk-based tests, failure-path investigation, and narrow verified bug fixes. Use for feature robustness, edge-case testing, and failure-handling requests; honors tests-only or audit-only scope. Not a general PR review, repository-wide rewrite, or automatic coverage expansion during ordinary implementation. | `npx skills add SurajsinhSolanki/skills --skill feature-hardening` |
| [implementation-planning](skills/implementation-planning/SKILL.md) | Analyze a repository and create or update an implementation-ready plan for a feature, bug, refactor, migration, or technical requirement. Use when the user requests planning or roadmap maintenance before coding; preserves existing plan formats and task history. Does not implement tasks or automatically create saved roadmaps for inline planning requests. | `npx skills add SurajsinhSolanki/skills --skill implementation-planning` |
| [pr-review](skills/pr-review/SKILL.md) | Review pull requests, branch comparisons, staged changes, or working-tree diffs for correctness, requirements, security, reliability, and production readiness. Use for pre-merge reviews, re-reviews after fixes, or “is this safe to ship?” requests. Produces evidence-backed findings and an approval, request-changes, or incomplete assessment; supports inline comments and host-structured findings. Reviews only, without applying fixes. | `npx skills add SurajsinhSolanki/skills --skill pr-review` |
| [production-cleanup](skills/production-cleanup/SKILL.md) | Audit or remove confirmed unnecessary code, dependencies, demo artifacts, assets, and debugging leftovers while preserving intended behavior. Use for conservative repository cleanup and release cleanup requests; not ordinary code review, dependency upgrades, feature development, or a full security certification. | `npx skills add SurajsinhSolanki/skills --skill production-cleanup` |
<!-- SKILLS:END -->

The table is generated from skill metadata. Run
`python scripts/update_catalog.py` after adding or updating a skill; CI rejects
stale catalogs. The installation source is configured in
[repository.json](repository.json); update it if the repository moves.

## Use

Once installed, ask the agent to use the relevant skill, for example:

- “Use pr-review to review my staged changes.”
- “Use pr-review to compare this branch against main.”
- “Re-review this PR against the previous head and report remaining findings.”
- “Use design-psychology-rules to review this checkout flow for usability, accessibility, and transparent pricing.”
- “Use production-cleanup to remove confirmed retired demo artifacts and preserve runtime behavior.”
- “Use codebase-diagrams to document the existing checkout request flow in Mermaid.”
- “Use implementation-planning to update our roadmap for CSV export. Plan only.”
- “Use feature-hardening to test profile validation and fix narrow confirmed bugs.”
- “Use execute-plan to implement task EXP-4 and verify its acceptance criteria.”

`pr-review` follows project rules, keeps team-policy and Google-style opt-ins
independent, and reviews without applying fixes. Its [usage guide](skills/pr-review/README.md)
explains targets, report modes, verdicts, offline coverage, and verification limits.
It can inspect sensitive project content: use the agent's existing permissions
and review commands before authorizing execution.

The [design skill](skills/design-psychology-rules/SKILL.md) separates confirmed
problems, suggestions, and unverified behavior. A screenshot cannot establish
complete accessibility conformance. A design review produces feedback; requested
implementation is a separate scope. Neither skill automatically activates the other.

Choose planning to describe future work, execution to carry out a roadmap task,
and hardening to investigate one feature's robustness. A tests-only hardening
request preserves production code; cleanup audits produce findings rather than
edits. Diagramming documents the current implementation. Loading a skill grants
no authority for deployment, publishing, production access, or unrelated work.

The [conversion coverage](docs/workflow-skills-conversion.md) maps the original
prompt topics to their improved guidance. The [workflow evaluations](evals/workflow-skills/README.md)
separate fixture checks, independent agent execution and installation evidence.

## Layout

```text
skills/pr-review/       Installable skill and its existing resources/evaluations
skills/design-psychology-rules/  Design skill, local references, and MIT license
skills/production-cleanup/      Evidence-based cleanup and audit guidance
skills/codebase-diagrams/       Source-backed Mermaid documentation
skills/implementation-planning/ Adaptive implementation plans and roadmaps
skills/feature-hardening/       Risk-based tests and narrow feature fixes
skills/execute-plan/            Selected-task implementation and verification
evals/workflow-skills/          Maintenance-only synthetic workflow evaluations
scripts/               Collection validation and catalog generation
tests/                 Collection validator regression tests
docs/                  Installation, compatibility, development, verification
.github/               Issue/PR templates and validation workflow
```

Each skill has one `SKILL.md` entry point. Resource directories stay within that
skill; they need not be renamed to fit a template. There is no root `SKILL.md`
and no custom installer or duplicate agent-specific skill definition.

## Contribute and maintain

See [CONTRIBUTING.md](CONTRIBUTING.md) and the [development guide](docs/development.md).
Validation uses the official reference validator plus narrow collection checks.
The [verification report](docs/verification.md) records what was actually tested
and [publishing steps](docs/development.md#publish) cover initial setup and updates.
Report vulnerabilities using [SECURITY.md](SECURITY.md).

Original work is [MIT licensed](LICENSE). Preserve the separate third-party
attributions and license terms in [NOTICE.md](NOTICE.md).
