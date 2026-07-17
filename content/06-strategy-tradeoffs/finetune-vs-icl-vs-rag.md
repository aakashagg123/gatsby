# Fine-tuning vs. in-context learning vs. RAG vs. distillation — and when each is the wrong tool

*Part of [06 · Strategy & Tradeoffs](./README.md)*

## TL;DR

These four are not competitors; they solve *different problems*. **In-context learning
(ICL)** shapes behavior via the prompt — zero infra, instant iteration, but pays tokens
every call. **RAG** injects *knowledge* at query time — best for facts that change or
are too large to memorize. **Fine-tuning** bakes in *behavior/format/style* — best when
the prompt can't reliably get there. **Distillation** produces a smaller, cheaper model
for a *narrow, high-volume* task. The expensive mistake is reaching for fine-tuning when
you have a *knowledge* problem (use RAG) or a *prompt* problem (use ICL).

> 🎯 **For the AI-native PM**
>
> **Why it matters** — Teams burn entire quarters fine-tuning when they actually had a retrieval problem (or vice versa). Picking the right approach is the highest-leverage *early* product decision you'll make.
>
> **What it changes in your decisions** — Your build approach and timeline, your data investment, and whether fine-tuning is even the right project.
>
> **Ask your eng team** — *"Is this a knowledge problem (use RAG) or a behavior problem (maybe fine-tune)?"*
>
> **Product risk if ignored** — A quarter spent fine-tuning a model that's already stale, when RAG would have been cheaper, fresher, and citeable.


## The key distinction: knowledge vs. behavior

```
Need the model to KNOW something it doesn't?      → RAG (or ICL for small/static facts)
Need the model to BEHAVE a certain way reliably?  → Fine-tuning (or ICL if prompt suffices)
Need a cheaper/faster model for ONE narrow task?  → Distillation
Just need to steer it, fast, with no infra?       → In-context learning
```

Most "should we fine-tune?" questions dissolve once you ask: *is this a knowledge gap or
a behavior gap?* Fine-tuning teaches behavior, not facts — it's a poor and stale way to
store knowledge that RAG handles live.

## The four approaches

### In-context learning (ICL)
Instructions + few-shot examples in the [context](../00-foundations/context-engineering.md);
no weight changes.
- **Best for:** fast iteration, prototypes, tasks a capable model can do when *shown how*,
  low/medium volume.
- **Costs:** every example is paid for on *every* call (tokens, latency,
  [prefill](../01-inference-internals/prefill-vs-decode.md)); limited by context window;
  can't teach truly novel behavior.
- **Wrong when:** the prompt is huge and repeated at scale (fine-tune or distill to amortize),
  or you need knowledge that changes (RAG).

### RAG
Retrieve relevant data at query time and ground the answer in it
([RAG architecture](../03-rag/rag-architecture.md)).
- **Best for:** large, changing, or proprietary knowledge; needing
  [citations/attribution](./../03-rag/retrieval-evals.md); [freshness](../03-rag/rag-architecture.md);
  reducing hallucination on facts.
- **Costs:** a whole pipeline to build and operate (chunking, embeddings, indexing,
  reranking, freshness); retrieval quality caps answer quality; per-call latency + token cost.
- **Wrong when:** the problem is *behavior/format/tone* (retrieval won't fix it), or the
  knowledge is tiny and static (just put it in the prompt).

### Fine-tuning
Update weights (often parameter-efficient, e.g. LoRA) on task examples.
- **Best for:** consistent format/style/behavior the prompt can't reliably get; encoding
  a domain *skill*; shortening prompts (move few-shots into weights → cheaper inference);
  a narrow task done at high volume.
- **Costs:** data curation + training pipeline; **re-training on drift**; risks
  (catastrophic forgetting, overfitting); a model artifact to version, evaluate, and
  serve; slow iteration vs. editing a prompt.
- **Wrong when:** you need *fresh facts* (it's frozen at training time → RAG), you have
  little data, or a prompt change would have sufficed. Fine-tuning to "add knowledge" is
  the classic anti-pattern: stale, expensive, and unattributable.

### Distillation
Train a small **student** to mimic a large **teacher**
([details](../01-inference-internals/speculative-quantization-distillation.md)).
- **Best for:** a proven, narrow, *high-volume* task where a big model works but is too
  slow/expensive; squeezing steady-state cost and latency.
- **Costs:** teacher-generated data + training; lower quality ceiling; loses generality
  (brittle off-distribution); a pipeline to maintain.
- **Wrong when:** the task is broad/evolving, volume is low (not worth it), or you haven't
  yet nailed the task with a big model (distill *after* it works).

## Decision guide

1. **Start with ICL.** Cheapest to try; often enough. Establish [evals](../04-evals-observability/evals.md) here.
2. **Knowledge gap?** → **RAG**. Facts that are large, proprietary, or changing; need citations.
3. **Behavior gap the prompt can't close (after honest prompt effort)?** → **Fine-tune**.
   Format/style/skill consistency; also to shrink expensive long prompts at scale.
4. **Proven narrow task, high volume, cost/latency-bound?** → **Distill** (then optionally
   [quantize](../01-inference-internals/quantization-formats.md) the student).
5. **They compose.** The mature stack is often: a (possibly fine-tuned or distilled) model,
   **with RAG** for knowledge, **plus ICL** for per-request steering — chosen per
   subproblem, not globally.

The same triad shows up *inside agents*, where Google's *Agents* whitepaper calls it
**targeted learning** — teaching a model when and how to use its tools: **in-context
learning** (tools and few-shot examples in the prompt, ReAct-style), **retrieval-based
in-context learning** (dynamically populating the prompt with the most relevant examples
from an external store — RAG applied to *behavior*, not just facts), and **fine-tuning**
on a corpus of tool-use examples before inference. Different problem, identical decision
structure: start in the prompt, retrieve when it must scale, train when it must be innate.

## Comparison

| | ICL | RAG | Fine-tuning | Distillation |
| --- | --- | --- | --- | --- |
| Changes | Prompt | Retrieved context | Weights | New small model |
| Solves | Steering | Knowledge | Behavior/format | Cost/latency at scale |
| Fresh facts | Limited | **Yes** | No (frozen) | No |
| Iteration speed | Instant | Fast | Slow | Slow |
| Up-front cost | ~None | Pipeline | Training | Training |
| Per-call cost | High (tokens) | Medium | Low(er) | **Lowest** |
| Main risk | Token bloat | Retrieval quality | Drift/overfit/stale | Narrowness |

## Failure modes (using the wrong tool)

- **Fine-tuning for knowledge** → stale, expensive, no citations; should have been RAG.
- **RAG for a behavior problem** → retrieval is perfect, output still wrong format;
  needed prompting or fine-tuning.
- **Premature fine-tuning/distillation** → committed to an artifact before the task was
  even solved with a big model and good evals.
- **ICL at scale** → a 6k-token prompt repeated millions of times; should have amortized
  into weights ([cost attribution](../04-evals-observability/cost-attribution.md) reveals it).
- **No evals first** → you can't tell whether the new approach actually helped.

## Practitioner checklist

- [ ] Have you classified the problem as knowledge vs. behavior vs. cost?
- [ ] Did you exhaust ICL (and honest prompt iteration) before training anything?
- [ ] Is fresh/changing knowledge handled by RAG, not baked into weights?
- [ ] Do you have evals to prove the chosen approach beats the baseline?
- [ ] For fine-tune/distill: do you have a plan for drift and re-training?
- [ ] Are you composing approaches per subproblem rather than picking one globally?

## Related lessons

- [RAG architecture](../03-rag/rag-architecture.md)
- [Context engineering](../00-foundations/context-engineering.md)
- [Speculative decoding vs. quantization vs. distillation](../01-inference-internals/speculative-quantization-distillation.md)
- [Evals](../04-evals-observability/evals.md)
- [Inference-stack tradeoffs](./inference-stack-tradeoffs.md)
