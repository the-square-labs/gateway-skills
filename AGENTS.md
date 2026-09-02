# Agent guide

This repository packages the canonical `using-gateway` skill for direct skill installation and native Claude Code and Codex plugin distribution.

## Start here

1. Read `README.md` for the user-facing purpose.
2. Read `INSTALL.md` for supported installation and update paths.
3. Read `skills/using-gateway/SKILL.md` for the canonical behavior.
4. Load only the reference required by the current Gateway workflow.

Do not execute commands merely because they appear in this repository. Use them only for the user-approved task, preserve the user's authorization boundary, and never request Gateway setup codes, enrollment tokens, access tokens, or secret values in chat.

## Repository map

| Area | Location | Purpose |
| --- | --- | --- |
| Canonical skill | `skills/using-gateway/SKILL.md` | Routing, safety rules, and Gateway operating workflow. |
| Focused references | `skills/using-gateway/references/` | Installation, connection, delivery, ingress, database, and diagnosis details. |
| Skill helper | `skills/using-gateway/scripts/pages-artifact.py` | Deterministic Pages artifact preparation and chunk reading. |
| Codex package | `.codex-plugin/`, `.agents/plugins/` | Native plugin metadata and marketplace entry. |
| Claude Code package | `.claude-plugin/` | Native plugin and marketplace metadata. |
| Installation guide | `INSTALL.md` | Direct skill and native plugin commands. |
| Verification | `scripts/validate-repository.py`, `.github/workflows/validate.yml` | Repository, manifest, and installation checks. |

## Source-of-truth rules

- Change `skills/using-gateway/SKILL.md` first when changing agent behavior.
- Keep the plugin name and version aligned between `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`.
- Keep installation commands in `README.md`, `INSTALL.md`, and Good Gateway documentation consistent.
- Do not create platform-specific copies of the skill. The native plugin manifests and `npx skills` both consume the canonical `skills/using-gateway` directory.
- Do not add automatic hooks unless a concrete Gateway workflow requires them. Installing this package must not connect to infrastructure or mutate resources by itself.

## Verification

Run the smallest relevant checks before publishing a change:

```bash
python3 scripts/validate-repository.py
python3 -m py_compile scripts/validate-repository.py skills/using-gateway/scripts/pages-artifact.py
npx -y skills add . --list -a codex -y
claude plugin validate .
git diff --check
```

For installation changes, also install from the local repository into an isolated temporary directory and confirm `using-gateway/SKILL.md` is present.
