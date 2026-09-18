# Site quality roadmap

A running status file for a site-wide initiative: every module gets (a) a voice pass
against `WRITER.md`, (b) a real navigation upgrade (sections + sub-sections instead of a
flat lesson list), and (c) a 4-axis gap analysis (depth, breadth, accuracy,
comprehensiveness) followed by content waves that close what's missing. "Authoring" and
"Methodology" meta-documentation is being removed from the two tracks that have it. This
file exists so the program's state survives context resets across sessions — update it as
each module ships.

## How the work is scoped

- **Voice pass**: rewrite every lesson against `WRITER.md` — thesis-first, active voice,
  no hedging, deliberate sentence-rhythm variation, one load-bearing analogy instead of
  decorative metaphor, no corporate filler, sharp closes. The house-style skeleton (TL;DR
  → 🎯 briefing → mental model → mechanics → tradeoffs → failure modes → checklist →
  related) stays — WRITER.md governs sentence- and paragraph-craft, not the pedagogical
  structure.
- **Nav**: a right-hand "on this page" scroll-spy outline (auto-built from each lesson's
  own headings) for `content/` and every flat track; a real two-level left sidebar
  (Phase → Lesson) for the phased tracks (`harness-engineering/`, `flowable/`), which
  currently have none.
- **Gap analysis**: depth (real mechanism, not just naming it), breadth (are the
  important sub-topics all present), accuracy (anything stale or oversimplified past the
  point of being right), comprehensiveness (does it cover what a learner searching this
  topic expects to find).

## Status

| Track | Nav | Voice pass | Gap analysis | Shipped | Notes |
| --- | --- | --- | --- | --- | --- |
| Right-hand outline nav infra (Workstream 2a) | — | — | — | ☐ | Generic infra: `content/` + all 16 flat tracks |
| `product-sense/` | ☐ | ☐ | ☐ | ☐ | |
| `technical-product-sense/` | ☐ | ☐ | ☐ | ☐ | |
| `technical-product-management/` | ☐ | ☐ | ☐ | ☐ | |
| `first-principles/` | ☐ | ☐ | ☐ | ☐ | |
| GenAI module 10 (AI security & guardrails) | ☐ | n/a (written fresh) | n/a | ☐ | |
| GenAI module 11 (Cost optimization) | ☐ | n/a (written fresh) | n/a | ☐ | Completes the 11-module family |
| Phased-track nav infra (Workstream 2b) | ☐ | — | — | ☐ | `harness-engineering/`, `flowable/` |
| Methodology/Authoring removal (Workstream 3) | — | — | — | ☐ | Delete 4 files, fix 6 link sites |
| GenAI module 1 (Generative AI: the big picture) | ☐ | ☐ | ☐ | ☐ | Retrofit |
| GenAI module 2 (LLMs) | ☐ | ☐ | ☐ | ☐ | Retrofit |
| GenAI module 3 (APIs & integrations) | ☐ | ☐ | ☐ | ☐ | Retrofit |
| GenAI module 4 (RAG & vector databases) | ☐ | ☐ | ☐ | ☐ | Retrofit |
| GenAI module 5 (Memory & context) | ☐ | ☐ | ☐ | ☐ | Retrofit |
| GenAI module 6 (Tool calling) | ☐ | ☐ | ☐ | ☐ | Retrofit |
| GenAI module 7 (AI agents) | ☐ | ☐ | ☐ | ☐ | Retrofit |
| GenAI module 8 (Agentic workflows) | ☐ | ☐ | ☐ | ☐ | Retrofit |
| GenAI module 9 (Evaluation & observability) | ☐ | ☐ | ☐ | ☐ | Retrofit |
| `content/` (AI engineering, 7 modules) | ☐ | ☐ | ☐ | ☐ | |
| `agentic-ai/` | ☐ | ☐ | ☐ | ☐ | |
| `knowledge-graphs/` | ☐ | ☐ | ☐ | ☐ | |
| `harness-engineering/` | ☐ | ☐ | ☐ | ☐ | Needs Workstream 2b shipped first |
| `flowable/` | ☐ | ☐ | ☐ | ☐ | Needs Workstream 2b shipped first |

## Execution order

1. Right-hand outline nav infra (own PR, ships before any content wave).
2. `product-sense/` → `technical-product-sense/` → `technical-product-management/` →
   `first-principles/` (user-directed priority order).
3. GenAI module 10, then module 11.
4. Phased-track nav infra + Methodology/Authoring removal (own PR).
5. Retrofit GenAI modules 1 → 9, in order.
6. `content/`.
7. `agentic-ai/`, `knowledge-graphs/`.
8. `harness-engineering/`, `flowable/`.

See `/root/.claude/plans/humble-crunching-meadow.md` (session-local, not in the repo) for
the full plan this roadmap was built from, including exploration findings on the
`forward-deployed` repo's nav patterns and gatsby's current per-track-shape nav code.
