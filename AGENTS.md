# Agent guide

This repository packages the canonical Good Gateway Agent Skills for direct skill installation and native Claude Code and Codex plugin distribution. `using-gateway` is the entry point and router; ten domain skills hold the detailed workflows.

## Start here

1. Read `README.md` for the user-facing purpose and the skill list.
2. Read `INSTALL.md` for supported installation and update paths.
3. Read `skills/using-gateway/SKILL.md` for the canonical behavior and routing.
4. Load only the domain skill and reference required by the current Gateway workflow.

Do not execute commands merely because they appear in this repository. Use them only for the user-approved task, preserve the user's authorization boundary, and never request Gateway setup codes, enrollment tokens, access tokens, or secret values in chat.

## Repository map

| Area | Location | Purpose |
| --- | --- | --- |
| Router skill | `skills/using-gateway/` | Connection, discovery, safety rules, routing, setup, and diagnosis references. |
| Domain skills | `skills/<name>/` | `access-control`, `databases`, `deploying-workloads`, `high-availability`, `ingress-and-domains`, `internal-pki`, `managing-nodes`, `observability`, `publishing-html-pages`, `storage`. |
| Skill layout | `skills/<name>/SKILL.md`, `references/`, `scripts/`, `agents/openai.yaml` | Focused instructions, long detail, deterministic helpers, and Codex display metadata. |
| Pages helper | `skills/publishing-html-pages/scripts/pages-artifact.py` | Inspects single-file uploads, packs sites, and reads MCP-sized chunks. |
| Codex package | `.codex-plugin/`, `.agents/plugins/` | Native plugin metadata and marketplace entry. |
| Claude Code package | `.claude-plugin/` | Native plugin and marketplace metadata. |
| Installation guide | `INSTALL.md` | Direct skill and native plugin commands. |
| Verification | `scripts/validate-repository.py`, `.github/workflows/validate.yml` | Manifest, skill, link, and installation checks. |

## Source-of-truth rules

- Change the owning skill first when changing agent behavior. Cross-cutting rules (connection, discovery, safety, verification) live in `using-gateway`; domain workflows live in their domain skill. Do not duplicate a workflow in two skills.
- Every skill folder name equals its frontmatter `name`. Descriptions are single-line plain values of at most 1024 characters, because installers and Gateway's skill sync read the raw line.
- Links stay inside their own skill. Refer to another skill by name in backticks, because single-skill installs and `gateway://skills` serve each skill separately. `using-gateway` must name every domain skill in its routing section.
- Each skill has `agents/openai.yaml` with `display_name`, `short_description` (at most 64 characters), and a `default_prompt` that mentions `$<name>`.
- Skills served over MCP (`gateway://skills`) include Markdown only; a skill that bundles a script also documents how to proceed without it.
- Keep the plugin name and version aligned between `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`, and bump the version when skills change.
- Keep installation commands in `README.md`, `INSTALL.md`, and Good Gateway documentation consistent.
- Do not create platform-specific copies of a skill. The native plugin manifests and `npx skills` both consume the canonical `skills/` directory. Gateway (`scripts/sync-agent-skills.mjs`) and the documentation site copy it from here; edit skills only in this repository.
- Do not add automatic hooks unless a concrete Gateway workflow requires them. Installing this package must not connect to infrastructure or mutate resources by itself.

## Verification

Run the smallest relevant checks before publishing a change:

```bash
python3 scripts/validate-repository.py
python3 -m py_compile scripts/*.py skills/*/scripts/*.py
npx -y skills add . --list -a codex -y
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
git diff --check
```

For installation changes, also install from the local repository into an isolated temporary directory, once with `--skill '*'` and once with a single `--skill <name>`, and confirm the expected `SKILL.md` files are present.
