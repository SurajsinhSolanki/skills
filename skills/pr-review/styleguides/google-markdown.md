# Google Markdown Style Guide — Review Checklist

Source: [Google Markdown Style Guide](https://google.github.io/styleguide/docguide/style.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; the applicable review guidance is summarized locally in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Load when the change is substantially documentation — a new or rewritten doc — not for a one-line README tweak.

Contents: [Scope and offline use](#scope-and-offline-use) · [To flag](#to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google Markdown policy for substantial documentation changes. Inspect the target renderer (CommonMark, GitHub, or project extensions) and documentation linter. Raw HTML, tables, and a TOC directive have renderer-dependent behavior. Source snapshot checked: **2026-10-26**; the source link is optional attribution.

Apply changed-line style rules only when opted in; project rules and configured formatting win. All checks and examples are local. Style alone is non-blocking; broken rendering/links need an actual affected consumer or renderer.

## To flag
- More than one H1, or a document that does not open with its H1 and a short introduction.
- Setext (underlined) headings — use ATX `#`. Headings that are not unique and descriptive, or lack a blank line before and after.
- Lines over 80 characters in prose (links, tables, headings, and code blocks excepted).
- Trailing whitespace used for line breaks — use a backslash.
- Nested list items not indented 4 spaces.
- Fenced code blocks without a language; long shell commands without backslash line continuations.
- Link text such as "here" or "this link" — make it descriptive. Full URLs to the same repo where a path would do; long or repeated URLs not turned into reference links.
- Images without descriptive alt text.
- Tables used for irregular data a list would express better.
- Raw HTML where Markdown would do.

**Application and exceptions:** Preserve code literals and semantic line breaks. Use relative links only when the output’s path resolution supports them. Validate heading anchors and rendering with the actual renderer; do not assume every extension supports identical IDs. List indentation depends on the marker/content width as well as adopted style. A useful doc comment explains why readers cannot follow or execute the documented steps, rather than requesting cosmetic rewrapping already handled by tooling.

## Example and review decision

````markdown
# Deploying the service

Run the existing deployment check:

```bash
make check-deploy
```

Read the [configuration reference](configuration.md).
````

The command and file are illustrative project context, not prescribed dependencies. A real review verifies that the referenced command/file exists in the selected snapshot. Use descriptive link text and a fence language; do not follow external links merely to apply these rules.
