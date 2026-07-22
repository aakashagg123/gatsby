# The Ten Principles of Process Automation

The conceptual spine of the Flowable track. Every lesson's Concept beat links back to
one of these. Read this first; it is the whole course at PM/architect altitude — the
phases then make you build each idea.

---

## 1. A process is a graph; execution is tokens moving through it

Strip away the notation and a BPMN model is a directed graph: nodes (events, tasks,
gateways) connected by sequence flows. Executing a process means placing a **token** on
the start event and advancing it along the edges until every token reaches an end event.
Parallel branches are multiple tokens; joining is waiting for tokens to merge.

If you can predict where the tokens are, you can predict everything the engine does.
That is why Phase 1 makes you build the token model before touching Flowable.

## 2. The diagram is the code

The BPMN XML you deploy *is* the executable artifact — not documentation of it. This is
the core bet of BPM engines: business stakeholders, product managers, and engineers
stare at the same picture, and the picture is what runs. When the diagram and the
behaviour can't drift apart, an entire class of "the spec says X but the code does Y"
disputes disappears — and your audit conversation becomes "here is the model, here is
every instance's path through it."

The cost: you must model honestly. A diagram that hides the real logic in code
underneath it is worse than no diagram.

## 3. The engine is a state machine with a database

A process engine's superpower is not running things — it is **stopping**. A loan
application waits three days for a document; a token sits at a user task for a week.
The engine persists the token's position and variables to relational tables, releases
every thread, and survives restarts, deploys, and crashes. Execution resumes exactly
where it stopped, possibly on another node.

Everything else — clustering, failover, audit — falls out of this one design decision:
**state lives in the database, not in memory**.

## 4. Wait states define transaction boundaries

The engine advances tokens synchronously until it hits a **wait state** (user task,
timer, message catch, async continuation) — then it commits. Everything between two
wait states is one ACID transaction: if a service task throws, the token rolls back to
the previous wait state, not to some arbitrary midpoint.

This is the single most misunderstood behaviour in BPM engines. When you know where the
transaction boundaries are, incidents stop being mysterious; when you don't, "the
process re-executed my payment call" becomes a production war story. Phase 2 is entirely
about this.

## 5. Time is a first-class citizen

"Remind the customer in 3 days", "expire the offer after 30 days", "escalate if not
approved within 4 hours" — in ordinary code these become cron jobs, scheduler tables,
and drift. In a process engine they are **timer events**: declared in the model, stored
as jobs, fired by the job executor, visible in the diagram, and versioned with the
process.

If your domain has deadlines, SLAs, or expiries, this is usually the feature that pays
for the engine.

## 6. Separate the flow from the work

The process model orchestrates; it should not *implement*. Service tasks delegate to
your domain services; user tasks delegate to humans; decision tasks delegate to DMN
tables. The engine owns sequencing, state, retries, and time — your code owns business
logic. When a model starts accumulating scripts and inline expressions full of domain
rules, the boundary has leaked, and you now have logic that is neither testable like
code nor readable like a diagram.

## 7. Decisions are not processes — give rules their own home

"Which applications need manual review?" is not a flow; it is a **decision**. Model it
as a DMN decision table: rows the business can read, hit policies that make conflicts
explicit, and changes that don't require redeploying the process. The process asks the
question; the table answers it. Mixing rule logic into gateway conditions scatters your
policy across the diagram where nobody can review it as a whole.

## 8. Not all work is a flowchart — but most of yours is

CMMN exists for genuinely unstructured work: a fraud investigation where the case
worker decides what happens next from a set of available activities. It is powerful and
rarely needed. Most "our process is too dynamic for BPMN" claims dissolve into a BPMN
model with a few event subprocesses. Reach for CMMN only after BPMN has actually
failed you — and be suspicious of anyone who starts with it.

## 9. Long-running instances outlive their definitions

A mortgage process runs for months; you will deploy new versions while thousands of
instances are mid-flight. Engines default to the safe answer — running instances keep
their old definition; new starts get the new one — and offer migration tooling for when
old instances must move. Every model change must be made with the question: *what
happens to the tokens currently inside?* This is the process-engine equivalent of a
database migration, and it deserves the same discipline.

## 10. The engine is infrastructure — treat the decision like one

Adopting a process engine is an architecture decision, not a library import. The honest
checklist:

- **Use an engine** when you have long-running, stateful, auditable flows with humans,
  timers, and multiple systems involved — loan origination, KYC, claims, onboarding.
- **Use a state column and a queue** when the flow is short, fully automated, and
  changes rarely — an engine would be ceremony.
- **Use a durable-execution runtime** (Temporal and friends) when the audience is
  purely engineers, flows are code-first, and nobody needs the diagram.

Flowable's particular position: open-source, embeddable in your JVM process or
standalone over REST, all three engines (BPMN/CMMN/DMN) in one platform, with a
commercial layer (Flowable Work) above it. Phase 10 turns this principle into concrete
decision guides.

## Connects to other tracks

- [The method: deconstruct, challenge, reconstruct](../../first-principles/the-method.md) — decomposing a process into tokens and wait states is first-principles thinking applied.
- [Multi-agent systems & protocols](../../agentic-ai/multi-agent-and-protocols.md) — orchestration by a shared engine vs. by autonomous agents that coordinate.

---

*Next: build principle 1 with your own hands —
[Tokens & sequence flow](../phases/01-bpmn-and-the-token-model/01-tokens-and-sequence-flow/docs/en.md).*
