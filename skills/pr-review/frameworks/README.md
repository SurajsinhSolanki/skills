# Stack-pass selection

## Offline contract

Each pass contains applicability/version notes, checks, evidence and correction guidance for its topics, and a worked example. External source links and verification dates support maintenance; they are not required reading during a review. Read installed versions/configuration from the selected project snapshot. When behavior is outside the documented scope or cannot be established locally, record the specific uncertainty rather than guessing. Shared verdict/gate policy stays in the bundled SKILL.md; explicitly composed passes remain local.


Load this index after triage when selecting stack references. Choose only stacks evidenced by the changed files and their manifests. A `.pr-review` stack pin is advisory: skip pinned stacks absent from the changed paths and add stacks evidenced by the diff even when the pin omits them. Disclose stale or unknown pin entries. Generic fallback applies when no specialized pass fits. References compose: a TypeScript Next.js change uses Next.js, React, and TypeScript; SQL and infrastructure changes add their cross-cutting passes. The default budget of three permits documented exceptions for concrete risks.

| Evidence in the diff | Load |
|---|---|
| `.ts` / `.tsx`, `tsconfig.json` | [typescript.md](typescript.md) — plus the framework file below |
| `.jsx` / `.tsx` with React imports | [react.md](react.md) |
| `next.config.*`, `app/` or `pages/` router, `'use client'` | [nextjs.md](nextjs.md) |
| `.vue`, `nuxt.config.*`, `defineComponent`, Pinia | [vue.md](vue.md) |
| `.component.ts`, `angular.json`, RxJS operators, decorators | [angular.md](angular.md) |
| `package.json` with a server framework (Express/Nest/Fastify/Koa) | [nodejs.md](nodejs.md) |
| `.py` with FastAPI, Flask, SQLAlchemy, Pydantic | [python.md](python.md) |
| `.py` with `settings.py`, `models.py`, DRF serializers, `migrations/` | [django.md](django.md) |
| `.java` / `.kt`, `pom.xml`, `build.gradle`, Spring annotations | [java.md](java.md) |
| `.cs`, `.csproj`, `Program.cs`, EF Core, ASP.NET | [dotnet.md](dotnet.md) |
| `.go`, `go.mod` | [go.md](go.md) |
| `.rb`, `Gemfile`, `app/models`, `db/migrate` | [rails.md](rails.md) |
| `.php`, `composer.json`, `artisan`, Eloquent | [laravel.md](laravel.md) |
| `.rs`, `Cargo.toml` | [rust.md](rust.md) |
| `.sql`, raw query strings, views, stored procedures | [sql.md](sql.md) |
| `Dockerfile`, k8s manifests, `.tf`, CI workflow files | [infra.md](infra.md) |
| React Native, Flutter (`pubspec.yaml`), `.swift`, `.kt` under an Android/iOS app | [mobile.md](mobile.md) |
| anything else, or a stack with no file here | [generic.md](generic.md) |

`sql.md` and `infra.md` are **cross-cutting** — load them whenever the diff contains raw SQL or deployment config, on top of the language file.

Detect from evidence, not from the repo's reputation. If the manifest says one thing and the changed files another, follow the changed files.

**Do not load a file for a stack the diff does not touch.** In a monorepo, the review is scoped to the changed paths: if only the Python service changed, the frontend files stay closed even though the repo contains them. State which stack files you used, so the reader can see the scope.

