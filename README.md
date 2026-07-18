<div align="center">

<img src="./assets/banner.svg" alt="AI Engineering — From Scratch to Production" width="100%" />

<br/>

![Tracks](https://img.shields.io/badge/tracks-7-D97757?style=flat-square&labelColor=1f1e1d)
![Lessons](https://img.shields.io/badge/lessons-58%2B-D97757?style=flat-square&labelColor=1f1e1d)
![Audience](https://img.shields.io/badge/for-Senior%20%26%20Principal%20PMs-1f1e1d?style=flat-square)
![Cross-links](https://img.shields.io/badge/internal%20links-1832%20verified-2e7d32?style=flat-square&labelColor=1f1e1d)
![License](https://img.shields.io/badge/license-educational-6b6a64?style=flat-square&labelColor=1f1e1d)

**[🌐 Live site](https://aakashagg123.github.io/gatsby/)** · **[📚 Learning path](./SUMMARY.md)** · **[📖 Glossary](./GLOSSARY.md)** · **[🎨 HTML editions](./html/index.html)** · **[🧭 Jump to modules](#-curriculum-map)** · **[🧵 Craft tracks](#-beyond-ai-engineering--the-craft-tracks)**

</div>

---

> **This is a curriculum for the product leaders who own AI features — not just the engineers who build them.**
> It teaches the engineering discipline underneath production LLM systems — inference, retrieval, evaluation, observability, safety, and cost — through the lens of the decisions a **Senior or Principal PM** has to make. Every lesson pairs the real mechanics with a **🎯 For the AI-native PM** briefing: why it matters to the product, what it changes in your decisions, the sharp question to ask your eng team, and the product risk if you ignore it.

<br/>

## 👤 Who this is for

<table>
<tr>
<td width="33%" valign="top">

### 🧭 The AI-native PM
You own an AI feature and keep hitting the gap between an impressive demo and something you can actually ship, price, and stand behind. You want to **lead the conversation**, not nod along in it.

</td>
<td width="33%" valign="top">

### 🏗️ The Principal scoping a bet
You're deciding fine-tune vs. RAG, build vs. buy, what to put in the SLA, and what "AI quality" even means on the roadmap. You need the **tradeoffs and their costs**, named plainly.

</td>
<td width="33%" valign="top">

### ⚙️ The engineer who wants the map
You know the pieces but want them connected — caching to isolation, prefill to cost, evals to drift — as **one discipline**, with the failure modes that tie them together.

</td>
</tr>
</table>

> If you've ever had a JSON parse error take down a workflow, a retrieval index go quietly stale, an agent loop run up a bill, or a cache serve one customer's data to another — this curriculum is the prevention you wish had been on the roadmap.

<br/>

## 🗺️ Curriculum map

Each module is a folder of cross-linked markdown, readable directly on GitHub. Prefer a designed reading experience? Every module also ships as a **[beautified HTML edition](./html/index.html)**.

<table>
<tr>
<td width="50%" valign="top">

### [`00` · Foundations](./content/00-foundations/README.md)
*The mindset shift from "writing prompts" to "engineering systems."*

- [Harness engineering, not just prompt engineering](./content/00-foundations/harness-engineering.md)
- [Context engineering, not just long prompts](./content/00-foundations/context-engineering.md)
- [Shipping LLM systems as infrastructure, not demos](./content/00-foundations/infra-not-demos.md)

</td>
<td width="50%" valign="top">

### [`01` · Inference internals](./content/01-inference-internals/README.md)
*What happens between your request and the tokens that come back.*

- [Prompt caching vs. semantic caching](./content/01-inference-internals/prompt-vs-semantic-caching.md)
- [KV cache: eviction, reuse, memory pressure](./content/01-inference-internals/kv-cache-management.md)
- [Prefill vs. decode latency](./content/01-inference-internals/prefill-vs-decode.md)
- [Continuous batching & paged attention](./content/01-inference-internals/batching-and-paged-attention.md)
- [Speculative decoding vs. quant vs. distillation](./content/01-inference-internals/speculative-quantization-distillation.md)
- [Quantization formats: INT8/INT4/FP8/AWQ/GPTQ](./content/01-inference-internals/quantization-formats.md)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [`02` · Reliable outputs & tool use](./content/02-reliable-outputs/README.md)
*Making models produce things downstream systems can trust.*

- [Structured output: validation, repair, fallback](./content/02-reliable-outputs/structured-output.md)
- [Function calling, tool contracts, idempotency](./content/02-reliable-outputs/function-calling.md)
- [Agent guardrails: loop, tool & token budgets](./content/02-reliable-outputs/agent-guardrails.md)
- [Model routing & degraded-mode UX](./content/02-reliable-outputs/model-routing.md)

</td>
<td width="50%" valign="top">

### [`03` · RAG & retrieval](./content/03-rag/README.md)
*Grounding models in your data — and proving they used it.*

- [RAG architecture: chunking → reranking → freshness](./content/03-rag/rag-architecture.md)
- [Retrieval evals: recall, grounding, citations](./content/03-rag/retrieval-evals.md)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [`04` · Evals & observability](./content/04-evals-observability/README.md)
*You cannot operate what you cannot measure.*

- [Evals: golden sets, adversarial, LLM-as-judge](./content/04-evals-observability/evals.md)
- [Observability: traces, tokens, latency, drift](./content/04-evals-observability/observability.md)
- [Cost attribution per feature, tenant & journey](./content/04-evals-observability/cost-attribution.md)

</td>
<td width="50%" valign="top">

### [`05` · Safety & multi-tenancy](./content/05-safety-multitenancy/README.md)
*Keeping tenants, users, and data out of each other.*

- [Safety: injection, leakage, permission boundaries](./content/05-safety-multitenancy/safety-engineering.md)
- [Multi-tenant isolation & cache contamination](./content/05-safety-multitenancy/multi-tenant-isolation.md)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [`06` · Strategy & tradeoffs](./content/06-strategy-tradeoffs/README.md)
*Picking the right tool, and naming the cost of every choice.*

- [Fine-tuning vs. ICL vs. RAG vs. distillation](./content/06-strategy-tradeoffs/finetune-vs-icl-vs-rag.md)
- [Latency / quality / cost / reliability tradeoffs](./content/06-strategy-tradeoffs/inference-stack-tradeoffs.md)
- [Production failure modes & how to prevent them](./content/06-strategy-tradeoffs/production-failure-modes.md)

</td>
<td width="50%" valign="top">

### 🎨 [HTML editions](./html/index.html)
*The same curriculum, in a designed reading experience.*

- One comprehensive page **per module**, styled in a warm, Anthropic-inspired UX.
- Open `html/index.html` locally, or host the folder.
- Built from the markdown — always in sync.

</td>
</tr>
</table>

<br/>

## 🧭 Beyond AI Engineering — the craft tracks

The AI Engineering modules above teach the *stack*. Six further tracks teach the *craft*
around it — each a standalone folder of cross-linked lessons in the same house style
(TL;DR → 🎯 briefing → mechanics → failure modes → checklist), each with a rendered HTML
edition on the [live site](https://aakashagg123.github.io/gatsby/).

| Track | What it teaches | Start here |
| :-- | :-- | :-- |
| [**Agentic AI**](./agentic-ai/README.md) | What agents actually are — the loop, tools, memory, planning — and the reliability, security, and economics that turn demos into products. Opens with a knowledge graph. | [What is an agent?](./agentic-ai/what-is-an-agent.md) |
| [**Harness engineering**](./harness-engineering/README.md) | Build a coding agent's harness from scratch — loop, tools, context, memory, evals — phase by phase, hands-on. | [Roadmap](./harness-engineering/ROADMAP.md) |
| [**Product sense**](./product-sense/README.md) | The five habits under great product judgment — behaviour, empathy, strategy, communication, domain — and how they bend for AI products. | [Motivation & behaviour](./product-sense/motivation-and-behaviour.md) |
| [**Technical product sense**](./technical-product-sense/README.md) | How systems are actually built — request paths, APIs, data, latency, reliability, tech debt — at the altitude a PM needs to lead technical conversations. | [How systems are built](./technical-product-sense/how-systems-are-built.md) |
| [**Technical product management**](./technical-product-management/README.md) | The operating craft: discovery, specs, prioritization, working with engineering, metrics, launches — and the AI-products capstone. | [The technical PM role](./technical-product-management/the-technical-pm-role.md) |
| [**First principles & the polymath mind**](./first-principles/README.md) | Reasoning from fundamentals instead of by analogy, and building the mental-model range to do it well. | [What first-principles thinking is](./first-principles/what-is-first-principles.md) |

<br/>

## 🧩 How each lesson is built

Every lesson follows the same shape, so you always know where to look:

| Section | What it gives you |
| :-- | :-- |
| **TL;DR** | The one-paragraph version. |
| 🎯 **For the AI-native PM** | Why it matters · what it changes in your decisions · the question to ask eng · the product risk if ignored. |
| **Mental model → Mechanics** | How to think about it, then how it actually works. |
| **Tradeoffs & decisions** | When to use what, and the cost of each choice. |
| **Failure modes** | How it breaks in production. |
| **Practitioner checklist** | What to verify before you ship. |
| **Related lessons** | Cross-links — the *linked* part of this repository. |

<br/>

## 🧵 Threads — follow one concern across the whole stack

The modules are ordered, but the real value is in the cross-links. Pull any thread:

- **💰 Caching & cost** — [Prompt vs. semantic caching](./content/01-inference-internals/prompt-vs-semantic-caching.md) → [KV cache](./content/01-inference-internals/kv-cache-management.md) → [Multi-tenant cache safety](./content/05-safety-multitenancy/multi-tenant-isolation.md) → [Cost attribution](./content/04-evals-observability/cost-attribution.md)
- **🛡️ Reliability** — [Structured output](./content/02-reliable-outputs/structured-output.md) → [Function calling](./content/02-reliable-outputs/function-calling.md) → [Agent guardrails](./content/02-reliable-outputs/agent-guardrails.md) → [Production failure modes](./content/06-strategy-tradeoffs/production-failure-modes.md)
- **⚡ Latency** — [Prefill vs. decode](./content/01-inference-internals/prefill-vs-decode.md) → [Batching & paged attention](./content/01-inference-internals/batching-and-paged-attention.md) → [Speculative decoding & quantization](./content/01-inference-internals/speculative-quantization-distillation.md) → [Stack tradeoffs](./content/06-strategy-tradeoffs/inference-stack-tradeoffs.md)
- **🎯 Quality** — [Context engineering](./content/00-foundations/context-engineering.md) → [RAG architecture](./content/03-rag/rag-architecture.md) → [Retrieval evals](./content/03-rag/retrieval-evals.md) → [Evals](./content/04-evals-observability/evals.md)
- **🧰 Which tool?** — [Fine-tune vs. ICL vs. RAG vs. distillation](./content/06-strategy-tradeoffs/finetune-vs-icl-vs-rag.md) → [RAG architecture](./content/03-rag/rag-architecture.md) → [Model routing](./content/02-reliable-outputs/model-routing.md)

<br/>

## 🚀 Where to start

<table>
<tr>
<td valign="top"><strong>New to the stack?</strong></td>
<td>Read <a href="./content/00-foundations/README.md">Foundations</a> top to bottom, then follow the <a href="./SUMMARY.md">learning path</a>.</td>
</tr>
<tr>
<td valign="top"><strong>Scoping a specific bet?</strong></td>
<td>Jump to <a href="./content/06-strategy-tradeoffs/finetune-vs-icl-vs-rag.md">Fine-tune vs. ICL vs. RAG vs. distillation</a> and the <a href="./content/06-strategy-tradeoffs/inference-stack-tradeoffs.md">tradeoffs map</a>.</td>
</tr>
<tr>
<td valign="top"><strong>Prepping a launch review?</strong></td>
<td>Use <a href="./content/06-strategy-tradeoffs/production-failure-modes.md">Production failure modes</a> as your pre-launch checklist.</td>
</tr>
<tr>
<td valign="top"><strong>Want the glossary first?</strong></td>
<td>Skim the <a href="./GLOSSARY.md">Glossary</a> — every term links to where it's developed.</td>
</tr>
</table>

<br/>

---

<details>
<summary><strong>🛠️ Project scaffold &amp; HTML build</strong></summary>

<br/>

The learning material lives entirely in [`content/`](./content/) as plain markdown — no build step required to read it.

- **HTML editions** are generated into [`html/`](./html/) from the markdown by [`scripts/build_html.py`](./scripts/build_html.py), so they never drift from the source. Regenerate with `python3 scripts/build_html.py`.
- The repository also retains its original [Gatsby](https://www.gatsbyjs.org/) scaffold, so the content can later be rendered as a full site.

</details>

<div align="center">
<br/>
<sub>Educational content. Use it, fork it, teach from it.</sub>
</div>
