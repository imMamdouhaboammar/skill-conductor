"""Constants and configurations for Skill Conductor."""

from __future__ import annotations

import re

VERSION = "4.0.0"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET_RE = re.compile(
    r"(sk-[A-Za-z0-9_-]{16,}|ANTHROPIC_API_KEY\s*=|OPENAI_API_KEY\s*=|BEGIN (?:RSA |EC )?PRIVATE KEY)"
)
ABSOLUTE_PERSONAL_RE = re.compile(
    r"(/(?:Users|home)/[^\s/]+|[A-Za-z]:[/\\]+(?:Users|home)[/\\]+[^\s/\\]+)"
)
PROCESS_HINT_RE = re.compile(
    r"\b(first|then|next|finally|step\s+\d+|after that|before you)\b", re.I
)

KNOWN_TARGETS = {
    "agent-skills",
    "chatgpt",
    "codex",
    "claude-code",
    "antigravity",
    "cursor",
    "windsurf",
    "opencode",
    "skills-sh",
    "dsh",
}

KNOWN_HOSTS = KNOWN_TARGETS

AGENT_CONFIG_MAP = {
    "claude-code": {
        "name": "Claude Code & Claude Desktop",
        "target_dir": ".claude-plugin",
        "global_dir": "~/.claude/plugins",
        "manifest": "plugin.json",
    },
    "codex": {
        "name": "OpenAI Codex & ChatGPT Plugins",
        "target_dir": ".codex-plugin",
        "global_dir": "~/.codex/plugins",
        "manifest": "plugin.json",
    },
    "chatgpt": {
        "name": "OpenAI ChatGPT Custom GPTs / Actions",
        "target_dir": ".codex-plugin",
        "global_dir": "~/.chatgpt/actions",
        "manifest": "plugin.json",
    },
    "antigravity": {
        "name": "Google Antigravity & Agent Kernel",
        "target_dir": ".agents/skills",
        "global_dir": "~/.gemini/antigravity/builtin/skills",
        "manifest": "marketplace.json",
    },
    "cursor": {
        "name": "Cursor IDE Agent",
        "target_dir": ".cursor/skills",
        "global_dir": "~/.cursor/skills",
        "manifest": None,
    },
    "windsurf": {
        "name": "Codeium Windsurf Cascade",
        "target_dir": ".windsurf/skills",
        "global_dir": "~/.codeium/windsurf/skills",
        "manifest": None,
    },
    "opencode": {
        "name": "OpenCode CLI & Agents",
        "target_dir": ".opencode/skills",
        "global_dir": "~/.opencode/skills",
        "manifest": None,
    },
    "dsh": {
        "name": "DeepSeek Harness / MasterOne Agent",
        "target_dir": ".dsh/skills",
        "global_dir": "~/.dsh/skills",
        "manifest": None,
    },
    "skills-sh": {
        "name": "Skills.sh Universal Catalog",
        "target_dir": "skills",
        "global_dir": "~/.skills",
        "manifest": "skills.json",
    },
}
