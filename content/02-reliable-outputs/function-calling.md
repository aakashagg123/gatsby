# Function Calling Reliability, Tool Contracts, Argument Validation, and Idempotency

*Part of [02 · Reliable Outputs & Tool Use](./README.md)*

## TL;DR

Function calling is where a model stops generating text and starts *causing effects* —
writing to databases, sending messages, moving money. That raises the stakes from
"wrong answer" to "wrong action." Reliability comes from treating tool calls like an
API boundary with an untrusted client: **tight contracts**, **strict argument
validation**, **idempotency** so retries are safe, and **authorization** so the model
can't do what the user couldn't. The model proposes; your harness disposes.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — This is where the AI stops *talking* and starts *doing* — moving money, sending email, editing records. The blast radius of a wrong action is far larger than a wrong sentence.
>
> **What it changes in your decisions** — Which actions you let the AI take autonomously vs. behind a confirmation, and your audit/compliance posture.
>
> **Ask your eng team** — *"If the model calls a tool with a hallucinated argument, what stops it from actually acting on it?"*
>
> **Product risk if ignored** — A double-charge, a wrong-customer email, or an unauthorized change — a real-world incident, not a chat mistake.


## Mental model

The model is an **untrusted client** of your tools. Its function call is a *request*,
not a command you execute blindly:

```
model proposes call ──▶ validate args (schema + semantics)
                    ──▶ authorize (can THIS user/tenant do this?)
                    ──▶ execute idempotently (safe to retry)
                    ──▶ return structured result (incl. errors the model can act on)
```

Every arrow can reject. A hallucinated or malformed call should fail validation, not
hit your database.

## Tool contracts

A tool contract is the schema + semantics + guarantees of a callable:

- **Crisp schema.** Typed, required vs. optional, enums, formats, ranges. This is the
  same [structured-output](./structured-output.md) discipline applied to *arguments*.
- **Descriptions are part of the contract.** The model picks and fills tools from
  their names/descriptions. Vague descriptions cause wrong tool selection and bad
  arguments — write them like API docs, with units and examples.
- **Narrow surface area.** Fewer, well-scoped tools beat many overlapping ones; the
  model confuses similar tools. Don't expose a raw `run_sql` when you mean
  `get_orders_by_customer`.
- **Errors are contractual.** Return structured, actionable errors ("customer_id not
  found") so the model can recover, not opaque 500s.

## Argument validation

Never pass model-provided arguments straight through:
- **Syntactic + semantic validation** against the schema (types, enums, ranges,
  referential existence).
- **Hallucinated arguments are common** — plausible-looking IDs, dates, enum values
  that don't exist. Validate against the real system of record before acting.
- **On invalid args, feed the error back** for a bounded [repair](./structured-output.md)
  rather than executing or crashing.

## Idempotency — the keystone for safe retries

Models retry, networks fail, agents re-issue calls. If a tool isn't idempotent, a
retry can double-charge a card or send two emails.

- **Idempotency keys.** Have the caller supply (or the harness derive) a stable key per
  logical operation; the tool dedupes on it so repeats are no-ops returning the prior
  result.
- **Prefer idempotent designs.** `set_status(order, shipped)` is naturally idempotent;
  `increment_balance(+10)` is not — model it as `apply_transaction(txn_id, +10)`.
- **Separate read vs. write.** Reads are freely retryable; writes need keys. Mark which
  tools have side effects so the harness knows what's safe to repeat.
- This is what makes [agent guardrails](./agent-guardrails.md) and retry/fallback logic
  safe: you can re-run a step without fear.

## Authorization & boundaries

The model must never be able to do something the *user* couldn't:
- **Enforce permissions in the tool, keyed on the real session/tenant** — not on
  arguments the model supplies. A model told "you are admin" by a
  [prompt injection](../05-safety-multitenancy/safety-engineering.md) must still be
  blocked by the tool's own authz.
- **Scope every call to the tenant/user context** to prevent
  [cross-tenant access](../05-safety-multitenancy/multi-tenant-isolation.md).
- **Least privilege.** Give tools the minimum scope they need; dangerous actions get
  confirmation or human approval.

## Reliability patterns

- **Parallel vs. sequential calls** — validate and (where side-effecting) order them;
  watch for the model issuing conflicting parallel writes.
- **Timeouts + retries with backoff** — but only retry idempotent operations
  automatically.
- **Circuit breakers** — if a tool is failing, stop calling it and degrade rather than
  hammering it.
- **Result shaping** — return concise, structured results; dumping a 10k-token API
  response back into context wrecreates a [context-engineering](../00-foundations/context-engineering.md)
  problem.

## Failure modes

- **Hallucinated tool call** — the model invents a tool or an argument; caught by
  validating tool names and args against the real contract/system.
- **Non-idempotent retry** — double-send / double-charge after a timeout retry.
- **Confused-deputy / injection** — retrieved or tool-returned content tells the model
  to call a dangerous tool; blocked by tool-side authz, not by trusting the model.
- **Wrong tool selected** — overlapping/vague tools; fix descriptions and narrow the
  surface.
- **Context blowup** — verbose tool results crowd out the task; shape and truncate them.

## Practitioner checklist

- [ ] Does every tool have a typed schema *and* clear, example-rich descriptions?
- [ ] Are all model-supplied arguments validated against the real system before use?
- [ ] Is every side-effecting tool idempotent (keys) or modeled to be?
- [ ] Is authorization enforced in the tool on the real session — never on model claims?
- [ ] Are only idempotent operations auto-retried?
- [ ] Are tool errors structured and actionable for recovery?
- [ ] Is the tool surface narrow and least-privilege?

## Related lessons

- [Structured output](./structured-output.md)
- [Agent guardrails](./agent-guardrails.md)
- [Safety engineering](../05-safety-multitenancy/safety-engineering.md)
- [Multi-tenant isolation](../05-safety-multitenancy/multi-tenant-isolation.md)
- [Production failure modes](../06-strategy-tradeoffs/production-failure-modes.md)
