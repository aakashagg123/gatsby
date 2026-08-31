# KV cache management: eviction, reuse, and memory pressure at scale

*Part of [01 · Inference Internals](./README.md)*

## TL;DR

During generation, the model caches the key and value tensors of every token it has
already processed. This way attention doesn't recompute the whole sequence at each
step. This **KV cache** is what makes [decode](./prefill-vs-decode.md) fast. It is
usually the binding constraint on how many requests a GPU can serve at once.
Managing it — sizing, reuse, eviction, fragmentation — is the core memory problem
of LLM serving.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — This is the hidden reason you can't just add longer context and more concurrent users cheaply. It sets your capacity ceiling and your unit economics.
>
> **What it changes in your decisions** — The context-length limits you expose in the product, your scaling plan, and your pricing tiers.
>
> **Ask your eng team** — *"What does doubling our max context length do to our cost and our capacity?"*
>
> **Product risk if ignored** — You promise long-context or high-concurrency features. They quietly blow up cost or fall over at scale.


## Mental model

Attention at step *t* needs the keys and values of all tokens `0..t-1`.
Recomputing them every step would make generation quadratic. Instead, the
server stores them:

```
KV cache size ≈ 2 (K and V)
              × num_layers
              × num_kv_heads × head_dim
              × sequence_length
              × bytes_per_element (dtype)
              × batch_size (sum of all sequences in flight)
```

The two things to feel in your gut:
1. **It grows linearly with total tokens in flight** (context length × concurrency).
2. **It lives in scarce GPU HBM**, competing with the model weights themselves.

A long-context, high-concurrency workload can need *more memory for KV than for the
model weights.* That's why KV cache — not FLOPs — limits your batch size and
throughput.

## The levers

### 1. Reuse
Identical prefixes can share KV entries. This is exactly what
[prompt/prefix caching](./prompt-vs-semantic-caching.md) exploits. A stable system
prompt shared across requests is computed once and reused. This saves both
prefill compute and memory. Reuse requires the entries to still be resident,
which ties reuse to eviction policy.

### 2. Eviction
When memory fills, something must go. Here are the policies and their costs:
- **By completion** — free a sequence's KV when it finishes (the baseline).
- **LRU on cached prefixes** — evict the least-recently-used shared prefix. A
  future request with that prefix pays full prefill again. This is a
  *recompute*, not a wrong answer.
- **Preemption / swapping** — under pressure, the server can pause a running
  sequence. It can then **recompute** the sequence's KV later, or **swap** it
  to CPU/host memory and back. Recompute trades compute for memory. Swapping
  trades PCIe bandwidth for memory. Both add tail latency.

### 3. Memory pressure & fragmentation
Naively, each sequence reserves a contiguous block sized for its *maximum*
possible length. This wastes memory for short outputs and fragments the pool.
**Paged attention** solves this by allocating the KV cache in fixed-size
blocks that need not be contiguous — OS-style virtual memory for the cache.
It nearly eliminates fragmentation and enables much higher concurrency. See
[paged attention](./batching-and-paged-attention.md).

### 4. Compression
- **Smaller dtype** — storing KV in FP8/INT8 halves or quarters cache size (a
  quality/memory tradeoff; see [quantization formats](./quantization-formats.md)).
- **Grouped/Multi-Query Attention (GQA/MQA)** — fewer *KV* heads than query
  heads, so the cache shrinks proportionally. Most modern models use GQA for
  exactly this reason.
- **Sliding-window / local attention** — bound the cache to the last *N* tokens.

## Why this is the throughput story

Concurrency — how many requests you batch together — is capped by how much KV
cache fits. More memory headroom means bigger batches, which means higher GPU
utilization, which means lower cost-per-token. So every KV optimization
(paging, GQA, FP8 KV, eviction policy) is really a **throughput and cost**
optimization. This is the mechanism behind
[continuous batching](./batching-and-paged-attention.md).

## Tradeoffs

| Lever | Buys you | Costs you |
| --- | --- | --- |
| Prefix reuse | Less prefill, less memory | Cache must stay resident; invalidation care |
| Aggressive eviction | Higher concurrency | Recompute/swap latency on the tail |
| FP8/INT8 KV | ~2–4× more concurrency | Small quality risk on long contexts |
| GQA/MQA | Big cache reduction | Baked into the model architecture |
| Sliding window | Bounded memory | Forgets distant context |

## Failure modes

- **OOM under load** — concurrency times context exceeded HBM, so requests get
  rejected or the server crashes. Mitigate with admission control and
  max-context limits.
- **Tail latency from preemption** — under pressure, long requests get
  swapped or recomputed, which spikes p99. You can see this only with
  [per-span latency tracing](../04-evals-observability/observability.md).
- **Cache thrash** — too many distinct prefixes for the pool, so reuse never
  hits. Standardize prefixes (context engineering) to keep the working set
  small.
- **Cross-tenant reuse hazard** — sharing KV across trust boundaries can leak
  data if it isn't carefully scoped. See
  [multi-tenant cache safety](../05-safety-multitenancy/multi-tenant-isolation.md).

## Practitioner checklist

- [ ] Have you computed KV memory for your max context × target concurrency?
- [ ] Does your model use GQA/MQA (and could FP8 KV buy headroom)?
- [ ] Is there admission control so you reject rather than OOM?
- [ ] Do you monitor preemption/swap rate and its effect on p99?
- [ ] Are shared prefixes scoped so reuse never crosses a tenant boundary?

## Related lessons

- [Prefill vs. decode](./prefill-vs-decode.md)
- [Continuous batching & paged attention](./batching-and-paged-attention.md)
- [Prompt vs. semantic caching](./prompt-vs-semantic-caching.md)
- [Quantization formats](./quantization-formats.md)
- [Multi-tenant isolation & cache safety](../05-safety-multitenancy/multi-tenant-isolation.md)
