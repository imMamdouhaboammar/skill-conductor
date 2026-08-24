# OpenAI Plugin Submission Pack

Status: `not_ready`

Architecture: `skills-only`

Target package: Skill Conductor 4.0.0

Repository: https://github.com/imMamdouhaboammar/skill-conductor

## Product job

Skill Conductor helps people create, review, test, adapt, and package reusable agent skills. It separates portable behavioral instructions from host-specific discovery, tool, and packaging mechanics.

## Public skill inventory

- `skill-conductor`: primary skill engineering workflow
- `host-workspace-operator`: maps file/repository work to the safest host-native capability
- `sandbox-python-executor`: governs deterministic Python execution and evidence

No MCP server is required for the core product.

## Listing draft

Name: Skill Conductor

Short description: Design and test agent skills

Long description: Create new agent skills, diagnose weak ones, build evidence-backed evals, adapt skills across agent hosts, and package them for distribution without treating provider-specific behavior as universal.

Category: Developer Tools

Website: https://github.com/imMamdouhaboammar/skill-conductor

Support: https://github.com/imMamdouhaboammar/skill-conductor/blob/main/SUPPORT.md

Privacy: https://github.com/imMamdouhaboammar/skill-conductor/blob/main/PRIVACY.md

Terms: https://github.com/imMamdouhaboammar/skill-conductor/blob/main/TERMS.md

Version: 4.0.0

Package name: skill-conductor

## Capabilities

- Design agent skills
- Evaluate skill behavior
- Port skills across hosts
- Package skills for distribution

## Starter prompts

1. Design a production-ready skill for this workflow and target it to ChatGPT and Codex.
2. Review this skill, find trigger and behavior failures, then propose the smallest evidence-backed fixes.
3. Port this Claude Code skill to an Agent Skills-compatible version and report host-specific gaps.

## Positive reviewer cases

### 1. Create for ChatGPT/Codex

Prompt: `Create a reusable skill that makes a coding agent inspect repository instructions, make a focused patch, run tests, and report evidence. Target ChatGPT and Codex.`

Expected behavior:
- activates `skill-conductor`
- captures a SkillSpec with triggers, negatives, baseline failure, workflow, host targets, and evals
- separates portable behavior from host-native file/shell mechanics
- produces a valid skill structure and test plan

Expected result shape:
- SkillSpec
- `SKILL.md`
- eval cases
- host notes

Fixture: none

### 2. Review a weak skill

Prompt: `Review this skill. It triggers on almost every coding question and often skips its body.`

Expected behavior:
- classifies overtriggering and process-in-description risks
- uses review/validation checks
- proposes small evidence-backed edits rather than a full rewrite by default

Expected result shape:
- findings
- critical failures
- proposed edits
- unverified checks

Fixture: a sample skill folder

### 3. Port from Claude Code

Prompt: `Port this Claude Code skill to ChatGPT/Codex without assuming Claude tool names exist.`

Expected behavior:
- reads source behavior and host assumptions
- keeps universal instructions
- replaces/isolates Claude-specific mechanics
- produces target-host gaps and retest requirements

Expected result shape:
- ported skill
- host gap report
- target eval matrix

Fixture: a Claude Code skill

### 4. Build evals

Prompt: `Create a held-out eval set for this skill. I need direct, indirect, negative, and pressure cases.`

Expected behavior:
- creates realistic prompt families
- distinguishes discovery from behavior assertions
- preserves held-out discipline

Expected result shape:
- eval JSON or equivalent structured cases
- acceptance criteria

Fixture: a skill or SkillSpec

### 5. Package as skills-only plugin

Prompt: `Package these skills as a ChatGPT/Codex plugin. They do not need external services.`

Expected behavior:
- chooses skills-only architecture
- creates `.codex-plugin/plugin.json`
- keeps skills under `./skills/`
- does not invent MCP dependencies
- validates package-relative paths

Expected result shape:
- plugin tree
- validation report
- submission-readiness blockers

Fixture: one or more valid skills

## Negative reviewer cases

### 1. Ordinary coding task

Prompt: `Fix the off-by-one bug in this loop.`

Expected behavior:
- Skill Conductor should not activate solely because the task is coding

Why:
- this is general implementation work, not skill engineering

### 2. Prompt-only copy request

Prompt: `Write me one prompt that summarizes an article.`

Expected behavior:
- do not force the request into a reusable skill unless the user asks for a repeatable skill/workflow

Why:
- ordinary prompt writing is outside the skill's primary boundary

### 3. Use an existing skill

Prompt: `Use my PDF skill to extract this table.`

Expected behavior:
- Skill Conductor should not replace the requested PDF skill
- it may only engage if the user asks to debug, improve, port, or package that skill

Why:
- using a skill is distinct from engineering a skill

## Brand assets

- `assets/logo-light.svg`
- `assets/logo-dark.svg`
- `assets/icon.svg`

Concept: three instruction tracks are routed through one controlled decision point into a target-host output.

## Current blockers

1. Developer/business identity must be selected from a verified identity in the OpenAI Platform. Do not infer it from the GitHub owner or manifest.
2. ChatGPT desktop/Web and Codex install/discovery smoke tests have not been executed by this repository-only change.
3. Final public URLs must be checked after merge so the `main` links resolve to the submitted content.
4. The final submission artifact and SHA256 must be generated from the exact release commit before submission.
5. Re-check live OpenAI submission requirements immediately before submitting.

## Required final evidence

- release commit/ref
- deterministic package/hash if used
- plugin manifest validation
- final skill tree validation
- ChatGPT/Codex smoke results
- five positive and three negative reviewer cases
- verified publisher identity
- public support/privacy/terms URLs
- final availability regions

Do not change status to `submission_ready` until every blocker is cleared.
