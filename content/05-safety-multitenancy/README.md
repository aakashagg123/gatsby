# Module 05 · Safety & multi-tenancy

LLM systems take in untrusted text and produce actions over privileged data — often for
many customers sharing the same infrastructure. That combination creates failure modes
that don't exist in classic apps: instructions hidden in your *data* can hijack
behavior, and shared caches or context can leak one customer into another.

- [**Safety engineering**](./safety-engineering.md) — prompt-injection defense, data
  leakage prevention, and permission boundaries. Treat model output as untrusted and
  enforce authority outside the model.
- [**Multi-tenant isolation**](./multi-tenant-isolation.md) — keeping tenants, users,
  and their data from contaminating each other through caches, context, and retrieval.

These build directly on [function calling](../02-reliable-outputs/function-calling.md)
(authority lives in tools, not prompts), [caching](../01-inference-internals/prompt-vs-semantic-caching.md)
(shared computation must respect trust boundaries), and [RAG](../03-rag/rag-architecture.md)
(retrieval must be scoped). Safety is not a feature you add at the end — it's a property
of how the whole [harness](../00-foundations/harness-engineering.md) is built.


## Connects to other tracks

- [Safety, security & governance for agents](../../agentic-ai/safety-security-and-governance.md) — the agent-layer view of injection and permissions.
- [Security & alignment in the harness](../../harness-engineering/phases/17-security-and-alignment/README.md) — tenant isolation and gating, built by hand.
- [Security & privacy sense](../../technical-product-sense/security-and-privacy.md) — the "what does the attacker hold tomorrow?" frame.

**📌 Close out the module:** [Recap & real-world examples](./recap.md) — war stories from production plus the key takeaways.

---

← Previous: [04 · Evals & Observability](../04-evals-observability/README.md) ·
→ Next: [06 · Strategy & Tradeoffs](../06-strategy-tradeoffs/README.md)
