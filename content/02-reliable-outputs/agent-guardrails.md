# Agent Guardrails: Loop Budgets, Tool Budgets, and Termination Conditions

*Part of [02 · Reliable Outputs & Tool Use](./README.md)*

## TL;DR

An agent is a loop: think → act → observe → repeat. Loops need brakes. Without
explicit **budgets** (max iterations, max tool calls, max tokens, max wall-clock, max
cost) and clear **termination conditions**, an agent can spin forever, thrash a tool,
or quietly run up a large bill — and because each step looks locally reasonable,
nobody notices until the invoice or the incident. Guardrails make the worst case
*bounded and observable* instead of open-ended.

## Mental model

Treat the agent loop like any unbounded recursion in production: it needs a base case
*and* a depth limit. The model decides *what* to do next; your harness decides
*whether it's still allowed to*.

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

Set defaults conservatively; raise per-task only with justification. Budgets should be
enforced by the harness, not requested of the model in the prompt — a model under
[injection](../05-safety-multitenancy/safety-engineering.md) or confusion won't respect
a polite "please stop after 5 steps."

## Termination conditions

An agent should stop on the *first* of:
- **Goal met** — a checkable success condition (output validates, task verified), not
  the model's self-assessment alone.
- **Explicit stop** — the model emits a terminal action/answer.
- **Budget exceeded** — any cap above.
- **No progress** — repeated identical actions, oscillation, or repeated errors
  (detect loops: same tool+args N times → break).
- **Unrecoverable error** — a tool hard-fails in a way retries won't fix.

Critically, define what happens *at* termination: return best partial result, escalate
to a human, fall back to a simpler path, or return a clean typed error — never just
hang or dump raw state.

## Detecting "no progress"

Runaway agents often aren't infinite — they're *circular*. Cheap detectors:
- Hash (action, args); if the same hash repeats K times, stop.
- Track whether state/goal-distance is changing; if not, stop.
- Cap consecutive tool errors.
These catch the common "agent keeps calling search with the same query" failure that a
raw iteration cap would let run to the limit.

## Observability for agents

Budgets are only safe if you can *see* them. Every agent run should emit a
[trace](../04-evals-observability/observability.md) with one span per step: action,
args, tool latency, tokens, cost, and which budget (if any) terminated it. Aggregate:
- distribution of steps-per-task (a rising tail = degrading agent),
- budget-hit rate (how often you terminate on a cap vs. success),
- cost-per-task by [feature/tenant](../04-evals-observability/cost-attribution.md).

## Tradeoffs

- **Tight budgets** → safe and cheap, but may cut off legitimately hard tasks
  (premature termination). **Loose budgets** → solves more, risks runaways and cost.
  Tune with evals: measure success rate *and* cost as you vary caps.
- Budgets interact with [model routing](./model-routing.md): a cheap model may need
  more steps; escalate hard tasks rather than letting a weak model loop.

## Failure modes

- **Runaway agent** — no cap, circular reasoning, large bill. (The canonical
  [production failure](../06-strategy-tradeoffs/production-failure-modes.md).)
- **Tool thrash** — same call repeated; non-idempotent versions cause repeated side
  effects (see [idempotency](./function-calling.md)).
- **Premature termination** — budget too tight, hard tasks fail; looks like "the agent
  is dumb" when it's actually "the agent was cut off."
- **Silent budget hits** — terminating on cap without surfacing it hides a quality
  problem as a "completed" run.

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
