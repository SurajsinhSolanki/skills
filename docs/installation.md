# Installation

The [official Skills CLI](https://github.com/vercel-labs/skills) reads standard
`SKILL.md` packages. No npm publication or repository manifest is needed for
this collection. CLI commands below were checked against version **1.7.4** on
**2026-10-26**; Node.js **22.20+** is required by that version. `npx skills` uses
the currently available release; pin `npx skills@1.7.4` to reproduce these checks.

## From GitHub

Run from the project that should receive the skill. The source is
[SurajsinhSolanki/skills](https://github.com/SurajsinhSolanki/skills).
These commands retrieve published content; newly added local skills must be
pushed before GitHub installations can retrieve them. See the
[verification record](verification.md) for what has actually been tested.

```bash
# Interactive skill/agent selection
npx skills add SurajsinhSolanki/skills
# Select the existing review skill
npx skills add SurajsinhSolanki/skills --skill pr-review
# Select the design skill
npx skills add SurajsinhSolanki/skills --skill design-psychology-rules
# Select both skills
npx skills add SurajsinhSolanki/skills --skill pr-review --skill design-psychology-rules
# Select any workflow skill individually
npx skills add SurajsinhSolanki/skills --skill production-cleanup
npx skills add SurajsinhSolanki/skills --skill codebase-diagrams
npx skills add SurajsinhSolanki/skills --skill implementation-planning
npx skills add SurajsinhSolanki/skills --skill feature-hardening
npx skills add SurajsinhSolanki/skills --skill execute-plan
# Combine planning and execution; they still activate independently
npx skills add SurajsinhSolanki/skills --skill implementation-planning --skill execute-plan
# Discover without installing
npx skills add SurajsinhSolanki/skills --list
# Select every skill; quote the wildcard to prevent shell expansion
npx skills add SurajsinhSolanki/skills --skill '*'
# Explicit, noninteractive, project-local installation for one agent
npx skills add SurajsinhSolanki/skills --skill pr-review --agent codex --yes
```

Repeat `--skill` to select multiple names, as in the two-skill example above.
Use `--list` to confirm which skills are available at the selected source.

Installation is project-local by default; add `--global` only when you intend to
install for your user account. Use `--agent claude-code`, `--agent codex`, or
`--agent cursor` to choose a target. `--copy` copies resources rather than linking
them. See [compatibility](compatibility.md) for verified paths and limits.

## From a local checkout

Use an absolute or relative path to the collection; replace `/path/to/agent-skills`
with your checkout. A local source is also useful for testing unpublished changes:

```bash
npx skills add /path/to/agent-skills --list
npx skills add /path/to/agent-skills --skill pr-review --agent codex --yes --copy
npx skills add /path/to/agent-skills --skill design-psychology-rules --agent codex --yes --copy
npx skills add /path/to/agent-skills --skill implementation-planning --skill execute-plan --agent codex --yes --copy
```

All framework, workflow, style, policy, and report references are bundled inside
`pr-review`. Normal reviews do not require browsing. Initial CLI download,
remote repository retrieval, optional provider context, and running a reviewed
project's own dependency-dependent gates may require network access. Git is
needed for the review workflow.

`design-psychology-rules` bundles all three design references and its MIT
license. The listed usability and accessibility checks can be applied offline;
official source links are optional maintenance references. A static artifact
cannot verify runtime behavior, and the skill must disclose that limit.

The five workflow skills also bundle their required guidance, examples, licenses
and notices. They do not require another skill, network lookup or installed
connector. Applying the instructions is offline-capable; executing a project's
own tests/builds or checking Mermaid syntax/rendering requires that project's
available tools. Missing tools are reported rather than installed automatically.
Planning defaults to inline output; existing roadmap formats take precedence
over its new-roadmap fallback. See [usage and selection](../README.md#use).

## Troubleshooting

- No skill discovered: check that the source has `skills/<name>/SKILL.md`
  and that a root `SKILL.md` is not shadowing nested discovery.
- Wrong project/agent: run in the intended project and choose `--agent` explicitly.
  Installation does not prove that an agent loaded or followed the skill.
- Offline initial setup: arrange CLI and source availability beforehand, then
  install from a local path. A cold `npx` invocation cannot download offline.
- Unsupported Node: use a release meeting the CLI's engine requirement.
- Changed catalog: use names returned by `--list`; do not guess new names.

The CLI documents optional anonymous usage telemetry. For private local checks,
set `DISABLE_TELEMETRY=1 DO_NOT_TRACK=1` before invoking it. CLI installation
options and supported agents may change; maintainers should recheck the
[command reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)
when upgrading the pinned smoke-test version.
