# Learning path

This is the recommended order. Each lesson links forward to what builds on it and
sideways to what it connects with. You can read top-to-bottom, or follow the
**threads** at the bottom across module boundaries.

---

## Module 00 — [Foundations](./content/00-foundations/README.md)

1. [Harness engineering, not just prompt engineering](./content/00-foundations/harness-engineering.md)
2. [Context engineering, not just long prompts](./content/00-foundations/context-engineering.md)
3. [Shipping LLM systems as infrastructure, not demos](./content/00-foundations/infra-not-demos.md)

## Module 01 — [Inference internals](./content/01-inference-internals/README.md)

4. [Prompt caching vs. semantic caching](./content/01-inference-internals/prompt-vs-semantic-caching.md)
5. [KV cache management: eviction, reuse, memory pressure](./content/01-inference-internals/kv-cache-management.md)
6. [Prefill vs. decode latency](./content/01-inference-internals/prefill-vs-decode.md)
7. [Continuous batching & paged attention](./content/01-inference-internals/batching-and-paged-attention.md)
8. [Speculative decoding vs. quantization vs. distillation](./content/01-inference-internals/speculative-quantization-distillation.md)
9. [Quantization formats: INT8, INT4, FP8, AWQ, GPTQ](./content/01-inference-internals/quantization-formats.md)

## Module 02 — [Reliable outputs & tool use](./content/02-reliable-outputs/README.md)

10. [Structured output: validation, repair loops, fallback chains](./content/02-reliable-outputs/structured-output.md)
11. [Function calling reliability, tool contracts, idempotency](./content/02-reliable-outputs/function-calling.md)
12. [Agent guardrails: loop budgets, tool budgets, termination](./content/02-reliable-outputs/agent-guardrails.md)
13. [Model routing, fallback logic, degraded-mode UX](./content/02-reliable-outputs/model-routing.md)

## Module 03 — [RAG & retrieval](./content/03-rag/README.md)

14. [RAG architecture: chunking, embeddings, hybrid search, reranking, freshness](./content/03-rag/rag-architecture.md)
15. [Retrieval evals: recall, precision, grounding, attribution, citations](./content/03-rag/retrieval-evals.md)

## Module 04 — [Evals & observability](./content/04-evals-observability/README.md)

16. [Evals: golden sets, regression, adversarial, LLM-as-judge, human](./content/04-evals-observability/evals.md)
17. [LLM observability: traces, spans, tokens, latency, errors, drift](./content/04-evals-observability/observability.md)
18. [Cost attribution per feature, workflow, tenant, journey](./content/04-evals-observability/cost-attribution.md)

## Module 05 — [Safety & multi-tenancy](./content/05-safety-multitenancy/README.md)

19. [Safety engineering: prompt injection, data leakage, permission boundaries](./content/05-safety-multitenancy/safety-engineering.md)
20. [Multi-tenant isolation & cache contamination prevention](./content/05-safety-multitenancy/multi-tenant-isolation.md)

## Module 06 — [Strategy & tradeoffs](./content/06-strategy-tradeoffs/README.md)

21. [Fine-tuning vs. in-context learning vs. RAG vs. distillation](./content/06-strategy-tradeoffs/finetune-vs-icl-vs-rag.md)
22. [Latency, quality, cost & reliability across the inference stack](./content/06-strategy-tradeoffs/inference-stack-tradeoffs.md)
23. [Production failure modes & how to engineer around them](./content/06-strategy-tradeoffs/production-failure-modes.md)

---

## Threads (cross-module reading paths)

Follow a single concern through the whole stack:

- **The caching thread** —
  [Prompt vs. semantic caching](./content/01-inference-internals/prompt-vs-semantic-caching.md) →
  [KV cache management](./content/01-inference-internals/kv-cache-management.md) →
  [Multi-tenant isolation](./content/05-safety-multitenancy/multi-tenant-isolation.md) →
  [Cost attribution](./content/04-evals-observability/cost-attribution.md)

- **The reliability thread** —
  [Structured output](./content/02-reliable-outputs/structured-output.md) →
  [Function calling](./content/02-reliable-outputs/function-calling.md) →
  [Agent guardrails](./content/02-reliable-outputs/agent-guardrails.md) →
  [Production failure modes](./content/06-strategy-tradeoffs/production-failure-modes.md)

- **The latency thread** —
  [Prefill vs. decode](./content/01-inference-internals/prefill-vs-decode.md) →
  [Continuous batching & paged attention](./content/01-inference-internals/batching-and-paged-attention.md) →
  [Speculative decoding & quantization](./content/01-inference-internals/speculative-quantization-distillation.md) →
  [Stack tradeoffs](./content/06-strategy-tradeoffs/inference-stack-tradeoffs.md)

- **The quality thread** —
  [Context engineering](./content/00-foundations/context-engineering.md) →
  [RAG architecture](./content/03-rag/rag-architecture.md) →
  [Retrieval evals](./content/03-rag/retrieval-evals.md) →
  [Evals](./content/04-evals-observability/evals.md)

- **The "which tool" thread** —
  [Fine-tuning vs. ICL vs. RAG vs. distillation](./content/06-strategy-tradeoffs/finetune-vs-icl-vs-rag.md) →
  [RAG architecture](./content/03-rag/rag-architecture.md) →
  [Model routing](./content/02-reliable-outputs/model-routing.md)

---

# Part II — The craft tracks

Standalone tracks in the same house style. Each is self-contained; the recommended
order below moves from thinking skills to product craft to agents.

## [First principles & the polymath mind](./first-principles/README.md)

1. [What first-principles thinking actually is](./first-principles/what-is-first-principles.md)
2. [The method: deconstruct, challenge, reconstruct](./first-principles/the-method.md)
3. [A latticework of mental models](./first-principles/mental-models-latticework.md)
4. [Becoming a polymath](./first-principles/becoming-a-polymath.md)
5. [Learning how to learn](./first-principles/learning-how-to-learn.md)
6. [Traps & limits](./first-principles/traps-and-limits.md) · [Recap](./first-principles/recap.md)

## [Product sense](./product-sense/README.md)

1. [Motivation & behaviour](./product-sense/motivation-and-behaviour.md)
2. [Cognitive empathy](./product-sense/cognitive-empathy.md)
3. [User research](./product-sense/user-research.md)
4. [Creativity: strategy & execution](./product-sense/creativity.md)
5. [Communication](./product-sense/communication.md)
6. [Domain expertise](./product-sense/domain-expertise.md)
7. [Product sense for AI products](./product-sense/product-sense-for-ai.md) · [Recap](./product-sense/recap.md)

## [Technical product sense](./technical-product-sense/README.md)

1. [How systems are built](./technical-product-sense/how-systems-are-built.md)
2. [APIs & contracts](./technical-product-sense/apis-and-contracts.md)
3. [Data & the data model](./technical-product-sense/data-and-the-data-model.md)
4. [Latency, scale & performance](./technical-product-sense/latency-scale-performance.md)
5. [Reliability & failure](./technical-product-sense/reliability-and-failure.md)
6. [Tech debt & estimation](./technical-product-sense/tech-debt-and-estimation.md)
7. [Security & privacy sense](./technical-product-sense/security-and-privacy.md)
8. [The economics of infrastructure](./technical-product-sense/economics-of-infrastructure.md)
9. [Technical sense for AI systems](./technical-product-sense/technical-sense-for-ai.md) · [Recap](./technical-product-sense/recap.md)

## [Technical product management](./technical-product-management/README.md)

1. [The technical PM role](./technical-product-management/the-technical-pm-role.md)
2. [Discovery to delivery](./technical-product-management/discovery-to-delivery.md)
3. [Specs, PRDs & RFCs](./technical-product-management/specs-prds-and-rfcs.md)
4. [Prioritization & roadmaps](./technical-product-management/prioritization-and-roadmaps.md)
5. [Working with engineering](./technical-product-management/working-with-engineering.md)
6. [Metrics & experimentation](./technical-product-management/metrics-and-experimentation.md)
7. [Launches, rollouts & migrations](./technical-product-management/launches-rollouts-and-migrations.md)
8. [Incidents & postmortems](./technical-product-management/incidents-and-postmortems.md)
9. [TPM for AI products](./technical-product-management/tpm-for-ai-products.md) · [Recap](./technical-product-management/recap.md)

## [Agentic AI](./agentic-ai/README.md)

1. [What is an agent?](./agentic-ai/what-is-an-agent.md)
2. [Tools & function calling](./agentic-ai/tools-and-function-calling.md)
3. [Context & memory](./agentic-ai/context-and-memory.md)
4. [Planning & reasoning](./agentic-ai/planning-and-reasoning.md)
5. [Multi-agent systems & protocols](./agentic-ai/multi-agent-and-protocols.md)
6. [Reliability & evals](./agentic-ai/reliability-and-evals.md)
7. [Safety, security & governance](./agentic-ai/safety-security-and-governance.md)
8. [Agentic AI as a product](./agentic-ai/agentic-ai-as-a-product.md) · [Recap](./agentic-ai/recap.md)

## [Harness engineering](./harness-engineering/README.md)

The hands-on build track: construct a coding agent's harness phase by phase. Start with
the [roadmap](./harness-engineering/ROADMAP.md).
