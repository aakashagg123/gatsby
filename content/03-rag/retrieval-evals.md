# Retrieval evals: recall, precision, grounding, attribution, and citation quality

*Part of [03 · RAG & Retrieval](./README.md)*

## TL;DR

A [RAG system](./rag-architecture.md) has two failure surfaces: *did we
retrieve the right thing?* and *did the model use it faithfully?* You must
measure them **separately**, or you'll tune the prompt to fix a retrieval
bug, or the reverse. Retrieval is judged by **recall** and **precision**.
Generation-over-retrieval is judged by **grounding** (faithfulness),
**attribution** (claims traced to sources), and **citation quality**.
End-to-end answer quality alone hides which half is broken.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — You can't claim "grounded" or "accurate" unless you measure grounding and attribution *separately*. This turns a marketing claim into a number you can defend to customers and legal.
>
> **What it changes in your decisions** — The quality bar you commit to, how you report accuracy externally, and any citation guarantees.
>
> **Ask your eng team** — *"How do we measure that answers are actually supported by sources, instead of plausibly made up?"*
>
> **Product risk if ignored** — You market accuracy you can't substantiate; hallucinated citations become a credibility — and legal — problem.


## Why split the evaluation

```
query ──▶ [ retriever ] ──chunks──▶ [ generator ] ──▶ answer
            measure here:                measure here:
            recall, precision            grounding, attribution, citations
```

If end-to-end accuracy is low, the split tells you where to invest: better
chunking, embeddings, and reranking, or better prompting and grounding
constraints. Without it, you're guessing. This mirrors the general
[evals](../04-evals-observability/evals.md) discipline applied to
retrieval.

(Every long-context model release re-raises "is RAG dead?" The answer stays
no. As long as knowledge is larger than the window, changes faster than
retraining, or is permissioned per user, retrieval is how freshness, access
control, and cost control happen. What the question *should* prompt is
exactly this lesson: measure your retrieval separately, so you know what
it's contributing.)

## Retrieval metrics

You need labeled data: queries paired with the documents or chunks that
*should* be retrieved — a [golden set](../04-evals-observability/evals.md)
for retrieval.

- **Recall@k** — of all relevant chunks, how many appear in the top *k*?
  This is the ceiling on the whole system: **if the right chunk isn't
  retrieved, no prompt can fix the answer.** It's usually the first metric
  to optimize.
- **Precision@k** — of the top *k* retrieved, how many are actually
  relevant? Low precision means the
  [context](../00-foundations/context-engineering.md) is noisy, the
  generator gets distracted, and you pay for junk tokens.
- **MRR / nDCG** — rank-aware metrics: is the relevant chunk near the *top*,
  not just present? These matter because of
  [lost-in-the-middle](../00-foundations/context-engineering.md), and
  because [reranking](./rag-architecture.md) is judged on ordering.
- **Context recall vs. context precision** — recall asks did we get enough
  to answer; precision asks how much of what we got was needed. This is the
  classic recall/precision tension.

Use these to tune chunk size, k, hybrid weighting, and reranking directly —
each metric points at a specific stage.

## Generation-over-retrieval metrics

Even with perfect retrieval, the model can ignore or misuse the context.

- **Grounding / faithfulness** — is every claim in the answer *supported by
  the retrieved context*, not invented from parametric memory? Low
  grounding means hallucination despite good retrieval. Measure it by
  checking each answer claim against the provided chunks, often via an
  [LLM-as-judge](../04-evals-observability/evals.md) or NLI/entailment
  scoring.
- **Attribution** — can each claim be *traced to the specific source* that
  supports it? This is stronger than grounding: not just "supported
  somewhere" but "supported *by this citation*."
- **Citation quality** — are the citations (a) **present** where claims
  need them, (b) **correct** — the cited source actually supports the
  claim, not a hallucinated or mismatched reference — and (c) **complete**,
  with no unsupported claims left uncited?
- **Answer relevance / completeness** — does the answer actually address
  the question, using the retrieved material?

A useful framing is the "RAG triad": **context relevance** (retrieval),
**groundedness** (answer ⊆ context), and **answer relevance** (answer ⊆
question). All three must hold.

## How to actually run these

1. **Build a retrieval golden set** — representative queries with labeled
   relevant chunks. Include hard cases: exact-identifier lookups,
   paraphrases, multi-hop, "answer not in corpus."
2. **Score retrieval offline** (recall@k, precision@k, nDCG) on every
   index, chunking, embedding, or reranker change. It's cheap,
   deterministic, and fast to iterate.
3. **Score grounding and attribution** with an
   [LLM judge](../04-evals-observability/evals.md) against a rubric,
   spot-validated by humans. Calibrate the judge before trusting it.
4. **Track freshness explicitly** — include time-sensitive queries whose
   correct answer changes, to catch
   [stale-index](./rag-architecture.md) regressions.
5. **Gate changes in CI** so a chunking tweak that quietly drops recall
   can't ship.

## Tradeoffs & what each metric pushes

| If this is low… | Likely cause | Fix |
| --- | --- | --- |
| Recall@k | Chunking/embedding/recall | Hybrid search, better embedder, more overlap |
| Precision@k | Too many/loose results | Reranking, tighter filters, lower k |
| nDCG/MRR | Bad ordering | Reranking |
| Grounding | Model ignoring context | Cite-from-context prompt, "say I don't know" |
| Attribution/citations | Weak provenance | Tag chunks with source ids; enforce citation |

Don't chase recall to 100%. Beyond "enough," extra chunks hurt precision,
grounding, and cost. The objective is the *right* context, not the *most*.

## Failure modes

- **Grading only end-to-end** — you can't tell whether retrieval or
  generation is the problem, so you fix the wrong one.
- **Hallucinated citations** — the answer cites a source that doesn't
  support the claim. It reads authoritative but is wrong. A
  citation-correctness eval catches it.
- **Recall regressions hidden by the LLM** — a strong model papers over
  weak retrieval using parametric knowledge, inflating accuracy while
  grounding silently drops.
- **Stale golden set** — labels drift from the live corpus. Refresh them.
- **Untrusted judge** — an uncalibrated LLM judge for grounding gives false
  confidence.

## Practitioner checklist

- [ ] Do you measure retrieval (recall/precision/nDCG) *separately* from answers?
- [ ] Is there a labeled retrieval golden set, including "answer not in corpus"?
- [ ] Do you score grounding and attribution, not just answer correctness?
- [ ] Are citations checked for presence, correctness, and completeness?
- [ ] Is your LLM grounding-judge calibrated against human labels?
- [ ] Do retrieval evals gate index/chunking/embedding/reranker changes in CI?
- [ ] Do time-sensitive queries guard against freshness regressions?

## Related lessons

- [RAG architecture](./rag-architecture.md)
- [Evals](../04-evals-observability/evals.md)
- [Context engineering](../00-foundations/context-engineering.md)
- [Observability](../04-evals-observability/observability.md)
- [Production failure modes](../06-strategy-tradeoffs/production-failure-modes.md)
