# Databases and private bindings

Use this reference for external connections, managed PostgreSQL, Redis, or ClickHouse, and private application access.

## Choose the database path

- Existing external database: register a connection only when Gateway should operate or observe it.
- New managed database: select an online compatible Database Node and the engine required by the application.
- Application access: create a private binding with a workload-specific identity instead of exposing the database publicly or sharing owner credentials.

Before provisioning, inspect engine availability, placement, capacity, entitlement, current Tasks, backup expectations, recovery ownership, and existing resources with the same purpose.

## Managed database lifecycle

Provisioning, restart, pause, credential rotation, certificate rotation, and deletion are distinct operations. Follow the returned Task and reported database state. Do not reveal credentials unless the user explicitly needs them for an authorized manual connection, and never repeat them in the final response.

Deleting a binding revokes one application's access. Deleting the managed database removes the database and its managed storage. Never infer authorization for database deletion from a request to disconnect, redeploy, or remove an application.

## Private bindings

Resolve the target workload through its owning Container, Deployment, or Compose Project. Create the binding through Gateway so the application receives a dedicated identity and runtime connection contract. Verify the binding is ready and then verify an application-level connection or query where the workflow supports it.

If the workload is recreated, verify that the binding remains attached through the owning resource model. Do not copy database owner credentials into environment variables as a shortcut.

## Verification

Separate these states:

1. Database resource provisioned and healthy.
2. Binding identity created and ready.
3. Workload received the binding runtime configuration.
4. Application successfully connected and performed the expected operation.

Report the last verified boundary. A healthy database does not prove the application can use it.
