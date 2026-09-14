# Speculative decoding vs. quantization vs. distillation

*Part of [01 · Inference Internals](./README.md)*

## TL;DR

Three ways to make inference faster or cheaper, with very different risk
profiles. **Speculative decoding** speeds up [decode](./prefill-vs-decode.md)
with *zero quality change* — the output distribution is provably preserved.
But it needs extra memory, and it helps only when a small draft model agrees
often. **Quantization** shrinks the model to use less memory and bandwidth,
which is cheaper and faster, with a *bounded, measurable* quality risk.
**Distillation** trains a genuinely smaller model. It's the biggest
speed/cost win, but it carries the largest and least reversible quality
risk, plus real training cost. Pick by which resource you're short on and
how much quality risk you can carry.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — These are the three knobs for "make it cheaper and faster," and each carries a *different* quality risk. Pick the wrong one, and it shows up as a silent quality regression your users feel.
>
> **What it changes in your decisions** — Your cost-reduction roadmap, how much quality risk you'll accept, and the eval gates you require before rollout.
>
> **Ask your eng team** — *"Which of these are we using, and did quality hold on our eval set after we turned it on?"*
>
> **Product risk if ignored** — A cost-cutting change quietly degrades the experience and no one's eval catches it.


## The three techniques

### Speculative decoding — *free speed, same answer*
A small, fast **draft** model proposes the next *k* tokens. The large
**target** model verifies all *k* in a single forward pass — parallel
verification is cheap because the target is bandwidth-bound, not
compute-bound. The server keeps accepted tokens; on the first rejection, it
falls back to the target's own token. Because verification uses the
target's true probabilities, **the output distribution is identical** to
plain decode.

- **Wins:** lower TPOT / inter-token latency. It can be 1.5–3× faster on
  agreeable workloads.
- **Costs:** extra GPU memory for the draft model. The benefit depends
  entirely on the **acceptance rate** — if the draft rarely agrees, you pay
  overhead for little gain.
- **Scope:** decode only. It does nothing for prefill-dominated (long-prompt)
  latency.
- **Variants:** separate draft model, Medusa-style extra heads, n-gram or
  lookahead decoding, EAGLE.

### Quantization — *smaller model, bounded quality risk*
Store, and sometimes compute, weights and activations in fewer bits — FP16
to INT8, FP8, or INT4. Moving less data directly helps the bandwidth-bound
decode phase and frees [KV/memory headroom](./kv-cache-management.md) for
bigger batches.

- **Wins:** lower memory footprint, lower $/token, often lower latency, more
  concurrency.
- **Costs:** quality degradation that grows as bits shrink, and that varies
  by method and by what you quantize — weights, activations, or KV. 8-bit is
  usually near-lossless. 4-bit needs care. Below that, quality often falls
  off a cliff.
- **Reversibility:** high. It's a post-training transform you can dial back.
- Full detail and method comparison: [Quantization formats](./quantization-formats.md).

### Distillation — *a new, smaller model*
Train a small **student** to imitate a large **teacher**, matching its
outputs or output distributions. The result is a permanently smaller,
cheaper, faster model specialized to your task distribution.

- **Wins:** the largest steady-state speed/cost reduction. It's great for a
  narrow, high-volume task.
- **Costs:** upfront training effort and data. The quality ceiling is lower
  and depends on the teacher and data. **Generality is lost** — the student
  is good at what it was distilled for and can be brittle off-distribution.
- **Reversibility:** low. You've trained an artifact and built a pipeline
  around it.

## Choosing between them

| | Speculative decoding | Quantization | Distillation |
| --- | --- | --- | --- |
| Primary win | Lower decode latency | Lower memory + cost | Lower cost at scale |
| Quality risk | **None** (lossless) | Bounded, tunable | Largest, task-dependent |
| Up-front cost | Low (config + draft model) | Low (convert once) | High (training pipeline) |
| Reversibility | Trivial | Easy | Hard |
| Helps prefill? | No | Yes (less data/faster math) | Yes (smaller model) |
| Best when | Latency-bound, draft agrees | Memory/cost-bound | One high-volume task, willing to train |

They are **composable**: a common production stack is a *quantized* model
served with *speculative decoding*, and for a hot narrow task, a *distilled*
student that is itself quantized. They attack different resources, so
stacking compounds the wins.

## Decision guide

1. **Latency-bound, output-heavy, can't touch quality?** Reach for
   speculative decoding first.
2. **Memory/cost-bound, and can tolerate a small, measured quality dip?**
   Use quantization — start at INT8/FP8, validate, and only go to INT4 if
   evals hold.
3. **One narrow, very high-volume task where a big model is overkill?** Use
   distillation, then quantize the student.
4. **Always:** gate every one of these behind your
   [eval suite](../04-evals-observability/evals.md). Speculative decoding
   shouldn't move evals at all — that's a red flag if it does. Quantization
   and distillation *will* move evals, so you must measure by how much.

## Failure modes

- **Speculative decoding with a bad draft** — a low acceptance rate makes
  it net-neutral or slower. Measure acceptance rate, not just "it's
  enabled."
- **Quantizing past the cliff** — INT4 on a task with tight numeric or
  format demands silently degrades. Only [evals](../04-evals-observability/evals.md)
  catch this, not eyeballing.
- **Distilling on the wrong distribution** — the student looks great
  offline but fails on the long tail of real traffic it wasn't distilled
  for.

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
