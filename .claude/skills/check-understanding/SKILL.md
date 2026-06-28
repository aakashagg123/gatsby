---
name: check-understanding
version: 1.0.0
description: Phase quiz for Harness Engineering from Scratch. Trigger with "quiz me", "test phase", "check my understanding", "do I know phase 3", or `/check-understanding <phase>`.
---

# Check Understanding

Test the learner's knowledge of a completed phase from **Harness Engineering from
Scratch**.

## Activation

- `/check-understanding 2` or `/check-understanding agent-loop`
- "quiz me on phase 3", "test phase 8", "am I ready for the next phase"

## Input

Accepts a phase number (0–19) or a phase name. If none given, list all 20 phases
(from `harness-engineering/ROADMAP.md`) and ask which to test.

## Phase Map

| Input | Directory | Phase |
|-------|-----------|-------|
| 0, setup | `00-setup-and-tooling` | Setup & Tooling |
| 1, io, llm-io | `01-llm-io-foundations` | LLM I/O Foundations |
| 2, loop, agent-loop | `02-the-agent-loop` | The Agent Loop |
| 3, tools | `03-tool-engineering` | Tool Engineering |
| 4, context | `04-context-engineering` | Context Engineering |
| 5, prompts | `05-prompt-instruction-architecture` | Prompt & Instruction Architecture |
| 6, files, code-ops | `06-file-and-code-operations` | File & Code Operations |
| 7, shell, sandbox | `07-shell-and-sandbox-execution` | Shell & Sandbox Execution |
| 8, permissions | `08-permissions-and-safety-gating` | Permissions & Safety Gating |
| 9, memory | `09-memory-and-persistence` | Memory & Persistence |
| 10, subagents | `10-subagents-and-orchestration` | Subagents & Orchestration |
| 11, planning | `11-planning-and-task-management` | Planning & Task Management |
| 12, mcp | `12-mcp-and-extensibility` | MCP & Extensibility |
| 13, retrieval | `13-retrieval-and-codebase-understanding` | Retrieval & Codebase Understanding |
| 14, reliability | `14-reliability-engineering` | Reliability Engineering |
| 15, evals | `15-evals-and-testing-the-harness` | Evals & Testing the Harness |
| 16, observability, cost | `16-observability-and-cost` | Observability & Cost |
| 17, security | `17-security-and-alignment` | Security & Alignment |
| 18, production, deploy | `18-production-and-deployment` | Production & Deployment |
| 19, capstone | `19-capstone-coding-agent` | Capstone: Build Your Own Coding Agent |

## Procedure

1. **Resolve the phase.** Validate the number is 0–19, or map the keyword. On a miss,
   show the full list.
2. **Read the content.** Glob `harness-engineering/phases/<phase-dir>/*/docs/en.md` and read them. For
   large phases (10+ lessons), read a representative spread (first, middle, last).
3. **Generate exactly 8 questions** from what you read:
   - Q1–4 **conceptual** (what/why): definitions, reasoning, relationships.
   - Q5–8 **practical** (how/build): implementation, correct ordering, "if you see X,
     do what?".
   Each has 3–4 options, exactly one correct; wrong options plausible but clearly
   wrong to someone who studied. Tag each with its source lesson.
4. **Present one at a time** via AskUserQuestion. Don't reveal answers until the end.
5. **Score & advise.** Report `N/8`. ≥6 → ready for the next phase. <6 → list the
   specific lessons (by path) to review, drawn from the questions they missed.
