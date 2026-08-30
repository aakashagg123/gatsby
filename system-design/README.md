# System design for the technical PM

How real systems are designed at scale — from rate limiters to stock exchanges — with the architecture, tradeoffs, and failure modes that shape product decisions.

```mermaid
flowchart LR
  subgraph Foundations
    F1[Scaling]
    F2[Estimation]
    F3[Framework]
  end
  subgraph Building Blocks
    B1[Rate limiting]
    B2[Consistent hashing]
    B3[KV stores]
    B4[Unique IDs]
  end
  subgraph Systems
    S1[Web-scale]
    S2[Real-time]
    S3[Storage]
    S4[Location]
    S5[Data infra]
    S6[Transactional]
  end
  Foundations --> Building Blocks --> Systems
```

Every lesson in this track follows the same shape:

- **TL;DR** — the system in a paragraph, the core tradeoff, the scale.
- 🎯 **For the technical PM** — why it matters to the product, what it changes in your decisions, the sharp question to ask your eng team, and the product risk if you ignore it.
- **Mental model** — the one diagram or analogy that makes the system click.
- **Mechanics** — how it actually works: components, data flow, protocols.
- **Tradeoffs & decisions** — named tradeoffs with costs.
- **Failure modes** — how it breaks in production.
- **Practitioner checklist** — what to verify before you ship or bet on this architecture.

This track covers **28 real-world systems** across eight lessons, grouped by the kind of problem they solve.

## Connects to other tracks

- The [technical product sense](../technical-product-sense/README.md) track teaches you how to *read* systems; this track teaches you how they're *designed*.
- The [AI engineering](../content/00-foundations/README.md) modules show what's different when LLMs are in the loop — caching, isolation, cost — and this track shows the distributed-systems foundations that everything rests on.
- The [agentic AI](../agentic-ai/README.md) track uses message queues, event sourcing, and state machines from this track as agent infrastructure.

## The lessons

- [Foundations & framework](./foundations-and-framework.md) — scaling from zero to millions, back-of-envelope estimation, and the four-step system design framework
- [Core building blocks](./core-building-blocks.md) — rate limiting, consistent hashing, distributed key-value stores, and unique ID generation
- [Web-scale services](./web-scale-services.md) — URL shortener, web crawler, notification system, and news feed
- [Real-time systems](./real-time-systems.md) — chat system, search autocomplete, and video streaming platforms
- [Storage & sync](./storage-and-sync.md) — cloud file storage and S3-like object storage
- [Location & geo services](./location-and-geo-services.md) — proximity service, nearby friends, and mapping/navigation
- [Data infrastructure](./data-infrastructure.md) — distributed message queues, metrics monitoring, ad click aggregation, and email service
- [Transactional & financial systems](./transactional-and-financial.md) — hotel reservation, gaming leaderboard, payment system, digital wallet, and stock exchange

**📌 Close out the module:** [Recap & real-world examples](./recap.md)
