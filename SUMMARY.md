# Learning Path

This is the recommended order. Each lesson links forward to what builds on it and
sideways to what it connects with. You can read top-to-bottom, or follow the
**threads** at the bottom across module boundaries.

---

## Module 00 — [Foundations](./content/00-foundations/README.md)

1. [Harness engineering, not just prompt engineering](./content/00-foundations/harness-engineering.md)
2. [Context engineering, not just long prompts](./content/00-foundations/context-engineering.md)
3. [Shipping LLM systems as infrastructure, not demos](./content/00-foundations/infra-not-demos.md)

## Module 01 — [Inference Internals](./content/01-inference-internals/README.md)

4. [Prompt caching vs. semantic caching](./content/01-inference-internals/prompt-vs-semantic-caching.md)
5. [KV cache management: eviction, reuse, memory pressure](./content/01-inference-internals/kv-cache-management.md)
6. [Prefill vs. decode latency](./content/01-inference-internals/prefill-vs-decode.md)
7. [Continuous batching & paged attention](./content/01-inference-internals/batching-and-paged-attention.md)
8. [Speculative decoding vs. quantization vs. distillation](./content/01-inference-internals/speculative-quantization-distillation.md)
9. [Quantization formats: INT8, INT4, FP8, AWQ, GPTQ](./content/01-inference-internals/quantization-formats.md)

## Module 02 — [Reliable Outputs & Tool Use](./content/02-reliable-outputs/README.md)

10. [Structured output: validation, repair loops, fallback chains](./content/02-reliable-outputs/structured-output.md)
11. [Function calling reliability, tool contracts, idempotency](./content/02-reliable-outputs/function-calling.md)
12. [Agent guardrails: loop budgets, tool budgets, termination](./content/02-reliable-outputs/agent-guardrails.md)
13. [Model routing, fallback logic, degraded-mode UX](./content/02-reliable-outputs/model-routing.md)

## Module 03 — [RAG & Retrieval](./content/03-rag/README.md)

14. [RAG architecture: chunking, embeddings, hybrid search, reranking, freshness](./content/03-rag/rag-architecture.md)
15. [Retrieval evals: recall, precision, grounding, attribution, citations](./content/03-rag/retrieval-evals.md)

## Module 04 — [Evals & Observability](./content/04-evals-observability/README.md)

16. [Evals: golden sets, regression, adversarial, LLM-as-judge, human](./content/04-evals-observability/evals.md)
17. [LLM observability: traces, spans, tokens, latency, errors, drift](./content/04-evals-observability/observability.md)
18. [Cost attribution per feature, workflow, tenant, journey](./content/04-evals-observability/cost-attribution.md)

## Module 05 — [Safety & Multi-tenancy](./content/05-safety-multitenancy/README.md)

19. [Safety engineering: prompt injection, data leakage, permission boundaries](./content/05-safety-multitenancy/safety-engineering.md)
20. [Multi-tenant isolation & cache contamination prevention](./content/05-safety-multitenancy/multi-tenant-isolation.md)

## Module 06 — [Strategy & Tradeoffs](./content/06-strategy-tradeoffs/README.md)

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
