<p align="center">
  <img src="assets/conductor.png" alt="Skill Conductor" width="100%">
</p>

# Skill Conductor

> Design the behavior first. Write the Skill second. Prove it works before you ship it.

Skill Conductor is a universal cross-host Skill engineering toolkit and plugin for **Claude Code, OpenAI Codex, ChatGPT, Google Antigravity, Cursor, Windsurf, OpenCode, DSH, and Skills.sh**.

It turns vague requests like *"teach my agent to do this consistently"* into defined behavioral contracts, deliberate Skill architectures, comprehensive evaluation banks, regression gates, and portable packages.

---

## ⚡ Quick Installation & Distribution

Install Skill Conductor via your preferred package manager or shell:

```bash
# 🍺 Homebrew (macOS & Linux)
brew install imMamdouhaboammar/tap/skill-conductor

# 🥟 Bun / npm (Global CLI)
bun install -g skill-conductor
# or
npm install -g skill-conductor

# 🌐 One-line POSIX curl installer (macOS & Linux)
curl -fsSL https://raw.githubusercontent.com/imMamdouhaboammar/skill-conductor/main/install.sh | sh

# 📦 Skills.sh Registry CLI
npx skills add imMamdouhaboammar/skill-conductor

# 🐍 PyPI / pip
pip install skill-conductor

# 🪟 Windows PowerShell
iex (irm https://raw.githubusercontent.com/imMamdouhaboammar/skill-conductor/main/install.ps1)
```

---

## 🤖 Multi-Agent Ecosystem Support

Skill Conductor includes built-in adapters and automatic installation routines for all modern AI agent hosts:

```bash
# Check detected agent environments on your system
skill-conductor doctor

# Install the entire skill suite to all detected agents
skill-conductor install --agent all

# Or install to a specific agent target:
skill-conductor install --agent claude-code   # Anthropic Claude Code & Claude Desktop
skill-conductor install --agent codex         # OpenAI Codex & ChatGPT Plugins
skill-conductor install --agent antigravity   # Google Antigravity & Agent Kernel
skill-conductor install --agent cursor        # Cursor IDE Agent (.cursor/skills)
skill-conductor install --agent windsurf      # Codeium Windsurf Cascade (.windsurf/skills)
skill-conductor install --agent opencode      # OpenCode CLI & Agents (.opencode/skills)
skill-conductor install --agent dsh           # DeepSeek Harness & MasterOne (.dsh/skills)
```

---

## 🌐 Skills.sh via Vercel Deployment

Deploy your own live Skills.sh registry and interactive web catalog to Vercel in seconds:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FimMamdouhaboammar%2Fskill-conductor)

```bash
# Deploy directly from CLI
vercel --prod
```

### Registry Endpoints:
- `GET /` — Interactive dark-mode Skills.sh Web Catalog & Documentation.
- `GET /api/skills` — Full JSON metadata catalog for all skills.
- `GET /api/skills/<name>` — Detailed skill documentation, markdown body, and evals.
- `GET /api/v1/package/<name>` — Direct `.skill` binary zip download.
- `GET /skills.json` & `GET /registry.json` — Standard Skills.sh discovery manifests.
- `GET /install.sh` — Direct raw installer script served from edge.

---

## 🛠️ Skills Suite

| Skill | Description |
|---|---|
| [`skill-conductor`](skills/skill-conductor) | Primary orchestrator and full lifecycle router (`CREATE`, `IMPROVE`, `VALIDATE`, `REVIEW`, `OPTIMIZE`, `PORT`, `PACKAGE`). |
| [`skill-architect`](skills/skill-architect) | Architecture-first creation, SOP/workflow-to-Skill compilation, and freedom calibration. |
| [`skill-evaluator`](skills/skill-evaluator) | Activation testing, behavioral assertions, pressure testing, and held-out regression control. |
| [`skill-portability-compiler`](skills/skill-portability-compiler) | Compiles host-neutral SkillSpecs into target host adapters with explicit capability gap reports. |
| [`host-workspace-operator`](skills/host-workspace-operator) | Safely binds workflow intent to host-native workspace capabilities (read, search, patch, write, shell). |
| [`sandbox-python-executor`](skills/sandbox-python-executor) | Deterministic Python helper for parsing, hash verification, archive inspection, and validation. |

---

## 🚀 CLI Commands

```bash
# List all skills in the suite with evaluation status
skill-conductor list

# Validate a skill against all 10 agent host targets
skill-conductor validate skills/skill-conductor

# Package skills into .skill distributable archives with SHA256 sidecars
skill-conductor package skills --out dist

# Export host adapter packages (Claude, Codex, Antigravity, Cursor, etc.)
skill-conductor export --out dist/adapters

# Compile a SkillSpec JSON into a full skill directory
skill-conductor compile --spec path/to/spec.json --out skills/
```

---

## 🧪 Verification & Testing

Run all local verification suites:

```bash
# Smoke tests
python3 skills/skill-conductor/scripts/test_smoke.py

# Portability test suite
python3 skills/skill-conductor/scripts/test_portability.py

# Multi-target static validation across all 10 host targets
python3 skills/skill-conductor/scripts/validate_portability.py skills/skill-conductor \
  --targets agent-skills,chatgpt,codex,claude-code,antigravity,cursor,windsurf,opencode,skills-sh,dsh \
  --plugin-root .
```

---

## License & Attribution

Distributed under the [MIT License](LICENSE). See [PRIVACY.md](PRIVACY.md), [TERMS.md](TERMS.md), and [SUPPORT.md](SUPPORT.md).
