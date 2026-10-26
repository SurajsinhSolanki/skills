# Agent Skills

A collection of independently installable AI coding-agent skills in the
[Agent Skills format](https://agentskills.io/specification). The collection
currently contains one maintained skill, `pr-review`; new skills belong in
separate directories under `skills/`.

`pr-review` provides evidence-based, read-only code review with bundled offline
framework guidance. Its 18 framework passes, 21 style guides, and review modes
remain together in one installable package. Load references selectively.

## Install

From your target project, with Node.js 22.20 or newer:

```bash
npx skills add SurajsinhSolanki/skills
npx skills add SurajsinhSolanki/skills --skill pr-review
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
| [pr-review](skills/pr-review/SKILL.md) | Review pull requests, branch comparisons, staged changes, or working-tree diffs for correctness, requirements, security, reliability, and production readiness. Use for pre-merge reviews, re-reviews after fixes, or “is this safe to ship?” requests. Produces evidence-backed findings and an approval, request-changes, or incomplete assessment; supports inline comments and host-structured findings. Reviews only, without applying fixes. | `npx skills add SurajsinhSolanki/skills --skill pr-review` |
<!-- SKILLS:END -->

The table is generated from skill metadata. Run
`python scripts/update_catalog.py` after adding or updating a skill; CI rejects
stale catalogs. The installation source is configured in
[repository.json](repository.json); update it if the repository moves.

## Use

Once installed, ask the agent to use the review skill, for example:

- “Use pr-review to review my staged changes.”
- “Use pr-review to compare this branch against main.”
- “Re-review this PR against the previous head and report remaining findings.”

The skill follows project rules, keeps team-policy and Google-style opt-ins
independent, and reviews without applying fixes. Its [usage guide](skills/pr-review/README.md)
explains targets, report modes, verdicts, offline coverage, and verification limits.
It can inspect sensitive project content: use the agent's existing permissions
and review commands before authorizing execution.

## Layout

```text
skills/pr-review/       Installable skill and its existing resources/evaluations
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
