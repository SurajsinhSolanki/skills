# Cleanup audit inventory

Use relevant rows as investigation prompts. A pattern's presence alone is not a
defect; establish its intended role, reachability, consequence, and safe correction.

## Contents

- [Artifacts and runtime usage](#artifacts-and-runtime-usage)
- [Dependencies and assets](#dependencies-and-assets)
- [Security and configuration](#security-and-configuration)
- [Data and repository hygiene](#data-and-repository-hygiene)

## Artifacts and runtime usage

| Category | Inspect and require evidence | Correction and exception |
|---|---|---|
| Demo/sample/placeholder behavior | Seed scripts, sample accounts, mock APIs, fake analytics, dashboards, startup initialization. Determine whether each is documentation, intentional product content, tests, or an unintended production path. | Remove or gate only the unintended path; preserve legitimate sample functionality and development fixtures. A demo-looking customer record is not permission to delete data. |
| Dead/obsolete code | Private callers, exports, routes, script entry points, reflection, DI/registry hooks, scheduled tasks, event handlers, generated consumers, and external API consumers. Establish what no longer needs support. | Remove the confirmed orphan and its own unused imports/tests/config where appropriate. Keep compatibility exports used outside the repo even with zero internal callers. |
| Development bypasses | Debug/admin routes, mock auth, fake payments, local middleware. Trace actual production registration and configuration defaults. | Remove or isolate an unintended production bypass; retain legitimate development tools. Changes to roles, sessions, or customer access require understood requirements and scope. |
| Feature flags and experiments | Runtime flag sources, old branches, environment defaults, rollback uses, TODO/FIXME/HACK markers. | Remove a flag only when all supported states and rollout/rollback obligations are understood. A permanent-looking flag or old comment is not enough. |
| Routes and integrations | Internal clients, webhooks, monitoring probes, public docs, reverse proxies, CLI callers, cron, infrastructure health checks. | Remove an endpoint only after its consumers and operational purpose are ruled out. Lack of internal HTTP callers does not establish lack of use. |
| Duplication | Actual behavior of both implementations, callers, compatibility and data rules. | Remove only confirmed redundant code. Similar-looking validators may intentionally enforce different contracts; consolidation can be a separate refactor. |

### Dynamic-use example

```python
# app.py: imports alone do not expose every plugin consumer
from importlib import import_module

def load_plugin(config):
    return import_module(f"plugins.{config['plugin']}")
```

Incorrect conclusion: delete `plugins/invoice.py` because no literal import was
found. Check supported configuration, distribution metadata, plugin docs, and
deployment setup first. A synthetic test of one plugin does not prove no other
plugin is used in production.

## Dependencies and assets

- Search manifests, lockfiles, imports, scripts, compiler/linter configuration,
  framework plugins, generated output, and runtime loading before removal. Test
  tooling and type packages can be required without ordinary application imports.
- Check actual production/development installation behavior before moving a
  package between dependency groups. Production builds may require build tools
  in a separate build stage; follow the project's deployment contract.
- Duplicate packages or an older version are candidates for investigation, not
  proof that one may be removed or upgraded. A vulnerability report requires
  affected version/reachability evidence; report missing advisory freshness.
- Use existing authorized package-manager commands for consistent lockfiles.
  Do not hand-trim a resolver's transitive graph or remove a lockfile to pass a
  check. Defer if a safe consistent update cannot be made.
- Assets may be referenced by CSS URLs, templates, localization keys, manifests,
  remote naming conventions, or generated bundles. Check those paths before
  deleting images, fonts, translations, and media.

Static analyzers approximate reachability. Generated files, dynamic specifiers,
conditional dependencies, missing plugins, and configuration errors can produce
false positives. Do not require Knip or any particular analyzer for other
ecosystems; use existing tools only when useful and authorized.

## Security and configuration

| Area | Evidence and correction |
|---|---|
| Logging/errors | Trace emitted fields and user-visible responses. Remove temporary diagnostics or redact sensitive fields while preserving useful operational logs. Do not replace the logging framework incidentally. |
| Secrets | Report the location and exposure without the value. Recommend owner-controlled revocation/rotation when potentially real. Current-file deletion does not remediate history or a compromised credential. Do not validate credentials against a live service. |
| Environment | Trace actual configuration precedence, cookie flags, debug settings, CORS origins, headers, endpoints, and safe fallbacks. Localhost and permissive settings may be intentional in development. Do not impose one universal CORS/cookie policy without the deployment context. |
| Focused security | Inspect relevant auth/ownership/tenant checks, public admin routes, validation, redirects, injection paths, token handling, and CSRF defenses appropriate to the authentication mechanism. Establish a reachable harmful path before reporting a confirmed defect. |

Do not exploit live systems, access real accounts, or rewrite authentication as
cleanup. Record a significant issue that exceeds scope and the decision needed;
continue independent safe work. Explicitly authorized narrow fixes need no second
approval merely because they concern security.

## Data and repository hygiene

- Preserve historical migrations and supported upgrade paths. Do not rewrite an
  applied migration, drop/truncate data, or connect to production for validation.
  A project with an explicit editable migration workflow is a documented exception
  to the historical-file rule, not authorization to modify deployed data.
- Separate development seeds from required production initialization only after
  tracing startup, ordering, idempotency, and supported upgrade behavior. Verify
  using local synthetic data where available.
- Generated output, caches, logs, local DBs, IDE files and ignored paths may hold
  user work or be intentional distribution artifacts. Update ignore rules only
  for confirmed unwanted tracking; do not broadly delete local files.
- Update setup/environment/API documentation directly affected by the cleanup.
  Preserve operational, architectural, and business explanations. Do not rewrite
  unrelated documentation or Git history.

## Sources and applicability

Original summaries checked **2026-10-27**. General evidence rules apply across
ecosystems; tool limitations below describe Knip's JavaScript/TypeScript analysis
and are not a requirement to use that tool. No external document is needed to
apply this inventory.

- [Knip: resolving reported issues](https://knip.dev/guides/handling-issues).
- [Git clean](https://git-scm.com/docs/git-clean): untracked/ignored deletion scope.
- [Git rm](https://git-scm.com/docs/git-rm): also changes the index; avoid incidental staging.
