# Good Gateway Agent Skills

Give Codex, Claude Code, Cursor, and other compatible coding agents the operating context they need to work with [Good Gateway](https://goodgateway.dev) through its authenticated remote MCP server.

## Install

Install the skill in the current project:

```bash
npx skills add the-square-labs/gateway-skills --skill using-gateway
```

Or install it globally for your user:

```bash
npx skills add the-square-labs/gateway-skills --skill using-gateway -g
```

Then ask your agent to connect to your Gateway installation or use an existing `good-gateway` MCP connection.

The skill teaches agents Gateway's actual resource model and MCP workflow: tool discovery, setup and OAuth, Build admission, Pages artifact upload, Docker and Compose ownership, database bindings, ingress, asynchronous Tasks, layered verification, and native rollback.

## Included skill

- `using-gateway`: install or connect Gateway, choose the correct deployment model, operate and diagnose resources, and return a verified result or a precise blocker.

Connection and product documentation is available at [docs.goodgateway.dev](https://docs.goodgateway.dev/en/ai/agent-skills/).

## License

The skill instructions in this repository are available under the MIT License. Good Gateway itself is distributed under its own license terms.
