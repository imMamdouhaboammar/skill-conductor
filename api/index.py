"""Vercel Serverless Function implementing the Skills.sh registry API and catalog."""

from __future__ import annotations

import io
import json
import mimetypes
import sys
import urllib.parse
import zipfile
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Add project root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from skill_conductor.packager import should_exclude
from skill_conductor.server import get_skill_detail, get_skills_catalog


class handler(BaseHTTPRequestHandler):
    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization, X-Agent-Target",
        )

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_HEAD(self) -> None:
        self.do_GET(is_head=True)

    def do_GET(self, is_head: bool = False) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Check for query parameters (used by Vercel routes)
        package_param = query.get("package", [None])[0]
        skill_param = query.get("skill", [None])[0]

        # 0. Static assets and Landing Page
        if path in {"", "/", "/index.html"}:
            html_file = REPO_ROOT / "public" / "index.html"
            if html_file.is_file():
                content = html_file.read_bytes()
                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                if not is_head:
                    self.wfile.write(content)
                return

        if path.startswith("/public/") or path.startswith("/assets/"):
            rel = path.lstrip("/")
            file_path = REPO_ROOT / rel
            if not file_path.is_file():
                file_path = REPO_ROOT / "public" / rel.replace("public/", "")
            if file_path.is_file():
                content = file_path.read_bytes()
                mime, _ = mimetypes.guess_type(str(file_path))
                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", mime or "application/octet-stream")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                if not is_head:
                    self.wfile.write(content)
                return

        if path in {"/install.sh", "/install.ps1"}:
            script_file = REPO_ROOT / path.lstrip("/")
            if script_file.is_file():
                content = script_file.read_bytes()
                mime = "text/x-shellscript" if path.endswith(".sh") else "text/plain"
                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", f"{mime}; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                if not is_head:
                    self.wfile.write(content)
                return

        # 1. Package Download Endpoint
        if package_param or path.startswith("/api/v1/package/"):
            skill_name = package_param or path.split("/")[-1].replace(".skill", "")
            skill_dir = REPO_ROOT / "skills" / skill_name
            if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").is_file():
                self.send_response(404)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                if not is_head:
                    self.wfile.write(
                        json.dumps(
                            {"error": "Skill not found", "skill": skill_name}
                        ).encode("utf-8")
                    )
                return

            # Build in-memory zip archive
            mem_buf = io.BytesIO()
            with zipfile.ZipFile(mem_buf, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in sorted(skill_dir.rglob("*")):
                    if not file_path.is_file():
                        continue
                    arcname = file_path.relative_to(skill_dir.parent)
                    if should_exclude(arcname):
                        continue
                    zipf.write(file_path, arcname)

            archive_data = mem_buf.getvalue()

            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/zip")
            self.send_header(
                "Content-Disposition", f'attachment; filename="{skill_name}.skill"'
            )
            self.send_header("Content-Length", str(len(archive_data)))
            self.end_headers()
            if not is_head:
                self.wfile.write(archive_data)
            return

        # 2. Individual Skill Detail Endpoint
        if (
            skill_param
            or path.startswith("/api/v1/skills/")
            or (path.startswith("/api/skills/") and path != "/api/skills")
        ):
            skill_name = (
                skill_param
                or (
                    path.split("/api/v1/skills/")[-1]
                    if "/api/v1/skills/" in path
                    else path.split("/api/skills/")[-1]
                )
            ).strip("/")
            detail = get_skill_detail(skill_name, REPO_ROOT)
            if not detail:
                self.send_response(404)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                if not is_head:
                    self.wfile.write(
                        json.dumps(
                            {"error": "Skill not found", "skill": skill_name}
                        ).encode("utf-8")
                    )
                return

            resp_data = json.dumps(detail, indent=2).encode("utf-8")
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp_data)))
            self.end_headers()
            if not is_head:
                self.wfile.write(resp_data)
            return

        # 3. Catalog / Registry Index Endpoint (/api/skills or /api/registry or /skills.json)
        catalog = get_skills_catalog(REPO_ROOT)
        registry_meta = {
            "registry": "Skills.sh Universal Catalog",
            "provider": "Skill Conductor",
            "version": "4.0.0",
            "repository": "https://github.com/imMamdouhaboammar/skill-conductor",
            "total_skills": len(catalog),
            "skills": catalog,
        }
        resp_data = json.dumps(registry_meta, indent=2).encode("utf-8")
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp_data)))
        self.end_headers()
        if not is_head:
            self.wfile.write(resp_data)
