# Team Standards — Python

Opt-in only, like `team.md`. Load when the project opted in to team standards **and** the diff touches `.py` files. Applies on top of `team.md` and `frameworks/python.md`. Severity and precedence rules are in `team.md`: style is SHOULD (`[LOW]`, grouped, never blocking), tests are MUST (`[HIGH]`, blocking).

Use the target-aware `review_diff`, `review_read`, `review_files`, and `review_grep` helpers in [../workflow/git-review.md](../workflow/git-review.md#step-7--reviewing-local-targets). For working-tree reviews, also inspect untracked files: diff-based checks do not include them. For unborn HEAD/conflicted index, follow that workflow's special handling rather than these helpers.

## First: what does tooling already enforce?

Read the repo's linter, formatter, and type-checker config before checking style by hand:

```bash
for f in pyproject.toml setup.cfg tox.ini .flake8 .pylintrc .pre-commit-config.yaml; do
  review_read "$f" 2>/dev/null | grep -nE 'line-length|max-line-length|^\[tool\.(ruff|black|isort|mypy|pylint)|select|convention|strict' \
    | sed "s|^|$f: |"
done
```

If a configured tool enforces a rule **and CI runs it**, skip that rule here — do not report it per line. Typical mapping: ruff `E501`/black -> line length, ruff `I`/isort -> import order, ruff `N`/pep8-naming -> naming, ruff `D`/pydocstyle -> docstrings, mypy strict -> type hints.

If the repo's configured value differs from the team rule (e.g. a different line length), the repo wins. Note the discrepancy once in the team-policy results.

## Helper

All checks below report `file:line` for lines **this change added**, so findings never land on code the author did not write:

```bash
added() {  # usage: added '<awk regex>' <pathspec>...
  review_diff -U0 -- "${@:2}" | awk -v re="$1" '
    /^\+\+\+ /{f=substr($0,7); next}
    /^@@/{split($3,a,/[,+]/); n=a[2]-1}
    /^\+/{n++; if (substr($0,2) ~ re) print f":"n": "substr($0,2)}'
}
```

Every hit is a *candidate*. It still goes through Phase 6 verification in `SKILL.md`.

### Test and migration locations — discover, don't assume

Projects lay these out differently. Find them, then use the pathspecs below in every command:

```bash
review_files | grep -iE '(^|/)(migrations?|migrate|alembic)/'   # migration dirs, if any

TESTS=(':(glob)**/test_*.py' ':(glob)**/*_test.py' ':(glob)**/tests/**' ':(glob)**/conftest.py')
NOT_TESTS=(':(exclude,glob)**/test_*.py' ':(exclude,glob)**/*_test.py' ':(exclude,glob)**/tests/**' ':(exclude,glob)**/conftest.py')
NOT_MIGRATIONS=(':(exclude,glob)<migration_dir>/**')   # one entry per dir found above; empty array if none
```

The test patterns are pytest's own discovery defaults. If the project configures `testpaths` or `python_files` differently (in `pyproject.toml`, `pytest.ini`, `setup.cfg`, or `tox.ini`), use its settings instead.

## Style — SHOULD (Google Python Style Guide + PEP 8)

The full Google Python checklist is in [../styleguides/google-python.md](../styleguides/google-python.md) and loads only with a separate Google-style opt-in. The team-specific rules below apply through the team opt-in alone; where they differ from Google (line length), this file wins.

### Line length — max 120 (unless repo config says otherwise)

```bash
LIMIT=120   # use the repo's configured value if it has one
review_diff -U0 -- '*.py' | awk -v L=$LIMIT '
  /^\+\+\+ /{f=substr($0,7); next} /^@@/{split($3,a,/[,+]/); n=a[2]-1}
  /^\+/{n++; if (length($0)-1 > L) print f":"n": "length($0)-1" chars"}'
```

Long URLs, long string literals that cannot be split, and generated files are acceptable exceptions.

### Naming — `lower_case_with_underscores` functions and variables, `CamelCase` classes

```bash
added '^[[:space:]]*(async[[:space:]]+)?def[[:space:]]+[a-z0-9_]*[A-Z]|^[[:space:]]*class[[:space:]]+[a-z_]' '*.py'
```

Exceptions: overrides of third-party methods that are camelCase by API (`setUp`, `visit_FunctionDef`), and names mirroring an external schema.

### Imports — top of file, three groups (stdlib, third-party, local), alphabetized, blank line between groups

```bash
added '^[[:space:]]+(import|from)[[:space:]]+[a-zA-Z_.]+' '*.py' "${NOT_TESTS[@]}"
```

This finds indented (mid-file) imports. **Not violations:** imports under `if TYPE_CHECKING:`, inside `try/except ImportError` for optional dependencies, or deliberately deferred to break an import cycle or avoid a heavy import at startup — check the surrounding lines before reporting. Group order and alphabetizing are checked by reading the changed import blocks, unless isort/ruff `I` enforces them.

### Docstrings — Google style for public modules, classes, functions, and methods

New public definitions without a docstring (private `_names`, tests, and migrations excluded — uses the pathspecs from the discovery step):

```bash
review_diff -U0 -- '*.py' "${NOT_TESTS[@]}" "${NOT_MIGRATIONS[@]}" | awk '
  /^\+\+\+ /{f=substr($0,7); next} /^@@/{split($3,a,/[,+]/); n=a[2]-1}
  /^\+/{n++; line=substr($0,2)
    if (pend) { if (line !~ /^[[:space:]]*(r|u)?("""|\047\047\047)/) print pf":"pn": "pd; pend=0 }
    if (line ~ /^[[:space:]]*((async[[:space:]]+)?def[[:space:]]+[a-zA-Z][a-zA-Z0-9_]*\(|class[[:space:]]+[A-Z])/ && line ~ /:[[:space:]]*$/) { pend=1; pf=f; pn=n; pd=line } }'
```

Multi-line signatures are not caught by this check; read those by hand. Where a docstring exists, check it has `Args:`, `Returns:`, and `Raises:` sections when the function takes arguments, returns a value, or raises deliberately. Prioritize docstrings on complex logic; a one-line docstring is enough for a trivial helper.

### Type annotations — encouraged

New public functions without parameter or return annotations: `[SUGGESTION]`. Becomes `[LOW]` if the repo runs a strict type checker that the code would fail.

### Comments

Prefer self-explanatory code; complex logic should carry a short comment explaining *why*. Flag only complex, non-obvious logic with no explanation at all — not missing comments in general.

## Tests — MUST (Pytest, unit and end-to-end)

### Which changed modules have tests?

```bash
review_diff --name-only -- '*.py' "${NOT_TESTS[@]}" "${NOT_MIGRATIONS[@]}"   # changed source
review_diff --name-only -- "${TESTS[@]}"                                      # changed tests
review_grep '<module_or_symbol>' "${TESTS[@]}"                                 # who tests a module
```

### Unit tests — MUST

New or changed behavior needs a unit test that exercises it. Missing: `[HIGH]`, **REQUEST CHANGES**. Name the untested function and the scenario that should be covered.

Not required for: pure pass-through or wiring code, configuration, type-only changes, migrations, and renames with no behavior change. Do not demand tests for code with no behavior to test.

### End-to-end tests — MUST when the workflow changes

The team defines an end-to-end test as running the tool on a small test dataset through the whole workflow. Find the suite:

```bash
review_files | grep -iE '(^|/)(e2e|end_to_end|end-to-end)(/|_|\.)'
review_grep 'mark\.e2e\|mark\.end_to_end\|mark\.integration' "${TESTS[@]}"
```

Repos name it differently — an `integration` suite that drives the full app counts if it runs the real workflow end to end. Judge by what the test does, not its folder name.

- The change alters the end-to-end workflow (inputs, outputs, pipeline stages, file formats, CLI or API flow) and no end-to-end test covers it: `[HIGH]`, **REQUEST CHANGES**.
- The repo has **no** end-to-end suite at all: *Pre-existing*, not the author's fault — note it in the policy results. It becomes MUST only if this PR creates the project or the tool.

### Pytest usage — SHOULD

- New tests use pytest style (plain `assert`, fixtures), not `unittest.TestCase`, unless the file already uses it: `added 'unittest\.TestCase|self\.assert' "${TESTS[@]}"`.
- Repeated test bodies differing only in values belong in `@pytest.mark.parametrize`.
- Shared setup belongs in fixtures, not copied between tests.
- Assertions are specific (compare exact values or exception types), not just "no exception raised".

### Running them

Follow *Running the project's gates* in `SKILL.md`: use the selected-target execution and failure-attribution rules, including dirty-tree restrictions. Otherwise mark *tests not run for this target*.

## Policy results when this file was loaded

Summarize these checks and exceptions in compact mode; add these rows to the team table in detailed mode.

| Area | Rule | Status | Notes |
|---|---|---|---|
| Python style | 120 cols, naming, imports | pass / N findings / enforced by `<tool>` | |
| Docstrings | Google style on public API | pass / N missing / enforced by `<tool>` | |
| Type hints | encouraged | ok / suggestions | |
| Unit tests | required for new behavior | pass / fail | |
| End-to-end tests | required when workflow changes | pass / fail / n/a / no suite (pre-existing) | |

For what compliant code looks like, see [team-python-example.md](team-python-example.md). Open it only when a style judgment is borderline.
