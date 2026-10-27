# Applied skill fixes

Applied 27 October 2026. Updated all 23 advertised skills, 20 cached artifact-template skills and the available review helper. Changed or restored **56 files** across **44 skill entrypoints**. No plugin connection, publishing, installation of new services, image generation or external messaging was performed.

## Verification

- Six behavioral tests passed: required-resource/tool detection, empty-name rejection, valid/invalid knowledge bundles, read-only bundle checks, graph generation with untrusted text, visualization CLI output, and installation of an older pinned commit. Some tests exercise multiple related cases.
- All changed Python files compile; links and anchors in changed Markdown resolve using the staged package and unchanged installed resources.
- Both installed package validators passed, including optional skill-resource checks.
- SHA-256 readback verified all 56 installed files against their validated staged content.
- Preserved the existing public display-style names `Presentations` and `Spreadsheets` for compatibility rather than renaming their invocation identities to satisfy the generic creator naming convention.
- Did not run billable generations, live Excel/Google operations or deployments to test wording-only changes.

The missing codebase-knowledge files were recovered from `SurajsinhSolanki/codebase-knowledge` at commit `aaabe62968f1c2d9f7f7516793b0dd85433ed8dc`, matching the installed skill lock. Its restored visualization script was also hardened to treat documentation titles and types as text rather than injected markup.

## Changes by skill

| Skill | Change |
|---|---|
| [orchestration](/home/surajsinh/.agents/skills/orchestration/SKILL.md) | Qualified generic coordination triggers with Orca context and preserved exact-runtime safeguards. |
| [orca-cli](/home/surajsinh/.agents/skills/orca-cli/SKILL.md) | Required Orca context and documented prerequisites and bounded unavailable-runtime handling. |
| [codebase-knowledge](/home/surajsinh/.agents/skills/codebase-knowledge/SKILL.md) | Restored the exact upstream resources; added hash-based overwrite/freshness rules, explicit bundle validation and read-only validation. |
| [find-skills](/home/surajsinh/.agents/skills/find-skills/SKILL.md) | Narrowed discovery triggers, replaced popularity gates with content inspection and made global/unattended installation conditional on scope. |
| [computer-use](/home/surajsinh/.agents/skills/computer-use/SKILL.md) | Made the Orca dependency explicit and routed ordinary host tasks to available host tools. |
| [frontend-design](/home/surajsinh/.agents/skills/frontend-design/SKILL.md) | Removed invented client history and mandatory novelty; added usability and contrast verification. |
| [openai-docs](/home/surajsinh/.codex/skills/.system/openai-docs/SKILL.md) | Preserved the corrected lookup fallback; clarified local inspection and host communication precedence. |
| [skill-creator](/home/surajsinh/.codex/skills/.system/skill-creator/SKILL.md) | Added optional resource/tool checks and rejected empty required frontmatter values. |
| [imagegen](/home/surajsinh/.codex/skills/.system/imagegen/SKILL.md) | Made native tool transparency and current schema authority explicit; retained authorized API fallback boundaries. |
| [skill-installer](/home/surajsinh/.codex/skills/.system/skill-installer/SKILL.md) | Clarified scope, provenance, escalation and replacement; fixed Git fallback for non-head pinned commits. |
| [sites-remix](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/sites/1.1.2/skills/sites-remix/SKILL.md) | Changed the question limit to batches of three and preserved unanswered-decision boundaries. |
| [sites](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/sites/1.1.2/skills/sites/SKILL.md) | Separated repository implementation from Sites hosting; reused established publication intent and restored required checks. |
| [plugin-management](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/plugin-management/0.1.0/skills/plugin-management/SKILL.md) | Selected the current removal tool from the live schema. |
| [artifact-template-strategy-memorandum](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-strategy-memorandum/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-business-review](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-business-review/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-project-tracker](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-project-tracker/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-operating-review](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-operating-review/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-three-statement-forecast](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-three-statement-forecast/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-financial-budget](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-financial-budget/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-legal-memorandum](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-legal-memorandum/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-analytics-dashboard](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-analytics-dashboard/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-sales-pipeline](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-sales-pipeline/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-design-report](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-design-report/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-minimal-letterhead](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-minimal-letterhead/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-team-alignment](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-team-alignment/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-simple-dark-mode](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-simple-dark-mode/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-project-kickoff](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-project-kickoff/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-operating-calendar](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-operating-calendar/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-simple-light-mode](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-simple-light-mode/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-system-design](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-system-design/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-market-trends-report](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-market-trends-report/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-experiment-analysis](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-experiment-analysis/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [artifact-template-investment-committee-memo](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/openai-templates/0.1.1/skills/artifact-template-investment-committee-memo/SKILL.md) | Added the reviewed template-specific input checks, missing-input handling and capability recovery. |
| [update-pet](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/work-pets/0.1.6/skills/update-pet/SKILL.md) | Captured current active selection before mutation to support preservation verification. |
| [pets](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/work-pets/0.1.6/skills/pets/SKILL.md) | Clarified the single confirmation path for an explicitly requested, identified deletion. |
| [create-pet](/home/surajsinh/.codex/plugins/cache/openai-curated-remote/work-pets/0.1.6/skills/create-pet/SKILL.md) | Added capability preflight, resource checkpoints and resumable stopping rules. |
| [visualize](/home/surajsinh/.codex/plugins/cache/openai-bundled/visualize/1.0.55/skills/visualize/SKILL.md) | Deferred progress communication to the host, clarified typography exceptions and extracted specialized layouts. |
| [presentations](/home/surajsinh/.codex/plugins/cache/openai-primary-runtime/presentations/26.1025.11240/skills/presentations/SKILL.md) | Replaced categorical style bans with contextual guidance and extracted writing examples. |
| [template-creator](/home/surajsinh/.codex/plugins/cache/openai-primary-runtime/template-creator/26.1025.11240/skills/template-creator/SKILL.md) | Supported sequential explicit batch updates and extracted the creation workflow. |
| [pdf](/home/surajsinh/.codex/plugins/cache/openai-primary-runtime/pdf/26.1025.11240/skills/pdf/SKILL.md) | Required explicit flattening intent, clarified runtime helper resolution and bounded repair handling. |
| [documents](/home/surajsinh/.codex/plugins/cache/openai-primary-runtime/documents/26.1025.11240/skills/documents/SKILL.md) | Preserved meaningful title punctuation/template styling; bounded repair attempts and moved equation implementation to a reference. |
| [spreadsheets](/home/surajsinh/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.1025.11240/skills/spreadsheets/SKILL.md) | Extracted shared guidance, allowed supported modern formulas and preserved requested output format. |
| [excel-live-control](/home/surajsinh/.codex/plugins/cache/openai-primary-runtime/spreadsheets/26.1025.11240/skills/excel-live-control/SKILL.md) | Shared workbook guidance and reused version-matched Office.js documentation without redundant reads. |
| [review-agent](/home/surajsinh/.codex/skills/.system/review-agent/SKILL.md) | Made committed-branch review compare against HEAD; uncommitted changes require the requested scope. |

## Backups and rollback

Original files and installation state: [20261027T152113Z-63ac26ad](/home/surajsinh/Desktop/pr-review/skill-fixes/backups/20261027T152113Z-63ac26ad/state.json). The state records which files were newly created and which were replaced. The installer preserves permissions, checks for concurrent edits, replaces files atomically and rolls back its own changes on a detected failure.

To verify the installed package:

```bash
python3 /home/surajsinh/Desktop/pr-review/skill-fixes/install_fixes.py --verify
```

To restore the pre-fix files:

```bash
python3 /home/surajsinh/Desktop/pr-review/skill-fixes/install_fixes.py --rollback '/home/surajsinh/Desktop/pr-review/skill-fixes/backups/20261027T152113Z-63ac26ad/state.json'
```

Applying or rolling back installed files requires write access outside this chat's default workspace sandbox. Rollback refuses to overwrite a file that has changed again since this installation.

[Complete patch](changes.diff), [manifest](manifest.json), [test results](validation.json), and [installer](install_fixes.py) are retained here. These are local edits to installed skills, including versioned plugin caches; an app or plugin update may replace them. Review any newer package before reapplying this patch. The current installer refuses mismatched file hashes instead of overwriting a newer version.
