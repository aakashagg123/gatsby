# Continuous batching & paged attention

*Part of [01 · Inference Internals](./README.md)*

## TL;DR

Two innovations made modern LLM serving economical. **Continuous batching** keeps the
GPU full by adding and removing requests at the *token* level instead of waiting for
a whole batch to finish. **Paged attention** manages the [KV cache](./kv-cache-management.md)
in fixed-size, non-contiguous blocks (like OS virtual memory) so memory isn't wasted
or fragmented — which lets you fit more sequences and therefore batch more. Together
they turn the bandwidth-bound [decode](./prefill-vs-decode.md) phase into a
high-throughput one.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — This is the throughput-vs-latency dial for self-hosted inference, and it sets the *gross margin* on your AI features more than almost anything else.
>
> **What it changes in your decisions** — Build-vs-buy for inference, your margin model, and the latency-vs-cost point you choose to operate at.
>
> **Ask your eng team** — *"What's our cost per token at our latency target, and how much does relaxing latency a little save us?"*
>
> **Product risk if ignored** — The margins assumed in your business case never materialize because the serving stack was never tuned.


## The problem they solve

Decode is **memory-bandwidth-bound**: each step streams the whole model through the
compute units to produce one token, leaving compute units idle. The cure is
**batching** — process many sequences per weight read so each expensive byte-movement
serves many users. But two things get in the way:

1. **Ragged completion.** In a static batch, sequences finish at different times.
   With naive batching the whole batch waits for the slowest sequence, and finished
   slots sit idle → wasted GPU.
2. **Memory waste.** Reserving a contiguous max-length KV block per sequence wastes
   memory (most outputs are short) and fragments the pool, capping how many sequences
   fit.

## Continuous (in-flight) batching

Instead of "form batch → run to completion → form next batch," the scheduler operates
per decoding step:

```
every step:
  - run one decode step for all active sequences
  - any sequence that emitted EOS → evict, free its KV, return result
  - any newly arrived request → admit, schedule its prefill, add to the batch
```

Effects:
- **GPU stays saturated** — finished slots are immediately refilled by waiting
  requests; no idle bubbles.
- **New requests don't wait for a batch boundary** — they join almost immediately, so
  queueing latency drops.
- **Throughput rises sharply** at a given latency target compared to static batching.

The catch: prefill of a newly admitted request can momentarily interfere with ongoing
decode (a TTFT-vs-TPOT tension). **Chunked prefill** mitigates this by slicing big
prefills and interleaving them with decode steps so no single large prompt stalls the
token stream.

## Paged attention

Borrowing virtual-memory ideas from operating systems: divide the KV cache into
fixed-size **blocks (pages)**. A sequence's KV is a *list of blocks* that need not be
contiguous; a block table maps logical positions to physical blocks.

Benefits:
- **Near-zero fragmentation** — allocate blocks on demand as a sequence grows, instead
  of reserving its maximum up front. More sequences fit in the same HBM →
  bigger batches → higher throughput.
- **Cheap sharing (copy-on-write).** Sequences with a common prefix can *share* the
  physical blocks for that prefix and only diverge when they differ — this is the
  mechanism behind efficient [prefix caching](./prompt-vs-semantic-caching.md) and
  parallel sampling/beam search.
- **Clean eviction/swap units.** Blocks are natural granules to evict or swap to host
  memory under [memory pressure](./kv-cache-management.md).

## How they reinforce each other

Paged attention raises how many sequences fit in memory; continuous batching turns
that headroom into sustained GPU utilization. The product is dramatically higher
throughput — and therefore lower **cost per token** — at comparable latency. This is
the core reason a well-configured open-source server (vLLM, TGI, TensorRT-LLM, SGLang)
can serve far more traffic per GPU than a naive loop.

## Tradeoffs

| Lever | Buys you | Watch out for |
| --- | --- | --- |
| Bigger batches | Throughput, lower $/token | Higher per-user TPOT; more KV memory |
| Continuous batching | Utilization + low queueing | Prefill/decode interference |
| Chunked prefill | Smoother TPOT under mixed load | Slightly higher prefill latency |
| Paged KV blocks | Concurrency, prefix sharing | Small bookkeeping overhead |

There is no free lunch: pushing batch size up improves cost and throughput but can
raise tail latency for individual requests. The right operating point is an
[SLO decision](../06-strategy-tradeoffs/inference-stack-tradeoffs.md), not a default.

## Failure modes

- **Throughput tuned, latency forgotten** — batch sizes cranked for cost, p99 TPOT
  quietly blows the SLO. Track both.
- **Prefill stalls** — a 32k-token prompt admitted mid-flight freezes everyone's token
  stream for a moment; needs chunked prefill.
- **KV exhaustion** — high concurrency × long context overruns the block pool →
  preemption/swap and tail-latency spikes (see [KV management](./kv-cache-management.md)).

## Practitioner checklist

- [ ] Are you on a server that does continuous batching + paged attention?
- [ ] Have you set a max batch size / max-num-seqs tied to an SLO, not just "max"?
- [ ] Is chunked prefill enabled if you mix long prompts with latency-sensitive decode?
- [ ] Do you alert on KV-pool utilization and preemption rate?
- [ ] Do you track throughput *and* p99 TTFT/TPOT together?

## Related lessons

- [KV cache management](./kv-cache-management.md)
- [Prefill vs. decode](./prefill-vs-decode.md)
- [Prompt vs. semantic caching](./prompt-vs-semantic-caching.md)
- [Inference-stack tradeoffs](../06-strategy-tradeoffs/inference-stack-tradeoffs.md)
