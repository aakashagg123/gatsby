# Speculative Decoding vs. Quantization vs. Distillation

*Part of [01 · Inference Internals](./README.md)*

## TL;DR

Three ways to make inference faster or cheaper, with very different risk profiles.
**Speculative decoding** speeds up [decode](./prefill-vs-decode.md) with *zero quality
change* (the output distribution is provably preserved) but needs extra memory and
helps only when a small draft model agrees often. **Quantization** shrinks the model
to use less memory/bandwidth — cheaper and faster, with a *bounded, measurable*
quality risk. **Distillation** trains a genuinely smaller model — the biggest
speed/cost win, but the largest and least reversible quality risk, plus real training
cost. Pick by which resource you're short on and how much quality risk you can carry.

## The three techniques

### Speculative decoding — *free speed, same answer*
A small, fast **draft** model proposes the next *k* tokens; the large **target** model
verifies all *k* in a single forward pass (parallel verification is cheap because the
target is bandwidth-bound, not compute-bound). Accepted tokens are kept; on the first
rejection it falls back to the target's own token. Because verification uses the
target's true probabilities, **the output distribution is identical** to plain decode.

- **Wins:** lower TPOT / inter-token latency; can be 1.5–3× faster on agreeable
  workloads.
- **Costs:** extra GPU memory for the draft model; benefit depends entirely on the
  **acceptance rate** — if the draft rarely agrees, you pay overhead for little gain.
- **Scope:** decode only. Does nothing for prefill-dominated (long-prompt) latency.
- **Variants:** separate draft model, Medusa-style extra heads, n-gram/lookahead, EAGLE.

### Quantization — *smaller model, bounded quality risk*
Store (and sometimes compute) weights/activations in fewer bits — FP16 → INT8 / FP8 /
INT4. Less data to move directly helps the bandwidth-bound decode phase and frees
[KV/memory headroom](./kv-cache-management.md) for bigger batches.

- **Wins:** lower memory footprint, lower $/token, often lower latency, more
  concurrency.
- **Costs:** quality degradation that grows as bits shrink and varies by method and
  by what you quantize (weights vs. activations vs. KV). 8-bit is usually near-lossless;
  4-bit needs care; below that, quality often falls off a cliff.
- **Reversibility:** high — it's a post-training transform you can dial back.
- Full detail and method comparison: [Quantization formats](./quantization-formats.md).

### Distillation — *a new, smaller model*
Train a small **student** to imitate a large **teacher** (matching its outputs or
output distributions). The result is a permanently smaller, cheaper, faster model
specialized to your task distribution.

- **Wins:** the largest steady-state speed/cost reduction; great for a narrow,
  high-volume task.
- **Costs:** upfront training effort and data; quality ceiling is lower and depends on
  the teacher and data; **generality is lost** — the student is good at what it was
  distilled for and can be brittle off-distribution.
- **Reversibility:** low — you've trained an artifact and built a pipeline around it.

## Choosing between them

| | Speculative decoding | Quantization | Distillation |
| --- | --- | --- | --- |
| Primary win | Lower decode latency | Lower memory + cost | Lower cost at scale |
| Quality risk | **None** (lossless) | Bounded, tunable | Largest, task-dependent |
| Up-front cost | Low (config + draft model) | Low (convert once) | High (training pipeline) |
| Reversibility | Trivial | Easy | Hard |
| Helps prefill? | No | Yes (less data/faster math) | Yes (smaller model) |
| Best when | Latency-bound, draft agrees | Memory/cost-bound | One high-volume task, willing to train |

They are **composable**: a common production stack is a *quantized* model served with
*speculative decoding*, and for a hot narrow task a *distilled* student that is itself
quantized. They attack different resources, so stacking compounds the wins.

## Decision guide

1. **Latency-bound, output-heavy, can't touch quality?** → Speculative decoding first.
2. **Memory/cost-bound, can tolerate a small, measured quality dip?** → Quantization
   (start at INT8/FP8, validate, only go to INT4 if evals hold).
3. **One narrow, very high-volume task where a big model is overkill?** → Distillation,
   then quantize the student.
4. **Always:** gate every one of these behind your [eval suite](../04-evals-observability/evals.md).
   Speculative decoding shouldn't move evals at all (red flag if it does); quantization
   and distillation *will* — you must measure by how much.

## Failure modes

- **Speculative decoding with a bad draft** — low acceptance rate makes it net-neutral
  or slower; measure acceptance rate, not just "it's enabled."
- **Quantizing past the cliff** — INT4 on a task with tight numeric/format demands
  silently degrades; caught only by [evals](../04-evals-observability/evals.md), not eyeballing.
- **Distilling on the wrong distribution** — student looks great offline, fails on the
  long tail of real traffic it wasn't distilled for.

## Practitioner checklist

- [ ] Are you short on latency, memory, or steady-state cost? (picks the technique)
- [ ] For spec decoding: do you monitor draft acceptance rate?
- [ ] For quantization: did evals hold at the chosen bit-width?
- [ ] For distillation: does the student's eval set reflect *production* traffic?
- [ ] Are all three gated by regression evals before rollout?

## Related lessons

- [Quantization formats: INT8, INT4, FP8, AWQ, GPTQ](./quantization-formats.md)
- [Prefill vs. decode](./prefill-vs-decode.md)
- [Fine-tuning vs. ICL vs. RAG vs. distillation](../06-strategy-tradeoffs/finetune-vs-icl-vs-rag.md)
- [Inference-stack tradeoffs](../06-strategy-tradeoffs/inference-stack-tradeoffs.md)
- [Evals](../04-evals-observability/evals.md)
