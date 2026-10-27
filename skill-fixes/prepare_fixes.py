from pathlib import Path
import json,re,shutil,hashlib
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text())
by={Path(x['target']).parent.name:x for x in manifest}
notes={}
def read(n):return Path(by[n]['staged']).read_text()
def write(n,s):Path(by[n]['staged']).write_text(s)
def edit(n,a,b):
 s=read(n)
 if a not in s:raise ValueError(f'Expected text missing in {n}: {a[:90]}')
 write(n,s.replace(a,b));notes.setdefault(n,[]).append(b[:110])
def addfile(target,content):
 target=Path(target);stage=ROOT/'staged'/target.relative_to('/home/surajsinh');stage.parent.mkdir(parents=True,exist_ok=True);stage.write_text(content)
 existing=next((x for x in manifest if x['target']==str(target)),None)
 if not existing:
  manifest.append({'target':str(target),'staged':str(stage),'before_sha256':hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None})
 return stage
def extra(n,rel,content):return addfile(Path(by[n]['target']).parent/rel,content)
def append(n,s):write(n,read(n).rstrip()+'\n\n'+s.rstrip()+'\n')

# Restore the original, revision-matched package resources.
up=Path('/tmp/codebase-knowledge-upstream')
for rel in ['references/knowledge-spec.md','scripts/quick_validate.py','scripts/visualize.py','agents/openai.yaml']:
 extra('codebase-knowledge',rel,(up/rel).read_text())
edit('codebase-knowledge','Do not overwrite a file unless it carries `<!-- AUTO-GENERATED -->` as the first body line, or the user explicitly asks for a full rebuild. If a human-edited file is stale, flag it for the user rather than silently overwriting.',
'Before replacing an existing file, verify both its `<!-- AUTO-GENERATED -->` first body line and its exact-byte SHA-256 against the prior generated output recorded in `knowledge/.generation-manifest.json`. A marker alone does not protect later human edits. If the hash differs or no baseline exists, preserve the file and report a proposed refresh; replace it only when the user explicitly authorizes that file or a full rebuild. Apply this protection to the inventory, indexes and log as well as concept documents; preserve existing log entries when appending a run.')
edit('codebase-knowledge','Compare source files against each doc\'s `generated_from` field and `timestamp`.',
'Compare the current SHA-256 of each `generated_from` source with its recorded source hash in `knowledge/.generation-manifest.json`; directories use a sorted map of in-scope file paths and their hashes. Use Git revisions as supporting evidence when useful. Timestamps are informational, not proof of freshness.')
edit('codebase-knowledge','1. **Refresh the inventory.** Re-run Phase 1 and diff the new `project_inventory.md` against the existing one. Note added, removed, and changed items.',
'1. **Refresh the inventory in memory.** Re-run Phase 1 without overwriting the existing inventory, then diff the proposed inventory against it. Apply the human-edit protection below before writing it. Note added, removed, and changed items.')
edit('codebase-knowledge','`scripts/quick_validate.py` automates the mechanical checks — run it first, then do the semantic checks below by hand.',
'Run `python3 <skill-directory>/scripts/quick_validate.py --bundle <knowledge-directory>` first, then do the semantic checks below by hand. The script is read-only; its separate `<skill-directory>` positional mode checks this skill package. Use an available Python runtime with PyYAML; report the missing dependency without claiming validation succeeded.')
edit('codebase-knowledge',"- No doc is stale: cross-check each doc's `timestamp` against the modification dates of its `generated_from` sources, and flag any where sources are newer.",
'- Check source freshness against recorded source hashes. If no source baseline exists, report freshness as unverified; copied files and Git checkouts can have misleading modification times.')
edit('codebase-knowledge','Produce a short report grouped by issue type, then update the completeness checklist in the root `index.md`.',
'Produce a short report grouped by issue type. Validation alone must not modify the checklist, log, manifest, or any other file. During an authorized Generate or Update run, refresh the completeness checklist only after applying the same human-edit protection used for other existing files.')
append('codebase-knowledge', '''## Generation manifest

After an authorized Generate or Update write, maintain `knowledge/.generation-manifest.json` using the contract in `references/knowledge-spec.md`. Record exact output hashes and in-scope source hashes only for content actually generated or refreshed. Do not adopt an existing human-edited file as generated merely to make its hash match. A missing or conflicting baseline requires preservation, not overwrite. Resolve script paths from this skill directory, not the repository working directory.
''')
p=Path(by['codebase-knowledge']['target']).parent/'references/knowledge-spec.md'
st=ROOT/'staged'/p.relative_to('/home/surajsinh');s=st.read_text();s=s.replace('Files that are safe to hand-edit and should be regenerated only on demand may include `<!-- AUTO-GENERATED -->` as the first body line (after frontmatter) to opt into automatic overwrite during updates. Files without that marker are treated as human-protected.',
'`<!-- AUTO-GENERATED -->` as the first body line identifies generated concept content. It is not sufficient overwrite authorization: a subsequent human edit may leave the marker intact. Existing content may be automatically replaced only when its exact-byte SHA-256 matches the previously recorded generated hash. A missing baseline, removed marker, or changed hash protects the file until explicit replacement authorization.')
s+='''\n## Generation manifest extension\n\n`knowledge/.generation-manifest.json` is a local bookkeeping extension, not an OKF concept document. Use JSON with `schema_version: 1` and a `documents` object keyed by bundle-relative file paths. Each entry contains `output_sha256` (exact bytes last written by the generator) and `sources` (repository-relative file path to exact-byte SHA-256 map). Include generated inventory and indexes; for the log, preserve prior entries when writing a new run. Do not put the manifest's own hash inside itself.\n\nBefore an update, compare current outputs to recorded output hashes and current in-scope source files to their recorded source hashes. Added and removed files must affect a directory source snapshot. Protect files with no baseline or modified bytes. Record only outputs actually written under the requested workflow, and never reset hashes for protected content. Write the manifest after successful document writes; if interrupted, treat mismatched outputs conservatively on resume. Validation never updates this manifest.\n''';st.write_text(s)

# Current versions already have correct defaults; make the live contract explicit.
edit('imagegen','For transparent images, ask built-in `image_gen` for a transparent background and preserve the generated alpha.',
'For transparent images, use the current built-in tool schema: set `transparent_background: true` when exposed, and preserve the generated alpha. For edits, preserve existing transparency unless the user asks to change it. Do not substitute chroma-key processing when native transparency is available.')
edit('imagegen','Ask built-in `image_gen` for a genuinely transparent background and preserve its alpha.',
'Use the native transparency control advertised by the current tool (`transparent_background: true` in supported sessions) and inspect the result. Do not infer capabilities from a model name or older cached guidance. If the actual tool lacks the required control or fails, explain the observed limit and offer a supported fallback within the existing authorization; changing to a separately billed API/model path requires user intent for that path.')
edit('imagegen','- Never modify `scripts/image_gen.py`. If something is missing, ask the user before doing anything else.',
'- Do not change the bundled generator during ordinary image work. If a required capability is unavailable, report that limitation and continue independent authorized work. Requests to repair this skill or its scripts may edit them with appropriate validation.')
append('openai-docs','''## Capability and configuration boundary

Use the live tool inventory to determine what is callable. If documentation MCP tools are missing during an ordinary lookup, use the official-domain browsing fallback; do not install servers, change configuration, escalate for installation, or request a restart. Local skill review and edits should inspect the relevant local files first. Source order must not prevent host-required progress updates or local diagnostics. Configure documentation integration only when that setup is explicitly requested, following the integration reference.
''')

# Focused discovery and safe, attributable installation.
edit('find-skills','- Asks "how do I do X" where X might be a common task with an existing skill',
'- Explicitly asks to discover a reusable skill for X, or a demonstrated capability gap makes discovery useful')
edit('find-skills','- Asks "can you do X" where X is a specialized capability',
'- Asks what installable capability is available for a specialized task; answer ordinary can-you-do-X task requests directly when existing tools suffice')
edit('find-skills',"### Step 2: Check the Leaderboard First",'### Step 2: Check existing capabilities first')
s=read('find-skills');start=s.index('Before running a CLI search,');end=s.index('### Step 3:',start)
s=s[:start]+'''Use already available skills and tools when they meet the request. Search the catalog when discovery is requested or a real capability gap remains. A leaderboard can suggest candidates, but install counts do not establish quality, safety, or suitability. Verify current metrics before quoting them; avoid hardcoded popularity claims.\n\n'''+s[end:];write('find-skills',s)
start=s.index('**Do not recommend a skill based solely on search results.**');end=s.index('### Step 5:',start)
s=s[:start]+'''Do not recommend based solely on search results, install count or repository stars. Inspect the candidate's actual instructions and any scripts that would run: match the requested task, check source provenance and maintenance, identify required credentials, external actions and write scope, and look for unrelated installation or configuration changes. Prefer a maintained source and a reviewable revision; popularity is secondary evidence. If inspection is unavailable, disclose what remains unverified.\n\n'''+s[end:];write('find-skills',s)
edit('find-skills','npx skills add <owner/repo@skill> -g -y','npx skills add <owner/repo@skill>')
edit('find-skills','The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.',
'Choose the user-requested installation scope. Add `-g` only for an authorized user-level installation; use `-y` only when that exact installation and scope are already authorized. Record the source and resolved revision when available. Follow the CLI\'s current help for revision support rather than inventing flags. Do not run update-all as part of a single installation.')
edit('skill-installer','All of these scripts use network, so when running in the sandbox, request escalation when running them.',
'These scripts use the network. Run within current permissions first; request scoped escalation only when a sandbox/network denial actually prevents the authorized operation. Do not treat every environment as requiring escalation.')
edit('skill-installer','- The skills at https://github.com/openai/skills/tree/main/skills/.system are preinstalled, so no need to help users install those. If they ask, just explain this. If they insist, you can download and overwrite.',
'- System skills are preinstalled. If the user explicitly requests replacement, prepare the replacement separately, validate it, preserve a recoverable backup, and replace only the requested skill. The installer refuses an existing destination; do not delete it to bypass that protection. Preserve unrelated files and use a targeted replacement after staging.')
append('skill-installer','''## Provenance and replacement

For installation, resolve the selected repository ref to its exact commit with an available Git/provider read, and pass that commit through the supported `--ref` option. Record the repository, skill path, resolved commit and destination in the handoff or a task-local installation record. If revision verification is unavailable, say so rather than describing a moving branch as pinned. Preserve credentials and never include tokens in that record. For replacement, stage and validate before switching; restore the backup if replacement verification fails.
''')

# Avoid mandatory novelty and invented client history.
s=read('frontend-design');start=s.index('Approach this as the design lead');end=s.index('## Ground it',start)
s=s[:start]+'''Choose a visual direction grounded in the actual brief, audience and product. Preserve an established design system when editing. For exploratory work, propose a distinctive element when it improves the experience; novelty and aesthetic risk are optional, not requirements for routine product work. Do not invent client preferences or a history of rejected designs.\n\n'''+s[end:];write('frontend-design',s)
edit('frontend-design',"and take one real aesthetic risk you can justify.","when useful.") if 'and take one real aesthetic risk you can justify.' in s else None
edit('frontend-design',"Type: the typefaces for 2+ roles (a characterful display face that's used with restraint, a complementary body face, and a utility face for captions or data if needed).",
'Type: use the existing type system where established; otherwise choose the fewest typefaces needed for clear display, body and utility roles. One family can serve several roles.')
edit('frontend-design','Spend your boldness in one place.', 'When the brief benefits from a signature element, concentrate boldness there.')
append('frontend-design','''## Verify usability

Check primary flows at narrow and wide viewports. Verify keyboard reachability, visible focus, meaningful names for controls, error recovery and reduced motion. Check text contrast against the actual background, targeting at least 4.5:1 for normal text and 3:1 for large text. Preserve the user's existing components and design tokens during bounded edits.
''')
for n in ['orca-cli','orchestration','computer-use']:
 s=read(n)
 insertion='''## Scope and prerequisites

This skill requires an Orca-managed context or an explicit request to use Orca. Generic handoffs, decomposition, skill sharing or desktop/browser tasks do not select Orca by themselves. When Orca is not involved, use the host-supported workflow and tools. Do not launch or configure Orca merely because this skill is present. If the selected Orca executable or runtime guide is unavailable, report that specific limitation and continue independent authorized work; do not substitute another Orca build or fabricate runtime commands.

'''
 at=s.index('## Resolve the CLI');s=s[:at]+insertion+s[at:];write(n,s)
edit('orca-cli','"handoff" / "handover" / "give this to another\n  agent", "Orca browser", "orca artifacts", or "share skills".',
'"handoff" / "handover" / "give this to another\n  agent" in an Orca context, "Orca browser", "orca artifacts", or Orca skill sharing.')
edit('orchestration','  Coordinate supervised Orca workers:', '  Coordinate supervised workers only in an Orca context:')
edit('computer-use','  Drives the GUI of a visible local app window through `orca computer`:', '  Drives the GUI of a visible local app window in an Orca session through `orca computer`:')
edit('orchestration','Engage Orca orchestration whenever you need structured multi-agent coordination:',
'Engage Orca orchestration when working in an Orca context and you need structured multi-agent coordination:')

# Document defaults should preserve real content and user design.
s=read('documents');start=s.index('**Title clarity is an absolute requirement.**');end=s.index('\n\n',start)
s=s[:start]+'''**Make titles clear.** State the specific subject and purpose. Use natural punctuation where meaningful, including technical names such as C++ and headings such as Q1: Results. For a new document without a supplied style, prefer Word's `Title` style and restrained, readable treatment. Existing templates, branding and requested formatting take precedence; do not remove their colors, borders or punctuation during unrelated edits.'''+s[end:];write('documents',s)
edit('documents','- If anything looks off, fix the DOCX and **re-render** (repeat until flawless)',
'- Fix material clipping, overlap, missing glyphs and unreadable or broken layout, then re-render affected pages. After three repair attempts for the same unresolved failure, preserve the best draft and report the exact blocker; do not claim the render gate passed. Do not continue cosmetic iteration without an observed defect.')
s=read('documents');start=s.index('## Equations:');end=s.index('## Quick start',start);block=s[start:end]
# A reference one directory deeper must point back to skill-local resources.
extra('documents','references/equations.md',block)
s=s[:start]+'''## Equations

When equations are present or requested, read [equation representation and rendering](references/equations.md). Preserve native editable equations when required and do not silently rasterize them.

'''+s[end:];write('documents',s)
edit('documents','Do not stop revising until all formatting issues are fixed.',
'Fix material formatting failures using the bounded render-and-repair procedure above; disclose unresolved defects instead of claiming completion.')
# PDF ambiguity and helper path portability.
edit('pdf','Report the ambiguity or produce a static result.',
'Report the ambiguity and preserve the interactive source. Produce a static result only if the user requested or explicitly accepted flattening; never infer that choice from a field-tree error.')
append('pdf','''## Runtime and recovery

Resolve `container_tools/mark_artifact_operation_started.mjs` from the workspace dependency/runtime loader's authoritative base, and invoke it by absolute path; do not assume it is relative to the task checkout. If a host-specific marker is not supplied, report that capability limit and follow the host's supported authoring path rather than inventing the helper. Reuse an available renderer before installing system packages. After three failed repairs of the same rendering issue, preserve the draft and report the unresolved issue without claiming it passed visual verification.
''')
# Presentations: replace the brittle writing taxonomy with a focused router and contextual reference.
s=read('presentations');start=s.index('## Writing Quality Instructions');end=s.index('## Important instructions',start);block=s[start:end]
for a,b in [('Em dashes are always slop.','Use an em dash when it makes the sentence easier to read; avoid repeated ornamental interruptions.'),('Semicolons are always slop.','Use a semicolon when it clearly joins related clauses; prefer shorter sentences when those read better.'),('ASCII dots are always slop.','Use separators only when they clarify genuinely parallel labels.'),('Vertical bars are always slop.','Use a vertical bar only when it clarifies the layout or notation.'),('Arrows are always slop.','Use arrows for real direction, sequence or causal relationships.'),('“Is / is not” sentence structures are always slop.','Use a contrast only when it explains a real distinction.'),('Passive voice is always slop.','Prefer active voice when the actor is known and relevant; preserve passive voice when it is more precise.'),('Imperative slide titles are always slop.','Use imperative titles for instructions or actions; choose factual titles for findings and explanations.')]:block=block.replace(a,b)
extra('presentations','references/writing-quality.md','# Contextual slide writing guidance\n\nThese examples are editing suggestions, not universal grammar bans. Preserve accurate technical notation, quotations, user wording and useful instructions.\n\n'+block)
s=s[:start]+'''## Writing quality

Write clear, accurate slide content for the intended audience. Keep necessary qualifications and use punctuation, passive voice, contrasts and imperative titles when they improve meaning. Remove filler and unsupported claims. For substantial writing or editing, consult [contextual writing examples](references/writing-quality.md); the examples are guidance rather than automatic rejection rules.

'''+s[end:];write('presentations',s)
# Hosting intent and existing repository boundaries.
edit('sites','description: Use Sites when the user wants a website built for them (including a landing page, portfolio, dashboard, portal, tracker, hub, game, event registration, or tool), requests changes to a website already built with Sites, wants to publish a website with Sites, or wants to manage Sites hosting.',
'description: Build or modify websites with Sites hosting when the user selects Sites, requests a hosted website, or identifies an existing Sites project. Use for Sites publication and hosting management. For implementation in an existing repository without Sites intent, follow that repository workflow.')
edit('sites','Take the requested website through the supported development and publishing workflow. Publish completed new Sites and edits unless the user requests local-only work or saving without deployment.',
'Take the requested Sites website through its supported workflow. Publish when hosting or deployment is requested or already authorized in the conversation. For an existing repository request without deployment intent, complete and verify the local change; do not register or publish a Site. Reuse established deployment authorization without another conversational gate.')
edit('sites','Run checks appropriate to the change; lint only when requested.',
'Run repository-required checks, including lint where required, and additional checks appropriate to the change. Reuse successful results for unchanged inputs.')
edit('sites-remix','Limit intake to **three questions total**.',
'Prefer at most **three questions per batch**, asking only unresolved decisions that change implementation. Additional necessary decisions may use a later batch; do not treat an unanswered question as permission.')
edit('plugin-management','- Use `uninstall_app` only when the user explicitly requests removal.',
'- Discover the current plugin-removal capability and follow its advertised schema (`uninstall_plugin` on supported Codex hosts, or `uninstall_app` where that is the available contract). Use it only when the user explicitly requests removal.')

# Consolidate the large identical workbook model section, retaining surface-specific sensitivity rules.
s=read('spreadsheets');b=read('excel-live-control');start=s.index('## Spreadsheet (Workbook) Complexity:');end=s.index('## Workflows',start);common=s[start:end]
old='- **Formula choices to avoid:** do not introduce `LET`, array/spill formulas, `MAP`, `REDUCE` or `LAMBDA`. Use familiar formulas and labeled intermediate steps. Normal range arguments in functions such as `SUMIFS` and `SUMPRODUCT` remain appropriate, as do the lookup, `INDIRECT`, `OFFSET` and `CHOOSE` patterns below. Preserve required existing/template behavior and do not rewrite unrelated formulas during a narrow edit. Formula length alone is not the test: the reader must be able to understand and extend the calculation.'
new='- **Formula compatibility and clarity:** choose formulas supported by the intended calculation engine and understandable to the workbook\'s maintainers. `LET`, dynamic arrays, `MAP`, `REDUCE` and `LAMBDA` are appropriate when supported and they simplify the requested work; test recalculation, spill ranges and export compatibility. Use familiar formulas or labeled intermediate steps when they are clearer or more portable. Preserve required existing/template behavior and do not rewrite unrelated formulas during a narrow edit.'
assert old in common;common=common.replace(old,new)
pat=r'- \*\*Sensitivity analysis:\*\*[^\n]+'
sensitivity=re.search(pat,common).group(0)
shared=re.sub(pat,'- **Sensitivity analysis:** follow the surface-specific sensitivity requirements in the active entrypoint. Verify the intended engine supports the requested feature; preserve the shared case-comparison rules above.',common)
# Remap links copied from entrypoint into its references directory.
shared=re.sub(r'\]\((?!https?:|#)([^)]+)\)',lambda m:'](../'+m.group(1)+')',shared)
extra('spreadsheets','references/workbook-quality.md','# Shared workbook quality\n\nRead the structure/formula sections for model creation or changes, and the writing section when authoring labels or guidance. Narrow edits preserve unrelated structure and formulas.\n\n'+shared)
for n in ['spreadsheets','excel-live-control']:
 z=read(n);a=z.index('## Spreadsheet (Workbook) Complexity:');e=z.index('## Workflows',a)
 own=re.search(pat,z[a:e]).group(0)
 target='references/workbook-quality.md' if n=='spreadsheets' else '../spreadsheets/references/workbook-quality.md'
 z=z[:a]+f'''## Shared workbook guidance

For new models or changes to structure, formulas or authored content, read the relevant sections of [shared workbook quality]({target}). It owns structure, formulas, missing-input behavior and writing guidance for both file authoring and live Excel. Read only the sections needed for the task; preserve unrelated content during narrow edits.

### Sensitivity analysis for this surface

{own}

'''+z[e:];write(n,z)
edit('spreadsheets','Read entirely for spreadsheet creation, editing, analysis, or visualization.',
'Read this entrypoint for routing and completion. Load the linked modeling, style, API and workflow references only as needed for the requested task.')
edit('spreadsheets','- Deliverable is saved as an `.xlsx` in `outputs/<unique_thread_id>/`.',
'- Deliverable is saved in the requested format and location. Default to `.xlsx` for a new workbook when no format is specified. Preserve requested CSV/TSV delimiters, quoting, encoding and values; these formats cannot retain multiple sheets, styles, charts or executable formulas. Explain a material format limitation and resolve it before discarding required features. A requested Google Sheets output follows its native routing contract.')
edit('excel-live-control','Before calling `run_officejs` for any reason, read `officejs.md` completely in the current turn and follow its decision boundary and instructions, even when the schema is already available.',
'Before the first `run_officejs` call, read `officejs.md` completely and follow its decision boundary and instructions. Reuse that guidance within this conversation while the package version and live capability schema remain unchanged. Re-read it after a relevant version/schema change or an error that shows the contract changed.')
# Output marker is host-relative in three skills; runtime path resolution also applies to docs/sheets.
for n in ['documents','spreadsheets']:
 append(n,'''## Runtime helper resolution

Resolve host-specific `container_tools/` helpers from the authoritative workspace dependency/runtime base and invoke their absolute paths. Do not assume the task checkout contains them. If a host does not supply a marker helper, report that host capability limit and use its supported authoring contract instead of inventing a helper or claiming it ran.
''')
# Template workflows: keep detailed create mode out of simple metadata updates.
s=read('template-creator');a=s.index('## Create workflow');e=s.index('## Update workflow',a);block=s[a:e]
# Links are authored relative to root skill; rewrite real relative links and internal fragment links.
block=re.sub(r'\]\((?!https?:|#)([^)]+)\)',lambda m:'](../'+m.group(1)+')',block)
block=block.replace('](#','](../SKILL.md#')
extra('template-creator','references/create-workflow.md',block)
s=s[:a]+'''## Create workflow

For a new template, read [creation and reference preparation](references/create-workflow.md) and follow the relevant artifact-type path. Metadata-only updates use the update workflow below without loading creation details.

'''+s[e:];write('template-creator',s)
edit('template-creator','Update only when the user explicitly asks to edit or update exactly one passed artifact-template skill. Treat that passed skill as the exact target; never choose a similarly named template.',
'Update only explicitly identified artifact-template skills. For multiple targets, process each sequentially with its own validation and atomic update; never select a similarly named template. Report success or failure per target.')
edit('template-creator','Stop if it is not a direct child of the personal skills directory or if more than one target was passed.',
'Stop for any target that is not a direct child of the personal skills directory or is ambiguous. When several exact targets were supplied, run this workflow separately for each; do not apply one target\'s reference or metadata to another.')
# Do not depend on current host-specific communication prohibitions.
edit('visualize','- Work silently unless blocked or the user explicitly asks for progress. Never send commentary or progress updates while reading this skill or writing or updating the file; the final response must be your first user-facing message.',
'- Follow the host\'s communication requirements for skill announcements and progress. Keep updates brief and useful; do not expose the implementation details of the visualization in its displayed content.')
edit('visualize','Never announce this skill, a visualization surface, widgets, HTML, SVG, scripts, local files, inline data, or implementation details.',
'Avoid unnecessary implementation details in the explanation. Host-required skill announcements and artifact handoffs remain allowed.')
edit('visualize','- Use only weights `400` and `500`. Never set custom font sizes or line heights.',
'- Use weights `400` and `500` and host-scaled typography by default. Plot labels may use the explicit chart-label sizes specified below, subject to the 11-screen-pixel readability floor. Product mockups use the separate mockup typography rules.')
# Move specialized recipes into references; the explicit chart contracts are retained.
s=read('visualize');a=s.index('### Calendar');e=s.index('## Layout and accessibility',a);block=s[a:e]
extra('visualize','references/specialized-layouts.md',block.replace('](tweak.md','](../tweak.md'))
s=s[:a]+'''### Specialized layouts

For calendars, interactive simulations, plots, maps, dense categorical grids or time-allocation views, read the applicable section of [specialized layouts](references/specialized-layouts.md). These recipes retain the chart sizing, data provenance, touch and label requirements for those visual types.

'''+s[e:];write('visualize',s)
# Bound expensive pet generation and record active selection before mutation.
append('create-pet','''## Checkpoints and resource limits

Before expensive generation, verify the required generation, Library, validation and upload capabilities and bundled scripts are available. Reuse a run's validated source rows and reports. Use an explicit user budget when supplied; otherwise checkpoint at the approximate run budget above. After two strategy changes for the same unresolved failure, stop that failing generation path and save the resumable run state rather than repeatedly spending resources. Report completed rows, failing gates, saved artifact IDs/paths and the next needed repair. Never upload or claim completion with a failed mandatory gate. Do not start additional generation beyond a user-specified budget without authorization.
''')
edit('pets','State the exact pet name and stable ID and that the pet record and stored sprite sheet will be permanently deleted before the destructive action is confirmed.',
'State the exact pet name and stable ID and explain permanent deletion. Use the host/tool confirmation path once when it is required; do not add a second chat approval when an explicit deletion request already unambiguously authorizes the same target and the host permits execution. Resolve target ambiguity before calling the destructive tool.')
edit('update-pet','5. Keep that stable pet ID as the target.',
'5. Before a mutation, capture the current `active_pet_id` (or confirmed inactive state) from a fresh collection read when it is not already current. Keep it as the baseline for active-selection preservation. Keep that stable pet ID as the target.')
# Per-template additions stay scoped to the recommendation; no invented data.
report=Path('/home/surajsinh/Desktop/pr-review/skills-review.md').read_text()
for n in list(by):
 if not n.startswith('artifact-template-'):continue
 pattern=r'\| \['+re.escape(n)+r'\]\([^\n]+?\) \| ([^\n]+) \|'
 match=re.search(pattern,report)
 assert match,n
 append(n,'## Input and completion checks\n\n'+match.group(1)+' Do not invent missing facts. Ask only for missing inputs that materially change the requested artifact; otherwise preserve an empty field or clearly identify the assumption. If the required artifact capability is unavailable, report the exact missing capability and preserve prepared inputs so the task can resume. Do not claim that an unrendered or unverified artifact is complete.')
# The review helper returned after the earlier review; patch only its committed-branch comparison.
r=Path('/home/surajsinh/.codex/skills/.system/review-agent/SKILL.md')
if r.exists():
 s=r.read_text();s=s.replace('then inspect `git diff <merge-base-sha>`.','then inspect `git diff <merge-base-sha> HEAD` for a committed-branch review. Include staged or unstaged changes only when that is the requested review target, and state that scope.')
 addfile(r,s)
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(ROOT/'preparation-notes.json').write_text(json.dumps(notes,indent=2)+'\n')
print('Prepared',len(manifest),'files')
