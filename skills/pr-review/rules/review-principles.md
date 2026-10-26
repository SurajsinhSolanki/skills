# Review Principles

## Review the change, not the codebase

Judge the diff against the code it lands in. Unchanged pre-existing problems belong in a separate, non-blocking note when relevant. If the change materially worsens one, evaluate the introduced regression and its impact.

## Requirement first, code second

Review against available requirements rather than reconstructing intent from the implementation. Confirmed wrong business behavior is blocking; missing material requirements are a verification gap, not proof of a defect.

## Consistency beats preference

If the codebase has an established pattern, the change should follow it. "I would have done it differently" is not a finding. A divergence needs a concrete maintenance consequence or an applicable documented rule to warrant a finding; difference alone is insufficient.

## Signal density

Prioritize consequential, evidence-backed findings and deduplicate root causes. Remove unsupported or low-value commentary, not distinct verified defects. Report length follows the actual change, with no finding-count quota.

## Say what you verified

State what you traced and what you could not. "I did not verify the migration against production data volume" is useful. Silent gaps are not.

## Be direct and specific

Point at the line. Describe the failure. Propose the fix. State uncertainty explicitly when evidence is incomplete; avoid lectures and praise padding.

## Do not rewrite the PR

Recommend the smallest change that resolves the finding. Redesign proposals belong in a follow-up ticket, not a merge gate.

## Respect the author's decision

If the author explains a tradeoff and the reasoning is sound, accept it and record it. Repeating a rejected finding is noise.
