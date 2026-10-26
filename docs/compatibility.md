# Compatibility

The collection uses one standard skill definition per directory. The
[Agent Skills specification](https://agentskills.io/specification) defines its
metadata and resource layout; the [official CLI agent table](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)
documents available install targets. Checked 2026-10-26 with CLI 1.7.4.

| Agent | Project-local path observed with `--copy` | Evidence |
|---|---|---|
| Claude Code | `.claude/skills/pr-review/` | CLI discovery and temporary installation; package bytes compared |
| Codex | `.agents/skills/pr-review/` | CLI discovery and temporary installation; package bytes compared |
| Cursor | `.agents/skills/pr-review/` | CLI discovery and temporary installation; package bytes compared |
| Other CLI-supported agents | Consult the CLI's agent table | Documented installer support; not tested here |

These checks verify packaging, not agent reasoning. No live agent review or
provider integration was exercised during repository setup. Agent versions,
permissions, context budgets, and structured output tools can affect behavior.
The skill falls back to a text report when host-specific output tools are absent.

`pr-review` uses Git and local repository evidence. GitHub/GitLab context is
optional and read-only; unavailable context is disclosed. Team policy and
Google style activate independently and only when opted in. Framework and style
references work offline within their stated version scope; unknown behavior
remains unverified. No extra agent-specific definitions or required connector
is bundled.

Maintainers need Python 3.11+ and Git for the pinned official reference validator
and collection tooling. Review users do not need Python merely to read the
skill; its evaluation scripts are development tools. Some example tests skip
when optional project runtimes or libraries are absent. See the
[verification report](verification.md) for exact outcomes.
