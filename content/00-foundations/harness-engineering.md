# Harness engineering, not just prompt engineering

*Part of [00 · Foundations](./README.md)*

## TL;DR

Prompt engineering optimizes the *string* you send the model. Harness engineering
optimizes the *system* that sends it: retries, validators, tool wiring, budgets,
fallbacks, caching, and observability. In production, the harness is where most of
your reliability — and most of your bugs — actually live. A great prompt inside a
naive harness is fragile; an average prompt inside a strong harness ships.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — The reliability your users feel comes from the system *around* the model, not the prompt inside it. "Improve the prompt" is rarely your highest-leverage roadmap item; the work that actually moves retention is harness work — validation, fallbacks, budgets, routing.
>
> **What it changes in your decisions** — How you scope "AI quality" epics, where you spend engineering cycles, and what you can credibly promise in an SLA.
>
> **Ask your eng team** — *"If the model returns garbage on a single call, what does the user actually see?"*
>
> **Product risk if ignored** — You ship a dazzling demo, then burn quarters firefighting reliability you never put on the roadmap.


## Mental model

Think of the model as a single, fast, unreliable, stateless function call:

```
output = model(context)   // non-deterministic, occasionally wrong, no memory
```

Everything that makes that call *useful and safe* is the harness:

```
result = harness(input):
    context   = assemble_context(input)        # context engineering
    raw       = call_model(context)            # the easy part
    parsed    = validate_and_repair(raw)       # structured output
    effects   = execute_tools(parsed)          # function calling, idempotency
    guarded   = enforce_budgets(...)           # loop/tool budgets
    observed  = trace_everything(...)          # spans, tokens, cost
    return    fallback_if_needed(guarded)      # routing, degraded mode
```

Each of those lines is a lesson elsewhere in this repo. The point of *this* lesson
is that they are **one discipline**, and that discipline — not prompt wording — is
what separates a demo from a service.

## Why the harness dominates in production

- **Models are stochastic.** The same input can produce a valid result once and a
  malformed one the next time. Only the harness can make the *system* deterministic
  enough to depend on (via validation, retries, and fallbacks).
- **Models are stateless.** Memory, history, scratchpads, and tool results all live
  in the harness. What the model "knows" on any given call is whatever your harness
  decided to put in the context.
- **Models don't have side effects — your harness does.** The moment a tool call
  writes to a database, sends an email, or moves money, correctness becomes an
  engineering property (see [idempotency](../02-reliable-outputs/function-calling.md)),
  not a prompting property.
- **Models don't have SLAs — your service does.** Latency, availability, and cost
  targets are met by [routing](../02-reliable-outputs/model-routing.md),
  [caching](../01-inference-internals/prompt-vs-semantic-caching.md), and
  [batching](../01-inference-internals/batching-and-paged-attention.md) — all harness.

## What lives in a serious harness

| Concern | Harness responsibility | Lesson |
| --- | --- | --- |
| Input shaping | Assemble, compress, order context | [Context engineering](./context-engineering.md) |
| Output trust | Schema validation + repair + fallback | [Structured output](../02-reliable-outputs/structured-output.md) |
| Side effects | Tool contracts, arg validation, idempotency | [Function calling](../02-reliable-outputs/function-calling.md) |
| Termination | Loop budgets, tool budgets, stop conditions | [Agent guardrails](../02-reliable-outputs/agent-guardrails.md) |
| Availability | Routing + graceful fallback | [Model routing](../02-reliable-outputs/model-routing.md) |
| Truth | Evals + regression gates | [Evals](../04-evals-observability/evals.md) |
| Operability | Traces, spans, drift detection | [Observability](../04-evals-observability/observability.md) |
| Economics | Per-feature/tenant cost attribution | [Cost attribution](../04-evals-observability/cost-attribution.md) |
| Safety | Injection defense, permission boundaries | [Safety engineering](../05-safety-multitenancy/safety-engineering.md) |

## Failure modes (when teams over-invest in prompts and under-invest in harness)

- **"It worked yesterday."** No regression evals, so a prompt tweak or model update
  silently breaks 5% of cases. Fix: [golden sets + CI gates](../04-evals-observability/evals.md).
- **The JSON sometimes doesn't parse.** No validation/repair, so one malformed
  output takes down a workflow. Fix: [structured output pipeline](../02-reliable-outputs/structured-output.md).
- **The agent ran for 40 steps and spent $12.** No budgets. Fix:
  [loop & tool budgets](../02-reliable-outputs/agent-guardrails.md).
- **Latency spikes at peak.** No routing/caching. Fix:
  [routing](../02-reliable-outputs/model-routing.md) +
  [caching](../01-inference-internals/prompt-vs-semantic-caching.md).
- **A prompt injection from a retrieved doc exfiltrated data.** The harness trusted
  model output as control flow. Fix:
  [permission boundaries](../05-safety-multitenancy/safety-engineering.md).

## Practitioner checklist

- [ ] Can your system survive the model returning garbage on any single call?
- [ ] Is every side-effecting tool call idempotent and validated?
- [ ] Is there a hard ceiling on iterations, tokens, and cost per request?
- [ ] Is every model call traced with tokens, latency, and cost?
- [ ] Can you change models without rewriting business logic?
- [ ] Do you have a regression eval that runs before prompt/model changes ship?

If the answer to any of these is "no," your reliability gap is in the harness, not
the prompt.

## Related lessons

- [Context engineering, not just long prompts](./context-engineering.md)
- [Shipping LLM systems as infrastructure, not demos](./infra-not-demos.md)
- [Agent guardrails](../02-reliable-outputs/agent-guardrails.md)
- [Production failure modes](../06-strategy-tradeoffs/production-failure-modes.md)
