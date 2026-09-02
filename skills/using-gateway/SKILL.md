---
name: using-gateway
description: Deploy, publish, configure, diagnose, or operate applications through a user-owned Good Gateway instance using its authenticated remote MCP. Use for Gateway setup, Pages, Docker containers, blue/green deployments, Compose Projects, Git builds, Build Workers, Domains, certificates, Routes, databases, and deployment verification. Do not use for generic Docker or hosting work that is not targeting Gateway.
---

# Using Gateway

Turn the user's application intent into one native Gateway workflow. Gateway owns deployment state, builds, artifacts, Compose revisions, domains, certificates, Routes, permissions, Tasks, and rollback-capable resources. Do not build a parallel orchestrator around shell access when Gateway MCP exposes the operation.

## Connect and discover

Use existing Gateway MCP tools when they are already available. If no usable Gateway instance exists, setup is incomplete, or the user wants a new installation, read [New instance setup](references/instance-setup.md). If the instance is ready but MCP is unavailable, unauthenticated, or points at the wrong instance, read [MCP connection](references/connection.md).

Never ask the user to paste an OAuth token, API token, setup code, node enrollment token, deploy token, registry password, database credential, or secret into chat.

Activate only the Gateway toolsets required for the request. Use `discover_tools`, then refresh the tool list after activation. Common toolsets include `pages`, `docker`, `proxy`, `nodes`, `databases`, and `system`. Before complex or recently added operations, use `read_gateway_documentation` or scoped `gateway://docs` resources instead of relying on remembered arguments. Use `find_resource` for names, domains, images, containers, deployments, Compose Projects, Pages Projects, certificates, nodes, databases, and builds; never invent resource IDs.

## Route the request

- New control plane, unfinished onboarding, or missing Nodes: read [New instance setup](references/instance-setup.md).
- MCP connection or OAuth problem: read [MCP connection](references/connection.md).
- Local static output or a static project with local-only changes: read [Pages](references/pages.md) and use artifact upload.
- Git-backed frontend or static site: use a Pages Project Git source and Gateway Build Worker.
- Git repository with a Dockerfile: create or attach a source to a standalone Container or blue/green Deployment.
- Existing Docker image, Dockerfile, or Compose application: read [Docker and Compose](references/docker-and-compose.md).
- Public hostname, TLS, Route, Secure Link, or reachability: read [Ingress](references/ingress.md).
- Managed or external PostgreSQL, Redis, ClickHouse, or application binding: read [Databases](references/databases.md).
- Incident, warning, failed Task, offline Node, or unexplained state: read [Diagnosis](references/diagnosis.md).

If an existing Gateway resource already represents the application, update or attach its source instead of creating a duplicate.

## Choose the native resource model

Prefer Pages for static output. Prefer a standalone Container for one ordinary service. Prefer a blue/green Deployment when health-checked cutover and rollback matter. Prefer a Compose Project when the application has multiple services or the repository already defines Compose. Prefer a private database binding over distributing owner credentials.

Inspect whether the repository already has a healthy deployment pipeline. If Gateway Git-source builds are admitted and no deployment CI exists, use Gateway source bindings, Build Workers, `autoBuild`, and `autoDeploy` instead of authoring CI solely to deploy through Gateway. Preserve an existing release pipeline unless the user asks to replace it.

## Preflight before promising success

Check only prerequisites relevant to the selected path:

- effective scopes, `mcp:use`, and feature entitlement;
- suitable online Nodes and advertised capabilities;
- build admission, allowlisted Git connector, exact repository and branch, writable internal registry, and Build Worker readiness;
- existing resources, conflicting names, active Tasks, Domains, certificates, Routes, Tags, and ownership;
- application port, health endpoint, persistent storage, build variables, runtime configuration, and secrets;
- database engine, placement, backup/recovery expectation, and binding target;
- DNS control and the intended public hostname.

Ask one focused question only when a missing value changes the resource model, target environment, availability, data safety, or external mutation. A deployment request authorizes ordinary create, build, publish, and verification operations for the named application and target. It does not authorize overwriting conflicting DNS, replacing an unrelated live Route, deleting persistent volumes or databases, destructive Compose `down`, rotating secrets, broadening permissions, or adopting a resource with unclear ownership.

## Execute, reconcile, and verify

Use Gateway-native state transitions and read the resulting resource after each asynchronous boundary. Do not treat a queued build, created Task, pending certificate, container start, Compose operation, database provisioning, migration, or rollout as completion.

1. Record returned resource, operation, request, build, and Task identifiers.
2. Follow the owning Task or status resource until a terminal state or concrete blocker is known.
3. Inspect structured failure details instead of retrying blindly.
4. Read the final desired and reported resource state.
5. Verify the external outcome when one exists: HTTPS response, workload health, database connection through the binding, or published Pages Tag.

Retry only when the failure is understood and the operation is safe to repeat. Never create duplicate resources as a retry strategy. After an ambiguous timeout, reconcile the first operation before repeating creation, deletion, migration, recovery, or credential rotation.

## Return a complete result

On success, report the environment, URL when applicable, resource identity, source commit or immutable artifact, Task/build result, verification evidence, and rollback path. On failure, report the exact missing prerequisite or failed boundary and the smallest safe next action. Never call a partial deployment successful.

## Safety invariants

- Diagnosis, inventory, explanation, and review requests remain read-only.
- Keep secrets write-only and out of ordinary tool arguments, shell history, logs, memory, and final responses.
- Use Gateway-managed volumes; do not introduce host bind mounts or Docker socket access.
- Git deployment uses exact commits and approved immutable artifacts, never a mutable branch or tag as runtime identity.
- Operate Compose Projects and Deployments through their owning resources, never their protected child containers or slots.
- Routes target stable Container names, Deployment IDs, Compose project/service identities, or ready Pages Tags.
- Pages Routes target mutable Tags, not immutable Deployments.
- Preserve a healthy production resource until its replacement passes required health and ingress checks.
- Treat license, permission, entitlement, worker, registry, DNS, certificate, policy, Node connectivity, and application health failures as distinct blockers.
