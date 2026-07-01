# Production failure modes & how to engineer around them

*Part of [06 · Strategy & Tradeoffs](./README.md)*

## TL;DR

LLM systems fail in a recognizable handful of ways: **hallucinated tool calls**,
**malformed JSON**, **stale retrieval**, **runaway agents**, and **silent eval
regressions** — plus their cousins (cost spikes, cross-tenant leaks, prompt injection,
degraded fallbacks). What they share is that they're *quiet*: the system keeps returning
plausible-looking output while doing the wrong thing. This lesson is a field guide: each
mode, why it happens, how to detect it, and which lesson hardens against it. Treat it as
the integration test for everything else in the repository.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — These are the incidents that will actually page your team. Knowing the catalog lets you put prevention on the roadmap *before* the postmortem instead of after it.
>
> **What it changes in your decisions** — Your pre-launch risk review, what you choose to monitor, and what goes in the runbook.
>
> **Ask your eng team** — *"Which of these five failure modes can happen to us today, and what's our detection for each?"*
>
> **Product risk if ignored** — You learn the catalog the expensive way — one outage at a time.


## Why LLM failures are different

In a normal service, failures throw: exceptions, 500s, timeouts. LLM failures often
**succeed loudly and are wrong quietly** — a hallucination reads like a fact, a malformed
plan parses far enough to act, a stale answer looks current. So the engineering response
isn't just error handling; it's **validation, bounding, grounding, and measurement** that
make silent failures *visible and contained*.

## The catalog

### 1. Hallucinated tool calls
- **What:** the model invents a tool, a parameter, or a plausible-but-fake argument
  (a non-existent id, an invalid enum), then "acts."
- **Why:** model output is treated as a trusted command; arguments aren't checked against
  the real system.
- **Detect:** tool-name/arg validation failures; downstream "not found" errors;
  [traces](../04-evals-observability/observability.md) of rejected calls.
- **Engineer around it:** strict [tool contracts + argument validation](../02-reliable-outputs/function-calling.md);
  validate args against the system of record; structured, actionable tool errors;
  [idempotency](../02-reliable-outputs/function-calling.md) so a bad-then-retried call is safe.

### 2. Malformed JSON / structured output
- **What:** output doesn't parse or violates the schema; a markdown fence, a trailing
  comma, a missing field takes down a workflow.
- **Why:** trusting raw generation; no validation; sometimes worsened by
  [aggressive quantization](../01-inference-internals/quantization-formats.md) hurting
  format adherence.
- **Detect:** parse/validation failure rate; repair rate trend.
- **Engineer around it:** [constrained decoding + schema validation + bounded repair +
  fallback chain](../02-reliable-outputs/structured-output.md); never `JSON.parse` without
  a schema; track validity after model/quantization changes.

### 3. Stale retrieval
- **What:** RAG cites outdated, deleted, or superseded content — confidently wrong on
  facts that *changed*.
- **Why:** the index is a cache that drifted from the source; deletions not propagated;
  no recency signals. (Same shape as [semantic-cache staleness](../01-inference-internals/prompt-vs-semantic-caching.md).)
- **Detect:** [freshness evals](../03-rag/retrieval-evals.md) with time-sensitive queries;
  recall/grounding trends; user "that's out of date" signals.
- **Engineer around it:** incremental indexing + deletion handling + recency ranking
  ([RAG freshness](../03-rag/rag-architecture.md)); cache TTLs/invalidation; "say I don't
  know" when context is absent.

### 4. Runaway agents
- **What:** an agent loops, thrashes a tool, or fans out — burning time and money, often
  *circularly* rather than infinitely.
- **Why:** no budgets, no termination/no-progress detection; non-idempotent tools amplify
  the damage.
- **Detect:** budget-hit rate, steps-per-task distribution, [cost](../04-evals-observability/cost-attribution.md)
  spikes by feature/tenant, repeated identical actions.
- **Engineer around it:** [loop/tool/token/cost/time budgets + termination + no-progress
  detection](../02-reliable-outputs/agent-guardrails.md); idempotent tools; per-tenant
  cost alerts.

### 5. Silent eval regressions
- **What:** quality drops with *no code change* — a provider model update, a prompt tweak
  with side effects, [drift](../04-evals-observability/observability.md) in data/inputs —
  and nobody notices for weeks.
- **Why:** no regression gate; reliance on "it looked fine"; aggregate metrics hiding a
  category cliff.
- **Detect:** [regression evals in CI](../04-evals-observability/evals.md); scheduled
  re-runs; per-stratum deltas; online quality proxies + drift monitors.
- **Engineer around it:** golden sets gating every change; stratified reporting;
  production sampling feeding back into evals.

## The cousins (don't forget these)

| Failure | Detect | Harden with |
| --- | --- | --- |
| **Cost spike** | per-feature/tenant cost alerts | [Cost attribution](../04-evals-observability/cost-attribution.md), budgets |
| **Cross-tenant leak** | adversarial isolation tests | [Multi-tenant isolation](../05-safety-multitenancy/multi-tenant-isolation.md) |
| **Prompt injection / exfiltration** | injection evals, egress monitoring | [Safety engineering](../05-safety-multitenancy/safety-engineering.md) |
| **Provider outage** | error-rate alerts | [Routing & fallback](../02-reliable-outputs/model-routing.md) |
| **Silent degraded mode** | route/quality monitoring | Honest [degraded-mode UX](../02-reliable-outputs/model-routing.md) |
| **Latency tail blowup** | p99 TTFT/TPOT, KV/preemption metrics | [Batching/KV](../01-inference-internals/kv-cache-management.md) |
| **Cache-busting prefix** | cache-hit-rate metric | [Prompt caching](../01-inference-internals/prompt-vs-semantic-caching.md) |

## The common cure

Every mode above is defeated by the same four habits — the thesis of this whole
repository:

1. **Treat model output as untrusted** → validate, bound, authorize.
2. **Put brakes on everything** → budgets, timeouts, fallbacks.
3. **Ground and isolate** → cite from context; scope by tenant.
4. **Measure relentlessly** → [evals](../04-evals-observability/evals.md) before shipping,
   [observability](../04-evals-observability/observability.md) while running, and feed
   incidents back into both.

This is the difference between [a demo and infrastructure](../00-foundations/infra-not-demos.md).

## Practitioner checklist (pre-launch failure review)

- [ ] Are tool calls validated so a hallucinated call can't act?
- [ ] Is every structured output schema-validated with bounded repair + fallback?
- [ ] Is the retrieval index fresh, with deletions handled and time-sensitive evals?
- [ ] Does every agent have enforced budgets and no-progress termination?
- [ ] Do regression evals gate changes, with scheduled re-runs and drift monitoring?
- [ ] Are cost, isolation, injection, outage, and latency-tail risks each covered?
- [ ] Does every incident become a new permanent eval case?

## Related lessons

- [Harness engineering](../00-foundations/harness-engineering.md)
- [Shipping as infrastructure, not demos](../00-foundations/infra-not-demos.md)
- [Structured output](../02-reliable-outputs/structured-output.md)
- [Function calling](../02-reliable-outputs/function-calling.md)
- [Agent guardrails](../02-reliable-outputs/agent-guardrails.md)
- [Evals](../04-evals-observability/evals.md) · [Observability](../04-evals-observability/observability.md)
- [Inference-stack tradeoffs](./inference-stack-tradeoffs.md)
