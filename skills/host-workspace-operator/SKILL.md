---
name: host-workspace-operator
description: Use when Skill Conductor needs to inspect, search, modify, or verify files in the active host workspace using the safest native capability available. Do NOT assume the Plugin itself grants filesystem, shell, search, patch, or Python access.
---

# Host Workspace Operator

Use capabilities supplied by the current host. Route by capability rather than a hard-coded vendor tool name

## Capability order

Prefer the narrowest operation that fits:

1. read a known file or range
2. list a directory or workspace scope
3. search broad concepts when wording or location is uncertain
4. grep or exact-match known terms, symbols, fields, or patterns
5. patch a focused existing section
6. write only when creation or replacement is authorized
7. shell for repository commands when narrower tools are insufficient
8. deterministic Python or equivalent computation for parsing, hashes, package inspection, or verification

Do not use shell or Python merely to imitate a safer read/search/file operation

## Read-only first

Before mutation:

- inspect repository instructions
- locate relevant files
- read enough context to preserve unrelated work
- distinguish source from generated/vendor files
- identify the smallest mutation that completes the request

## Mutation boundary

Treat write, patch, delete, move, rename, format, and mutating commands as state changes

Only mutate when the user requested or clearly authorized the change
Prefer a focused patch over a broad rewrite
Never write credentials or secrets into source, examples, manifests, logs, or artifacts

After mutation, read changed areas and run relevant checks when the host can execute them

## Evidence rule

Never say a file was read, searched, modified, tested, or executed unless the host produced evidence of that action

If the required capability is unavailable:

- do not invent a tool or manifest permission
- use another capability only if it preserves semantics and safety
- otherwise keep the dependent result unverified

This Skill teaches workspace behavior. It grants no permissions
