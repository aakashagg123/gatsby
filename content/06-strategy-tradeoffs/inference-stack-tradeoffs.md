# Latency, Quality, Cost, and Reliability Across the Full Inference Stack

*Part of [06 · Strategy & Tradeoffs](./README.md)*

## TL;DR

Almost every decision in an LLM system is a move in a four-way tradeoff between
**latency**, **quality**, **cost**, and **reliability**. You rarely improve one without
spending another. Mature AI engineering means making these tradeoffs *deliberately and
per-use-case* — driven by explicit SLOs and budgets — instead of accepting whatever
defaults give you. This lesson is the map that connects every other lesson in the
repository to the axis it moves.

## The four axes

- **Latency** — TTFT and TPOT ([prefill vs. decode](../01-inference-internals/prefill-vs-decode.md)),
  end-to-end including retrieval/tools; judged at p95/p99, not the mean.
- **Quality** — correctness, grounding, format validity, helpfulness; measured by
  [evals](../04-evals-observability/evals.md), not vibes.
- **Cost** — $/request and per-unit economics, attributed by
  [feature/tenant](../04-evals-observability/cost-attribution.md).
- **Reliability** — availability, graceful degradation, consistency, isolation; the
  worst-case behavior, not the average.

You cannot maximize all four. The job is to hit your *required* level on each and
optimize the rest.

## Same lever, different axis — the whole stack

Each technique elsewhere in this repo is a trade among the four:

| Lever | Helps | Spends | Lesson |
| --- | --- | --- | --- |
| Bigger model | Quality | Cost, latency | [Routing](../02-reliable-outputs/model-routing.md) |
| Smaller/cheaper model | Cost, latency | Quality | [Routing](../02-reliable-outputs/model-routing.md) |
| Quantization (INT4…) | Cost, latency, memory | Some quality | [Quantization](../01-inference-internals/quantization-formats.md) |
| Distillation | Cost, latency | Quality, generality | [Distillation](../01-inference-internals/speculative-quantization-distillation.md) |
| Speculative decoding | Latency | A little cost/memory; quality neutral | [Spec decoding](../01-inference-internals/speculative-quantization-distillation.md) |
| Bigger batches | Cost (throughput) | Per-user latency | [Batching](../01-inference-internals/batching-and-paged-attention.md) |
| Prompt caching | Cost, latency | ~Nothing (lossless) | [Caching](../01-inference-internals/prompt-vs-semantic-caching.md) |
| Semantic caching | Cost, latency | Quality risk (staleness/wrong hits) | [Caching](../01-inference-internals/prompt-vs-semantic-caching.md) |
| More retrieved context | Quality (recall) | Cost, latency, distraction | [RAG](../03-rag/rag-architecture.md) |
| Reranking | Quality (precision) | A little latency/cost | [RAG](../03-rag/rag-architecture.md) |
| Repair loops / retries | Reliability, quality | Latency, cost | [Structured output](../02-reliable-outputs/structured-output.md) |
| Fallback / multi-provider | Reliability | Cost, complexity | [Routing](../02-reliable-outputs/model-routing.md) |
| Tight agent budgets | Cost, reliability | Quality on hard tasks | [Guardrails](../02-reliable-outputs/agent-guardrails.md) |
| Tenant-scoped caches | Reliability (isolation) | Cost (lower hit rate) | [Isolation](../05-safety-multitenancy/multi-tenant-isolation.md) |

Read this table as the unifying thread: there is no globally "best" configuration, only
the best one *for a given SLO*.

## The classic tensions

- **Latency ↔ Quality** — a bigger model or more retrieval/reasoning is better but
  slower. Cascades and routing let you spend latency only on hard requests.
- **Cost ↔ Quality** — cheaper/smaller/quantized cuts cost and may cut quality; keep it
  *within* a quality floor enforced by evals.
- **Latency ↔ Cost (throughput)** — batching lowers $/token but raises per-user TPOT;
  pick the operating point from your SLO.
- **Reliability ↔ Cost/Latency** — retries, fallbacks, multi-provider, and isolation all
  add cost/latency to buy resilience.
- **Quality ↔ Reliability** — the most capable single model may be less *available* than
  a routed multi-provider setup that's slightly weaker but never down.

## How to make the tradeoff deliberately

1. **Set SLOs/budgets per use case.** Interactive chat ≠ overnight batch job ≠
   safety-critical workflow. Define required latency, quality floor, cost ceiling, and
   availability *separately* for each.
2. **Measure all four.** [Observability](../04-evals-observability/observability.md) for
   latency/cost/reliability, [evals](../04-evals-observability/evals.md) for quality. You
   can't trade what you don't measure.
3. **Optimize the slack, protect the floor.** Improve the unconstrained axes without
   breaching the required level on the others — e.g. cut cost via quantization *only if*
   evals stay above the quality floor.
4. **Differentiate by request.** [Route](../02-reliable-outputs/model-routing.md) easy
   traffic cheap/fast, hard traffic capable; don't pay worst-case cost for the average
   request.
5. **Revisit continuously.** Models, prices, and traffic change; today's optimal point
   drifts — re-evaluate as part of operations.

## Failure modes

- **Optimizing one axis blindly** — cost-cutting that quietly tanks quality, or a
  latency push that wrecks reliability.
- **One config for all requests** — paying premium cost/latency on easy cases or starving
  hard ones.
- **No SLOs** — "make it faster/cheaper/better" with no target means you can't tell when
  you're done or when you've gone too far.
- **Mean-driven decisions** — tuning to averages while p99 latency and worst-case
  reliability — the things users actually feel — degrade.

## Practitioner checklist

- [ ] Do you have explicit latency, quality, cost, and reliability targets per use case?
- [ ] Do you measure all four (evals + observability), at the tail, not just the mean?
- [ ] Does each optimization protect the floor on the axes it isn't improving?
- [ ] Do you route/differentiate by request difficulty instead of one global config?
- [ ] Do you re-evaluate the operating point as models, prices, and traffic change?

## Related lessons

- [Prefill vs. decode](../01-inference-internals/prefill-vs-decode.md)
- [Model routing](../02-reliable-outputs/model-routing.md)
- [Cost attribution](../04-evals-observability/cost-attribution.md)
- [Evals](../04-evals-observability/evals.md)
- [Production failure modes](./production-failure-modes.md)
