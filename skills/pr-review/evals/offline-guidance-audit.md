# Offline guidance audit

Completed 2026-10-26. Scope: all 18 framework passes and 21 style guides, plus their indexes and the entry point. The original topic inventory was captured before editing. No original topic was silently dropped; obsolete absolutes were corrected within their existing topic. Rules remain review candidates that require local evidence, with project conventions and independent opt-ins preserved.

## Validation boundary

- External pages were consulted for authoring/maintenance; every technology file now includes local guidance, applicability, examples, caveats, source attribution and a check date. These are scoped review summaries, not complete vendor manuals or a guarantee about future versions.
- Runtime checks: Python 3.14.4, Node 24.16.0, SQLite through Python, Bash, and rustc 1.97.1 were available. The executable guide checks passed. Pydantic is not installed: its runtime check was skipped. Go’s snap wrapper refused to run in this sandbox; no permission or installation changes were attempted.
- Vue/compiler-sfc, Next.js, Angular/RxJS, Pydantic, SQLAlchemy, Django, .NET, Spring, Rails/Laravel, and mobile SDK examples were source/manual checked, not executed as applications. Language snippets needing surrounding project declarations are identified as fragments. No dependency was installed.
- The fixture suite has 32 cases. Source-grounded framework cases are labeled in cases.json. Fixture checks and unit tests do not establish blind agent review quality. Live provider tests and a full multi-runtime compatibility matrix remain outstanding.

## Recorded check results

- Skill validator: passed.
- Local Markdown targets and anchors (excluding illustrative fenced code): 641 checked, all passed.
- Topic inventory: 174 original topics accounted for; 104 expanded and 70 corrected plus expanded. All 39 technology files and both indexes updated.
- Full unit suite: 22 tests collected, 21 passed, 1 skipped because Pydantic is unavailable. Runnable guide checks include Python, Node, SQLite, Bash and Rust.
- Disposable fixture suite: 32 cases built with matching evaluator rubrics and explicit source-only labels for unavailable framework/compiler runtime checks. The cache-identity fixture was additionally executed in Node: baseline passed and changed key failed as expected.
- No blind agent review or live provider validation is claimed by these checks.

## Per-topic disposition

Expanded means the topic gained local application/evidence, correction or exception guidance; corrected + expanded also replaces an inaccurate or overly broad rule. Headings listed below are the original topics. New applicability, examples, navigation and source sections are additional.

| File | Original topic | Disposition | Reason |
|---|---|---|---|
| [frameworks/angular.md](../frameworks/angular.md) | Subscriptions and RxJS — the top defect source | Corrected + expanded | Finite observables and long-lived subscriptions have different lifetimes.; Completed and intentionally persistent sources are exceptions. |
| [frameworks/angular.md](../frameworks/angular.md) | Change detection | Corrected + expanded | OnPush has triggers beyond input identity. |
| [frameworks/angular.md](../frameworks/angular.md) | DI and services | Expanded | Locate provider registration and consumer lifetime. |
| [frameworks/angular.md](../frameworks/angular.md) | HTTP | Expanded | Inspect effective interceptor order and destination allowlists. |
| [frameworks/angular.md](../frameworks/angular.md) | Forms | Expanded | Compare form model, template, and user-visible errors. |
| [frameworks/angular.md](../frameworks/angular.md) | Routing and security | Corrected + expanded | Guards depend on first emission, not stream completion.; Avoid treating all dynamic values as exploitable. |
| [frameworks/angular.md](../frameworks/angular.md) | Consistency | Expanded | Check local migration/configuration intent. |
| [frameworks/django.md](../frameworks/django.md) | ORM | Corrected + expanded | Actual behavior is backend/test-context dependent.; Bulk insert and update do not have identical field behavior. |
| [frameworks/django.md](../frameworks/django.md) | Migrations | Expanded | Inspect historical model access, reverse behavior, table size, and application compatibility across deploy order. |
| [frameworks/django.md](../frameworks/django.md) | DRF and security | Corrected + expanded | Correct DRF list/detail/create permission semantics.; Cross-field validation is not a per-field hook.; Serializer declarations do not alone prove privilege escalation. |
| [frameworks/django.md](../frameworks/django.md) | Views, transactions, signals | Corrected + expanded | Signal behavior depends on save path and sender; avoid architecture mandates. |
| [frameworks/django.md](../frameworks/django.md) | Settings and files | Expanded | Identify production settings selection, reverse proxy behavior, upload storage and cache identity. |
| [frameworks/dotnet.md](../frameworks/dotnet.md) | Async correctness | Corrected + expanded | Task lifetime and scoped dependency lifetime differ. |
| [frameworks/dotnet.md](../frameworks/dotnet.md) | EF Core | Expanded | Locate the context instance and query execution points. |
| [frameworks/dotnet.md](../frameworks/dotnet.md) | Dependency injection | Corrected + expanded | Two documented lifetime patterns are valid.; Container tracking and retention differ from missing disposal. |
| [frameworks/dotnet.md](../frameworks/dotnet.md) | Web pipeline and security | Corrected + expanded | Role-based authorization is valid. |
| [frameworks/dotnet.md](../frameworks/dotnet.md) | Language and runtime | Expanded | Check actual enumeration count, culture/time semantics, lock ownership, and structured logger behavior. |
| [frameworks/generic.md](../frameworks/generic.md) | Trace the layers | Corrected + expanded | Generic review must work for projects without layered services. |
| [frameworks/generic.md](../frameworks/generic.md) | Universal smells | Corrected + expanded | Replace architecture preferences with observable consequences. |
| [frameworks/generic.md](../frameworks/generic.md) | Language-agnostic correctness | Expanded | Use boundary values with the actual language semantics: overflow versus arbitrary-precision arithmetic, decimal versus binary rounding requirements, ambiguous local timestamps, invalid encodings, aliases, and concurrent mutation. |
| [frameworks/go.md](../frameworks/go.md) | Errors | Expanded | Trace every error to its caller and user-facing outcome. |
| [frameworks/go.md](../frameworks/go.md) | Goroutines and context | Corrected + expanded | Go 1.23 changes timer collection and channel semantics. |
| [frameworks/go.md](../frameworks/go.md) | Data races | Corrected + expanded | The change applies to newly declared loop variables, not all loops. |
| [frameworks/go.md](../frameworks/go.md) | Slices, maps, interfaces | Expanded | Check slice capacity and ownership, nil-interface construction, and map initialization with small boundary inputs. |
| [frameworks/go.md](../frameworks/go.md) | Resources and stdlib | Expanded | Follow the early error branch before deferring resource closure, then iteration errors and close ownership. |
| [frameworks/go.md](../frameworks/go.md) | Testing | Corrected + expanded | Explain the actual failure mechanism. |
| [frameworks/infra.md](../frameworks/infra.md) | Dockerfile | Corrected + expanded | Avoid claiming an automatic container escape. |
| [frameworks/infra.md](../frameworks/infra.md) | Kubernetes | Corrected + expanded | Kubernetes supports both mechanisms; describe does not normally expand secret references. |
| [frameworks/infra.md](../frameworks/infra.md) | Terraform / IaC | Corrected + expanded | Replacement and lifecycle protection require context. |
| [frameworks/infra.md](../frameworks/infra.md) | CI/CD | Corrected + expanded | Approval workflow is a project policy. |
| [frameworks/infra.md](../frameworks/infra.md) | Configuration | Expanded | Trace each new required setting into deployment configuration and startup validation. |
| [frameworks/java.md](../frameworks/java.md) | Transactions — proxy semantics are the classic trap | Corrected + expanded | Proxy mode and method visibility matter.; Configurable rollback rules override defaults. |
| [frameworks/java.md](../frameworks/java.md) | JPA / Hibernate | Corrected + expanded | Remove unconditional severity from configuration choice. |
| [frameworks/java.md](../frameworks/java.md) | Spring web and security | Corrected + expanded | Service-level annotation is not universally mandatory. |
| [frameworks/java.md](../frameworks/java.md) | Concurrency and state | Expanded | Locate mutable singleton fields and executor ownership. |
| [frameworks/java.md](../frameworks/java.md) | General | Expanded | Check resource closure, Optional presence, time/culture choices, and configuration conversion on actual boundary values. |
| [frameworks/java.md](../frameworks/java.md) | Kotlin specifics | Expanded | Identify Hibernate bytecode/proxy requirements and Kotlin compiler plugins before flagging final classes. |
| [frameworks/laravel.md](../frameworks/laravel.md) | Request path | Corrected + expanded | Validation effectiveness matters more than file organization.; No mandatory architecture pattern. |
| [frameworks/laravel.md](../frameworks/laravel.md) | Eloquent & data | Expanded | Inspect accepted fields, global scopes, raw fragments, query counts, and transaction rollback. |
| [frameworks/laravel.md](../frameworks/laravel.md) | Migrations | Expanded | Read generated database operations against the actual adapter/version and deploy overlap. |
| [frameworks/laravel.md](../frameworks/laravel.md) | Jobs, events, and mail | Corrected + expanded | Latency and consistency requirements decide queue usage. |
| [frameworks/laravel.md](../frameworks/laravel.md) | Output & security | Expanded | Trace the actual response template/resource and configuration cache. |
| [frameworks/mobile.md](../frameworks/mobile.md) | Release and compatibility | Corrected + expanded | Identify actual compatibility failures instead of claiming every response change breaks all builds. |
| [frameworks/mobile.md](../frameworks/mobile.md) | Permissions and privacy | Expanded | Test permission denied/restricted/revoked states and data leaving the device. |
| [frameworks/mobile.md](../frameworks/mobile.md) | Lifecycle and background | Expanded | Simulate background/foreground, process termination, and replayed notifications. |
| [frameworks/mobile.md](../frameworks/mobile.md) | Network and offline | Expanded | Exercise delayed/out-of-order responses, reconnect, and repeated submit. |
| [frameworks/mobile.md](../frameworks/mobile.md) | Rendering | Corrected + expanded | APIs and architecture differ across React Native versions.; Mounted-state checks allow valid async context use. |
| [frameworks/mobile.md](../frameworks/mobile.md) | Platform parity and accessibility | Expanded | Inspect screen-reader semantics, text scaling, focus, keyboard/back behavior, and locale layouts on changed platforms. |
| [frameworks/nextjs.md](../frameworks/nextjs.md) | The server/client boundary — the highest-risk area | Corrected + expanded | Do not infer a credential leak merely from an imported non-public env lookup. |
| [frameworks/nextjs.md](../frameworks/nextjs.md) | Server Actions | Corrected + expanded | Invalidation depends on what was cached.; Transported closure data is not necessarily plaintext exposure. |
| [frameworks/nextjs.md](../frameworks/nextjs.md) | Caching and rendering | Corrected + expanded | Cache defaults and modes differ by major version.; Tags and cache identity have different roles.; Rendering behavior depends on cache model.; Different cache layers need evidence rather than an absolute conclusion. |
| [frameworks/nextjs.md](../frameworks/nextjs.md) | Middleware | Corrected + expanded | Middleware/proxy runtime assumptions evolve. |
| [frameworks/nextjs.md](../frameworks/nextjs.md) | Correctness | Expanded | Compare server-rendered output with the first browser render and test direct navigation plus client navigation for parallel slots. |
| [frameworks/nextjs.md](../frameworks/nextjs.md) | Config | Expanded | Follow rewrite/redirect destinations and header merge behavior. |
| [frameworks/nodejs.md](../frameworks/nodejs.md) | Request path | Corrected + expanded | Parsed query values are not always strings. |
| [frameworks/nodejs.md](../frameworks/nodejs.md) | Async & errors | Corrected + expanded | Distinguish detached and caught rejections. |
| [frameworks/nodejs.md](../frameworks/nodejs.md) | Performance & event loop | Expanded | Find the actual event-loop blocking operation or unbounded retained resource and estimate request size/concurrency. |
| [frameworks/nodejs.md](../frameworks/nodejs.md) | Data & security | Corrected + expanded | Review must not create a permission flow absent project policy. |
| [frameworks/nodejs.md](../frameworks/nodejs.md) | Operational | Expanded | Check deadline propagation, in-flight drain, consumer termination, and logging redaction. |
| [frameworks/python.md](../frameworks/python.md) | Layering | Corrected + expanded | Layered services/repositories are project choices, not mandatory FastAPI architecture. |
| [frameworks/python.md](../frameworks/python.md) | FastAPI | Corrected + expanded | Distinguish request-scoped mutable state from valid singleton clients.; FastAPI supports return annotations and explicit response construction. |
| [frameworks/python.md](../frameworks/python.md) | Async | Corrected + expanded | Not every coroutine call is directly awaited.; Do not require locks around all mutable async state. |
| [frameworks/python.md](../frameworks/python.md) | SQLAlchemy 2 (async) | Expanded | Check session creation, commit/rollback, closure, and all tasks using it. |
| [frameworks/python.md](../frameworks/python.md) | Pydantic v2 | Corrected + expanded | Pydantic model defaults differ from ordinary function defaults. |
| [frameworks/python.md](../frameworks/python.md) | General Python | Corrected + expanded | Logging syntax alone is not a correctness defect.; Tool choice does not establish path safety. |
| [frameworks/python.md](../frameworks/python.md) | Before approving | Expanded | Use existing project commands and report whether the selected snapshot was actually executed; dependency absence is a verification limit, not evidence of a code defect. |
| [frameworks/rails.md](../frameworks/rails.md) | ActiveRecord | Corrected + expanded | unscoped bypasses the default scope. |
| [frameworks/rails.md](../frameworks/rails.md) | Transactions and callbacks | Expanded | Trace save/callback/commit ordering and the queue adapter’s transaction behavior. |
| [frameworks/rails.md](../frameworks/rails.md) | Controllers and security | Corrected + expanded | Serialization overrides can already restrict output.; Permission and reachability determine overposting risk. |
| [frameworks/rails.md](../frameworks/rails.md) | Migrations | Corrected + expanded | Migration costs are adapter/version-specific. |
| [frameworks/rails.md](../frameworks/rails.md) | Jobs and caching | Corrected + expanded | Active Job and raw Sidekiq serialize differently. |
| [frameworks/rails.md](../frameworks/rails.md) | Ruby | Expanded | Check time-zone context, exception ownership, JSON key handling, and mutation of shared constants. |
| [frameworks/react.md](../frameworks/react.md) | State boundaries | Corrected + expanded | A store/library choice is not a universal rule. |
| [frameworks/react.md](../frameworks/react.md) | Hooks & rendering | Corrected + expanded | Hook exceptions are version/API-specific. |
| [frameworks/react.md](../frameworks/react.md) | Components | Corrected + expanded | Remove universal file-organization policy.; Remove arbitrary two-level prop threshold. |
| [frameworks/react.md](../frameworks/react.md) | Quality gates | Corrected + expanded | Dynamic HTML is not automatically unsafe. |
| [frameworks/react.md](../frameworks/react.md) | TypeScript | Expanded | Compare types with actual producer/consumer behavior. |
| [frameworks/react.md](../frameworks/react.md) | Before approving | Expanded | CI configuration is not a result; use the shared gate rules to determine what was actually checked. |
| [frameworks/rust.md](../frameworks/rust.md) | Panics — the main production risk | Corrected + expanded | Cargo/rustc settings can change overflow behavior.; These operations panic on invalid inputs, not unconditionally. |
| [frameworks/rust.md](../frameworks/rust.md) | Async | Expanded | Locate every held guard and mutation at await points. |
| [frameworks/rust.md](../frameworks/rust.md) | Errors | Corrected + expanded | Error crate preference is not a universal defect. |
| [frameworks/rust.md](../frameworks/rust.md) | Correctness and ownership | Expanded | Inspect actual clone/allocate scale and lock acquisition order. |
| [frameworks/rust.md](../frameworks/rust.md) | `unsafe` | Corrected + expanded | Missing comments do not alone prove unsoundness. |
| [frameworks/rust.md](../frameworks/rust.md) | Serde and boundaries | Expanded | Test omitted/extra fields, numeric limits, and ambiguous variants against actual consumers. |
| [frameworks/rust.md](../frameworks/rust.md) | Tests | Expanded | Review assertions against the intended contract. |
| [frameworks/sql.md](../frameworks/sql.md) | Correctness before performance | Corrected + expanded | NULL semantics need precise conditions.; UNION is not guaranteed to sort. |
| [frameworks/sql.md](../frameworks/sql.md) | Pagination | Expanded | Choose a deterministic tie-breaker and define behavior while rows change between pages. |
| [frameworks/sql.md](../frameworks/sql.md) | Indexes and sargability | Corrected + expanded | Modern planners can use non-leading predicates. |
| [frameworks/sql.md](../frameworks/sql.md) | Transactions and concurrency | Corrected + expanded | MERGE and ON CONFLICT do not share universal arbiter requirements. |
| [frameworks/sql.md](../frameworks/sql.md) | DDL and migrations | Corrected + expanded | PostgreSQL DDL is not a universal SQL rule.; Constraint applicability and lock semantics differ. |
| [frameworks/sql.md](../frameworks/sql.md) | Data modelling | Expanded | Test null/empty distinctions, deletion scope, and normalized uniqueness values. |
| [frameworks/sql.md](../frameworks/sql.md) | Evidence | Expanded | Use supplied plans or an authorized read-only EXPLAIN. |
| [frameworks/typescript.md](../frameworks/typescript.md) | Type soundness | Corrected + expanded | Keep optional Google style out of the generic correctness pass.; Severity must follow evidence and project requirements.; Remove anthropomorphic and imprecise compiler claims. |
| [frameworks/typescript.md](../frameworks/typescript.md) | Types are not validation | Corrected + expanded | Evidence-based boundary validation without prescribed new dependencies.; Contract changes may remain compatible without regenerated tracked types. |
| [frameworks/typescript.md](../frameworks/typescript.md) | Modelling | Corrected + expanded | Modern enum checks and style adoption require context.; Excess properties are structural typing, not automatically a defect. |
| [frameworks/typescript.md](../frameworks/typescript.md) | Async | Corrected + expanded | Promise rejection does not cancel sibling operations.; Unawaited work does not necessarily swallow rejection. |
| [frameworks/typescript.md](../frameworks/typescript.md) | Interop and imports | Expanded | Inspect output imports and the actual bundler/runtime before recommending syntax. |
| [frameworks/typescript.md](../frameworks/typescript.md) | Errors | Expanded | Identify which errors callers match and how the runtime constructs their prototypes/stacks. |
| [frameworks/vue.md](../frameworks/vue.md) | Reactivity — where most Vue bugs live | Corrected + expanded | Vue 3.5 compiler transform invalidates the blanket rule.; Dependencies are recollected each execution, not frozen at the first run. |
| [frameworks/vue.md](../frameworks/vue.md) | Composables and lifecycle | Corrected + expanded | Vue composables do not have React’s blanket hook-order rule. |
| [frameworks/vue.md](../frameworks/vue.md) | Template | Corrected + expanded | Trust and sanitization determine exploitability. |
| [frameworks/vue.md](../frameworks/vue.md) | State (Pinia / Vuex) | Expanded | Trace store creation per app/request and cache invalidation on user changes. |
| [frameworks/vue.md](../frameworks/vue.md) | SSR / Nuxt | Expanded | Compare requests for two identities and initial hydration against browser navigation. |
| [frameworks/vue.md](../frameworks/vue.md) | Quality | Expanded | Check form errors and keyboard/focus behavior, using the project’s UI components before requiring new ones. |
| [styleguides/google-angular.md](../styleguides/google-angular.md) | Naming and structure | Expanded | Feature grouping and matching test names improve discovery; do not force renaming a stable public/framework contract for cosmetic consistency. |
| [styleguides/google-angular.md](../styleguides/google-angular.md) | Components and directives — to flag | Corrected + expanded | Different Angular input APIs have different readonly semantics. |
| [styleguides/google-cpp.md](../styleguides/google-cpp.md) | Formatting | Expanded | Apply formatting through existing tooling; long literals and generated output can have explicit exceptions. |
| [styleguides/google-cpp.md](../styleguides/google-cpp.md) | Headers | Expanded | Compile a header in its intended include environment before asserting a missing dependency. |
| [styleguides/google-cpp.md](../styleguides/google-cpp.md) | Naming | Expanded | Keep public/interop spellings compatible. |
| [styleguides/google-cpp.md](../styleguides/google-cpp.md) | To flag | Expanded | Review ownership, lifetime, initialization, and conversions behind bug-risk labels. |
| [styleguides/google-csharp.md](../styleguides/google-csharp.md) | Formatting | Expanded | Two-space same-line braces belong to this opt-in policy; the repository’s enforced formatter wins. |
| [styleguides/google-csharp.md](../styleguides/google-csharp.md) | Naming | Expanded | Match access-level naming, including _camelCase non-public fields. |
| [styleguides/google-csharp.md](../styleguides/google-csharp.md) | Organization | Expanded | Follow the listed order only where no project formatter or stronger convention specifies it; ordering does not establish runtime safety. |
| [styleguides/google-csharp.md](../styleguides/google-csharp.md) | To flag | Expanded | Choose input interfaces by the capabilities actually needed. |
| [styleguides/google-dart.md](../styleguides/google-dart.md) | Formatting | Expanded | dart format may use a configured page width; strings/URIs and semantic multiline text have exceptions. |
| [styleguides/google-dart.md](../styleguides/google-dart.md) | Naming | Expanded | Private names use _, while public constants normally use lowerCamelCase. |
| [styleguides/google-dart.md](../styleguides/google-dart.md) | Directives | Expanded | Group dart:, package:, relative imports and exports; do not change the actual import target solely to reorder it. |
| [styleguides/google-go.md](../styleguides/google-go.md) | Formatting | Corrected + expanded | Do not invent a hard Go comment-line limit. |
| [styleguides/google-go.md](../styleguides/google-go.md) | Naming | Expanded | Scope affects name length. |
| [styleguides/google-go.md](../styleguides/google-go.md) | Comments | Expanded | Exported comments explain the contract, not just repeat the signature. |
| [styleguides/google-go.md](../styleguides/google-go.md) | Imports | Expanded | Side-effect imports require an understood initialization effect; adopted generated/framework integrations may justify an exception. |
| [styleguides/google-go.md](../styleguides/google-go.md) | Errors — to flag | Expanded | Style of error text is distinct from lost error handling; cite the failing caller before treating an error-API shape as a bug. |
| [styleguides/google-go.md](../styleguides/google-go.md) | Language — to flag | Expanded | Small consumer interfaces and synchronous APIs are defaults, not proof that every producer interface, alias, or first-use generic is wrong. |
| [styleguides/google-go.md](../styleguides/google-go.md) | Tests | Expanded | Use the project’s adopted comparison/assertion tools. |
| [styleguides/google-haskell.md](../styleguides/google-haskell.md) | Formatting | Expanded | Layout changes can change parsing, so preserve semantic grouping and use the configured formatter where available. |
| [styleguides/google-haskell.md](../styleguides/google-haskell.md) | To flag | Corrected + expanded | Include the source guide’s generated-export exception. |
| [styleguides/google-html-css.md](../styleguides/google-html-css.md) | General | Expanded | HTTPS avoids mixed content for network resources; relative URLs, data assets, and documented development origins need context. |
| [styleguides/google-html-css.md](../styleguides/google-html-css.md) | HTML — to flag | Corrected + expanded | type=module is required module semantics, not redundant style. |
| [styleguides/google-html-css.md](../styleguides/google-html-css.md) | CSS — to flag | Corrected + expanded | Keep required zero units and the verified leading-zero convention. |
| [styleguides/google-java.md](../styleguides/google-java.md) | Formatting | Expanded | Formatter-owned whitespace needs no manual line-by-line findings. |
| [styleguides/google-java.md](../styleguides/google-java.md) | Imports | Expanded | Import group ordering is separate from runtime class loading; do not replace an import merely for personal preference. |
| [styleguides/google-java.md](../styleguides/google-java.md) | Naming | Expanded | An immutable static final constant differs from a mutable collection held in a final variable. |
| [styleguides/google-java.md](../styleguides/google-java.md) | Javadoc | Expanded | A useful Javadoc summary states caller-visible behavior, including null/error contracts; obvious overrides may inherit documentation. |
| [styleguides/google-java.md](../styleguides/google-java.md) | Programming practices to flag | Expanded | A missing @Override is a style/compiler-safety issue unless an actual unintended overload or broken contract is established. |
| [styleguides/google-javascript.md](../styleguides/google-javascript.md) | Formatting | Expanded | Semicolons and braces are style requirements here; a real automatic-semicolon-insertion failure needs an affected expression or return path. |
| [styleguides/google-javascript.md](../styleguides/google-javascript.md) | Declarations and modules | Expanded | Keep module systems compatible with the project loader. |
| [styleguides/google-javascript.md](../styleguides/google-javascript.md) | Naming | Expanded | Distinguish deeply immutable constants from mutable objects whose binding happens to be const. |
| [styleguides/google-javascript.md](../styleguides/google-javascript.md) | Documentation | Expanded | JSDoc records the public contract; do not demand annotations already supplied by a generated interface or adopted tooling. |
| [styleguides/google-javascript.md](../styleguides/google-javascript.md) | To flag | Expanded | Loose-null equality is an explicit exception. |
| [styleguides/google-json.md](../styleguides/google-json.md) | To flag | Corrected + expanded | Enum encoding alone does not guarantee forward compatibility. |
| [styleguides/google-json.md](../styleguides/google-json.md) | Envelope (only if the API uses it) | Expanded | Reserved envelope fields apply only when that envelope is adopted. |
| [styleguides/google-kotlin.md](../styleguides/google-kotlin.md) | Formatting | Expanded | The column target permits package/import/URL exceptions. |
| [styleguides/google-kotlin.md](../styleguides/google-kotlin.md) | Imports | Expanded | Keep one sorted import list. |
| [styleguides/google-kotlin.md](../styleguides/google-kotlin.md) | Naming | Expanded | Compose naming applies to Unit-returning composables, not every function carrying a composable type. |
| [styleguides/google-kotlin.md](../styleguides/google-kotlin.md) | KDoc | Expanded | KDoc should describe caller-visible behavior; avoid empty tags and preserve inherited documentation for straightforward overrides. |
| [styleguides/google-kotlin.md](../styleguides/google-kotlin.md) | To flag | Corrected + expanded | Do not invent a blanket ban on multiline expression-bodied functions. |
| [styleguides/google-lisp.md](../styleguides/google-lisp.md) | Formatting | Expanded | Use indentation that reflects Lisp forms, not a mechanical two-space rule for every argument. |
| [styleguides/google-lisp.md](../styleguides/google-lisp.md) | To flag | Expanded | Inspect package exports, docstrings, conditions, and macro expansion. |
| [styleguides/google-markdown.md](../styleguides/google-markdown.md) | To flag | Expanded | Preserve code literals and semantic line breaks. |
| [styleguides/google-objc.md](../styleguides/google-objc.md) | Formatting | Expanded | Objective-C++ may adopt the project’s C++ width. |
| [styleguides/google-objc.md](../styleguides/google-objc.md) | Naming | Expanded | Preserve SDK selectors and superclass overrides. |
| [styleguides/google-objc.md](../styleguides/google-objc.md) | To flag | Corrected + expanded | Distinguish immutable snapshot contracts from mutable collection ownership. |
| [styleguides/google-python.md](../styleguides/google-python.md) | Formatting | Expanded | Formatting exceptions apply to long paths/URLs and syntax where wrapping harms meaning; do not restyle formatter-owned output. |
| [styleguides/google-python.md](../styleguides/google-python.md) | Naming | Expanded | Keep acronym and public/private naming consistent without renaming external overrides merely to match a local preference. |
| [styleguides/google-python.md](../styleguides/google-python.md) | Imports | Expanded | A qualified module import makes ownership visible; typing-related and documented interoperability exceptions remain valid. |
| [styleguides/google-python.md](../styleguides/google-python.md) | Docstrings and comments | Expanded | Document parameters, results, and raised errors that callers need; omit empty sections on trivial functions. |
| [styleguides/google-python.md](../styleguides/google-python.md) | Language rules to flag | Expanded | A bug-risk label calls for a concrete input/state and wrong result. |
| [styleguides/google-r.md](../styleguides/google-r.md) | To flag | Expanded | Use BigCamelCase functions and .PrivateHelper for Google policy; other data names can use descriptive snake_case. |
| [styleguides/google-shell.md](../styleguides/google-shell.md) | When shell is the wrong tool | Corrected + expanded | A style guideline is not an automatic rewrite demand. |
| [styleguides/google-shell.md](../styleguides/google-shell.md) | Formatting | Expanded | Indent heredoc content according to its intended output, and do not change significant literal whitespace. |
| [styleguides/google-shell.md](../styleguides/google-shell.md) | Naming | Expanded | Use local within Bash functions; constants/exported environment variables differ from mutable locals. |
| [styleguides/google-shell.md](../styleguides/google-shell.md) | Structure | Expanded | Document inputs, outputs, global mutations, and exit codes of non-obvious functions. |
| [styleguides/google-shell.md](../styleguides/google-shell.md) | To flag | Corrected + expanded | Do not apply Bash syntax to a POSIX shell. |
| [styleguides/google-swift.md](../styleguides/google-swift.md) | Formatting | Expanded | Use configured formatting and import groups; @testable imports belong to tests, not production access-control bypass. |
| [styleguides/google-swift.md](../styleguides/google-swift.md) | Naming | Expanded | Follow Swift API readability at the call site. |
| [styleguides/google-swift.md](../styleguides/google-swift.md) | To flag | Expanded | Force operations need an invariant: a documented test fixture differs from untrusted input. |
| [styleguides/google-typescript.md](../styleguides/google-typescript.md) | Naming | Expanded | Preserve external API spelling and framework contracts; naming changes are policy issues, not inherently runtime defects. |
| [styleguides/google-typescript.md](../styleguides/google-typescript.md) | Modules | Expanded | Named exports aid consistent imports; a framework-mandated default export or external declaration can override this policy through the project rules. |
| [styleguides/google-typescript.md](../styleguides/google-typescript.md) | Types — to flag | Corrected + expanded | Presence and undefined values are not always equivalent. |
| [styleguides/google-typescript.md](../styleguides/google-typescript.md) | Classes | Expanded | Readonly protects reassignment of the field, not deep immutability. |
| [styleguides/google-typescript.md](../styleguides/google-typescript.md) | Other rules to flag | Expanded | Control-flow, catch, and iteration rules need the actual value path before bug severity. |
| [styleguides/google-vim.md](../styleguides/google-vim.md) | Formatting | Expanded | Maintain the configured indentation and literal regex contents; accidental escaping can change matching behavior. |
| [styleguides/google-vim.md](../styleguides/google-vim.md) | To flag | Expanded | Test with user mappings and ignorecase settings enabled. |
| [styleguides/google-xml.md](../styleguides/google-xml.md) | To flag | Expanded | Use meaningful lowerCamelCase names; a name longer than the suggested limit can be clearer than an abbreviation. |

## File and source coverage

All existing filenames are preserved. Source links in each file are optional attribution, not instructions to fetch documentation during a review. The JavaScript style guide is explicitly marked as an upstream legacy policy snapshot. The C# source URL was corrected to the available official guide. R’s previously external tidyverse baseline is summarized locally.

| File | Local applicability/source notes |
|---|---|
| [frameworks/angular.md](../frameworks/angular.md) | Angular with RxJS; inspect Angular/RxJS versions, standalone versus NgModule setup, signals, and zone/zoneless configuration. takeUntilDestroyed is available in Angular 16+; use the project’s compatible lifecycle mechanism. |
| [frameworks/django.md](../frameworks/django.md) | Django ORM and DRF with the installed database backend. Confirm Django/DRF versions, ATOMIC_REQUESTS, permission defaults, and serializer overrides. Locking and concurrent-index notes are backend-specific, especially PostgreSQL versus SQLite. |
| [frameworks/dotnet.md](../frameworks/dotnet.md) | C#/.NET, ASP.NET Core, and EF Core. Inspect target framework, nullable settings, EF provider/version, DI registrations, and host lifecycle. Legacy ASP.NET synchronization contexts and older EF client evaluation differ from modern ASP.NET Core. |
| [frameworks/generic.md](../frameworks/generic.md) | Fallback for a language/stack without a dedicated pass, or cross-boundary checks alongside one. Establish language/runtime, data model, concurrency, and project conventions locally. This file does not prescribe a service/repository architecture. |
| [frameworks/go.md](../frameworks/go.md) | Go modules; read the go directive, toolchain, build tags, race settings, and GODEBUG. Loop-variable behavior changes with Go 1.22 language semantics; timer behavior changes with Go 1.23 semantics and compatibility overrides. |
| [frameworks/infra.md](../frameworks/infra.md) | Docker/BuildKit, Kubernetes manifests, Terraform/provider plans, and CI definitions. Identify deployed API/provider versions, cluster policy, runner trust, and actual environment before applying platform-specific syntax. Supplied plans are evidence; never apply infrastructure during review. |
| [frameworks/java.md](../frameworks/java.md) | Java/Kotlin services using Spring transactions/security and JPA/Hibernate. Inspect Spring version, proxy versus AspectJ mode, transaction manager, ORM provider, Kotlin plugins, and database adapter. An annotation alone does not establish active advice. |
| [frameworks/laravel.md](../frameworks/laravel.md) | Laravel/PHP with installed framework, queue driver, PHP version, middleware groups, and config-cache setup. Queue model reloading and after-commit dispatch depend on framework/connection/job options; use their local configuration. |
| [frameworks/mobile.md](../frameworks/mobile.md) | React Native, Flutter, native Android/iOS. Inspect app/framework/SDK versions, supported OS range, storage schema, permissions, and release/deployment configuration. Evaluate only platforms actually changed; store-policy compliance cannot be assumed current without locally supplied evidence. |
| [frameworks/nextjs.md](../frameworks/nextjs.md) | Next.js App Router. Read next/package version, route segment config, cacheComponents, runtime, and deployment adapter. Distinguish Next 14, Next 15, and Next 16 Cache Components; do not infer Pages Router behavior from this file. |
| [frameworks/nodejs.md](../frameworks/nodejs.md) | Node.js server paths using the installed Express, NestJS, Fastify, or Koa version. Error forwarding differs between Express 4 and 5; body/query coercion may be provided by framework validation pipes/plugins. Identify ESM/CJS and supported runtime APIs. |
| [frameworks/python.md](../frameworks/python.md) | Python 3; inspect pyproject/lockfiles and the actual web framework. SQLAlchemy notes target 2.x async APIs and Pydantic notes target v2. Do not apply those APIs to older dependencies; Flask does not inherit FastAPI dependency or response-model behavior. |
| [frameworks/rails.md](../frameworks/rails.md) | Ruby on Rails/ActiveRecord and the actual job backend. Inspect Rails/Ruby versions, database adapter, Active Job versus raw Sidekiq invocation, transaction-enqueue options, and time-zone settings. Do not assume PostgreSQL DDL on another adapter. |
| [frameworks/react.md](../frameworks/react.md) | React function components and Hooks; inspect React version, compiler/lint settings, router, and installed data libraries. The special use API belongs to React 19+. Server components and framework caches need their matching framework pass. |
| [frameworks/rust.md](../frameworks/rust.md) | Rust with Cargo edition, release profile, panic/overflow settings, target, async runtime, and Serde formats identified locally. Task cancellation and JoinHandle semantics are runtime-specific; examples of detached spawning assume Tokio-like behavior, not every executor. |
| [frameworks/sql.md](../frameworks/sql.md) | SQL queries, ORM fragments, views, and migrations. Identify engine/version, column types/collation, constraints, isolation, data distribution, and execution-plan source. PostgreSQL-specific commands below are labeled; do not apply them to MySQL, SQL Server, or SQLite blindly. |
| [frameworks/typescript.md](../frameworks/typescript.md) | TypeScript with compiler version, strict flags, module resolution, emit target, runtime/transpiler, and lint configuration inspected locally. Numeric enum checks and narrowing evolve across compiler releases. Google-specific style is a separate opt-in, not a condition of TypeScript correctness. |
| [frameworks/vue.md](../frameworks/vue.md) | Vue 3 Composition API; inspect matching vue/compiler-sfc versions and Nuxt/Pinia versions. The Vue 3.5 defineProps transform applies within script setup, not arbitrary object destructuring. Vue 2 and Options API code need locally verified equivalents. |
| [styleguides/google-angular.md](../styleguides/google-angular.md) | Current Angular style snapshot; determine framework generation and whether signal or decorator APIs are used. Apply TypeScript conventions through the bundled TypeScript guide when opted in. |
| [styleguides/google-cpp.md](../styleguides/google-cpp.md) | Google C++ policy; inspect the project’s C++ standard, exception/RTTI policy, ownership conventions, generated headers, and formatter settings. |
| [styleguides/google-csharp.md](../styleguides/google-csharp.md) | Google C# policy, which differs from common Microsoft formatting defaults. Inspect target language version, .editorconfig, nullability, and generated bindings. |
| [styleguides/google-dart.md](../styleguides/google-dart.md) | Effective Dart style with installed SDK language version and formatter configuration. Existing constant-name or generated-code conventions can override the default naming preference. |
| [styleguides/google-go.md](../styleguides/google-go.md) | Google Go policy; inspect module language/toolchain versions and project gofmt/lint setup. Google policy choices such as test helpers are not universal Go requirements. |
| [styleguides/google-haskell.md](../styleguides/google-haskell.md) | Google Haskell style revision 1.01 snapshot; inspect GHC/base versions, extensions, generated declarations, build warnings, and formatter policy. |
| [styleguides/google-html-css.md](../styleguides/google-html-css.md) | Google HTML/CSS style for the project’s HTML/CSS dialect. JSX, templates, CSS modules, and formatter output may impose different syntax; do not apply raw-HTML casing blindly to components. |
| [styleguides/google-java.md](../styleguides/google-java.md) | Google Java policy; inspect supported language level and formatter. Records, generated bindings, and overriding APIs can impose names or documentation exceptions. |
| [styleguides/google-javascript.md](../styleguides/google-javascript.md) | Google’s JavaScript guide is a legacy policy snapshot and is no longer updated upstream. Apply it to JavaScript only when opted in; do not require migrating the project to TypeScript. |
| [styleguides/google-json.md](../styleguides/google-json.md) | Google JSON contract policy (revision 0.9 snapshot), not a universal schema or incidental-config policy. Respect existing API envelopes and consumer compatibility. |
| [styleguides/google-kotlin.md](../styleguides/google-kotlin.md) | Android Kotlin style snapshot; inspect Kotlin/Compose versions, compiler target, formatter, and framework override contracts. |
| [styleguides/google-lisp.md](../styleguides/google-lisp.md) | Google Common Lisp style snapshot; inspect implementation, reader/package configuration, macro expansion environment, and generated code. This is Common Lisp, not Scheme or Clojure. |
| [styleguides/google-markdown.md](../styleguides/google-markdown.md) | Google Markdown policy for substantial documentation changes. Inspect the target renderer (CommonMark, GitHub, or project extensions) and documentation linter. Raw HTML, tables, and a TOC directive have renderer-dependent behavior. Source snapshot checked: **2026-10-26**; the source link is optional attribution. |
| [styleguides/google-objc.md](../styleguides/google-objc.md) | Google Objective-C/Objective-C++ style; inspect ARC versus manual ownership, SDK availability, nullability, and any C++ language mode. |
| [styleguides/google-python.md](../styleguides/google-python.md) | Python 3 Google-style policy; recognize generated code and project formatter/config exceptions. This is not the Pydantic model-default rule. |
| [styleguides/google-r.md](../styleguides/google-r.md) | Google R style extensions plus a local summary of the referenced tidyverse basics. Inspect R version, package namespace, and project styler/lintr configuration. |
| [styleguides/google-shell.md](../styleguides/google-shell.md) | Google Bash policy. Identify the shebang and shell version first; POSIX sh lacks arrays, [[, and process substitution. Preserve scripts that intentionally target another shell under project policy. |
| [styleguides/google-swift.md](../styleguides/google-swift.md) | Google Swift style snapshot; inspect Swift language mode, concurrency checking, minimum OS, formatter, and imported Objective-C API naming. |
| [styleguides/google-typescript.md](../styleguides/google-typescript.md) | Google TypeScript policy snapshot; inspect compiler/module settings and required framework exports. Negative type tests have a narrow @ts-expect-error exception. |
| [styleguides/google-vim.md](../styleguides/google-vim.md) | Google legacy Vimscript policy; check Vim/Neovim version and script dialect. Vim9script and Lua plugins have different semantics and are outside these legacy rules. |
| [styleguides/google-xml.md](../styleguides/google-xml.md) | Google XML format-design policy version 1.0 snapshot. Check the adopted schema, namespace versioning, and consuming parsers; this is not a requirement to redesign incidental XML configuration. |

## Corrections and removals within topics

The following reasons describe final rule changes, including source-reference corrections. They remove automatic findings from preferences and qualify behavior by version/configuration. The old directives are not retained as competing guidance.

- [frameworks/angular.md](../frameworks/angular.md): Finite observables and long-lived subscriptions have different lifetimes. Completed and intentionally persistent sources are exceptions. OnPush has triggers beyond input identity. Guards depend on first emission, not stream completion. Avoid treating all dynamic values as exploitable.
- [frameworks/django.md](../frameworks/django.md): Actual behavior is backend/test-context dependent. Correct DRF list/detail/create permission semantics. Cross-field validation is not a per-field hook. Bulk insert and update do not have identical field behavior. Serializer declarations do not alone prove privilege escalation. Signal behavior depends on save path and sender; avoid architecture mandates.
- [frameworks/dotnet.md](../frameworks/dotnet.md): Task lifetime and scoped dependency lifetime differ. Two documented lifetime patterns are valid. Role-based authorization is valid. Container tracking and retention differ from missing disposal.
- [frameworks/generic.md](../frameworks/generic.md): Generic review must work for projects without layered services. Replace architecture preferences with observable consequences.
- [frameworks/go.md](../frameworks/go.md): Go 1.23 changes timer collection and channel semantics. The change applies to newly declared loop variables, not all loops. Explain the actual failure mechanism.
- [frameworks/infra.md](../frameworks/infra.md): Kubernetes supports both mechanisms; describe does not normally expand secret references. Replacement and lifecycle protection require context. Approval workflow is a project policy. Avoid claiming an automatic container escape.
- [frameworks/java.md](../frameworks/java.md): Proxy mode and method visibility matter. Configurable rollback rules override defaults. Remove unconditional severity from configuration choice. Service-level annotation is not universally mandatory.
- [frameworks/laravel.md](../frameworks/laravel.md): Validation effectiveness matters more than file organization. No mandatory architecture pattern. Latency and consistency requirements decide queue usage.
- [frameworks/mobile.md](../frameworks/mobile.md): APIs and architecture differ across React Native versions. Mounted-state checks allow valid async context use. Identify actual compatibility failures instead of claiming every response change breaks all builds.
- [frameworks/nextjs.md](../frameworks/nextjs.md): Do not infer a credential leak merely from an imported non-public env lookup. Invalidation depends on what was cached. Transported closure data is not necessarily plaintext exposure. Cache defaults and modes differ by major version. Tags and cache identity have different roles. Rendering behavior depends on cache model. Different cache layers need evidence rather than an absolute conclusion. Middleware/proxy runtime assumptions evolve.
- [frameworks/nodejs.md](../frameworks/nodejs.md): Review must not create a permission flow absent project policy. Parsed query values are not always strings. Distinguish detached and caught rejections.
- [frameworks/python.md](../frameworks/python.md): Layered services/repositories are project choices, not mandatory FastAPI architecture. Distinguish request-scoped mutable state from valid singleton clients. FastAPI supports return annotations and explicit response construction. Pydantic model defaults differ from ordinary function defaults. Logging syntax alone is not a correctness defect. Tool choice does not establish path safety. Not every coroutine call is directly awaited. Do not require locks around all mutable async state.
- [frameworks/rails.md](../frameworks/rails.md): Active Job and raw Sidekiq serialize differently. Migration costs are adapter/version-specific. Serialization overrides can already restrict output. unscoped bypasses the default scope. Permission and reachability determine overposting risk.
- [frameworks/react.md](../frameworks/react.md): A store/library choice is not a universal rule. Hook exceptions are version/API-specific. Remove universal file-organization policy. Remove arbitrary two-level prop threshold. Dynamic HTML is not automatically unsafe.
- [frameworks/rust.md](../frameworks/rust.md): Cargo/rustc settings can change overflow behavior. Error crate preference is not a universal defect. Missing comments do not alone prove unsoundness. These operations panic on invalid inputs, not unconditionally.
- [frameworks/sql.md](../frameworks/sql.md): NULL semantics need precise conditions. Modern planners can use non-leading predicates. PostgreSQL DDL is not a universal SQL rule. Constraint applicability and lock semantics differ. UNION is not guaranteed to sort. MERGE and ON CONFLICT do not share universal arbiter requirements.
- [frameworks/typescript.md](../frameworks/typescript.md): Keep optional Google style out of the generic correctness pass. Severity must follow evidence and project requirements. Modern enum checks and style adoption require context. Evidence-based boundary validation without prescribed new dependencies. Promise rejection does not cancel sibling operations. Remove anthropomorphic and imprecise compiler claims. Unawaited work does not necessarily swallow rejection. Contract changes may remain compatible without regenerated tracked types. Excess properties are structural typing, not automatically a defect.
- [frameworks/vue.md](../frameworks/vue.md): Vue 3.5 compiler transform invalidates the blanket rule. Dependencies are recollected each execution, not frozen at the first run. Vue composables do not have React’s blanket hook-order rule. Trust and sanitization determine exploitability.
- [styleguides/google-angular.md](../styleguides/google-angular.md): Different Angular input APIs have different readonly semantics.
- [styleguides/google-csharp.md](../styleguides/google-csharp.md): Replace an unavailable source URL with the current official guide.
- [styleguides/google-go.md](../styleguides/google-go.md): Do not invent a hard Go comment-line limit.
- [styleguides/google-haskell.md](../styleguides/google-haskell.md): Include the source guide’s generated-export exception.
- [styleguides/google-html-css.md](../styleguides/google-html-css.md): type=module is required module semantics, not redundant style. Keep required zero units and the verified leading-zero convention. Preserve the current source convention for CSS fractions.
- [styleguides/google-json.md](../styleguides/google-json.md): Enum encoding alone does not guarantee forward compatibility.
- [styleguides/google-kotlin.md](../styleguides/google-kotlin.md): Do not invent a blanket ban on multiline expression-bodied functions.
- [styleguides/google-objc.md](../styleguides/google-objc.md): Distinguish immutable snapshot contracts from mutable collection ownership.
- [styleguides/google-shell.md](../styleguides/google-shell.md): A style guideline is not an automatic rewrite demand. Do not apply Bash syntax to a POSIX shell.
- [styleguides/google-typescript.md](../styleguides/google-typescript.md): Presence and undefined values are not always equivalent.

## Offline acceptance and follow-up

- Each pass can be applied using the bundled skill plus relevant local project files; local links for shared policy or explicitly composed passes are intentional.
- Unknown dependency versions, unsupported engines, unavailable runtime checks, and missing execution plans are recorded as specific verification gaps. They do not trigger an automatic web dependency or an invented defect.
- Refresh source-check dates only after actually checking the relevant sources. Future additions should include both a failing scenario and a valid counterexample where blanket rules would create false positives.
- A blind evaluator must use only the case prompt, fixture repository, and bundled skill. Do not supply this audit or expected.json to the reviewer. Report any browsing attempts, missed defects, false positives and unsupported version assumptions.
