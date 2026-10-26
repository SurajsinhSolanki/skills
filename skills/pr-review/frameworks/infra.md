# Infrastructure Review (Docker · Kubernetes · Terraform · CI)

Config changes deploy the same as code and break production the same way. Review them with equal care.

Contents: [Applicability and offline use](#applicability-and-offline-use) · [Dockerfile](#dockerfile) · [Kubernetes](#kubernetes) · [Terraform / IaC](#terraform--iac) · [CI/CD](#cicd) · [Configuration](#configuration) · [Worked example and counterexample](#worked-example-and-counterexample) · [Sources and maintenance](#sources-and-maintenance)

## Applicability and offline use

Docker/BuildKit, Kubernetes manifests, Terraform/provider plans, and CI definitions. Identify deployed API/provider versions, cluster policy, runner trust, and actual environment before applying platform-specific syntax. Supplied plans are evidence; never apply infrastructure during review.

This file contains the review checks and examples needed offline. Source links are optional attribution. Verify a check against local code/configuration before reporting; unknown version-specific behavior remains unverified. Shared severity, gates, and opt-ins stay in the bundled skill.

## Dockerfile
- Inspect user, capabilities, host mounts, and writable paths together. Root inside a container is not by itself a proven host escape; unnecessary privilege plus accessible host resources can create a concrete exposure. Follow the workload’s required security policy.
- Base image on a floating tag (`:latest`, `:3`) rather than pinned, ideally by digest — builds become irreproducible.
- **Secrets in build args, `ENV`, or a `COPY`ed file persist in image layers** even if a later layer deletes them. Use build secrets or runtime injection.
- `COPY . .` with no `.dockerignore` ships `.git`, `.env`, and local credentials into the image.
- No `HEALTHCHECK`, or one that only checks the process is alive.
- Package manager cache not cleaned; no multi-stage build, so compilers and dev dependencies ship to production.
- `CMD` via a shell wrapper so the process does not receive `SIGTERM` as PID 1 — breaks graceful shutdown.

**Evidence and correction:** Inspect final layers, build context, effective command/user, and signal handling. Demonstrate that a secret enters persisted history/artifacts or untrusted content enters the image. A missing HEALTHCHECK or multi-stage build is not a defect when orchestration or packaging already covers the need.

## Kubernetes
- **Missing resource requests and limits** — one pod can starve the node; no requests means unpredictable scheduling.
- No `readinessProbe`: traffic reaches a pod before it is ready. A `livenessProbe` that checks a *dependency* restarts healthy pods when the dependency blips — a common self-inflicted outage.
- `terminationGracePeriodSeconds` shorter than the app's shutdown, or the app ignoring `SIGTERM`: in-flight requests are killed on every deploy.
- `replicas: 1` for something on the request path, and no `PodDisruptionBudget`.
- Secret references in env and mounted files are both supported. `describe pod` normally shows a secret reference rather than its value; application logs, process access, dumps, and RBAC still need review. Plaintext committed credentials are a separate verified exposure.
- `securityContext` missing: `runAsNonRoot`, `readOnlyRootFilesystem`, dropped capabilities, `allowPrivilegeEscalation: false`. `privileged: true` or `hostPath`/`hostNetwork` needs a strong reason.
- Overly broad RBAC — a `ClusterRole` with `*` verbs or resources.
- `imagePullPolicy` plus a mutable tag means different nodes can run different code.
- No `NetworkPolicy` in a cluster that otherwise has them, leaving the new workload open.
- Rollout strategy: `maxUnavailable` during a migration-sensitive deploy; init containers for migrations that run once per pod.

**Evidence and correction:** Compare deployment/probe/resource/security settings with workload behavior and adopted cluster policy. Test readiness and graceful termination assumptions; CPU limits, PDBs, and replica counts involve real availability tradeoffs rather than a universal checklist. Verify secret values are actually exposed before reporting leaks.

## Terraform / IaC
- Inspect stateful replacements in a supplied plan for retained storage, snapshots, cutover, and intentional recreation. A replacement is not automatically data loss; block a confirmed destructive change or required-policy violation. `prevent_destroy` can prevent planned destruction while present, but does not protect a resource whose configuration is removed.
- Plan output not reviewed, or the PR changes resources it does not mention.
- Hardcoded secrets in `.tf` or committed `.tfvars`; state stored without encryption or locking.
- `count` used where `for_each` belongs: removing a middle element shifts indices and destroys and recreates unrelated resources.
- Provider and module versions unpinned.
- Security groups / firewall rules opened to `0.0.0.0/0`, public buckets, disabled encryption or logging.
- IAM policies with `*` actions or resources.
- Drift between environments — a change applied to one environment's config only.

**Evidence and correction:** Use the supplied plan to identify object identities and destructive transitions. Check snapshots, retained volumes, replacements, dependencies, and environment scope. A plan may contain secrets; cite only sanitized evidence. Do not run plan when its provider/data sources could make unapproved external calls.

## CI/CD
- Third-party actions/images unpinned — pin to a commit SHA, since a tag can be moved.
- Excessive token permissions; default write-all where read is enough.
- **A workflow that runs untrusted PR code with access to secrets** (`pull_request_target`, or a self-hosted runner on fork PRs) is a credential-exfiltration path.
- Secrets echoed into logs, or a build step printing the environment.
- Cache keys that let a PR poison a shared cache consumed by the default branch.
- A pipeline step made non-blocking (`|| true`, `continue-on-error`) so a failing gate silently passes.
- Check production deployment controls against adopted policy; automatic deploys may be intentional. Verify secrets, environment boundaries, artifact identity, and rollback rather than requiring a manual gate universally.
- Migrations run automatically on deploy with no backup step, where the project's convention is manual.

**Evidence and correction:** Trace trigger, trust boundary, checkout ref, token permissions, secrets, caches, and published artifacts. An untrusted fork workflow is dangerous when it actually executes attacker code with authority. A trigger name alone does not establish execution or exfiltration.

## Configuration
- A new required setting with no default and no entry in the env example — the service starts and fails on first use.
- Timeout, pool-size, and replica values changed without a stated reason.
- Log level raised to debug in a production config (volume, cost, and possible PII).

**Evidence and correction:** Trace each new required setting into deployment configuration and startup validation. Missing example documentation alone is not proof that production will fail; missing runtime supply plus a required read is. Estimate meaningful effects of timeouts/pools/logging using service constraints.

## Worked example and counterexample

```dockerfile
# Unsafe credential persistence when TOKEN is a real build credential.
ARG TOKEN
RUN echo "$TOKEN" > /root/token
# Prefer an ephemeral BuildKit mount; do not copy its contents into output.
RUN --mount=type=secret,id=token test -s /run/secrets/token
```

The second command demonstrates mount access only. An actual build tool should consume the secret directly and avoid echoing it into logs, generated files, or layers.

## Sources and maintenance

[Docker build secrets](https://docs.docker.com/build/building/secrets/); [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/); [Terraform lifecycle](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle). Source checks: **2026-10-26**. This is a review-focused summary in original wording, not a complete vendor manual or a guarantee for unlisted/newer versions. Recheck source claims when maintaining this file; ordinary reviews need no network.
