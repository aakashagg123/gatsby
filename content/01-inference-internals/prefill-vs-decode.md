# Prefill vs. Decode Latency

*Part of [01 · Inference Internals](./README.md)*

## TL;DR

Generation has two phases with opposite hardware profiles. **Prefill** processes the
entire prompt in parallel to build the [KV cache](./kv-cache-management.md) — it is
**compute-bound** and its cost scales with *input* length. **Decode** then emits
output tokens one at a time, each step reading the whole model and KV cache — it is
**memory-bandwidth-bound** and its cost scales with *output* length. They have
different bottlenecks, so they are optimized with different techniques. Conflating
them leads to optimizing the wrong thing.

> 🧭 **In plain terms**
>
> Every answer has two parts: *reading* the question and *writing* the reply — like someone who skims a long email in a flash but then types the response one key at a time. 'It feels slow' has two completely different causes: slow to *start* answering versus slow to *finish* typing. Each has a different fix, so knowing which one you have stops you from funding the wrong speed-up.


<!--sep-->

> 🎯 **For the AI-native PM**
>
> **Why it matters** — "It feels slow" has two different causes — time-to-first-token vs. per-token speed — with different fixes. Knowing which one you have lets you fund the right latency work instead of guessing.
>
> **What it changes in your decisions** — Your latency SLOs, UX choices (streaming, skeleton states), and which optimization you pay for.
>
> **Ask your eng team** — *"Is our latency problem time-to-first-token, or tokens-per-second?"*
>
> **Product risk if ignored** — You fund the wrong latency fix and the number you promised the exec doesn't move.


## Mental model

```
PREFILL  (process N prompt tokens together)        DECODE (generate one token at a time)
  ─ one big parallel matmul over all input          ─ T sequential steps
  ─ saturates the GPU's compute (FLOPs)             ─ each step: load weights + KV, do tiny matmul
  ─ cost ∝ input length                              ─ cost ∝ output length
  ─ bottleneck: arithmetic throughput               ─ bottleneck: memory bandwidth
```

The two user-visible latency numbers map directly onto the phases:

- **TTFT — Time To First Token** ≈ prefill time (plus queueing). Dominated by *input*
  length and [prompt-cache](./prompt-vs-semantic-caching.md) hits.
- **TPOT / ITL — Time Per Output Token / Inter-Token Latency** ≈ decode step time.
  Dominated by model size, memory bandwidth, and batch dynamics.

Total latency ≈ `TTFT + (num_output_tokens × TPOT)`.

## Why they're bound by different limits

- **Prefill is compute-bound** because all prompt tokens are processed at once: large,
  dense matrix multiplies that keep the GPU's compute units busy. Doubling the prompt
  roughly doubles prefill work. The fix is to *do less of it*: shorten/compress input
  ([context engineering](../00-foundations/context-engineering.md)) or skip it with
  [prefix caching](./prompt-vs-semantic-caching.md).
- **Decode is memory-bandwidth-bound** because each single-token step must stream the
  *entire* set of model weights (and the growing KV cache) through the compute units
  to produce one token. The arithmetic per step is tiny; the bottleneck is moving
  bytes. The GPU is underutilized on compute — which is exactly why
  [batching](./batching-and-paged-attention.md) helps decode so much (more sequences
  share each weight read).

## How this changes what you optimize

| Goal | Attack the right phase | Techniques |
| --- | --- | --- |
| Lower **TTFT** | Prefill | Prompt caching, shorter input, chunked prefill, more compute |
| Lower **TPOT** | Decode | [Speculative decoding](./speculative-quantization-distillation.md), smaller/[quantized](./quantization-formats.md) model, more bandwidth |
| Higher **throughput** | Decode-side batching | [Continuous batching](./batching-and-paged-attention.md), bigger batches via [KV headroom](./kv-cache-management.md) |

Key consequences:

- **Speculative decoding only helps decode**, not prefill — it attacks the
  sequential token-by-token bottleneck. Don't expect it to fix a slow TTFT caused by
  a huge prompt.
- **Quantization can help both**, but for different reasons: less data to move (helps
  bandwidth-bound decode) and sometimes faster math (helps compute-bound prefill).
- **Batching is mostly a decode/throughput lever.** It improves tokens/sec across
  many users but can slightly raise any single user's TPOT.
- **Chunked prefill** interleaves prefill of new requests with ongoing decode so a
  giant prompt doesn't stall everyone else's token stream — a scheduling fix for the
  prefill/decode interference problem.

## Workload shape matters

- **Long input, short output** (classification, extraction, RAG answer over big
  context) → **prefill-dominated**. Prompt caching and input compression are your
  biggest wins.
- **Short input, long output** (open-ended generation, long agent turns) →
  **decode-dominated**. Speculative decoding, smaller models, and batching matter
  most.
- Knowing which regime you're in tells you where to spend engineering effort. Measure
  TTFT and TPOT separately in [observability](../04-evals-observability/observability.md)
  — a single "latency" number hides which phase is the problem.

## Failure modes

- **Optimizing the wrong phase** — adding speculative decoding to fix latency that is
  actually 90% prefill of a 30k-token prompt.
- **Prefill stalls** — one user's huge prompt monopolizes the GPU and spikes everyone
  else's TPOT. Fix: chunked prefill / scheduler tuning.
- **Reporting only average latency** — hides that TTFT is fine but TPOT is terrible
  (or vice versa). Always split the two.

## Practitioner checklist

- [ ] Do you measure TTFT and TPOT as separate metrics?
- [ ] Do you know whether your workload is prefill- or decode-dominated?
- [ ] Is prompt caching enabled for long, shared prefixes (prefill win)?
- [ ] Are decode-side wins (spec decoding, batching) applied where output is long?
- [ ] Does a large prompt from one user degrade others' token stream?

## Related lessons

- [KV cache management](./kv-cache-management.md)
- [Continuous batching & paged attention](./batching-and-paged-attention.md)
- [Speculative decoding vs. quantization vs. distillation](./speculative-quantization-distillation.md)
- [Inference-stack tradeoffs](../06-strategy-tradeoffs/inference-stack-tradeoffs.md)
