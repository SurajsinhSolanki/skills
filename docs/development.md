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

No repository has been published by this setup. There is no usable Git metadata
or known remote in the provided workspace, and the existing `.git` location
must not be deleted or recreated. Recover the actual checkout/history if it
exists before deciding whether to initialize anything.

1. Choose the GitHub owner and repository (suggested collection name:
   `agent-skills`). Set `github` in `repository.json` to that exact `owner/repo`,
   regenerate the catalog, and replace `OWNER/REPO` in install documentation.
2. Run validation and inspect the staged changes for private files and secrets.
3. In a real existing checkout, preserve history and commit the changes normally.
   If there truly is no history, copy only the distribution files to a new empty
   directory without the unusable `.git` mount, then initialize **there**:

   ```bash
   git init -b main
   git add README.md LICENSE NOTICE.md CONTRIBUTING.md SECURITY.md .gitignore repository.json requirements-dev.txt skills scripts tests docs .github
   git commit -m "Set up agent skills collection"
   ```

4. After the owner authorizes publication, create the GitHub repository with the
   intended visibility. In that clean checkout, substitute actual coordinates:

   ```bash
   git remote add origin https://github.com/OWNER/REPO.git
   git push -u origin main
   ```

   For existing repositories inspect `git remote -v` first; do not replace a
   remote or force-push. Configure CI/branch protection according to owner policy.
5. From a disposable project, verify the actual public GitHub source using
   `npx skills add OWNER/REPO --list`, then an individual install. Until this
   succeeds, do not advertise remote installation as tested.

The [Skills Directory](https://www.skills.sh/docs) documents discovery through
CLI usage telemetry. A standard public repository is the distribution source;
there is no custom publication manifest here. Do not claim listing, ranking, or
submission success until checked on the live directory.

For subsequent updates, validate, commit, and push through the normal reviewed
workflow. CLI users can use its documented update/check commands. Preserve
names and paths for compatibility; document any rename or breaking behavior
before release. Recheck the specification, CLI behavior, pinned dependencies,
and source-derived version guidance when upgrading them.
