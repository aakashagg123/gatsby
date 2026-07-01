# Evals & observability — recap & real-world examples

*Part of [04 · Evals & Observability](./README.md)*

## Real-world examples & war stories

**Klarna's AI assistant (2024).** Klarna reported its OpenAI-powered assistant was
handling **~two-thirds of customer-service chats** — work it equated to hundreds of
full-time agents — within months. 🎯 *PM takeaway:* at that volume you *cannot* operate on
vibes. [Cost attribution](./cost-attribution.md) (what does each resolved chat cost?) and
continuous [quality monitoring](./observability.md) are what make a number like that safe
rather than terrifying.

**"Did the model change?" (the GPT-4 drift debates).** Practitioners repeatedly reported
that hosted models *behaved differently over time* on the same prompts, sparking public
back-and-forth about silent regressions. 🎯 *PM takeaway:* you can't control the
provider's weights — so you need **your own** [regression evals](./evals.md). Teams with a
golden set find out from CI; teams without one find out from churn.

**The LLM-observability category exists now.** LangSmith, Langfuse, Arize Phoenix,
Braintrust and others turned [traces, spans, token/cost accounting, and eval runs](./observability.md)
into a standard tooling layer. 🎯 *PM takeaway:* this is no longer exotic — "we have no
tracing or evals" is now a visible maturity gap, not a defensible default.

## Module recap

| Lesson | The one idea | The decision it drives |
| --- | --- | --- |
| [Evals](./evals.md) | The eval set *is* the product spec for a stochastic system | Release gates; how you compare models |
| [Observability](./observability.md) | LLMs fail silently; you must instrument quality, not just errors | Incident response; drift detection |
| [Cost attribution](./cost-attribution.md) | Per-feature/tenant cost, not just the total bill | Pricing, packaging, where to optimize |

**The through-line:** **you cannot operate what you cannot measure.** Evals tell you it's
*correct* before you ship; observability tells you it's *working* while it runs; cost
attribution tells you what it's *costing* and who's driving it. All three feed each
other — production traces become new eval cases; incidents become adversarial tests.

> **Walk-away question:** *"If quality dropped 10% tomorrow, would we find out from our
> dashboards — or from angry users three weeks later?"*

---

← Back to [module index](./README.md) · → Next module: [05 · Safety & Multi-tenancy](../05-safety-multitenancy/README.md)
