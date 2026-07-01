# Context engineering, not just long prompts

*Part of [00 · Foundations](./README.md)*

## TL;DR

The context window is a scarce, expensive, and *quality-sensitive* resource. Context
engineering is the discipline of deciding **what** goes into it, **in what order**,
**in what form**, and **what gets left out** — on every single call. "Just stuff in
more text" is the anti-pattern: longer context costs more, runs slower, and often
makes answers *worse*, not better.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — Context is a budget you spend on *every* request — it shows up directly in latency, cost, and answer quality. "Just give the model more info" is a product decision with a bill and a quality cost attached.
>
> **What it changes in your decisions** — What data you invest in making retrievable, how you scope memory/personalization features, and your cost-per-interaction.
>
> **Ask your eng team** — *"What's actually in the context window on a typical request, and what does each part cost us?"*
>
> **Product risk if ignored** — Prompt creep quietly triples unit cost and *lowers* quality — invisible until the invoice or the churn shows up.


## Mental model

Treat the context window like a working set in a memory hierarchy, not a junk
drawer. The model can only attend to what is in front of it, and its effective
attention is **non-uniform**: information at the start and end of the window is used
more reliably than information buried in the middle ("lost in the middle"). So
context engineering optimizes three things at once:

1. **Relevance** — is the right information present at all? (a retrieval problem →
   [RAG architecture](../03-rag/rag-architecture.md))
2. **Signal-to-noise** — is it *crowded out* by irrelevant tokens?
3. **Position & format** — is it placed and shaped so the model actually uses it?

## Why more tokens is not more quality

- **Distraction.** Irrelevant retrieved chunks pull attention away from the answer.
  Precision often matters more than recall once you have *enough* signal — see
  [retrieval evals](../03-rag/retrieval-evals.md).
- **Lost in the middle.** Long contexts degrade for facts placed mid-window. Put the
  most decision-critical material near the top or bottom.
- **Cost & latency scale with input length.** Every input token is paid for in the
  [prefill](../01-inference-internals/prefill-vs-decode.md) phase and in dollars.
  Doubling context roughly doubles prefill compute.
- **Contamination risk.** Every extra source (a retrieved doc, a tool result, prior
  turns) is a potential [prompt-injection](../05-safety-multitenancy/safety-engineering.md)
  vector. More context = larger attack surface.

## The components of a well-engineered context

A typical context is assembled from layered sources, each with its own budget:

```
[ system / role + policy ]      ← stable, cache-friendly prefix
[ tool definitions / contracts ] ← stable
[ task instructions ]
[ retrieved knowledge ]          ← ranked, reranked, trimmed, cited
[ relevant memory / history ]    ← summarized, not raw
[ the user's actual request ]    ← often best placed last
```

Engineering decisions for each layer:

- **Stable prefix first.** Keep system prompt, policies, and tool contracts at the
  front and *unchanging* so they can be reused by
  [prompt caching](../01-inference-internals/prompt-vs-semantic-caching.md). Putting a
  timestamp or user name at the very top silently breaks prefix caching.
- **Retrieve, then rerank, then trim.** Don't paste your top-50 chunks. Rerank and
  keep the few that matter — see [RAG architecture](../03-rag/rag-architecture.md).
- **Summarize history, don't replay it.** Long agent transcripts should be
  compressed into running summaries plus the last few turns.
- **Make provenance explicit.** Tag each retrieved chunk with a source id so the
  model can produce [citations](../03-rag/retrieval-evals.md) and so you can defend
  against [injection](../05-safety-multitenancy/safety-engineering.md).

## Tradeoffs & decisions

| Lever | More of it helps | But costs |
| --- | --- | --- |
| Retrieved chunks | Recall / coverage | Precision, distraction, $$ |
| History depth | Continuity | Tokens, drift, latency |
| Few-shot examples | Format adherence | Tokens; can overfit to examples |
| Long system prompt | Control | Cache-stable but pricey on every call |

The recurring tension is **recall vs. precision vs. budget**. Context engineering is
the art of spending your token budget where it moves the answer.

## Failure modes

- **Prompt bloat creep.** Every incident adds "also, never do X" to the system
  prompt until it is 4,000 tokens of contradictory rules. Treat the system prompt
  like code: review it, test it, and prune it with [evals](../04-evals-observability/evals.md).
- **Cache-busting prefixes.** Dynamic content near the top destroys
  [prefix cache hits](../01-inference-internals/prompt-vs-semantic-caching.md) and
  quietly triples cost.
- **Raw history replay.** Feeding the entire conversation every turn → quadratic
  cost growth and lost-in-the-middle degradation.
- **Unbounded retrieval.** "Top-k = 20" with no reranking buries the answer in noise.

## Practitioner checklist

- [ ] Is your context assembled from explicit, budgeted layers — not string concat?
- [ ] Is the stable prefix actually stable (cache-friendly)?
- [ ] Do you rerank and trim retrieved context instead of dumping it?
- [ ] Is conversation history summarized rather than replayed?
- [ ] Is every external chunk tagged with provenance and treated as untrusted?
- [ ] Have you measured whether *adding* context improves your evals, or just cost?

## Related lessons

- [Harness engineering](./harness-engineering.md)
- [RAG architecture](../03-rag/rag-architecture.md)
- [Prompt caching vs. semantic caching](../01-inference-internals/prompt-vs-semantic-caching.md)
- [Prefill vs. decode](../01-inference-internals/prefill-vs-decode.md)
- [Safety engineering](../05-safety-multitenancy/safety-engineering.md)
