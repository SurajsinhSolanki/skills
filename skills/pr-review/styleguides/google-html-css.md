# Google HTML/CSS Style Guide — Review Checklist

Source: [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [General](#general) · [HTML — to flag](#html--to-flag) · [CSS — to flag](#css--to-flag) · [Additional local conventions](#additional-local-conventions) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google HTML/CSS style for the project’s HTML/CSS dialect. JSX, templates, CSS modules, and formatter output may impose different syntax; do not apply raw-HTML casing blindly to components.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## General
- HTTPS for every embedded resource. **(bug risk: mixed content)**
- 2-space indentation, lowercase element and attribute names, no trailing whitespace, UTF-8 (`<meta charset="utf-8">`).
- No fixed line limit; wrapping long lines is optional.

**Application and exceptions:** HTTPS avoids mixed content for network resources; relative URLs, data assets, and documented development origins need context.

## HTML — to flag
- Missing `<!doctype html>`; invalid markup without a stated reason.
- Elements used against their meaning (a `div` as a button, headings for styling). **(bug risk: accessibility)**
- Images without `alt`; media without captions or transcripts. **(bug risk: accessibility)**
- Inline styles and scripts mixed into markup instead of separate files.
- Entity references where the literal UTF-8 character would do (except `<`, `&`, and invisible characters).
- Redundant text/css or text/javascript type attributes. Keep type="module" and meaningful non-default content types.
- Single-quoted attribute values — use double quotes.
- Styling hooked to `id`s — use classes.

Omitting optional tags is allowed by the guide but not required — do not flag either way.

**Application and exceptions:** Semantic controls and empty alt text for genuinely decorative images can be correct. Keep type="module"; remove only redundant content-type annotations.

## CSS — to flag
- Invalid CSS without a browser-bug reason.
- Class names that describe appearance rather than purpose; words not separated by hyphens.
- ID selectors; type-qualified class selectors (`div.error`).
- `!important` and user-agent hacks.
- Unnecessary units on zero lengths; preserve units required by the property’s grammar (for example zero time durations). The verified Google CSS convention includes a leading zero on fractional values (`0.8em`); follow configured project formatting.
- 6-character hex where 3 would do; longhand where a shorthand would do.
- Missing semicolon after the last declaration; no space after the colon.
- Several selectors on one line; no blank line between rules.
- Double quotes in CSS (use single quotes); quoted `url()` values.

**Application and exceptions:** Selector specificity and !important may intentionally override a constrained third-party system. Check the actual cascade and grammar; zero time values may require units.

## Additional local conventions

Documentation: explain non-obvious browser workarounds and required cascade constraints locally. HTML/CSS have no language import-order policy here beyond the actual stylesheet/script dependency order.

## Example and review decision

```html
<!-- Defect: click-only generic element has no native keyboard button behavior. -->
<div onclick="save()">Save</div>
<!-- Better native semantics; wire the handler through project conventions. -->
<button type="button">Save</button>
<script type="module" src="app.js"></script>
```

CSS `.notice { opacity: 0.8; }` illustrates the guide’s fractional-zero convention; it is style, not a runtime bug.
