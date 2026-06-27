# Model Routing, Graceful Fallback Logic, and Degraded-Mode UX

*Part of [02 · Reliable Outputs & Tool Use](./README.md)*

## TL;DR

Don't hard-wire one model to every request. **Routing** sends each request to the
*right* model for its difficulty, latency budget, and cost — small/cheap for easy
cases, large/expensive for hard ones. **Fallback** keeps the system up when a model
times out, errors, rate-limits, or returns low-confidence output by trying another
path. **Degraded-mode UX** makes the fallback *honest and usable* for the user instead
of a silent quality drop or a hard failure. Together they decouple your product's
reliability from any single model's reliability.

## Mental model

Your provider/model is a dependency with its own latency, error rate, and outages.
Production systems don't bet availability on a single dependency — they route and fall
back. The same applies here:

```
request ──▶ classify (difficulty / cost ceiling / latency SLO / privacy)
        ──▶ pick model (cheap → capable)
        ──▶ call with timeout
        ──▶ on error / timeout / rate-limit / low-confidence:
              ├─ retry (backoff, idempotent only)
              ├─ failover to alt provider / model
              ├─ degrade (smaller model, cached, simpler answer)
              └─ clean typed error + degraded-mode UX
```

## Routing strategies

- **Difficulty-based (cascade).** Try a cheap/fast model first; escalate to a stronger
  one only when needed (low confidence, validation failure, explicit "I'm not sure").
  Most traffic is easy, so cascades cut cost dramatically — but add latency on
  escalated requests. Pairs naturally with [structured-output fallback](./structured-output.md).
- **Classifier / router model.** A small upfront classifier predicts which model can
  handle the request, routing in one hop (no escalation latency) at the cost of router
  accuracy.
- **Capability-based.** Route by need: vision → multimodal model, code → code model,
  long context → long-context model, cheap bulk → small model.
- **Constraint-based.** Honor latency SLOs (fast model for interactive),
  [cost budgets](../04-evals-observability/cost-attribution.md), and **data-residency/
  privacy** (sensitive data → on-prem/approved model only — a
  [safety boundary](../05-safety-multitenancy/safety-engineering.md)).

## Graceful fallback logic

Fail over on the right signals, in order of cost:
1. **Transient errors** (timeout, 5xx, rate-limit) → retry with backoff (only
   [idempotent](./function-calling.md) operations) then failover to an alternate
   provider/model.
2. **Quality signals** (validation failure, low confidence, refusal) → escalate to a
   stronger model or stricter generation.
3. **Hard outage** → serve from [semantic cache](../01-inference-internals/prompt-vs-semantic-caching.md),
   a smaller local model, or a non-LLM fallback (templated/rule-based response).

Principles:
- **Multi-provider** removes single-vendor outage risk — but you must keep prompts and
  [evals](../04-evals-observability/evals.md) portable, since models behave differently.
- **Circuit breakers**: when a model is failing, stop routing to it for a cooldown
  rather than piling on.
- **Idempotency + budgets**: fallback chains can multiply calls; bound them like any
  [agent loop](./agent-guardrails.md).

## Degraded-mode UX

A fallback that silently lowers quality is a *trust* bug. Make degradation legible:
- **Be honest.** "We're experiencing high load — here's a quick answer; ask for more
  detail to retry" beats a confidently worse answer presented as normal.
- **Preserve the core job.** Drop nice-to-haves (citations, rich formatting, long
  reasoning) before dropping the actual answer.
- **Offer a path back.** Let the user retry the full-quality path when it recovers.
- **Never expose internals.** No stack traces, raw model text, or "provider X 503" —
  surface a clean, typed, user-appropriate message (the end of the
  [structured-output fallback chain](./structured-output.md)).

## Tradeoffs

| Strategy | Buys | Costs |
| --- | --- | --- |
| Cheap-first cascade | Big cost savings | Added latency on escalations |
| Upfront router | Low latency, one hop | Router errors mis-route |
| Multi-provider failover | Outage resilience | Prompt/eval portability burden |
| Degraded mode | Stays up under stress | Lower quality; must be honest |

## Failure modes

- **No fallback** — provider has a bad hour, your whole feature is down.
- **Silent degradation** — quality quietly drops on fallback; users lose trust, evals
  don't catch it because they only test the happy path.
- **Routing misclassification** — easy task sent to the expensive model (cost) or hard
  task to the weak model (quality). Monitor per-route success and cost.
- **Fallback amplification** — chained retries/failovers explode cost and latency
  without budgets.
- **Portability gaps** — failover model gives differently-shaped output that breaks
  downstream parsing; validate every route against the same schema/evals.

## Practitioner checklist

- [ ] Does every model call have a timeout and a defined fallback path?
- [ ] Do you route by difficulty/capability/cost/latency, not one-model-fits-all?
- [ ] Is there a second provider/model for outage failover?
- [ ] Are retries idempotent and the whole fallback chain budget-bounded?
- [ ] Is degraded mode honest, job-preserving, and free of raw internals?
- [ ] Do you monitor per-route success rate, latency, and cost?
- [ ] Are all routes validated against the same output schema and evals?

## Related lessons

- [Structured output & fallback chains](./structured-output.md)
- [Agent guardrails](./agent-guardrails.md)
- [Cost attribution](../04-evals-observability/cost-attribution.md)
- [Evals](../04-evals-observability/evals.md)
- [Inference-stack tradeoffs](../06-strategy-tradeoffs/inference-stack-tradeoffs.md)
