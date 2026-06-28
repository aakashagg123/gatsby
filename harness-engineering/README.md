<div align="center">

# Harness Engineering — from scratch

**Build a production coding agent (a "harness" like Claude Code) by hand, one piece at a
time — then use the real SDKs.** Every lesson ships a reusable artifact.

![Phases](https://img.shields.io/badge/phases-20-3553ff?style=flat-square&labelColor=1f1e1d)
![Track](https://img.shields.io/badge/track-build%20it%20%2F%20use%20it-3553ff?style=flat-square&labelColor=1f1e1d)

**[🗺️ Roadmap](./ROADMAP.md)** · **[🧭 Methodology](./METHODOLOGY.md)** · **[✍️ Authoring](./AUTHORING.md)** · **[📐 Ten Principles](./foundations/harness-principles.md)**

</div>

> This is a **separate track** from the AI Engineering module (which lives in the repo
> root). A *harness* is the system around the model — the loop, tools, context, memory,
> permissions, subagents, and evals. Here you build each piece yourself, then run the
> same thing through the real framework, so the abstraction is transparent.

## Audience

This track assumes you work inside **Claude Code or Codex**. You build each piece of a
harness yourself to understand it, then every **Use It** maps it to how those tools do it
(memory files, hooks, skills, subagents, MCP, permissions), and every shipped artifact is
installable into them.

## How it works

Each lesson runs the same six beats: **Motto → Problem → Concept → Build It → Use It →
Ship It**, then a short self-quiz. You implement from the standard library first, then
use the production SDK. See [`METHODOLOGY.md`](./METHODOLOGY.md).

## Start here

- **Find your level:** run `/find-your-level` (placement quiz) — or just open the
  [Roadmap](./ROADMAP.md).
- **Read the spine first:** [The Ten Principles of a Working Harness](./foundations/harness-principles.md).
- **First worked lessons:**
  - [The agent loop from scratch](./phases/02-the-agent-loop/01-agent-loop/docs/en.md)
  - [Sprint contracts & budgeted waves](./phases/10-subagents-and-orchestration/01-sprint-contract-and-waves/docs/en.md)

## Status

Phases **2 (The Agent Loop)** and **10 (Subagents & Orchestration)** are complete; the
rest are scaffolded in the [Roadmap](./ROADMAP.md). Quiz yourself per phase with
`/check-understanding <phase>`.

## Run the code

```bash
python3 harness-engineering/phases/02-the-agent-loop/01-agent-loop/code/agent_loop.py
```

<div align="center"><sub>Educational content. Use it, fork it, teach from it.</sub></div>
