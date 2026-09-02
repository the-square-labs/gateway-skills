#!/usr/bin/env python3

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    path = ROOT / relative_path
    if not path.is_file():
        raise SystemExit(f"missing required file: {relative_path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"invalid JSON in {relative_path}: {error}") from error


codex = load_json(".codex-plugin/plugin.json")
claude = load_json(".claude-plugin/plugin.json")
codex_marketplace = load_json(".agents/plugins/marketplace.json")
claude_marketplace = load_json(".claude-plugin/marketplace.json")

for key in ("name", "version", "description", "author"):
    if not codex.get(key):
        raise SystemExit(f"Codex manifest is missing {key}")
    if not claude.get(key):
        raise SystemExit(f"Claude manifest is missing {key}")

if codex["name"] != claude["name"]:
    raise SystemExit("plugin names differ between Codex and Claude manifests")
if codex["version"] != claude["version"]:
    raise SystemExit("plugin versions differ between Codex and Claude manifests")
if not re.fullmatch(r"\d+\.\d+\.\d+", codex["version"]):
    raise SystemExit("plugin version must be strict semver")

skill_path = ROOT / "skills/using-gateway/SKILL.md"
skill_text = skill_path.read_text(encoding="utf-8")
if not skill_text.startswith("---\n") or "name: using-gateway" not in skill_text:
    raise SystemExit("canonical using-gateway skill has invalid frontmatter")

for relative_path in re.findall(r"\]\((references/[^)]+|scripts/[^)]+)\)", skill_text):
    target = skill_path.parent / relative_path
    if not target.is_file():
        raise SystemExit(f"skill links to missing file: {relative_path}")

interface = codex.get("interface", {})
for key in ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities"):
    if not interface.get(key):
        raise SystemExit(f"Codex interface is missing {key}")

for asset_key in ("composerIcon", "logo"):
    relative_path = interface.get(asset_key)
    if not relative_path or not (ROOT / relative_path).is_file():
        raise SystemExit(f"Codex interface references a missing {asset_key}")

codex_entries = codex_marketplace.get("plugins", [])
claude_entries = claude_marketplace.get("plugins", [])
if len(codex_entries) != 1 or codex_entries[0].get("name") != codex["name"]:
    raise SystemExit("Codex marketplace must expose exactly the canonical plugin")
if len(claude_entries) != 1 or claude_entries[0].get("name") != claude["name"]:
    raise SystemExit("Claude marketplace must expose exactly the canonical plugin")

source = codex_entries[0].get("source", {})
if source.get("source") != "url" or source.get("url") != "https://github.com/the-square-labs/gateway-skills.git":
    raise SystemExit("Codex marketplace must reference the public repository root")
if claude_entries[0].get("source") != "./":
    raise SystemExit("Claude marketplace must reference the repository root")

print(f"validated gateway plugin {codex['version']} and using-gateway skill")
