# Gateway MCP connection

Use this reference only when Gateway remote MCP is missing, unauthenticated, or connected to the wrong instance. If Gateway itself is not installed, still requires first-run setup, or has no Node suitable for the workload, read [New instance setup](instance-setup.md) first.

## Endpoint

Gateway exposes one Streamable HTTP MCP endpoint:

```text
https://<gateway-host>/api/mcp
```

Normalize a base URL by removing a trailing slash before adding `/api/mcp`. Prefer HTTPS. Do not infer a production hostname from a repository name, email domain, or previous task.

## Codex

Inspect existing configuration first:

```bash
codex mcp get gateway
```

If no `gateway` server exists:

```bash
codex mcp add gateway --url https://gateway.example.com/api/mcp
codex mcp login gateway
codex mcp list
```

If `gateway` already points elsewhere, report the mismatch before replacing it. Use a distinct name such as `gateway-staging` when the user needs multiple installations.

## Claude Code

```bash
claude mcp add --transport http gateway --scope user https://gateway.example.com/api/mcp
claude mcp login gateway
claude mcp get gateway
```

Use project scope only when the repository should share the server definition; every developer still signs in with their own Gateway account.

## Authentication and scopes

Gateway uses OAuth Authorization Code with PKCE and dynamic client registration. Let the user complete browser login and consent. Never ask them to paste the resulting token.

Gateway MCP accepts only OAuth access tokens issued for the MCP resource. Ordinary `gw_` API tokens, browser cookies, `gwl_` logging tokens, `gwi_` inference tokens, and OAuth tokens for another resource are not substitutes.

The account requires `mcp:use` plus scopes for the intended resources. If a tool is absent, distinguish an undiscovered toolset from a missing scope, entitlement, disabled MCP server, unavailable subsystem, or incompatible client.

After setup, refresh MCP tools or start a new task if the host cannot hot-load the connection. Do not create a plugin-owned proxy or store credentials in the skill directory.
