# Safety & Multi-tenancy — Recap & Real-World Examples

*Part of [05 · Safety & Multi-tenancy](./README.md)*

## Real-world examples & war stories

**The ChatGPT Redis bug (March 2023).** A caching bug in an async library let some users
briefly see **other users' chat titles** — and exposed limited payment-related info for a
small number of subscribers. OpenAI took the service down to patch it. 🎯 *PM takeaway:*
this is the textbook [cross-user contamination](./multi-tenant-isolation.md) incident —
shared/cached state that wasn't correctly scoped per user. It's the failure that ends B2B
AI trust overnight.

**Indirect prompt injection & the "lethal trifecta."** Research (Greshake et al., 2023)
and Simon Willison's widely-cited framing showed that an assistant which (1) reads
untrusted content, (2) can access private data, and (3) can communicate externally can be
hijacked by a **poisoned web page or email** to exfiltrate data — with the user never
typing anything malicious. 🎯 *PM takeaway:* audit every agent for the
[trifecta](./safety-engineering.md) and break at least one leg.

**Samsung's data leak (2023).** Confidential code pasted into a public model left the
company's boundary. 🎯 *PM takeaway:* [data-leakage prevention](./safety-engineering.md)
starts with *what you let into the context and where it can go.*

**The $1 Tahoe and DPD's swearing bot (2023–24).** Direct prompt injection / jailbreaks
turned public-facing bots into liabilities. 🎯 *PM takeaway:* injection isn't theoretical;
it's a launch blocker that [adversarial evals](../04-evals-observability/evals.md) must
cover.

## Module recap

| Lesson | The one idea | The decision it drives |
| --- | --- | --- |
| [Safety engineering](./safety-engineering.md) | No prompt fully stops injection — enforce authority in *code* | Enterprise readiness; autonomy granted |
| [Multi-tenant isolation](./multi-tenant-isolation.md) | Anything shared/cached must be scoped per tenant | Isolation architecture; SOC 2 / contracts |

**The through-line:** an LLM mixes trusted instructions and untrusted data in one channel,
and often serves many tenants from shared infrastructure. So: **treat all model output as
untrusted, enforce permissions in tools on the real session (never on the model's
beliefs), break the lethal trifecta, and scope every cache, index, and log by tenant.**
Security here is architectural, not a prompt you can write.

> **Walk-away question:** *"If a poisoned document entered our knowledge base — or a cache
> key forgot the tenant id — what's the blast radius?"*

---

← Back to [module index](./README.md) · → Next module: [06 · Strategy & Tradeoffs](../06-strategy-tradeoffs/README.md)
