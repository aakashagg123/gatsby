# Module 01 · Inference Internals

You can't make good latency, cost, and reliability decisions without knowing what
actually happens when a model serves a request. This module opens the box.

Two phases, one cache, and a handful of throughput and compression techniques
explain almost everything about LLM serving economics:

- [**Prompt caching vs. semantic caching**](./prompt-vs-semantic-caching.md) — two
  completely different things that share a word.
- [**KV cache management**](./kv-cache-management.md) — the data structure that makes
  generation fast, and the memory pressure it creates at scale.
- [**Prefill vs. decode latency**](./prefill-vs-decode.md) — why the two phases are
  bottlenecked by different hardware limits and optimized differently.
- [**Continuous batching & paged attention**](./batching-and-paged-attention.md) —
  how modern servers hit high throughput without wrecking latency.
- [**Speculative decoding vs. quantization vs. distillation**](./speculative-quantization-distillation.md)
  — three ways to go faster/cheaper, with different risk profiles.
- [**Quantization formats**](./quantization-formats.md) — INT8, INT4, FP8, AWQ, GPTQ,
  and when compression starts hurting quality.

Everything here feeds the cross-stack tradeoff reasoning in
[Module 06](../06-strategy-tradeoffs/inference-stack-tradeoffs.md).


**📌 Close out the module:** [Recap & real-world examples](./recap.md) — war stories from production plus the key takeaways.

---

← Previous: [00 · Foundations](../00-foundations/README.md) ·
→ Next: [02 · Reliable Outputs](../02-reliable-outputs/README.md)
