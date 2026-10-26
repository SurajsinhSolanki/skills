# Google Vim script Style Guide — Review Checklist

Source: [Google Vimscript Style Guide](https://google.github.io/styleguide/vimscriptguide.html) (CC-BY 3.0, Google). Optional attribution and maintenance reference; all review rules below are bundled locally and summarized in original wording.

Apply the shared opt-in, precedence, reporting, and bug-risk rules in the [style guide index](README.md#applying-guides).

Contents: [Scope and offline use](#scope-and-offline-use) · [Formatting](#formatting) · [To flag](#to-flag) · [Example and review decision](#example-and-review-decision)

## Scope and offline use

Google legacy Vimscript policy; check Vim/Neovim version and script dialect. Vim9script and Lua plugins have different semantics and are outside these legacy rules.

Apply only when opted in and on changed lines. Project rules/formatter output take precedence. Style observations are non-blocking; bug-risk markers need a concrete verified failure. No external page is required to apply this file. Source snapshot checked: **2026-10-26**.

## Formatting
- 2-space indentation, continuation lines +4, 80-column lines, spaces around operators.

**Application and exceptions:** Maintain the configured indentation and literal regex contents; accidental escaping can change matching behavior.

## To flag
- `=~` or `==` without an explicit case modifier — use `=~#` / `=~?` and `==#` / `==?`. **(bug risk)**
- Regexes not starting with `\m\C` (they then depend on user settings). **(bug risk)**
- `normal` instead of `normal!` (user mappings leak in). **(bug risk)**
- `:substitute` in plugin code where a function such as `search()` would do; matching locale-dependent error text instead of error codes. **(bug risk)**
- Autoloaded functions missing `!` or `abort`; plugin commands defined with `!` (silently overwrite user commands).
- Autocommands outside a uniquely named `augroup` cleared with `autocmd!`. **(bug risk: duplicate handlers on reload)**
- `:set` / `&` where `:setlocal` / `&l:` is meant. **(bug risk)**
- Variables without a scope prefix (`g:`, `s:`, `a:`, `l:`, `b:`, `w:`).
- Double-quoted strings without escape sequences — use single quotes.

**Application and exceptions:** Test with user mappings and ignorecase settings enabled. Set options locally when the plugin intends buffer/window scope; keep global changes deliberate. Use autoload/script-local names and unique augroups to avoid reload collisions.

## Example and review decision

```vim
" Stable comparison independent of the user’s ignorecase setting.
if a:name ==# 'ready'
  return 1
endif
```

Document public commands/options in plugin help. This legacy fragment belongs inside a function; do not require a Vim9 module to use legacy a:/l: argument scopes.
