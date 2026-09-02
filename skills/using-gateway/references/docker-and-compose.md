# Docker, Deployments, and Compose

Use this reference for Dockerfile, image, blue/green, and Compose applications.

## Git source builds

Before creating a source-backed resource, call the source `admission` operation. Admission requires the applicable entitlement, writable internal registry, allowlisted Git connector, and online Build Worker advertising the enforced capabilities. Resolve the requested branch to an exact commit.

Use `manage_docker_source` with:

- `targetType: container` for an ordinary single service;
- `targetType: deployment` for health-checked blue/green cutover and rollback;
- `targetType: compose` for a first-class Compose Project.

Use `create` for a new resource and `upsert` when attaching or changing the source of an existing resource. Keep build secrets and runtime secrets separate. Follow builds with `list_docker_builds` and `manage_docker_build`; an approved artifact digest, not a source branch name, is the runtime identity.

If admission fails, fix or report the returned entitlement, connector, registry, or builder prerequisite. Do not silently create an external CI pipeline as a workaround.

## Existing images

If an approved image already exists, inspect and pull it to the selected Docker Node before creating the resource. Prefer Gateway-managed volumes and explicit networks. Apply secrets through dedicated secret operations.

## Blue/green Deployments

Use a Deployment when controlled traffic switch, health validation, and rollback are material. Operate the Deployment resource, never its protected slot Containers. Do not switch traffic until the new slot satisfies the configured health condition.

## Compose Projects

Use `manage_docker_compose` for manual image-only YAML and lifecycle. Use `manage_docker_source` with `targetType: compose` for repository Compose files containing the supported build subset.

Compose invariants:

- one project is placed on one Docker Node;
- revisions are immutable;
- repository builds create one isolated child build per build-enabled service;
- a revision is applied only after all expected child artifacts are approved;
- Routes and Secure Links target the project/service identity;
- child Containers, project-owned networks, and volumes are protected from standalone mutation;
- persistent volumes are not deleted unless the user explicitly selects them;
- external Compose Projects remain read-only until adopted with complete YAML.

Manual YAML is image-only. Repository Compose may use the currently supported bounded build fields. Report unsupported fields from validation instead of silently dropping them.

Treat start, stop, restart, apply, pull/apply, down, cancellation, project deletion, and volume deletion as distinct lifecycle operations. Destructive `down` or `delete_volumes` requires explicit user intent.
