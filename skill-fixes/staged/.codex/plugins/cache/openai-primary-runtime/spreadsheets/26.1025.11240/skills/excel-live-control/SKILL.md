---
name: "excel-live-control"
description: "Control an open or active Microsoft Excel workbook through the ChatGPT add-in or connected session. Use when the user tags the Microsoft Excel app in Codex or follows up on an established live Excel task. Do not use for standalone spreadsheet files or Google Sheets."
---

# Excel Live Control

Inspect, edit, analyze, format, and verify the workbook in the selected live Microsoft Excel session. Use connected-document tools for workbook reads and writes; use Computer Use only for application setup, target confirmation, and focus management.

On initial entry, complete the setup gates in order before session discovery. On follow-ups, reuse only the verified target and rediscover after workbook or add-in lifecycle changes.

Resolve every referenced file relative to this skill folder. Do not load the sibling artifact skill or its artifact-tool instructions while this live route is active.

## Important Instructions
- For new workbooks or authorized redesigns, plan the simplest correct workbook that meets the task, audience, actual data and domain. If formulas become hard to read, first reconsider whether the workbook’s structure, layout, or logic is overcomplicated before simplifying individual formulas. Remove unnecessary or duplicated logic while preserving calculation correctness, required business relationships, and financial reconciliation
- Instruction precedence for workbook content, layout, and formatting is: user request > reference/template > domain defaults/conventions > general defaults.

## Hard Routing Rules

Use this skill only when explicitly tagged or when the request clearly targets the Microsoft Excel desktop application, an open, active, or connected workbook in Excel Desktop, a selected range in Excel Desktop, the ChatGPT add-in for Excel, or a follow-up edit on the live-control path. For generic requests such as "create a spreadsheet," "create a workbook," or "create an Excel file" without explicit targeting of the Microsoft Excel desktop application or ChatGPT add-in, use the local workbook-authoring `Spreadsheets` skill instead. Stay on the live-control path unless the user explicitly switches targets; keep follow-up edits on the same path.

Routing selects the execution and delivery surface only; it does not override requested workbook content or a supplied reference/template.

Setup is part of the task. Use Computer Use only for setup checks and focus management, then use connected-document tools for workbook reads and writes. If a setup gate or required live capability is unavailable, stop and use the applicable exact guidance below. Do not silently switch to artifact authoring, open an unrelated workbook, or edit workbook cells through Computer Use.

Keep user-facing language to "Microsoft Excel", "ChatGPT add-in for Excel", "open workbook", "connected Excel session", or "live Excel control"; avoid internal connector/backend names.

## Setup State Machine

Complete these gates in order. A later gate cannot prove that an earlier gate passed.

Checklist: Excel app open -> intended workbook active and unambiguous -> ChatGPT add-in installed -> pane open -> signed in -> connected-document tools available -> target workbook registered.

### 1. Open Microsoft Excel And Establish The Target Workbook

Use Computer Use to inspect the Microsoft Excel application.

- If Microsoft Excel is installed but closed, open it.
- If Microsoft Excel is unavailable, use the exact **Excel unavailable** guidance below.
- If Excel shows its start screen or has no workbook open, open the workbook named by the user. If the user did not name an existing workbook, create a blank workbook.
- Wait until the workbook title, worksheet grid, and ribbon are visible. The Excel start screen is not a workbook.
- If several workbook windows are open, identify the intended workbook by title. Do not assume that the frontmost workbook is the target.
- If the request depends on the current selection, verify the selected sheet and range. If the selection is missing or ambiguous, ask the user to select it or provide an exact sheet and range.

### 2. Determine Whether The ChatGPT Add-in Is Installed

Inspect the Home ribbon only after a workbook grid is active.

- A visible `ChatGPT` button on the ribbon is positive evidence that the add-in is installed.
- If the button is absent, open **Home > Add-ins** and look for **ChatGPT** published by **OpenAI, LLC**. Do not infer that the add-in is missing only because its task pane is closed.
- If ChatGPT is not present in the ribbon or the installed add-ins list, treat the add-in as not installed.

For a missing add-in, give the user these exact choices:

1. Open the official Microsoft Marketplace listing: https://marketplace.microsoft.com/en-us/product/office/WA200010215
2. Or, in Excel, go to **Home > Add-ins**, search for **ChatGPT**, verify that the publisher is **OpenAI, LLC**, and choose **Add** or **Get it now**.
3. Return to the target workbook and open **ChatGPT** from the ribbon.

Installing an add-in is a user-controlled software-install action. Ask the user to complete the final install step, then resume inspection. If the Microsoft Marketplace or Office add-in store is blocked by organization policy, ask the user to contact their Microsoft 365 administrator. The official OpenAI setup and admin-deployment guidance is at https://help.openai.com/en/articles/20001063-chatgpt-for-excel/.

### 3. Open The ChatGPT Add-in Pane

If the add-in is installed but its pane is not visible, click **ChatGPT** on the Home ribbon. Allow a few seconds for the task pane to load, then inspect the pane again.

- A ribbon button without a visible task pane means installed but not open.
- A task pane titled **ChatGPT** means the add-in is open, but it does not by itself prove that the user is signed in.
- If Excel shows an add-in load or restart error, retry opening the pane once. If the same error returns, stop and tell the user what Excel displayed. For a recurring Windows SSO add-in error, direct the user to OpenAI Support as described in the official setup guidance.

### 4. Verify ChatGPT Sign-in

Inspect the contents of the open task pane.

- A normal chat surface such as **New chat** with the composer text **Ask anything, @ for context** is positive evidence that the add-in is signed in.
- A **Sign in**, **Log in**, **Get started**, account-choice, or workspace-access screen means sign-in is incomplete.
- Do not infer sign-in from the ribbon button, the pane title, or a previously signed-in browser session.

If sign-in is incomplete, ask the user to take over and finish sign-in with the ChatGPT account and workspace they intend to use. The user must handle credentials, account choice, SSO, and MFA. If the workspace says the add-in is disabled, the user needs a ChatGPT workspace administrator to enable **ChatGPT for Excel and Sheets** in workspace permissions. Resume only after the normal chat composer is visible.

### 5. Verify Connected-Document Tool Availability

After Excel, the target workbook, the open add-in pane, and sign-in are all verified, check whether `list_document_sessions` is available in the current Codex thread.

- If the tool is unavailable, do not report that the workbook failed to register. The current Codex thread did not load the connected-document tool surface.
- Tell the user to confirm that the Spreadsheets plugin is installed or reinstalled, then start a new Codex thread and retry the Microsoft Excel request. A thread does not necessarily acquire newly installed plugin tools after it has started.

### 6. Verify Workbook Registration

Call `list_document_sessions(surface="excel")` only after the previous gates pass.

- If exactly one session matches the target workbook, select it.
- If several sessions match and the target is unclear, ask the user which workbook to use.
- If sessions exist only for other workbooks, do not send commands to them. Activate the intended workbook, open its ChatGPT pane, keep the pane visible, and retry discovery.
- If no Excel session exists, keep the target workbook active, select a cell in it, keep the signed-in ChatGPT pane open, wait briefly, and retry once.
- If no session appears, close and reopen the ChatGPT pane once, wait for the normal composer, and retry once.
- If the workbook still does not register, tell the user that Excel and the add-in are ready but Codex cannot see a connected session. Ask the user to reopen the target workbook or restart Excel, then reopen ChatGPT and sign in if prompted. Do not loop indefinitely.

Workbook registration is tied to the current workbook and add-in lifecycle. Rediscover sessions after the workbook is renamed or saved under a new name, after the add-in reloads, after Excel recovers or restarts, or when a previously working command reports a missing or stale session. Never reuse an `executor_session_id` merely because its workbook title looks similar.

### Exact User Guidance For Incomplete Gates

Use the smallest applicable message and wait for the user when their action is required:

- **Excel unavailable:** "I cannot find the Microsoft Excel desktop app. Install or make Microsoft Excel available, open it, and tell me to continue. I will not switch this request to another spreadsheet workflow unless you ask me to."
- **Target workbook unclear:** "Microsoft Excel has more than one workbook open, and I cannot safely identify the target. Tell me the workbook title to use, or bring that workbook to the front and tell me to continue."
- **Add-in missing:** "Microsoft Excel and the workbook are open, but ChatGPT for Excel is not installed. Install the OpenAI add-in from https://marketplace.microsoft.com/en-us/product/office/WA200010215, or use Home > Add-ins in Excel and search for ChatGPT by OpenAI, LLC. Open ChatGPT from the ribbon when installation finishes, then tell me to continue."
- **Installation blocked:** "Your organization is blocking the Microsoft Marketplace or the ChatGPT add-in. Ask your Microsoft 365 administrator to deploy ChatGPT for Excel using the admin guidance at https://help.openai.com/en/articles/20001063-chatgpt-for-excel/. After the add-in appears in Excel, open it and tell me to continue."
- **Pane closed:** "ChatGPT for Excel is installed, but its task pane is closed. Open ChatGPT from the Home ribbon and keep the pane visible, then tell me to continue."
- **Signed out:** "The ChatGPT pane is open, but sign-in is not complete. Please finish sign-in, account/workspace selection, and any MFA in the pane. When you see New chat and the Ask anything composer, tell me to continue."
- **Tools unavailable:** "Excel and ChatGPT for Excel are ready, but this Codex thread does not have the connected Excel tools. Reinstall or enable the Spreadsheets plugin if needed, then start a new Codex thread and retry this request."
- **Wrong workbook registered:** "Codex can see an Excel workbook, but it is not the workbook you asked me to use. Activate the target workbook, open its ChatGPT pane, and tell me to retry. I will not send commands to the other workbook."
- **Workbook not registered:** "Excel and the signed-in ChatGPT pane are ready, but Codex cannot see this workbook yet. Keep the target workbook active, reopen the ChatGPT pane, and tell me to retry. If it still does not connect, reopen the workbook or restart Excel and open ChatGPT again."

## Live Commands

Before live commands, fetch the selected session's tool schemas with `get_document_tool_schemas`, then call `execute_document_command` with the exact `executor_session_id`, schema-valid args, and a caller-stable `idempotency_key`. Treat advertised schemas as the live-control contract.

Default to direct live workbook tools when the selected session advertises them: `read_ranges`, `search_workbook`, `list_items`, `write_range`, `clear_range`, `update_sheet`, `update_workbook`, `copy_range_to`, `read_range_image`, `read_sheets_metadata`, `resize_range`, `update_sheet_view`, `format_range`, `chart`, `table`, and `pivot_table`. The session may also advertise `run_officejs`; use it only under the Office.js gate below.

### Live Workbook Quality Checklist

For generated workbooks, source-to-workbook conversions, analytical trackers, and substantial workbook edits, apply the shared workbook quality rules and live completion rules in this skill before final response.

Minimum live verification:

- Inspect key values and formulas after writes; resolve formula errors, blank outputs, broken references, and obvious mismatches with the requested logic.
- Follow `features/charts.md` for chart source and object verification. For tables and PivotTables, verify source ranges before creation and confirm the expected native objects with `list_items` when available.
- Use `read_range_image` for charts, dashboards, dense presentation tables, or substantial layout changes; fix blank charts, clipped headers or numbers, unreadable formatting, and obvious layout overflow.
- For long multi-sheet builds, verify and format each user-facing sheet before moving far ahead; do not defer all content checks and layout repair until the end.
- For dashboards, reports, scorecards, and trackers, apply the relevant layout and formatting guidance from `style_guidelines.md` and chart decision rules from `features/charts.md` when those files are required.
- Do not treat successful setup, a completed command, or a saved workbook as task completion until the workbook content has passed the relevant checks.

When the user expects a file from a live Excel session, save through the selected session only when an advertised command supports save or export behavior. If no such command is available, report that limitation and leave host-global save or recovery unchanged.

If the selected session does not advertise a tool needed for the request, follow the workbook-registration rediscovery rules once if the workbook or add-in changed. Otherwise report the missing live capability and wait for the user to repair setup or explicitly switch targets.

## Office.js Gate

Before the first `run_officejs` call, read `officejs.md` completely and follow its decision boundary and instructions. Reuse that guidance within this conversation while the package version and live capability schema remain unchanged. Re-read it after a relevant version/schema change or an error that shows the contract changed. The hard routing rules above continue to govern setup, Computer Use, and fallback behavior.

## Out Of Scope

Do not use live Excel control for Google Drive, Google Sheets, or other cloud spreadsheet connector requests.

Do not claim live control can install desktop apps, change OS or Excel settings, enable macros, use COM/win32com, run native print/PDF/export/page-setup workflows, bypass workbook protections, or perform commands not advertised by the selected session.

Treat spreadsheet-processing code questions as software implementation or debugging unless the user also asks to control a connected Excel session.

## Shared workbook guidance

For new models or changes to structure, formulas or authored content, read the relevant sections of [shared workbook quality](../spreadsheets/references/workbook-quality.md). It owns structure, formulas, missing-input behavior and writing guidance for both file authoring and live Excel. Read only the sections needed for the task; preserve unrelated content during narrow edits.

### Sensitivity analysis for this surface

- **Sensitivity analysis:** For requested one- or two-input sensitivity analyses, use native What-If Data Tables where supported when the alternative would duplicate complex model logic in the sensitivity grid. Simple, self-contained calculations may use ordinary formulas. For requested Excel financial-model sensitivities, default to native What-If Data Tables where supported; follow [Finance Guidance](domain_guidance/financial_models.md#valuation-and-returns) for model links and verification. Do not introduce `TABLE` into an ordinary forecast or case comparison, or manufacture a second varying input with a metric selector. Excel supports one or two varying inputs; use a native data table only when the selected Excel session advertises a supported command. Two inputs test one output across their combinations; use separate tables for additional outputs. If the requested native design is unsupported, explain the limitation before agreeing on a formula-based design or change-input/recalculate/restore process. Label captured results and their refresh method. Ordinary case comparisons follow the single-build and comparison boundary above.

## Workflows
Required:
- `workflows/edit_workflows.md` for existing files/follow-ups.
- `workflows/create_workflows.md` for new files

## Resources
Read the following BEFORE starting the task:

Required:
- `style_guidelines.md` for formatting.

As applicable:
- `officejs.md`: read completely before using `run_officejs`; do not read it for direct-tool-only work.
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
Use native Excel tools to verify requested features and results within the authorized changes and their affected dependencies. Match coverage to the scope, complexity and risk. Report unrelated pre-existing defects without repairing them and keep authoring-only tests out of the delivered workbook.

Use only tools advertised by the selected Excel session, with their advertised schemas.

1. Inspect key ranges:
- Read key values and formulas after writes with `read_ranges` or an advertised equivalent.
- Use workbook metadata, range reads, and object inspection to capture the pre-edit baseline and check for unintended changes across tabs.
- Confirm chart, table, and PivotTable objects and their source ranges with `list_items` and other advertised reads when available.

2. Scan formula errors:
- Use `search_workbook` or an advertised equivalent to locate `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A`, `#NUM!`, `#NULL!`, `#SPILL!`, and `#CALC!` errors.

3. Verify visual output with `read_range_image` or an advertised equivalent:
- For long multi-sheet builds, verify each user-facing sheet as it is built rather than deferring all checks until the end.
For creation or broad authorized restructuring, visually review every sheet. For a narrow edit, review the changed view and affected dependencies, then compare all tabs with the source for unintended value, formula, object, validation or style changes. Do not repeatedly render unchanged tabs; investigate any scope-preservation failure.

Inspect at normal zoom with cells unselected. Fix blank/broken charts, low-contrast text, unreadable fonts, clipped headers/numbers, `####`, awkward wrapping, truncated chart labels, default blank sheets and content outside the working area. Check effective cell/chart fonts, fitted row heights and widths, pane boundaries and conditional-format ranges. Logical titles and labels should appear once with a clear layout. Valid check values should stay neutral, with errors and missing inputs visibly distinct. Do not shrink content to force a fit.

4. Keep verification compact:
- Use native Excel tools to verify requested features and results, reusing checks for unchanged content.
- Successful setup or a completed command does not prove that the requested workbook content is correct. Apply the shared checks to the connected workbook itself.
- Avoid arbitrary formula count checks, assumptions about file storage, and huge diagnostic dumps.

5. Finalize when the connected workbook passes the checks above.
- Follow this skill's setup and missing-capability rules if a required live check is unavailable. Do not substitute Artifact Tool or require a local workbook export to verify a live edit.

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

## Completion

- Complete a live edit only after the connected workbook contains the requested changes, key values and formulas have been inspected, and native objects have been confirmed when relevant.
- Use `read_range_image` or the advertised equivalent for charts, dashboards, dense presentation tables, or substantial layout changes. Fix material clipping, overlap, blank charts, unreadable formatting, and visible formula errors before finishing.
- Do not require a local `.xlsx` export unless the user explicitly requests one and the selected session advertises a supported save or export command.
- For question-only requests, answer from the connected workbook context without editing unless the user asks for a change.
- If setup or a required live capability is blocked, use the smallest applicable user guidance from this skill and wait. Do not silently switch to artifact authoring.

## Error Recovery
On first tool or API error:
1. Read error text.
2. Consult the selected workflow's targeted help or schema discovery only if needed.
3. Retry with minimal patch (not full rewrite).
4. Continue from existing workbook state.

Do not loop indefinitely on similar failures.



## Comment Author
- If the authenticated profile provides a display name, use it as the threaded-comment author unless the user requests another name. Default to `User`.

## Source, PDF, and Attachment Processing
- For attachment references, include only the file/section/table details needed to locate supporting data. Do not paste large PDF excerpts unless requested.
- Use bundled extraction libraries only for supporting analysis. Keep auditable and user-editable calculations in workbook formulas, then write results through the connected Excel session.
