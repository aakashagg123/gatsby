# Generative AI — the family roadmap

A new top-level **family** of eleven deep, standalone modules, written in the same
product-leader / CPO lens and house style as the rest of the curriculum. It is the
**topic-organized front door** to applied generative AI — the names people actually
search for — sitting alongside (not replacing) the existing tracks, which it
cross-links for extra depth.

> **Status:** pilot shipped (*RAG & vector databases*, module 4), sign-off received.
> Modules 1 (*Generative AI: the big picture*), 2 (*LLMs*), and 3 (*APIs &
> integrations*) are now built. Remaining seven modules are batched in learning order.

## Decisions (locked)

| Decision | Choice |
| --- | --- |
| Shape | 11 full, multi-lesson modules (not single-lesson hubs) |
| Audience | Senior/Principal PMs & product leaders (CPO lens) |
| Overlap with existing tracks | **Coexist & cross-link** — new modules are the canonical topic homes; `content/`, `agentic-ai/`, `knowledge-graphs/` stay as complementary references, linked both ways. Nothing deleted. |
| Dedup | Hub-and-spoke — a lesson gives a complete standalone overview and links out to an existing deep dive rather than re-deriving it |
| Size | Right-sized per topic (deeper topics 7-8 lessons, tighter ones 4-6) |
| House style | Match exactly: TL;DR → 🎯 For the product leader → mental model/mechanics → tradeoffs → failure modes → checklist → related; one mermaid diagram per lesson; README knowledge-graph opener; HTML edition; glossary + knowledge-graph node registration; per-lesson Key-terms box |
| Positioning | New "Generative AI" family on the landing, in the learning order below, cross-linked into one site-wide knowledge graph |
| Sequencing | Plan all → build one pilot end-to-end for sign-off → batch the rest |

## The eleven modules (learning order)

Each module is a standalone track folder (e.g. `rag-vector-databases/`) with a
`README.md` (knowledge-graph opener), its lessons, and a `recap.md`.

### 1. 🤖 Generative AI: the big picture — *6 lessons* — **BUILT**
The umbrella. What generative AI is and isn't, and how it reshapes the product surface.
1. [What makes AI "generative"?](./generative-ai/what-is-generative-ai.md) · 2. [The five modalities](./generative-ai/the-modalities.md) · 3. [Probabilistic software](./generative-ai/probabilistic-software.md) · 4. [The generative AI product stack](./generative-ai/the-genai-product-stack.md) · 5. [Build, buy, or fine-tune](./generative-ai/build-buy-or-fine-tune.md) · 6. [Where value is created and destroyed](./generative-ai/where-value-is-created-and-destroyed.md). → [Recap](./generative-ai/recap.md).
*Spokes:* `content/00-foundations`, `content/01-inference-internals`, `content/06-strategy-tradeoffs`, `rag-vector-databases`, `agentic-ai`.

### 2. 🧠 LLMs — *7 lessons* — **BUILT**
The engine most of the family runs on.
1. [What an LLM actually is](./llms/what-is-an-llm.md) · 2. [The context window](./llms/the-context-window.md) · 3. [Capabilities & the jagged frontier](./llms/capabilities-and-the-jagged-frontier.md) · 4. [Prompting & in-context learning](./llms/prompting-and-in-context-learning.md) · 5. [Temperature, sampling & determinism](./llms/temperature-sampling-and-determinism.md) · 6. [Choosing a model](./llms/choosing-a-model.md) · 7. [Prompting vs. RAG vs. fine-tuning](./llms/prompting-vs-rag-vs-finetuning.md). → [Recap](./llms/recap.md).
*Spokes:* `content/01-inference-internals/*`, `content/06-strategy-tradeoffs/finetune-vs-icl-vs-rag`.

### 3. 🔗 APIs & integrations — *6 lessons* — **BUILT**
How the model reaches the rest of your system.
1. [The request/response contract](./api-integrations/the-request-response-contract.md) · 2. [Calling an LLM API](./api-integrations/calling-an-llm-api.md) · 3. [Structured output & JSON mode](./api-integrations/structured-output-and-json-mode.md) · 4. [Webhooks & async patterns](./api-integrations/webhooks-and-async-patterns.md) · 5. [Integrating into existing systems](./api-integrations/integrating-into-existing-systems.md) · 6. [MCP & standard connectors](./api-integrations/mcp-and-standard-connectors.md). → [Recap](./api-integrations/recap.md).
*Spokes:* `technical-product-sense/apis-and-contracts`, `content/02-reliable-outputs/structured-output`, `agentic-ai/tools-and-function-calling`.

### 4. 🗂️ RAG & vector databases — *7 lessons* — **BUILT** (pilot)
Grounding models in your data — and proving they used it.
1. Why RAG (grounding, freshness, private data, citations) · 2. Embeddings & semantic search · 3. Vector databases (indexing, ANN, filtering, scale) · 4. Chunking & ingestion pipelines · 5. Retrieval quality (hybrid search, reranking, recall/precision) · 6. RAG vs. long-context vs. fine-tuning · 7. Beyond flat RAG: GraphRAG & structured retrieval. → Recap.
*Spokes:* `content/03-rag/*`, `knowledge-graphs/*`.

### 5. 💾 Memory & context — *6 lessons*
What the model can "see," and what it remembers.
1. The context window as working memory · 2. Short-term vs. long-term memory · 3. Context engineering (curation, compaction, offloading) · 4. Memory architectures (episodic, semantic, profile) · 5. Retrieval as memory · 6. Failure modes (context rot, poisoning, staleness). → Recap.
*Spokes:* `content/00-foundations/context-engineering`, `agentic-ai/context-and-memory`.

### 6. 🛠️ Tool calling — *5 lessons*
How a model acts on the world.
1. What tool calling is · 2. Tool schemas & contracts · 3. Reliability (validation, repair, idempotency) · 4. Permissions & the blast radius of a tool · 5. MCP & tool ecosystems. → Recap.
*Spokes:* `content/02-reliable-outputs/function-calling`, `agentic-ai/tools-and-function-calling`.

### 7. ⚙️ AI agents — *7 lessons*
Software that decides its own next step.
1. What an agent is (the loop) · 2. The autonomy spectrum · 3. Planning & reasoning · 4. Tools & the environment · 5. Memory & state across a run · 6. Single-agent reliability (compounding error) · 7. When *not* to build an agent. → Recap.
*Spokes:* `agentic-ai/what-is-an-agent`, `agentic-ai/planning-and-reasoning`, `agentic-ai/reliability-and-evals`.

### 8. 🔄 Agentic workflows — *6 lessons*
Orchestrating many steps and many agents.
1. Workflows vs. agents (enumerable vs. open-ended) · 2. Orchestration patterns (chains, routers, parallel) · 3. Multi-agent systems & protocols · 4. Human-in-the-loop & approvals · 5. Durable execution & long-running work · 6. Workflow capture as product strategy. → Recap.
*Spokes:* `agentic-ai/multi-agent-and-protocols`, `flowable/*`, `agentic-ai/agentic-ai-as-a-product`.

### 9. 📊 Evaluation & observability — *7 lessons*
You cannot operate what you cannot measure.
1. Why eval is the job · 2. Evals (golden sets, LLM-as-judge, adversarial) · 3. Error analysis (open & axial coding) · 4. Observability (traces, spans, drift) · 5. Trajectory evals for agents · 6. Eval-driven development · 7. The eval stack in production. → Recap.
*Spokes:* `content/04-evals-observability/*`, `agentic-ai/reliability-and-evals`, `technical-product-management/tpm-for-ai-products`.

### 10. 🔐 AI security & guardrails — *7 lessons*
Keeping the system, its data, and its tenants safe.
1. The threat model (prompt injection, jailbreaks, leakage) · 2. The lethal trifecta · 3. Guardrails (input/output, runtime, fail-closed) · 4. Least privilege & permissions · 5. Multi-tenant isolation · 6. Human-in-the-loop & audit trails · 7. Governance & compliance. → Recap.
*Spokes:* `content/05-safety-multitenancy/*`, `agentic-ai/safety-security-and-governance`.

### 11. 💰 Cost optimization — *6 lessons*
Making the economics work.
1. Where AI cost comes from (tokens & inference) · 2. Cost attribution per feature, tenant & journey · 3. Model routing & the cheap path · 4. Caching (prompt & semantic) · 5. Controlling context & retrieval cost · 6. Unit economics & the supervised-cost view. → Recap.
*Spokes:* `content/04-evals-observability/cost-attribution`, `content/02-reliable-outputs/model-routing`, `content/01-inference-internals/prompt-vs-semantic-caching`, `agentic-ai/agentic-ai-as-a-product`.

**Total:** ~70 lessons + 11 READMEs + 11 recaps.

## Cross-link discipline (hub-and-spoke)

- Each lesson stands alone for a product leader, then points to its **spoke** (an existing
  deep-dive lesson) with a one-line "go deeper" link — never re-deriving mechanics that
  already have a home.
- Existing spoke lessons get a **back-link** to the new module over time, so the graph is
  bidirectional. New modules are canonical *topic homes*; existing tracks keep their angle.
- Every new term added to the glossary follows `GLOSSARY_FRAMEWORK.md` and homes to a
  lesson in the family, so each new lesson gets its Key-terms box automatically.

## Build order after the pilot

Foundations (1 GenAI, 2 LLMs, 3 APIs) → Building blocks (4 RAG ✅ pilot, 5 Memory, 6 Tools)
→ Systems (7 Agents, 8 Workflows) → Operations (9 Evals, 10 Security, 11 Cost). Each module
ships complete (content + HTML + glossary + graph + Key-terms) before the next begins.

## Wiring checklist per module (mirrors the existing tracks)

- [ ] `<slug>/` markdown: `README.md` (knowledge-graph opener) + lessons + `recap.md`.
- [ ] `scripts/build_<slug>.py` (thin wrapper around `build_standalone.build_track`).
- [ ] Register in `build_site.py` (HTML dir + copy + landing card), `build_graph.py`
      (`TRACKS` colour + `FLAT_TRACKS`), `check_links.py` (`SCAN_DIRS`).
- [ ] Glossary terms for the module's key concepts, homing to its lessons.
- [ ] `README.md` family table + `SUMMARY.md` learning path.
- [ ] Build, `check_links.py`, mermaid validate, headless-verify, ship.
