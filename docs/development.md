# Development

## Set up

Use Python 3.11+ and Git. From the collection root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

The dependency pins the [official reference validator](https://github.com/agentskills/agentskills/tree/main/skills-ref)
to a reviewed commit. Upstream describes it as a demonstration library, so the
collection supplements it with packaging/link checks; validation is not a
security or behavior guarantee. Dependency installation needs network access.

## Add or update a skill

Create `skills/<name>/SKILL.md` with YAML `name` and `description`, then actionable
instructions for a real task. Choose a unique lowercase ASCII kebab-case name,
1–64 characters, matching its directory. Descriptions must be nonempty and at
most 1024 characters. Supported optional fields follow the official spec; avoid
custom top-level metadata fields. Add only useful resources, all inside the
skill directory, and link them relatively. Keep attribution/license notices in
the standalone package too. Never add a nested `SKILL.md` or a collection-root
entry point that could shadow discovery.

For updates, retain public names, resource paths, and invocation behavior unless
a deliberate migration is necessary. Update affected examples and regression
cases together. The `pr-review` package keeps its established resource folder
names and evaluation suite to preserve its existing local references.

## Validate

Run the same checks used by CI:

```bash
python scripts/validate_skills.py
python scripts/update_catalog.py --check
python -m unittest discover -s tests -v
python -m unittest discover -s skills/pr-review/evals -p 'test_*.py' -v
python skills/pr-review/evals/run.py
```

After metadata changes, run `python scripts/update_catalog.py` before checking.
To use the official validator directly: `skills-ref validate skills/pr-review`.
Collection validation discovers every immediate skill directory, checks metadata
and duplicate names, rejects missing/nested entry points, checks rendered
Markdown local links/anchors and package boundaries, and scans UTF-8 text for
obvious key formats, private-key headers, long literal credentials, and personal
filesystem paths. It does not execute skill scripts. Binary data, unfenced
reference syntax variants, obfuscated secrets, and Git history require separate
review; this conservative scanner is not a full secret-detection product.
Fenced example links are not treated as live links. Local agent installations,
virtual environments, caches, and Git internals are excluded.

Unit tests and fixture generation do not establish that an agent follows the
skill. Use the package's [blind evaluation procedure](../skills/pr-review/evals/README.md)
for that, recording the revision, model, settings, and raw results. Keep generated
repositories and review outputs in temporary directories, outside the collection.

For a packaging smoke test, use a disposable project directory and the official
CLI with the absolute collection path, `--skill pr-review --agent codex --yes
--copy`. Inspect copied resources as well as the entry point. Repeat for any
newly claimed agent target. Never use a global install for an isolated check.

## Publish

The collection is hosted at
[SurajsinhSolanki/skills](https://github.com/SurajsinhSolanki/skills), with `main`
as its default branch. Preserve the existing Git history and remote when making
updates.

1. Run the validation commands above and inspect `git diff` for unintended
   changes, private files, and secrets.
2. Regenerate the catalog after changing skill metadata. If the repository is
   renamed or transferred, update `repository.json` and the installation
   documentation together.
3. Commit the intended files and publish through the repository's reviewed
   workflow. Inspect `git status` and `git remote -v` first; do not replace the
   remote or force-push. Push only when authorized by the owner.
4. Check the [validation workflow](https://github.com/SurajsinhSolanki/skills/actions/workflows/validate-skills.yml)
   for the published commit. From a disposable project, verify discovery and an
   individual install:

   ```bash
   npx skills add SurajsinhSolanki/skills --list
   npx skills add SurajsinhSolanki/skills --skill pr-review --agent codex --yes --copy
   ```

The [Skills Directory](https://www.skills.sh/docs) documents discovery through
CLI usage telemetry. A standard public repository is the distribution source;
there is no custom publication manifest here. Do not claim listing, ranking, or
submission success until checked on the live directory.

CLI users can use its documented update/check commands. Preserve names and
paths for compatibility; document any rename or breaking behavior before
release. Recheck the specification, CLI behavior, pinned dependencies, and
source-derived version guidance when upgrading them.
