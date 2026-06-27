# Multi-Tenant Isolation, Cache Safety, and Cross-User Context Contamination Prevention

*Part of [05 · Safety & Multi-tenancy](./README.md)*

## TL;DR

When many customers (tenants) and users share the same LLM infrastructure, the failure
that ends companies is **one tenant's data appearing in another's results**. LLM
systems add new leak paths that traditional multi-tenant apps don't have:
**[semantic caches](../01-inference-internals/prompt-vs-semantic-caching.md)** keyed only
on text, shared **context windows**, reused **[KV cache](../01-inference-internals/kv-cache-management.md)**,
and **retrieval indexes** without per-tenant scoping. Isolation must be enforced on
every one of these paths, defaulting to "scoped to this tenant" everywhere.

## Mental model

Every place where computation or data is **shared or reused** across requests is a
potential cross-tenant channel. Enumerate them and put a tenant boundary on each:

```
request(tenant=T, user=U)
  ├─ retrieval index      → filter to T's documents (ACL/tenant pre-filter)
  ├─ semantic cache       → key MUST include T (and permission scope)
  ├─ prompt/KV cache reuse→ share only non-sensitive prefixes; never reuse T's KV for T'
  ├─ conversation memory  → scoped to U; never bleed into another session
  ├─ context window        → only T/U-authorized content assembled in
  └─ logs/traces          → tenant-tagged, access-controlled
```

The default for anything shared must be **deny / scope to tenant**, not "share unless we
remember to isolate."

## The leak paths

### 1. Semantic cache contamination (the classic)
A [semantic cache](../01-inference-internals/prompt-vs-semantic-caching.md) returns a
prior *response* for a similar query. If the key is just the query text, **User B can
receive User A's answer** — which may contain A's private data, or simply be wrong for
B's permissions/tenant.
- **Fix:** the cache key must include **tenant id, and the permission/role scope** (and
  often user id) — not just the embedded query. Two identical questions from different
  tenants are *different* cache entries.
- Cache *personalized or authorization-dependent* responses per scope, or not at all.

### 2. Retrieval cross-tenant leakage
A shared vector index without a tenant filter can surface Tenant A's documents to Tenant
B — a [RAG](../03-rag/rag-architecture.md) isolation failure.
- **Fix:** tag every chunk with tenant/ACL metadata and apply it as a **hard pre-filter**
  before ranking (not a post-filter, not a soft signal). Prefer per-tenant namespaces/
  indexes for strong isolation where feasible.

### 3. Context / conversation contamination
Memory or history from one user/session bleeding into another — usually a state-
management or cache-key bug (shared session store, mis-scoped memory).
- **Fix:** scope all memory/history strictly to the (tenant, user, session); never use a
  global or loosely-keyed store.

### 4. KV / prompt-cache reuse across trust boundaries
[Prefix/KV cache reuse](../01-inference-internals/kv-cache-management.md) is great for
cost — but reusing a *tenant-specific* prefix's KV for another tenant could expose data.
- **Fix:** share KV only for **non-sensitive, common prefixes** (system prompt, tool
  defs). Anything containing tenant data must not be cross-tenant reusable. Scope cache
  pools by tenant where the threat model demands it.

### 5. Logs, traces, and training data
[Observability](../04-evals-observability/observability.md) stores and any fine-tuning
pipeline can pool tenant data.
- **Fix:** tenant-tag and access-control all traces; redact PII; never train on one
  tenant's data and serve another without explicit consent and isolation.

## Defense principles

- **Tenant context is non-negotiable on every request.** Plumb an authenticated tenant/
  user identity through the whole pipeline; every cache key, retrieval query, tool call,
  and log line carries it.
- **Scope by default, share by exception.** Sharing (caches, indexes, KV) is an
  optimization you *opt into* for explicitly non-sensitive data — never the default.
- **Enforce in code, not in the prompt.** Like [permission boundaries](./safety-engineering.md),
  isolation must be structural; you cannot ask the model nicely to keep tenants apart.
- **Test isolation adversarially.** [Evals](../04-evals-observability/evals.md) that
  specifically try to retrieve/cache across tenants, run in CI.

## Tradeoffs

| Isolation choice | Stronger isolation | Cost |
| --- | --- | --- |
| Per-tenant indexes/namespaces | Strong retrieval isolation | More infra, less sharing |
| Tenant+scope cache keys | No cache cross-leak | Lower hit rate (fewer shared entries) |
| No cross-tenant KV reuse | No KV leak | Less prefix-cache savings |
| Shared everything | Cheapest | Unacceptable leak risk |

The recurring tension is **isolation vs. the cost savings of sharing**. Resolve it by
sharing only what is provably non-sensitive and scoping everything else — and by pricing
the isolation in, because a single cross-tenant leak costs more than years of the
savings.

## Failure modes

- **Query-only semantic cache key** → one user's answer served to another. (The most
  common and most damaging.)
- **Unfiltered shared index** → cross-tenant documents retrieved.
- **Global/mis-scoped memory store** → conversation bleed between users.
- **Cross-tenant KV reuse** → data exposure via cached computation.
- **Untagged logs** → tenant data pooled and over-exposed.
- **"It works in single-tenant testing"** → isolation bugs only appear under concurrent
  multi-tenant load; test that explicitly.

## Practitioner checklist

- [ ] Does an authenticated tenant/user identity flow through every stage?
- [ ] Do **all** cache keys include tenant (and permission scope), never query-only?
- [ ] Is retrieval hard-filtered by tenant/ACL before ranking (or per-tenant indexed)?
- [ ] Is conversation memory strictly scoped to (tenant, user, session)?
- [ ] Is cross-tenant KV/prompt-cache reuse limited to non-sensitive prefixes?
- [ ] Are traces/logs tenant-tagged, access-controlled, and PII-redacted?
- [ ] Do adversarial cross-tenant retrieval/cache tests run in CI under concurrency?

## Related lessons

- [Safety engineering](./safety-engineering.md)
- [Prompt vs. semantic caching](../01-inference-internals/prompt-vs-semantic-caching.md)
- [KV cache management](../01-inference-internals/kv-cache-management.md)
- [RAG architecture](../03-rag/rag-architecture.md)
- [Cost attribution](../04-evals-observability/cost-attribution.md)
