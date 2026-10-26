# Detailed review report

Use for `--detailed` or an explicit request for a full report. Apply the same finding requirements, metadata, confidence, and limitations as the [compact report](review-report.md). Detail expands explanations and organization; it does not change verdict thresholds or create extra findings.

## Verdict and review context

Lead with the verdict and its reason. Include the Target, Verification, Not verified, Review basis, and applicable Provider context defined in the compact report. Organize this metadata as labeled lines or a small table. If a separate Verification section below is clearer, place check results there once.

## Findings

Group findings by blocking versus non-blocking when that helps navigation. For each, include severity, title, causal location, confidence, problem, concrete impact, supporting evidence, and the smallest recommended fix. Use a paragraph for straightforward defects or labeled fields for complex ones.

Confirmed CRITICAL/HIGH defects and introduced applicable MUST violations belong under Blocking Issues. Explicitly conditional Likely findings remain separate. Do not list the same root cause under both findings and test gaps.

If there are no findings, state that briefly and omit empty issue sections. Do not manufacture findings or summary bullets to fill this template.

## Verification and remaining work

Describe commands and outcomes against the correct snapshot, behavior/call paths traced, and material coverage limits. Include relevant missing tests, questions for the author, pre-existing issues, and optional suggestions only when useful and clearly labeled. State the evidence needed to resolve an incomplete assessment.

## Opted-in policy

- **Team Standards:** only with team opt-in, use the compliance table in [standards/team.md](../standards/team.md), plus rows from loaded language policies. Confirmed introduced MUST violations also appear in findings.
- **Google Style:** only with Google-style opt-in, list languages/guides checked and their results, tool coverage, exceptions, and unverified areas. This never enables team-policy checks.

## Assessment

Add strengths or a final assessment only when they add information beyond the opening verdict and findings. Explain material tradeoffs, remaining risks, or required human approval without repeating the report. There is no minimum number of sections or bullets.
