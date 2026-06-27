# RAG Architecture: Chunking, Embeddings, Hybrid Search, Reranking, and Freshness

*Part of [03 · RAG & Retrieval](./README.md)*

## TL;DR

RAG is a pipeline, and quality is bounded by its weakest stage. **Chunking** decides
what a retrievable unit *is*; **embeddings** decide how meaning is matched; **hybrid
search** combines keyword and vector recall; **reranking** sharpens precision before
the prompt; **freshness** keeps the index from lying. The generator can only answer
from what retrieval surfaces — so most "the LLM is wrong" RAG bugs are actually
retrieval bugs. Optimize retrieval first, generation second.

> 🧭 **In plain terms**
>
> **RAG** is giving the AI an open-book exam instead of asking it to answer from memory: it looks up your actual documents before replying. The grade depends almost entirely on whether it found the right page — good filing, good search, and up-to-date files matter more than the model's raw IQ. That's why most 'the AI was wrong' moments are really 'it grabbed the wrong page,' and why fixing retrieval beats endlessly tweaking the prompt.


<!--sep-->

> 🎯 **For the AI-native PM**
>
> **Why it matters** — Most "the AI gave a wrong answer" bugs are actually *retrieval* bugs, not model bugs. RAG quality is where grounded, current, citeable answers come from — the core of enterprise trust.
>
> **What it changes in your decisions** — What data you invest in indexing, your freshness SLAs, and whether you can promise citations.
>
> **Ask your eng team** — *"When an answer is wrong, is it because we never retrieved the right source in the first place?"*
>
> **Product risk if ignored** — You blame the model and tune prompts for months while the real defect — retrieval — goes unfixed.


## The pipeline

```
INDEX TIME:   documents ──▶ chunk ──▶ embed ──▶ vector store (+ keyword index)
                                  └──▶ keep fresh (re-index on change)

QUERY TIME:   query ──▶ (rewrite) ──▶ hybrid search (dense + lexical)
                    ──▶ rerank top-N ──▶ trim to budget ──▶ context + cite ──▶ generate
```

This is [context engineering](../00-foundations/context-engineering.md) in motion:
retrieval is *how the right information gets into the window*.

## Chunking — define the retrievable unit

- **Why it matters:** too big → chunks dilute relevance and waste tokens; too small →
  you lose the context needed to answer. Chunk size is a recall/precision dial.
- **Strategies:** fixed-size with **overlap** (simple, robust); **structure-aware**
  (split on headings/sections/functions — usually better because it respects meaning);
  **semantic chunking** (split where topic shifts).
- **Carry metadata** on every chunk: source id, title, section, timestamp, tenant,
  permissions. Metadata powers [citations](./retrieval-evals.md), [freshness](#freshness),
  and [tenant filtering](../05-safety-multitenancy/multi-tenant-isolation.md).
- **Tabular/structured data** often shouldn't be free-text chunked at all — consider
  text-to-SQL or structured retrieval instead.

## Embeddings — how meaning is matched

- Embeddings map text to vectors so semantic nearness = vector nearness. Choice of
  model sets your semantic ceiling.
- **Match query and document embeddings** (same model/space). **Domain fit matters** —
  a general embedder may miss jargon, code, or multilingual content; sometimes a
  domain-tuned embedder is the highest-leverage change.
- **Asymmetric search:** short queries vs. long passages benefit from models trained
  for that (query/passage encoders).
- **Cost/latency:** embedding dimension and model size trade retrieval quality against
  storage and query speed. Re-embedding the whole corpus on a model change is a real
  migration cost — version your embeddings.

## Hybrid search — recall from two angles

Dense (vector) search captures *meaning* but can miss exact terms (IDs, error codes,
rare names, acronyms). Lexical search (BM25/keyword) nails exact matches but misses
paraphrase. **Hybrid** runs both and fuses results (e.g. Reciprocal Rank Fusion or
weighted scores).

- Hybrid almost always beats either alone, especially for technical/enterprise corpora
  full of exact identifiers.
- Add **metadata filters** (tenant, date, doc type, ACL) as hard constraints *before*
  ranking — both for relevance and for [isolation/security](../05-safety-multitenancy/multi-tenant-isolation.md).

## Reranking — precision before the prompt

First-stage retrieval optimizes recall (cast a wide net, top-50). A **cross-encoder
reranker** then scores each (query, chunk) pair jointly for true relevance and keeps
the top few.

- **Why:** cheaply pull many candidates, then spend a precise model on a short list.
  This is usually the single biggest precision win in a RAG system.
- **Effect on the generator:** fewer, better chunks reduce distraction and
  [lost-in-the-middle](../00-foundations/context-engineering.md) failures, and cut
  [prefill cost](../01-inference-internals/prefill-vs-decode.md).
- **Cost:** an extra model call and latency — but on a small candidate set, and it
  often lets you *shrink* the context you send, paying for itself.

## Freshness — keep the index honest

A retrieval index is a cache of your data and goes stale the moment the source changes.
- **Incremental indexing / CDC:** re-embed and upsert on create/update/delete; don't
  full-rebuild nightly if data changes continuously.
- **Deletions and tombstones:** removed source docs must leave the index, or you'll
  cite deleted/retracted content.
- **Recency signals:** timestamp chunks and let ranking prefer recent versions; expire
  or down-weight stale ones.
- Freshness failures mirror [semantic-cache staleness](../01-inference-internals/prompt-vs-semantic-caching.md):
  a confident answer from outdated data.

## Generation & attribution

- Pass reranked, trimmed chunks **with source tags** and instruct the model to answer
  *from the context* and **cite** sources — enabling [grounding and citation evals](./retrieval-evals.md).
- Handle "**not in the context**" explicitly: the model should say it doesn't know
  rather than fill the gap from parametric memory (a hallucination guard).

## Tradeoffs

| Stage | Dial toward recall | Dial toward precision/cost |
| --- | --- | --- |
| Chunk size | Smaller, more overlap | Larger, structure-aware |
| Retrieval k | Higher k | Lower k + reranking |
| Search type | Hybrid + loose filters | Tight filters |
| Reranking | (skip for speed) | Add for precision |
| Freshness | Frequent re-index | Cheaper, staler index |

## Failure modes

- **Right answer never retrieved** — chunking/embedding/recall problem; no prompt fixes
  it. Measure [retrieval recall](./retrieval-evals.md).
- **Answer buried in noise** — too many chunks, no reranking; distraction degrades the
  answer.
- **Stale/deleted content cited** — freshness/deletion gap.
- **Exact-match misses** — dense-only search can't find an error code; add lexical.
- **Cross-tenant leakage** — missing ACL/tenant filter returns another customer's docs
  (see [isolation](../05-safety-multitenancy/multi-tenant-isolation.md)).

## Practitioner checklist

- [ ] Is chunking structure-aware with rich metadata (source, time, tenant, ACL)?
- [ ] Do query and document embeddings share a model/space, fit to your domain?
- [ ] Is search hybrid (dense + lexical) with metadata pre-filters?
- [ ] Is there a reranking stage feeding a small, trimmed context?
- [ ] Is the index updated incrementally, with deletions honored?
- [ ] Does the prompt enforce cite-from-context and "say I don't know"?
- [ ] Do you measure retrieval quality separately from answer quality?

## Related lessons

- [Retrieval evals](./retrieval-evals.md)
- [Context engineering](../00-foundations/context-engineering.md)
- [Prompt vs. semantic caching](../01-inference-internals/prompt-vs-semantic-caching.md)
- [Multi-tenant isolation](../05-safety-multitenancy/multi-tenant-isolation.md)
- [Fine-tuning vs. ICL vs. RAG vs. distillation](../06-strategy-tradeoffs/finetune-vs-icl-vs-rag.md)
