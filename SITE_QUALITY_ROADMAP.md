# Site quality roadmap

A running status file for a site-wide initiative: every module gets (a) a voice pass
against `WRITER.md`, (b) a real navigation upgrade (sections + sub-sections instead of a
flat lesson list), and (c) a 4-axis gap analysis (depth, breadth, accuracy,
comprehensiveness) followed by content waves that close what's missing. "Authoring" and
"Methodology" meta-documentation is being removed from the two tracks that have it. This
file exists so the program's state survives context resets across sessions — update it as
each module ships.

> **Update (2026-09-29).** The status table below records the first audit, which used a
> voice grep and a spoke-link check. That method could not find wrong facts or hard-to-read
> prose, and later work found both (see `CONTENT_FRAMEWORK.md`, section 10). Treat "no
> material gaps" below as "passed the first audit's checks". New passes follow
> `CONTENT_FRAMEWORK.md` and are tracked in the "Framework-based passes" section at the
> end of this file. Note: the `WRITER.md` file named below is not in the repository. The
> style reference in the repository is `WRITING-STYLE.md`.

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
| `agentic-ai/` | n/a | ☑ | ☑ | ☑ | Audited (background agent, all 9 files including `multi-agent-and-protocols.md` self-checked). Fully compliant, zero voice issues, no material gaps. Confirmed its one-directional linking from the newer GenAI-family tracks (ai-agents/, tool-calling/, etc.) is correct by design — agentic-ai/ is the deep spoke those compact tracks point into, not the other way round. No edits shipped. |
| `knowledge-graphs/` | n/a | ☑ | ☑ | ☑ | Audited (background agent, 9 files). Fully compliant voice-wise. One real gap found and fixed: `knowledge-graphs-and-llms.md` never backlinked to `rag-vector-databases/graphrag-and-structured-retrieval.md` despite that lesson linking in three times — added the missing link to the lesson body, its Related lessons, and the module README's "Connects to other tracks." |
| `harness-engineering/` | ☑ | ☑ | ☑ | ☑ | Audited (background agent; spine docs + 20 phase READMEs read in full, 1 lesson/phase sampled, exhaustive voice grep across all ~142 pages). Voice compliant, six-beat structure holds. Two real fixes: a stale README "Status" section claimed only 2 of 20 phases were complete when all 20 are (per ROADMAP.md) — corrected; and 4 missing cross-links to newer GenAI-family tracks (tool-calling/, ai-security-and-guardrails/, evaluation-and-observability/, cost-optimization/) — added, mapped to their matching phases. |
| `flowable/` | ☑ | ☑ | ☑ | ☑ | Audited (background agent; spine docs + 12 phase READMEs read in full, 1 lesson/phase sampled, exhaustive voice grep across all ~95 pages). Voice compliant, structure holds (capstone's simpler format is intentional). One real fix: added a reciprocal link from the README to `technical-product-management/tpm-for-ai-products.md`, which already linked into Phase 8 but wasn't linked back. This closes out the site-quality initiative — every track in the repo has now been audited. |

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

## Framework-based passes

Each module is improved with the workflow in `CONTENT_FRAMEWORK.md` and scored with
`python3 scripts/check_module.py <track>`. Baseline below was measured on 2026-09-29,
before any framework-based pass. Verdicts are readability plus structure checks; WARN for
a track without review stamps means it has not yet been onboarded to the full standard.

| Track | Lessons | Avg sentence | >30w % | Flesch | Test yourself | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `agentic-ai` | 8 | 15.1 | 5 | 52 | yes | WARN |
| `agentic-workflows` | 2 | 28.5 | 35 | 41 | no | FAIL |
| `ai-agents` | 3 | 26.6 | 40 | 48 | no | FAIL |
| `ai-security-and-guardrails` | 2 | 24.4 | 28 | 42 | no | FAIL |
| `api-integrations` | 6 | 25.9 | 31 | 46 | no | FAIL |
| `context-engineering` | 7 | 19.5 | 13 | 55 | no | WARN |
| `cost-optimization` | 2 | 26.1 | 32 | 44 | no | FAIL |
| `evaluation-and-observability` | 2 | 26.7 | 29 | 47 | no | FAIL |
| `first-principles` | 6 | 14.2 | 5 | 55 | yes | WARN |
| `generative-ai` | 6 | 20.1 | 17 | 58 | no | WARN |
| `knowledge-graphs` | 8 | 15.7 | 7 | 50 | no | WARN |
| `llms` | 7 | 23.3 | 25 | 52 | no | FAIL |
| `memory-and-context` | 4 | 27.0 | 34 | 34 | no | FAIL |
| `product-sense` | 7 | 15.4 | 7 | 53 | yes | WARN |
| `prompt-engineering` | 10 | 13.3 | 3 | 67 | yes | WARN |
| `rag-vector-databases` | 7 | 20.7 | 17 | 52 | no | WARN |
| `system-design` | 8 | 12.7 | 2 | 48 | no | WARN |
| `technical-product-management` | 9 | 16.5 | 10 | 54 | yes | WARN |
| `technical-product-sense` | 9 | 14.8 | 6 | 59 | yes | WARN |
| `tool-calling` | 3 | 24.9 | 25 | 47 | no | FAIL |

### Passes completed or in progress

| Track | Status | Notes |
| --- | --- | --- |
| `prompt-engineering/` | Reviewed and fixed (PR #136), not yet onboarded | Fact-checked against Anthropic guidance. Prefill and CoT attribution errors fixed. Lesson 10 added. Still needs stamps, Under-the-hood sections and a Sources list to meet the full standard. |
| `context-engineering/` | Reviewed and extended (PR #136), not yet onboarded | Added finite-context, agent, trust and noise coverage. Same follow-up as above. |
| `ai-agents/` | First framework-based pass (done, PR #137) | Expanded from 3 to 5 lessons (production runbook, acceptance testing). Before: avg sentence 26.6, 40% over 30 words, Flesch 48. After: 11.5, 2%, 70, PASS. Stamped, sourced, Under-the-hood and Test yourself added. Independent fact-check found 3 WRONG and 1 STALE claim (Moffatt date and amount, a misquote, the METR rate); all fixed. Primary pages for Gartner, METR, OWASP and CanLII could not be opened from the build sandbox, so those claims are labelled as resting on search excerpts. |
| `memory-and-context/` | Framework pass (done, PR pending) | Expanded from 4 to 5 lessons (new: writing and maintaining memory). Before: avg sentence 27.0, 34% over 30 words, Flesch 34. After: 10.6, 1%, 63, PASS. Added worked examples, Under the hood, Sources, stamps and Test yourself. Poisoning, named laws and a test section folded into lesson 5. Unsourced recap stories replaced. Blocked in the sandbox: openai.com, OWASP, GDPR and DPDP texts, so those claims are labelled. |
| `agentic-workflows/` | Framework pass (done, PR pending) | Expanded from 2 to 3 lessons (new: choosing a workflow pattern, covering the five patterns that no other lesson names). Before: avg sentence 28.5, 35% over 30 words, Flesch 41. After: 11.7, 2%, 67, PASS. Added worked examples, Under the hood, Sources, stamps and Test yourself. Restated agentic-ai content cut to summaries and pointers. Unsourced recap stories replaced with the Anthropic multi-agent post and a labelled illustration. Blocked in the sandbox: Cognition and Temporal docs, so those claims are labelled. |
| `ai-security-and-guardrails/` | Framework pass (done, PR pending) | Expanded from 2 to 3 lessons (new: red-teaming, with a measured attack-success-rate method). Before: avg sentence 24.4, 28% over 30 words, Flesch 42. After: 11.7, 2%, 63, PASS. Fixed the stale EU AI Act dates (July 2026 Digital Omnibus, Regulation (EU) 2026/1744). Fixed loose claims: many-shot shot counts, the sleeper-agent training result, an unsourced DAN story. Added OWASP and NIST mapping, worked examples, Under the hood, Sources, stamps and Test yourself. Blocked in the sandbox: arXiv, Gibson Dunn and the Official Journal, so those claims are labelled as search excerpts or secondary sources. |
| `access-control/` | New track (done, PR pending) | New flat track: 8 lessons plus recap on RBAC, ABAC, ReBAC and policy engines, OAuth/OIDC tokens, Keycloak and AI agents. Checker: avg sentence 11.3, 2% over 30 words, Flesch 61, PASS. Keycloak 26.7.5 was run locally to verify tokens, roles, attributes, authorization decisions and token exchange. Cedar and Rego snippets were run. Standards pages (NIST, RFCs, OWASP, Zanzibar) could not be opened from the sandbox and are labelled. |
| `harness-engineering/` | Trimmed to the core build path (done, PR pending) | 20 phases and 120 lessons became 10 phases and 41 lessons (51 folded into host lessons, 28 cut). Lesson docs fell from about 58.6k to about 30.8k words (code blocks included), with per-lesson quizzes, Ship It and generic Related removed and one Test yourself per phase. Fixed bugs and unverified claims found in the audit (egress guard bypass, MCP spec shapes, settings.json syntax, the cd-persistence claim, demos that could not fail). The capstone is now one agent with a unittest. All 45 offline code files run and assert. Claude Code, MCP and model-ID claims were checked against current docs. Blocked in the sandbox: modelcontextprotocol.io (spec read from its GitHub source). `check_module.py` does not cover phased tracks. |
