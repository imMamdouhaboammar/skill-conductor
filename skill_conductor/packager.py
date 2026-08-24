"""Packaging engine for Skill Conductor."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

from .validator import check_skill

EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git", ".idea", ".vscode"}
EXCLUDE_GLOBS = {"*.pyc", "*.pyo", "*.swp", "*.DS_Store"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}
ROOT_EXCLUDE_DIRS = {"evals"}


def should_exclude(rel_path: Path) -> bool:
    """Check if a relative path should be excluded from packaging."""
    parts = rel_path.parts
    if any(part in EXCLUDE_DIRS for part in parts):
        return True
    if len(parts) > 1 and parts[1] in ROOT_EXCLUDE_DIRS:
        return True
    name = rel_path.name
    if name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in EXCLUDE_GLOBS)


def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 checksum of a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def package_skill(
    skill_path: Path | str, output_dir: Path | str | None = None
) -> dict[str, Any]:
    """Package a skill into a distributable .skill archive."""
    skill_path = Path(skill_path).resolve()
    if not skill_path.is_dir():
        raise FileNotFoundError(f"Skill directory not found: {skill_path}")

    # Validate first
    findings = check_skill(skill_path)
    errors = [f for f in findings if f["severity"] == "error"]
    if errors:
        raise ValueError(
            f"Cannot package invalid skill ({len(errors)} error(s)): {errors[0]['message']}"
        )

    out = Path(output_dir).resolve() if output_dir else Path.cwd()
    out.mkdir(parents=True, exist_ok=True)

    skill_name = skill_path.name
    archive_path = out / f"{skill_name}.skill"

    files_added = []
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in sorted(skill_path.rglob("*")):
            if not file_path.is_file():
                continue
            arcname = file_path.relative_to(skill_path.parent)
            if should_exclude(arcname):
                continue
            zipf.write(file_path, arcname)
            files_added.append(str(arcname))

    sha256 = compute_sha256(archive_path)
    size_bytes = archive_path.stat().st_size

    # Write metadata sidecar
    meta_path = out / f"{skill_name}.json"
    metadata = {
        "name": skill_name,
        "archive": archive_path.name,
        "sha256": sha256,
        "size_bytes": size_bytes,
        "files_count": len(files_added),
        "files": files_added,
    }
    meta_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    return {
        "path": str(archive_path),
        "name": skill_name,
        "sha256": sha256,
        "size_bytes": size_bytes,
        "files": files_added,
        "metadata_path": str(meta_path),
    }


def package_all_skills(
    skills_root: Path | str, output_dir: Path | str
) -> list[dict[str, Any]]:
    """Package all immediate skill subdirectories in a root folder."""
    root = Path(skills_root).resolve()
    out = Path(output_dir).resolve()
    results = []
    for entry in sorted(root.iterdir()):
        if entry.is_dir() and (entry / "SKILL.md").is_file():
            results.append(package_skill(entry, out))
    return results
