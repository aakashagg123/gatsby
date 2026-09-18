# Generative AI — the family roadmap

A new top-level **family** of eleven deep, standalone modules, written in the same
product-leader / CPO lens and house style as the rest of the curriculum. It is the
**topic-organized front door** to applied generative AI — the names people actually
search for — sitting alongside (not replacing) the existing tracks, which it
cross-links for extra depth.

> **Status:** pilot shipped (*RAG & vector databases*, module 4), sign-off received.
> Modules 1 (*Generative AI: the big picture*), 2 (*LLMs*), 3 (*APIs &
> integrations*), 5 (*Memory & context*), 6 (*Tool calling*), 7 (*AI agents*), 8
> (*Agentic workflows*), 9 (*Evaluation & observability*), and 10 (*AI security &
> guardrails*) are now built. One module remains.

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

### 5. 💾 Memory & context — *4 lessons* — **BUILT** (rescoped from 6 → 4)
What the model can "see," and what it remembers.
1. [Memory as a product decision](./memory-and-context/memory-as-a-product-decision.md) · 2. [Session, user & organizational memory](./memory-and-context/session-user-and-organizational-memory.md) · 3. [Retrieval as memory](./memory-and-context/retrieval-as-memory.md) · 4. [When memory goes wrong](./memory-and-context/when-memory-goes-wrong.md). → [Recap](./memory-and-context/recap.md).
*Spokes:* `content/00-foundations/context-engineering`, `agentic-ai/context-and-memory`, `rag-vector-databases`, `content/05-safety-multitenancy/multi-tenant-isolation`.

*Rescoping note:* the module was planned as 6 lessons ("the context window as working
memory," "short-term vs. long-term memory," and "memory architectures" among them), but
`content/00-foundations/context-engineering.md` and `agentic-ai/context-and-memory.md`
already cover context-window mechanics, compaction, and the episodic/semantic/profile
memory taxonomy in full engineering depth. Re-deriving that mechanics here would violate
the hub-and-spoke dedup rule. The module was cut to the 4 lessons that are genuinely new
at the product-leader altitude — treating memory as a scoped product decision, naming its
three shapes, framing retrieval as its implementation, and the trust failures it produces
— and spokes out to the two existing lessons for the mechanics.

### 6. 🛠️ Tool calling — *3 lessons* — **BUILT** (rescoped from 5 → 3)
How a model acts on the world.
1. [What tool calling is](./tool-calling/what-tool-calling-is.md) · 2. [Tool contracts & reliability](./tool-calling/tool-contracts-and-reliability.md) · 3. [Permissions, blast radius & the trust boundary](./tool-calling/permissions-blast-radius-and-the-trust-boundary.md). → [Recap](./tool-calling/recap.md).
*Spokes:* `agentic-ai/tools-and-function-calling`, `content/02-reliable-outputs/function-calling`, `api-integrations/mcp-and-standard-connectors`, `agentic-ai/safety-security-and-governance`, `technical-product-sense/security-and-privacy`.

*Rescoping note:* the module was planned as 5 lessons ("tool schemas & contracts,"
"reliability," "permissions & blast radius," and "MCP & tool ecosystems" as separate
lessons), but this topic turned out to have the densest existing coverage of any module
built so far — `agentic-ai/tools-and-function-calling.md` already develops the full
mechanics, tool-design craft, and containment discipline; `content/02-reliable-outputs/
function-calling.md` already develops contracts, validation, idempotency, and
authorization in full engineering depth; and `api-integrations/mcp-and-standard-
connectors.md` already covers the MCP integration-economics question. Several core terms
(`function-calling`/"tool calling", `tool`, `idempotency`, `mcp`, `least-privilege`,
`blast-radius`) were also already glossary entries homed to those lessons. Re-deriving any
of it would violate the hub-and-spoke dedup rule, so the module compresses to the 3
lessons that are genuinely new at the product-decision altitude — what tool calling is as
a product surface, the product decisions behind a tool's contract, and reviewing a toolbox
for permissions and third-party trust — and adds no new glossary terms, since every key
concept already had a home.

### 7. ⚙️ AI agents — *3 lessons* — **BUILT** (rescoped from 7 → 3)
Software that decides its own next step.
1. [What an agent is, and how much autonomy it needs](./ai-agents/what-an-agent-is-and-how-much-autonomy-it-needs.md) · 2. [Planning, reasoning & reliability across a run](./ai-agents/planning-reasoning-and-reliability-across-a-run.md) · 3. [When not to build an agent](./ai-agents/when-not-to-build-an-agent.md). → [Recap](./ai-agents/recap.md).
*Spokes:* `agentic-ai/what-is-an-agent`, `agentic-ai/planning-and-reasoning`,
`agentic-ai/reliability-and-evals`, `agentic-ai/agentic-ai-as-a-product`,
`tool-calling`, `memory-and-context`.

*Rescoping note:* this module had the most overlap of any module built so far. The
planned 7 lessons ("what an agent is," "the autonomy spectrum," "planning & reasoning,"
"tools & the environment," "memory & state across a run," "single-agent reliability,"
and "when not to build an agent") map almost one-to-one onto four existing, deeply
developed lessons in `agentic-ai/` — `what-is-an-agent.md` already covers the loop *and*
the autonomy spectrum as one of its own sections; `planning-and-reasoning.md` and
`reliability-and-evals.md` cover reasoning patterns and the compounding-error math in
full depth; and `agentic-ai-as-a-product.md` covers the build-or-not economics. Two of
the planned lessons (tools, memory) are also already the dedicated subject of this
family's own [Tool calling](./tool-calling/README.md) and
[Memory & context](./memory-and-context/README.md) modules, which would have made a
7-lesson AI agents module triple-duplicate itself against its own siblings. The module
compresses to the 3 lessons that survive after accounting for both the deeper agentic-ai
track and its sibling modules in this family, and adds no new glossary terms — every
core term (`agent-loop`, `autonomy-spectrum`, `compounding-error`, `supervised-cost`,
`reflection`) already exists and homes correctly to `agentic-ai/`.

### 8. 🔄 Agentic workflows — *2 lessons* — **BUILT** (rescoped from 6 → 2)
Orchestrating many steps and many agents.
1. [Orchestrating more than one agent](./agentic-workflows/orchestrating-more-than-one-agent.md) · 2. [Making a workflow durable, and worth owning](./agentic-workflows/making-a-workflow-durable-and-worth-owning.md). → [Recap](./agentic-workflows/recap.md).
*Spokes:* `agentic-ai/multi-agent-and-protocols`, `flowable/*`, `agentic-ai/agentic-ai-as-a-product`, `ai-agents`, `agentic-ai/safety-security-and-governance`.

*Rescoping note:* this module had the densest overlap of any module in the family —
denser even than AI agents. Of the planned 6 lessons, "workflows vs. agents" is already
the subject of `ai-agents/what-an-agent-is-and-how-much-autonomy-it-needs.md` (module 7,
this same family); "orchestration patterns" and "multi-agent systems & protocols" are
both already developed in full in `agentic-ai/multi-agent-and-protocols.md`;
"human-in-the-loop & approvals" is already covered by `agentic-ai-as-a-product.md`'s
agent-UX section and the `human-in-the-loop` glossary term, which homes to
`agentic-ai/safety-security-and-governance.md` — itself the future spoke for this
family's AI security & guardrails module; "durable execution" is the entire subject of
the twelve-phase `flowable/` track; and "workflow capture as product strategy" is
already a full section of, and an existing glossary term homed to,
`agentic-ai-as-a-product.md`. The module compresses to the 2 lessons that survive once
every sibling module and the deeper agentic-ai track are accounted for, and adds no new
glossary terms — `multi-agent`, `subagent`, `mcp`, `a2a`, `wait-state`, `job-executor`,
and `workflow-capture` all already exist and correctly home elsewhere.

### 9. 📊 Evaluation & observability — *2 lessons* — **BUILT** (rescoped from 7 → 2)
You cannot operate what you cannot measure.
1. [Why eval investment is the job](./evaluation-and-observability/why-eval-investment-is-the-job.md) · 2. [Building the eval stack in the right order](./evaluation-and-observability/building-the-eval-stack-in-the-right-order.md). → [Recap](./evaluation-and-observability/recap.md).
*Spokes:* `content/04-evals-observability/*`, `agentic-ai/reliability-and-evals`, `technical-product-management/tpm-for-ai-products`.

*Rescoping note:* this is the most exhaustively covered topic in the entire curriculum,
not just this family. `content/04-evals-observability/evals.md` and `observability.md`
already develop golden sets, regression tests, adversarial tests, LLM-as-judge, error
analysis (open and axial coding), traces, spans, and drift detection in complete
engineering depth, all in this same product-leader house style.
`agentic-ai/reliability-and-evals.md` already develops trajectory evals for agents in
full, and `technical-product-management/tpm-for-ai-products.md` already develops
eval-driven development as an operating discipline. Every core term the planned 7
lessons would have introduced — `eval`, `golden-set`, `llm-as-judge`, `error-analysis`,
`open-coding`, `axial-coding`, `trace`, `span`, `drift`, `trajectory-eval`,
`eval-driven-development` — is already a glossary entry homed to one of those four
sources. The module compresses to the 2 lessons that are genuinely new: the case for why
this investment is the job before a team feels ready for it, and the build order that
turns reading real traces into a full eval and observability practice without
over-building. No new glossary terms were added.

### 10. 🔐 AI security & guardrails — *2 lessons* — **BUILT** (rescoped from 7 → 2)
Keeping the system, its data, and its tenants safe.
1. [The threat model, and guardrails as architecture](./ai-security-and-guardrails/the-threat-model-and-guardrails.md) · 2. [Governance, audit & compliance](./ai-security-and-guardrails/governance-audit-and-compliance.md). → [Recap](./ai-security-and-guardrails/recap.md).
*Spokes:* `content/05-safety-multitenancy/*`, `agentic-ai/safety-security-and-governance`.

*Rescoping note:* this topic is as densely pre-covered as module 9 was, for the same
reason. `content/05-safety-multitenancy/safety-engineering.md` and
`multi-tenant-isolation.md` already develop prompt injection, the lethal trifecta, data
leakage prevention, permission boundaries, and cross-tenant isolation in full engineering
depth; `agentic-ai/safety-security-and-governance.md` already develops least privilege,
sandboxing, human-in-the-loop approval gates, audit trails, and organizational
governance (registry, identity, policy, accountable owner) in full. Every core term the
planned 7 lessons would have introduced for those topics — `prompt-injection`,
`lethal-trifecta`, `least-privilege`, `human-in-the-loop`, `multi-tenancy`,
`guardrail` — already exists and homes correctly to those sources. The module compresses
to the 2 lessons that are genuinely new: the full four-part threat taxonomy (jailbreak,
injection, extraction, poisoning — jailbreak specifically had no existing home) and
guardrails as a fail-closed architecture; and turning internal governance into external
compliance evidence (SOC 2, GDPR's automated-decision rules, the EU AI Act's risk tiers,
red-teaming, model cards — none of which existed anywhere in the curriculum before this
module). Four new glossary terms were added: `jailbreak`, `red-teaming`, `soc-2`,
`eu-ai-act`.

### 11. 💰 Cost optimization — *6 lessons*
Making the economics work.
1. Where AI cost comes from (tokens & inference) · 2. Cost attribution per feature, tenant & journey · 3. Model routing & the cheap path · 4. Caching (prompt & semantic) · 5. Controlling context & retrieval cost · 6. Unit economics & the supervised-cost view. → Recap.
*Spokes:* `content/04-evals-observability/cost-attribution`, `content/02-reliable-outputs/model-routing`, `content/01-inference-internals/prompt-vs-semantic-caching`, `agentic-ai/agentic-ai-as-a-product`.

**Total:** ~51 lessons + 11 READMEs + 11 recaps (module 5 rescoped from 6 to 4 lessons;
module 6 rescoped from 5 to 3 lessons; module 7 rescoped from 7 to 3 lessons; module 8
rescoped from 6 to 2 lessons; module 9 rescoped from 7 to 2 lessons).

## Cross-link discipline (hub-and-spoke)

- Each lesson stands alone for a product leader, then points to its **spoke** (an existing
  deep-dive lesson) with a one-line "go deeper" link — never re-deriving mechanics that
  already have a home.
- Existing spoke lessons get a **back-link** to the new module over time, so the graph is
  bidirectional. New modules are canonical *topic homes*; existing tracks keep their angle.
- Every new term added to the glossary follows `GLOSSARY_FRAMEWORK.md` and homes to a
  lesson in the family, so each new lesson gets its Key-terms box automatically.

## Build order after the pilot

Foundations (1 GenAI, 2 LLMs, 3 APIs) → Building blocks (4 RAG ✅, 5 Memory ✅, 6 Tools ✅)
→ Systems (7 Agents ✅, 8 Workflows ✅) → Operations (9 Evals ✅, 10 Security ✅, 11 Cost). Each
module ships complete (content + HTML + glossary + graph + Key-terms) before the next
begins.

## Wiring checklist per module (mirrors the existing tracks)

- [ ] `<slug>/` markdown: `README.md` (knowledge-graph opener) + lessons + `recap.md`.
- [ ] `scripts/build_<slug>.py` (thin wrapper around `build_standalone.build_track`).
- [ ] Register in `build_site.py` (HTML dir + copy + landing card), `build_graph.py`
      (`TRACKS` colour + `FLAT_TRACKS`), `check_links.py` (`SCAN_DIRS`).
- [ ] Glossary terms for the module's key concepts, homing to its lessons.
- [ ] `README.md` family table + `SUMMARY.md` learning path.
- [ ] Build, `check_links.py`, mermaid validate, headless-verify, ship.
