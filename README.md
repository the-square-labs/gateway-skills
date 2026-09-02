# Good Gateway for AI agents

Give Codex, Claude Code, Cursor, and other compatible coding agents the operating context they need to work with [Good Gateway](https://goodgateway.dev) through its authenticated remote MCP server.

## Quick install

The universal Agent Skills route works across supported agents:

```bash
npx skills add the-square-labs/gateway-skills --skill using-gateway
```

Native plugin installation is also available:

```bash
# Claude Code
claude plugin marketplace add the-square-labs/gateway-skills
claude plugin install gateway@gateway-skills

# Codex
codex plugin marketplace add the-square-labs/gateway-skills --ref main
codex plugin add gateway@gateway-skills
```

Use one installation route per agent, then start a new session. See [INSTALL.md](INSTALL.md) for global installation, updates, verification, and MCP connection commands.

You can also ask an agent to install it for you:

```text
Install the Good Gateway skill or native plugin from
https://github.com/the-square-labs/gateway-skills, follow its AGENTS.md and
INSTALL.md, then help me connect my Gateway instance through OAuth MCP.
```

The package does not connect to infrastructure or run anything automatically. Ask your agent to connect to your Gateway installation or use an existing `good-gateway` MCP connection.

The skill teaches agents Gateway's actual resource model and MCP workflow: tool discovery, setup and OAuth, Build admission, Pages artifact upload, Docker and Compose ownership, database bindings, ingress, asynchronous Tasks, layered verification, and native rollback.

## Canonical skill

- `using-gateway`: install or connect Gateway, choose the correct deployment model, operate and diagnose resources, and return a verified result or a precise blocker.

Connection and product documentation is available at [docs.goodgateway.dev](https://docs.goodgateway.dev/en/ai/agent-skills/).

## Package layout

- `skills/using-gateway`: the single source of truth consumed by direct skill and native plugin installations.
- `.codex-plugin` and `.agents/plugins`: Codex package and marketplace metadata.
- `.claude-plugin`: Claude Code package and marketplace metadata.
- `assets`: plugin presentation assets.

No always-on hooks are included. Gateway access remains explicit and governed by the connected user's OAuth session, scopes, confirmations, and the task requested by the user.

## License

The skill instructions in this repository are available under the MIT License. Good Gateway itself is distributed under its own license terms.
