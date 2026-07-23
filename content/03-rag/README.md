# Module 03 · RAG & retrieval

Retrieval-Augmented Generation grounds a model in *your* data — docs, tickets, code,
records the model never saw in training and that change every day. Done well, it's how
you get current, attributable, domain-specific answers without retraining. Done badly,
it's a confident model reciting the wrong or stale passage.

- [**RAG architecture**](./rag-architecture.md) — the pipeline: chunking, embeddings,
  hybrid search, reranking, and freshness. Where quality is won or lost.
- [**Retrieval evals**](./retrieval-evals.md) — measuring it: recall, precision,
  grounding, attribution, and citation quality. You cannot tune what you don't measure.

RAG is applied [context engineering](../00-foundations/context-engineering.md): the
retriever decides what occupies the window, and the generator can only be as good as
what the retriever found. The two lessons here are a matched pair — build the pipeline,
then prove it works.


## Connects to other tracks

- [What is a knowledge graph?](../../knowledge-graphs/what-is-a-knowledge-graph.md) — structured retrieval and GraphRAG.
- [Retrieval & codebase understanding](../../harness-engineering/phases/13-retrieval-and-codebase-understanding/README.md) — the same retrieval stack at repo scale.
- [Context & memory in agents](../../agentic-ai/context-and-memory.md) — retrieval as the agent's working memory.

**📌 Close out the module:** [Recap & real-world examples](./recap.md) — war stories from production plus the key takeaways.

---

← Previous: [02 · Reliable Outputs](../02-reliable-outputs/README.md) ·
→ Next: [04 · Evals & Observability](../04-evals-observability/README.md)
