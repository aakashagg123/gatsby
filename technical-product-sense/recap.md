# Technical product sense — recap & real-world examples

*Part of [Technical product sense for the AI PM](./README.md)*

## Real-world examples & war stories

**The duplicate-charge outage.** A payment request times out. The client retries. Without
[idempotency](./apis-and-contracts.md), the customer gets charged twice. One missing
idempotency key turns into a support-and-refund fire drill. 🎯 *Takeaway:* "what happens on
retry?" is one of the highest-leverage questions a PM can ask. It stays invisible until the
day it isn't.

**The p95 that averaged fine.** A feature ships with a healthy 200 ms *average* response. But
the team's most valuable power users — the ones with the most data — quietly suffer 4-second
loads. Nobody checked the [p95 tail](./latency-scale-performance.md). 🎯 *Takeaway:* averages
hide your worst experiences. Always ask for percentiles.

**The migration that wasn't scoped.** A "quick" feature turns out to need a relationship the
[data model](./data-and-the-data-model.md) never stored. A two-week estimate becomes a
two-month migration. 🎯 *Takeaway:* "does this data exist, in a usable shape?" belongs in
discovery, not mid-build.

**Air Canada's chatbot invented a refund policy (2024).** A support bot gave a confident,
well-formed, and *wrong* answer. A tribunal held the airline to it. 🎯 *Takeaway:* the
[AI-specific failure](./technical-sense-for-ai.md) is a 200-OK wrong answer. That is why
[validation, grounding, and a wrong-answer path](./reliability-and-failure.md) are core, not
polish.

**The AI feature nobody could debug.** A model feature ships without evals or observability.
Weeks later, quality has drifted and no one can tell why — the prompt, the retrieval, the
model version, or the data could all be the cause. 🎯 *Takeaway:*
[evals and observability](./technical-sense-for-ai.md) *are* the reliability of an AI feature.
The [debt](./tech-debt-and-estimation.md) of skipping them comes due exactly when you can
least afford it.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [How systems are built](./how-systems-are-built.md) | A request travels a chain of boxes | Which box does the expensive work? |
| [APIs & contracts](./apis-and-contracts.md) | Components talk through promises | What happens on failure or retry? |
| [Data & the data model](./data-and-the-data-model.md) | The model decides what's possible | Does this data exist, usably, and may we use it? |
| [Latency, scale & performance](./latency-scale-performance.md) | Latency is a budget; scale is load | Which hop dominates, and is this speed or load? |
| [Reliability & failure](./reliability-and-failure.md) | Design the unhappy paths | When this fails, what does the user see? |
| [Tech debt & estimation](./tech-debt-and-estimation.md) | Debt charges interest; estimates are ranges | What shortcut are we taking, and when do we repay? |
| [Technical sense for AI](./technical-sense-for-ai.md) | The system around the model is the product | What, other than the model, will make this fail? |

**The through-line:** technical product sense is the ability to see the *system* behind the
feature. That means the boxes a request travels, the contracts between them, where the data
lives, where time and money go, how it fails, and what it costs to change. For the AI PM,
every one of these gains a probabilistic twist. The discipline stays the same: understand the
shape of the system well enough to build *with* it, and to earn the trust of the engineers
who do.

> **Walk-away question:** *"For this feature, can I draw the system on a whiteboard — the boxes,
> the slow hop, the failure paths — and if there's a model in it, is the product the trustworthy
> machinery around the model, not the model itself?"*

---

← Back to [module overview](./README.md)

## Test yourself

1. **"It's slow" and "it falls over under load" — why must you never conflate them?**
   <details><summary>Answer</summary>Latency (one request's time) and scale (how many requests) need different fixes. Latency needs you to find and cache the slow hop. Scale needs horizontal scaling and relief for the shared bottleneck. Fixing the wrong one wastes months. (<a href="./latency-scale-performance.md">Latency, scale & performance</a>)</details>
2. **A payment call times out and the app retries. What property makes that safe, and how does it work?**
   <details><summary>Answer</summary>Idempotency. The client sends a unique key per attempt. The server returns the original result for a repeated key, so a retry can't double-charge. (<a href="./apis-and-contracts.md">APIs & contracts</a>)</details>
3. **Why is "where does this data live, and how is it shaped?" a product question?**
   <details><summary>Answer</summary>The data model decides what features are possible without a migration. A question the model can't answer is a feature you can't ship. Analytical reads also don't belong on the transactional store. (<a href="./data-and-the-data-model.md">Data & the data model</a>)</details>
4. **Name the four tools that keep a dependency slowdown from becoming your outage.**
   <details><summary>Answer</summary>Timeouts cap the wait. Retries with backoff and jitter stop the storm from synchronizing. Circuit breakers fail fast while a dependency is sick. And a designed fallback controls what the user sees. (<a href="./reliability-and-failure.md">Reliability & failure</a>)</details>
5. **What's the blast-radius question, and when do you ask it?**
   <details><summary>Answer</summary>"If this piece were compromised tonight, what does the attacker hold tomorrow?" Ask it at design time, for every component, credential, and data store — not after the incident. (<a href="./security-and-privacy.md">Security & privacy sense</a>)</details>
