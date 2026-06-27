# RAG & Retrieval — Recap & Real-World Examples

*Part of [03 · RAG & Retrieval](./README.md)*

## Real-world examples & war stories

**Air Canada's invented refund policy (2024).** The canonical grounding failure: the bot
answered from "imagination" instead of the airline's actual, current policy — and a
tribunal made the company honor the made-up version. 🎯 *PM takeaway:* the fix is
architectural — answer **only from retrieved, current sources, with citations**, and say
"I don't know" when the context is silent. See
[RAG architecture](./rag-architecture.md).

**Enterprise RAG with permissions (Glean, Notion AI, Sourcegraph).** Production systems
that search across a company's docs, tickets, and code live or die on three things this
module covers: **hybrid search** (so exact identifiers and error codes are found),
**permission/ACL filtering** (so retrieval never crosses a user's access — a
[multi-tenant boundary](../05-safety-multitenancy/multi-tenant-isolation.md)), and
**freshness** (so deleted or superseded docs stop being cited). 🎯 *PM takeaway:* retrieval
quality and access scoping *are* the product.

**Citations as a feature (Perplexity, Bing/Copilot).** These products made
inline source attribution a core trust signal. 🎯 *PM takeaway:* if you want users (or
legal) to trust answers, you need [attribution and citation quality](./retrieval-evals.md)
you can measure — not just a confident paragraph.

**"Lost in the middle," again.** The same research that warns against over-stuffing
context is why dumping your top-50 chunks *hurts*: the answer gets buried. 🎯 *PM takeaway:*
**reranking down to a few great chunks** beats retrieving many mediocre ones — better
answers *and* lower [token cost](../04-evals-observability/cost-attribution.md).

## Module recap

| Lesson | The one idea | The decision it drives |
| --- | --- | --- |
| [RAG architecture](./rag-architecture.md) | Quality is capped by the weakest pipeline stage | Data to index; freshness SLA; citations |
| [Retrieval evals](./retrieval-evals.md) | Measure retrieval *and* grounding separately | The accuracy bar you can defend |

**The through-line:** most "the AI gave a wrong answer" bugs are **retrieval** bugs, not
model bugs. Build the pipeline — chunk → embed → hybrid search → rerank → keep fresh — then
**prove it** by measuring recall/precision (did we find it?) separately from
grounding/attribution (did we use it faithfully?). The generator can only be as good as
what retrieval surfaces.

> **Walk-away question:** *"When an answer is wrong, did we fail to **retrieve** the right
> source, or fail to **ground** the answer in it?"* Different bug, different fix.

---

← Back to [module index](./README.md) · → Next module: [04 · Evals & Observability](../04-evals-observability/README.md)
