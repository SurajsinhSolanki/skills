---
name: "Spreadsheets"
description: "Use skill when user requests to create, modify, analyze, visualize, or work with spreadsheet files (`.xlsx`, `.xls`, `.csv`, `.tsv`) or Google Sheets with formulas, formatting, charts, tables, and recalculation. Do not use for live controlling Microsoft Excel app or a live Excel session."
---

# Spreadsheets skill
Read this entrypoint for routing and completion. Load the linked modeling, style, API and workflow references only as needed for the requested task.

## Decision Boundary
- Google Sheets targeted outputs also require `routing/google_sheets.md`. Otherwise, author local files with artifact tool.

## Important Instructions
- For new workbooks or authorized redesigns, plan the simplest correct workbook that meets the task, audience, actual data and domain. If formulas become hard to read, first reconsider whether the workbook’s structure, layout, or logic is overcomplicated before simplifying individual formulas. Remove unnecessary or duplicated logic while preserving calculation correctness, required business relationships, and financial reconciliation
- Instruction precedence for workbook content, layout, and formatting is: user request > reference/template > domain defaults/conventions > general defaults.

## Tools + Contract Requirements
- Author the spreadsheet with `@oai/artifact-tool` JS and only `load_workspace_dependencies` executables/dependencies, never repo-local deps. If unavailable, check `~/.cache/codex-runtimes/codex-primary-runtime/dependencies/`. Never modify dependency directories.
- In a writable, conversation-specific or tmp directory, create a `node_modules` symlink or Windows junction to the loader `node_modules`.
- Prefer to patch/rerun one `.mjs` builder. No heredocs or duplicate builders.
- Use the provided API reference for supported syntax. Its examples do not set workbook structure, formatting or formula defaults. Do not inspect package internals or prototypes. If blocked, run at most one targeted `workbook.help("<api_or_feature>")` query.
- No `openpyxl`, `xlsxwriter`, or `pandas.ExcelWriter` authoring unless asked, or  `@oai/artifact-tool` is unavailable.
- Analyze with JS/formulas, else bundled Python (libraries) and JSON/CSV intermediates; other libraries only for missing capabilities.
- Use `update_plan` for complex work.
- In your final response, omit builders, previews, or other support files unless requested.
- Immediately before the first create/edit authoring command, run `mark_artifact_operation_started.mjs` successfully exactly once using the command below. Do not run it for read-only work. For edits, replace `create` with `edit`; adjust the expected count and output format to match the requested outputs.
  ```bash
  node container_tools/mark_artifact_operation_started.mjs --operation-kind create --expected-output-count 1 --output-format xlsx
  ```

## Shared workbook guidance

For new models or changes to structure, formulas or authored content, read the relevant sections of [shared workbook quality](references/workbook-quality.md). It owns structure, formulas, missing-input behavior and writing guidance for both file authoring and live Excel. Read only the sections needed for the task; preserve unrelated content during narrow edits.

### Sensitivity analysis for this surface

- **Sensitivity analysis:** For requested one- or two-input sensitivity analyses, use native What-If Data Tables where supported when the alternative would duplicate complex model logic in the sensitivity grid. Simple, self-contained calculations may use ordinary formulas. For requested Excel financial-model sensitivities, default to native What-If Data Tables where supported; follow [Finance Guidance](domain_guidance/financial_models.md#valuation-and-returns) for model links and verification. Do not introduce `TABLE` into an ordinary forecast or case comparison, or manufacture a second varying input with a metric selector. Excel supports one or two varying inputs; the current Artifact Tool supports only two-variable tables, with both input cells on the table’s worksheet. Read [Data Tables](artifact_tool_docs/DATA_TABLES.md) before creating one. Two inputs test one output across their combinations; use separate tables for additional outputs. If the requested native design is unsupported, explain the limitation before agreeing on a formula-based design or change-input/recalculate/restore process. Label captured results and their refresh method. Ordinary case comparisons follow the single-build and comparison boundary above.

## Workflows
Required:
- `workflows/edit_workflows.md` for existing files/follow-ups.
- `workflows/create_workflows.md` for new files

## Resources
Read the following BEFORE starting the task:

Required:
- `artifact_tool_docs/API_QUICK_START.md` for `artifact_tool` JS API documentation. Read entirely.
- `style_guidelines.md` for formatting.

As applicable:
- `references/template-elicitation.md`: if user has not provided a template, reference, or visual direction.
- `references/image-references.md`: if a reference image or screenshot is provided.
- `references/read_only_qna.md`: for Q&/audits
- `features/charts.md`: for creating or editing charts.

<a id="domain-requirements"></a>

## Role and Domain Guidance
Before authoring, identify the user's **task/function**, **role**, **audience** and **industry** separately, then read the relevant guides below. Apply the professional conventions of the work being done; a role or industry label alone does not determine the workbook's structure or formatting.
- Use function guidance for the work being done. Financial forecasts, budgets, cash models and valuations use Finance guidance in any industry.
- Add industry requirements only when they affect definitions, units, source handling or the workflow. A healthcare company's financial forecast uses Finance guidance; an appointment tracker does not inherit financial-model structure or colors.
- Use the user's role and audience to choose useful detail, terminology and outputs, and to resolve ambiguity in the task. Do not apply Finance conventions to an unrelated task just because the user works in Finance. Explicit instructions and templates retain precedence; relevant domain conventions override generic defaults.

Guides:
- Finance, corporate finance and FP&A, financial modeling, valuation and investment banking: `domain_guidance/financial_models.md`. Read the relevant financial requirements below the shared structure, formula and style rules.
- Healthcare: `domain_guidance/healthcare.md`
- Marketing and advertising: `domain_guidance/marketing_advertising.md`
- Scientific research: `domain_guidance/scientific_research.md`

## Create and Edits
For any task that requires modifying or creating a workbook:

### Data Formatting Rules
- Store numbers, percentages, currency, and dates as typed spreadsheet values, not preformatted strings. Use text only for true identifiers such as ZIP codes, account IDs, SKUs, or labels.
- Use Excel-invariant number/date format codes, not locale-specific display strings. Generic numeric examples include `#,##0`, `#,##0.0`, `0.0%`, `0.00%`, `"$"#,##0`, `"$"#,##0.00`. Preserve source dates and unrelated existing formats.
- Percentages: Follow the domain or reference's precision. Otherwise, use 1 decimal for most analytical cells, 0 decimals for dashboard outputs, and 2 decimals where small rate differences matter.
- Do not swap `.` and `,` in format codes to mimic locale separators; separators are controlled by spreadsheet/render locale. Use `0.0%`, not `0,0%`, and `#,##0`, not `#.##0`.
- Choose the appropriate format for readability. Match precision to meaning: counts use `#,##0`; rates usually use `0.0%` or `0.00%`; currency uses whole units unless cents matter.

- For dates in data columns, default to a short date format appropriate to the workbook's language/location, such as `mm/dd/yy` for the US. Follow explicit user preferences and reference/template or domain conventions.

Keep underlying dates numeric and sortable. A display format does not change the period represented or authorize aggregation. Fit the final display so dates do not truncate or show `####`.

### Verification Rules
Use Artifact Tool to verify requested features and results within the authorized changes and their affected dependencies. Match coverage to the scope, complexity and risk. Report unrelated pre-existing defects without repairing them. Reuse checks for unchanged content and keep authoring-only tests out of the delivered workbook.

After completing all edits, call `workbook.recalculate()` once before the final checks below and export. If you make further edits, recalculate again before repeating affected checks and exporting.
```js
workbook.recalculate();
```

1. Inspect labels, values and formulas in key ranges:
```js
const check = await workbook.inspect({
  kind: "table",
  range: "Dashboard!A1:H20",
  include: "values,formulas",
  tableMaxRows: 20,
  tableMaxCols: 12,
});
console.log(check.ndjson);
```

Check what each source row represents, units, reporting periods, and numerators and denominators for rates. Spot-check representative metrics against source data or an independent calculation. Trace headline results through the build to inputs, including named and dynamic references. Confirm the build does useful calculations and does not depend on terminal Checks/Audit. When cases are used, trace each period to its active assumptions. Summary should link to finished results without repeating the build or routing results through Assumptions. An actuals-only historical calibration reference is allowed.

Check formula copying across and down at first, middle and later rows/periods. When the workflow promises extensions, test the next record, period or requested case. Keep notes and overrides tied to stable record IDs after supported sorts or refreshes. Reconcile key totals to independent source controls using the right period aggregation. Apply tolerances appropriate to the units and precision, but compare identifiers, counts and categories exactly. Investigate double-counting or conflicting data and fix confirmed errors within scope.

2. Scan formula errors:
```js
const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);
```

Check wrong or shifted references and unintended cycles as well as reported errors. Distinguish deliberate missing-data markers from unexpected failures. Trace unavailable results and zero issue counts through their prerequisites: a failed detail calculation must not disappear into a healthy zero or an understated summary.

3. Verify applicable recalculation in the intended engine. Test representative input changes and boundaries in a disposable copy or restore every temporary edit before delivery. Include blank versus zero, missing/duplicate keys, period cutoffs, overrides and rounding. For cases, change the selector and a later-period driver. Confirm the same build and linked outputs update while actuals remain unchanged. A blank unselected input must not block a valid active case; selecting that case must expose the missing input. Verify any agreed comparison refresh and stale-state behavior separately. Report any engine checks that could not be performed.

For workflows, check that required human inputs have editable fields and that completion guidance accounts for every prerequisite. Complete one prerequisite while leaving another open and confirm the remaining action stays visible. For input-driven rankings and action lists, change an input that should alter the order or included records and verify the list updates. Verify affected charts, status text, validation and conditional formatting react to edits. A saved value, static matrix or unchanged PASS cell is not recalculation proof.

4. Render sheets/ranges to verify visual output. Skip only when the rendered view and its data/formula dependencies are unchanged:
```js
const blob = await workbook.render({ sheetName: "Sheet1", range: "A1:H20", scale: 2 });
```
For creation or broad authorized restructuring, visually review every sheet. For a narrow edit, review the changed view and affected dependencies, then compare all tabs with the source for unintended value, formula, object, validation or style changes. Do not repeatedly render unchanged tabs; investigate any scope-preservation failure.

Inspect at normal zoom with cells unselected. Fix blank/broken charts, low-contrast text, unreadable fonts, clipped headers/numbers, `####`, awkward wrapping, truncated chart labels, default blank sheets and content outside the working area. Check effective cell/chart fonts, fitted row heights and widths, pane boundaries and conditional-format ranges. Logical titles and labels should appear once with a clear layout. Valid check values should stay neutral, with errors and missing inputs visibly distinct. Do not shrink content to force a fit.

Keep output compact: avoid arbitrary formula-count checks, assumptions about file storage and huge NDJSON dumps.

5. Export:
```js
await fs.mkdir(outputDir, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${outputDir}/output.xlsx`);
```

6. Inspect the saved file when an affected feature or export concern requires it. Verify requested or preserved native features in the intended engine, including any explicitly required Data Table input/output behavior. Check iteration and capture behavior separately when used.

Finalize only after successful export and the applicable checks. Report what was performed and any remaining limitations. Formula text, a preview and a successful export do not establish native-application behavior.
- Do not export extra `.xlsx` variants unless asked.

### Citation Requirements
These are defaults for new workbooks: user instructions, reference/template conventions and domain guidance take precedence. For edits, follow the workbook’s existing citation practices.
- Cite real sources when they exist.
- Keep citations and sources in one place: an existing input tab (sources or data tab) or in the correct input section in a tab, alongside the input data.
- There are two ways to cite a source: 
  1. (Preferred) Inline in the input tab when the tab exists.
    - If there are multiple unique sources (different pages/lines don't count), inline them in an adjacent cell at the table's end, with one column as a buffer, when a table exists
    - If there is a single source, just have a single cell above the data, left aligned.
  2. (Fallback) Cell note, not a comment/thread, with the citation
    Only do this for hardcoded inputs not on a separate input tab, such as an input area on a build sheet. For adjacent cells in the same row or column that come from the same source, do not add duplicate cell notes. Never add citation notes to titles or headers.
- If there is no clear place for sources, return sources in chat. Do not add a tab just for citations.
- Citation format should follow best practice for domain, default to `(Source: Company 10-K, FY2026, Page 20, Revenue Note, [URL LINK])`
- Do not add citations, comments or notes to cover/presentation tabs or output regions unless requested. On a mixed-use sheet, citations may sit beside the input data, outside the output region.
- When comments are requested, keep them succinct, minimal and easy to read.
- Do not add a different annotation type to a cell that already has one. Update an existing note/comment/thread rather than layering another system over it.
- Do not add cell comments unless the user requests them. Preserve existing annotations.

## Completion Criteria
### Criteria for Question / Read only requests
- Answer from the available workbook context. Do not edit or overwrite unless the user asks for a workbook change.

### Criteria for all create and edit requests
Complete only when:
- Content is populated, addresses the user's request, and formulas compute, with no obvious formula errors in key scanned ranges (including bad-reference, off-by-one or circular errors).
- Deliverable is saved in the requested format and location. Default to `.xlsx` for a new workbook when no format is specified. Preserve requested CSV/TSV delimiters, quoting, encoding and values; these formats cannot retain multiple sheets, styles, charts or executable formulas. Explain a material format limitation and resolve it before discarding required features. A requested Google Sheets output follows its native routing contract.
- Visual verification passes: organized, legible layout matches requested style or default/existing edit baseline; all important numbers/callouts are visible; numbers, text, charts and content are unclipped without awkward wrapping.
- Required controls, charts, panes and requested features exist.

## Error Recovery
On first tool or API error:
1. Read error text.
2. Consult the selected workflow's targeted help or schema discovery only if needed.
3. Retry with minimal patch (not full rewrite).
4. Continue from existing workbook state.

Do not loop indefinitely on similar failures.

## Final response

### Final Response Citations

- **Create/edit:** for created or edited spreadsheets, cite each final deliverable exactly once with `purpose="output"`, in its own paragraph. Briefly describe the result without repeating its filename, path, or link. Never put output directives inside prose or list items.
- **Q&A and summaries:** Every file whose contents you summarize or use to support an answer MUST receive a `:codex-file-citation{...}` with `purpose="source"` in the final response. Use the source citation in place of the filename, wherever the filename would appear. Do not write the filename separately and append its citation at the end. Files merely inspected but not used in the answer need no citation. Do not emit output citations for unchanged files or read-only answers.

- Emit `:codex-file-citation{...}` directly, without backticks, code fences, or a Markdown-link wrapper. Use verified targets only. No need to cite or reference intermediate work.

For file citations, set `path` to the verified absolute file path on the task host. Omit `mode`.

Some illustrative examples, real responses use verified targets outside code fences.

```text
:codex-file-citation{path="/abs/path/book.xlsx" artifact_kind="workbook" purpose="output"}
```

```text
The review of :codex-file-citation{path="/abs/path/book.xlsx" artifact_kind="workbook" purpose="source"} is due Friday.
```

### Additional citation guidance


For substantive whole-workbook claims, use a plain source citation. Otherwise use the narrowest reliable `sheet` + `range`, including the exact cell for a discrete value. Cite discontiguous cells separately where they support the answer. For objects, use `sheet` + exact inspected `object_id`; add `object_kind`/`label` only when useful. Never cite a sheet alone or guess locators. Cite only distinct inputs, drivers, formulas, or results the answer needs.

```text
Revenue falls because the growth assumption is negative in :codex-file-citation{path="/abs/path/book.xlsx" purpose="source" artifact_kind="workbook" sheet="Revenue Model" range="C27"}.
```

- Calculations: cite only distinct inputs, drivers, formulas, or results the answer needs.



## Comment Author
- If the authenticated/user profile or env context provides a user display name, use it as the threaded comment display name unless the user requests another name. Default to `User`.

## Source, PDF, and Attachment Processing
- For attachment references, include only the file/section/table details needed to locate supporting data. Do not paste large PDF excerpts unless requested.
- Bundled Python libraries available in the bundled runtime environment for extraction/analysis include `pandas`, `numpy`, `pypdf`, `python-docx`, and `reportlab`. You may read/extract in separate scripts if needed.
- Bundled JS libraries available for document/PDF work include `docx`, `pdf-lib`, and `pdfjs-dist`.

## Runtime helper resolution

Resolve host-specific `container_tools/` helpers from the authoritative workspace dependency/runtime base and invoke their absolute paths. Do not assume the task checkout contains them. If a host does not supply a marker helper, report that host capability limit and use its supported authoring contract instead of inventing a helper or claiming it ran.
