# What an agent is, and how much autonomy it needs

*Part of [AI agents for the product leader](./README.md)*

*Last reviewed: 2026-09 · Volatility: fast*

## TL;DR

An agent is a loop. It gathers context, decides the next action, takes it, and observes
the result. It repeats until the goal is met or a budget runs out. Nothing about that loop
needs a special product, protocol, or architecture. It is the shape underneath all of
them.

The first design decision comes before any build: how much autonomy does the task need?
"Agent or not" is the wrong question. Autonomy is a dial. At one end, your code decides
every step. At the other end, the model decides its own. More autonomy buys flexibility on
problems you cannot specify in advance. It costs predictability, speed, money, and the
ability to debug.

Anthropic draws the same line. A **workflow** runs a large language model (LLM) and tools along paths your code
defines. An **agent** lets the LLM direct its own process and tool use. Their advice is to
start with the simplest approach and add complexity only when it is needed.

> 🎯 **Production Bottom Line**
>
> "Agent" covers everything from a scripted pipeline with one model call to a system that
> plans its own steps. Place each proposal on the autonomy dial first. If you cannot, you
> cannot estimate its cost, its risk, or how it will fail. Start from a fixed workflow with
> model steps inside. It is cheaper, faster, and easier to debug. Get this wrong and you ship
> an expensive, unpredictable loop where a five-step pipeline would have worked. Or you sell a
> scripted workflow as an autonomous agent, and promise what the design cannot deliver.
> **Ask your team:** *"Could we draw this task as a flowchart? If yes, what are we paying an
> agent to rediscover on every request?"*

## The mental model: the loop, and the dial next to it

```mermaid
flowchart LR
  G["Goal"] --> GATHER["Gather context"]
  GATHER --> DECIDE["Decide the<br/>next action"]
  DECIDE --> ACT["Act"]
  ACT --> OBS["Observe the result"]
  OBS --> CHECK{"Goal met, or<br/>budget spent?"}
  CHECK -->|"no"| DECIDE
  CHECK -->|"yes"| DONE["Deliver"]
```

Every agent you will evaluate is this loop plus one setting: how much of each step your
code decides in advance, and how much the model decides. At one end, your code fixes every
step. The model only fills in language or judgment inside a step. That is cheap and
predictable. At the other end, the model picks its own steps from start to finish. That is
flexible, but harder to predict, price, and debug.

The full mechanics of the loop are in [What is an agent?](../agentic-ai/what-is-an-agent.md).

## Where a task belongs on the dial

Two questions place most tasks.

**Could an expert write down the procedure?** If yes, encode it. A fixed workflow calls
the model only where language or judgment is needed. It is cheaper and faster. Its
failures stay local and easy to trace.

**Do the steps depend on what is found along the way?** Debugging, open-ended research,
and negotiation work this way. A fixed pipeline either explodes into branches or breaks on
the first surprise. Here the loop earns its cost, because it chooses its next move from
what it just learned.

A third factor sits on top of both. Autonomy should shrink as stakes and irreversibility
rise, however well the task fits the agent shape.

## Worked example: an MSME loan-intake proposal

*An illustrative example with no real lender or data behind it.*

A lending team at a business lender proposes "an agent that handles small-business (MSME)
loan applications." You ask four questions.

1. **Can an expert write the steps?** Mostly. Check that the required documents are
   present. Run the eligibility rules, such as business age, sector, and loan size. Then send
   the file to underwriting, or ask the applicant for what is missing. Most applications
   follow this path. A **rules engine**, software that applies written business rules, already
   does the eligibility step well.
2. **What is unpredictable?** A minority of files are messy. The business name differs across
   documents. A bank statement shows large transfers nobody has explained. These need
   judgment.
3. **What are the stakes?** A request for a missing document is easy to correct. A credit
   decision is not. A wrong approval puts money at risk, and a wrong decline loses a good
   customer.
4. **Where does that put it on the dial?** The rules engine stays in charge of eligibility. A
   model step reads the documents, extracts the fields, and drafts the request for missing
   items. A credit officer approves every credit decision. An agent loop runs only on the
   messy files. Its job is to gather the evidence and write a discrepancy note for the
   officer, within a low step and cost limit.

The result is not "an agent." It is a workflow with one model step, one human gate, and one
small agent for the hard files. That design costs far less to run than an agent on every
application, and its failures are easy to locate.

## Tradeoffs and decisions

- **Flexibility vs. predictability.** More autonomy handles surprises. It also produces
  surprises of its own.
- **Cost and speed.** Anthropic notes that agentic systems often trade latency and cost
  for better task performance. Pay that price only where the task needs it.
- **Debuggability.** In a workflow, a failure points to one step. In an agent, a failure
  can sit anywhere in a chain of choices. Plan for tracing before you plan the model.
- **Stakes.** Turn the dial down as an action becomes harder to undo.

## Why the decision comes before the build

Once a team has built an agent, it wants to keep one. The orchestration is a sunk cost.
The demo impressed people. The story is "we built an agent for this."

That pull is why the question belongs at the start of scoping. A proposal that cannot say
why the model must choose its own steps is often a workflow wearing an agent's name. You
pay for flexibility the task never needed.

## Failure modes

- **Agent-washing.** A scripted workflow is called an "agent" because the label sells
  better. This mis-sets cost expectations and hides the real failure points.
- **Maximum autonomy by default.** A free-roaming agent is chosen because its demo looked
  good. A five-step pipeline would have done the job for a fraction of the cost.
- **Autonomy that ignores stakes.** The same open-ended design is used for a low-stakes
  draft and an irreversible production action.

## Under the hood

The difference between a workflow and an agent is who owns the control flow. Here is the
same task both ways, in outline.

```python
# Workflow: your code owns the control flow. Model calls sit inside fixed steps.
def handle_application(app):
    docs = fetch_documents(app.id)                    # plain code
    if not passes_eligibility_rules(app):             # the rules engine decides
        return route_to_officer(app, reason="rule check failed")
    fields = llm("Extract the fields.", context=docs) # one model step
    return send_to_underwriting(app, fields)

# Agent: the model owns the control flow. Your code owns the limits.
def run_agent(goal, tools, max_steps=8, max_cost=0.50):
    history, cost = [goal], 0.0
    for _ in range(max_steps):                        # a budget, not a hope
        step = llm_decide(history, tools)             # the model picks the next action
        cost += step.cost
        if step.is_final or cost > max_cost:
            return step.answer
        result = tools[step.tool](**step.args)        # act
        history.append((step, result))                # observe, then loop
    return escalate(goal, reason="step budget spent")
```

Three points matter to an engineer.

- **The limits live in your code.** The step cap and cost cap are not the model's choice.
- **Each result feeds the next decision.** That is why context grows, and why long runs get
  expensive. See [Context & memory](../agentic-ai/context-and-memory.md).
- **Tools are how an agent acts.** [Tool calling](../tool-calling/README.md) covers how a
  model requests a tool and how your code runs it.

**Two protocols you will hear named.** The **Model Context Protocol (MCP)** is an open
standard for connecting an AI application to tools and data. In December 2025 Anthropic
donated it to the Agentic AI Foundation, a directed fund under the Linux Foundation. The
**Agent2Agent protocol (A2A)** lets autonomous agents collaborate across platforms.
Google donated it to the Linux Foundation in June 2025. MCP connects an agent to tools. A2A
connects an agent to other agents. Neither changes the loop above. For the honest state of
each, read [multi-agent and protocols](../agentic-ai/multi-agent-and-protocols.md).

## Practitioner checklist

- [ ] Where does this proposal sit on the dial, from fixed workflow to full autonomy? Could
      one notch less do the job for less?
- [ ] Could an expert write down the task's steps? If yes, why is a model choosing them
      fresh on every request?
- [ ] Does autonomy shrink as an action's stakes or irreversibility rise?
- [ ] If the word "agent" were removed from the pitch, would the design still make sense?
- [ ] Are the step limit and cost limit set in code, not left to the model?

## Related lessons

- [Planning, reasoning & reliability across a run](./planning-reasoning-and-reliability-across-a-run.md)
  — what happens once the loop is running.
- [When not to build an agent](./when-not-to-build-an-agent.md) — the economics that often
  settle the autonomy question.
- [What is an agent?](../agentic-ai/what-is-an-agent.md) — the full mechanics and
  vocabulary behind this lesson.
- [Tool calling](../tool-calling/README.md) — how an agent acts.
- [Data and decisions](../business-acumen/data-and-decisions.md) — how to price a wrong
  approval against a wrong decline, with lending examples.

## Sources

- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
  (Dec 2024): the definitions of workflow and agent, and the advice to use the simplest
  solution first. Checked 2026-09.
- Anthropic, [Donating MCP to the Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
  (Dec 2025): the donation and MCP's description. Checked 2026-09.
- Google Cloud, [Agent2Agent protocol is getting an upgrade](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade)
  (2025): confirms the A2A donation to the Linux Foundation in June 2025. Checked 2026-09.
