# Module 04 · Evals & Observability

LLM systems fail *silently*: a wrong answer looks exactly like a right one, and quality
can regress with no code change at all (a model update, a data shift, an aging index).
The only defense is measurement — before you ship (evals) and while you run
(observability) — plus knowing what it all costs.

- [**Evals**](./evals.md) — golden sets, regression tests, adversarial tests,
  LLM-as-judge, and human evals. How you know it's *correct*.
- [**Observability**](./observability.md) — traces, spans, tokens, latency, errors, and
  drift. How you know it's *working* in production.
- [**Cost attribution**](./cost-attribution.md) — per feature, workflow, tenant, and
  journey. How you know what it's *costing* and who's paying.

This module is the backbone the rest of the curriculum leans on: every "validate before
shipping" in [reliable outputs](../02-reliable-outputs/README.md), every "measure
retrieval" in [RAG](../03-rag/README.md), and every quality claim about
[quantization](../01-inference-internals/quantization-formats.md) ultimately routes
through here.


**📌 Close out the module:** [Recap & real-world examples](./recap.md) — war stories from production plus the key takeaways.

---

← Previous: [03 · RAG & Retrieval](../03-rag/README.md) ·
→ Next: [05 · Safety & Multi-tenancy](../05-safety-multitenancy/README.md)
