<p align="center">
  <img src="assets/conductor.png" alt="Skill Conductor" width="100%">
</p>

# Skill Conductor

> Design, test, repair, port, and package agent Skills from one evidence-driven workflow

Skill Conductor is a meta-skill for building other Skills

It does not start with "write a SKILL.md"

It starts with the failure you want to fix, turns that into a portable SkillSpec, maps the Skill to the target agent's capabilities, tests the behavior, and only then packages the result

```text
failure evidence
      |
      v
  SkillSpec
      |
      v
 host contract
      |
      v
 implementation
      |
      v
    evals
      |
      v
 quality gate
      |
      v
   package
```

## What changed in v4

Earlier versions already had a strong eval core: TDD baselines, architecture selection, BinEval, held-out gates, pressure tests, judge calibration, and controlled self-improvement

v4 keeps that core and removes the biggest portability assumption: Skill design is no longer tied to Claude Code

The Conductor now separates:

1. **Universal behavior**: what the Skill must teach or enforce
2. **Host contract**: what ChatGPT, Codex, Claude Code, or another agent can actually discover and execute
3. **Evidence**: which tests were really run on which host
4. **Packaging**: standalone Agent Skill, ChatGPT/Codex Plugin, Claude Code plugin, or a custom host package

That separation matters because a Skill can be structurally valid and still fail on a specific agent due to discovery, tool, approval, filesystem, or runtime differences

## One SkillSpec, multiple agents

Before authoring a non-trivial Skill, Conductor captures a neutral SkillSpec

```json
{
  "name": "release-auditor",
  "purpose": "Review a release candidate before shipping",
  "baseline_failure": "The agent skips package-boundary and changelog checks",
  "triggers": {
    "positive": [
      "review this release before I publish",
      "check whether this package is ready to ship",
      "audit this release candidate"
    ],
    "negative": [
      "write release notes",
      "publish this package"
    ]
  },
  "outputs": [
    "release verdict",
    "blocking findings",
    "verification evidence"
  ],
  "host_targets": ["chatgpt", "codex", "claude-code"],
  "workflow": [
    {
      "action": "Inspect release inputs",
      "why": "The review must be grounded in the exact candidate",
      "freedom": "medium"
    }
  ],
  "evals": [
    {
      "prompt": "Review this package before I publish it",
      "should_trigger": true
    },
    {
      "prompt": "Write a launch tweet",
      "should_trigger": false
    },
    {
      "prompt": "Check this release candidate for blockers",
      "should_trigger": true
    }
  ]
}
```

The portable compiler can then scaffold an Agent Skills-compatible Skill:

```bash
python3 skills/skill-conductor/scripts/compile_skill_spec.py \
  --spec skill-spec.json \
  --out ./generated
```

## Seven modes

| Mode | Job | Result |
| --- | --- | --- |
| CREATE | Build a new Skill | SkillSpec + implementation + eval set |
| IMPROVE | Fix an unreliable Skill | Small evidence-backed edits |
| VALIDATE | Test a Skill | Structural + discovery + behavior + portability evidence |
| REVIEW | Inspect a third-party Skill | Quality and safety gate |
| OPTIMIZE | Improve triggering | Held-out description candidate |
| PORT | Adapt to another agent | Target-host variant + gap report |
| PACKAGE | Distribute | Standalone Skill or host plugin package |

## Architecture before instructions

Conductor keeps the architecture-first approach from earlier releases

Choose a pattern before writing detailed instructions:

| Pattern | Use when |
| --- | --- |
| Sequential workflow | Order matters |
| Iterative refinement | Quality improves through bounded cycles |
| Context-aware selection | The same job needs different paths by context |
| Domain intelligence | The agent needs specialized knowledge |
| Multi-tool coordination | The job spans several services or capability families |

Then set freedom per step:

| Freedom | Use when |
| --- | --- |
| Low | A mistake is expensive and behavior should be deterministic |
| Medium | A preferred method exists but judgment is still needed |
| High | Several approaches can be correct |

The practical test is simple: the higher the consequence of a mistake, the lower the freedom should be

## Host profiles

The Conductor ships with profiles for:

- Agent Skills baseline
- ChatGPT
- Codex
- Claude Code
- custom or unknown hosts

A host profile records capabilities instead of assuming tool names:

```text
discovery
skill format
package format
read
list
search
grep
write / patch
shell
python
subagents
network
approval behavior
trigger evidence
install evidence
```

If a host is unknown, Conductor produces a portable baseline Skill plus an explicit gap list rather than inventing fields or tool calls

## Cross-host evaluation

A "portable" claim requires four different checks:

1. **Artifact**: the Skill is structurally valid
2. **Discovery**: intended prompts trigger and near-misses do not
3. **Behavior**: the Skill changes the target behavior in the intended way
4. **Portability**: host-specific assumptions are either satisfied or reported

Evidence is labeled by host

A successful Claude Code trigger test is not evidence that ChatGPT or Codex will trigger the Skill correctly

## Evaluation core

The existing research-heavy evaluation engine remains central

### TDD baseline

Prove the agent fails without the Skill before adding instructions

If the baseline already succeeds reliably, the Skill may be unnecessary

### BinEval

Instead of hiding quality behind one fuzzy score, Conductor decomposes evaluation into atomic binary questions across:

- Discovery
- Clarity
- Structure
- Robustness
- Completeness

Critical questions form the gate

The scalar score is diagnostic, not the release criterion

### Held-out improvement gate

When improving a Skill:

- freeze the train / held-out split
- learn from train cases
- apply at most three atomic edits per iteration
- reject candidates that create a confirmed held-out regression
- reject candidates that introduce a new critical failure
- keep the best accepted version

### Pressure testing

For instructions that must hold under temptation, ambiguity, conflicting requests, or time pressure, use repeated fresh-context micro-tests and adversarial cases

## ChatGPT and Codex Plugin

v4 includes a skills-only Plugin package for ChatGPT and Codex

```text
.codex-plugin/
  plugin.json

skills/
  skill-conductor/
  host-workspace-operator/
  sandbox-python-executor/

assets/
  logo-light.svg
  logo-dark.svg
  icon.svg

.agents/plugins/
  marketplace.json
```

Why skills-only?

Skill Conductor does not need a remote service to do its core job

It teaches workflow and uses capabilities already exposed by the current host

An MCP server can be added later only if a real external data or action boundary requires one

### Add the repository marketplace

```bash
codex plugin marketplace add imMamdouhaboammar/skill-conductor --ref main
```

Then use the ChatGPT desktop Plugin Directory or Codex plugin controls to install and test the package on the surfaces available to you

## Internal routing

`skill-conductor` remains the public orchestrator

Two narrow helper Skills support it:

- `host-workspace-operator`: routes repository work through the safest read, search, patch, write, shell, or Python capability the current host exposes
- `sandbox-python-executor`: requires actual Python execution evidence for deterministic parsing, validation, archive inspection, or hashing

This avoids a common plugin problem where several public Skills compete for the same trigger and the model picks unpredictably

## Runtime

Design, review, and SkillSpec work do not require Claude or Anthropic credentials

Portable compiler and static portability checks use Python 3 standard library:

```bash
python3 skills/skill-conductor/scripts/test_portability.py

python3 skills/skill-conductor/scripts/validate_portability.py \
  skills/skill-conductor \
  --targets agent-skills,chatgpt,codex,claude-code \
  --plugin-root .
```

The older trigger optimization runner is intentionally kept as a Claude Code adapter because it observes Claude-specific discovery behavior

Do not use its result as cross-host evidence

## Repository layout

```text
skills/skill-conductor/
  SKILL.md
  agents/
    grader.md
    comparator.md
    analyzer.md
    bineval.md
  references/
    skill-spec.md
    host-profiles.md
    cross-host-evaluation.md
    patterns.md
    schemas.md
    sop-practices.md
    bineval-method.md
    quality-questions.md
    pressure-testing.md
    runtime-setup.md
  scripts/
    compile_skill_spec.py
    validate_portability.py
    test_portability.py
    init_skill.py
    eval_skill.py
    run_eval.py
    run_loop.py
    improve_description.py
    aggregate_benchmark.py
    generate_report.py
    package_skill.py
    quick_validate.py
    test_smoke.py
```

## Authoring principles

The Conductor still applies the core rules developed in previous versions:

- prove the failure before adding a Skill
- keep process out of discovery metadata
- use `SKILL.md` as a map and move deep material into references
- write for a fresh practitioner, not for the author who already knows the context
- explain why a risky step exists
- test with a blind agent
- place checks at the point of risk
- use one term per concept
- remove text that does not change behavior
- match the form of the instruction to the failure being corrected

## Research foundations

The project synthesizes methods and findings from work including:

- Anthropic Skill Creator and Claude Skill guidance
- Superpowers `writing-skills`
- Microsoft SkillOpt
- Hamel Husain's eval methodology
- Grafana skill-authoring practices
- Trail of Bits skill-improver work
- Standard Operating Procedure literature and TWI Job Instruction
- BinEval / "Ask, Don't Judge"
- TICK and CheckEval
- Guardrails Beat Guidance
- SkillJuror and SkillReducer
- work on judge self-preference and externally gated self-correction

The repository's detailed references remain the source for the exact methodology and citations

## Plugin submission status

The repository contains a reviewer-facing submission draft at:

```text
submission/OPENAI_PLUGIN_SUBMISSION.md
```

Packaging work and public submission are intentionally separate states

A package can be locally valid without being submitted, approved, or published

The submission pack therefore records unresolved publisher identity, live host testing, and final artifact evidence instead of pretending those gates passed

## Credits

Skill Conductor was originally created by `smixs` and developed around architecture-first Skill authoring and evidence-based evaluation

This fork extends that work toward cross-agent portability and ChatGPT/Codex Plugin distribution while keeping the original MIT license and methodology lineage

## License

MIT
