# LLM observability: traces, spans, tokens, latency, errors, and drift

*Part of [04 · Evals & Observability](./README.md)*

## TL;DR

[Evals](./evals.md) tell you if the system is correct *before* you ship; observability
tells you what it's doing *in production*. LLM observability is a first-class
discipline because these systems fail silently and non-deterministically: you need
end-to-end **traces** made of **spans**, with **tokens**, **latency** (split into
TTFT/TPOT), **errors**, **quality**, and **cost** on every step — plus **drift**
detection to catch the slow regressions that no deploy caused. If you can't replay
exactly what happened on a bad request, you can't fix it.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — AI fails silently — wrong answers look exactly like right ones. Without traces, tokens, latency, and drift, you're operating blind and you learn about problems from churn.
>
> **What it changes in your decisions** — What you instrument, your incident-response plan, and how you detect slow quality decay.
>
> **Ask your eng team** — *"Can we pull up exactly what happened on a specific bad request?"*
>
> **Product risk if ignored** — Quality drifts down for weeks with no alarm, you can't debug complaints, and you're flying blind.


## Mental model

A single LLM request is a distributed transaction across many components (retrieval,
rerank, model calls, tools, validation, repair). Borrow distributed-tracing ideas, but
add the LLM-specific dimensions:

```
TRACE: "answer support ticket #4821"  (tenant=acme, feature=support_copilot)
 ├─ span: retrieve         42ms   chunks=8  recall_proxy=...
 ├─ span: rerank           18ms   kept=3
 ├─ span: model.generate  910ms   ttft=210ms tpot=14ms in=3,100 out=180 tok  $0.0042
 │    ├─ prompt (full context, redacted as needed)
 │    └─ completion + finish_reason
 ├─ span: validate         2ms    repairs=0
 └─ span: tool.create_note 75ms   idempotency_key=... status=ok
TOTAL 1.05s   $0.0046   status=ok
```

The trace is the unit of debugging; the span is the unit of measurement.

## What to capture

### Traces & spans
- One trace per request; one span per meaningful step (retrieve, rerank, each model
  call, each tool, validate, repair, route decision).
- Record inputs/outputs **with privacy controls** — prompts and completions are gold for
  debugging but may contain PII; redact/tokenize and respect
  [tenant boundaries](../05-safety-multitenancy/multi-tenant-isolation.md).
- Capture the *decisions*: which model/route was chosen, why fallback fired, which
  budget terminated an [agent](../02-reliable-outputs/agent-guardrails.md).

### Tokens
- Input vs. output tokens per call (they cost differently and behave differently —
  [prefill vs. decode](../01-inference-internals/prefill-vs-decode.md)).
- Prompt-cache hit/miss (a cheap cost lever — see
  [caching](../01-inference-internals/prompt-vs-semantic-caching.md)).
- Tokens are the raw material for [cost attribution](./cost-attribution.md).

### Latency
- **Split it:** TTFT (≈ prefill) and TPOT/inter-token (≈ decode) separately — a single
  "latency" number hides which phase is slow.
- Queueing time vs. compute time; end-to-end including retrieval/tools.
- Report **distributions (p50/p95/p99)**, never just the mean — tails are where SLOs and
  [preemption spikes](../01-inference-internals/kv-cache-management.md) live.

### Errors
- Provider errors (timeout, rate-limit, 5xx), validation/parse failures, repair
  exhaustion, tool failures, budget terminations, refusals.
- **The hard part: silent errors.** A grounded-looking hallucination throws nothing.
  Approximate quality online with proxy signals (validation pass rate, grounding
  spot-checks, [judge](./evals.md) sampling, user thumbs/edits/retries).

### Drift
The regression that no deploy caused:
- **Input drift** — query mix, length, language, new topics shift over time.
- **Output/quality drift** — judge scores, refusal rate, format-validity, grounding
  trending down.
- **Model drift** — provider updated weights underneath you; behavior changes with no
  code change.
- **Data/retrieval drift** — corpus grows/ages; [recall](../03-rag/retrieval-evals.md)
  decays.
Detect by tracking these distributions over time and alerting on shifts — and by
**re-running evals on a schedule**, not only at deploy.

## From signals to operations

- **Dashboards & SLOs:** latency (p95/p99 TTFT/TPOT), error rate, token/cost per
  request, cache-hit rate, eval scores — per feature and tenant.
- **Alerts:** on error spikes, cost spikes, cache-hit collapse, drift, budget-hit rate.
- **Trace-level debugging:** jump from an alert or a user complaint to the exact trace,
  with the full chain reconstructed.
- **Feed the loop:** sampled production traces become new [eval](./evals.md) cases;
  observed failures become [adversarial tests](./evals.md). Observability and evals are
  a cycle, not two silos.

## Guardrails vs. evaluators

Two production roles that get conflated because both "check outputs":

- **Guardrails** run **inline**, per request, and can *block* — the output is checked
  (PII, policy, format, obvious hallucination signals) before the user sees it. They
  must be fast and cheap enough to sit on the critical path, and they fail closed for
  the worst categories.
- **Evaluators** run **offline** — in CI to gate changes, and over sampled production
  traffic to measure quality trends. They can be slow, expensive, and thorough, because
  no user is waiting.

The distinction disciplines your architecture: an evaluator too slow or too expensive
to run on every request is not a guardrail, and a guardrail lightweight enough for the
hot path is usually too crude to be your quality measurement. Using an evaluator to
auto-*correct* outputs in production (grade, then regenerate on failure) is possible
but pays latency and cost per retry — reserve it for high-stakes surfaces, and log
every correction as an eval case.

## Tradeoffs

| Capture more… | Buys | Costs |
| --- | --- | --- |
| Full prompt/completion logging | Best debugging | Storage, PII/privacy risk |
| High sampling rate for judges | Tight quality signal | Extra model spend |
| Fine-grained spans | Pinpoint bottlenecks | Instrumentation overhead |
| Long retention | Trend/drift analysis | Cost, compliance scope |

Sample intelligently: trace everything cheaply (metrics), retain full payloads for a
sample + all errors, and judge-score a representative slice.

## Failure modes

- **Mean-only latency** — hides a terrible p99; users feel the tail.
- **No silent-error signal** — hallucinations and quality drops invisible until users
  churn.
- **Undetected drift** — slow decay over weeks with no alarm because nothing was
  trended.
- **PII in logs** — debugging convenience becomes a compliance/leakage incident.
- **Untagged traces** — can't slice by feature/tenant, so you can't localize a problem
  or attribute cost.

## Practitioner checklist

- [ ] Is every request a trace with per-step spans (retrieve, model, tool, validate)?
- [ ] Do you record input/output tokens, cache hits, TTFT, TPOT, cost per call?
- [ ] Are latency and cost reported as p50/p95/p99 distributions?
- [ ] Do you capture validation failures, repairs, refusals, and budget hits?
- [ ] Is there an online proxy for *quality* (judge sampling, user signals)?
- [ ] Do you trend input/output/model/data drift and alert on shifts?
- [ ] Are traces tagged by feature and tenant, with PII redaction?
- [ ] Do production traces feed back into the eval set?

## Related lessons

- [Evals](./evals.md)
- [Cost attribution](./cost-attribution.md)
- [Prefill vs. decode](../01-inference-internals/prefill-vs-decode.md)
- [Agent guardrails](../02-reliable-outputs/agent-guardrails.md)
- [Production failure modes](../06-strategy-tradeoffs/production-failure-modes.md)
