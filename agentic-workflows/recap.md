# Agentic workflows — recap & real-world examples

*Part of [Agentic workflows for the product leader](./README.md)*

## Real-world examples & war stories

**Coding agents built as orchestrator-subagent systems.** Serious production coding
agents increasingly delegate messy, token-heavy subtasks — grepping a large codebase,
running a long test suite — to subagents with their own context window, keeping the lead
agent's context clean for the actual decision-making. 🎯 *Takeaway:*
[context isolation, not just parallelism](./orchestrating-more-than-one-agent.md), is
often the real reason a multi-agent split earns its coordination cost.

**Loan origination and KYC workflows that run for days, not seconds.** Regulated
financial workflows — a loan application awaiting a document, a KYC check awaiting a
manual review — routinely pause for hours or days waiting on a human or an external
system, then resume exactly where they paused. Production process engines exist
specifically because this kind of workflow cannot be modeled as one continuous call. 🎯
*Takeaway:* [durability is the precondition](./making-a-workflow-durable-and-worth-owning.md)
for any workflow that has to survive real-world waiting, not an edge case to patch in
later.

**"Overfunded BPO" concerns in early service-as-a-software startups.** As AI services
marketed as fully autonomous proliferated, a recurring pattern surfaced in due diligence:
some of them were, on inspection, staffed heavily by humans quietly completing the work
behind the interface, with the promised absorption into software never actually
happening. 🎯 *Takeaway:*
[the honest fraction of the workflow still done by a human](./making-a-workflow-durable-and-worth-owning.md),
not the marketed autonomy claim, is what reveals whether a captured workflow is real.

**Multi-agent systems that quietly cost more than the single agent they replaced.**
A recurring pattern as multi-agent frameworks proliferated: teams split a task across
several agents because the architecture diagram looked more sophisticated, then found
token spend, latency, and debugging effort all increased without a corresponding quality
gain. 🎯 *Takeaway:*
[every additional agent needs a named bottleneck](./orchestrating-more-than-one-agent.md)
it's solving — parallelism, context isolation, or specialization — or it's adding cost
without adding capability.

**Point-solution AI tools displaced by whole-workflow competitors.** Across several
categories, a narrow tool that automated a single step of a workflow well lost ground to
a competitor that captured the entire workflow end to end, because the second removed a
seam the first one's users still had to stitch together by hand. 🎯 *Takeaway:*
[owning the whole workflow](./making-a-workflow-durable-and-worth-owning.md) is
frequently the more defensible position than doing one step of it exceptionally well.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [Orchestrating more than one agent](./orchestrating-more-than-one-agent.md) | Every additional agent needs a named bottleneck — context, parallelism, or specialization — or it's just added cost | Would one agent with better tools and cleaner context do this — and have we actually tried? |
| [Making a workflow durable, and worth owning](./making-a-workflow-durable-and-worth-owning.md) | Durability is the precondition for trust; owning the whole workflow is the strategic payoff once it's earned | If the system restarted mid-workflow, would every instance resume exactly where it left off — and do we own the whole workflow, or just one step of it? |

**The through-line:** the word "workflow" adds two things a single agent run doesn't
have to worry about — coordinating more than one loop, and surviving the real time a
long-running process actually takes. This module deliberately stayed at that decision
altitude rather than re-deriving the mechanics already developed in full depth in
[Multi-agent systems & protocols](../agentic-ai/multi-agent-and-protocols.md),
[Flowable](../flowable/README.md), and
[Agentic AI as a product](../agentic-ai/agentic-ai-as-a-product.md), because the
mistakes that actually sink agentic workflow initiatives are rarely about the orchestration
pattern chosen. They're a durability gap discovered on the first real restart, or a
roadmap aimed at one step of a workflow a competitor was willing to own end to end.

> **Walk-away question:** *"For this workflow: does every additional agent in it earn its
> coordination cost, would it survive a restart mid-run without losing its place, and are
> we aiming to own the whole thing or just automate one step of it?"*

If yes, this is a workflow worth building. If no, you now know exactly which lesson in
this module to reread — and where the deeper engineering and strategy live, one module
away in [Multi-agent systems & protocols](../agentic-ai/multi-agent-and-protocols.md) and
[Flowable](../flowable/README.md).
