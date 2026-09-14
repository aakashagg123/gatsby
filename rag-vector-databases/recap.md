# RAG & vector databases — recap & real-world examples

*Part of [RAG & vector databases for the product leader](./README.md)*

## Real-world examples & war stories

**The support bot that invented a policy (2025).** Users of an AI coding tool were
mysteriously logged out; the company's AI support agent confidently explained it was
"expected behaviour under a new login policy" that never existed. Users cancelled, the
company apologized. 🎯 *Takeaway:* a closed-book model answering from memory
[hallucinates your own business](./why-rag.md). Grounding the bot in the actual, current
support docs — with a path to say "I don't have that" — is the difference between a helpful
answer and a churn event.

**"Just search our docs" that couldn't find the obvious doc.** A recurring internal-tool
story: a RAG assistant fails to answer a question whose answer is plainly in the handbook.
The model gets blamed; the cause is upstream — the handbook was
[chunked](./chunking-and-ingestion.md) mid-section so no chunk contained the whole answer,
or retrieval was pure-semantic and the query hinged on an exact term. 🎯 *Takeaway:*
[retrieval quality](./retrieval-quality.md), not model IQ, is the ceiling — and you only see
it if you measure recall.

**The stale-index incident.** A team ships a RAG feature, it's accurate at launch, and
weeks later it's citing a retracted policy with a confident source link. Nobody built a
[delete/refresh path](./chunking-and-ingestion.md), so the retracted document still sat in
the index. 🎯 *Takeaway:* ingestion is a permanent product surface; a knowledge feature
that can't forget is worse than one that never knew, because people trust the citation.

**Microsoft GraphRAG (2024).** Microsoft Research showed that vector-only RAG fails on
*global* questions ("what are the main themes in this corpus?") and multi-hop questions,
and that building a graph over the corpus with pre-summarized communities lets an LLM answer
both, with sources. It went from paper to product roadmaps within a year. 🎯 *Takeaway:*
[flat RAG has a definite edge](./graphrag-and-structured-retrieval.md); knowing the *shape*
of question it can't answer tells you when structure earns its cost — and when it's fashion.

**The "long context killed RAG" cycle.** Each time context windows jump, the claim returns
that you can drop retrieval and paste everything in. Teams that tried it on real corpora
hit the same wall: the bill scaled with document count × calls, latency ballooned, and
answers got *worse* as the relevant passage hid in the haystack. 🎯 *Takeaway:*
[long-context is a partner to RAG, not a replacement](./rag-vs-long-context-vs-finetuning.md)
— great when the knowledge is small and static, expensive and lossy when it isn't.

**Fine-tuning to teach facts.** A common expensive mistake: a team fine-tunes a model on
their knowledge base to "make it know our product," then discovers the facts are stale the
next release, can't be cited, and every update means retraining. 🎯 *Takeaway:*
[fine-tune for behaviour, retrieve for facts](./rag-vs-long-context-vs-finetuning.md) —
conflating the two burns money and trust.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [Why RAG?](./why-rag.md) | Open-book beats closed-book for private, fresh, citable knowledge | Can our answer point to a real, current source? |
| [Embeddings & semantic search](./embeddings-and-semantic-search.md) | Meaning becomes geometry; similar ≠ correct | Does retrieval find the right passage when the wording differs? |
| [Vector databases](./vector-databases.md) | The easy, commoditized part — filtering and freshness matter more than the math | How many vectors, filtered by what, at what latency — and did we try what we already run? |
| [Chunking & ingestion](./chunking-and-ingestion.md) | You can only find what you filed well | Can the right answer survive our chunking, and how fast does the index reflect change? |
| [Retrieval quality](./retrieval-quality.md) | Retrieval quality *is* RAG quality — measure it | What's our recall on real, hard questions? |
| [RAG vs. long-context vs. fine-tuning](./rag-vs-long-context-vs-finetuning.md) | Fine-tune for behaviour, retrieve for facts, long-context when it's small | Are we changing behaviour or supplying facts? |
| [Beyond flat RAG](./graphrag-and-structured-retrieval.md) | Retrieve structure when the answer is a connection or a summary | Are our failing questions multi-hop/global, or just tuned badly? |

**The through-line:** every lesson annotates one picture — the
[module knowledge graph](./README.md): a pipeline that turns your data into findable
passages, a retrieval step that hands the model the right ones, a quality loop that keeps it
honest, and a set of decisions (RAG vs. the alternatives, flat vs. structured) about *which*
retrieval to build. The teams who win with RAG aren't the ones with the fanciest vector
database — they're the ones who chunked with care, measured retrieval, paid the freshness
bill, and grounded every answer in a source they'd stand behind.

> **Walk-away question:** *"For our RAG feature: can I name the four jobs it needs, show its
> retrieval recall on hard questions, point to the delete/refresh path that keeps it
> current, and defend every answer with a citation a user could open — and do I know which
> questions it can't answer without structure?"*

If yes, you've built a knowledge product, not a demo. If not, you now know exactly which
lesson to reread — and where the deeper mechanics live, one spoke away in
[RAG architecture](../content/03-rag/rag-architecture.md) and
[Retrieval evals](../content/03-rag/retrieval-evals.md).
