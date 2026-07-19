# Methodology — how the *from-scratch* build track works

This document defines the pedagogical framework for the hands-on **Harness Engineering**
build track: the lesson shape, the artifacts, and the way phases stack. The
[`foundations/`](./foundations/harness-principles.md) docs give the conceptual spine; the lessons make you
build it.

---

## 0. Audience assumption — you use Claude Code or Codex

Every lesson assumes the reader works inside an agentic coding tool — **Claude Code** or
**Codex**. You build each harness component from scratch to understand it, then the
**Use It** beat maps that component to how Claude Code / Codex already do it
(`CLAUDE.md` / `AGENTS.md` memory, `settings.json` hooks, skills, subagents, MCP servers,
permission modes). The artifacts each lesson ships are installable into those tools. When
a lesson says "in a real harness," it means Claude Code or Codex.

## 1. The thesis: *Build It, then Use It*

Every capability is learned twice:

1. **Build It** — implement the thing by hand, no frameworks, just the standard library.
   Small, complete, runnable (~80–150 lines).
2. **Use It** — do the same task again with the production tool (the model SDK, the MCP
   SDK, a sandbox runtime…). Now the framework is transparent, because you wrote the toy
   version first.

You earn the right to skip an abstraction by building it once. This is the single most
important idea in the track.

## 2. The six-beat lesson template

Every lesson has the *same* shape, so the reader never re-learns the navigation:

| Beat | Purpose |
| :-- | :-- |
| **MOTTO** | One sentence. The core idea, quotable. |
| **PROBLEM** | A concrete pain. "What can't you do without this?" |
| **CONCEPT** | Diagram + intuition. Code comes *after*. |
| **BUILD IT** | From scratch, raw, no frameworks. |
| **USE IT** | The same thing through the real SDK / framework. |
| **SHIP IT** | A reusable artifact the lesson produces. |
| **CHECK YOURSELF** | 3–5 quiz questions + one challenge exercise. |

## 3. Every lesson ships something real

A lesson doesn't end with "congratulations, you learned X." It ends with a **tool you
keep**, saved under the lesson's `outputs/`:

- a **prompt** (paste into any assistant),
- a **skill** (`SKILL.md`, drop into any agent that reads it),
- a **hook**, **harness module**, **eval**, **settings** file, or
- an **MCP server** (plug into any MCP client).

By the end you have a portfolio of artifacts you understand because you built them.

## 4. Stacked phases — a dependency graph, not a flat list

Phases are arranged so **lower layers are prerequisites for higher ones**: LLM I/O →
agent loop → tools → context → memory → subagents → MCP → reliability → evals →
security → production → **capstone**.

The model-as-a-function is the floor; a working coding agent is the roof. Skip ahead if
you know a lower layer, but don't skip and then wonder why the top is breaking.

## 5. Same folder shape, everywhere

```
phases/<NN>-<phase-name>/<NN>-<lesson-name>/
├── code/      runnable implementations (Python and/or TypeScript)
├── notebook/  optional Jupyter experimentation
├── docs/
│   └── en.md  the lesson narrative (translations: zh.md, ja.md, …)
└── outputs/   the prompt / skill / hook / module / eval / MCP server it ships
```

[`ROADMAP.md`](./ROADMAP.md) is the **single source of truth** for phases and lessons.
Status glyphs `✅ 🚧 ⬚` on every row track progress. Authoring is editing markdown in a
strict format (see [`AUTHORING.md`](./AUTHORING.md)).

## 6. Diagrams first, quizzes throughout

- **Diagrams** lead the Concept beat — Mermaid for flows/architecture, tables for
  comparisons, ASCII for simple mental models.
- **Quizzes** make it stick: each lesson ends with self-test questions (answers in
  collapsed blocks), and two skills automate placement and review —
  [`/find-your-level`](../.claude/skills/find-your-level/SKILL.md) and
  [`/check-understanding <phase>`](../.claude/skills/check-understanding/SKILL.md).

The track is meant to be *run inside an agent* (Claude, Cursor, Codex), not just read.

## 7. Operating principles (the tone)

- No five-minute videos, no copy-paste deploys, no hand-holding.
- Everything runs on your own laptop.
- Python first, TypeScript where the harness ecosystem lives (Node).
- The [`foundations/`](./foundations/harness-principles.md) docs are the **Concept** reading each build lesson
  links to — read the idea, then build it.
- Default to the latest, most capable model in Use-It code (**Claude Opus 4.8**,
  `claude-opus-4-8`).

## 8. The capstone

One end-to-end project: assemble every phase into a working coding agent — loop, tools,
file ops, context, memory, permissions, subagents, MCP, evals, and observability.
