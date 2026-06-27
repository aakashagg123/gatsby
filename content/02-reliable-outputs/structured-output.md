# Structured Output: Validation, Repair Loops, and Fallback Chains

*Part of [02 · Reliable Outputs & Tool Use](./README.md)*

## TL;DR

When a downstream system expects JSON (or any schema), "usually valid" is a production
incident waiting to happen. Reliable structured output is a *pipeline*, not a prompt:
**constrain** generation where you can, **validate** every output against a schema,
**repair** failures by feeding the error back, and **fall back** through progressively
safer options so a malformed response never reaches your business logic. The goal is a
component that returns valid data or a clean, typed error — never garbage.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — Most "the AI broke the workflow" incidents are a malformed output that a downstream system trusted. This is reliability your users — and your integrations — feel immediately.
>
> **What it changes in your decisions** — Your integration/API commitments, your error budget, and what "done" means for an AI feature that feeds other systems.
>
> **Ask your eng team** — *"When the model returns invalid output, does it crash, retry, or degrade gracefully?"*
>
> **Product risk if ignored** — One parse error takes down an entire automated workflow and erodes trust in the whole feature.


## Mental model

Model output is **untrusted input**. You wouldn't `JSON.parse()` a request body and
use it without validation; don't do it with a model either. The pipeline:

```
generate ──▶ parse ──▶ validate(schema) ──▶ ✅ typed object
   ▲           │            │
   │           └─ fail ─────┤
   │                        ▼
   └───── repair loop ◀── error fed back (bounded retries)
                            │ still failing
                            ▼
                      fallback chain ──▶ safer model / stricter mode / default / typed error
```

## Layer 1 — Constrain generation (prevent, don't just detect)

The cheapest invalid output is the one that can't be produced.
- **Constrained / structured decoding** (grammar- or schema-guided, e.g. JSON-schema
  modes, GBNF grammars, "JSON mode," tool/function schemas) masks the token
  distribution so only schema-valid tokens can be emitted. This makes *syntactic*
  validity near-certain.
- **Caveat:** constrained decoding guarantees the output *parses and fits the schema*,
  not that it's *semantically correct*. A grammar can force `{"age": 200}` to be valid
  JSON; it can't make 200 a sensible age. You still need validation.
- Be aware constrained decoding can interact with quality — over-tight grammars can
  push the model into awkward continuations; pair it with clear schema descriptions.

## Layer 2 — Validate (always, even with constrained decoding)

Validate every output against a real schema (Pydantic, JSON Schema, zod, protobuf):
- **Syntactic:** does it parse and match types/required fields?
- **Semantic:** are values in range, enums legal, references resolvable, invariants
  held? (`end_date > start_date`, `total == sum(items)`, ids that exist.)
- Validation produces a precise, machine-readable error — which is the fuel for the
  repair loop.

## Layer 3 — Repair loop (bounded)

On validation failure, send the model the invalid output **plus the specific error**
and ask it to fix only what's wrong:

```
for attempt in 1..MAX_REPAIRS:        # MAX_REPAIRS is small (1–2)
    out = model(prompt + last_output + validation_error)
    if validate(out): return out
return fallback(...)                   # don't loop forever
```

Discipline:
- **Bound it.** One or two repairs, then fall back. Unbounded repair is an
  [agent runaway](./agent-guardrails.md) and a cost leak.
- **Be specific.** "Field `priority` must be one of [low, med, high]; got `urgent`" repairs
  far better than "invalid JSON."
- **Track repair rate** in [observability](../04-evals-observability/observability.md) —
  a rising rate signals prompt/model/schema drift.

## Layer 4 — Fallback chain

When repair fails, degrade deliberately instead of throwing:
1. **Stricter generation** — re-run with constrained decoding / lower temperature.
2. **A more capable model** — escalate via [model routing](./model-routing.md) for the
   hard case.
3. **A safe default / partial result** — e.g. return the fields you *could* validate,
   flag the rest.
4. **A clean typed error** — surface a structured failure the caller can handle and
   that [degraded-mode UX](./model-routing.md) can render — never a stack trace or raw
   model text.

## Tradeoffs

| Lever | Buys | Costs |
| --- | --- | --- |
| Constrained decoding | Near-certain valid syntax | Possible quality skew; not all providers/grammars |
| More repair attempts | Higher success rate | Latency + tokens + cost |
| Escalate to bigger model | Rescues hard cases | $$ and latency; route carefully |
| Strict schema | Safety, clear contracts | More repair churn if model struggles |

## Failure modes

- **Trusting `JSON.parse` with no schema** — a stray markdown fence or trailing comma
  crashes the workflow. (Strip fences defensively; still validate.)
- **Unbounded repair loops** — a persistently malformed case retries forever, burning
  cost — see [budgets](./agent-guardrails.md).
- **Valid-but-wrong** — schema passes, values are nonsense; only semantic validation
  and [evals](../04-evals-observability/evals.md) catch it.
- **Quantization-induced malformation** — [aggressive quantization](../01-inference-internals/quantization-formats.md)
  degrades strict-format adherence; watch JSON validity after model swaps.
- **Silent schema drift** — you tightened the schema; repair rate spiked; nobody
  noticed because it wasn't monitored.

## Practitioner checklist

- [ ] Is every model output validated against an explicit schema before use?
- [ ] Do you validate semantics (ranges, enums, invariants), not just syntax?
- [ ] Is the repair loop bounded (1–2 tries) with specific error feedback?
- [ ] Is there a fallback chain ending in a clean typed error, never a crash?
- [ ] Do you track parse-failure and repair rates as metrics?
- [ ] Did structured-output validity hold after your last model/quantization change?

## Related lessons

- [Function calling reliability](./function-calling.md)
- [Agent guardrails](./agent-guardrails.md)
- [Model routing & degraded-mode UX](./model-routing.md)
- [Quantization formats](../01-inference-internals/quantization-formats.md)
- [Production failure modes](../06-strategy-tradeoffs/production-failure-modes.md)
