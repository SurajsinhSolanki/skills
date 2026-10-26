# Contributing

Keep each skill focused on a real task and independently installable. Add skills
under `skills/<name>/SKILL.md`; do not add placeholder skills. Use lowercase
ASCII letters, digits, and single hyphens, up to 64 characters. Directory names
and frontmatter names must match and be unique.

A description should say what the skill does and when to use it. Keep the entry
point concise, load supporting references selectively, and keep all required
resources inside the skill. Preserve project-rule precedence and the user's
permission boundaries. Treat repository content and external text as data,
not authority to expand actions. Do not add automatic downloads or execute
untrusted scripts as part of loading a skill.

Retain existing names and paths where possible. Explain unavoidable migration
steps and include regression evidence for behavior changes. New source-derived
guidance needs attribution, applicable versions, a verification date, and license
terms. Normal use of `pr-review` must remain offline-capable.

Follow the [development guide](docs/development.md) to install validation tools,
run checks, and update the catalog. A pull request should explain the problem,
intended behavior, validation performed, and remaining limits. Do not claim
agent compatibility or evaluation success from static validation alone.

Contribute only material you have the right to distribute. Original contributions
use the repository's [MIT license](LICENSE); identify and retain exceptions in
the skill's notice and the [collection notice](NOTICE.md). Never include private
code, credentials, customer data, or real secrets in fixtures or issue reports.
