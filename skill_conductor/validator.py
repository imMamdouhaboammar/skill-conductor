"""Portability and structural validation for Skill Conductor."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .constants import (
    ABSOLUTE_PERSONAL_RE,
    KNOWN_TARGETS,
    NAME_RE,
    PROCESS_HINT_RE,
    SECRET_RE,
)


def parse_frontmatter(text: str) -> tuple[str | None, str | None]:
    """Parse YAML frontmatter name and description without heavy dependencies."""
    if not text.startswith("---\n"):
        return None, None
    end = text.find("\n---", 4)
    if end == -1:
        return None, None
    block = text[4:end].splitlines()
    name = None
    description_lines = []
    in_description = False
    for line in block:
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip("'\"")
            in_description = False
        elif line.startswith("description:"):
            value = line.split(":", 1)[1].strip()
            in_description = value in {">", "|", ">-", "|-"} or not value
            if value and not in_description:
                description_lines.append(value.strip("'\""))
        elif in_description and (line.startswith(" ") or line.startswith("\t")):
            description_lines.append(line.strip())
        elif line and not line.startswith(" "):
            in_description = False
    description = " ".join(description_lines).strip() or None
    return name, description


def check_skill(skill_dir: Path) -> list[dict[str, Any]]:
    """Validate a skill folder structure, frontmatter, secrets, and references."""
    findings: list[dict[str, Any]] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [
            {
                "severity": "error",
                "code": "SKILLMD_MISSING",
                "message": "SKILL.md is missing",
            }
        ]

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    name, description = parse_frontmatter(text)

    if not name or not NAME_RE.fullmatch(name):
        findings.append(
            {
                "severity": "error",
                "code": "NAME_INVALID",
                "message": "frontmatter name is missing or not kebab-case",
            }
        )
    if name and skill_dir.name != name:
        findings.append(
            {
                "severity": "error",
                "code": "FOLDER_NAME_MISMATCH",
                "message": f"folder name '{skill_dir.name}' does not match skill name '{name}'",
            }
        )
    if not description:
        findings.append(
            {
                "severity": "error",
                "code": "DESCRIPTION_MISSING",
                "message": "description is missing",
            }
        )
    elif len(description) > 1024:
        findings.append(
            {
                "severity": "error",
                "code": "DESCRIPTION_TOO_LONG",
                "message": f"description exceeds 1024 characters ({len(description)} chars)",
            }
        )
    elif PROCESS_HINT_RE.search(description):
        findings.append(
            {
                "severity": "warning",
                "code": "DESCRIPTION_PROCESS_HINT",
                "message": "description may contain workflow sequencing",
            }
        )

    if len(text.splitlines()) >= 500:
        findings.append(
            {
                "severity": "warning",
                "code": "BODY_LARGE",
                "message": "SKILL.md is 500 lines or more",
            }
        )

    for path in skill_dir.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(skill_dir)
        content = (
            path.read_text(encoding="utf-8", errors="ignore")
            if path.suffix.lower() in {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
            else ""
        )
        if SECRET_RE.search(content):
            findings.append(
                {
                    "severity": "error",
                    "code": "SECRET_SHAPED_CONTENT",
                    "message": f"secret-shaped content in {rel}",
                }
            )
        if ABSOLUTE_PERSONAL_RE.search(content):
            findings.append(
                {
                    "severity": "warning",
                    "code": "PERSONAL_ABSOLUTE_PATH",
                    "message": f"personal absolute path in {rel}",
                }
            )
        parts = rel.parts
        if parts and parts[0] == "references" and len(parts) > 2:
            findings.append(
                {
                    "severity": "warning",
                    "code": "DEEP_REFERENCE",
                    "message": f"reference nesting exceeds one level: {rel}",
                }
            )

    return findings


def resolve_inside(root: Path, raw: str) -> tuple[bool, Path]:
    if not isinstance(raw, str) or not raw.startswith("./"):
        return False, root
    candidate = (root / raw[2:]).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return False, candidate
    return True, candidate


def check_openai_plugin(plugin_root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    manifest_dir = plugin_root / ".codex-plugin"
    manifest = manifest_dir / "plugin.json"
    if not manifest.is_file():
        return [
            {
                "severity": "error",
                "code": "OPENAI_MANIFEST_MISSING",
                "message": ".codex-plugin/plugin.json is missing",
            }
        ]

    extras = [p.name for p in manifest_dir.iterdir() if p.name != "plugin.json"]
    if extras:
        findings.append(
            {
                "severity": "error",
                "code": "OPENAI_MANIFEST_DIR_EXTRA",
                "message": f"only plugin.json may be in .codex-plugin/: {extras}",
            }
        )

    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        return [
            {
                "severity": "error",
                "code": "OPENAI_MANIFEST_JSON",
                "message": f"invalid plugin.json: {exc}",
            }
        ]

    for key in ("name", "version", "description"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            findings.append(
                {
                    "severity": "error",
                    "code": f"OPENAI_{key.upper()}_MISSING",
                    "message": f"plugin.json {key} is required",
                }
            )

    skills = data.get("skills")
    ok, path = (
        resolve_inside(plugin_root, skills) if skills is not None else (False, plugin_root)
    )
    if not ok or not path.is_dir():
        findings.append(
            {
                "severity": "error",
                "code": "OPENAI_SKILLS_PATH",
                "message": "skills must be a package-relative existing directory",
            }
        )

    interface = data.get("interface", {})
    if interface and not isinstance(interface, dict):
        findings.append(
            {
                "severity": "error",
                "code": "OPENAI_INTERFACE_TYPE",
                "message": "interface must be an object",
            }
        )
        interface = {}
    for field in ("composerIcon", "logo"):
        if field in interface:
            ok, path = resolve_inside(plugin_root, interface[field])
            if not ok or not path.is_file():
                findings.append(
                    {
                        "severity": "error",
                        "code": f"OPENAI_{field.upper()}_PATH",
                        "message": f"{field} path does not resolve inside plugin",
                    }
                )

    for prompt in (
        interface.get("defaultPrompt", [])
        if isinstance(interface.get("defaultPrompt", []), list)
        else []
    ):
        if not isinstance(prompt, str) or len(prompt) > 128:
            findings.append(
                {
                    "severity": "error",
                    "code": "OPENAI_DEFAULT_PROMPT",
                    "message": "each defaultPrompt must be a string of at most 128 characters",
                }
            )

    return findings


def check_claude_plugin(plugin_root: Path) -> list[dict[str, Any]]:
    manifest = plugin_root / ".claude-plugin" / "plugin.json"
    if not manifest.is_file():
        return [
            {
                "severity": "warning",
                "code": "CLAUDE_MANIFEST_MISSING",
                "message": ".claude-plugin/plugin.json is missing",
            }
        ]
    try:
        json.loads(manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        return [
            {
                "severity": "error",
                "code": "CLAUDE_MANIFEST_JSON",
                "message": f"invalid Claude plugin.json: {exc}",
            }
        ]
    return []


def check_antigravity_plugin(plugin_root: Path) -> list[dict[str, Any]]:
    manifest = plugin_root / ".agents" / "plugins" / "marketplace.json"
    if not manifest.is_file():
        return [
            {
                "severity": "warning",
                "code": "ANTIGRAVITY_MANIFEST_MISSING",
                "message": ".agents/plugins/marketplace.json is missing",
            }
        ]
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if "plugins" not in data or not isinstance(data["plugins"], list):
            return [
                {
                    "severity": "error",
                    "code": "ANTIGRAVITY_PLUGINS_ARRAY",
                    "message": "marketplace.json must define a 'plugins' array",
                }
            ]
    except Exception as exc:
        return [
            {
                "severity": "error",
                "code": "ANTIGRAVITY_MANIFEST_JSON",
                "message": f"invalid marketplace.json: {exc}",
            }
        ]
    return []


def validate_all(
    skill_dir: Path, targets: list[str], plugin_root: Path | None = None
) -> dict[str, Any]:
    """Validate skill directory against one or multiple host targets."""
    for t in targets:
        if t not in KNOWN_TARGETS and not t.startswith("custom:"):
            raise ValueError(f"Unknown target: {t}")

    findings = check_skill(skill_dir)

    if plugin_root:
        if "chatgpt" in targets or "codex" in targets:
            findings.extend(check_openai_plugin(plugin_root))
        if "claude-code" in targets:
            findings.extend(check_claude_plugin(plugin_root))
        if "antigravity" in targets:
            findings.extend(check_antigravity_plugin(plugin_root))

    errors = sum(1 for item in findings if item["severity"] == "error")
    warnings = sum(1 for item in findings if item["severity"] == "warning")
    return {
        "skill": str(skill_dir),
        "targets": targets,
        "errors": errors,
        "warnings": warnings,
        "findings": findings,
        "pass": errors == 0,
    }
