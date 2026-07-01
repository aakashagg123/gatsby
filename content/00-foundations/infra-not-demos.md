# Shipping LLM systems as infrastructure, not demos

*Part of [00 · Foundations](./README.md)*

## TL;DR

A demo proves the model *can* do the task once. Infrastructure makes it do the task
correctly, observably, affordably, and safely — for every user, every tenant, at
p99, indefinitely. The gap between the two is almost entirely engineering:
evaluation, observability, cost control, safety, and graceful degradation. Demos are
judged by their best case; infrastructure is judged by its worst case.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — The gap between an impressive demo and a dependable feature is the work that doesn't demo well — and it's most of the timeline. PMs who can't see that gap chronically under-scope AI projects.
>
> **What it changes in your decisions** — Your launch-readiness criteria, your definition of done for AI features, and the expectations you set with execs.
>
> **Ask your eng team** — *"What would it take to operate this for a year without it surprising us?"*
>
> **Product risk if ignored** — Friday-demo, Monday-outage: you green-light a launch that was never operationally real.


## Mental model

Ask of every LLM feature the same questions you'd ask of any production service:

- **How do I know it's working?** → [observability](../04-evals-observability/observability.md)
- **How do I know it's *correct*?** → [evals](../04-evals-observability/evals.md)
- **What happens when a dependency fails?** → [routing & fallback](../02-reliable-outputs/model-routing.md)
- **What's the worst a malicious input can do?** → [safety engineering](../05-safety-multitenancy/safety-engineering.md)
- **What does it cost, and who's paying?** → [cost attribution](../04-evals-observability/cost-attribution.md)
- **Can it leak one customer's data to another?** → [multi-tenant isolation](../05-safety-multitenancy/multi-tenant-isolation.md)

If you can't answer these, you have a demo.

## The demo-to-infrastructure gap

| Property | Demo | Infrastructure |
| --- | --- | --- |
| Correctness | "Looks right" in a few runs | Measured against a [golden set](../04-evals-observability/evals.md), gated in CI |
| Failure | Crashes / hangs | Degrades gracefully with [fallbacks](../02-reliable-outputs/model-routing.md) |
| Output | Trusted as-is | Validated, repaired, schema-checked |
| Cost | Ignored | Attributed, budgeted, alerted |
| Latency | "Fast enough on my laptop" | p50/p95/p99 SLOs under load |
| Safety | Trusts all input | Defends against [injection](../05-safety-multitenancy/safety-engineering.md) |
| Observability | `print()` | [Traces, spans, metrics, drift](../04-evals-observability/observability.md) |
| Change safety | Hope | Regression evals before every change |

## Why LLM systems are *harder* to operationalize than typical services

- **Non-determinism** breaks "write a test that asserts equality." You need
  distribution-level and rubric-based evaluation, not exact-match unit tests.
- **Silent failure.** A wrong answer looks exactly like a right one. Errors don't
  throw; they *read plausibly*. Detection requires
  [evals](../04-evals-observability/evals.md) and
  [drift monitoring](../04-evals-observability/observability.md), not exception
  handlers.
- **Upstream drift.** The model provider can update weights; your data changes; your
  retrieval index ages. The system can regress with *no code change at all*.
- **Unbounded cost and latency.** Token usage — and therefore dollars and seconds —
  depends on inputs and on how many times an [agent loops](../02-reliable-outputs/agent-guardrails.md).

## The operational baseline (minimum bar to call it "shipped")

1. **A golden eval set** that runs in CI and blocks regressions —
   [Evals](../04-evals-observability/evals.md).
2. **End-to-end tracing** with tokens, latency, cost, and errors per request —
   [Observability](../04-evals-observability/observability.md).
3. **Output validation** so malformed responses never reach downstream systems —
   [Structured output](../02-reliable-outputs/structured-output.md).
4. **Budgets** on iterations, tokens, and tool calls —
   [Agent guardrails](../02-reliable-outputs/agent-guardrails.md).
5. **Fallback paths** for provider outage, timeout, or low confidence —
   [Model routing](../02-reliable-outputs/model-routing.md).
6. **Cost attribution** per feature and tenant —
   [Cost attribution](../04-evals-observability/cost-attribution.md).
7. **Safety boundaries** for injection and data leakage —
   [Safety engineering](../05-safety-multitenancy/safety-engineering.md).

## Failure modes

- **The "Friday demo, Monday outage" pattern** — impressive launch, then a long tail
  of edge cases nobody measured.
- **Cost surprise** — a feature that was "basically free" in testing costs
  five figures a month at scale because nobody attributed tokens.
- **Silent regression** — quality drops after a model upgrade and no one notices for
  three weeks because there were no evals.

## Practitioner checklist

- [ ] Could you operate this feature for a year without it surprising you?
- [ ] Do you measure correctness with numbers, not vibes?
- [ ] Does every external dependency have a fallback?
- [ ] Can you attribute every dollar of spend to a feature and tenant?
- [ ] Would a malicious document in your retrieval corpus be contained?

## Related lessons

- [Harness engineering](./harness-engineering.md)
- [Evals](../04-evals-observability/evals.md)
- [Observability](../04-evals-observability/observability.md)
- [Production failure modes](../06-strategy-tradeoffs/production-failure-modes.md)
