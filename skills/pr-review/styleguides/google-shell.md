# Google Shell Style Guide — Review Checklist

Source: [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [When shell is the wrong tool](#when-shell-is-the-wrong-tool) · [Formatting](#formatting) · [Naming](#naming) · [Structure](#structure) · [To flag](#to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google Bash policy. Identify the shebang and shell version first; POSIX sh lacks arrays, [[, and process substitution. Preserve scripts that intentionally target another shell under project policy.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## When shell is the wrong tool
- The Google shell policy targets Bash. Large/complex scripts may benefit from a structured language, but line count alone is not a defect or a reason to rewrite an established project tool. Apply the repository’s interpreter and maintenance policy.

**Application and exceptions:** Judge migration suggestions by demonstrated complexity and maintenance needs, not an automatic line count.

## Formatting
- 2-space indentation, no tabs (except `<<-` heredocs). 80-column lines.
- `; then` / `; do` on the same line as `if` / `for` / `while`. Long pipelines: one segment per line, `|` leading.
- Tooling: ShellCheck — skip what it enforces in CI.

**Application and exceptions:** Indent heredoc content according to its intended output, and do not change significant literal whitespace.

## Naming
- Functions and variables `lower_with_under`; constants and exported variables `UPPER_WITH_UNDER`, declared `readonly`.
- Function-local variables declared with `local`.

**Application and exceptions:** Use local within Bash functions; constants/exported environment variables differ from mutable locals. Avoid overwriting system environment variables.

## Structure
- File header comment. Comments on non-trivial functions covering globals, arguments, outputs, and return values.
- All functions together after constants; a `main` function called last as `main "$@"` when there is more than one function.
- Errors go to STDERR.

**Application and exceptions:** Document inputs, outputs, global mutations, and exit codes of non-obvious functions. main "$@" preserves argument boundaries.

## To flag
- Unquoted variable expansions and command substitutions. **(bug risk)**
- `$*` where `"$@"` is meant. **(bug risk)**
- Backticks instead of `$(…)`.
- In Bash, prefer [[ … ]] for explicit conditional syntax under this policy. POSIX sh has no [[ … ]]; quoted test/[ can be correct. Report actual splitting/globbing or comparison failures separately.
- `let`, `expr`, `$[…]` instead of `(( … ))`.
- Bare `*` globs — use `./*` so filenames starting with `-` are not read as flags. **(bug risk)**
- `eval`. **(bug risk)**
- Piping into `while` (the loop runs in a subshell and loses variables) — use process substitution or `readarray`. **(bug risk)**
- Lists stored in a space-joined string instead of an array. **(bug risk)**
- Return values not checked — `if`, `$?`, or `PIPESTATUS` for pipelines. **(bug risk)**
- External commands where a builtin or parameter expansion would do.
- SUID/SGID on scripts.

**Application and exceptions:** Reproduce failures with spaces, wildcard characters, leading dashes, and command failure. Quoting and -- prevent many argument-boundary problems, but validate values before passing them as shell code.

## Example and review decision

```bash
# Unsafe splitting/globbing:
cp $source $destination
# Preserve two path arguments; protect leading dashes when cp supports --.
cp -- "$source" "$destination"
```

Quote variables in POSIX sh too. [[ is a Bash policy choice, not a portable replacement for every test command.
