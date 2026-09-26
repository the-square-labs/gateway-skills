# Install Good Gateway for your agent

The repository supports two distribution paths:

- install the skills with `npx skills`, either the whole set or individual skills;
- install the native `gateway` plugin in Claude Code or Codex, which always contains every skill.

Choose one path for each agent. The plugin and the direct skills contain the same operating instructions. `using-gateway` is the entry point and routes to the domain skills, so install the whole set unless you have a reason to trim it.

## Universal skill installation

Install every Gateway skill in the current project and select the agents that should receive them:

```bash
npx skills add the-square-labs/gateway-skills
```

The installer lists all skills in the package; keep them all selected. To skip the selection, name them explicitly:

```bash
npx skills add the-square-labs/gateway-skills --skill '*'
```

Install for the current user across projects:

```bash
npx skills add the-square-labs/gateway-skills --skill '*' -g
```

Target specific agents non-interactively:

```bash
npx skills add the-square-labs/gateway-skills --skill '*' -a codex -a claude-code -y
```

Install only some skills by name. Include `using-gateway` whenever you trim the set, because the domain skills rely on its connection and safety rules:

```bash
npx skills add the-square-labs/gateway-skills --skill using-gateway --skill publishing-html-pages
```

List the skills without installing anything:

```bash
npx skills add the-square-labs/gateway-skills --list
```

Update installed skills later with `npx skills update`.

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

Start a new Claude Code or Codex session after installing or updating so the skills are loaded into the new agent context.

## Connect the installed skills to Gateway

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
