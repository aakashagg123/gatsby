# Technical sense for AI systems

*Part of [Technical product sense for the AI PM](./README.md)*

## TL;DR

An AI feature is a normal distributed system — everything in this module still applies. It has
one unusual component wired in: a **probabilistic model**, often a third-party API, that's
slow, priced per token, and occasionally confidently wrong. Technical sense for AI means
knowing the **anatomy** of that system (guardrails → retrieval → prompt → model → validate →
tools), where its latency and cost live, how it fails, and how you'd ever *know* it's working.
That's why **evals and observability** aren't optional extras — they are the reliability of the
feature. The model is the easy part to add. The system around it is the product.

> 🎯 **For the AI PM**
>
> **Why it matters** — This is where every prior lesson converges. Architecture, APIs, data,
> latency, reliability, and debt all take on an AI-specific twist at once. Miss the system and
> you've shipped a demo, not a product.
>
> **What it changes in your decisions** — Scope the feature to what the system can make
> *reliable and affordable*, not just what the model can do in a demo. Fund the unglamorous
> parts — retrieval quality, evals, observability, guardrails — as the feature itself.
>
> **Ask yourself** — *"What's the full path around the model call, and which part — not the
> model — is most likely to make this feature fail?"*
>
> **Risk if ignored** — The classic AI-product failure: magical in the demo, untrustworthy,
> unobservable, and unaffordable in production.

## The anatomy of an AI feature

The model call is one box in a pipeline. The product lives in the boxes around it:

```mermaid
flowchart LR
  U["User input"] --> G["Guardrails<br/>(input checks)"]
  G --> R["Retrieval<br/>(fetch context)"]
  R --> P["Prompt assembly"]
  P --> M["Model call"]
  M --> V["Validate / parse"]
  V -->|valid| T["Tools / actions"]
  V -->|invalid| P
  T --> O["Response to user"]
  M -.->|traces, tokens, cost, latency| OBS[["Observability + evals"]]
  V -.-> OBS
  T -.-> OBS
```

- **Guardrails (in)** — Check and sanitize input. Block prompt injection and
  out-of-scope requests before they reach the model.
- **Retrieval** — Fetch the right context (documents, data) so the model answers from
  *your* facts, not its memory. Quality here caps answer quality — see the AI
  Engineering track's [RAG architecture](../content/03-rag/rag-architecture.md).
- **Prompt assembly** — Combine instructions, context, and input within the model's
  token limit. This is
  [context engineering](../content/00-foundations/context-engineering.md).
- **Model call** — The probabilistic step: slow, per-token cost, non-deterministic.
- **Validate / parse** — Check the output is well-formed and safe. Loop back to repair
  if it isn't. Never trust raw model output downstream.
- **Tools / actions** — The model triggers real operations, which must be
  [idempotent and bounded](./apis-and-contracts.md).
- **Observability + evals** — Every step emits traces, tokens, cost, and latency, and
  evals grade quality continuously. Without this, you are flying blind.

## The four technical dimensions, AI-flavoured

- **Latency & cost** — The model call costs seconds and per-token dollars, and it's
  usually the dominant hop. Levers: [streaming](./latency-scale-performance.md) for
  perceived speed, a smaller or quantized model, caching, and retrieving less. Cost
  per call times volume is a unit-economics decision, not an afterthought.
- **Reliability** — The model API rate-limits, times out, and returns bad answers with
  a 200. You need the whole [reliability toolkit](./reliability-and-failure.md) *plus*
  a plan for wrong-but-well-formed output: validation, "I don't know," and a non-AI
  fallback.
- **Data** — The feature is only as good as its retrieval corpus, its examples, and
  its permission model.
  [Where the data lives and who can see it](./data-and-the-data-model.md) is the
  product.
- **Debt** — Prompt spaghetti, no evals, untracked model/prompt versions, and a
  fragile data pipeline are the [debt](./tech-debt-and-estimation.md) unique to AI.
  It's invisible until quality regresses and nobody can say why.

## Measuring "is it working?"

With deterministic software, correct is correct. With a model, quality is a distribution, so
you have to measure it. An **eval** is a graded set of representative and adversarial cases
the feature must pass, run continuously so regressions surface before users find them. Pair it
with **observability** — traces of each step's tokens, cost, latency, and errors — so when
quality drops you can see *which box* caused it. Together these are the AI Engineering track's
[evals](../content/04-evals-observability/evals.md) and
[observability](../content/04-evals-observability/observability.md) lessons. For an AI feature
they *are* its reliability.

## Scope to the reliable frontier

Model capability is **jagged** — brilliant at some tasks, unreliable at adjacent ones. The
highest-leverage technical-product decision is **scoping**: point the model at the jobs it does
reliably and inside your cost/latency budget, and use a deterministic path (or a human) for the
jobs where a wrong answer is costly. Often the best AI product uses the model for the delightful
20% and boring, correct machinery for the 80% that must not fail.

## A worked pass: the napkin for "AI answers support tickets"

Before the roadmap, do the arithmetic. Proposal: draft answers for inbound support
tickets. Volume: 60,000 tickets/month. Per ticket, the context is the ticket thread
plus retrieved help-center passages — call it 4,000 input tokens at p50. But check p95
too: long threads run 12,000, and cost scales with usage, so price the distribution,
not the average. Output is about 500 tokens. At list prices for a mid-tier model,
that's roughly a few cents per ticket — say $2–4k/month before caching. The system
prompt and help-center boilerplate are identical across tickets, so prompt caching
should cut real input cost hard. Verify the hit rate; don't assume it.

Against what baseline? If a drafted answer saves an agent 2 minutes at a loaded
$40/hour, that's about $1.33 saved per ticket used — but only for tickets where the
draft is *accepted*. Now the number that rules them all: acceptance rate. At 70%
acceptance the feature prints money. At 25% it's a cost line plus an annoyance. That's
why the first build artifact isn't the prompt — it's the eval: 100 real tickets,
graded drafts, a pass bar agreed with the support lead. The napkin tells you whether to
start. The eval tells you whether to ship. Neither requires writing a line of code, and
both are the PM's job.

## Failure modes

- **Model-shaped thinking** — Treating "the model" as the product and ignoring the
  pipeline that makes it trustworthy.
- **No evals / no observability** — You can't tell if the feature works or why it
  regressed.
- **Unbounded cost/latency** — A feature that's delightful at demo scale and
  unaffordable or too slow in production.
- **Trusting raw output** — No validation, so a malformed or wrong answer flows
  straight to the user or an action.
- **Over-scoping** — Pointing the model at jobs outside its reliable frontier, where
  failure is costly and invisible.

## Practitioner checklist

- [ ] Can I draw the full pipeline around the model call, not just the call?
- [ ] Do I know the cost and latency per call at expected volume?
- [ ] Is there validation, a wrong-answer path, and a non-AI fallback?
- [ ] Are evals and observability in place — can we tell if it works and why it broke?
- [ ] Is the feature scoped to the model's reliable frontier, with the risky parts guarded?

## Related lessons

- [How systems are built](./how-systems-are-built.md)
- [Reliability & failure](./reliability-and-failure.md)
- [Tech debt & estimation](./tech-debt-and-estimation.md)
- [Recap & real-world examples](./recap.md)
