# Compatibility

The collection uses one standard skill definition per directory. The
[Agent Skills specification](https://agentskills.io/specification) defines its
metadata and resource layout; the [official CLI agent table](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)
documents available install targets. Initial checks ran on 2026-10-26; local
installation of both skills was checked on 2026-10-27 with CLI 1.7.4.

| Agent | Project-local parent observed with `--copy` | Evidence |
|---|---|---|
| Claude Code | `.claude/skills/` | Both named skill directories installed individually; all package bytes compared |
| Codex | `.agents/skills/` | Both named skill directories installed individually; all package bytes compared |
| Cursor | `.agents/skills/` | Both named skill directories installed individually; all package bytes compared |
| Other CLI-supported agents | Consult the CLI's agent table | Documented installer support; not tested here |

The published GitHub source was also tested with CLI 1.7.4: discovery found
`pr-review`, and a temporary Codex copy installation matched all 75 local skill
files. The [verification report](verification.md) records the published commit
and successful hosted CI run.

The later two-skill local checks installed `design-psychology-rules` (6 files)
and `pr-review` (75 files) in fresh temporary projects. Individual installs for
all three agents, combined selection, wildcard selection, and standalone
metadata/link validation passed. The new design skill's GitHub installation
remains unverified until that addition is pushed and tested remotely.

These checks verify packaging, not agent reasoning. No live agent review or
provider integration was exercised during repository setup. Agent versions,
permissions, context budgets, and structured output tools can affect behavior.
`pr-review` falls back to a text report when host-specific output tools are absent.

`design-psychology-rules` is an instruction-only design workflow. Its three
references, MIT license, and attribution notice are bundled; normal use does not require browsing,
a runtime dependency, or a particular design tool. A screenshot can support
visual observations, but runtime accessibility and usability claims need
appropriate evidence. Neither skill automatically activates the other, and a
design critique does not authorize implementation.

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
