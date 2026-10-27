Resource paths in this reference are relative to the parent skill directory unless a link specifies otherwise.

## Create workflow

1. Require exactly one supported reference unless the user explicitly requests a batch. For a batch, complete this workflow separately for every reference:
   - Document: `.docx`
   - Presentation: `.pptx`
   - Spreadsheet: `.xlsx`
   - Google Workspace: one Google Docs, Google Slides, or Google Sheets URL
   - ImageGen or Product Design image: `.png`
   - Email or Slack message: `.txt`
   - Site: an existing Site project directory
   - When email or Slack content is pasted rather than attached, materialize the exact content as a temporary UTF-8 `reference.txt` without rewriting it.
2. Infer a concise display name and intended-use description from the reference and request. Infer document, presentation, spreadsheet, and image from the file extension. For a Site project directory, use `site`. Infer `google-docs`, `google-slides`, or `google-sheets` from the supplied Workspace URL; for a generic Drive share URL, use Google Drive metadata to identify the native file type and resolve its canonical `docs.google.com` URL. Ask only when the link is inaccessible or does not identify a supported native Workspace artifact. For an image, set its gallery kind to `product-design` when the request includes `@Product Design`; otherwise default to `imagegen`, including when the user provides only the image and this skill. Ask only when the request explicitly includes both Product Design and ImageGen and the intended target remains unclear. For `.txt`, determine whether the user requested `email` or `slack`; ask if the intended type is ambiguous.
3. For references other than Site projects, create `preview.png` before packaging:
   - DOCX: use Documents to render the reference and copy its first page PNG.
   - PPTX: use Presentations to render the reference and copy its first slide PNG.
   - XLSX: use Spreadsheets to render the used range of the first visible non-empty sheet.
   - Google Workspace: load the `google-drive` skill and the matching `google-docs`, `google-slides`, or `google-sheets` skill from [@Google Drive](plugin://google-drive@openai-curated-remote), inspect the native artifact, and use the file bridge below. Then:
     - Google Docs: export to PDF and render its first content page to `reference.png`. Normally this is PDF page 1. For a tabbed Doc, Google may prepend one or more synthetic pages that contain only a tab title; skip only those consecutive tab-title separator pages and use the first page containing the first tab's actual document body. Treat that page as the artifact's first page rather than as a later-page substitution. Do not skip a real content page merely to choose a more attractive preview, and stop if the export contains no representative content page.
     - Google Slides: export to PDF and render only its first slide to `reference.png`.
     - Google Sheets: identify the first visible non-empty sheet, export to XLSX, and use Spreadsheets to render that sheet's used range to `reference.png`.
   - PNG: copy the reference PNG unchanged.
   - Email or Slack: render a legible representative portion of the exact reference text on a neutral canvas. Do not paraphrase, decorate, or invent content.
   - For a Google Workspace template, copy the checked `reference.png` unchanged to `preview.png`.
   - A Google Workspace URL is sufficient to activate the Google Drive workflow; do not require the user to add @Google Drive. Before entering `functions.exec`, check whether the Google Drive `fetch` tool is callable. If it is not, use `tool_search` once to find and load the Google Drive action that fetches a native Google Doc, Sheet, or Slides file with raw-file download support, then check the callable tools again. Do not run the file bridge until `fetch` is loaded, and do not report that it is unavailable before this discovery attempt has failed or returned no matching action.
   - For every Google Workspace export, use the connected Google Drive `fetch` tool with `download_raw_file` and `raw_export_mime_type`. Do not download through the in-app browser, open a Google `/export` URL, follow a `googleusercontent.com` download redirect, use a shell HTTP client, or request browser download permission. Browser inspection does not substitute for connector export. If `fetch` is unavailable, the Drive connection lacks access, or the connector does not return the requested file, stop and explain the connector requirement instead of falling back to a browser download.

   Load the workspace dependencies and use the checked-in file bridge for Google Docs and Slides PDF exports and Google Sheets XLSX exports. Run this inside one `functions.exec` call. The bridge resolves the Google Drive `fetch` action, requests an authenticated raw export, validates the returned base64 file, and writes it inside the task workspace without exposing it to a shell argument or browser download:

```js
const SKILL_DIR = "<absolute-template-creator-skill-directory>";
const WORKSPACE = "<absolute-task-workspace>";
const NODE_BIN = "<absolute-node-path-from-workspace-dependency-loader>";
const usesPowerShell = /^(?:[A-Za-z]:[\\/]|\\\\)/.test(SKILL_DIR);
const loadCommand = usesPowerShell
  ? "Get-Content -Raw -LiteralPath '.\\host\\export-google-workspace-file.mjs'"
  : "/bin/cat -- ./host/export-google-workspace-file.mjs";
const loaded = await tools.exec_command({
  cmd: loadCommand,
  shell: usesPowerShell ? "powershell.exe" : "/bin/sh",
  workdir: SKILL_DIR,
  login: false,
  yield_time_ms: 30000,
  max_output_tokens: 30000,
});
if (loaded.exit_code !== 0)
  throw new Error("Could not load the Google Workspace exporter");
const exportGoogleWorkspaceFile = new Function(
  `${loaded.output}\nreturn exportGoogleWorkspaceFile;`,
)();
const result = await exportGoogleWorkspaceFile({
  sourceUrl: "<canonical-google-workspace-url>",
  mimeType: "<application/pdf-or-xlsx-mime-type>",
  nodePath: NODE_BIN,
  receiverPath: `${SKILL_DIR}/host/google-workspace-export-stdin-receiver.mjs`,
  outputPath: `${WORKSPACE}/<reference.pdf-or-reference.xlsx>`,
  workspaceRoot: WORKSPACE,
  tools,
});
text(JSON.stringify(result));
```

Use the canonical `docs.google.com` URL, including any `resourcekey` query parameter required for link access. Use `application/pdf` and an output ending in `.pdf` for Google Docs and Slides. Use `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` and an output ending in `.xlsx` for Google Sheets. Do not manually copy base64 export content into a command or file-editing tool.

4. Visually inspect the PNG when one was created. Stop if it is blank, clipped, corrupted, or not representative of the reference. Site templates use a bundled generic Sites PNG preview and do not require a screenshot.
5. Do not create an intermediary request file or use a file-editing tool for script inputs. Set `SKILL_DIR` to the directory containing the parent `SKILL.md` (one directory above this reference), load the workspace dependency runtime, and pass the values directly. Before substituting real values into the command, shell-escape each value as one argument for the active shell. Never interpolate a raw path, display name, description, or skill name.

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --reference-path "/absolute/path/reference.docx" \
  --preview-path "/absolute/path/preview.png" \
  --display-name "Standup" \
  --description "Run a structured daily standup with updates, blockers, and owners."
```

Use the Node path returned by the dependency loader for `NODE_BIN`. Do not use a system Node installation.

Pass `--kind "image"` and `--gallery-kind "imagegen"` or `--gallery-kind "product-design"` for image templates. Pass `--kind "email"` or `--kind "slack"` for text templates, and `--kind "site"` for Site project directories. The script can infer the three Office kinds and image from their extensions, but Template Creator must pass the image gallery kind explicitly so ImageGen and Product Design templates remain separate. `.txt` always requires `--kind "email"` or `--kind "slack"`. Site templates never require `--preview-path`.

For a Google Workspace template, pass its exact kind, resolved `docs.google.com` link as `--source-url`, and the rendered PNG as both the reference and preview inputs. The script validates that the link matches the requested kind and stores a canonical file URL without account-routing or deep-link parameters while preserving a `resourcekey` required for link-based access.

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --kind "google-docs" \
  --source-url "https://docs.google.com/document/d/example/edit?usp=sharing" \
  --reference-path "/absolute/path/reference.png" \
  --preview-path "/absolute/path/reference.png" \
  --display-name "Project Brief" \
  --description "Create project briefs with this Google Doc's native structure and visual system."
```

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --kind "image" \
  --gallery-kind "product-design" \
  --reference-path "/absolute/path/reference.png" \
  --preview-path "/absolute/path/preview.png" \
  --display-name "Launch Visual" \
  --description "Create launch visuals with this product-design direction."
```

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --kind "email" \
  --reference-path "/absolute/path/reference.txt" \
  --preview-path "/absolute/path/preview.png" \
  --display-name "Launch Email" \
  --description "Draft launch emails with this structure, voice, and call to action."
```

```bash
"$NODE_BIN" "$SKILL_DIR/scripts/create-template-skill.mjs" \
  --kind "site" \
  --reference-path "/absolute/path/existing-site" \
  --display-name "Marketing Site" \
  --description "Create a marketing site with this layout and component system."
```

6. Read the JSON result. Verify that `skillName` begins with `artifact-template-` and that the generated directory contains `SKILL.md`, `artifact-template.json`, `agents/openai.yaml`, and `assets/preview.png`. For Site templates, verify that the project is retained in `assets/source` with the generic Sites preview. Read the original project's `.gitignore` when present, inspect `assets/source`, and remove ignored files, project-specific credentials, customer exports, runtime data, generated archives, and unnecessary large files from the generated copy without modifying the original project before reporting success. For all other templates, verify the retained canonical `assets/reference.<ext>`. For a Google Workspace template, also verify that the manifest contains the canonical `sourceUrl` and `assets/reference.png`. If any check fails, do not claim the template was created or emit an artifact-template card.

