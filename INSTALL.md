# Install Good Gateway for your agent

The repository supports two equivalent distribution paths:

- install the canonical `using-gateway` skill with `npx skills`;
- install the native `gateway` plugin in Claude Code or Codex.

Choose one path for each agent. The plugin and direct skill contain the same operating instructions.

## Universal skill installation

Install in the current project and select the agents that should receive it:

```bash
npx skills add the-square-labs/gateway-skills --skill using-gateway
```

Install for the current user across projects:

```bash
npx skills add the-square-labs/gateway-skills --skill using-gateway -g
```

To target specific agents non-interactively:

```bash
npx skills add the-square-labs/gateway-skills --skill using-gateway -a codex -a claude-code -y
```

## Claude Code plugin

```bash
claude plugin marketplace add the-square-labs/gateway-skills
claude plugin install gateway@gateway-skills
```

Verify or update it:

```bash
claude plugin list
claude plugin marketplace update gateway-skills
```

## Codex plugin

```bash
codex plugin marketplace add the-square-labs/gateway-skills --ref main
codex plugin add gateway@gateway-skills
```

Verify or update it:

```bash
codex plugin list
codex plugin marketplace upgrade gateway-skills
codex plugin remove gateway
codex plugin add gateway@gateway-skills
```

Start a new Claude Code or Codex session after installing or updating so the skill is loaded into the new agent context.

## Connect the installed skill to Gateway

This package does not bundle a fixed MCP server because every Good Gateway installation has its own hostname and OAuth boundary.

For Codex:

```bash
codex mcp add good-gateway --url https://gateway.example.com/api/mcp
codex mcp login good-gateway
```

For Claude Code:

```bash
claude mcp add --transport http good-gateway --scope user https://gateway.example.com/api/mcp
claude mcp login good-gateway
```

Replace `gateway.example.com` with the public hostname of your installation. Complete authentication in the browser; do not paste a Gateway API token into the agent chat.

See the [Good Gateway agent guide](https://docs.goodgateway.dev/en/ai/agent-skills/) for permissions, first prompts, and MCP setup details.
