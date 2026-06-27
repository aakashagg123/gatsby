# AI Engineering — From Scratch to Production

A **linked learning repository** for engineers who want to ship LLM systems as
**reliable infrastructure**, not demos wrapped around prompts.

This is not a prompt-engineering tutorial. It is a curriculum about the
*engineering discipline* underneath production AI systems: the inference stack,
retrieval, evaluation, observability, safety, cost, and the tradeoffs that
connect them.

> Inspired by the topic list at [aiengineeringfromscratch.com](https://aiengineeringfromscratch.com)

---

## How to use this repository

Every lesson is a self-contained markdown file that follows the same shape:

- **TL;DR** — the one-paragraph version.
- **Mental model** — how to think about the topic.
- **Mechanics** — how it actually works.
- **Tradeoffs & decisions** — when to use what, and the cost of each choice.
- **Failure modes** — how it breaks in production.
- **Practitioner checklist** — what to verify before you ship.
- **Related lessons** — cross-links to connected ideas (this is the *linked* part).

The modules are ordered, but the cross-links mean you can also follow a thread —
e.g. *caching → KV cache → multi-tenant cache safety → prompt injection* — across
module boundaries.

Start with the [**learning path in SUMMARY.md**](./SUMMARY.md) or jump straight to
a module below. Unfamiliar terms are defined in the [**Glossary**](./GLOSSARY.md).

---

## Curriculum map

### [00 · Foundations](./content/00-foundations/README.md)
The mindset shift from "writing prompts" to "engineering systems."
- [Harness engineering, not just prompt engineering](./content/00-foundations/harness-engineering.md)
- [Context engineering, not just long prompts](./content/00-foundations/context-engineering.md)
- [Shipping LLM systems as infrastructure, not demos](./content/00-foundations/infra-not-demos.md)

### [01 · Inference Internals](./content/01-inference-internals/README.md)
What happens between your request and the tokens that come back.
- [Prompt caching vs. semantic caching](./content/01-inference-internals/prompt-vs-semantic-caching.md)
- [KV cache management: eviction, reuse, and memory pressure](./content/01-inference-internals/kv-cache-management.md)
- [Prefill vs. decode latency](./content/01-inference-internals/prefill-vs-decode.md)
- [Continuous batching & paged attention](./content/01-inference-internals/batching-and-paged-attention.md)
- [Speculative decoding vs. quantization vs. distillation](./content/01-inference-internals/speculative-quantization-distillation.md)
- [Quantization formats: INT8, INT4, FP8, AWQ, GPTQ](./content/01-inference-internals/quantization-formats.md)

### [02 · Reliable Outputs & Tool Use](./content/02-reliable-outputs/README.md)
Making models produce things downstream systems can trust.
- [Structured output: validation, repair loops, fallback chains](./content/02-reliable-outputs/structured-output.md)
- [Function calling reliability, tool contracts, and idempotency](./content/02-reliable-outputs/function-calling.md)
- [Agent guardrails: loop budgets, tool budgets, termination](./content/02-reliable-outputs/agent-guardrails.md)
- [Model routing, fallback logic, and degraded-mode UX](./content/02-reliable-outputs/model-routing.md)

### [03 · RAG & Retrieval](./content/03-rag/README.md)
Grounding models in your data — and proving they actually used it.
- [RAG architecture: chunking, embeddings, hybrid search, reranking, freshness](./content/03-rag/rag-architecture.md)
- [Retrieval evals: recall, precision, grounding, attribution, citations](./content/03-rag/retrieval-evals.md)

### [04 · Evals & Observability](./content/04-evals-observability/README.md)
You cannot operate what you cannot measure.
- [Evals: golden sets, regression, adversarial, LLM-as-judge, human](./content/04-evals-observability/evals.md)
- [LLM observability: traces, spans, tokens, latency, errors, drift](./content/04-evals-observability/observability.md)
- [Cost attribution per feature, workflow, tenant, and journey](./content/04-evals-observability/cost-attribution.md)

### [05 · Safety & Multi-tenancy](./content/05-safety-multitenancy/README.md)
Keeping tenants, users, and data from leaking into each other.
- [Safety engineering: prompt injection, data leakage, permission boundaries](./content/05-safety-multitenancy/safety-engineering.md)
- [Multi-tenant isolation and cache contamination prevention](./content/05-safety-multitenancy/multi-tenant-isolation.md)

### [06 · Strategy & Tradeoffs](./content/06-strategy-tradeoffs/README.md)
Picking the right tool, and naming the cost of every choice.
- [Fine-tuning vs. in-context learning vs. RAG vs. distillation](./content/06-strategy-tradeoffs/finetune-vs-icl-vs-rag.md)
- [Latency, quality, cost & reliability across the inference stack](./content/06-strategy-tradeoffs/inference-stack-tradeoffs.md)
- [Production failure modes & how to engineer around them](./content/06-strategy-tradeoffs/production-failure-modes.md)

---

## Who this is for

Engineers building LLM features who keep hitting the gap between "works in the
notebook" and "works for 10,000 tenants at p99." If you have ever had a JSON
parse error take down a workflow, a retrieval index quietly go stale, an agent
loop run up a bill, or a cache serve one user's data to another — this is for you.

---

## Project scaffold

The repository ships as a [Gatsby](https://www.gatsbyjs.org/) site so the content
can later be rendered as a browsable learning site. The learning material itself
lives entirely in [`content/`](./content/) as plain markdown and is readable
directly on GitHub — no build step required. See [`SUMMARY.md`](./SUMMARY.md) for
the full table of contents.

## License

Educational content. Use it, fork it, teach from it.
