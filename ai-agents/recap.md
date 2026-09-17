# AI agents — recap & real-world examples

*Part of [AI agents for the product leader](./README.md)*

## Real-world examples & war stories

**Coding agents beating open-ended writing agents to reliability.** Across the industry,
agents that work inside a codebase — where a failing test gives immediate, unambiguous
feedback — improved faster and became trustworthy sooner than agents built for open-ended
writing or research tasks, where "did this work?" has no clean answer. 🎯 *Takeaway:*
[the environment's feedback quality](./planning-reasoning-and-reliability-across-a-run.md)
predicts an agent's reliability better than the sophistication of its reasoning does.

**A customer-service chatbot bound by a hallucinated policy.** A well-known incident saw
an airline's support chatbot invent a refund policy that didn't exist; a tribunal later
held the company to the promise the bot had made up. 🎯 *Takeaway:* this is exactly what
[an unverifiable, high-stakes action with no human gate](./when-not-to-build-an-agent.md)
looks like in production — the fix isn't a smarter model, it's not letting an
unsupervised agent make binding, irreversible commitments in the first place.

**"Agent-washing" in vendor pitches.** As agent hype grew, a recurring pattern of
enterprise complaints emerged: products marketed as autonomous "agents" turned out, on
inspection, to be fixed scripted workflows with a single model call inside them — or the
reverse, genuinely open-ended systems marketed as predictable, scoped assistants. 🎯
*Takeaway:* [placing a proposal honestly on the autonomy spectrum](./what-an-agent-is-and-how-much-autonomy-it-needs.md)
before signing off on it catches a mismatch between what was promised and what was built.

**Early coding-agent benchmarks that looked strong on short tasks and collapsed on long
ones.** As agent benchmarks matured, a consistent pattern appeared: success rates that
looked respectable on short, few-step tasks fell sharply as task length grew — the
signature of compounding per-step error rather than any single dramatic failure. 🎯
*Takeaway:* [demo-horizon thinking](./planning-reasoning-and-reliability-across-a-run.md)
— judging a three-step demo as if it predicts thirty-step production performance — is one
of the most consistent ways teams overestimate what an agent will do in the real world.

**"Overfunded BPO" concerns in early agent startups.** As service-as-a-software pitches
proliferated, a recurring skeptical pattern emerged in due diligence: some AI services
marketed as autonomous were, on closer inspection, staffed heavily by humans quietly doing
the work behind the interface. 🎯 *Takeaway:*
[the honest supervised cost](./when-not-to-build-an-agent.md), not the marketed autonomy
level, is the number that reveals whether an agent economy is real or subsidized.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What an agent is, and how much autonomy it needs](./what-an-agent-is-and-how-much-autonomy-it-needs.md) | An agent is a loop; the real design decision is how much autonomy the task needs | Could I draw this task as a flowchart — and if so, why pay for an agent to rediscover it? |
| [Planning, reasoning & reliability across a run](./planning-reasoning-and-reliability-across-a-run.md) | Small per-step error rates compound into large end-to-end failure over long runs | What does the compounding math predict for this task's typical length, given our real per-step success rate? |
| [When not to build an agent](./when-not-to-build-an-agent.md) | An agent only pays off where work is verifiable, low-stakes-if-wrong, and frequent enough | What's the supervised cost — including catching its mistakes — against the honest cost of the old way? |

**The through-line:** the loop behind an agent is simple; almost everything that
determines whether it succeeds is a decision made around it — how much autonomy it's
given, how well it's set up to notice its own mistakes, and whether the task was ever a
good economic fit for a loop in the first place. This module deliberately stayed at that
decision altitude rather than re-deriving the mechanics already developed in full depth in
[Agentic AI for the AI PM](../agentic-ai/README.md), and rather than repeating what
[Tool calling](../tool-calling/README.md) and [Memory & context](../memory-and-context/README.md)
already cover in this same family, because the mistakes that actually sink agent
initiatives are rarely mechanical. They're a scope call made by demo appeal instead of
economics, or a reliability bar set by a three-step test instead of the real thirty-step
task.

> **Walk-away question:** *"For this agent proposal: have we placed it honestly on the
> autonomy spectrum, do we know what our real per-step reliability implies at its actual
> task length, and does the honest supervised cost beat what we're already doing today?"*

If yes, this is an agent worth building. If no, you now know exactly which lesson in this
module to reread — and where the deeper engineering lives, one module away in
[Agentic AI for the AI PM](../agentic-ai/README.md).
