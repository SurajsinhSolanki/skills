# Repository setup verification

Checked **2026-10-26**. The initial workspace held one skill at the root, with
72 files and no collection-level automation or license. There were no naming
conflicts. Git reported “not a git repository”; the existing `.git` location
was preserved. There was no discoverable GitHub owner or remote at that time.

After the owner published the collection, a follow-up check confirmed the public
repository [SurajsinhSolanki/skills](https://github.com/SurajsinhSolanki/skills),
its `main` branch, and commit `e539272addc9bcab80fc341164c31e8b5e8ed383`.
The collection identity and installation documentation now use these coordinates.

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
| Published GitHub source `--list` and isolated Codex `--copy` install | Passed; all 75 files match the local skill |
| Hosted validation workflow at `e539272` | [Passed](https://github.com/SurajsinhSolanki/skills/actions/runs/40375798411) |

The CLI tests ran in fresh temporary projects with telemetry disabled. They did
not change user-level installations. The original `pr-review` package has **75 files**,
including its license/attribution resources. Generated Python caches are ignored
and removed from distribution content.

Tooling used: Node.js 24.16.0, Python 3.14.4, Skills CLI 1.7.4, and the official
Agent Skills reference validator at upstream commit
`69ef37e9424c0a7ea9dd2293b559e43ec8176379`. CI targets Python 3.12 on Ubuntu;
the initial equivalent Python commands ran locally. The later published commit
also passed the hosted workflow, as recorded above. Follow-up documentation
changes had not yet been pushed at that verification step.
The validator dependency is pinned to that commit. CLI support and layout were
checked against the [specification](https://agentskills.io/specification),
[CLI commands](https://github.com/vercel-labs/skills/blob/main/docs/commands.md),
and [skill discovery documentation](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md).

## Limits and remaining owner work

- Public GitHub discovery, installation, and hosted CI are now verified for the
  published commit above. A skills.sh listing remains unverified. The owner
  performed the initial push; no push was performed during this follow-up.
  Follow the [publishing instructions](development.md#publish) for updates.
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
- The initial setup contained only `pr-review`. The design-skill integration
  below adds the second package through the same layout and automatic discovery.

## Maintenance

Add/update guidance with relevant tests and source attribution, regenerate the
catalog, and run the [development checks](development.md#validate). Recheck
agent installation paths and CLI requirements when upgrading tools. Preserve
public skill names and internal links; document any necessary breaking migration.

## Design skill integration — 2026-10-27

Integrated [design-psychology-rules](../skills/design-psychology-rules/SKILL.md)
as the second independent skill. The maintainer confirmed distribution under
the repository's MIT license. Its six-file package contains the entry point,
three existing reference files, a standalone copy of that license, and the
attribution notice referenced by the license.

### Changed files and corrections

- The design entry point adds MIT metadata, the agreed scoped description,
  project/user precedence, permission boundaries, linked selective loading,
  and evidence limits. Review requests produce feedback; implementation needs
  an implementation request. Missing screenshot evidence is not a failure.
- The psychological foundations retain rules 1–26, qualify numerical shortcuts,
  preserve necessary choices, and require an observable misleading mechanism
  before calling pricing emphasis deceptive.
- The UI/UX reference retains rules 27–49 and locally documents WCAG scope,
  target-size/contrast/reflow exceptions, AA versus AAA focus requirements,
  error-prevention alternatives, and motion/flashing distinctions. Adjacent
  criterion summaries clarify keyboard/dragging, status announcements,
  authentication assistance, and repeated help. Official W3C links and a
  2026-10-27 check date accompany the original summaries.
- The toolkit adds evidence/scope fields, not-verified/not-applicable matrix
  entries, and an insufficient-evidence assessment. An untested mockup is not
  certified or implicitly approved. Valid product conventions are not defects
  solely because another pattern is preferred.
- The collection README/catalog, installation guide, compatibility guide, and
  this report now cover both skills. Existing CI and validation scripts already
  discover both; they and `pr-review` were not changed.

### Executed checks

| Check | Result |
|---|---|
| Official reference validator, both skills | Passed |
| Skill-creator quick validation, design skill | Passed |
| Collection metadata, packaging, local links/anchors, basic secret/path scan | Passed |
| Generated catalog and whitespace checks | Passed |
| Collection regression tests | 14 passed |
| Existing review regression tests | 21 passed; 1 optional Pydantic test skipped |
| Existing fixture builder | 32 scenarios built; available local conditions checked |
| Design rule numbering | All 49 present exactly once, in order |
| Standalone license | Byte-identical to repository MIT license |
| Existing skill preservation | All 75 `pr-review` files hash-match the pre-integration snapshot |
| Local CLI `--list` | Exactly both skills found; no installation performed |
| Individual `--copy` installs for Codex, Claude Code, Cursor | Both skills passed for each agent; all 6/75 package files hash-match sources |
| Combined two-name selection and quoted wildcard | Both passed in separate temporary Codex projects |
| Installed package validation | Metadata and local package-boundary/link checks passed independently |

All installation checks used CLI 1.7.4 with Node.js 24.16.0, a local source,
fresh temporary projects, and telemetry disabled. Validation used Python
3.14.4 and the previously pinned official reference-validator commit. No new
dependencies, global installations, custom installer, or agent definitions
were added. Git commit, push, publication, and visibility changes were not
performed.

### Manual scenario walkthrough

These are instruction/source walkthroughs, not generated agent reviews, live
browser tests, or a blind behavioral evaluation. The following supplied
conditions were traced through the updated rules and toolkit:

| Supplied scenario | Walkthrough outcome and basis |
|---|---|
| Screenshot-only checkout review; no DOM or interaction recording | Assess visible hierarchy/copy; mark keyboard, accessible names, live announcements, and hidden behavior not verified. Material missing runtime evidence prevents a runtime ship recommendation (scope/evidence and toolkit). |
| 20×20 CSS px pointer targets with 20 px gaps and known rectangular hit areas | Their centered 24 px circles do not intersect adjacent targets/circles; no 2.5.8 failure solely from being under 24 px (Rule 42). |
| Inline prose link, disabled low-contrast control, or unmodified browser target sizing | Check the relevant inline, inactive, or user-agent exception; do not manufacture a size/contrast failure (Rule 42). |
| Adjacent 16×16 CSS px hit areas, no gaps, no equivalent controls or other exceptions | Circle spacing fails; report confirmed 2.5.8 AA failure and Not ready at the default baseline (Rule 42 and toolkit). |
| Focused item partially overlapped by a header but still visible, including its focus indicator | Not automatically an AA 2.4.11 failure; distinguish the stronger AAA target and any observed usability issue (Rule 42). |
| Wide data table needs two dimensions; surrounding content and cell text reflow | Table scrolling alone is not a reflow failure; inspect the exception's limits (Rule 42). |
| Qualifying transaction is reversible, with no separate review screen | Reversibility can satisfy 3.3.4; do not demand a redundant confirmation step solely for this criterion (Rule 41). |
| Animation lacks a reduced-motion media query; no other demonstrated failure | Recommend motion controls without labeling that omission alone an AA violation. Unknown flashing thresholds remain unverified (Rule 42). |
| Clearly labeled overflow and several dashboard goals follow established tasks | No automatic defect from an overflow menu, click count, or multiple primary tasks; assess actual discoverability and task impact (Rules 1, 2, 8 and toolkit). |
| Most expensive plan appears first; all alternatives and material prices/terms remain clear | Ordering alone does not prove deception; a finding needs evidence of misleading information or constraints (Rule 19). |
| Request concerns only a backend migration or general code review | Outside the design skill's activation scope. No automatic composition with `pr-review` (description and scope). |

The walkthrough found these intended outcomes represented in the guidance.
It does not measure whether a model follows them. A comprehensive research
audit of the psychology rules and a live/blind design-review evaluation remain
outside this integration. Remote discovery/install of the new skill and hosted
CI for these local changes remain unverified until the addition is pushed.

## Design skill research follow-up — 2026-10-27

Applied the targeted findings from the web/source check to the existing six-file
package. All 49 numbered rules remain intact; no additional dependencies, agent
definitions, or install mechanism were introduced. The entry-point checklist
and review toolkit now route reviewers through the corrected checks.

| Finding | Completed correction |
|---|---|
| Rule 46 authentication copy could disclose account existence | Replaced the registration example with neutral field-copy guidance and a security-context exception. Recovery copy must describe actual behavior and respect enumeration protections; normal product errors should remain useful. |
| Rule 41 omitted redundant-entry exceptions | Bundled essential, security, and no-longer-valid exceptions, with auto-population/selection for ordinary repeats. Input preservation now respects secret-retention and expiration rules. |
| Rule 38 suggested progress values for any long operation | Known totals justify determinate progress; unknown-duration work may use labeled indeterminate status. Percentages, steps, and estimates cannot be invented. Duration ranges are examples, not universal thresholds. |
| Rule 23 email normalization was ambiguous | Separated case-insensitive domains from potentially case-sensitive local parts; rewriting or identity merging requires an explicit project/provider contract. |
| Rule 42 omitted visible-label/name matching | Added WCAG 2.5.3, a failing `Delete`/`Remove item` example, and a valid longer name containing the visible label. Exact equality is not universally required. |
| Tooltip recommendations lacked interaction requirements | Added WCAG 1.4.13 dismissal, hoverability, persistence, and exceptions. A tooltip is not mandatory on every icon, a replacement for its name, or sufficient explanation for an unfocusable disabled control. |
| Eight-character example could imply a universal password policy | Replaced it with an explicitly conditional project-name example. Summarized NIST's 15-character single-factor / 8-character MFA distinction only where that standard applies; the project's applicable policy governs. |

The relevant original summaries and optional source links are bundled in
[Rule 23](../skills/design-psychology-rules/references/rules.md#23-be-forgiving-with-inputs-postels-law),
[Rule 38](../skills/design-psychology-rules/references/ux-quality.md#38-visibility-of-system-status--loading),
[Rule 41](../skills/design-psychology-rules/references/ux-quality.md#41-error-prevention--recovery),
[Rule 42](../skills/design-psychology-rules/references/ux-quality.md#42-accessibility-by-default),
and [Rule 46](../skills/design-psychology-rules/references/ux-quality.md#46-content-design).
Sources include RFC 5321, Carbon, NIST SP 800-63B-4, OWASP, and official W3C
Understanding guidance. Normal use still requires no web lookup.

### Follow-up validation

- Official design-skill metadata validation, collection metadata/package/link
  checks, catalog freshness, and whitespace checks passed.
- Collection tests: 14 passed. Existing review tests: 21 passed, with the
  optional Pydantic example skipped. All 32 existing fixtures built and their
  available local conditions checked.
- Local CLI 1.7.4 discovery found both skills without installing. Fresh
  individual design-skill copy installations for Codex, Claude Code, and Cursor,
  plus combined and wildcard Codex installations, passed. Every selected file
  matched its source, and installed standalone packages passed local validation.
- All 49 design rule numbers remain present exactly once. All 75 `pr-review`
  file hashes match the snapshot taken before this follow-up.

Manual instruction walkthroughs covered an unknown-duration job, an email whose
local-part case must be preserved, a repeated shipping field versus an expired
security value, account-sensitive recovery copy, a mismatched speech label,
a valid longer accessible name, a tooltip that disappears on pointer entry,
and the native-tooltip exception. The written rules now distinguish failures,
valid exceptions, and evidence limits in those scenarios. No live UI or blind
agent evaluation was performed; these walkthroughs and the existing fixture
checks do not prove agent behavior. Remote installation and hosted CI for the
updated skill remain unverified. Nothing was committed or pushed.
