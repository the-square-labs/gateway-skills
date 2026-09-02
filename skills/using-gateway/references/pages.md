# Deploying Gateway Pages

Use this reference for static sites and frontend build output.

## Choose local artifact or Git source

Use a Git source when the repository is available through an allowlisted connector and repeatable push-to-deploy is desired. Use MCP artifact upload for local-only changes, an already prepared output directory, or source that should intentionally remain disconnected from Gateway.

## Git-backed Pages

Git source builds require the applicable entitlement, allowlisted connector, writable internal registry, and online Build Worker.

1. Discover or create the Pages Project on a Pages-capable Ingress Node.
2. Use `manage_pages` source discovery to inspect the repository and package manifest.
3. Configure application root, package manager, runtime version, build script, artifact directory, publication Tag, automatic build/deploy, public build variables, Build Secret names, and vulnerability policy.
4. Store secret values through source-secret operations only.
5. Start the build when it is not queued automatically.
6. Follow the build with `list_docker_builds` and `manage_docker_build` until the immutable artifact is approved and the Pages Deployment is ready.
7. Confirm the intended mutable Tag points to the ready Deployment.

Frontend-prefixed build variables are public by construction; never put secrets in them or expose Build Secret values in chat.

## Local artifact upload

Build using the repository's own instructions and select the actual static output directory. Resolve the bundled helper relative to this skill directory:

```bash
python3 <skill-dir>/scripts/pages-artifact.py prepare ./dist --output /tmp/gateway-pages.tar.gz
```

The helper returns the archive path, exact byte size, and SHA-256. Use `upload_pages_artifact`:

1. `begin` with the Pages Project ID, declared size, SHA-256, idempotency key, optional Tag, and safe source metadata;
2. read each chunk with `pages-artifact.py chunk ... --offset <nextOffset>`;
3. send the returned base64 content and continue from the acknowledged `nextOffset`;
4. call `finalize`, then read the resulting Deployment and Tag.

The MCP connection supplies authentication. Never pass a deploy token or Authorization header to the artifact tool, restart from offset zero after an acknowledged chunk, or include base64 payloads in the final response.

## Publication and rollback

Routes target ready mutable Tags. The system `latest` Tag follows successful publication; use a named Tag such as `production` when an explicit release pointer or rollback control is needed. Roll back by moving the Tag to a previous ready immutable Deployment.

Runtime configuration is public browser data and must not contain secrets.
