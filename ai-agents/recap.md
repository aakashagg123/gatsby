# AI agents — recap & real-world examples

*Part of [AI agents for the product leader](./README.md)*

## Real-world examples & war stories

**A chatbot's invented refund policy, and who paid.** In November 2022 a customer asked Air
Canada's website chatbot about bereavement fares. The chatbot said the customer could claim the
discount after travel. The airline's policy did not allow that. In February 2024 the Civil
Resolution Tribunal of British Columbia (*Moffatt v. Air Canada*, 2024 BCCRT 149) rejected
the airline's suggestion that the chatbot was a separate entity. It held the company
responsible for the information on its website. It awarded CA$650.88 in damages, CA$812.02
in total with interest and fees. This was a small-claims decision.
🎯 *Takeaway:* if your agent says it, you said it. This is the case for
[risk tiers and approval gates](./running-an-agent-in-production.md) on any action or
statement that binds the company.

**Agent-washing, estimated.** In June 2025 Gartner predicted that over 40% of agentic AI
projects will be cancelled by the end of 2027, citing rising costs, unclear business value,
or weak risk controls. It also described "agent-washing": rebranding existing assistants,
robotic process automation, and chatbots as agents, and it estimated that only about 130 of
the thousands of vendors were real. 🎯 *Takeaway:*
[test the claim on your own cases](./choosing-and-acceptance-testing-an-agent.md) before you
sign, and place any pitch on
[the autonomy dial](./what-an-agent-is-and-how-much-autonomy-it-needs.md).

**Agents get better at short tasks first.** The research group Model Evaluation & Threat Research (METR) measures agents by how
long a task, in human time, they can finish with 50% success. In a March 2025 study, this
length had doubled about every seven months since 2019, measured on software tasks. METR has
reported a faster recent pace since. 🎯 *Takeaway:* progress is real, and success still falls
as tasks get longer.
[Judge reliability at the real task length](./planning-reasoning-and-reliability-across-a-run.md),
not on a three-step demo.

**Feedback beats cleverness.** Anthropic's guidance on building agents says an agent should
gain "ground truth" from the environment at each step, such as tool results or code
execution, and should have stopping conditions. 🎯 *Takeaway:* what an agent can see when it
is wrong predicts its reliability better than how sophisticated its reasoning is.

**The runaway loop (an illustration).** Picture an agent that files tickets, and a supplier
that changes an email format. A repeat cap stops the first loop within minutes, a per-agent
kill switch limits the damage, and the audit trail shows the cause. 🎯 *Takeaway:* controls
that live in code, tested before launch, are what turn an incident into a small one. See the
[hour-by-hour example](./running-an-agent-in-production.md).

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What an agent is, and how much autonomy it needs](./what-an-agent-is-and-how-much-autonomy-it-needs.md) | An agent is a loop. The real design choice is how much autonomy the task needs. | Could I draw this task as a flowchart? If so, why pay an agent to rediscover it? |
| [Planning, reasoning & reliability across a run](./planning-reasoning-and-reliability-across-a-run.md) | Small per-step error rates compound into large end-to-end failure. | What does the compounding maths predict at this task's real length? |
| [When not to build an agent](./when-not-to-build-an-agent.md) | An agent pays off only where work is cheap to check, survivable when wrong, and frequent. | What is the supervised cost, including catching its mistakes, against the old way? |
| [Running an agent in production](./running-an-agent-in-production.md) | Limits and gates live in code, matched to the risk of each action. | If it started misbehaving now, how fast could we stop it? |
| [Choosing and acceptance-testing an agent](./choosing-and-acceptance-testing-an-agent.md) | Agree the pass bar first, then test on your own cases, several times. | What pass rate, cost, and failure behaviour would we accept, in writing? |

**The through-line:** the loop behind an agent is simple. Almost everything that decides
whether it succeeds is a decision around the loop. How much autonomy does it get? How does
it notice its own mistakes? Was the task ever a good fit? What limits and gates surround it?
Was the claim tested before you paid? This module stays at that decision altitude and points
to [Agentic AI for the AI PM](../agentic-ai/README.md) for the mechanics.

> **Walk-away question:** *"For this agent proposal: have we placed it honestly on the
> autonomy dial, do we know the reliability at its real task length, does the supervised cost
> beat the old way, are the limits and gates enforced in code, and did it pass a test we
> wrote before we saw the results?"*

If yes, this is an agent worth running. If no, you know which lesson to reread.

## Test yourself

1. **What is the difference between a workflow and an agent?**
   <details><summary>Answer</summary>In a workflow your code defines the path, and the model works inside fixed steps. In an agent the model directs its own process and tool use. Autonomy is a dial between the two. (<a href="./what-an-agent-is-and-how-much-autonomy-it-needs.md">Lesson 1</a>)</details>
2. **A step succeeds 95% of the time. Roughly how often does a 20-step task succeed?**
   <details><summary>Answer</summary>About 36%, because per-step rates multiply (0.95 to the power of 20). At 99% per step the same task succeeds about 82% of the time. (<a href="./planning-reasoning-and-reliability-across-a-run.md">Lesson 2</a>)</details>
3. **What is the "supervised cost," and why does it matter more than the cost of one run?**
   <details><summary>Answer</summary>It is the cost of a run plus the cost of catching the runs that go wrong, compared with the old way. An agent that is cheap per run but needs full review can cost more than the old process. (<a href="./when-not-to-build-an-agent.md">Lesson 3</a>)</details>
4. **Name the three questions that decide whether a task suits an autonomous agent.**
   <details><summary>Answer</summary>Is the work cheap to check? Is a mistake reversible and low-cost? Does it happen often enough to repay the setup cost? (<a href="./when-not-to-build-an-agent.md">Lesson 3</a>)</details>
5. **Why should limits such as a cost cap live in code and not in the prompt?**
   <details><summary>Answer</summary>A prompt is a request. A confused or hijacked run can ignore it. Code enforces the limit whatever the model decides. (<a href="./running-an-agent-in-production.md">Lesson 4</a>)</details>
6. **What makes a kill switch real and not decorative?**
   <details><summary>Answer</summary>It is fast, checked every step, available at run, agent, and global scope, owned by a named person, and tested on a schedule. (<a href="./running-an-agent-in-production.md">Lesson 4</a>)</details>
7. **Why write the acceptance thresholds before you see the results, and run each case several times?**
   <details><summary>Answer</summary>Thresholds set after the results move to fit them. Agents are not deterministic, so one pass can be luck. Repeat runs show how often a case really passes. (<a href="./choosing-and-acceptance-testing-an-agent.md">Lesson 5</a>)</details>

## Sources

- *Moffatt v. Air Canada*, 2024 BCCRT 149, Civil Resolution Tribunal of British Columbia
  (decision of 14 Feb 2024): chat in Nov 2022, CA$650.88 damages, CA$812.02 in total. See
  [Choosing and acceptance-testing an agent](./choosing-and-acceptance-testing-an-agent.md#sources).
- Gartner press release, 25 Jun 2025: over 40% of agentic AI projects cancelled by end of
  2027, and the agent-washing estimate. See the same Sources list. Estimate, not measured.
- METR, Mar 2025: the seven-month doubling over 2019-2025. See
  [Planning, reasoning & reliability](./planning-reasoning-and-reliability-across-a-run.md#sources).
- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
  (Dec 2024): ground truth from the environment, and stopping conditions.

---

← Back to [module overview](./README.md)
