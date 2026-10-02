---
name: check-understanding
version: 1.0.0
description: Phase quiz for Harness Engineering from Scratch. Trigger with "quiz me", "test phase", "check my understanding", "do I know phase 3", or `/check-understanding <phase>`.
---

# Check Understanding

Test the learner's knowledge of a completed phase from **Harness Engineering from
Scratch**.

## Activation

- `/check-understanding 2` or `/check-understanding tools`
- "quiz me on phase 3", "test phase 8", "am I ready for the next phase"

## Input

Accepts a phase number (1–10) or a phase name. If none given, list all 10 phases
(from `harness-engineering/ROADMAP.md`) and ask which to test.

## Phase Map

| Input | Directory | Phase |
|-------|-----------|-------|
| 1, loop, foundations | `01-foundations-and-the-loop` | Foundations & the loop |
| 2, tools | `02-tools` | Tools |
| 3, context, memory | `03-context-and-memory` | Context & memory |
| 4, prompts, instructions | `04-prompts-and-instructions` | Prompts & instructions |
| 5, files, shell | `05-files-and-shell` | Files & shell |
| 6, permissions, security | `06-permissions-and-security` | Permissions & security |
| 7, planning, subagents | `07-planning-and-subagents` | Planning & subagents |
| 8, mcp, skills, retrieval | `08-extending-mcp-skills-retrieval` | Extending: MCP, skills, retrieval |
| 9, reliability, evals, ops | `09-reliability-evals-and-ops` | Reliability, evals & ops |
| 10, capstone | `10-capstone` | Capstone |

## Procedure

1. **Resolve the phase.** Validate the number is 1–10, or map the keyword. On a miss,
   show the full list.
2. **Read the content.** Read `harness-engineering/phases/<phase-dir>/README.md` (its
   "Test yourself" questions show what matters) and glob
   `harness-engineering/phases/<phase-dir>/*/docs/en.md`. Read every lesson in the phase.
3. **Generate 6 questions** (4 for the capstone) from what you read:
   - Q1–3 **conceptual** (what/why): definitions, reasoning, relationships.
   - Q4–6 **practical** (how/build): implementation, correct ordering, "if you see X,
     do what?".
   Each has 3–4 options, exactly one correct; wrong options plausible but clearly
   wrong to someone who studied. Tag each with its source lesson. Do not reuse the
   README questions word for word.
4. **Present one at a time** via AskUserQuestion. Don't reveal answers until the end.
5. **Score & advise.** Report `N/6` (`N/4` for the capstone). At least 5/6 (3/4) → ready
   for the next phase. Below that → list the specific lessons (by path) to review, drawn
   from the questions they missed.
