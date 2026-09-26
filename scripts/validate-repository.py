#!/usr/bin/env python3

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
ROUTER_SKILL = "using-gateway"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
FENCE_PATTERN = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.DOTALL | re.MULTILINE)
INLINE_CODE_PATTERN = re.compile(r"`[^`\n]*`")
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SCHEME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
HEADING_PATTERN = re.compile(r"^#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$", re.MULTILINE)

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def load_json(relative_path: str) -> dict:
    path = ROOT / relative_path
    if not path.is_file():
        raise SystemExit(f"missing required file: {relative_path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"invalid JSON in {relative_path}: {error}") from error


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


# --- Plugin manifests -------------------------------------------------------

codex = load_json(".codex-plugin/plugin.json")
claude = load_json(".claude-plugin/plugin.json")
codex_marketplace = load_json(".agents/plugins/marketplace.json")
claude_marketplace = load_json(".claude-plugin/marketplace.json")

for key in ("name", "version", "description", "author"):
    if not codex.get(key):
        fail(f"Codex manifest is missing {key}")
    if not claude.get(key):
        fail(f"Claude manifest is missing {key}")

if codex.get("name") != claude.get("name"):
    fail("plugin names differ between Codex and Claude manifests")
if codex.get("version") != claude.get("version"):
    fail("plugin versions differ between Codex and Claude manifests")
if not re.fullmatch(r"\d+\.\d+\.\d+", str(codex.get("version", ""))):
    fail("plugin version must be strict semver")
if codex.get("skills") != "./skills/":
    fail('Codex manifest must expose skills from "./skills/"')

interface = codex.get("interface", {})
for key in ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities"):
    if not interface.get(key):
        fail(f"Codex interface is missing {key}")

for asset_key in ("composerIcon", "logo"):
    asset_path = interface.get(asset_key)
    if not asset_path or not (ROOT / asset_path).is_file():
        fail(f"Codex interface references a missing {asset_key}")

codex_entries = codex_marketplace.get("plugins", [])
claude_entries = claude_marketplace.get("plugins", [])
if len(codex_entries) != 1 or codex_entries[0].get("name") != codex.get("name"):
    fail("Codex marketplace must expose exactly the canonical plugin")
if len(claude_entries) != 1 or claude_entries[0].get("name") != claude.get("name"):
    fail("Claude marketplace must expose exactly the canonical plugin")

source = codex_entries[0].get("source", {}) if codex_entries else {}
if source.get("source") != "url" or source.get("url") != "https://github.com/the-square-labs/gateway-skills.git":
    fail("Codex marketplace must reference the public repository root")
if claude_entries and claude_entries[0].get("source") != "./":
    fail("Claude marketplace must reference the repository root")


# --- Skills -----------------------------------------------------------------


def parse_frontmatter(skill_file: Path) -> dict[str, str] | None:
    """Parse the flat `key: value` frontmatter that skill installers and Gateway's skill sync read."""
    match = FRONTMATTER_PATTERN.match(skill_file.read_text(encoding="utf-8"))
    if not match:
        fail(f"{relative(skill_file)}: missing frontmatter delimited by --- lines")
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if line[0].isspace() or ":" not in line:
            fail(f"{relative(skill_file)}: frontmatter must be flat single-line `key: value` pairs, got {line!r}")
            continue
        key, value = line.split(":", 1)
        if key in fields:
            fail(f"{relative(skill_file)}: duplicate frontmatter key {key!r}")
        fields[key] = value.strip()
    return fields


def check_plain_scalar(skill_file: Path, key: str, value: str) -> None:
    """Values must be unquoted single-line YAML plain scalars: the sync scripts read the raw line."""
    if value[:1] in "\"'|>&*!%@`{[#,?-" or value.endswith(":"):
        fail(f"{relative(skill_file)}: frontmatter {key} must be an unquoted single-line plain value")
    if ": " in value or " #" in value:
        fail(f"{relative(skill_file)}: frontmatter {key} must not contain ': ' or ' #' (invalid plain YAML)")
    if "<" in value or ">" in value:
        fail(f"{relative(skill_file)}: frontmatter {key} must not contain angle brackets")


def heading_anchors(markdown_file: Path) -> set[str]:
    text = FENCE_PATTERN.sub("", markdown_file.read_text(encoding="utf-8"))
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for heading in HEADING_PATTERN.findall(text):
        plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading).replace("`", "")
        slug = re.sub(r"[^\w\- ]", "", plain.strip().lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors


def check_links(skill_dir: Path, markdown_file: Path) -> None:
    text = INLINE_CODE_PATTERN.sub("", FENCE_PATTERN.sub("", markdown_file.read_text(encoding="utf-8")))
    for target in LINK_PATTERN.findall(text):
        if SCHEME_PATTERN.match(target):
            continue
        path_part, _, anchor = target.partition("#")
        resolved = (markdown_file.parent / path_part).resolve() if path_part else markdown_file
        where = f"{relative(markdown_file)} -> {target}"
        if skill_dir.resolve() not in resolved.parents and resolved != skill_dir.resolve():
            fail(f"{where}: links must stay inside the skill; refer to other skills by name")
            continue
        if not resolved.exists():
            fail(f"{where}: target does not exist")
            continue
        if anchor:
            if resolved.suffix != ".md" or not resolved.is_file():
                fail(f"{where}: anchors are only checked in Markdown files")
            elif anchor not in heading_anchors(resolved):
                fail(f"{where}: no heading for anchor #{anchor}")


def check_openai_metadata(skill_dir: Path, name: str) -> None:
    metadata = skill_dir / "agents" / "openai.yaml"
    if not metadata.is_file():
        fail(f"{relative(skill_dir)}: missing agents/openai.yaml")
        return
    text = metadata.read_text(encoding="utf-8")
    values = dict(re.findall(r'^  (display_name|short_description|default_prompt): "([^"\n]+)"$', text, re.MULTILINE))
    if not text.startswith("interface:\n"):
        fail(f"{relative(metadata)}: must start with an interface: mapping")
    for key in ("display_name", "short_description", "default_prompt"):
        if not values.get(key):
            fail(f"{relative(metadata)}: missing quoted interface.{key}")
    if len(values.get("short_description", "")) > 64:
        fail(f"{relative(metadata)}: short_description must be at most 64 characters")
    if f"${name}" not in values.get("default_prompt", ""):
        fail(f"{relative(metadata)}: default_prompt must mention ${name}")


if not SKILLS_DIR.is_dir():
    raise SystemExit("missing skills/ directory")

skill_names: dict[str, Path] = {}
for skill_dir in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        fail(f"{relative(skill_dir)}: missing SKILL.md")
        continue
    fields = parse_frontmatter(skill_file)
    if fields is None:
        continue

    name = fields.get("name", "")
    description = fields.get("description", "")
    if name != skill_dir.name:
        fail(f"{relative(skill_file)}: frontmatter name {name!r} must equal the folder name {skill_dir.name!r}")
    if not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        fail(f"{relative(skill_file)}: name must be lowercase words joined by hyphens, at most 64 characters")
    if not 1 <= len(description) <= 1024:
        fail(f"{relative(skill_file)}: description must be 1-1024 characters, found {len(description)}")
    for key in ("name", "description"):
        if fields.get(key):
            check_plain_scalar(skill_file, key, fields[key])

    if name in skill_names:
        fail(f"duplicate skill name {name!r} in {relative(skill_names[name])} and {relative(skill_dir)}")
    skill_names[name] = skill_dir

    for markdown_file in sorted(skill_dir.rglob("*.md")):
        check_links(skill_dir, markdown_file)
    check_openai_metadata(skill_dir, name)

if ROUTER_SKILL not in skill_names:
    fail(f"canonical router skill {ROUTER_SKILL!r} is missing")
else:
    router_text = (skill_names[ROUTER_SKILL] / "SKILL.md").read_text(encoding="utf-8")
    for name in skill_names:
        if name != ROUTER_SKILL and f"`{name}`" not in router_text:
            fail(f"{ROUTER_SKILL} must route to the {name!r} skill by name")

if errors:
    raise SystemExit("repository validation failed:\n" + "\n".join(f"- {error}" for error in errors))

print(f"validated gateway plugin {codex['version']} and {len(skill_names)} skills: {', '.join(skill_names)}")
