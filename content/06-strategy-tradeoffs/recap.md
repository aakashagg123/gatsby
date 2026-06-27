# Strategy & Tradeoffs — Recap & Real-World Examples

*Part of [06 · Strategy & Tradeoffs](./README.md)*

## Real-world examples & war stories

**The "fine-tune our docs into the model" anti-pattern.** A recurring industry story:
a team fine-tunes a model to "teach it our knowledge base," ships something that's
**stale the day the docs change**, can't cite its sources, and is expensive to re-train —
then quietly rebuilds it as [RAG](../03-rag/rag-architecture.md). 🎯 *PM takeaway:* classify
the problem *first* — knowledge → RAG, behavior → fine-tune. See
[fine-tune vs. ICL vs. RAG vs. distillation](./finetune-vs-icl-vs-rag.md).

**Cheap-first routing / cascades (e.g., FrugalGPT research).** Sending most traffic to a
small model and escalating only the hard cases has been shown to cut cost dramatically
while holding quality — because most requests are easy. 🎯 *PM takeaway:* don't pay
worst-case cost for the average request; [route by difficulty](../02-reliable-outputs/model-routing.md).

**Distillation and small specialized models.** Distilled rerankers, embedders, and
on-device models deliver most of the quality of a big model for a narrow task at a
fraction of the cost/latency. 🎯 *PM takeaway:* once a task is *proven and high-volume*, a
smaller specialized model can transform your unit economics — but distill *after* it
works, not before. See [distillation](../01-inference-internals/speculative-quantization-distillation.md).

**Every real launch picks a point on the four axes.** Interactive chat optimizes latency;
an overnight batch job optimizes cost; a medical or legal workflow optimizes
reliability and quality over speed. 🎯 *PM takeaway:* there is no globally "best" config —
only the best one for *your* SLO. See [the four-axis tradeoff](./inference-stack-tradeoffs.md).

## Module recap

| Lesson | The one idea | The decision it drives |
| --- | --- | --- |
| [Fine-tune vs. ICL vs. RAG vs. distillation](./finetune-vs-icl-vs-rag.md) | Knowledge vs. behavior vs. cost → different tools | Build approach & timeline |
| [Inference-stack tradeoffs](./inference-stack-tradeoffs.md) | You can't max latency + quality + cost + reliability | SLOs; what to optimize vs. protect |
| [Production failure modes](./production-failure-modes.md) | A handful of *quiet* failures recur everywhere | Pre-launch risk review; what to monitor |

**The through-line:** mature AI engineering is **deliberate tradeoff-making.** Pick the
right tool for the *type* of problem, accept that improving one axis spends another, and
treat the failure catalog as your pre-launch checklist. The whole curriculum converges
here: every earlier lesson is a point in this tradeoff space.

> **Walk-away question:** *"Which axis are we choosing to trade — and is this a knowledge,
> behavior, or cost problem?"* Answer both and most of the roadmap writes itself.

---

← Back to [module index](./README.md) · ↩ Back to the [curriculum map](../../README.md)
