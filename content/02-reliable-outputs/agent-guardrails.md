# Agent guardrails: loop budgets, tool budgets, and termination conditions

*Part of [02 · Reliable Outputs & Tool Use](./README.md)*

## TL;DR

An agent is a loop: think, act, observe, repeat. Loops need brakes. Without
explicit **budgets** — max iterations, max tool calls, max tokens, max
wall-clock, max cost — and clear **termination conditions**, an agent can
spin forever, thrash a tool, or quietly run up a large bill. Each step looks
locally reasonable, so nobody notices until the invoice or the incident.
Guardrails make the worst case *bounded and observable* instead of
open-ended.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — Agents can loop, thrash, and run up cost with no upper bound. Budgets are how you make worst-case behavior — and worst-case spend — predictable enough to ship.
>
> **What it changes in your decisions** — Whether you ship autonomous agents at all, your per-task cost ceilings, and the UX for "I couldn't finish that."
>
> **Ask your eng team** — *"What's the most this agent can cost — or do — on a single request?"*
>
> **Product risk if ignored** — A runaway agent burns budget or takes too many actions, causing bill shock or a trust-destroying incident.


## Mental model

Treat the agent loop like any unbounded recursion in production: it needs a
base case *and* a depth limit. The model decides *what* to do next. Your
harness decides *whether it's still allowed to*.

```
while not done:
    if over_any_budget(): terminate_with_partial_result_or_escalate()
    action = model.decide(state)
    if action == STOP or goal_met(state): return result
    observe = execute(action)        # validated, idempotent tools
    state = update(state, observe)
```

## The budgets

| Budget | Caps | Prevents |
| --- | --- | --- |
| **Loop / iteration** | Max think-act cycles | Infinite reasoning loops |
| **Tool** | Total calls, per-tool calls | Thrashing one API; repeated side effects |
| **Token** | Cumulative input+output tokens | Context blowup, runaway cost |
| **Cost** | Dollars per request/session | Bill shock |
| **Wall-clock** | Total elapsed time | Hung requests, bad UX |
| **Depth** | Sub-agent / recursion depth | Fan-out explosions |

Set defaults conservatively, and raise them per-task only with
justification. The harness should enforce budgets, not request them of the
model in the prompt — a model under
[injection](../05-safety-multitenancy/safety-engineering.md) or confusion
won't respect a polite "please stop after 5 steps."

## Termination conditions

An agent should stop on the *first* of these:
- **Goal met** — a checkable success condition (output validates, task
  verified), not the model's self-assessment alone.
- **Explicit stop** — the model emits a terminal action or answer.
- **Budget exceeded** — any cap above.
- **No progress** — repeated identical actions, oscillation, or repeated
  errors. Detect loops by breaking when the same tool and args repeat N
  times.
- **Unrecoverable error** — a tool hard-fails in a way retries won't fix.

Critically, define what happens *at* termination: return the best partial
result, escalate to a human, fall back to a simpler path, or return a clean
typed error. Never just hang or dump raw state.

## Detecting "no progress"

Runaway agents often aren't infinite — they're *circular*. Here are some
cheap detectors:
- Hash (action, args). If the same hash repeats K times, stop.
- Track whether state or goal-distance is changing. If not, stop.
- Cap consecutive tool errors.

These catch the common "agent keeps calling search with the same query"
failure that a raw iteration cap would let run to the limit.

## Observability for agents

Budgets are only safe if you can *see* them. Every agent run should emit a
[trace](../04-evals-observability/observability.md) with one span per step:
action, args, tool latency, tokens, cost, and which budget, if any,
terminated it. Aggregate:
- the distribution of steps-per-task — a rising tail means a degrading agent,
- budget-hit rate — how often you terminate on a cap versus success,
- cost-per-task by [feature/tenant](../04-evals-observability/cost-attribution.md).

## Tradeoffs

- **Tight budgets** are safe and cheap, but they may cut off legitimately
  hard tasks — premature termination. **Loose budgets** solve more tasks but
  risk runaways and cost. Tune with evals: measure success rate *and* cost
  as you vary caps.
- Budgets interact with [model routing](./model-routing.md): a cheap model
  may need more steps. Escalate hard tasks rather than letting a weak model
  loop.

## Failure modes

- **Runaway agent** — no cap, circular reasoning, large bill. This is the
  canonical [production failure](../06-strategy-tradeoffs/production-failure-modes.md).
- **Tool thrash** — the same call repeats; non-idempotent versions cause
  repeated side effects (see [idempotency](./function-calling.md)).
- **Premature termination** — the budget is too tight, so hard tasks fail.
  This looks like "the agent is dumb" when it's actually "the agent was cut
  off."
- **Silent budget hits** — terminating on a cap without surfacing it hides
  a quality problem as a "completed" run.

## Practitioner checklist

- [ ] Are iteration, tool, token, cost, and time budgets all enforced in the harness?
- [ ] Is there a no-progress / loop detector beyond the raw iteration cap?
- [ ] Are termination conditions explicit, including what happens *at* termination?
- [ ] Are tool calls idempotent so a re-issued step is safe?
- [ ] Do agent traces record per-step action, tokens, cost, and the stop reason?
- [ ] Do you monitor budget-hit rate and steps-per-task over time?

## Related lessons

- [Function calling reliability & idempotency](./function-calling.md)
- [Structured output](./structured-output.md)
- [Model routing](./model-routing.md)
- [Observability](../04-evals-observability/observability.md)
- [Cost attribution](../04-evals-observability/cost-attribution.md)
- [Production failure modes](../06-strategy-tradeoffs/production-failure-modes.md)
