# Memory & context — recap & real-world examples

*Part of [Memory & context for the product leader](./README.md)*

## Real-world examples & war stories

**ChatGPT's memory feature rollout (2024).** OpenAI introduced a persistent memory feature
that let ChatGPT remember facts across separate conversations, shipped with a visible
settings page showing exactly what was stored, an option to turn it off, and a way to
delete individual memories. 🎯 *Takeaway:* [treating memory as a product decision](./memory-as-a-product-decision.md)
means shipping the visibility and control alongside the capability, not as a follow-up
feature — users trusted the capability faster because they could see and edit what it
stored from day one.

**Personalization that followed you to the wrong screen.** A recurring pattern across
recommendation and assistant products: a preference or a browsing detail from one context
— often assumed private or session-specific — resurfaces somewhere the user didn't expect,
like a shared or family-visible screen, prompting public complaints about a product
"knowing too much." 🎯 *Takeaway:* this is exactly the [boundary confusion](./session-user-and-organizational-memory.md)
between what should be session memory and what became visible more broadly — the shape of
the memory, not its existence, was the mistake.

**Enterprise AI assistants and the shared-knowledge boundary.** As companies rolled out AI
assistants trained or grounded on internal documents, a recurring incident type emerged:
an assistant surfaced information from one team's restricted documents to an employee in a
different team, because the retrieval or memory boundary followed the technical
architecture rather than the company's actual access-control policy. 🎯 *Takeaway:*
[organizational memory's entire risk](./session-user-and-organizational-memory.md)
concentrates in the boundary of who's "inside" it — and that boundary has to be enforced
by the system, mirroring real permissions, not assumed from how the data happened to be
indexed.

**"Right to be forgotten" meeting AI memory.** As privacy regulation matured, companies
operating AI features with persistent memory faced a genuinely hard question their
architecture hadn't anticipated: a user's deletion request needs to reach not just the
raw stored record, but anything derived or summarized from it — the same problem
[Knowledge graphs](../knowledge-graphs/governance-quality-and-trust.md) names for
inferred facts, now applied to AI memory. 🎯 *Takeaway:* [deletion has to be designed in
from the start](./when-memory-goes-wrong.md) — retrofitting it onto a memory system built
without provenance is a much harder project than building it in from day one.

**Assistants confidently repeating outdated company information.** A common support-tool
failure: an AI assistant grounded in a company's own documentation or an evolving customer
relationship confidently states a policy or a fact that changed months earlier, because
nothing in the memory or retrieval system tracked freshness. 🎯 *Takeaway:*
[staleness is a design problem](./when-memory-goes-wrong.md), not a rare edge case — any
memory or retrieval system needs an explicit freshness signal, or it will eventually state
something outdated with full confidence.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [Memory as a product decision](./memory-as-a-product-decision.md) | Memory is a feature you choose to build, with a cost and a promise attached | What do we actually promise to remember, for whom, and for how long? |
| [Session, user & organizational memory](./session-user-and-organizational-memory.md) | Three shapes, three different stakes — name which one before building | Which of the three shapes is this feature, and is the boundary enforced? |
| [Retrieval as memory](./retrieval-as-memory.md) | Retrieval and memory are often the same investment, aimed at different content | Is this memory feature really a retrieval problem in disguise? |
| [When memory goes wrong](./when-memory-goes-wrong.md) | Staleness, leakage, and no correction path — three specific, testable failures | Would we find a memory failure from monitoring, or from a user telling us? |

**The through-line:** memory is never something a model gives you — it's something your
product builds, on purpose, as a set of specific promises. This module deliberately
stayed at that altitude rather than re-deriving the engineering already developed in
[Context engineering](../content/00-foundations/context-engineering.md) and
[Context & memory](../agentic-ai/context-and-memory.md), because the mistakes that
actually sink memory features are rarely engineering mistakes. They're decisions nobody
made on purpose: a shape left unnamed, a boundary assumed instead of tested, a correction
path that was never built. The products that get memory right aren't the ones with the
cleverest retrieval pipeline — they're the ones that decided, specifically and in writing,
what they were promising to remember, and built the visibility and control to back that
promise up.

> **Walk-away question:** *"For our AI feature's memory: could we tell a user exactly what
> we remember about them, could they see and correct it, is the boundary around it tested
> rather than assumed, and did anyone actually decide this on purpose?"*

If yes, memory is a feature your product can stand behind. If no, you now know exactly
which lesson in this module to reread — and where the deeper engineering lives, one module
away in [Context engineering](../content/00-foundations/context-engineering.md) and
[Context & memory](../agentic-ai/context-and-memory.md).
