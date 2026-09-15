# APIs & integrations — recap & real-world examples

*Part of [APIs & integrations for the product leader](./README.md)*

## Real-world examples & war stories

**Model provider outages cascading downstream (2023–2024).** Several widely used AI
products experienced their own outages or degraded service directly tied to their model
provider having a rough hour, because the AI call sat in the critical path with no
fallback and no isolation from the rest of the product. 🎯 *Takeaway:*
[failure isolation](./integrating-into-existing-systems.md) is not optional insurance — a
provider's bad day is a certainty over a long enough timeline, and the only question is
whether your product absorbs it or passes it straight through to users.

**Viral growth hitting rate limits (ongoing).** A recurring pattern across AI-powered
products: a feature goes viral, traffic spikes far faster than expected, and the product
hits its model provider's rate limits within hours, turning a growth moment into a
degraded, error-filled experience for exactly the users a team most wanted to impress.
🎯 *Takeaway:* [rate limits](./calling-an-llm-api.md) are not a detail to discover under
load — checking expected traffic against vendor limits before launch is cheap; discovering
the gap during a viral spike is not.

**ChatGPT's streaming reply became the expected UX (2022 onward).** The now-familiar
sight of a chat response appearing word by word, rather than all at once, set a user
expectation so strong that a competing product's full-response-only reply now reads as
noticeably slower, even when the total generation time is similar. 🎯 *Takeaway:*
[streaming](./calling-an-llm-api.md) changed from a technical option to something close to
a baseline user expectation for any interactive AI feature — perceived speed, not just
actual speed, is a product decision.

**Stripe's idempotency-key pattern became the industry reference.** Long before AI APIs
existed, Stripe popularized a simple, now widely copied pattern for payment APIs: attach a
unique key to a request, and a retried request with the same key is recognized and safely
ignored rather than processed twice. 🎯 *Takeaway:* [idempotency](./integrating-into-existing-systems.md)
solved this exact problem — safe retries on a system where duplication is costly — well
before AI made retries routine, and it's the same pattern to reach for now.

**The Model Context Protocol's fast, wide adoption (2024–2025).** Anthropic introduced MCP
in late 2024 as an open standard for connecting AI assistants to tools and data. Within
about a year, other major AI providers adopted the same standard, turning what could have
been a fragmented, vendor-specific integration landscape into a shared one. 🎯 *Takeaway:*
[standard connectors](./mcp-and-standard-connectors.md) can genuinely change integration
economics industry-wide, not just inside one company — this is what the "build once, works
everywhere" argument for this lesson actually looks like in practice.

**Why JSON mode exists at all.** Early AI products asking a model in plain language to
"please respond only in JSON" regularly got back a JSON block wrapped in an explanatory
sentence, or syntax a parser would reject — reliable enough for a demo, not for production.
Model providers responded by adding schema-constrained generation as a request-level
feature. 🎯 *Takeaway:* [JSON mode](./structured-output-and-json-mode.md) exists precisely
because plain-language formatting instructions weren't reliable enough for systems that
needed to trust the shape of what came back — a mechanism built from a real, repeated
production failure.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [The request/response contract](./the-request-response-contract.md) | A model call is a contract, with the same properties any API contract has | Could I sketch what we send and what comes back? |
| [Calling an LLM API](./calling-an-llm-api.md) | Auth, rate limits, streaming, and retries decide if it works under real traffic | What would users experience during our provider's worst hour? |
| [Structured output & JSON mode](./structured-output-and-json-mode.md) | The API constrains shape; your system still has to validate values | Would a syntactically valid but wrong response be caught? |
| [Webhooks & async patterns](./webhooks-and-async-patterns.md) | Long work needs "start now, notify later," not a blocking wait | Have we matched sync vs. async to how long the work really takes? |
| [Integrating into existing systems](./integrating-into-existing-systems.md) | Latency budgets, idempotency, and isolation — the same discipline as any critical dependency | Is every AI-driven side effect safe to retry? |
| [MCP & standard connectors](./mcp-and-standard-connectors.md) | Build the connector once, reuse it across tools, when reuse is likely | Will this integration need to serve more than one AI tool? |

**The through-line:** none of the mechanics in this module are exotic to AI. Contracts,
authentication, rate limits, retries, idempotency, and failure isolation are the same
discipline that has always separated a resilient integration from a fragile one. What
changed is the dependency on the other end: slower, less predictable, and more prone to
routine failure than most APIs a team has integrated before. The teams that ship reliable
AI features aren't the ones with a cleverer model — they're the ones who applied ordinary,
proven integration discipline to a genuinely new kind of dependency, instead of assuming a
demo's happy path would hold under real traffic.

> **Walk-away question:** *"For our AI integration: do we know our provider's rate limits,
> is every AI-driven action safe to retry, is the AI call isolated from the rest of the
> flow if it fails, and have we matched sync versus async to how long the work actually
> takes?"*

If yes, the integration is built to survive contact with real users, not just a demo. If
no, you now know exactly which lesson in this module to reread.
