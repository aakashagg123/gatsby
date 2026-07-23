# Module 02 · Reliable outputs & tool use

A model that is right 95% of the time will break a workflow that calls it a hundred
times. This module is about closing that gap — turning a stochastic text generator
into a component whose outputs and actions downstream systems can *trust*.

- [**Structured output**](./structured-output.md) — getting valid, schema-conformant
  data out, with validation, repair loops, and fallback chains for when you don't.
- [**Function calling**](./function-calling.md) — reliable tool invocation: contracts,
  argument validation, and idempotency so retries are safe.
- [**Agent guardrails**](./agent-guardrails.md) — loop budgets, tool budgets, and
  termination conditions so an agent can't run away.
- [**Model routing**](./model-routing.md) — choosing models per request and degrading
  gracefully instead of failing hard.

The throughline: **never trust model output as if it were a typed return value.**
Treat it as untrusted input to be validated, bounded, and made safe to act on. This
is the [harness](../00-foundations/harness-engineering.md) doing its job.


## Connects to other tracks

- [Tools & function calling](../../agentic-ai/tools-and-function-calling.md) — the agent's view of the same tool contracts.
- [Tool engineering in the harness](../../harness-engineering/phases/03-tool-engineering/README.md) — building reliable tools by hand.
- [Service integration & error handling (Flowable)](../../flowable/phases/04-service-integration-and-error-handling/README.md) — the same idempotency and retry discipline in a process engine.

**📌 Close out the module:** [Recap & real-world examples](./recap.md) — war stories from production plus the key takeaways.

---

← Previous: [01 · Inference Internals](../01-inference-internals/README.md) ·
→ Next: [03 · RAG & Retrieval](../03-rag/README.md)
