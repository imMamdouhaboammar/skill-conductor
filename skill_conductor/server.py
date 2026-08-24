"""Skills.sh Registry and Catalog Server for Skill Conductor."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .constants import VERSION
from .validator import parse_frontmatter


def get_skills_catalog(repo_root: Path | str | None = None) -> list[dict[str, Any]]:
    """Scan skills/ directory and build full catalog metadata."""
    root = (
        Path(repo_root).resolve()
        if repo_root
        else Path(__file__).resolve().parent.parent
    )
    skills_dir = root / "skills"

    catalog: list[dict[str, Any]] = []
    if not skills_dir.is_dir():
        return catalog

    for skill_path in sorted(skills_dir.iterdir()):
        if not skill_path.is_dir():
            continue
        skill_md = skill_path / "SKILL.md"
        if not skill_md.is_file():
            continue

        text = skill_md.read_text(encoding="utf-8", errors="replace")
        name, description = parse_frontmatter(text)

        # Check for evals
        evals_path = skill_path / "evals" / "evals.json"
        has_evals = evals_path.is_file()
        evals_count = 0
        if has_evals:
            try:
                evals_data = json.loads(evals_path.read_text(encoding="utf-8"))
                if isinstance(evals_data, list):
                    evals_count = len(evals_data)
            except Exception:
                pass

        # Check for references
        refs_dir = skill_path / "references"
        refs = [p.name for p in refs_dir.iterdir() if p.is_file()] if refs_dir.is_dir() else []

        # Check for scripts
        scripts_dir = skill_path / "scripts"
        scripts = [p.name for p in scripts_dir.iterdir() if p.is_file()] if scripts_dir.is_dir() else []

        catalog.append(
            {
                "name": name or skill_path.name,
                "version": VERSION,
                "description": description or "",
                "path": str(skill_path.relative_to(root)),
                "has_evals": has_evals,
                "evals_count": evals_count,
                "references": refs,
                "scripts": scripts,
                "supported_hosts": [
                    "claude-code",
                    "codex",
                    "chatgpt",
                    "antigravity",
                    "cursor",
                    "windsurf",
                    "opencode",
                    "skills-sh",
                    "dsh",
                ],
                "author": "Mamdouh Aboammar",
                "license": "MIT",
                "repository": "https://github.com/imMamdouhaboammar/skill-conductor",
            }
        )

    return catalog


def get_skill_detail(skill_name: str, repo_root: Path | str | None = None) -> dict[str, Any] | None:
    """Retrieve full details of a specific skill including SKILL.md body and evals."""
    root = (
        Path(repo_root).resolve()
        if repo_root
        else Path(__file__).resolve().parent.parent
    )
    skill_path = root / "skills" / skill_name
    skill_md = skill_path / "SKILL.md"
    if not skill_md.is_file():
        return None

    raw_text = skill_md.read_text(encoding="utf-8", errors="replace")
    name, description = parse_frontmatter(raw_text)

    evals = []
    evals_path = skill_path / "evals" / "evals.json"
    if evals_path.is_file():
        try:
            evals = json.loads(evals_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    return {
        "name": name or skill_name,
        "version": VERSION,
        "description": description or "",
        "content": raw_text,
        "evals": evals,
        "supported_hosts": [
            "claude-code",
            "codex",
            "chatgpt",
            "antigravity",
            "cursor",
            "windsurf",
            "opencode",
            "skills-sh",
            "dsh",
        ],
        "author": "Mamdouh Aboammar",
        "license": "MIT",
    }
