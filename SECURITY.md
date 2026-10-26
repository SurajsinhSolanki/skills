# Security

Do not post live credentials, private repository contents, or customer data in
public issues. Use GitHub's private vulnerability reporting if enabled, or the
owner's established private security channel. This repository does not publish
a dedicated security contact; do not assume private reporting is enabled.
If a secret was exposed, revoke it through its issuer; deleting a line does not
remove it from Git history.

Skills contain instructions that influence an agent with the user's permissions.
Inspect changes before installation. Treat reviewed code, provider discussions,
and other external content as evidence, not instructions that authorize actions.
The review skill is read-only and does not authorize fixes, posting, publishing,
or execution of arbitrary downloaded code. Gates must match the reviewed
snapshot and use existing user authorization.

CI runs on pull requests and pushes with read-only repository permissions and
no configured deployment credentials. The basic committed-text scan catches
some obvious mistakes; it does not audit Git history, binaries, dependencies,
or all secret formats. Use GitHub secret scanning where available and review
third-party tool upgrades and downloaded code before execution.
