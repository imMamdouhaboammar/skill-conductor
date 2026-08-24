"""Cross-agent installation manager for Skill Conductor."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from .constants import AGENT_CONFIG_MAP, KNOWN_TARGETS


def detect_installed_agents(workspace_root: Path | None = None) -> dict[str, bool]:
    """Detect which agent environments exist locally in project or user home."""
    root = workspace_root or Path.cwd()
    home = Path.home()

    detected = {}
    for agent, config in AGENT_CONFIG_MAP.items():
        local_path = root / config["target_dir"]
        expanded_global = Path(os.path.expanduser(config["global_dir"]))
        detected[agent] = local_path.exists() or expanded_global.exists()
    return detected


def install_to_agent(
    skill_or_repo_path: Path | str,
    agent: str,
    workspace_root: Path | None = None,
    is_global: bool = False,
) -> dict[str, Any]:
    """Install skills to a specific agent runtime."""
    if agent not in AGENT_CONFIG_MAP and agent != "all":
        raise ValueError(
            f"Unsupported agent: {agent}. Supported: {', '.join(sorted(AGENT_CONFIG_MAP.keys()))}"
        )

    src = Path(skill_or_repo_path).resolve()
    root = workspace_root or Path.cwd()
    home = Path.home()

    if agent == "all":
        results = []
        for a in sorted(AGENT_CONFIG_MAP.keys()):
            if a in {"agent-skills", "skills-sh"}:
                continue
            results.append(install_to_agent(src, a, root, is_global))
        return {"agent": "all", "results": results}

    config = AGENT_CONFIG_MAP[agent]
    target_base = (
        Path(os.path.expanduser(config["global_dir"]))
        if is_global
        else root / config["target_dir"]
    )
    target_base.mkdir(parents=True, exist_ok=True)

    # Determine if source is single skill or repository root
    if (src / "SKILL.md").is_file():
        # Single skill directory
        skill_name = src.name
        dest = target_base / skill_name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        installed = [skill_name]
    elif (src / "skills").is_dir():
        # Multi-skill repo
        installed = []
        for skill_dir in (src / "skills").iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file():
                dest = target_base / skill_dir.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(skill_dir, dest)
                installed.append(skill_dir.name)
    else:
        raise ValueError(f"Source {src} does not contain SKILL.md or skills/ directory")

    return {
        "agent": agent,
        "agent_name": config["name"],
        "target_path": str(target_base),
        "is_global": is_global,
        "installed_skills": installed,
        "count": len(installed),
        "status": "installed",
    }
