# Methodology — what we're borrowing from *AI Engineering from Scratch*

This document extracts the pedagogical framework behind
[aiengineeringfromscratch.com](https://aiengineeringfromscratch.com) /
[`rohitg00/ai-engineering-from-scratch`](https://github.com/rohitg00/ai-engineering-from-scratch),
so we can apply the *same* framework to **Harness Engineering**.

It is descriptive (what they do) followed by prescriptive (what we copy, what we change).

---

## 1. The thesis: *Build It, then Use It*

> "Every algorithm gets built from raw math first … By the time PyTorch shows up, you
> already know what it's doing under the hood."

The whole curriculum is one move repeated hundreds of times:

1. **Build It** — implement the thing by hand, no frameworks, just the standard library
   and the underlying math. Small, ugly, ~100–150 lines, but *complete and runnable*.
2. **Use It** — do the same task again with the production tool (PyTorch, sklearn,
   tiktoken…). Now the framework is transparent because you wrote the toy version.

You learn the abstraction by first earning the right to skip it. This is the single
most important idea to carry over.

## 2. The six-beat lesson template

Every lesson — all 503 of them — has the *same* shape, so the reader never has to
re-learn the navigation:

| Beat | Purpose |
| :-- | :-- |
| **MOTTO** | One sentence. The core idea, quotable. |
| **PROBLEM** | A concrete pain. "What can't you do without this?" |
| **CONCEPT** | Diagrams + intuition. Code comes *after*. |
| **BUILD IT** | From scratch, raw, no frameworks. |
| **USE IT** | Same thing through the real library. |
| **SHIP IT** | A reusable artifact the lesson produces. |
| *(Exercises)* | 2 + 1 challenge, to make it stick. |

## 3. Every lesson ships something real

The defining differentiator versus other courses. A lesson does not end with
"congratulations, you learned X." It ends with a **tool you keep**:

- a **prompt** (paste into any assistant),
- a **skill** (`SKILL.md`, drop into Claude/Cursor/Codex),
- an **agent** (a loop you wrote yourself),
- an **MCP server** (plug into any MCP client).

> "By the end you have a portfolio of 503 artifacts you actually understand because
> you built them."

These artifacts are installable (`scripts/install_skills.py`). The course is also a
toolbox.

## 4. Stacked phases — a dependency graph, not a flat list

20 phases, each 12–42 lessons, arranged so **lower layers are prerequisites for higher
ones**: math → classical ML → deep learning → (vision / NLP / speech / RL) →
transformers → LLMs → LLM engineering → tools/protocols → agents → autonomous →
multi-agent → infra → ethics → **capstone**.

"Math is the floor. Agents and production are the roof. Skip ahead if you know the
lower layers, but don't skip and then wonder why the top is breaking."

## 5. Same folder shape, everywhere

```
phases/<NN>-<phase-name>/<NN>-<lesson-name>/
├── code/      runnable implementations (Python, TS, Rust, Julia)
├── notebook/  optional Jupyter experimentation
├── docs/
│   └── en.md  the lesson narrative (translations: zh.md, ja.md, …)
└── outputs/   the prompt / skill / agent / MCP server it ships
```

The `README.md` + `ROADMAP.md` are the **single source of truth**: a build script
(`site/build.js`) parses their phase headers and lesson tables to generate the website
data. Status glyphs `✅ 🚧 ⬚` on every row track progress. **Authoring = editing
markdown in a strict format**, then a build step renders it. No CMS.

## 6. Self-placement and self-checking, agent-native

Two skills make the course adaptive without an LMS:

- `/find-your-level` — a 10-question quiz that maps you to a starting phase and builds
  a personalized path with hour estimates.
- `/check-understanding <phase>` — an 8-question per-phase quiz with feedback and the
  exact lessons to review.

The course is meant to be *run inside an agent* (Claude, Cursor, Codex), not just read.

## 7. Operating principles (the tone)

- "No five-minute videos, no copy-paste deploys, no hand-holding."
- Free, open-source, MIT, runs on your own laptop.
- Multi-language to prove the idea transcends any one ecosystem.
- The README/ROADMAP themselves are beautiful — banner, badges, mermaid diagrams.

---

## 8. What we copy vs. change for Harness Engineering

| Dimension | AIEFS | Harness Engineering from Scratch |
| :-- | :-- | :-- |
| **Core move** | Build It / Use It | **Keep identical.** Build the loop/tool/context-manager by hand, then use the real SDK/framework. |
| **Six-beat lesson** | Motto→Problem→Concept→Build→Use→Ship | **Keep identical.** |
| **Ships an artifact** | prompt/skill/agent/MCP | **Keep + extend** → also **hooks**, **harness modules**, **evals**, **settings**. |
| **Stacked phases** | math → … → agents | **Re-theme**: I/O → agent loop → tools → context → memory → subagents → MCP → reliability → evals → security → production → **capstone: build your own coding agent**. |
| **Folder shape** | `phases/NN/NN-lesson/{code,docs,outputs}` | **Keep identical** for consistency. |
| **Languages** | Python, TS, Rust, Julia | **Python + TypeScript** (harnesses are mostly TS/Node + Python SDKs). |
| **"From raw math"** | numpy/stdlib | **"From raw stdlib"** — `requests`/`fetch` + a model API, no agent framework, until Use It. |
| **Existing `content/`** | n/a | Becomes the **CONCEPT** reading each lesson links to — we don't throw it away, we build *on top* of it. |
| **Capstone** | 17 products | **One capstone**: assemble every phase into a working coding agent. |
