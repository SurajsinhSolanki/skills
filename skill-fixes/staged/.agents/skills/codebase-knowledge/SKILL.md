---
name: codebase-knowledge
description: Generate, update, validate, and visualize a `knowledge/` folder that documents an entire codebase as a conformant Open Knowledge Format (OKF v0.1) bundle — for humans, LLMs, and coding agents.
license: MIT
metadata:
  required_resources:
    - references/knowledge-spec.md
    - scripts/quick_validate.py
    - scripts/visualize.py
---

# Codebase Knowledge

Generate and maintain a structured `knowledge/` folder that documents a codebase in an evidence-backed format conformant with the **Open Knowledge Format (OKF) v0.1** — a vendor-neutral spec for representing knowledge as plain markdown files with YAML frontmatter. The output is a real OKF bundle: readable with `cat`, shippable with `git clone`, consumable by any OKF-aware agent, and still human-friendly.

This skill supports four workflows. Identify which one applies, then follow it.

## Choose the workflow

1. **Generate** — no `knowledge/` folder exists yet, or the user wants a fresh full build. → See "Generate" below.
2. **Update** — `knowledge/` already exists and code and/or requirements changed. → See "Update" below.
3. **Validate** — check an existing `knowledge/` for OKF conformance, broken links, missing coverage, or stale docs without regenerating. → See "Validate" below.
4. **Visualize** — render an existing `knowledge/` bundle as a static, self-contained HTML graph. → See "Visualize" below.

If unsure which the user wants, check whether `knowledge/` exists. If it does and they mention changes, default to Update.

## Universal rules (apply to all workflows)

These govern every file produced. The full content spec, OKF frontmatter schema, and directory layout live in `references/knowledge-spec.md` — read it before generating or updating any documentation file.

- **Never hallucinate.** If something cannot be determined from source, write exactly: `> Unknown from source code.`
- **Never modify application code**, rename files, or alter project structure. Only write inside `knowledge/`.
- **Cite evidence.** Every non-trivial claim is backed by a numbered `# Citations` list pointing at source files (and symbol/lines when available) — see the Citations format in `references/knowledge-spec.md`.
- **Respect scope.** Ignore `node_modules/`, `dist/`, `build/`, `coverage/`, `.git/`, `.next/`, `out/`, `target/`, `vendor/`, `logs/`, `tmp/`, `.cache/`, and generated code. Read lockfiles only for dependency versions.
- **Be concise and non-redundant.** One concept = one canonical document; link instead of repeating.
- **OKF frontmatter on every concept document.** Every non-reserved `.md` begins with the YAML block defined in `references/knowledge-spec.md`. The `type` field is the only OKF-mandated key and must never be empty; `title`, `description`, `resource`, `tags`, `timestamp` are the recommended OKF keys and are always filled in; `confidence`, `generated_from`, and `version` are this skill's custom extensions — OKF requires consumers to tolerate and preserve unknown keys, so these are safe additions.
- **`index.md` and `log.md` are reserved.** Never put concept content or frontmatter in them — they follow the fixed forms in `references/knowledge-spec.md`.
- **Hedge unprovable claims.** Never assert code is unused or dead; describe it as a candidate with `confidence: Low`.

---

## Workflow: Generate

Run two phases in a single execution — do not pause between them.

**Phase 1 — Inventory.** Survey the repo (respecting scope) and write `knowledge/project_inventory.md`: languages, frameworks, dependencies + versions, modules, database tables, APIs, background/cron jobs, event systems, environment variables, integrations, Docker services, CI/CD workflows. This inventory is the authoritative checklist for Phase 2.

**Phase 2 — Document.** Using the inventory as a coverage checklist, generate the full `knowledge/` tree as a conformant OKF bundle. The exact folder structure, per-file content requirements, OKF frontmatter schema, citation format, Mermaid rules, and cross-linking rules are all in `references/knowledge-spec.md` — follow it precisely. Every subdirectory gets an `index.md` (no frontmatter, per OKF); the bundle root gets `index.md` and `log.md`.

For very large monorepos that exceed the context window: process one package/service at a time, merge inventories into one `project_inventory.md`, generate incrementally, and preserve cross-links between packages.

Record the run in `knowledge/log.md` (see log format in the spec).

After generating, run the **Validate** workflow before finishing.

---

## Workflow: Update

Use when `knowledge/` exists and code or requirements changed. The goal is a surgical refresh, not a full rebuild — this preserves human edits and saves time.

1. **Refresh the inventory in memory.** Re-run Phase 1 without overwriting the existing inventory, then diff the proposed inventory against it. Apply the human-edit protection below before writing it. Note added, removed, and changed items.
2. **Determine what changed.** Compare the current SHA-256 of each `generated_from` source with its recorded source hash in `knowledge/.generation-manifest.json`; directories use a sorted map of in-scope file paths and their hashes. Use Git revisions as supporting evidence when useful. Timestamps are informational, not proof of freshness. A doc is stale if any of its source files changed, or if the inventory diff added/removed something it covers. If the user describes a requirements change (not just code), also update affected `business/rules.md` and any module/API docs that encode those rules.
3. **Regenerate only stale docs.** For each stale file, first apply the human-edit protection in the next step. Regenerate only eligible or explicitly authorized files per `references/knowledge-spec.md`, bump `version`, and set `timestamp` to now (ISO 8601).
4. **Preserve human edits.** Before replacing an existing file, verify both its `<!-- AUTO-GENERATED -->` first body line and its exact-byte SHA-256 against the prior generated output recorded in `knowledge/.generation-manifest.json`. A marker alone does not protect later human edits. If the hash differs or no baseline exists, preserve the file and report a proposed refresh; replace it only when the user explicitly authorizes that file or a full rebuild. Apply this protection to the inventory, indexes and log as well as concept documents; preserve existing log entries when appending a run.
5. **Handle additions and removals.** Create docs for new inventory items (full OKF frontmatter, linked from the nearest `index.md`). For removed items, do not delete the doc automatically — mark it with a `> Status: source removed` note and flag it in the summary, unless the user asked to prune.
6. **Update cross-links and indexes.** Ensure new docs are linked from their directory's `index.md`, and the root `index.md` completeness checklist reflects reality.
7. **Record the run** in `knowledge/log.md`: prepend a new dated entry (newest first) summarizing what was regenerated, preserved, and flagged.

Then run the **Validate** workflow.

---

## Workflow: Validate

Check the integrity and OKF conformance of an existing `knowledge/` without regenerating content. Report results; fix only what the user approves (or auto-fix if they asked). Run `python3 <skill-directory>/scripts/quick_validate.py --bundle <knowledge-directory>` first, then do the semantic checks below by hand. The script is read-only; its separate `<skill-directory>` positional mode checks this skill package. Use an available Python runtime with PyYAML; report the missing dependency without claiming validation succeeded.

Verify:

- **OKF conformance:** every non-reserved `.md` has parseable YAML frontmatter with a non-empty `type` field (spec conformance rule); `index.md` files carry no frontmatter; `log.md` uses ISO 8601 date headings, newest first.
- Every internal Markdown link resolves to a file that exists (broken links are tolerated by the OKF spec itself, but still worth flagging to the user).
- Every file cited in a `# Citations` block or listed in `generated_from` exists in the repo.
- Every Mermaid diagram is syntactically valid.
- Every item in `project_inventory.md` has a corresponding document (coverage).
- No two documents describe the same concept (no duplication).
- Check source freshness against recorded source hashes. If no source baseline exists, report freshness as unverified; copied files and Git checkouts can have misleading modification times.

Produce a short report grouped by issue type. Validation alone must not modify the checklist, log, manifest, or any other file. During an authorized Generate or Update run, refresh the completeness checklist only after applying the same human-edit protection used for other existing files.

---

## Workflow: Visualize

Render an existing `knowledge/` OKF bundle as a static, self-contained HTML graph — no backend, no build step, opens directly in a browser.

1. Run `scripts/visualize.py knowledge/` (or the path to the bundle) to produce `knowledge/visualization.html`.
2. The script walks the bundle, parses every document's frontmatter (`type`, `title`) and every markdown cross-link, and emits one self-contained HTML file: nodes are documents (colored/grouped by `type`), edges are cross-links, with pan/zoom and a search box. No external assets, no CDN — it must work fully offline.
3. If the bundle has changed since the last visualization, regenerate it; do not hand-edit `visualization.html`.
4. Report the output path to the user; do not attempt to open a browser yourself unless asked.

---

## Completion summary

End every run (generate, update, or visualize) with a concise summary — do not dump file contents to the terminal:

- Files generated (and preserved/flagged, for updates)
- Counts: modules, APIs, database entities, integrations documented
- Validation result: pass, or list of unresolved issues
- Any unknowns or low-confidence areas worth human review

## Reference files

- `references/knowledge-spec.md` — the complete specification: OKF-conformant folder tree, per-file content requirements, frontmatter schema (OKF-mandated vs. this skill's extensions), confidence scale, citation format, business-rule format, ADR format, Mermaid rules, cross-linking, `index.md`/`log.md` formats, and the index completeness checklist. **Read this before generating or updating any documentation file.**
- `scripts/quick_validate.py` — automates the mechanical OKF conformance checks (frontmatter presence, `type` non-empty, reserved-filename rules, YAML validity).
- `scripts/visualize.py` — generates the self-contained HTML graph view of a bundle.

## Generation manifest

After an authorized Generate or Update write, maintain `knowledge/.generation-manifest.json` using the contract in `references/knowledge-spec.md`. Record exact output hashes and in-scope source hashes only for content actually generated or refreshed. Do not adopt an existing human-edited file as generated merely to make its hash match. A missing or conflicting baseline requires preservation, not overwrite. Resolve script paths from this skill directory, not the repository working directory.
