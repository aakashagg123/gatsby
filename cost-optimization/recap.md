# Cost optimization — recap & real-world examples

*Part of [Cost optimization for the product leader](./README.md)*

## Real-world examples & war stories

**Model providers cutting prices repeatedly, and teams that never re-checked their
build-vs-buy math.** Frontier-model per-token prices have fallen steeply and repeatedly
since the category began — a pattern that keeps moving the
[self-hosting breakeven volume](./the-cost-stack-and-the-build-vs-buy-breakeven.md)
higher every time it happens. Teams that calculated the crossover once, at launch, and
never revisited it are routinely sitting on a stale answer in one direction or the
other. 🎯 *Takeaway:* a build-vs-buy decision has an expiration date tied to volume and
price, not a permanent verdict.

**GPU serving efficiency becoming the real margin lever for self-hosted teams.**
As continuous batching and paged attention matured into standard practice across serving
stacks (vLLM, TGI, TensorRT-LLM, SGLang), the gap between a naively-served self-hosted
model and a well-tuned one widened into the difference between a losing and a winning
unit-economics story — the same fixed GPU capacity serving dramatically more tokens per
dollar. 🎯 *Takeaway:* [the cost stack](./the-cost-stack-and-the-build-vs-buy-breakeven.md)
levers compound — a self-hosting decision made without the serving-stack investment lands
nowhere near the marginal cost the breakeven math assumed.

**Teams discovering a runaway agent loop from the invoice, not a budget alert.** A
recurring pattern in early agentic-product operations: a loop bug, a retry storm, or a
cache-busting change burns weeks of allocated spend before anyone notices, because
nothing automatic was watching — only a dashboard a human forgot to check. 🎯 *Takeaway:*
[a budget that only alerts, instead of enforcing](./finops-budgets-forecasting-and-the-cost-review.md),
catches the problem after the money is already spent.

**Forecasts that got surprised by moving in only one direction.** A common forecasting
failure: a team models AI spend as a single line extrapolated from last month's bill,
missing that usage growth and falling token prices pull in opposite directions
simultaneously — and gets blindsided whichever curve moves faster than the naive line
assumed. 🎯 *Takeaway:*
[modeling both curves separately](./finops-budgets-forecasting-and-the-cost-review.md)
is the difference between a forecast with two quarters of warning and one with none.

**Chargeback adoption changing engineering behavior overnight.** Organizations that
moved from showback (visibility only) to chargeback (real budget impact) for AI spend
consistently report the same effect: teams that previously defaulted to the biggest
available model start asking, on their own, whether a cheaper route or a smaller model
would do. 🎯 *Takeaway:* [attribution changes behavior only once it touches a
budget](./finops-budgets-forecasting-and-the-cost-review.md) — visibility alone rarely
does.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [The cost stack, and the build-vs-buy breakeven](./the-cost-stack-and-the-build-vs-buy-breakeven.md) | Every cost tactic attacks one of four levers, and self-hosting has a real, calculable crossover volume | Which of tokens, caching, routing, or context is actually our slack lever — and have we run the breakeven math? |
| [FinOps for AI: budgets, forecasting & the cost review](./finops-budgets-forecasting-and-the-cost-review.md) | Attribution shows where money went; FinOps decides where it goes next | If spend doubled overnight, would anything stop it automatically? |

**The through-line:** AI cost optimization isn't one skill, it's diagnosis plus
governance. Diagnosis means knowing which of a small number of levers is actually slack
before proposing a fix, and knowing the real crossover volume for build-vs-buy instead of
guessing. Governance means budgets with teeth, cost visibility that actually changes
behavior, a forecast that respects two curves moving in opposite directions, and a
recurring review that catches drift before the invoice does. This module deliberately
stayed at that decision altitude rather than re-deriving mechanics already developed in
full depth across
[Prefill vs. decode](../content/01-inference-internals/prefill-vs-decode.md),
[Prompt vs. semantic caching](../content/01-inference-internals/prompt-vs-semantic-caching.md),
[Model routing](../content/02-reliable-outputs/model-routing.md), and
[Cost attribution](../content/04-evals-observability/cost-attribution.md), because the
mistake that actually erodes margin is rarely a missing technique. It's a lever nobody
diagnosed, or a governance practice that stopped at a dashboard.

> **Walk-away question:** *"For our biggest AI cost line: do we know which lever is
> actually slack, have we run the build-vs-buy breakeven with current numbers, and would
> a runaway spend spike stop itself before we found out from the invoice?"*

If yes, cost is something the team actively manages rather than discovers. If no, you
now know exactly which lesson in this module to reread — and where the deeper mechanics
live, one module away in
[Cost attribution](../content/04-evals-observability/cost-attribution.md) and
[The economics of infrastructure](../technical-product-sense/economics-of-infrastructure.md).

This closes out the eleven-module [Generative AI family](../GENERATIVE_AI_ROADMAP.md).
