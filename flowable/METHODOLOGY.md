# Methodology — how the Flowable *from-scratch* track works

This document defines the pedagogical framework for the **Flowable** track: the lesson
shape, the two audience layers, and the way phases stack. The
[`foundations/`](./foundations/process-automation-principles.md) doc gives the conceptual
spine; the lessons make you build it.

---

## 0. Audience assumption — two layers, explicitly

Every lesson serves two readers at once:

- The **PM / architect** reads Motto → Problem → Concept (and Ship It when the artifact
  is a decision guide). These beats never require code. Together with the
  `foundations/` spine they form a complete course in process automation architecture:
  when BPMN, when CMMN, when DMN; when to embed the engine, when to run it standalone;
  when Flowable is the right tool at all versus a state machine in your own tables or a
  durable-execution runtime like Temporal.
- The **engineer** additionally does Build It and Use It. Build It is always plain
  Python standard library — no Java toolchain needed to understand the semantics. Use It
  targets a real Flowable engine over REST (Docker image `flowable/flowable-rest`) or,
  where the point *is* the embedding, a Spring Boot snippet.

## 1. The thesis: *Build It, then Use It*

Every engine capability is learned twice:

1. **Build It** — implement the semantics by hand: a token engine, a gateway evaluator,
   a persistent wait state, a job executor. Small, complete, runnable (~80–150 lines).
2. **Use It** — run the same process through the real Flowable engine. Now the engine is
   transparent: `runtimeService.startProcessInstanceByKey(...)` isn't magic, it's the
   loop you wrote, with a database and twenty years of edge cases.

You earn the right to trust an engine by building a toy version once. This is the single
most important idea in the track.

## 2. The six-beat lesson template

| Beat | Purpose | Layer |
| :-- | :-- | :-- |
| **MOTTO** | One sentence. The core idea, quotable. | both |
| **PROBLEM** | A concrete pain. "What can't you do without this?" | both |
| **CONCEPT** | Diagram + intuition. Code comes *after*. | both |
| **BUILD IT** | From scratch, Python stdlib, no engine. | engineer |
| **USE IT** | The same thing on real Flowable (REST or Spring Boot). | engineer |
| **SHIP IT** | A reusable artifact the lesson produces. | both |
| **CHECK YOURSELF** | 3–5 quiz questions + one challenge exercise. | both |

## 3. Every lesson ships something real

A lesson ends with an artifact you keep, saved under the lesson's `outputs/`:

- a **process model** (`.bpmn20.xml` — deployable to any BPMN 2.0 engine),
- a **decision table** (`.dmn`),
- a **module** (a reusable Python building block of the toy engine),
- a **client** (a REST script that drives a real engine), or
- a **decision guide** (a one-page architecture/product cheat sheet).

## 4. Stacked phases — a dependency graph, not a flat list

Phases are arranged so lower layers are prerequisites for higher ones: the token model →
engine state & transactions → human tasks → system integration → decisions (DMN) → cases
(CMMN) → events → versioning → operations → architecture → **capstone**.

The token model is the floor; a production loan-origination process is the roof. Skip
ahead if you know a lower layer, but don't skip and then wonder why the top is breaking.

## 5. Same folder shape, everywhere

```
phases/<NN>-<phase-name>/<NN>-<lesson-name>/
├── code/      runnable implementations (Python; Java/XML where the point is Flowable itself)
├── docs/
│   └── en.md  the lesson narrative (translations: zh.md, ja.md, …)
└── outputs/   the process model / module / client / decision guide it ships
```

[`ROADMAP.md`](./ROADMAP.md) is the **single source of truth** for phases and lessons.
Status glyphs `✅ 🚧 ⬚` on every row track progress. Authoring is editing markdown in a
strict format (see [`AUTHORING.md`](./AUTHORING.md)).

## 6. Diagrams first, quizzes throughout

- **Diagrams** lead the Concept beat — Mermaid for process flows and architecture,
  tables for comparisons (BPMN vs CMMN vs DMN, Flowable vs Camunda vs Temporal).
- **Quizzes** make it stick: each lesson ends with self-test questions, answers in
  collapsed blocks.

## 7. Operating principles (the tone)

- No vendor marketing. Trade-offs stated plainly, including when *not* to use Flowable.
- Everything in Build It runs on your own laptop with plain Python.
- Use It requires only Docker (`flowable/flowable-rest`); Java appears only where the
  lesson is *about* embedding the engine.
- Fintech-flavoured examples throughout — loan origination, KYC, approvals — because
  that is where BPM engines earn their keep.

## 8. The capstone

One end-to-end project: a loan origination process combining BPMN (the flow), DMN (the
credit decision), user tasks (manual review), service tasks (bureau calls), timers
(offer expiry), and error handling (bureau downtime) — deployed and driven over REST.
