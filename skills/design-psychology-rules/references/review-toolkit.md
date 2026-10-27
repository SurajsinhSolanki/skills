# Review Toolkit

Tools for formal or full-screen design reviews. Rule numbers refer to [psychological foundations](rules.md) (1–26) and [UI/UX quality](ux-quality.md) (27–49). Follow the [skill's scope and evidence rules](../SKILL.md#scope-and-evidence).

---

## Feature Accessibility Matrix

Run for major features within the review's scope. Mark each cell ✅ pass / ⚠️ partial / ❌ fail / ? not verified / — not applicable, with evidence or a one-line explanation. Partial means evidence establishes incomplete support; not verified means evidence is missing. Use not applicable only with a reason, not to hide a missing check. A screenshot does not prove keyboard, semantic, or assistive-technology behavior.

| Question | Pass condition | Rule |
|---|---|---|
| Can users find it? | Obvious location or search path | 28, 32 |
| Can users recognize it? | Clear label/icon | 28, 46 |
| Can users understand it? | Purpose is clear before activation | 28 |
| Can users reach it? | No unnecessary layers or barriers | 27, 29 |
| Can users operate it? | Mouse, touch, keyboard, and speech as applicable; visible labels represented in accessible names | 11, 42 |
| Can users see its state? | State is clearly communicated (visually and to AT) | 37, 42 |
| Can users recover? | Undo / cancel / retry where appropriate | 40, 41 |
| Does it work responsively? | Mobile / tablet / desktop considered | 43 |
| Is it accessible? | Applicable checks, including any hover/focus content, evidenced at the recorded target; exceptions considered | 42 |
| Is it consistent? | Matches established patterns in the product | 20, 21 |
| Is advanced functionality discoverable? | Progressive disclosure is clearly signposted | 29, 30 |
| Is user control preserved? | No traps or deceptive patterns | 26, 40, 48 |

Example (compact form): the export menu is keyboard-tested and cannot receive focus; observed running export gives no feedback. Overflow is labeled, and three navigation steps are established project convention, so neither is a defect by itself. Responsive behavior has not been tested; this control exposes no advanced settings.

| Feature | Find | Recog. | Underst. | Reach | Operate | State | Recover | Resp. | A11y | Consist. | Adv. disc. | Control |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Export CSV | ✅ labeled overflow | ✅ | ✅ | ✅ established path | ❌ menu not keyboard-reachable | ❌ no feedback | ✅ tested retry | ? not tested | ❌ keyboard failure | ✅ | — none | ✅ |

---

## Edge-Case Sweep

Walk the screen through applicable conditions and note what the user sees (full list with detail: [Rule 44](ux-quality.md#44-edge-cases)). Mark unavailable runtime checks not verified; do not invent outcomes for untested states.

- [ ] 0 items · 1 item · many items (10,000+)
- [ ] Very long / very short text · unbroken strings · missing images · missing fields
- [ ] Slow network · offline · API failure · partial results
- [ ] Unknown progress duration · repeated fields with security/expiry constraints · privacy-sensitive authentication errors
- [ ] Permission denied · read-only · expired session
- [ ] Large text (200%) · small viewport (320 px) · dark mode / forced colors
- [ ] Keyboard-only · screen reader · touch-only
- [ ] Translated text 40% longer · RTL
- [ ] Concurrent edit · stale data

---

## Review Report Template

Use for formal reviews. For quick questions, a few targeted bullets are enough. Omit empty issue sections. Record the artifact, evaluated flow, accessibility target, and what was actually inspected or tested.

Choose the assessment for the reviewed scope:

- **Not ready:** a confirmed blocker, including an applicable accessibility-criterion failure after checking exceptions. Known blockers remain blockers even when other areas are unknown.
- **Insufficient evidence:** no confirmed blocker, but missing material evidence prevents a ship decision. Name the missing evidence and how to obtain it.
- **Ship with fixes:** sufficient evidence for the reviewed scope, with non-blocking issues to address.
- **Ship:** sufficient evidence for the reviewed scope and no confirmed issues; suggestions alone do not block. This is not whole-product approval or a WCAG conformance certification.

Do not certify an untested mockup or let unchecked matrix cells imply a pass. Missing nonessential evidence may remain a disclosed limit without forcing an insufficient-evidence assessment. Keep hypothetical conditions as verification questions, not confirmed findings.

```markdown
## Design review: <screen / flow>

**User goal:** <what the user is trying to do>
**Primary actions:** <actions supporting that goal; identify missing context as an assumption/question>
**Evidence and scope:** <artifact/version, flow, supplied requirements, inspected source, actual tests>
**Accessibility target:** <WCAG 2.2 AA by default, or explicit project target; applicable exceptions>
**Verdict:** Ship / Ship with fixes / Not ready / Insufficient evidence

### Blockers
Confirmed failures of applicable accessibility criteria, demonstrated deception, blocked goals, or data loss.
1. **<Issue and location>** — Rule <n> / criterion <id, level if relevant>. **Evidence:** <observed behavior and exception check>. **Impact:** <consequence to the user>. **Fix:** <concrete change>.

### Major
Significant friction, missing states, discoverability failures.

### Minor
Inconsistencies, copy improvements, small hierarchy issues.

### Polish
Aesthetic refinements that don't affect task success.

### Principle tensions
<Which rules conflict here, and how the conflict hierarchy resolves it.>

### What works
<Keep this — briefly, so good decisions survive the next iteration.>

### Untested assumptions
<Unknown runtime behavior, missing context, scope limits, and what evidence resolves each. Distinguish these from confirmed findings and name user-testing assumptions under Rule 49.>
```

Severity guide:
- **Blocker** — confirmed failure of an applicable accessibility criterion at the recorded target, demonstrated deception, blocked goal, or data loss. Check evidence and exceptions before assigning it.
- **Major** — most users hit friction or confusion, a key state is missing, or an important feature isn't discoverable.
- **Minor** — some users notice; workaround exists.
- **Polish** — optional aesthetic refinement without an established task-success problem. Do not claim a measured lack of effect unless it was measured.
