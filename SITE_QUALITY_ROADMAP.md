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
| Right-hand outline nav infra (Workstream 2a) | — | — | — | ☑ | Generic infra: `content/` + all 16 flat tracks. Shipped PR #71. |
| `product-sense/` | ☑ | ☑ | ☑ | ☑ | Audited full module against WRITER.md and the 4 axes. Already compliant — thesis-first, active voice, no hedging/filler, mini-cases doing real work, sharp closes. No content gaps material enough to warrant a wave: prioritization/metrics frameworks are deliberately out of scope here and already cross-linked to `technical-product-management/`. No edits shipped. |
| `technical-product-sense/` | ☑ | ☑ | ☑ | ☑ | Audited full module (9 lessons + recap). Already compliant with WRITER.md — thesis-first TL;DRs, worked-pass mini-cases with real mechanism (idempotency key, retry storm, p95 budget breakdown, unit-economics napkin), sharp closes, no hedging or filler. No content gaps material enough to warrant a wave. No edits shipped. |
| `technical-product-management/` | ☑ | ☑ | ☑ | ☑ | Audited full module (9 lessons + recap). Already compliant with WRITER.md — thesis-first, evidence-driven (Knight Capital, expand/migrate/contract), sharp closes, no filler. No content gaps material enough to warrant a wave. No edits shipped. |
| `first-principles/` | ☑ | ☑ | ☑ | ☑ | Audited full module (6 lessons + recap). Already compliant with WRITER.md — thesis-first, sourced case studies (SpaceX, Wright brothers, Theranos, Munger, Ericsson) doing real work, sharp closes, no filler. No content gaps material enough to warrant a wave. No edits shipped. |
| GenAI module 10 (AI security & guardrails) | ☑ | ☑ (written fresh) | n/a | ☑ | Shipped 2-lesson module in WRITER.md voice from the start, rescoped from a planned 7 lessons — see `GENERATIVE_AI_ROADMAP.md` for the rescoping rationale. |
| GenAI module 11 (Cost optimization) | ☑ | ☑ (written fresh) | n/a | ☑ | Shipped 2-lesson module in WRITER.md voice from the start, rescoped from a planned 6 lessons. Completes the 11-module family. |
| Phased-track nav infra (Workstream 2b) | ☑ | — | — | ☑ | Two-level Phase → Lesson left sidebar for `harness-engineering/`, `flowable/`. Active phase expands; others collapse to a link to their own README. |
| Methodology/Authoring removal (Workstream 3) | — | — | — | ☑ | Deleted 4 files, fixed all reference sites. `check_links.py` confirms 0 broken links. |
| GenAI module 1 (Generative AI: the big picture) | ☑ | ☑ | ☑ | ☑ | Audited (background agent). Already WRITER.md-compliant — thesis-first, one load-bearing analogy per lesson, sharp closes, zero hedging/filler hits. No material gaps. No edits shipped. |
| GenAI module 2 (LLMs) | ☑ | ☑ | ☑ | ☑ | Audited (background agent). Already compliant, zero hedging/filler hits (spot-checked "might be"/"leverage"/"unlocked" in context — all legitimate). No material gaps; deeper mechanics correctly deferred to inference-internals spokes. No edits shipped. |
| GenAI module 3 (APIs & integrations) | ☑ | ☑ | ☑ | ☑ | Audited (background agent). Already compliant, zero hedging/filler hits. MCP history and recap examples verified accurate as of today. No material gaps. No edits shipped. |
| GenAI module 4 (RAG & vector databases) | ☑ | ☑ | ☑ | ☑ | Audited (background agent). Already compliant, zero hedging/filler hits (the one "leverage" hit is legitimate noun usage). Depth/breadth/accuracy solid; hub-and-spoke discipline followed correctly. No edits shipped. |
| GenAI module 5 (Memory & context) | ☑ | ☑ | ☑ | ☑ | Audited (background agent). Already compliant — "might be"/"seems to" hits are all in-scope descriptions of memory's illusion/variability, not authorial hedging. No material gaps within its deliberately narrow scope. No edits shipped. |
| GenAI module 6 (Tool calling) | ☑ | ☑ | ☑ | ☑ | Audited (background agent). Already compliant, zero hedging/filler hits. All 5 spoke links verified to resolve. No material gaps. No edits shipped. |
| GenAI module 7 (AI agents) | ☑ | ☑ | ☑ | ☑ | Audited (background agent). Already compliant, zero hedging/filler hits, no exclamation points. All spoke links to agentic-ai/ verified. No material gaps. No edits shipped. |
| GenAI module 8 (Agentic workflows) | ☑ | ☑ | ☑ | ☑ | Audited (background agent). Already compliant, zero hedging/filler hits. Spoke links to agentic-ai/ and flowable/ verified. No material gaps. No edits shipped. |
| GenAI module 9 (Evaluation & observability) | ☑ | ☑ | ☑ | ☑ | Audited (background agent). Already compliant, zero hedging/filler hits. All 4 spoke links verified. No material gaps. No edits shipped. |
| `content/` (AI engineering, 7 modules) | n/a | ☑ | ☑ | ☑ | Audited (3 background agents, 37 files). Already WRITER.md-compliant, zero material voice issues. Two real gap classes found and fixed: (1) modules 02/03/05 predated the newer GenAI-family tracks and never backlinked to `tool-calling/`, `rag-vector-databases/`, `ai-security-and-guardrails/` — added 6 spoke links. (2) `01-inference-internals` was missing 3 genuinely current (2025-26) techniques: MLA (DeepSeek-V2/V3 KV compression), prefill/decode disaggregation as a production serving architecture, and FP4 (Blackwell-class quantization) — added to `kv-cache-management.md`, `batching-and-paged-attention.md`/`prefill-vs-decode.md`, and `quantization-formats.md` respectively. Nav (right-hand outline) already live from Workstream 2a. |
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
