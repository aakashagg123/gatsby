# Forward Deployed Engineering — the module plan

A plan for a new standalone module on the **Forward Deployed Engineer (FDE)** — the role
that makes AI work in production, not just in demos. Written for the product leader who
scopes, hires, or becomes one.

> **Status:** planning captured; open decisions listed below need an answer before the
> pilot lesson starts.

## Why this module

Three signals say the role is real and growing, not a fad:

- Job postings for forward deployed engineers grew more than 800% in 2025 (*Financial
  Times*).
- An estimated 70% of AI pilots never reach production. The FDE exists to close that gap.
- Global base compensation for the role commonly starts above $220k, with senior and
  staff-level FDEs well past that.

A forward deployed engineer builds, deploys, and owns AI systems inside a customer's real
environment. The role spans software, platform, and solution work. It exists to make AI
work beyond the demo. Palantir, OpenAI, and Anthropic hire for it, and the pattern is now
spreading across the industry.

## The FDE work cycle

The source material describes a six-step cycle. Each step becomes a lesson:

1. **Understand the business reality** — learn how the business actually works, past the
   stated requirement.
2. **Define the right problem** — translate business pain into a clear, solvable problem
   worth using AI for.
3. **Design the AI approach** — decide what the AI should do, what data it uses, and how
   you measure success.
4. **Build within real constraints** — fit the solution to the data, systems, security,
   and infrastructure that already exist.
5. **Deploy into production** — ship working AI into a live environment where real users
   depend on it.
6. **Own outcomes and improve** — monitor performance, fix failures, and improve from
   real use.

## Topics: extracted, then expanded

**From the source program:**

- The six-step FDE work cycle (discovery to ownership)
- Dual track — technical execution and consulting delivery run together
- The Learn → Apply → Build loop — concept, then simulation, then a real system
- Agentic orchestration (LangGraph, CrewAI, Semantic Kernel)
- Advanced prompting (chain-of-thought, ReAct, DSPy)
- Vector search (Pinecone, Weaviate, Qdrant)
- LLM operations — tracing, cost, and quality tooling
- Deployment stack (Modal, Replicate, Together AI, BentoML)
- Safety and guardrails — input/output checks, PII detection
- Case simulations — fraud detection, CRM enrichment, ticket routing, API docs

**Added for depth (gaps a product leader needs, not in the source):**

- FDE vs. adjacent roles — software engineer, consultant, solutions engineer
- The pilot-to-production chasm — why 70% fail, named and mapped
- The success contract — acceptance criteria agreed with the client up front
- Enterprise and legacy integration — the systems the AI must fit into
- Security, compliance, and data governance — the enterprise bar
- Adoption and change management — trust is the real blocker, not accuracy
- Unit economics of a deployment — the cost the outcome must beat
- Handoff, ownership, and SLAs — who runs it after you leave
- The commercial layer — scoping, pricing, land-and-expand
- From one deployment to a product — repeatability and the moat

## Proposed lesson outline

Ten lessons and a recap, following the work cycle, then adding the consulting and
commercial craft that the cycle alone doesn't cover. Each lesson links to a deeper spoke
in an existing track.

| # | Lesson | Phase | Spokes |
| --- | --- | --- | --- |
| 1 | What a forward deployed engineer is | The role | `product-sense` |
| 2 | Why AI pilots fail | The problem | `content/04-evals-observability`, `content/06-strategy-tradeoffs` |
| 3 | Understand the business and frame the problem | Cycle · steps 1–2 | `product-sense`, `technical-product-management` |
| 4 | Design the AI approach and the success contract | Cycle · step 3 | `rag-vector-databases`, `agentic-ai` |
| 5 | Build within real constraints | Cycle · step 4 | `system-design`, `technical-product-sense` |
| 6 | Deploy into production | Cycle · step 5 | `system-design`, `content/05-safety-multitenancy` |
| 7 | Own outcomes and improve | Cycle · step 6 | `content/04-evals-observability`, `agentic-ai` |
| 8 | Communicate, build trust, drive adoption | Consulting craft | `product-sense`, `technical-product-management` |
| 9 | Scope, price, and expand the engagement | Commercial | `agentic-ai`, `knowledge-graphs` |
| 10 | The FDE toolkit and career path | Toolkit & career | `agentic-ai`, `rag-vector-databases` |
| ↩ | Recap & real-world examples | Close-out | — |

## How it fits the curriculum

- **Slug:** `forward-deployed-engineering` — a flat track, same shape as `agentic-ai` and
  `rag-vector-databases`.
- **Positioning:** the role that ships the Generative AI family. The family teaches the
  parts (LLMs, RAG, agents, evals, security); this track teaches the person who
  assembles them for one customer, in production.
- **Dedup:** hub-and-spoke. Each lesson is a standalone overview that links to the deep
  dive (RAG, agents, evals, security, system design) instead of repeating it.
- **House style:** matched exactly — TL;DR → 🎯 For the product leader → mental model →
  mechanics → tradeoffs → failure modes → checklist → related. One diagram per lesson.
  Key-terms box per lesson.

## Build steps (per `CLAUDE.md`)

1. Write the markdown — README, ten lessons, and recap, in house style and Simplified
   English.
2. Add the build script — `scripts/build_forward_deployed_engineering.py`, a thin config
   on `build_standalone.build_track`.
3. Wire `build_site.py` — a track HTML constant, a copytree block, a landing card, and a
   bumped module count.
4. Register the graph and links — the slug in `build_graph.py` (`TRACKS` and
   `FLAT_TRACKS`), `build_html.py`'s `FLAT` tuple, and `check_links.py`'s `SCAN_DIRS`.
5. Add glossary terms — new terms homing to the new lessons (pilot-to-production,
   success contract, land-and-expand) so each lesson gets its Key-terms box.
6. Update root docs — the README craft-tracks table and `SUMMARY.md`.
7. Build and verify — run the build, `check_links.py`, validate the diagrams, confirm the
   track shows in the graph's node counts.
8. Ship — commit through a `claude/*` branch, open a PR, merge to `master`. Pages deploys
   within minutes.

## Sequencing

Pilot-first, the way the Generative AI family is built. Build lesson 2, **Why AI pilots
fail**, first — it is the thesis of the whole track and the sternest test of the
hub-and-spoke links into evals and strategy. Lock that pattern, then batch the rest in
cycle order: the six cycle lessons, then the consulting, commercial, and toolkit lessons.

## Open decisions

Four calls that change the build — needed before the pilot lesson starts:

1. **Depth** — product-leader lens only, or a dual layer (concept for PMs plus a build
   layer for engineers, like Flowable)? The source program is engineer-heavy.
2. **Family** — inside the Generative AI family, or its own top-level "Field & delivery"
   track? It is a role, not a capability.
3. **Tools** — name specific tools (LangGraph, Pinecone, Modal) as the source does, or
   stay tool-agnostic and teach the frameworks? House style leans framework-first.
4. **Scope** — keep it at ten lessons, or split the commercial and consulting craft into
   its own module later?
