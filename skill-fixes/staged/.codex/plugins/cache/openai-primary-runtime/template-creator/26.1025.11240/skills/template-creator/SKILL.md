---
name: template-creator
description: Create or update a reusable personal Codex artifact-template skill. Use when the user invokes $template-creator or asks in natural language to create a reusable template from a reference document, presentation, spreadsheet, Google Docs, Slides, or Sheets link, ImageGen or Product Design image, email, Slack message, or Site project, or explicitly asks to edit or update a passed artifact-template skill. Do not use for one-off creation from an existing template.
---

# Template Creator

Create or update a reference-backed template. Keep the source file, Site project, or a canonical Google Workspace URL and rendered reference image inside the skill so later use can reproduce its structure, voice, and visual system precisely.

## Routing

- Manage only personal skills under `${CODEX_HOME:-~/.codex}/skills`.
- Create a new template by default. Use a numbered skill name instead of overwriting an existing template.
- Update only explicitly identified artifact-template skills. For multiple targets, process each sequentially with its own validation and atomic update; never select a similarly named template. Report success or failure per target.
- Do not modify an installed or bundled plugin cache. If the passed template is plugin-backed, explain that this skill can update only a personal template.
- Do not create, modify, upload, or publish a plugin. If the request also asks to share the template with a workspace, explain that this skill only manages personal templates.
- A template exists only after `create-template-skill.mjs` succeeds. Never hand-author, rename, or copy a normal skill and report it as an artifact template.

## Create workflow

For a new template, read [creation and reference preparation](references/create-workflow.md) and follow the relevant artifact-type path. Metadata-only updates use the update workflow below without loading creation details.

## Update workflow

1. Resolve the exact passed artifact-template skill and read its `SKILL.md`, `artifact-template.json`, `agents/openai.yaml`, retained reference, and preview. Stop for any target that is not a direct child of the personal skills directory or is ambiguous. When several exact targets were supplied, run this workflow separately for each; do not apply one target's reference or metadata to another.
2. Preserve the skill folder name. For Sites, rebuild the entire template from the selected source; for other templates, preserve every file or behavior the user did not ask to change.
3. Apply the requested edit:
   - For reference content or visual changes, use the matching artifact, image, or text workflow to edit a temporary copy of the retained reference, render a new preview from it, and visually inspect the result. Never edit a linked Google Workspace source artifact; update its canonical URL and rendered reference image only when the user explicitly changes the template source.
   - For Site project changes, use the updated project directory as the reference without creating a preview.
   - For display-name or intended-use changes, preserve the current reference and, when applicable, preview unless the request also changes them. For Site metadata-only changes, use the existing template's `assets/source`, not the current project.
   - For instruction-only or other skill-owned text changes, edit only the requested files directly and keep the manifest and agent metadata consistent.
4. When the reference, preview, display name, or description changes, pass the existing kind and values for every unchanged field directly to the script. For an image template, also pass its existing `galleryKind` as `--gallery-kind`. For a Google Workspace template, pass its existing or explicitly updated `sourceUrl` as `--source-url`. For a Site template, pass the updated project directory or the existing template's `assets/source`, as selected above, as `--reference-path` without `--preview-path`. Do not create or edit a request file:

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --mode "update" \
  --skill-name "artifact-template-standup" \
  --kind "document" \
  --reference-path "/absolute/path/updated-reference.docx" \
  --preview-path "/absolute/path/updated-preview.png" \
  --display-name "Standup" \
  --description "Run a structured daily standup with updates, blockers, and owners."
```

5. The script validates the existing template kind, preserves additional skill-owned files, and replaces the package atomically without changing its skill name.
6. Verify every requested change in the target directory and confirm there are no staging or backup directories left behind.

## Response

After verification, replace the placeholders with the script result and respond with only the applicable content between the comment markers below. The markers delimit the response template; do not emit them. For templates other than Sites, also include the card directive:

<!-- TEMPLATE CREATOR RESPONSE START -->

Here’s your {displayName} template.

### How to find templates

Find it in the **Template Gallery** when @{kind} is added to the prompt.

### How to use a template

Tag ${skillName} and describe what you want to build.

::artifact-template{skill_name="{skillName}" skill_directory="{skillPath}" display_name="{displayName}" artifact_kind="{kind}"}

<!-- TEMPLATE CREATOR RESPONSE END -->

Formatting rules:

- Include the **How to find templates** section for document, presentation, spreadsheet, Google Workspace, and image templates. Omit its heading and sentence for email, Slack, and Site templates because their source plugins do not open the Template Gallery.
- Keep the paragraph wording and punctuation unchanged apart from replacing `{displayName}`, `{skillPath}`, `{skillName}`, and `{kind}`.
- For an image template, append `gallery_kind="{galleryKind}"` inside the artifact-template directive, using the exact `galleryKind` returned by the script. Omit `gallery_kind` for every non-image template.
- In the how to find template section, substitute @{kind} with the matching gallery-enabled mention: `@Documents`, `@Presentations`, `@Spreadsheets`, `$google-drive:google-docs`, `$google-drive:google-slides`, `$google-drive:google-sheets`, `$imagegen`, or `@Product Design`. `@Google Drive` also shows all three Google Workspace template kinds together. For image templates, use the generated template's exact `galleryKind`; never treat ImageGen and Product Design as interchangeable. Preserve the literal `@` or `$` so Codex renders an unquoted mention.
- Do not tell users to add `@Gmail`, `@Outlook Email`, or `@Slack` to open the Template Gallery. Email and Slack templates are used by tagging their saved template skill directly.
- In the usage sentence, preserve the literal `$` before the exact returned `skillName` so Codex renders an unquoted skill mention.
- For Site templates, omit the `::artifact-template` directive because the result-card renderer does not support `site`.
- Put the directive on its own line, using the exact returned `skillName`, `skillPath`, `displayName`, and lowercase `kind` values.
- Escape directive attribute values when needed so the directive remains valid.
- For a batch, repeat the applicable response block for each created or updated skill.

## Constraints

- Do not search for or fetch remote templates.
- Do not create or edit `request.json` or any other intermediary request file. Pass script inputs through command-line flags so Template creation never surfaces a code-file edit card.
- Do not delete or sanitize retained artifact-reference files; the user chose reference retention for fidelity. For Site projects, retain application source, project configuration, package-manager metadata, static assets, migrations, and logical D1/R2 bindings. Use the project's `.gitignore` to guide cleanup of the generated source, and exclude environment files, credentials, private keys, symlinks, dependencies, caches, build outputs, databases, and runtime or customer data without modifying the original project. Remove the original `project_id` from `.openai/hosting.json`.
- Treat every linked Google Workspace source artifact as read-only. Generated template skills must copy the complete native artifact before making changes.
- Generated Site templates must use the existing Sites workflow with `assets/source`; do not scaffold a new project over the retained source.
- Do not send an email or post a Slack message merely because a template was created or invoked.
- Do not create or mutate workspace plugins or marketplaces.
- Do not add Artifact.md package generation here. The artifact plugins own template distillation and creation.
- Do not modify global skill metadata or protocol files.
