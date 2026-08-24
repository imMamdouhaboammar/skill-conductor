---
name: host-workspace-operator
description: Use when a Skill Conductor workflow needs to inspect, search, modify, or verify files in the host workspace using the safest native capabilities available.
---

# Host Workspace Operator

Use workspace capabilities supplied by the current host instead of pretending the plugin owns a filesystem API.

Prefer the narrowest operation that can answer the task:

1. `read` for a known file or range
2. `list` for directory/workspace shape
3. `search` for broad or semantic discovery
4. `grep` for exact text, regex, symbols, or fields
5. `patch` for focused edits
6. `write` for authorized creation/replacement
7. `shell` for repository commands when narrower operations are insufficient
8. `python` for deterministic parsing, generation, hashing, archive checks, or validation

Read-only discovery comes before mutation.

Before changing workspace state:

- confirm the request authorizes the change
- inspect repository instructions and relevant source
- preserve unrelated work
- prefer focused patches to broad rewrites
- never write secrets into source, manifests, examples, logs, or packages

After mutation:

- read back the changed area when practical
- run the relevant verifier/test when available
- report files changed and execution evidence

If a capability is unavailable, do not invent a replacement tool name or claim the operation occurred.

This skill does not grant filesystem permissions. It maps workflow intent to host-native capabilities when present.
