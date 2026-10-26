# Google Style Guides — Index

## Offline contract

Every language file includes the applicable local conventions, exceptions, review-decision guidance, and an example. Source URLs are optional attribution/maintenance links; following them is unnecessary to apply the file. These are review-focused source snapshots, not complete language manuals or promises about future releases. Read compiler/formatter/framework versions and project overrides locally; disclose unsupported version-sensitive rules. Source-check dates live in the guides.


**Opt-in only.** Use this folder only when the project opted in to Google style: `style: google` in its `.pr-review` file, its docs or config saying it follows Google style, or the user asking for it in the review. Without that, style is judged purely against the project's own config, docs, and surrounding code, and nothing here applies.

Use a default budget of three guide files per review, prioritizing risk and changed lines. Load more for concrete concerns and explain exceptions in Review basis; disclose omitted coverage. Markdown, JSON, and XML guides only when the change is substantially a document or a data contract.


Load the Google guide for each language in the diff:

| Changed files | Load |
|---|---|
| `.py` | [google-python.md](google-python.md) |
| `.java` | [google-java.md](google-java.md) |
| `.kt`, `.kts` | [google-kotlin.md](google-kotlin.md) |
| `.js`, `.mjs`, `.cjs`, `.jsx` | [google-javascript.md](google-javascript.md) |
| `.ts`, `.tsx` | [google-typescript.md](google-typescript.md) |
| Angular (`*.component.ts`, `angular.json`) | [google-angular.md](google-angular.md), on top of TypeScript |
| `.go` | [google-go.md](google-go.md) |
| `.cc`, `.cpp`, `.cxx`, `.hpp`, `.h` (C++) | [google-cpp.md](google-cpp.md) |
| `.cs` | [google-csharp.md](google-csharp.md) |
| `.sh`, `.bash`, Bash shebang | [google-shell.md](google-shell.md) |
| `.html`, `.css`, `.scss` | [google-html-css.md](google-html-css.md) |
| `.swift` | [google-swift.md](google-swift.md) |
| `.m`, `.mm`, `.h` (Objective-C) | [google-objc.md](google-objc.md) |
| `.dart` | [google-dart.md](google-dart.md) |
| `.R`, `.Rmd` | [google-r.md](google-r.md) |
| `.hs` | [google-haskell.md](google-haskell.md) |
| `.lisp`, `.lsp`, `.cl` | [google-lisp.md](google-lisp.md) |
| `.vim`, `vimrc` | [google-vim.md](google-vim.md) |
| JSON contracts (API shapes, schemas) | [google-json.md](google-json.md) |
| Markdown docs (substantial changes) | [google-markdown.md](google-markdown.md) |
| XML formats and schemas | [google-xml.md](google-xml.md) |

A `.h` file is Objective-C if `.m`/`.mm` files sit beside it, C++ otherwise.

Report this pass under **Google Style**, independently of **Team Standards**. A style-only opt-in does not activate team-policy checks.

## Applying guides

- **Only new and changed lines.** Never ask the author to restyle code they did not touch.
- **Tooling first.** If a configured formatter or linter enforces a rule in CI (`gofmt`, `google-java-format`, `clang-format`, Black, Prettier, ESLint, ShellCheck, `swift-format`, `dart format`, `styler`), skip that rule.
- **The repo wins.** If the repo's config or established convention differs from Google's (line length, quote style, exceptions in C++, a JSON envelope), follow the repo and note the difference once in the report's **Review basis** line (and in the team-policy results too, if team standards are also on). Do not file per-line findings for it.
- **Severity.** Style findings are `[LOW]`, grouped one finding per rule with up to five locations. Items marked **(bug risk)** in a guide can be reported at a higher severity when Phase 6 confirms a concrete failure.
- **Languages without a Google guide** (Ruby, PHP, Rust, SQL, Elixir, Scala, and others): no guide for those languages is bundled in this skill. Check style only through the repo's own formatter or linter config (for example RuboCop, PHP-CS-Fixer or PSR-12, rustfmt and Clippy, sqlfluff), and say in the **Review basis** line that no Google guide applies.
