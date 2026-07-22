# Knowledge graphs — recap & real-world examples

*Part of [Knowledge graphs for the product leader](./README.md)*

## Real-world examples & war stories

**Google's "things, not strings" (2012).** Google launched its Knowledge Graph to stop
matching text and start knowing what text *refers to* — entities with identities,
properties, and relationships, powering the info panels beside search results. It gave
the field its name and its cleanest slogan. 🎯 *Takeaway:* the shift that mattered
wasn't a database — it was [treating identity as the product](./what-is-a-knowledge-graph.md).
The moment "jaguar" became three *things* instead of one string, whole product surfaces
became possible.

**The Panama Papers (2016).** Handed 11.5 million leaked documents, the ICIJ loaded
extracted entities — companies, officers, addresses — into a graph database and let
hundreds of journalists *traverse*: from a politician to a shell company to a shared
registered agent to the next shell. Connections no keyword search could surface fell
out as paths. 🎯 *Takeaway:* [traversal is a capability, not a report](./reasoning-and-analytics.md)
— when the question is "how is A connected to B?", the graph doesn't just answer
faster; it answers questions you couldn't previously ask. (Note also what did the heavy
lifting first: extraction and [entity resolution](./building-the-graph.md) across
millions of messy documents.)

**Amazon's Product Graph (2018→).** Amazon set out to build an authoritative graph of
products and everything about them — brands, attributes, compatibility, variants —
feeding search, recommendations, and Alexa answers. The published lesson: the hard
science was never storage; it was extraction from messy seller text and reconciling
conflicting sources at catalog scale. 🎯 *Takeaway:* exactly the
[80% claim](./building-the-graph.md) — the pipeline is the product. Even with
world-class infrastructure, the budget and the breakthroughs live in extraction and
resolution.

**LinkedIn's Economic Graph.** LinkedIn frames its entire asset as one graph — members,
companies, skills, jobs, schools — and its features as traversals of it: "people you
may know" is [link prediction](./reasoning-and-analytics.md); recruiter search is
multi-hop filtering; economic research is aggregate graph analytics. 🎯 *Takeaway:*
when [the relationships are the product](./what-is-a-knowledge-graph.md), the graph
isn't infrastructure behind the product — it *is* the product, and every feature is a
different query against the same compounding asset.

**NASA's lessons-learned graph.** NASA connected decades of siloed mission documents,
incident reports, and engineering lessons into a knowledge graph so an engineer
designing a component can find what past programs learned — across programs, decades,
and vocabularies that never matched. 🎯 *Takeaway:* the
[ontology work is organizational](./ontologies-and-data-modeling.md) — the technical
graph was the easy half; agreeing what a "lesson," an "anomaly," and a "subsystem"
mean across generations of programs was the actual project.

**Microsoft GraphRAG (2024).** Microsoft Research showed that vector-only RAG fails on
*global* questions ("what are the main themes in this corpus?") and multi-hop
questions — and that building a graph over the corpus, detecting communities, and
pre-summarizing them lets an LLM answer both, with sources. The pattern went from
paper to product roadmaps in about a year. 🎯 *Takeaway:* the
[graph-LLM marriage](./knowledge-graphs-and-llms.md) is not vendor fog — it targets
measured, structural failures of similarity-only retrieval. But adopt it the way the
lesson says: after your evals show *those* failures, not before.

**The enterprise graveyard (ongoing).** Every data leader knows one: the two-year
enterprise-ontology program with a 400-page model and no shipped feature; the pilot
that wowed and then decayed unstewarded; the "graph initiative" renamed twice and
quietly absorbed into a BI team. These don't make conference talks, which is why the
pattern repeats. 🎯 *Takeaway:* the failures are portfolio failures —
[no killer query, no visible feature, no steady state](./knowledge-graphs-as-a-product.md)
— and the [quiet death](./governance-quality-and-trust.md) arrives without a
postmortem. Sequencing and stewardship, not technology, decide survival.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What is a knowledge graph?](./what-is-a-knowledge-graph.md) | Things, not strings — connections made explicit and queryable | Which valuable questions are multi-hop across our systems? |
| [Ontologies & data modeling](./ontologies-and-data-modeling.md) | The ontology is a product contract, negotiated not specified | What can this ontology never answer — and did we choose that? |
| [Building the graph](./building-the-graph.md) | The pipeline is the product; entity resolution is the boss fight | Who reviews the low-confidence matches every week? |
| [Storage & querying](./storage-and-querying.md) | Query shapes pick the store; benchmark boring first | What's our deepest traversal, at what latency, in which feature? |
| [Reasoning & analytics](./reasoning-and-analytics.md) | Five families, one trust gradient — paths explain, predictions suggest | Is this answer traversed, inferred, or guessed — and does the UX say so? |
| [Knowledge graphs & LLMs](./knowledge-graphs-and-llms.md) | The graph grounds the model; the model builds the graph — through review | Can every AI claim cite fact, source, and permission? |
| [Governance, quality & trust](./governance-quality-and-trust.md) | Trust is manufactured: provenance, metrics, permissions, owners | Can we show why the graph asserts this — and who may see it? |
| [Knowledge graphs as a product](./knowledge-graphs-as-a-product.md) | Fund features, sequence adjacent domains, let the asset compound | What ships in two quarters that a user will notice? |

**The through-line:** every lesson is an annotation on the
[module's own knowledge graph](./README.md): an ontology gives meaning, a pipeline
manufactures the asset, storage serves it, reasoning and LLMs cash it into features,
governance keeps it believable, and the product loop funds the next domain. The
organizations that win with knowledge graphs aren't the ones with the biggest node
counts or the fanciest databases — they're the ones that picked killer queries, paid
the unglamorous resolution-and-curation bill, showed their work on every fact, and let
the asset compound one adjacent domain at a time.

> **Walk-away question:** *"For my knowledge graph: can I name the killer query, the
> first visible feature and its quarter, the steward behind each domain, the four
> quality numbers on the dashboard, the provenance chain behind any AI answer — and
> the moat in one sentence that doesn't mention a database?"*

If yes — you're not buying a graph, you're building a compounding knowledge asset. If
no, you now know exactly which lesson to reread.
