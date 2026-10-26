# Review report — compact by default

Use the [authoritative verdict mapping](../SKILL.md#severity). Compactness changes presentation, not investigation depth, evidence, or disclosure. Honor a requested format. Use [detailed-report.md](detailed-report.md) for `--detailed` or a natural-language request for a full report; otherwise use the layout below.

## Default layout

```text
<VERDICT> — <one-sentence reason>. Risk: <LOW / MEDIUM / HIGH>.
Target: <repo, target kind, comparison and snapshot identifiers>.

<Findings, most consequential first; omit this block if there are none.>

Verification: <checks and outcomes; relevant trace/coverage evidence>.
Not verified: <limitations and their implications, or “none” only when justified>.
Review basis: <convention sources and references applied; budget exceptions>.
<Provider, policy, or follow-up lines only when applicable.>
```

When no confirmed blockers exist, say so without implying that an incomplete review is approved. A clean review needs no executive summary, empty findings list, praise section, or repeated final assessment. Do not add a sentence merely to reach a length or bullet quota.

## Finding format

Each finding is one paragraph or bullet, expanded only when the failure needs explanation:

```text
[HIGH] <title> — <file:line> (Confirmed). Given <inputs/state>, <observed behavior> causes <consequence>. Fix: <smallest useful correction>. <Supporting caller/reference when relevant.>
```

Every finding retains location, observed problem, concrete impact, recommendation, and confidence. Anchor unchanged-caller regressions to the causal change and cite the caller. Separate conditional Likely findings from confirmed blockers. Needs Verification items are questions, not defects. Group shared root causes; do not omit distinct verified defects to meet a finding-count limit.

## Required context in every prose report

Combine related fields into short lines instead of repeating them across sections:

- **Target:** repository and target kind. Committed reviews record base ref/SHA, head SHA, merge-base SHA, base-selection source, and ref freshness. Local reviews record baseline SHA or empty baseline, staged/working-tree scope, and observed snapshot changes; a baseline SHA does not preserve prior local content.
- **Verification:** actual checks, their outcomes and snapshot, important traced behavior, and unrun/partial checks. Report observed evidence, not just a list of checklist names. Material limitations belong under **Not verified** and affect the verdict as defined in SKILL.md.
- **Review basis:** convention sources and stack/checklist references used, including reasons for exceeding reference budgets.
- **Provider context, only when supplied/attempted:** identity/URL, retrieval time or supplied provenance, metadata SHAs, collection completeness, and CI-to-snapshot relationship. See the [provider workflow](../workflow/provider-context.md); metadata already recorded under Target need not be repeated.
- **Opted-in policy only:** summarize which applicable team/style checks passed, failed, or remain unverified, and disclose exclusions. Identify failures and uncertainty by rule. Detailed mode uses the full team compliance table. Team and Google-style opt-ins remain independent.
- **Follow-up only when useful:** missing test scenarios, questions, relevant pre-existing problems, or optional suggestions. Label these clearly, avoid duplicating findings, and state required human approval when applicable.

For INCOMPLETE, identify the unresolved evidence and the next action needed. Known blockers remain REQUEST CHANGES even when other areas are incomplete. Neither format posts a review or changes provider state.
