<p align="center">
  <img src="assets/conductor.png" alt="Skill Conductor" width="100%">
</p>

# Skill Conductor

> Design the behavior first. Write the Skill second. Prove it works before you ship it.

Skill Conductor is a cross-host Skill engineering toolkit for ChatGPT, Codex, Claude, API agents, and other compatible agent hosts

It turns a vague request like “teach my agent to do this consistently” into a defined behavioral contract, a deliberate Skill architecture, an evaluation bank, a regression gate, and a portable package

The core lifecycle is:

**need → contract → architecture → baseline → build → evaluate → improve → port → package**

## What changed in v4

Earlier Conductor releases built a strong architecture-first and eval-first methodology, but parts of the workflow assumed a Claude-specific runtime, Anthropic execution paths, and `uv` as if they were universal requirements

v4 separates two things that should never have been mixed:

1. **Portable Skill behavior**
   - user job
   - activation boundary
   - decisions
   - evidence gates
   - completion conditions
   - freedom level
   - eval contract

2. **Host adapter**
   - install layout
   - manifest format
   - tool names
   - hooks
   - runtime details
   - packaging mechanics

That means the same Skill can be designed once, then adapted honestly for ChatGPT, Codex, Claude, or another agent without copying the whole workflow into several drifting versions

## The Plugin

This repository now includes a Skills-only ChatGPT/Codex Plugin surface under `.codex-plugin/plugin.json`

Public Skills:

| Skill | Job |
|---|---|
| `skill-conductor` | Router and full lifecycle conductor |
| `skill-architect` | Design a new Skill or compile a workflow into one |
| `skill-evaluator` | Test activation, behavior, pressure resistance, and regressions |
| `skill-portability-compiler` | Separate portable behavior from host-specific adapters |
| `host-workspace-operator` | Use host-native workspace capabilities safely when present |

The Plugin does not need MCP for its core job and does not grant filesystem, shell, Python, or external-service access by itself

## Universal Skill Contract

Before authoring, Conductor freezes ten contracts:

1. Skill identity
2. activation
3. behavior
4. knowledge
5. freedom
6. tool capability
7. evidence
8. evaluation
9. portability
10. release

See `skills/skill-conductor/references/skill-contract.md`

This prevents the common failure where a polished `SKILL.md` hides an undefined job, broad triggering, missing failure behavior, or invented tool assumptions

## Core modes

### CREATE

Prove the Skill should exist, freeze the contract, choose architecture, write the smallest useful candidate, then build the eval bank

### IMPROVE

Diagnose the failure class, make small attributable edits, and accept them only when held-out behavior does not regress

### VALIDATE

Separate structural validity from behavioral validity. A tidy Skill that was never behaviorally tested is not “proven”

### REVIEW

Inspect third-party Skills for activation collisions, unclear decision logic, hidden dependencies, unnecessary context, unsafe mutation assumptions, and weak evidence

### OPTIMIZE

Improve activation text against positive and negative prompts without leaking the full workflow into the description

### PORT

Extract the portable core and create host adapters only for real host differences

### PACKAGE

Validate intended files, references, paths, and distribution boundaries before producing a package

## Architecture patterns

Choose the control pattern before prose:

- Sequential workflow
- Iterative refinement
- Context-aware selection
- Domain intelligence
- Multi-service coordination

Then set freedom per step:

- **Low** for fragile deterministic mechanics
- **Medium** for constrained decision procedures
- **High** where judgment is the actual value

## Evaluation philosophy

Conductor keeps the strongest ideas from earlier releases:

- TDD-style no-Skill baseline
- binary evidence-grounded evaluation
- critique before verdict
- threshold-blind judging when possible
- cross-family judge calibration when available
- pressure tests for brittle discipline rules
- held-out regression gates
- small edit budgets
- blind A/B comparison for major changes
- variance-aware acceptance

The rule is simple: do not call an improvement real because one sample looks better

## Evidence states

Conductor distinguishes:

- `OBSERVED`
- `DERIVED`
- `INFERRED`
- `PROPOSED`

And release states such as:

- `DESIGNED`
- `STRUCTURALLY_VALIDATED`
- `BEHAVIOR_TESTED`
- `PORTABILITY_STRUCTURAL_ONLY`
- `PORTABILITY_TESTED`
- `PACKAGED`
- `SUBMISSION_DRAFT`
- `SUBMITTED`
- `APPROVED`
- `PUBLISHED`

No state is silently upgraded into another

## Repository shape

```text
.codex-plugin/
  plugin.json

skills/
  skill-conductor/
    SKILL.md
    agents/
    references/
    scripts/
    eval-viewer/
  skill-architect/
    SKILL.md
  skill-evaluator/
    SKILL.md
  skill-portability-compiler/
    SKILL.md
  host-workspace-operator/
    SKILL.md

assets/
  logo-light.svg
  logo-dark.svg
  mark.svg
```

The original Conductor evaluation agents, BinEval references, pressure-testing material, viewer, and helper scripts remain part of the repository and are reused where the active host can actually execute them

## Cross-host rule

A host receives one explicit status:

- `SUPPORTED_TESTED`
- `SUPPORTED_STRUCTURAL_ONLY`
- `ADAPTER_REQUIRED`
- `UNSUPPORTED`
- `UNKNOWN`

“Works everywhere” is not a valid status

## OpenAI Skills and Plugins

OpenAI Skills follow the Agent Skills open standard and are supported across ChatGPT, Codex, and the API. Plugins can package one or more Skills and may remain Skills-only when no external app is required

Skill Conductor uses that Skills-only architecture for its ChatGPT/Codex Plugin surface

## Credits and methodology roots

Conductor builds on ideas and research from Anthropic Skill Creator, Superpowers writing-skills, SkillOpt, BinEval / Ask Don't Judge, TICK, CheckEval, SkillJuror, SkillReducer, SOP/TWI practice, and the other references documented throughout this repository

The project keeps those ideas as methodology inputs rather than treating any single vendor runtime as the definition of a Skill

## License

MIT
