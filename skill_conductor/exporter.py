"""Host Adapter Exporter for Skill Conductor."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from .constants import AGENT_CONFIG_MAP, KNOWN_TARGETS, VERSION


def export_for_claude_code(repo_root: Path, output_dir: Path) -> dict[str, Any]:
    """Export Claude Code plugin bundle."""
    target = output_dir / "claude-code"
    target.mkdir(parents=True, exist_ok=True)
    manifest_dir = target / ".claude-plugin"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    source_manifest = repo_root / ".claude-plugin" / "plugin.json"
    if source_manifest.is_file():
        shutil.copy2(source_manifest, manifest_dir / "plugin.json")
    else:
        manifest = {
            "name": "skill-conductor",
            "version": VERSION,
            "description": "Design, evaluate, port, and package reliable agent skills.",
            "author": {"name": "Mamdouh Aboammar"},
            "license": "MIT",
        }
        (manifest_dir / "plugin.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )

    # Copy skills
    skills_src = repo_root / "skills"
    if skills_src.is_dir():
        skills_dst = target / "skills"
        if skills_dst.exists():
            shutil.rmtree(skills_dst)
        shutil.copytree(skills_src, skills_dst)

    return {"target": "claude-code", "output": str(target), "status": "success"}


def export_for_codex(repo_root: Path, output_dir: Path) -> dict[str, Any]:
    """Export OpenAI Codex / ChatGPT plugin bundle."""
    target = output_dir / "codex"
    target.mkdir(parents=True, exist_ok=True)
    manifest_dir = target / ".codex-plugin"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    source_manifest = repo_root / ".codex-plugin" / "plugin.json"
    if source_manifest.is_file():
        shutil.copy2(source_manifest, manifest_dir / "plugin.json")

    skills_src = repo_root / "skills"
    if skills_src.is_dir():
        skills_dst = target / "skills"
        if skills_dst.exists():
            shutil.rmtree(skills_dst)
        shutil.copytree(skills_src, skills_dst)

    assets_src = repo_root / "assets"
    if assets_src.is_dir():
        assets_dst = target / "assets"
        if assets_dst.exists():
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst)

    return {"target": "codex", "output": str(target), "status": "success"}


def export_for_antigravity(repo_root: Path, output_dir: Path) -> dict[str, Any]:
    """Export Google Antigravity & Agent Kernel bundle."""
    target = output_dir / "antigravity"
    target.mkdir(parents=True, exist_ok=True)
    agents_dir = target / ".agents"
    agents_dir.mkdir(parents=True, exist_ok=True)

    source_market = repo_root / ".agents" / "plugins" / "marketplace.json"
    if source_market.is_file():
        market_dir = agents_dir / "plugins"
        market_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_market, market_dir / "marketplace.json")

    skills_src = repo_root / "skills"
    if skills_src.is_dir():
        skills_dst = agents_dir / "skills"
        if skills_dst.exists():
            shutil.rmtree(skills_dst)
        shutil.copytree(skills_src, skills_dst)

    return {"target": "antigravity", "output": str(target), "status": "success"}


def export_for_editor(
    repo_root: Path, output_dir: Path, editor_name: str
) -> dict[str, Any]:
    """Export for Cursor, Windsurf, OpenCode, or DSH."""
    target = output_dir / editor_name
    target.mkdir(parents=True, exist_ok=True)
    target_skills = target / f".{editor_name}" / "skills"
    target_skills.parent.mkdir(parents=True, exist_ok=True)

    skills_src = repo_root / "skills"
    if skills_src.is_dir():
        if target_skills.exists():
            shutil.rmtree(target_skills)
        shutil.copytree(skills_src, target_skills)

    return {"target": editor_name, "output": str(target), "status": "success"}


def export_adapters(
    repo_root: Path | str, output_dir: Path | str, targets: list[str] | None = None
) -> list[dict[str, Any]]:
    root = Path(repo_root).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    active_targets = targets or list(KNOWN_TARGETS)
    results = []

    for t in active_targets:
        if t == "claude-code":
            results.append(export_for_claude_code(root, out))
        elif t in {"codex", "chatgpt"}:
            results.append(export_for_codex(root, out))
        elif t == "antigravity":
            results.append(export_for_antigravity(root, out))
        elif t in {"cursor", "windsurf", "opencode", "dsh"}:
            results.append(export_for_editor(root, out, t))
        elif t in {"agent-skills", "skills-sh"}:
            # Standard folder structure
            target = out / t / "skills"
            target.parent.mkdir(parents=True, exist_ok=True)
            skills_src = root / "skills"
            if skills_src.is_dir():
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(skills_src, target)
            results.append({"target": t, "output": str(target.parent), "status": "success"})

    return results
