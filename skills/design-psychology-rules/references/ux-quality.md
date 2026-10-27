# Rules 27–49 — UI/UX Quality

Psychology alone doesn't make a production-quality interface. These rules cover what a complete review also needs: discoverability, information architecture, states, recovery, accessibility, resilience, content, data-heavy UI, and trust. They build on Rules 1–26 in [psychological foundations](rules.md). Where a topic overlaps an earlier rule, the earlier rule holds the detail and is cross-referenced. Project needs determine which patterns apply; these lists are not a requirement to add every listed feature or state.

Contents: [Discoverability and IA](#part-6-discoverability--information-architecture) · [States and recovery](#part-7-states-feedback--recovery) · [Accessibility](#42-accessibility-by-default) · [Responsive and edge cases](#43-responsive-behavior) · [Content, data, and trust](#part-9-content-data--trust) · [Accessibility sources](#accessibility-sources-and-scope)

---

## Part 6: Discoverability & Information Architecture

### 27. Hide Complexity, Not Functionality *(foundational)*
A clean interface doesn't mean removing access to features. When an interface has many capabilities:

1. Prioritize the most common actions.
2. Keep critical functionality visible.
3. Group related functionality.
4. Use progressive disclosure for secondary functionality.
5. Use collapsible sections for advanced configuration.
6. Use overflow menus for low-frequency actions.
7. Use search or a command palette for large feature sets.
8. Let users customize visibility where appropriate.
9. Never hide important functionality behind ambiguous or undiscoverable controls.

**Everything should be accessible without everything needing to be visible at the same time.** When tempted to delete a feature to declutter, first try 3–8.

### 28. Feature Discoverability
Every important feature should pass seven questions:

| Question | Fails when… |
|---|---|
| **Can the user find it?** | There's no obvious location and no search path. |
| **Can they recognize it?** | The label or icon doesn't communicate what it does (unlabeled icons are the usual culprit). |
| **Can they understand it?** | Its purpose is unclear until after activation. |
| **Can they reach it?** | It's buried under several layers for no reason. |
| **Can they operate it?** | It needs hover, right-click, a gesture, or precise pointing with no alternative. |
| **Can they see its state?** | Active / disabled / loading / expanded / saved / failed isn't distinguishable. |
| **Can they recover?** | There's no undo, cancel, retry, or correction path. |

Hidden-by-default gestures (swipe-to-reveal, long-press, double-tap) are never the *only* way to reach an important action.

### 29. Progressive Disclosure
Reduce cognitive load without reducing discoverability. Assign every feature a visibility level:

| Level | Treatment | Examples |
|---|---|---|
| **1 — Primary** | Shown directly | Main CTA, search, primary nav, most common actions, critical status |
| **2 — Secondary** | Nearby or in a clearly labeled section | Filters, sort, secondary actions, extra info |
| **3 — Advanced** | Collapsible section or advanced settings | Advanced config, developer options, automation rules, fine-grained preferences |
| **4 — Rare / expert** | Overflow menu, command palette, context menu, dedicated page | Bulk admin, export formats, destructive account actions |

Assign levels by **frequency × importance**, not by what's easiest to build. A rarely used but critical feature (e.g., "Export my data", "Cancel subscription") must not be buried at Level 4 behind an ambiguous control.

**Collapsed does not mean inaccessible.** The user must be able to tell more exists and how to open it.

### 30. Collapsible UI Must Be Understandable
Applies to accordions, disclosure controls, "Show more," "Advanced settings," sidebar groups, and nested nav. Check:

- It's obvious the section is expandable (chevron/caret, not just bold text).
- Current state is visible (▸ collapsed / ▾ expanded) and exposed to assistive tech (`aria-expanded`).
- The label says what's inside: `Advanced settings ▾` beats `Options`; `Show 12 more fields` beats `More`.
- The trigger is a real `<button>`; Enter/Space toggle it; focus stays on the trigger after toggling.
- Expanding doesn't jump the page or move content out from under the cursor.
- Expanded content still makes sense in context.
- Nothing the user needs to complete the main task — or anything with consequences (fees, terms, data sharing) — is collapsed by default.
- Expanded/collapsed state persists when it's a user preference (e.g., sidebar groups).

### 31. Information Architecture
Organize by the **user's mental model, not the company's org chart or the codebase.** The user shouldn't need to understand internal architecture to navigate.

Check:
- Related features are grouped; categories are meaningful and mutually distinct.
- Categories aren't too broad ("General", "Misc", "Other" are smells) or too deep (prefer ≤ 3 levels).
- Labels use user vocabulary, not internal/technical terms.
- No duplicate locations that behave differently, and no orphan features reachable from nowhere.
- Users can predict where something lives before they look.

Validate with card sorting (to build the structure) and tree testing (to check findability) when IA is non-trivial.

### 32. Navigation, Findability & Search as a Safety Net
Complex products need **multiple paths** to important functionality:
- Primary and secondary navigation
- Breadcrumbs and clear "you are here" indicators (active nav item, page title matching the nav label)
- Contextual actions and related links
- Global search, settings search, and/or a command palette (`⌘K` / `Ctrl+K` — "Search settings, pages, actions…")
- Recent items, favorites, pinned items

Search should **complement** good IA, not excuse bad IA. Good search: tolerates typos and synonyms, searches actions and settings (not just content), shows recent items when empty, and handles no-results helpfully (Rule 39).

### 33. Information Density
When a screen holds too much, don't start by deleting. Ask in order:
1. Can related items be grouped?
2. Can low-priority information be collapsed?
3. Can advanced settings move behind progressive disclosure?
4. Can secondary actions move into an overflow menu?
5. Can users choose visible fields?
6. Can content split into logical tabs?
7. Can actions appear only when contextually relevant? (Rule 34)
8. Can search/filtering shrink the visible dataset?

Use density intentionally. For data-heavy UIs, offer density modes (comfortable / compact / dense) and let users control it. Expert tools can and should be denser than consumer onboarding.

### 34. Contextual Actions
Don't show every possible action everywhere; show actions when they're relevant.

```
Before selection:  Search | Filter | Sort
After selecting:   3 selected | Archive | Export | Delete | ✕ Clear
```

This reduces noise while keeping functionality available. Keep the contextual bar in a consistent position, always show the selection count and a way to clear it, and make the triggers reachable without hover (touch and keyboard users).

### 35. Progressive Complexity
Support multiple skill levels in one product:

| User | Needs |
|---|---|
| **Beginner** | Simple defaults, guidance, safe paths |
| **Regular** | Faster workflows, visible secondary controls |
| **Advanced** | Keyboard shortcuts, bulk actions, customization |
| **Expert** | Command palette, automation, advanced settings, API, power workflows |

Don't force beginners to understand expert functionality. Don't force experts through slow beginner workflows. Accelerators (shortcuts, bulk ops) are added *on top of* the discoverable path, never as a replacement for it. Show shortcuts in menus and tooltips so users can graduate.

### 36. Personalization Without Complexity
Allow customization of complex interfaces when it helps: visible columns, sidebar items, dashboard widgets, density, saved filters, pinned actions, default views.

But personalization **must not be required** to use the product. Start with sensible defaults, make customization discoverable but out of the way, and always offer "Reset to default."

---

## Part 7: States, Feedback & Recovery

### 37. State Completeness
A design that only specifies the happy path is incomplete. Design every meaningful state:

| Element | States |
|---|---|
| **Buttons** | default, hover, focus, pressed, disabled, loading, success, error |
| **Inputs** | empty, focused, filled, valid, invalid, disabled, read-only, loading |
| **Pages** | loading, empty, populated, error, offline, permission denied, partial data, success |
| **Tables** | loading, empty, no search results, error, selected rows, bulk actions, pagination, long content, missing data |

Notes:
- **Disabled controls** should explain why and what enables them, through nearby helper text or another accessible mechanism. A tooltip on a native disabled control alone is insufficient when that control cannot receive keyboard focus. If a tooltip is used, apply the hover/focus behavior in Rule 42. Often it's better to keep the button enabled and show a validation message on press.
- **Focus** is a distinct state from hover — never remove focus outlines without a visible replacement (Rule 42).
- **Hover** can never carry information that isn't available otherwise (touch has no hover).

### 38. Visibility of System Status & Loading
Users should always know what the system is doing, immediately after every important action. *(Nielsen heuristic #1; timing thresholds in Rule 22.)*

Good status messages are specific:
- `Saving…` → `Saved` (or `Saved 2 min ago`)
- `Uploading 3 of 10 files`
- `Syncing…`
- `Offline — changes will sync when you're back online.`
- `Processing — this may take a few minutes. You can leave this page.`

Loading-pattern examples, by rough expected duration; choose for the task and observed latency rather than treating the ranges as universal thresholds:

| Duration | Pattern |
|---|---|
| < ~1 s | Usually nothing beyond the pressed state; avoid spinner flicker |
| 1–3 s | Skeleton or inline spinner in the affected area |
| 3–10 s | Labeled progress: `Generating report…` |
| > 10 s | Meaningful status; tracked progress/steps or a supported estimate when available, otherwise an indeterminate indicator. Offer backgrounding, notification, or cancellation when the operation supports it. |

Use determinate progress only when completed work can be related to a known total. Show real steps or time estimates only when the operation supplies a defensible basis; never invent percentages, step counts, or remaining time to satisfy a duration guideline. Unknown-duration work can use a labeled indeterminate indicator, changing to determinate if progress becomes measurable.

Never an unexplained spinner on a blank page. Expose qualifying status messages to assistive technology without moving focus, using suitable semantics (Rule 42, WCAG 4.1.3); not every progress tick needs an announcement.

Source checked **2026-10-27**: [Carbon progress-bar guidance](https://www.carbondesignsystem.com/building-blocks/core/components/progress-bar/guidelines). Its determinate/indeterminate distinction is bundled above; its product-specific presentation choices are not mandatory for every project.

### 39. Empty States
An empty state answers three questions:
1. **What** is empty?
2. **Why** is it empty?
3. **What can the user do next?**

> **No projects yet**
> Create your first project to start organizing your work.
> `Create project`

Distinguish the types — they need different copy:
- **First use** ("No projects yet") → onboarding + primary action.
- **No results** ("No projects match 'q3 plan'") → show the query, offer to clear filters or fix spelling.
- **Cleared / done** ("All caught up") → positive closure (Rule 25).
- **No permission** ("You don't have access to any projects in this workspace") → who to ask.

Never just `No data`.

### 40. User Control & Freedom
Users should be able to cancel, undo, redo, go back, edit, retry, restore, recover drafts, leave a flow, and reverse non-destructive actions. **Users should never feel trapped in a flow.**

- **Prefer Undo over confirmation dialogs** for reversible actions (`Archived 3 items · Undo`). Confirmations interrupt every time and get habitually dismissed; undo costs nothing when the user was right.
- **For destructive, irreversible actions**, say clearly:
  - what will happen and what will be deleted (name it: "Delete project 'Q3 Launch' and its 48 tasks"),
  - whether it's reversible,
  - what they could do instead (archive, export first).

  Make the confirm button name the action (`Delete project`, not `OK`) and style it as destructive. For high-stakes deletes, require typing the name.
- Soft-delete with a recovery window ("Trash — items are deleted after 30 days") is often the best of both.
- Back/browser-back must not lose work; warn before discarding unsaved changes (Rule 18).
- Modals and multi-step flows always have a visible way out (✕, Cancel, Esc).

### 41. Error Prevention & Recovery
**Prevent first:** constrain inputs where useful, use sensible defaults, disable impossible combinations, show format hints up front, and confirm high-risk actions when needed. For qualifying legal/financial commitments, modifications/deletions of user-controllable stored data, or submission of test responses, WCAG 3.3.4 requires at least one safeguard: the submission is reversible, inputs are checked with an opportunity to correct errors, or users can review, confirm, and correct before finalizing. A separate review screen is one option, not mandatory when another option is met.

**When errors happen, the message answers four questions:**
1. **What** went wrong?
2. **Where?** (next to the field, plus a summary at the top for long forms)
3. **Why?**
4. **How do I fix it?**

| | Message |
|---|---|
| ❌ Bad | `Invalid input` |
| 🟡 Better | `Project names must be 50 characters or fewer.` |
| ✅ Best | For a field whose actual project limit is 50, show `50 characters maximum` before typing, a useful `54/50` counter, and `Project name is too long — remove 4 characters.` after validation. |

These are copy examples, not prescribed product limits. Password requirements must come from the project's applicable authentication policy. Where NIST SP 800-63B-4 applies, single-factor passwords require at least 15 characters; passwords used only as part of MFA may have an 8-character minimum. Do not impose either number universally or flag a different policy without establishing applicability. Source checked **2026-10-27**: [NIST password-verifier requirements](https://pages.nist.gov/800-63-4/sp800-63b.html#passwordver).

Also:
- **Preserve non-sensitive input** after an error where policy permits; do not unnecessarily clear unrelated fields. Passwords, one-time codes, and other secrets follow the applicable security and expiration rules rather than a blanket retention requirement.
- Validate on blur or submit, not on every keystroke for fields the user hasn't finished; clear the error as soon as it's fixed.
- Mark required fields explicitly (don't rely on color or an unexplained asterisk).
- Errors are identified in text and programmatically associated with the field (WCAG 3.3.1, 3.3.3), not shown by red borders alone.
- Move focus to the first error (or the error summary) on submit.
- System errors: say what happened in plain language, whether data was lost, and offer **Retry**. `Error 403` → `You don't have permission to edit this project. Ask an admin for access.`
- Information entered by or supplied to the user that must be entered again in the same process should be auto-populated or selectable (WCAG 3.3.7). Exceptions apply when re-entry is essential, needed for content security, or the earlier information is no longer valid. Do not flag an evidenced security recheck or expired value solely because it repeats a field. The exception is not permission to request redundant non-sensitive information unnecessarily.

Forgiving input formats are covered in Rule 23.

---

## Part 8: Accessibility & Resilience

### 42. Accessibility by Default
Accessibility is evaluated during design, not as a final QA step. **WCAG 2.2 Level AA is the default web-review baseline**, including applicable Level A criteria. Record an explicit different project target and separate its requirements from stronger recommendations. WCAG organizes requirements under four principles — **Perceivable, Operable, Understandable, Robust** — with testable success criteria at A, AA, and AAA. This review-focused selection is not the complete standard or a conformance certification. For native interfaces, distinguish web CSS/HTML criteria from the platform's requirements.

Before reporting a violation, establish the relevant criterion, level, observed behavior, and whether an exception applies. A mockup can specify intended semantics and interaction but cannot prove their implementation. Mark keyboard, assistive-technology, motion, zoom, and hidden-state behavior not verified unless the necessary source or execution evidence is available.

**Visual**
- Text contrast normally needs 4.5:1; large text needs 3:1 (1.4.3). Large means at least 18 pt, or 14 pt bold (24 or approximately 18.67 CSS px). Exemptions cover logos/brand names and incidental text: inactive controls, pure decoration, text invisible to everyone, or text embedded in a picture with significant other visual content. A placeholder in an active input is not exempt merely because it is a placeholder. Verify actual colors and font sizes; do not certify contrast from an uncalibrated screenshot.
- Non-text contrast (1.4.11) normally needs 3:1 against adjacent colors for visual cues needed to identify controls/states and meaningful graphics. It does not demand a border on every button: sufficiently contrasting text/icon content can identify a control. Inactive controls and unmodified user-agent appearances are exempt; graphics may have an essential-presentation exception. Author-created focus cues still need applicable adjacent-color contrast. This is distinct from AAA focus-change contrast below.
- Never communicate information by color alone — pair with meaningful text, icon, or pattern (1.4.1). An error needs a non-color cue; an additional icon is not mandatory if clear text already supplies it.
- Text alternatives for meaningful images and icon-only buttons; decorative images marked as such (1.1.1).
- Text normally must resize to 200% without losing content or functionality (1.4.4); captions and images of text are excepted from that criterion. Separately test reflow (1.4.10): vertically scrolling content must work at 320 CSS px width; horizontally scrolling content at 256 CSS px height, without two-dimensional scrolling or loss. Required two-dimensional content, such as a data table, map, or diagram, may scroll in two dimensions. Ordinary surrounding content and text within table cells still need appropriate reflow. At a 1280 px starting viewport, 400% zoom gives the 320 CSS px reflow test; passing 200% text resize alone does not prove reflow.
- Honor reduced-motion preferences as a design recommendation. Interaction-triggered animation that can be disabled is addressed by AAA criterion 2.3.3, with an essential-animation exception; do not label lack of `prefers-reduced-motion` alone an AA failure. Under Level A 2.2.2, automatically starting motion/blinking/scrolling lasting more than five seconds alongside other content needs pause/stop/hide unless essential. Auto-updating information alongside other content needs pause/stop/hide or control over update frequency unless essential; it has no five-second exemption.
- Flashing (2.3.1, Level A) must stay at no more than three flashes in any one-second period **or** below the general/red-flash thresholds. Thresholds depend on luminance/color change and affected visual area; use a suitable analysis tool when claiming that exception, rather than inferring safety from the animation's CSS or a still image. Avoid flashing where possible; without analysis, report the threshold question as not verified.

**Keyboard**
- All functionality must be keyboard-operable (2.1.1), except input whose underlying function depends on the path of movement, such as freehand drawing; this does not exempt ordinary drag-and-drop controls. Provide a way to leave keyboard interactions (2.1.2).
- Focus order must preserve meaning and operability (2.4.3); it need not duplicate every visual position when more than one logical order works.
- Keyboard focus must be visible (2.4.7). AA 2.4.11 requires that a focused component not be entirely hidden by author-created content. User-movable content is assessed in its initial position; user-opened content may obscure an item if it can be revealed without advancing focus. Partial obstruction is not automatically a 2.4.11 failure, though it may harm usability or hide the focus indicator and fail another criterion.
- Stronger targets are AAA: 2.4.12 avoids any obscuring; 2.4.13 requires a focus-indicator area at least equivalent to a 2 CSS px perimeter and 3:1 contrast between the same pixels in focused/unfocused states, subject to unmodified/user-agent indicator exceptions. Do not report these AAA thresholds as mandatory AA rules.
- Enter/Space activate buttons; Esc closes menus, popovers, and modals; arrow keys move within composite widgets (tabs, menus, radio groups).
- **Modals:** focus moves into the dialog, Tab cycles within it, Esc closes it, and focus returns to the trigger on close. (Containing focus inside an open modal is correct; it's a trap only if there's no way out.)
- Provide a "Skip to content" link on pages with repeated navigation.

**Assistive technology**
- Use semantic HTML first (`button`, `a`, `nav`, `main`, headings in order, `label`); ARIA only to fill gaps.
- Every control has an accessible name, correct role, and exposed state/value (4.1.2) — expanded, selected, checked, pressed, disabled, current page.
- For controls with a visible text label, the accessible name must contain that visible text (2.5.3, Level A). Starting the name with the visible label is a recommendation, not an extra requirement. A button displaying `Delete` but named only `Remove item` can frustrate speech activation even though it has a name; `Delete project` contains the visible text. Inspect the actual accessible name; do not infer a mismatch from a screenshot or require exact equality when the visible label is included.
- Form fields have persistent visible labels, not placeholder-only labels (3.3.2).
- Status messages that do not take focus must be programmatically available to assistive technology (4.1.3), using suitable semantics such as `role="status"` or a live region. Not every dynamic DOM change requires an announcement; choose timing and scope that avoid overwhelming users.

**Tooltips and other hover/focus content**
- Under 1.4.13 (AA), additional content that appears on hover or focus must remain available while the user needs it: hover-triggered content must be hoverable, and it must persist until the trigger is removed, the user dismisses it, or its information becomes invalid.
- Provide dismissal without moving hover or focus, for example Escape, unless the content communicates an input error or neither obscures nor replaces other content. This exception removes the dismissal requirement, not hoverability or persistence. Unmodified user-agent content, such as a browser's native `title` tooltip, is excepted from this criterion, but is not a general substitute for an accessible label or touch access.
- Test mouse, focus, and touch access separately. A tooltip that vanishes before the pointer can enter it fails the hoverability requirement; a tooltip only described in a mockup remains not verified. Do not require every action to have a tooltip if its purpose is already clear.

**Other WCAG 2.2 criteria that affect design decisions**
- Pointer targets normally need 24×24 CSS px (2.5.8). Five exceptions apply: sufficient spacing, an equivalent compliant control on the same page, inline targets in a sentence or constrained by surrounding non-target line height, unmodified user-agent target sizing, or an essential/legally required presentation. For spacing, center a 24 CSS px diameter circle on each undersized target's bounding box: it must intersect neither another target nor another undersized target's circle. A 20 px button may pass through spacing; tightly packed 16 px icon buttons without any exception do not. Rendered icon size alone does not establish the clickable target area.
- Dragging interactions need a single-pointer alternative without dragging (2.5.7), unless dragging is essential or the interaction is unmodified user-agent functionality. Keyboard support is a separate check.
- Repeated help mechanisms must appear in a consistent relative order across a set of pages unless the user initiates a change (3.2.6). This does not require adding a help mechanism where none exists.
- Authentication must avoid mandatory cognitive tests unless an allowed exception applies (3.3.8): a non-cognitive alternative, a mechanism assisting completion, object recognition, or identification of the user's own supplied non-text content. Allow paste and password-manager support to reduce memorization/transcription burdens; do not demand removal of authentication safeguards simply because login exists.

Design artifacts should include focus states, accessible names for icon buttons, heading structure, and reading/focus order — not just visuals.

#### Accessibility sources and scope

The summaries above are original review guidance checked against official W3C material on **2026-10-27**. These links are optional attribution and maintenance references; the applicability and exceptions needed for the listed checks are bundled here. The remaining design heuristics have not received a comprehensive research audit in this integration pass.

- [WCAG 2.2 standard](https://www.w3.org/TR/WCAG22/) and [Understanding index](https://www.w3.org/WAI/WCAG22/Understanding/)
- [Text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), and [text resize](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)
- [Target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) and [reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)
- [Visible focus](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html), [focus not obscured, AA](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html), [focus not obscured, AAA](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-enhanced.html), and [focus appearance, AAA](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html)
- [Error prevention](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html), [flashing](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html), [interaction animation, AAA](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html), and [pause, stop, hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)
- [Keyboard operation](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [focus order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html), and [status messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)
- [Dragging alternatives](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html), [consistent help](https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html), and [accessible authentication](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html)
- [Label in name](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html), [content on hover or focus](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html), and [redundant entry](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html)

### 43. Responsive Behavior
Don't just shrink desktop UI. For each viewport decide:
- What stays visible? What collapses? What moves?
- What becomes a drawer, bottom sheet, or menu?
- What stays sticky? (Keep sticky elements few — they eat small screens and can obscure focus.)
- Is the primary action still reachable — ideally in the thumb zone? (Rule 11)
- Is content readable without zooming or horizontal scroll?
- Do tables still work? (Priority columns, row → card transformation, or horizontal scroll with a sticky first column — chosen deliberately.)
- Are controls still easy to tap, with no hover-dependent interactions?

**The interface's hierarchy must survive the transformation.** If the primary action is obvious on desktop, it must still be obvious on mobile. Also check orientation changes, tablet widths, and 200% zoom on desktop (which behaves like a narrow viewport).

### 44. Edge Cases
Designs must survive real-world data, not ideal mock data. Review with:

- **Quantity:** 0 items · 1 item · 10 items · 10,000 items
- **Content:** very long names · very short names · missing images/avatars · missing fields · unbroken strings (URLs, emails) · emoji · duplicates
- **Network:** slow network · offline · API failure · timeouts · partial results
- **Access:** permission denied · read-only · expired session (preserve work, re-auth in place) · feature not on user's plan
- **Presentation:** large text · small viewport · high zoom · dark mode / forced colors
- **Input:** keyboard-only · screen reader · touch-only
- **Time:** stale data · concurrent edits by another user · actions that complete after the user navigated away

Truncate deliberately (ellipsis + full value on hover/focus/tap), wrap where possible, and never let a long value break layout.

### 45. Localization
Design for text expansion; don't assume English length.
- Translations can run 30–40% longer on average, and 200–300% for very short strings ("Save" → longer words in German or Finnish). Some languages are shorter — layouts should handle both.
- Avoid fixed-width buttons, tabs, and labels; let containers grow and wrap.
- Use proper pluralization rules (not `item(s)`; some languages have several plural forms).
- Localize dates, numbers, currency, and units; handle time zones explicitly ("3:00 PM IST").
- Support RTL layouts (mirrored layout and directional icons; logical CSS properties like `margin-inline-start`).
- Don't embed text in images; don't concatenate translated fragments into sentences.
- Watch locale-specific terminology, names (not everyone has a first/last name split), address formats, and phone formats (Rule 23).

---

## Part 9: Content, Data & Trust

### 46. Content Design
UI copy is part of the interaction. Labels describe the user's action or expected outcome, in the user's language rather than internal jargon. *(Nielsen heuristic #2: match between system and the real world.)*

| Prefer | Over |
|---|---|
| `Create project` | `Continue` |
| `Delete project` | `OK` |
| `You don't have permission to edit this project.` | `Error 403` |
| `Send invite` | `Submit` |

- Buttons are verbs (+ object). Dialog buttons repeat the action from the title.
- Front-load the important words; users scan (Rule 9).
- Be specific and consistent — one term per concept across the product (Rule 21).
- Write errors without blame, such as `Enter a project name` rather than `You entered invalid data`. In public login, recovery, or registration flows, useful copy must also respect the project's account-enumeration protections: do not prescribe messages that reveal whether an account exists, is locked, or is disabled. For example, `If an account matches those details, we'll send recovery instructions` can describe a real recovery flow without confirming membership. Keep detailed diagnosis in an appropriately protected channel; do not invent email delivery or recovery behavior the product does not implement.
- Microcopy reduces anxiety at decision points: "You can change this later," "We'll never post without asking."
- Icon-only buttons need accessible names; add visible labels when icons are ambiguous. Tooltips can supplement discoverability but are not mandatory for every button or a replacement for its name. If used, their interaction must satisfy the applicable Rule 42 checks.

Security-copy source checked **2026-10-27**: [OWASP authentication and error messages](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html#authentication-and-error-messages). This guard applies to security-sensitive disclosure, not a blanket demand for vague errors throughout the product.

### 47. Data-Heavy Interfaces
For tables, dashboards, admin systems, analytics, and enterprise products, evaluate:

- **Finding:** search, filters (with visible active-filter chips and "Clear all"), sorting (with visible sort direction), saved views
- **Navigating:** pagination vs. infinite scroll vs. virtualization (pagination for tasks needing position/return; never infinite scroll above a footer users need), result count, sticky headers, sticky first column
- **Shaping:** column visibility, column order, column width, density (Rule 33)
- **Acting:** row selection, select-all-across-pages semantics made explicit, bulk actions (Rule 34), export
- **States:** empty, no results, loading, error, partial data (Rule 37)
- **Values:** long values (truncate + reveal), missing values (`—` with meaning, not blank or `null`), consistent number alignment (right-aligned, tabular figures), units in headers

```
Columns ▾
  ✓ Name
  ✓ Status
  ✓ Owner
  ✓ Created
  ✓ Updated
    Internal ID
```

This beats permanently displaying every possible field. Preserve filters, sort, and scroll position when the user navigates into a row and back.

### 48. Trust & Transparency
Before committing, users should understand:
- what will happen next, and what an action changes,
- whether it's reversible or permanent,
- why a permission is needed (ask in context, at the moment of need — not all upfront),
- what data is collected and what will be shared,
- what they're paying, when, and for how long (including renewals and the full price before the final step),
- what happens after cancellation (access until period end? data retained?).

Never hide important consequences behind visual tricks (low-contrast fine print, collapsed fee details, pre-scrolled terms). Ethical defaults are covered in Rule 7; dark-pattern tests in Rules 19 and 26.

### 49. Validate With Real Users
Rules are hypotheses about users; testing checks them.
- Small rounds of task-based testing (often starting around five participants) can expose useful problems, but do not guarantee that most defects or affected user groups are covered. Choose participants and sample size for the tasks, diversity, risk, and research goal; iterate on findings.
- Include users with disabilities and assistive-technology users when possible; automated accessibility checkers catch only a fraction of issues.
- Use card sorting and tree testing for IA (Rule 31); first-click and 5-second tests for hierarchy (Rule 1).
- Measure outcomes (task success, time on task, error rate), not just preference.
- A design that looks good to the team but hasn't been watched in use is unvalidated — say so in reviews and name the riskiest untested assumption.
