---
name: skill-conductor
description: >
  Design, create, improve, evaluate, port, review, and package agent Skills. Use when a user wants to teach an agent a repeatable workflow, convert a prompt/SOP/runbook into a Skill, fix unreliable Skill activation or behavior, test a Skill, compare Skill versions, make a Skill portable across ChatGPT/Codex/Claude or another agent host, or prepare a Skill for distribution, even when they do not explicitly say "Skill". Do NOT use for merely executing an already-installed Skill or for unrelated general coding.
---

# Skill Conductor

Design Skills as behavioral products, not long prompts

The invariant lifecycle is:

`need -> contract -> architecture -> baseline -> build -> evaluate -> improve -> port -> package`

Host syntax comes after the behavioral contract

## Router

Choose the narrowest path that completes the user's job

| Intent | Route |
|---|---|
| create a new Skill or turn a workflow into one | `skill-architect` then evaluation |
| fix or strengthen an existing Skill | diagnose then `skill-evaluator`, apply gated edits |
| test or benchmark a Skill | `skill-evaluator` |
| make a Skill work on another agent host | `skill-portability-compiler` |
| review a third-party Skill | review contract + structural and behavioral gates |
| package a standalone Skill | validate then use existing packaging scripts when executable |
| package this repository as ChatGPT/Codex Plugin | use Plugin Autopilot rules and keep submission evidence separate |

If focused Skills are unavailable, execute the same contracts from this Skill directly

## Universal pre-flight

Before authoring, read:

- `references/skill-contract.md`
- `references/sop-practices.md`
- `references/patterns.md`

Read `references/host-adapters.md` when the target host matters
Read `references/pressure-testing.md` for discipline or brittle-rule Skills
Read `references/bineval-method.md` and `references/quality-questions.md` for evaluation

Do not require `uv`, an Anthropic key, or any vendor-specific runtime merely to design or review a Skill

When an executable helper is useful, first inspect the active host capabilities. Run the helper only when the host actually provides execution. Otherwise keep execution-dependent claims unverified

## Phase 1: Prove the Skill should exist

Capture at least:

1. one recurring user job
2. two or three realistic trigger prompts
3. close negative examples
4. the failure or inconsistency of the base agent
5. the consequence if the agent gets the behavior wrong

Prefer an actual no-Skill baseline when the host can run an isolated test

If no baseline can be executed, label the need as `INFERRED_NEED`, not proven failure

If the base agent already performs the job reliably and the Skill adds no durable preference, workflow, domain knowledge, or gate, recommend no Skill

## Phase 2: Freeze the Skill Contract

Create the contract from `references/skill-contract.md`

At minimum freeze:

- one job
- positive triggers
- implicit triggers
- negative triggers
- collision set
- behavioral preconditions and completion conditions
- evidence rules
- mutation boundaries
- required/optional capabilities
- evaluation coverage

Do not write the final `SKILL.md` until the contract is coherent

## Phase 3: Choose architecture before prose

Use `references/patterns.md`

Common patterns:

- sequential workflow
- iterative refinement
- context-aware selection
- domain intelligence
- multi-service coordination

A Skill may combine patterns, but one pattern should own the main control flow

### Calibrate freedom per step

Use consequence, reversibility, and verifiability

- low freedom: deterministic script, schema, exact checker
- medium freedom: decision table, pseudocode, constrained template
- high freedom: judgment with several acceptable outputs

Do not use rigid instructions where judgment is the product
Do not leave fragile mechanics to free-form judgment when a deterministic check is practical

## Phase 4: Design activation

Treat the description as routing metadata

A strong description answers:

- what capability this Skill provides
- when users need it
- several ways users may phrase that need
- nearby cases where it should not load

Do not encode the workflow in the description
Do not rely only on the canonical domain term
Do not make the description so broad that it competes with generic agent behavior

Build an activation bank with positive, implicit, negative, and collision prompts before finalizing the description

## Phase 5: Author with progressive disclosure

Use this shape unless the job needs something more specific:

```text
skill-name/
  SKILL.md
  references/   optional deep guidance
  scripts/      optional deterministic mechanics
  assets/       optional output resources
```

Keep `SKILL.md` as the operating map
Move deep explanations into `references/`
Move repeated or fragile deterministic work into `scripts/`

Prefer:

- imperative instructions
- decision tables at branching points
- inline checks exactly where failure risk appears
- examples that demonstrate boundaries, not decorative examples
- explicit evidence and stop conditions

Remove:

- generic model knowledge that changes no behavior
- duplicated rules
- contradictory synonyms for the same concept
- hidden environment assumptions
- personal absolute paths
- credential values
- claims about tools the active host may not provide

## Phase 6: Evaluate behavior, not appearance

Use `skill-evaluator` when available. Otherwise apply the same gate directly

Evaluation must cover four independent questions:

1. Activation: did the Skill load for the right prompts and stay out for the wrong prompts
2. Compliance: did the agent follow the important decisions and gates
3. Outcome: did the produced result satisfy the user job
4. Efficiency: did the Skill add needless context, steps, tokens, or tool work

Prefer binary questions grounded in evidence over an opaque scalar score

A structural pass is not a behavioral pass
A plausible output is not evidence that the Skill caused the right behavior

### Baseline and comparison

For CREATE, compare against no-Skill behavior when executable
For IMPROVE, compare against the frozen parent version
For major redesigns, use blind A/B comparison when the host can provide isolated runs

### Pressure testing

For discipline Skills, test situations that tempt the model to bypass the rule

Use `references/pressure-testing.md`

Do not add a prohibition just because a shaping example failed. Match the form of the rule to the failure class

## Phase 7: Improve with a regression gate

Do not rewrite the Skill wholesale from a few failures

For each iteration:

1. identify the smallest generalized failure
2. propose no more than three atomic edits
3. apply edits using TRAIN evidence only when a train/held-out split exists
4. rerun all relevant cases
5. reject the candidate if held-out behavior regresses or a new critical failure appears
6. record transitions: improved, regressed, persistent-fail, stable-success

Stop when critical failures are cleared or the iteration budget is exhausted

Keep the best accepted version, not the latest version

## Phase 8: Compile for the target host

Read `references/host-adapters.md`

Separate:

### Portable core

- user job
- activation intent
- decision logic
- gates
- evidence requirements
- schemas
- examples
- completion conditions

### Host adapter

Only host-specific differences such as:

- install/package layout
- manifest metadata
- tool invocation names
- hooks or lifecycle syntax
- supported resource types

Do not duplicate the portable core into every adapter

For every claimed host assign one status:

- `SUPPORTED_TESTED`
- `SUPPORTED_STRUCTURAL_ONLY`
- `ADAPTER_REQUIRED`
- `UNSUPPORTED`
- `UNKNOWN`

Never report structural compatibility as tested behavioral compatibility

## Phase 9: Validate and package

When host execution is available, use the existing repository validators and packagers where applicable

Inspect any untrusted script before executing it

Package only intended Skill files
Reject:

- secrets
- symlinks when the target format forbids them
- absolute user paths
- missing referenced files
- path traversal
- stale generated output
- claims of tests that were not executed

For deterministic packagers, build twice and compare hashes when practical

## Phase 10: Report evidence states clearly

Use distinct states:

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

Do not collapse them

## Existing Conductor assets

The repository already includes mature evaluation material and scripts. Reuse them when they fit the active host instead of rewriting mechanics from scratch:

- `agents/grader.md`
- `agents/comparator.md`
- `agents/analyzer.md`
- `agents/bineval.md`
- `references/bineval-method.md`
- `references/quality-questions.md`
- `references/pressure-testing.md`
- `scripts/eval_skill.py`
- `scripts/aggregate_benchmark.py`
- `scripts/improve_description.py`
- `scripts/package_skill.py`
- `scripts/quick_validate.py`

Treat vendor-specific executor instructions inside legacy assets as adapter implementation details. Preserve their useful evaluation logic without making that vendor a universal dependency

## Completion gate

Before saying a Skill is ready, answer with evidence:

- Does one clear recurring job justify the Skill
- Are positive, implicit, negative, and collision triggers defined
- Is the architecture chosen before prose
- Is freedom calibrated by consequence
- Are references/scripts used for the right reasons
- Are required host capabilities honest
- Are critical behaviors testable
- Were baseline or parent comparisons actually executed when claimed
- Are regressions gated
- Is portability status explicit per host
- Are packaging and submission states reported separately

If any answer depends on an unexecuted test, mark it unverified instead of guessing
