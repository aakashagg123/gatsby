# Agentic workflows — recap & real-world examples

*Part of [Agentic workflows for the product leader](./README.md)*

## Real-world examples & war stories

**A multi-agent system that won, and what it cost (2025).** In June 2025 Anthropic
described its multi-agent research system. A lead agent split a question and sent
subagents to search in parallel. On Anthropic's internal research evaluation, it beat a
single-agent Claude Opus 4 by 90.2%. It also used about 15 times the tokens of a chat,
against about 4 times for a single agent. 🎯 *Takeaway:* parallel workers can win on broad
research. They multiply cost. Estimate both before you
[add an agent](./orchestrating-more-than-one-agent.md).

**The same article says where it does not fit.** Anthropic notes that most coding tasks
"involve fewer truly parallelizable tasks than research." It also says agents are "not yet
great at coordinating and delegating to other agents in real time." 🎯 *Takeaway:* the
pattern depends on the task. Check how much of your work is truly independent. See
[choosing a pattern](./choosing-a-workflow-pattern.md).

**The counter-view (2025).** Cognition, which builds a coding agent, argued that running
agents in parallel tends to create more problems than it solves. Its reasoning is that
actions carry hidden decisions, and agents without shared context make conflicting ones.
🎯 *Takeaway:* treat shared context as a design requirement for any multi-agent split. This
summary comes from search-result excerpts. The original page could not be opened.

**Vague delegation (2025).** Anthropic reports that when its lead agent gave short,
vague tasks, subagents "misinterpreted the task or performed the exact same searches as
other agents." Clear briefs with an objective, an output format and boundaries fixed it.
🎯 *Takeaway:* most multi-agent failures are
[specification failures at the handoff](./orchestrating-more-than-one-agent.md).

**Updating a system that is never idle (2025).** Anthropic's research agents run for long
periods, so a code update can land in the middle of a run. It used "rainbow deployments,"
which shift traffic gradually so running agents are not cut off. It also built agents to
resume from where an error happened instead of restarting. 🎯 *Takeaway:*
[durability covers deployments too](./making-a-workflow-durable-and-worth-owning.md), not
only crashes.

**The refund that vanished (an illustration).** A workflow waits three days for a manager's
approval. The server restarts on day two. State was held in memory, so the request is gone
and the customer never hears back. 🎯 *Takeaway:* any wait longer than one run needs saved
state, a timer and an escalation path. See the
[worked example](./making-a-workflow-durable-and-worth-owning.md).

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [Choosing a workflow pattern](./choosing-a-workflow-pattern.md) | Five patterns cover most work. Pick the first one that fits. | Which of the five is this, and could the one before it do the job? |
| [Orchestrating more than one agent](./orchestrating-more-than-one-agent.md) | Every extra agent needs a named bottleneck. The cost is large. | Would one better-built agent do this, and have we tried? |
| [Making a workflow durable, and worth owning](./making-a-workflow-durable-and-worth-owning.md) | Durability comes first: saved state, waits, retries, safe repeats, undo. Ownership follows. | If we restarted mid-run, would every workflow resume with nothing done twice? |

**The through-line:** the word "workflow" adds two things a single agent run does not face.
One is choosing a shape for several steps or agents. The other is surviving the real time a
long process takes. Most failures are not about the pattern chosen. They are an over-flexible
pattern bought by default, vague handoffs, or a durability gap found on the first restart.
This module stays at the decision level. The engineering depth lives in
[Multi-agent systems & protocols](../agentic-ai/multi-agent-and-protocols.md),
[Flowable](../flowable/README.md) and
[Agentic AI as a product](../agentic-ai/agentic-ai-as-a-product.md).

> **Walk-away question:** *"For this workflow: do we know which pattern it is and why a
> simpler one would not do, does every added agent earn its cost, and would it survive a
> restart mid-run with nothing done twice?"*

If yes, this is a workflow worth building. If no, you know which lesson to reread.

## Test yourself

1. **Name the five workflow patterns.**
   <details><summary>Answer</summary>Prompt chaining, routing, parallelization, orchestrator-workers, and evaluator-optimizer. (<a href="./choosing-a-workflow-pattern.md">Lesson 1</a>)</details>
2. **In which patterns does your code decide the path, and in which does a model decide?**
   <details><summary>Answer</summary>Chaining, routing and parallelization keep the path in your code. In orchestrator-workers a model decides the path. In evaluator-optimizer a model decides when to stop. (<a href="./choosing-a-workflow-pattern.md">Lesson 1</a>)</details>
3. **A task has three fixed steps and two input types. Which pattern should you start with, and why not orchestrator-workers?**
   <details><summary>Answer</summary>Route, then a chain per type. The steps are known, so a model-led pattern adds cost and unpredictability for no gain. (<a href="./choosing-a-workflow-pattern.md">Lesson 1</a>)</details>
4. **Why is an evaluator-optimizer loop risky without a limit?**
   <details><summary>Answer</summary>It can run until the budget runs out. Set a round limit, and use a real check such as a test or rubric where you can. (<a href="./choosing-a-workflow-pattern.md">Lesson 1</a>)</details>
5. **What does multi-agent cost, and when does it help?**
   <details><summary>Answer</summary>Anthropic measured about 15 times the tokens of a chat, against about 4 times for an agent. It helps on broad, parallel tasks with information beyond one context window. It suits tightly coupled work, such as much coding, less. (<a href="./orchestrating-more-than-one-agent.md">Lesson 2</a>)</details>
6. **What should a brief to a subagent contain?**
   <details><summary>Answer</summary>A goal, a scope, an output format, the sources to use, boundaries, and a stop rule. Vague briefs lead to duplicated or off-topic work. (<a href="./orchestrating-more-than-one-agent.md">Lesson 2</a>)</details>
7. **A workflow waits three days for an approval and the server restarts. What must already be true?**
   <details><summary>Answer</summary>State is saved to durable storage after each step, the wait has a timer, and the workflow can read its state back and continue. Each action is safe to repeat. (<a href="./making-a-workflow-durable-and-worth-owning.md">Lesson 3</a>)</details>
8. **Why do retries need idempotency keys?**
   <details><summary>Answer</summary>A retry or restart can run a step twice. A key makes the repeat return the same result instead of charging or sending twice. (<a href="./making-a-workflow-durable-and-worth-owning.md">Lesson 3</a>)</details>

## Sources

- Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
  (Jun 13, 2025): the 90.2% result, 4x and 15x token figures, where multi-agent fits and
  does not, vague delegation, resuming from errors, and rainbow deployments. Checked
  2026-09.
- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
  (Dec 2024): the five workflow patterns. Checked 2026-09.
- Cognition, "Don't Build Multi-Agents" (2025). Search-result excerpts only; the page could
  not be opened.
- The refund story is an invented illustration.

---

← Back to [module overview](./README.md)
