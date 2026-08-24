# Host Adapters

Keep the Skill's behavioral core host-neutral. Add an adapter only when a host changes loading, installation, tool naming, packaging, or execution semantics.

## Capability Profile

Build this table for every claimed host:

| Capability | Required by Skill | Host provides | Adapter needed | Fallback |
|---|---:|---:|---:|---|
| instruction loading | yes/no | yes/no/unknown | yes/no | behavior |
| supporting references | yes/no | yes/no/unknown | yes/no | behavior |
| bundled scripts | yes/no | yes/no/unknown | yes/no | behavior |
| filesystem read | yes/no | yes/no/unknown | yes/no | behavior |
| filesystem mutation | yes/no | yes/no/unknown | yes/no | behavior |
| command execution | yes/no | yes/no/unknown | yes/no | behavior |
| deterministic computation | yes/no | yes/no/unknown | yes/no | behavior |
| web research | yes/no | yes/no/unknown | yes/no | behavior |
| connected private data | yes/no | yes/no/unknown | yes/no | behavior |
| external actions | yes/no | yes/no/unknown | yes/no | behavior |

Do not mark unknown capabilities as supported.

## 1. OpenAI Skills Adapter (Codex & ChatGPT)

OpenAI Skills follow the Agent Skills open standard and can be used in ChatGPT, Codex, and the OpenAI API.
- Manifest: `.codex-plugin/plugin.json` at plugin root.
- Skill location: `skills/<skill-name>/SKILL.md`.
- Tool mapping: OpenAI function calling / native workspace tools.

## 2. Claude-Compatible Adapter (Claude Code & Claude Desktop)

- Manifest: `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
- Skill location: `skills/<skill-name>/SKILL.md`.
- Tool mapping: Claude Code Read/Write/Grep/Bash tools.
- Evaluator note: Do not require Anthropic API keys for basic validation; treat LLM eval as an optional evaluator path.

## 3. Google Antigravity & Agent Kernel Adapter

- Manifest: `.agents/plugins/marketplace.json`.
- Skill location: `.agents/skills/<skill-name>/` or `~/.gemini/antigravity/builtin/skills/`.
- Tool mapping: Antigravity tool calling engine (`view_file`, `write_to_file`, `replace_file_content`, `run_command`, `invoke_subagent`).
- Full compatibility with the shared Agent Kernel constitution.

## 4. Cursor IDE Adapter

- Skill location: `.cursor/skills/<skill-name>/` or `.cursorrules`.
- Installation: `skill-conductor install --agent cursor`.

## 5. Codeium Windsurf Adapter

- Skill location: `.windsurf/skills/<skill-name>/` or `~/.codeium/windsurf/skills/`.
- Installation: `skill-conductor install --agent windsurf`.

## 6. OpenCode CLI Adapter

- Skill location: `.opencode/skills/<skill-name>/` or `.agents/skills/`.
- Installation: `skill-conductor install --agent opencode`.

## 7. DeepSeek Harness (DSH) / MasterOne Adapter

- Skill location: `.dsh/skills/<skill-name>/`.
- Compatible with custom LLM provider orchestration and fast inference runners.

## 8. Skills.sh Universal Registry Adapter (Vercel)

- Manifest: `skills.json` and `registry.json`.
- Distribution: Direct `.skill` zip downloads via Vercel Edge Serverless functions (`/api/v1/package/:name`).
- CLI integration: `npx skills add imMamdouhaboammar/skill-conductor` or `bunx skills add ...`.

---

## Adapter Quality Rules

Reject an adapter when it:
- copies the entire portable core instead of referencing it
- changes the user job
- silently removes gates or evidence requirements
- claims a host capability without evidence
- embeds user-specific absolute paths
- requires credentials unrelated to the Skill's actual job
- reports untested compatibility as tested support

## Portability Status

Use one status per host:
- `SUPPORTED_TESTED`
- `SUPPORTED_STRUCTURAL_ONLY`
- `ADAPTER_REQUIRED`
- `UNSUPPORTED`
- `UNKNOWN`
