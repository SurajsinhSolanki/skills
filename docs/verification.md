# Repository setup verification

Checked **2026-10-26**. The initial workspace held one skill at the root, with
72 files and no collection-level automation or license. There were no naming
conflicts. Git reported “not a git repository”; the existing `.git` location
was preserved. There was no discoverable GitHub owner or remote.

## Changes and preservation

The complete skill moved to `skills/pr-review/`, keeping its public name,
review modes, 18 framework passes, 21 style guides, checklists, policy,
workflows, templates, and evaluation resources. A before/after SHA-256 comparison
confirmed 71 original files byte-identical. `SKILL.md` differs only by a license
metadata field; removing that line reproduces its original hash. License and
attribution files were added to the standalone package.

Collection additions are the generated catalog, repository identity setting,
validation scripts/tests, contribution/security docs, installation/compatibility/
development guides, issue and PR templates, and GitHub Actions workflow.
No placeholder production skills or custom installation system were added.

## Actual results

| Check | Result |
|---|---|
| Official `skills-ref validate skills/pr-review` | Passed |
| Collection metadata, naming, duplicate detection, package boundaries | Passed |
| Rendered Markdown local files/anchors, including standalone skill links | Passed |
| Basic UTF-8 credential/private-key/personal-path scan | Passed; no hits |
| Generated README catalog check | Passed |
| Collection regression tests | 14 passed |
| Existing review regression tests | 21 passed, 1 skipped (22 total) |
| Existing fixture builder | 32 scenarios built; available local conditions checked |
| CLI 1.7.4 local collection `--list` | Found exactly `pr-review` |
| Project-local `--copy` installs: Codex, Claude Code, Cursor | Passed; each package file hash matched source |
| Quoted `--skill '*'` | Passed in a temporary Codex project |
| Repeated `--skill` for two distinct skills | Passed using disposable fixture skills outside this collection |
| Workflow YAML and issue templates | Parsed locally; expected triggers/steps checked |

The CLI tests ran in fresh temporary projects with telemetry disabled. They did
not change user-level installations. The final skill package has **75 files**,
including its license/attribution resources. Generated Python caches are ignored
and removed from distribution content.

Tooling used: Node.js 24.16.0, Python 3.14.4, Skills CLI 1.7.4, and the official
Agent Skills reference validator at upstream commit
`69ef37e9424c0a7ea9dd2293b559e43ec8176379`. CI targets Python 3.12 on Ubuntu;
the equivalent Python commands ran locally, not on a hosted Actions runner.
The validator dependency is pinned to that commit. CLI support and layout were
checked against the [specification](https://agentskills.io/specification),
[CLI commands](https://github.com/vercel-labs/skills/blob/main/docs/commands.md),
and [skill discovery documentation](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md).

## Limits and remaining owner work

- No public GitHub source exists in the available configuration. GitHub-source
  installation, visibility, actual hosted CI, and a skills.sh listing remain
  unverified. No push or publication was performed. Follow the
  [publishing instructions](development.md#publish) after choosing coordinates
  and recovering any existing Git history.
- Installation and fixture checks are not live agent reviews. Blind behavioral
  evaluation and real provider access still need separate runs.
- Pydantic was not installed; its optional executable example skipped. That
  framework behavior remains source-verified only. The existing fixture suite
  also labels framework cases whose runtime was unavailable.
- The repository scan inspects current UTF-8 text, not history or every secret
  format. Security review found no literal credential hits or new automatic
  download/execution behavior in the installed skill. Existing evaluation tools
  execute bundled example code and synthetic commands in temporary repositories;
  they are maintenance tools, not normal review steps. Review their changes as
  executable code.
- Only `pr-review` exists today. The flat per-skill layout, automatic discovery,
  and generated catalog allow more real skills without reorganizing the repo.

## Maintenance

Add/update guidance with relevant tests and source attribution, regenerate the
catalog, and run the [development checks](development.md#validate). Recheck
agent installation paths and CLI requirements when upgrading tools. Preserve
public skill names and internal links; document any necessary breaking migration.
