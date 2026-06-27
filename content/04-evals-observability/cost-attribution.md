# Cost Attribution per Feature, Workflow, Tenant, and User Journey — Not Just per Model

*Part of [04 · Evals & Observability](./README.md)*

## TL;DR

"Our LLM bill is $80k/month" is not an actionable number. To optimize, control, and
price an AI product you must attribute cost along the dimensions you make decisions on:
**which feature, which workflow, which tenant, which user journey** is spending the
tokens. Per-model spend is what the provider invoices; per-*feature*/*tenant* spend is
what tells you what to cache, route, cap, or bill. Cost attribution is a product and
business capability, not just a finance line item.

> 🧭 **In plain terms**
>
> 'What does this AI feature cost?' isn't enough — you need cost *per feature, per customer, per task*, the way a business tracks margin per product line. A handful of power users can quietly destroy your profitability, and you can't price or optimize what you can only see as one big monthly bill. The total hides the story; the breakdown is where the decisions live.


<!--sep-->

> 🎯 **For the AI-native PM**
>
> **Why it matters** — "What does this AI feature cost, and who's driving the spend?" is a core PM question. Per-tenant and per-feature cost is the foundation of pricing, packaging, and margin.
>
> **What it changes in your decisions** — Pricing and plan limits, which tenants are unprofitable, and where optimization actually pays off.
>
> **Ask your eng team** — *"Can we see cost per feature and per tenant — not just the total bill?"*
>
> **Product risk if ignored** — You price blind, a few power users quietly destroy margin, and you can't tell which feature to fix.


## Mental model

Tokens are the currency, and every token is generated *for a reason* — a feature
serving a workflow for a tenant during a user journey. If your [traces](./observability.md)
carry those tags, cost rolls up along any of them:

```
$ total
 ├─ by feature      (support_copilot vs. search vs. summarize)
 ├─ by workflow      (onboarding flow vs. report generation)
 ├─ by tenant        (acme: $9k, globex: $40 — wildly uneven)
 ├─ by user journey  (first 3 messages cost 5× the rest)
 └─ by model/route   (what the invoice shows)
```

The provider gives you only the last row. You have to build the rest.

## Why per-model is not enough

- **You can't optimize what you can't localize.** A 30% cost cut hides in *which*
  feature's prompt is bloated or *which* workflow loops too much — invisible at the
  model level.
- **Tenants are wildly uneven.** In multi-tenant SaaS, a tiny fraction of tenants often
  drives most spend. Without per-[tenant](../05-safety-multitenancy/multi-tenant-isolation.md)
  cost you can't find unprofitable accounts, set quotas, or price fairly.
- **Unit economics need a denominator.** "Cost per resolved ticket," "per generated
  report," "per active user" — these require attribution to the *unit*, not the model.
- **Runaway detection.** A [runaway agent](../02-reliable-outputs/agent-guardrails.md) or
  a [cache-busting prefix](../01-inference-internals/prompt-vs-semantic-caching.md) shows
  up as a feature/tenant cost spike — but only if cost is sliced that way.

## What to capture (per call, then roll up)

On every model/tool span, record:
- **Tokens:** input and output **separately** (priced differently), plus
  cache-read/cache-write tokens (cached input is much cheaper —
  [prompt caching](../01-inference-internals/prompt-vs-semantic-caching.md)).
- **Model & route** chosen (and whether a [fallback/escalation](../02-reliable-outputs/model-routing.md)
  fired — escalations are a cost driver).
- **Dimensional tags:** feature, workflow step, tenant, user, request/journey id.
- **Derived cost:** apply the price book (per-model, per-token-type) to the tokens.

These are the same [tags on your traces](./observability.md) — cost attribution is an
aggregation over instrumented spans, not a separate system.

## Dimensions that matter

| Dimension | Question it answers | Decision it drives |
| --- | --- | --- |
| **Feature** | Which capability costs most? | Where to cache/route/optimize |
| **Workflow** | Which step burns tokens? | Compress context, cut loops |
| **Tenant** | Who's expensive/unprofitable? | Quotas, pricing, plan limits |
| **User journey** | Where in the funnel is spend? | UX changes, cheap paths early |
| **Model/route** | What's the per-route blend? | Routing strategy, vendor mix |

## From attribution to control

Attribution is the input; control is the point:
- **Budgets & quotas** per tenant/feature; alert and throttle on breach (ties to
  [agent budgets](../02-reliable-outputs/agent-guardrails.md)).
- **Routing decisions:** push cheap traffic to small models; reserve big models for
  hard cases ([routing](../02-reliable-outputs/model-routing.md)) — measured by cost-per-route.
- **Caching ROI:** quantify savings from prompt/semantic caching and protect cache-hit
  rate as a cost metric.
- **Context discipline:** target the bloated prompts attribution exposes
  ([context engineering](../00-foundations/context-engineering.md)).
- **Pricing & packaging:** set plan limits and prices from real unit economics, not
  guesses.

## Tradeoffs

- **Tag granularity vs. overhead** — more dimensions = richer slicing but more
  instrumentation and cardinality cost. Tag the dimensions you actually *decide* on.
- **Real-time vs. batch** — live cost dashboards enable fast reaction but cost more to
  run than daily rollups; match to how fast you need to act.
- **Cost vs. quality vs. latency** — cheapest route isn't always acceptable; attribution
  lets you optimize cost *within* quality/latency SLOs, the theme of
  [stack tradeoffs](../06-strategy-tradeoffs/inference-stack-tradeoffs.md).

## Failure modes

- **Flat bill, no slices** — a cost spike, no idea which feature/tenant caused it.
- **Ignoring cache-read pricing** — over-reporting cost or missing the value of caching.
- **Input/output lumped together** — misreads where spend really is (long context vs.
  long generation need different fixes).
- **No per-tenant view** — unprofitable accounts hide; pricing is guesswork.
- **Attribution without action** — pretty dashboards, no budgets/routing changes.

## Practitioner checklist

- [ ] Do spans record input/output (and cache-read/write) tokens separately?
- [ ] Is every call tagged with feature, workflow, tenant, and journey?
- [ ] Can you produce cost per tenant and per unit (ticket, report, active user)?
- [ ] Do you track cost-per-route and escalation rate?
- [ ] Are there per-tenant/feature budgets with alerts and throttling?
- [ ] Is prompt-cache hit rate tracked as a cost metric?
- [ ] Does attribution actually drive routing/caching/pricing decisions?

## Related lessons

- [Observability](./observability.md)
- [Prompt vs. semantic caching](../01-inference-internals/prompt-vs-semantic-caching.md)
- [Model routing](../02-reliable-outputs/model-routing.md)
- [Multi-tenant isolation](../05-safety-multitenancy/multi-tenant-isolation.md)
- [Inference-stack tradeoffs](../06-strategy-tradeoffs/inference-stack-tradeoffs.md)
