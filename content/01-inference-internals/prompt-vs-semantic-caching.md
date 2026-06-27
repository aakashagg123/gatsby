# Prompt Caching vs. Semantic Caching

*Part of [01 · Inference Internals](./README.md)*

## TL;DR

They share the word "caching" and almost nothing else. **Prompt caching** reuses the
model's internal computation (the [KV cache](./kv-cache-management.md)) for an
*exact* shared prefix — it is lossless and changes only cost/latency, never the
answer. **Semantic caching** returns a previously generated *response* when a new
query is *similar* — it can skip the model entirely but risks returning a subtly
wrong answer. One is a performance optimization; the other is a correctness gamble
you must validate.

> 🧭 **In plain terms**
>
> Caching means reusing work you already did so you don't pay for it twice. **Prompt caching** is your café remembering the prep for your regular order — same drink, just faster and cheaper, and *never wrong*. **Semantic caching** is the barista guessing today's order is 'close enough' to last time and handing you the old one — usually fine, occasionally the wrong drink. One is free speed; the other can quietly serve a stale or wrong answer, which is a trust (and sometimes privacy) problem, not just a performance tweak.


<!--sep-->

> 🎯 **For the AI-native PM**
>
> **Why it matters** — Caching is one of your biggest levers on cost and latency — but *semantic* caching can serve a wrong or stale answer, which is a trust and even a compliance problem, not just a performance tweak.
>
> **What it changes in your decisions** — Cost targets, whether to enable semantic caching for a given feature, and the SLAs you can stand behind.
>
> **Ask your eng team** — *"Are we caching responses across users, and how do we know we're not serving the wrong one?"*
>
> **Product risk if ignored** — A loosely-tuned cache serves one user's answer to another — a privacy incident dressed up as an optimization.


## The two are not the same layer

```
                      ┌─────────────────────────────────────────┐
   request ──────────▶│ semantic cache?  (embed query, ANN match)│──hit──▶ stored response
                      └─────────────────────────────────────────┘         (NO model call)
                                       │ miss
                                       ▼
                      ┌─────────────────────────────────────────┐
                      │ model server: prompt cache reuses KV for │──▶ generate tokens
                      │ the matching prompt *prefix*             │
                      └─────────────────────────────────────────┘
```

## Prompt (prefix / KV) caching

**What it reuses:** the computed key/value tensors for a prompt *prefix* that is
byte-for-byte identical to one seen before. The [prefill](./prefill-vs-decode.md)
phase for that prefix is skipped; decode proceeds normally.

**Why it matters:** prefill is compute-heavy and scales with input length. If 2,000
tokens of system prompt + tool definitions are shared across every request, caching
that prefix removes most of the prefill cost for every call after the first.

**Properties:**
- **Lossless.** The output distribution is unchanged — you compute the same thing,
  just skip recomputing the shared part.
- **Prefix-only and order-sensitive.** The cache matches from the start of the
  prompt. One changed byte near the top (a timestamp, a user name) invalidates
  everything after it. This is why [context engineering](../00-foundations/context-engineering.md)
  insists on a *stable prefix*.
- **Time-limited.** Cached entries expire (provider TTLs are short, often minutes);
  self-hosted entries are subject to [KV cache eviction](./kv-cache-management.md)
  under memory pressure.

**Design rules:**
- Put stable content (system prompt, policies, tool contracts, few-shot examples)
  *first*; put volatile content (the user's query) *last*.
- Keep the prefix identical across requests — no per-request strings up top.
- In multi-tenant systems, be deliberate: a shared prefix is fine, but never let
  cache *reuse* cross a trust boundary in a way that exposes data — see
  [multi-tenant cache safety](../05-safety-multitenancy/multi-tenant-isolation.md).

## Semantic caching

**What it reuses:** a *final response*. The query is embedded; if its nearest
neighbor in a vector store is within a similarity threshold, the stored answer is
returned and the model is never called.

**Why it matters:** the biggest possible win — you skip generation entirely, cutting
latency to a lookup and cost to ~zero for repeat-ish questions (FAQs, common
support queries).

**Properties & risks:**
- **Lossy and approximate.** "Similar embedding" ≠ "same correct answer." `What's my
  account balance?` and `What was my account balance last month?` can sit close in
  embedding space and demand totally different answers.
- **Staleness.** A cached answer can be correct today and wrong tomorrow (prices,
  inventory, policy). Needs TTLs and invalidation — connects to retrieval
  [freshness](../03-rag/rag-architecture.md).
- **Context-blind.** Two users asking the same words may need different answers
  (different permissions, tenant, locale). Caching across users without keying on
  context causes [cross-user contamination](../05-safety-multitenancy/multi-tenant-isolation.md).
- **Threshold tuning is a precision/recall problem.** Too loose → wrong answers
  served confidently; too tight → almost no hits.

## Tradeoffs at a glance

| | Prompt (prefix) caching | Semantic caching |
| --- | --- | --- |
| Reuses | KV computation of shared prefix | Final response |
| Correctness impact | None (lossless) | Can return wrong/stale answers |
| Match type | Exact prefix | Approximate (embedding similarity) |
| Saves | Prefill compute | The entire model call |
| Main risk | Cache misses from unstable prefixes | False hits, staleness, contamination |
| Who owns it | Mostly the inference server/provider | You, in the application harness |

## Failure modes

- **Silent prefix busting** — a logging timestamp injected at the top of the system
  prompt drops your prompt-cache hit rate to ~0 and triples cost. Catch it with
  [cost attribution](../04-evals-observability/cost-attribution.md) and cache-hit
  metrics in [observability](../04-evals-observability/observability.md).
- **Confident wrong semantic hit** — threshold too loose; users get plausible,
  incorrect answers with no model call to catch it. Guard with conservative
  thresholds, context-aware cache keys, and [evals](../04-evals-observability/evals.md).
- **Stale semantic cache** — yesterday's price served today. Add TTLs + event-based
  invalidation.

## Practitioner checklist

- [ ] Is your prompt prefix stable enough to actually hit the prompt cache?
- [ ] Do you measure prompt-cache hit rate as a first-class metric?
- [ ] Does your semantic cache key include user/tenant/permission context?
- [ ] Do semantically cached entries have TTLs and invalidation hooks?
- [ ] Have you evaluated semantic-cache false-hit rate on a labeled set?

## Related lessons

- [KV cache management](./kv-cache-management.md)
- [Prefill vs. decode](./prefill-vs-decode.md)
- [Context engineering](../00-foundations/context-engineering.md)
- [Multi-tenant isolation & cache safety](../05-safety-multitenancy/multi-tenant-isolation.md)
- [Cost attribution](../04-evals-observability/cost-attribution.md)
