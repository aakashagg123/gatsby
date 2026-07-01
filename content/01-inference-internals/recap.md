# Inference internals — recap & real-world examples

*Part of [01 · Inference Internals](./README.md)*

## Real-world examples & war stories

**PagedAttention / vLLM (UC Berkeley, 2023).** By managing the
[KV cache](./kv-cache-management.md) in non-contiguous "pages" instead of one big
reserved block, the PagedAttention paper reported up to **~24× higher throughput** than
prior serving systems at the same latency. vLLM became a default open-source serving
engine on the strength of it. 🎯 *PM takeaway:* the same GPU can serve far more traffic —
your **$/token and gross margin** are an engineering choice, not a fixed input. See
[batching & paged attention](./batching-and-paged-attention.md).

**Prompt caching goes mainstream (2024).** Anthropic, OpenAI, and Google all shipped
prefix/prompt caching that can cut the cost of the *cached* input by up to **~90%** and
reduce time-to-first-token — but only when your prompt prefix is byte-stable. 🎯 *PM
takeaway:* a stable system prompt is literally money; a per-request timestamp at the top
of the prompt quietly throws that discount away. See
[prompt vs. semantic caching](./prompt-vs-semantic-caching.md).

**Speculative decoding in production.** Techniques like Medusa and EAGLE, and provider
features such as "predicted outputs," use a cheap draft to accelerate
[decode](./prefill-vs-decode.md) with **no change to the output** — often 1.5–3× faster
token streaming. 🎯 *PM takeaway:* a latency win you can take *without* a quality-risk
conversation. See [speculative decoding](./speculative-quantization-distillation.md).

**4-bit models on one GPU (GPTQ / AWQ).** Quantization is why large open models run on a
single or even consumer GPU. But teams have repeatedly found 4-bit quality slipping on
*math, code, and strict JSON* while summarization barely notices. 🎯 *PM takeaway:* "we
quantized to save money" is a margin decision with a quality blast radius — gate it on
evals. See [quantization formats](./quantization-formats.md).

## Module recap

| Lesson | The one idea | The decision it drives |
| --- | --- | --- |
| [Prompt vs. semantic caching](./prompt-vs-semantic-caching.md) | One is lossless (KV reuse), one can serve wrong answers | When to cache responses; SLA risk |
| [KV cache management](./kv-cache-management.md) | KV memory — not FLOPs — caps concurrency | Context limits; capacity & pricing tiers |
| [Prefill vs. decode](./prefill-vs-decode.md) | Two phases, two bottlenecks (compute vs. bandwidth) | Which latency fix to fund |
| [Batching & paged attention](./batching-and-paged-attention.md) | Throughput vs. per-user latency dial | Build-vs-buy; margin model |
| [Spec-decode / quant / distill](./speculative-quantization-distillation.md) | Three speed/cost knobs, three risk profiles | Cost roadmap; quality risk accepted |
| [Quantization formats](./quantization-formats.md) | Format sets the ceiling; method gets you there | Whether to approve a quantization change |

**The through-line:** **two phases (prefill is compute-bound, decode is bandwidth-bound),
one cache (KV), throughput from batching + paging, and compression from
spec-decoding / quantization / distillation** explain almost all LLM serving economics.
Every latency, cost, and capacity number traces back to one of these.

> **Walk-away question:** *"Is our latency problem time-to-first-token or tokens-per-second
> — and is our prompt prefix actually cacheable?"*

---

← Back to [module index](./README.md) · → Next module: [02 · Reliable Outputs](../02-reliable-outputs/README.md)
