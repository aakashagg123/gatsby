# RAG & vector databases — recap & real-world examples

*Part of [RAG & vector databases for the product leader](./README.md)*

## Real-world examples

**The support bot that invented a policy (2025).** Users of an AI coding tool were logged out without warning. The company's AI support agent explained that this was expected under a new login policy. The policy did not exist. Users cancelled before staff stepped in. 🎯 *Takeaway:* a model answering from memory [invents your own business](./why-rag.md). Grounding the bot in current support documents, with a path to say "I don't have that", is the difference between a helpful answer and lost customers.

**Contextual retrieval (2024).** Anthropic tested a simple change to ingestion: add a short note about the whole document to each chunk before embedding it. Failed retrievals in the top 20 fell by 35%. With keyword search added, they fell by 49%. With a reranker, by 67%. The same post says a knowledge base under about 200,000 tokens can often skip RAG and go in the prompt. 🎯 *Takeaway:* the biggest gains came from [chunking](./chunking-and-ingestion.md) and [retrieval](./retrieval-quality.md), not from a bigger model. And the first question is still [whether you need RAG](./when-to-use-rag.md).

**Microsoft GraphRAG (2024).** Microsoft Research showed that flat RAG struggles with global questions, such as "what are the main themes in this corpus?". Their method builds a graph over the corpus and writes summaries for clusters of related entities in advance. A model can then answer global questions from those summaries. 🎯 *Takeaway:* [flat RAG has a definite edge](./graphrag-and-structured-retrieval.md). Know which question shapes it cannot answer.

**"Lost in the middle" (2023).** Researchers at Stanford and elsewhere moved the passage that held the answer around a long prompt. Models often did best when it was at the start or end, and worse when it was in the middle. 🎯 *Takeaway:* a bigger window is not a free replacement for retrieval. [Fewer, better passages](./rag-vs-long-context-vs-finetuning.md) often beat everything at once.

**The stale-index pattern.** A common story in teams that ship RAG: the feature is accurate at launch, and weeks later cites a retracted policy with a confident source link. Nobody built a [delete path](./chunking-and-ingestion.md). In this module's Fernpay corpus, the retracted refund policy scores 0.927 against 0.936 for the current one. 🎯 *Takeaway:* ingestion is a permanent product surface. A feature that cannot forget is worse than one that never knew, because people trust the citation.

**Fine-tuning to teach facts.** Another common pattern: a team fine-tunes a model on its knowledge base to "make it know our product". The facts are stale by the next release, cannot be cited, and every update means retraining. 🎯 *Takeaway:* [fine-tune for behaviour, retrieve for facts](./rag-vs-long-context-vs-finetuning.md).

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [When to use RAG](./when-to-use-rag.md) | The shape of the answer picks the tool | Is this a passage, a number, a record, a document or a behaviour? |
| [Why RAG?](./why-rag.md) | Open book beats closed book for private, fresh, citable knowledge | Can our answer point to a real, current source, and refuse when there is none? |
| [Embeddings](./embeddings-and-semantic-search.md) | Meaning becomes geometry, and similar is not correct | Does retrieval find the right passage when the wording differs? |
| [Vector databases](./vector-databases.md) | The search is a commodity; filters and freshness decide | How many vectors, filtered by what, and do filtered queries return enough? |
| [Chunking and ingestion](./chunking-and-ingestion.md) | You can only find what you filed well | Can the answer survive our chunking, and how fast does the index follow changes? |
| [Retrieval quality](./retrieval-quality.md) | Retrieval quality is RAG quality, so measure it | What is our recall on hard questions, by type? |
| [RAG vs. long context vs. fine-tuning](./rag-vs-long-context-vs-finetuning.md) | Fine-tune for behaviour, retrieve for facts, send small knowledge whole | Does our cost grow with the corpus or with use? |
| [GraphRAG](./graphrag-and-structured-retrieval.md) | Retrieve structure when the answer is a connection, a summary or a count | Are our failing questions multi-hop, global or numeric? |
| [Building RAG](./building-rag-with-claude-code.md) | You set the contract and the gate; the agent fills in the stages | Which command proves retrieval works, and does the agent run it? |
| [RAG terms](./rag-terms.md) | Every term has a place on the pipeline | Which stage does this number measure? |

**The through-line.** Every lesson annotates one picture, the [module knowledge graph](./README.md). A pipeline turns your data into findable passages. Retrieval hands the model the right ones. A quality loop keeps it honest. And a set of decisions comes first: RAG or something simpler, flat or structured. The teams who win with RAG do not have the fanciest vector database. They chose RAG only where it fit, chunked with care, measured retrieval, paid the freshness bill, and grounded every answer in a source they would stand behind.

> **Walk-away question:** *"For our RAG feature: can I say why RAG beat the simpler options, show recall on hard questions by type, point to the delete path, and defend every answer with a citation a user could open?"*

## Test yourself

1. **A product manager asks for RAG so users can ask "how many invoices are overdue this month?". What do you recommend, and why?**
   <details><summary>Answer</summary>A database query or a tool call, not RAG. The answer is a count over rows. Top-k retrieval returns at most k chunks, so it cannot count past k, and a model reading them would give a confident wrong number. (<a href="./when-to-use-rag.md">Lesson 1</a>)</details>
2. **Your HR handbook is 35,000 tokens and changes twice a year. Every employee may see all of it. RAG or not?**
   <details><summary>Answer</summary>Not RAG. It is small, stable and the same for everyone, so none of the three deciding signals (too big, changes often, differs by user) holds. Put it in the prompt and use prompt caching. In the lesson's sketch, cached long context costs $106.50 per 10,000 questions against $61.50 for RAG, and needs no pipeline. (<a href="./when-to-use-rag.md">Lesson 1</a>)</details>
3. **Name the four jobs RAG does that a bare model cannot.**
   <details><summary>Answer</summary>Grounding (answering from real text), freshness (today's data without retraining), private knowledge (your data, never in a training set) and attribution (citing the source). (<a href="./why-rag.md">Lesson 2</a>)</details>
4. **Why is a similarity threshold alone a weak "I don't know" gate?**
   <details><summary>Answer</summary>Similarity scores do not track relevance well enough. In the Fernpay example, an off-topic weather question scores 0.301, and a real question about error E-4021 scores only 0.113. A threshold would refuse the real question and answer the off-topic one. Checking the keyword leg as well gets both right. (<a href="./why-rag.md">Lesson 2</a>)</details>
5. **The current refund policy scores 0.936 and the retracted one 0.927. What fixes this?**
   <details><summary>Answer</summary>A metadata filter on status, plus a delete path in ingestion. Embeddings cannot tell which version is in force, because the two texts are nearly identical. (<a href="./embeddings-and-semantic-search.md">Lesson 3</a>)</details>
6. **The team switches embedding models but keeps the old document vectors. What happens?**
   <details><summary>Answer</summary>Retrieval quietly breaks. Old and new vectors live in different spaces, so distances mean nothing. In the lesson's demo, recall@3 falls from 0.833 to 0.167 with no error. Changing models means re-embedding the whole corpus. (<a href="./embeddings-and-semantic-search.md">Lesson 3</a>)</details>
7. **What does an approximate nearest-neighbour index trade, and what is the dial?**
   <details><summary>Answer</summary>It trades a little recall for a lot of speed by checking only part of the vectors. The dial is how much it scans: lists probed in IVF, or ef_search in HNSW. In the demo, scanning 25% of the vectors found 95.5% of the true top 10. (<a href="./vector-databases.md">Lesson 4</a>)</details>
8. **A small tenant's searches return 1 result instead of 10. What is the likely cause?**
   <details><summary>Answer</summary>The filter is applied after the approximate index scan. The scan returns the nearest candidates across all tenants, and few belong to the small one. Fixes include iterative index scans (pgvector 0.8.0 and later), a partial index, or exact search within the tenant. (<a href="./vector-databases.md">Lesson 4</a>)</details>
9. **Why did 80-character chunks answer only 7 of 12 questions while section chunks answered 11?**
   <details><summary>Answer</summary>Blind cuts sliced two answer facts in half, so no chunk held them whole. Fixed chunks also lost the titles and headings, which carried many of the matching words. (<a href="./chunking-and-ingestion.md">Lesson 5</a>)</details>
10. **Keyword search scores 0.667 recall@3, vector search 0.833 and hybrid 0.917. Why does hybrid win?**
    <details><summary>Answer</summary>Each leg covers the other's blind spot. Keyword search finds exact codes and misses paraphrases. Vector search finds paraphrases and misses codes. Reciprocal rank fusion combines the two lists. (<a href="./retrieval-quality.md">Lesson 6</a>)</details>
11. **At what corpus size does cached long context stop being an option, and why does RAG's cost not grow with the corpus?**
    <details><summary>Answer</summary>When the corpus no longer fits the context window: 2.5 million tokens does not fit a 1 million token window. RAG sends the same few retrieved chunks per question, so its cost depends on use, not on corpus size. (<a href="./rag-vs-long-context-vs-finetuning.md">Lesson 7</a>)</details>
12. **"Which customers are exposed to the recall at Kestrel Metals?" Why does flat RAG fail, and what works?**
    <details><summary>Answer</summary>The answer is a chain: supplier, parts, products, customers. No chunk holds the chain, so flat retrieval found one of three customers. A graph walk that follows the links finds all three. (<a href="./graphrag-and-structured-retrieval.md">Lesson 8</a>)</details>
13. **In a Claude Code build, which three things should a person own rather than the agent?**
    <details><summary>Answer</summary>The eval questions, the permission rules, and the bar the eval must pass. The agent must not write the questions it is graded on. Enforce the bar with a hook or CI, because CLAUDE.md is advice. (<a href="./building-rag-with-claude-code.md">Lesson 9</a>)</details>
14. **In pgvector, the index uses vector_l2_ops and the query orders by the <=> operator. What goes wrong?**
    <details><summary>Answer</summary>The operator class does not match the cosine distance operator, so Postgres cannot use the index, and every search scans the whole table. Use vector_cosine_ops with <=>. (<a href="./building-rag-with-claude-code.md">Lesson 9</a>)</details>
15. **A review says "the RAG feature is 90% accurate". What do you ask?**
    <details><summary>Answer</summary>Which stage that measures, on which questions, and how. Recall@k measures retrieval. Faithfulness and answer relevance measure the answer. A low score in each needs a different fix. (<a href="./rag-terms.md">Lesson 10</a>)</details>

## Sources

- AI Incident Database, [Incident 1039](https://incidentdatabase.ai/cite/1039/), April 2025: an AI support agent invented a login policy. Read 2026-10.
- Anthropic, [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval), 19 September 2024. Read 2026-10.
- Edge et al., *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*, Microsoft Research, 2024 ([arxiv.org/abs/2404.16130](https://arxiv.org/abs/2404.16130)).
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, Transactions of the ACL, 2024 ([arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)).
- The stale-index and fine-tuning patterns are composites, not single documented incidents. The Fernpay numbers come from `rag-vector-databases/code/`.
