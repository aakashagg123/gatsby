# Question bank: 50 design questions mapped to the lessons

*Part of [System design for the technical PM](./README.md)*

*Last reviewed: 2026-10 · Volatility: stable*

## TL;DR

This page is a practice list. It holds 50 questions that come up in design reviews and interviews, grouped by the kind of knowledge each one tests. Each row says how hard the question is and where this track answers it. **Read** means a lesson covers it. **Partly** means a lesson covers part of it. **Planned** means a later lesson will cover it. At the time of writing, 34 are covered, 3 are partly covered and 13 are planned.

The best way to use it is recall. Pick a question. Answer it aloud, on a blank page, in about five minutes. Then read the lesson and mark what you missed. Recalling an answer teaches more than reading one again.

> 🎯 **For the technical PM**
>
> **Why it matters** — The questions show what engineers are expected to know. They also show the gaps in your own mental map, before a design review finds them for you.
>
> **What it changes in your decisions** — You can tell which questions your team has answered with evidence and which they have answered with a favourite tool.
>
> **Ask your eng team** — *"Which three of these questions would we struggle to answer for our own system?"*
>
> **Risk if ignored** — Gaps you did not know you had show up first in production.

## The mental model: one map from question to lesson

Think of the list as an index into the track. The levels are a guide: junior questions test fundamentals, mid questions test core designs, senior questions test depth and trade-offs. A strong answer at any level states its assumptions, gives numbers and names what happens when something fails.

## Mechanics

### How the list is organized

The rows run in five groups, in order. Questions 1 to 10 cover building blocks. Questions 11 to 20 cover data and distributed systems. Questions 21 to 34 are classic product designs. Questions 35 to 42 cover ML and GenAI systems. Questions 43 to 50 cover reliability and operations.

### The bank

| # | Question | Level | Where |
| --- | --- | --- | --- |
| 1 | What does a design discussion test, and how do you spend 45 minutes? | Junior | [Read](./foundations-and-framework.md) |
| 2 | Why prefer stateless services and horizontal scaling? | Junior | [Read](./foundations-and-framework.md) |
| 3 | How do L4 and L7 load balancers differ, and what do health checks do? | Junior | [Read](./traffic-caching-apis-and-storage-choice.md) |
| 4 | Which caching strategies exist, and how do you avoid a stampede? | Mid | [Read](./traffic-caching-apis-and-storage-choice.md) |
| 5 | What does a CDN do, and when is it the right tool? | Junior | [Read](./traffic-caching-apis-and-storage-choice.md) |
| 6 | How do you choose between SQL and NoSQL? | Mid | [Read](./traffic-caching-apis-and-storage-choice.md) |
| 7 | How do message queues differ from event logs, and what do the delivery guarantees mean? | Mid | [Read](./data-infrastructure.md) |
| 8 | How do you design an API: REST, gRPC, GraphQL, pagination, idempotency? | Mid | [Read](./traffic-caching-apis-and-storage-choice.md) |
| 9 | Estimate the load and storage for a Twitter-like service. | Mid | [Read](./foundations-and-framework.md) |
| 10 | Design a rate limiter and distribute it. | Mid | [Read](./core-building-blocks.md) |
| 11 | Compare leader-follower, multi-leader and leaderless replication. | Mid | [Read](./distributed-data-and-consistency.md) |
| 12 | How do you shard a database, and what goes wrong? | Mid | [Read](./distributed-data-and-consistency.md) |
| 13 | Explain consistent hashing and virtual nodes. | Mid | [Read](./core-building-blocks.md) |
| 14 | What do CAP and PACELC say? | Mid | [Read](./distributed-data-and-consistency.md) |
| 15 | Explain the main consistency models with an example. | Senior | [Read](./distributed-data-and-consistency.md) |
| 16 | How do quorum reads and writes work? | Senior | [Read](./core-building-blocks.md) |
| 17 | What is consensus, and where do Raft and Paxos fit? | Senior | [Read](./distributed-data-and-consistency.md) |
| 18 | How do you keep data consistent across services: 2PC, sagas, outbox? | Senior | [Read](./distributed-data-and-consistency.md) |
| 19 | How do you generate unique IDs at scale? | Mid | [Read](./core-building-blocks.md) |
| 20 | Why can you not trust wall-clock time? | Senior | [Read](./distributed-data-and-consistency.md) |
| 21 | Design a URL shortener. | Mid | [Read](./web-scale-services.md) |
| 22 | Design a chat system. | Senior | [Read](./real-time-systems.md) |
| 23 | Design a news feed. | Senior | [Read](./web-scale-services.md) |
| 24 | Design find-nearby-drivers for ride hailing. | Senior | [Read](./location-and-geo-services.md) |
| 25 | Design a payment system. | Senior | [Read](./transactional-and-financial.md) |
| 26 | Design a short-video upload and processing pipeline. | Senior | [Partly](./real-time-systems.md) |
| 27 | Design live streaming for tens of millions of viewers. | Senior | [Partly](./real-time-systems.md) |
| 28 | Design a like button that updates for everyone at global scale. | Mid | Planned |
| 29 | Design photo storage that serves a 15-year-old photo on demand. | Senior | [Partly](./storage-and-sync.md) |
| 30 | Design metrics collection and monitoring for thousands of servers. | Mid | [Read](./data-infrastructure.md) |
| 31 | Design search over a social graph. | Senior | Planned |
| 32 | Design a swipe-and-match system. | Mid | Planned |
| 33 | Design a delivery routing system. | Senior | Planned |
| 34 | Design a notification system. | Mid | [Read](./web-scale-services.md) |
| 35 | How does ML system design differ from classic system design? | Mid | Planned |
| 36 | Design a recommendation system for short videos. | Senior | Planned |
| 37 | Design ads click prediction. | Senior | Planned |
| 38 | Design product search ranking and listing classification. | Mid | Planned |
| 39 | Design reverse image search over 100 billion images. | Senior | Planned |
| 40 | Design an LLM chat service. | Senior | Planned |
| 41 | Design a platform that runs AI agents at scale. | Senior | Planned |
| 42 | How do you keep autonomous agents safe in production? | Senior | Planned |
| 43 | Reason about availability with SLIs, SLOs, SLAs and nines. | Junior | [Read](./numbers-and-formulas.md) |
| 44 | What should an observability setup include? | Mid | [Read](./reliability-and-operations.md) |
| 45 | Which resilience patterns prevent cascading failures? | Senior | [Read](./reliability-and-operations.md) |
| 46 | How do you deploy changes safely, including configuration? | Mid | [Read](./reliability-and-operations.md) |
| 47 | Design for regional failure: multi-region, RPO and RTO. | Senior | [Read](./reliability-and-operations.md) |
| 48 | How do you limit the blast radius of human error? | Mid | [Read](./reliability-and-operations.md) |
| 49 | What does a backup strategy that works look like? | Mid | [Read](./reliability-and-operations.md) |
| 50 | What happens when you type a URL and press Enter? | Junior | Planned |

### How to answer well

Use the same steps every time: scope the problem, estimate the load, sketch the design, go deep on the hardest part, and close with trade-offs and failure. The [foundations lesson](./foundations-and-framework.md) has the full framework.

## Tradeoffs and decisions

- **Breadth vs. depth.** Cover many questions lightly or a few deeply. Depth shows in the senior rows.
- **Memorized answers vs. reasoning.** An answer you can derive from numbers beats one you recall.
- **Planned rows.** Treat them as a to-do list for your own study until a lesson covers them.

## Failure modes

- **Reading instead of recalling.** The answer feels familiar, so you think you know it.
- **Skipping numbers.** A design with no estimate cannot be judged.
- **Naming tools.** "Use Kafka" is not a design until you say which problem it solves.
- **Ignoring failure.** A design that never says what breaks.

## Under the hood

The levels and the coverage column are a plain table in this file. Each link points to the lesson with the closest answer. When a new lesson ships, change the matching row from **Planned** or **Partly** to **Read**. The code behind most answers is in `system-design/code/`. Run `python3 system-design/code/test_examples.py` to check all of it.

## Worked example: answering question 9

*The numbers come from `system-design/code/estimator.py`.*

The question is "Estimate the load and storage for a Twitter-like service." Say your assumptions: 200 million daily users, 2 posts each, 300 bytes per post, 100 reads per write. Then compute. 400 million posts a day is about 4,630 writes per second. Reads are about 463,000 per second. Post text is about 120 GB a day, or about 43.8 TB a year. The conclusion that drives the design: reads dominate, so cache and precompute feeds. Text is small, and media will dominate storage.

## Practitioner checklist

- [ ] Have you answered ten questions aloud without notes?
- [ ] Did every answer include an estimate with units?
- [ ] Did every answer say what happens on failure?
- [ ] Have you marked the rows you missed and read those lessons?
- [ ] Have you asked a colleague to grade one answer?

## Related lessons

- [Foundations and framework](./foundations-and-framework.md) — the answer framework and a seven-stage practice plan.
- [Numbers, formulas and papers](./numbers-and-formulas.md) — the figures every answer uses.
- [Recap](./recap.md) — the systems at a glance and a self-test.
- [Technical product sense](../technical-product-sense/README.md) — reading systems rather than designing them.
- [Evaluation and observability](../evaluation-and-observability/README.md) — measuring what you build.

## Sources

- Alex Xu, *System Design Interview*, volumes 1 and 2, and Martin Kleppmann, *Designing Data-Intensive Applications*: the topics the questions cover.
- The question wording, the levels and the coverage column are this track's own. The levels are a judgement, not a standard.
