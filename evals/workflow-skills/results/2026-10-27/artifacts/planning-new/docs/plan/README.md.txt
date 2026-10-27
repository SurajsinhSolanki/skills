# Display-name validation roadmap

Reject blank display names using the existing `Profile` class. Preserve valid
input exactly, raise `ValueError` for blank names, and preserve the stored name
when a rename is rejected, as required by the [project contract](../../README.md).

This is a saved implementation plan. Application code and tests have not been
changed. There was no existing roadmap format or task history to extend.

| Phase | Task | Status | Dependencies |
| --- | --- | --- | --- |
| [1 — Enforce the profile contract](phase-1.md) | [P1-T001 — Reject blank names](phase-1.md#p1-t001--reject-blank-names) | Ready | None |

Execution order: complete P1-T001, including its focused and regression checks.
Next ready task: P1-T001. No implementation work is complete.

`Ready` means the task has enough evidence and decisions to implement. `Done`
requires all task acceptance criteria and verification evidence; writing this
plan does not satisfy them.

Scope decisions: the nonblank contract applies to explicit constructor names
as well as renames because both set the display name. Blank means an empty
string or a string whose `str.strip()` result is empty. Use that result only to
check blankness; retain the original valid string. Non-string input behavior is
outside this change. No unresolved decision blocks this scope.

Evidence from 2026-10-27: the existing two-test suite passed, but it contains no
blank-name cases. Direct local calls confirmed both entry points currently
accept empty and whitespace-only strings. These are baseline observations,
not verification of the proposed fix.
