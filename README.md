<p align="center">
  <img src="assets/conductor.png" alt="Skill Conductor" width="100%">
</p>

# Skill Conductor

> Design the behavior first. Write the Skill second. Prove it works before you ship it.

Skill Conductor is a cross-host Skill engineering toolkit and plugin for ChatGPT, Codex, Claude Code, Agent Skills, and compatible agent hosts.

It turns vague requests like *"teach my agent to do this consistently"* into defined behavioral contracts, deliberate Skill architectures, comprehensive evaluation banks, regression gates, and portable packages.

The core lifecycle is:

$$\text{need} \longrightarrow \text{contract} \longrightarrow \text{architecture} \longrightarrow \text{baseline} \longrightarrow \text{build} \longrightarrow \text{evaluate} \longrightarrow \text{improve} \longrightarrow \text{port} \longrightarrow \text{package}$$

---

## What Changed in v4

Earlier Conductor releases established a strong architecture-first and eval-first methodology, but parts of the workflow assumed vendor-specific runtimes or Anthropic execution keys as universal requirements.

**v4 cleanly separates:**

1. **Portable Skill Behavior**
   - User job & intent boundary
   - Positive, implicit, and negative triggers
   - Decision points and gates
   - Evidence requirements & mutation boundaries
   - Freedom level calibration (high/medium/low)
   - Evaluation contract & held-out test banks

2. **Host Adapters**
   - Installation layout
   - Manifest format (`.codex-plugin`, `.claude-plugin`, `.agents`)
   - Tool & capability bindings
   - Runtime-specific execution details
   - Packaging mechanics

Design once, then adapt honestly for ChatGPT, Codex, Claude Code, or any Agent Skills-compatible host.

---

## Skills Suite

| Skill | Description |
|---|---|
| [`skill-conductor`](skills/skill-conductor) | Primary orchestrator and full lifecycle router (`CREATE`, `IMPROVE`, `VALIDATE`, `REVIEW`, `OPTIMIZE`, `PORT`, `PACKAGE`). |
| [`skill-architect`](skills/skill-architect) | Architecture-first creation, SOP/workflow-to-Skill compilation, and freedom calibration. |
| [`skill-evaluator`](skills/skill-evaluator) | Activation testing, behavioral assertions, pressure testing, and held-out regression control. |
| [`skill-portability-compiler`](skills/skill-portability-compiler) | Compiles host-neutral SkillSpecs into target host adapters with explicit capability gap reports. |
| [`host-workspace-operator`](skills/host-workspace-operator) | Safely binds workflow intent to host-native workspace capabilities (read, search, patch, write, shell). |
| [`sandbox-python-executor`](skills/sandbox-python-executor) | Deterministic Python helper for parsing, hash verification, archive inspection, and validation. |

---

## Universal Skill Contract

Before authoring, Skill Conductor freezes ten core contracts:

1. **Identity**: Name, single job, target user.
2. **Activation**: Positive, implicit, and close negative prompts + collision set.
3. **Behavior**: Preconditions, decision logic, completion conditions.
4. **Knowledge**: Domain facts, references separation.
5. **Freedom**: High (judgment) vs. Medium (pseudocode) vs. Low (scripts/schemas).
6. **Capabilities**: Required vs. optional host capabilities.
7. **Evidence**: Grounding rules before consequential actions.
8. **Evaluation**: BinEval assertions, held-out splits, pressure tests.
9. **Portability**: Explicit compatibility matrices per host.
10. **Release**: Verification gates before packaging.

---

## Core Modes

### 1. CREATE
Prove the Skill should exist, freeze the contract, select architectural patterns, draft the minimal candidate, and produce the evaluation blueprint.

### 2. IMPROVE
Diagnose failure classes, apply minimal targeted patches, and verify against held-out regression cases.

### 3. VALIDATE
Run multi-gate verification: structural checks, manifest schemas, portability audits, and behavioral evals.

### 4. REVIEW
Audit third-party Skills for trigger collisions, overbroad activation, brittle rules, unsafe mutations, or fake test claims.

### 5. OPTIMIZE
Calibrate descriptions for optimal activation recall and precision using held-out prompt sets.

### 6. PORT
Compile portable SkillSpecs into target host adapters (ChatGPT, Codex, Claude Code, Agent Skills) and generate gap matrices.

### 7. PACKAGE
Package distributable `.skill` zip archives or multi-agent plugin bundles with validated manifests.

---

## Quickstart & Verification

Run local test suites:

```bash
# Run unit & smoke tests
python3 skills/skill-conductor/scripts/test_smoke.py

# Run portability test suite
python3 skills/skill-conductor/scripts/test_portability.py

# Validate Skill Conductor against all target hosts
python3 skills/skill-conductor/scripts/validate_portability.py skills/skill-conductor --targets agent-skills,chatgpt,codex,claude-code --plugin-root .
```

---

## License & Attribution

Distributed under the [MIT License](LICENSE). See [PRIVACY.md](PRIVACY.md), [TERMS.md](TERMS.md), and [SUPPORT.md](SUPPORT.md).
