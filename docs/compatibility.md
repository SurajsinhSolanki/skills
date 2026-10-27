# Compatibility

The collection uses one standard skill definition per directory. The
[Agent Skills specification](https://agentskills.io/specification) defines its
metadata and resource layout; the [official CLI agent table](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)
documents available install targets. Initial checks ran on 2026-10-26; local
installation of both skills was checked on 2026-10-27 with CLI 1.7.4.
The later workflow-skill conversion checked all seven local packages with the
same CLI; historical remote results below apply only to their recorded revision.

| Agent | Project-local parent observed with `--copy` | Evidence |
|---|---|---|
| Claude Code | `.claude/skills/` | Existing two packages previously tested; five new workflow packages individually copied and byte-compared on 2026-10-27 |
| Codex | `.agents/skills/` | Existing two packages previously tested; five new workflow packages individually copied and byte-compared on 2026-10-27 |
| Cursor | `.agents/skills/` | Existing two packages previously tested; five new workflow packages individually copied and byte-compared on 2026-10-27 |
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

## Workflow packages — 2026-10-27

The local source now contains seven independently installable packages. CLI 1.7.4
found all seven. Individual copy installations of the five new workflow skills
passed for Codex, Claude Code and Cursor; combined five-name selection and a
wildcard installation of all seven passed in fresh Codex projects. Installed
resource hashes matched source files. No user-level installation was changed.

The five packages are instruction-only and self-contained. Planning does not
require the execution skill; execution can read another project's existing plan
format without the planning skill. Diagrams use available Mermaid tooling and
record unavailable parser/render checks. Project-specific tests and tools may
have prerequisites; no runtime or connector is installed automatically.

Focused workflow execution evaluations use fresh agents on the current host,
separately from CLI packaging checks. Their cases and actual outcomes are in the
[verification report](verification.md) and [evaluation procedure](../evals/workflow-skills/README.md).
They do not establish behavior on Claude Code, Cursor, every model, or arbitrary
real projects. Remote discovery/install and hosted CI for these unpublished
workflow additions remain unverified until pushed and tested.
