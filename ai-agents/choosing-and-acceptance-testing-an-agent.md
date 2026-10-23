# Choosing and acceptance-testing an agent

*Part of [AI agents for the product leader](./README.md)*

*Last reviewed: 2026-09 · Volatility: fast*

## TL;DR

Sooner or later you will be asked to buy an agent, or to sign off on one your team built.
Two problems make this hard. The label "agent" is used loosely, so a product may not be what
it says. And a demo cannot show how the agent behaves across many real cases.

This lesson gives you two tools. The first is a short **due-diligence checklist** that
separates a real agent from a rebranded one and surfaces the questions a vendor would
rather skip. The second is an **acceptance test**: a fixed set of real cases, run many
times, scored on outcome, path, and cost, against thresholds you agree before you sign.

You own the result either way. As reported in legal commentary, a Canadian tribunal held an
airline liable in February 2024 for wrong information its chatbot gave a customer. The
airline had argued, in effect, that the chatbot was a separate legal entity. The tribunal
rejected that. It was a small-claims tribunal, but the point holds: if your agent says it,
you said it.

> 🎯 **Production Bottom Line**
>
> A demo shows the cases the vendor chose. Your risk sits in the cases it did not show: high
> cost per run, weak controls, and failures on your real inputs. Most of these can be seen
> before purchase, if you test for them. Sign only against a written acceptance test, run on
> your own cases, not the vendor's demo cases. Without one, you buy a demo. It works on the
> happy path and fails on your real inputs, and the contract has no measure of "works," so you
> have no remedy. **Ask your team:** *"If we ran this agent on 200
> of our own past cases tomorrow, what pass rate, cost, and failure behaviour would we accept,
> and have we written that down?"*

## The mental model: claim, test, threshold

```mermaid
flowchart LR
  CLAIM["Vendor or team claim"] --> Q["Due-diligence questions"]
  Q --> CASES["Your real cases<br/>+ hostile cases"]
  CASES --> RUN["Run each case<br/>several times"]
  RUN --> SCORE["Score outcome,<br/>path, cost"]
  SCORE --> GATE{"Meets the agreed<br/>thresholds?"}
  GATE -->|"yes"| SIGN["Sign and launch<br/>in stages"]
  GATE -->|"no"| REJECT["Fix, renegotiate,<br/>or walk away"]
```

The thresholds come first. Agree them before you see results. Otherwise the results set the
bar, and the bar moves to meet them.

## Due diligence: is it really an agent, and can you rely on it?

**Agent-washing** means selling an existing product, such as a chatbot, a scripted
workflow, or robotic process automation, under the "agent" label without real agentic
capability. Treat the label as a claim to check.

Ask these questions. A good answer is specific and shows evidence.

1. **Where does it sit on the autonomy dial?** Ask which steps the model chooses and which
   your code fixes. See [What an agent is](./what-an-agent-is-and-how-much-autonomy-it-needs.md).
2. **What is the per-step and end-to-end success rate, on what tasks, measured how?** Ask for
   the task length. A three-step rate says little about a thirty-step task.
3. **What does a run cost, at the 90th percentile and not only the average?**
4. **What are the limits?** Ask for step, time, cost, and repeat caps, and where they are
   enforced. See [Running an agent in production](./running-an-agent-in-production.md).
5. **Which actions need a human, and who decides that?**
6. **What happens when a tool fails or returns nothing?** Ask them to show it.
7. **Can we see a full trace of a run, and export it?**
8. **How is it updated, and how do we know when behaviour changes?** Model updates can change
   behaviour without a code change.
9. **Which of our data does it see, where does it go, and what is retained?** If the vendor
   serves other lenders on the same platform, ask how it keeps your files apart from theirs.
10. **What is the exit path?** Ask how you get your data, traces, and configuration out.

Two answers should worry you. One is "it just works" with no numbers. The other is a demo
on cases the vendor chose.

## Acceptance testing: design the test before the deal

An acceptance test is a fixed, written procedure with pass thresholds. Build it in four
parts.

**1. The case set.** Collect 100 to 300 real past cases. Include the routine ones, the
messy ones, and the ones your people find hard. Add hostile cases: inputs that try to
redirect the agent, and inputs that are missing or contradictory. Keep a hidden slice the
vendor never sees.

**2. Repeat runs.** Agents are not deterministic. Run each case several times, at least
five. A case that passes three times out of five is a finding, not a pass.

**3. Three scores.** Score every run on:
- **Outcome.** Did it reach the right result? Use exact checks where you can, and a
  rubric plus a human spot-check where you cannot.
- **Path.** Did it take a sensible route? Check steps used, tools called, and whether it
  stayed within its limits. A right answer reached by a risky path is a failure.
- **Cost.** Tokens, tool spend, and time per run.

**4. Thresholds and stop behaviour.** Write the pass bar in advance. Include behaviour under
failure: it must stop at its caps, escalate when unsure, and never invent a result after a
tool error.

## Worked example: an acceptance test for a claim

*An illustrative example. The vendor, numbers, and thresholds are assumed.*

A vendor claims: "Our agent completes document verification on 90% of small-business loan
files without a human."

You turn the claim into a test.

| Measure | How you test it | Agreed threshold |
| --- | --- | --- |
| Outcome on routine cases | 150 past loan files, 5 runs each, exact match on the verification outcome your officers recorded | At least 90% of cases pass on at least 4 of 5 runs |
| Outcome on hard cases | 50 files your credit officers marked difficult | At least 60%, and the rest escalate, not guess |
| Hostile inputs | 20 files with instructions hidden in uploaded documents, missing data, or requests for another tenant's records | 0 unsafe actions. 0 reads of another tenant's data. At least 95% escalate or refuse correctly |
| Path | Trace review of 40 runs | 0 runs exceed step or cost caps. 0 tool calls outside the allowed set |
| Cost | Cost per run across all runs | Median under the agreed figure. 90th percentile under twice the median |
| Failure behaviour | Force 10 tool failures | 100% stop, retry once, or escalate. 0 invented results |

Suppose results come back. Routine cases: 82% pass on at least 4 of 5 runs. Hard cases: 41%,
with 30% invented answers. The vendor's 90% claim held only on their chosen demo set. The
test found this before the contract, and the numbers give you a basis to renegotiate,
narrow the scope, or walk away.

## Tradeoffs and decisions

- **Test size vs. cost.** More cases and more runs give firmer numbers and cost more. Start
  with 100 cases and five runs, and grow where results are close to the threshold.
- **Automated vs. human scoring.** Automated scoring is cheap and can miss subtle errors.
  Spot-check a sample by hand.
- **Vendor's data vs. yours.** A vendor's benchmark shows what they optimised. Your cases
  show what you need.
- **Contract flexibility vs. safety.** Tie payment or scope to the acceptance result, and
  keep the right to re-test after model updates.

## Failure modes

- **Testing the demo.** The acceptance set is the vendor's showcase cases.
- **A moving bar.** Thresholds are set after seeing results, so they match what the agent
  already does.
- **One run per case.** A lucky pass counts as a pass.
- **Outcome-only scoring.** The agent reaches right answers by risky or costly paths, and
  nobody looks at the trace.
- **Test once, trust forever.** A model update changes behaviour, and no one re-runs the
  test.
- **Agent-washed purchase.** You buy a chatbot with an agent label, and pay agent prices.

## Under the hood

An acceptance harness is a loop over cases and runs that records outcome, path, and cost.

```python
import statistics

def acceptance(cases, agent, runs=5):
    report = []
    for case in cases:
        results = []
        for _ in range(runs):
            trace = agent.run(case.input, limits=case.limits)     # full trace, not just the answer
            results.append({
                "outcome": case.check(trace.answer),               # exact check or rubric
                "path_ok": trace.steps <= case.limits.max_steps
                           and set(trace.tools) <= case.allowed_tools,
                "stopped_correctly": trace.stopped_reason in case.allowed_stops,
                "cost": trace.cost,
            })
        report.append({"case": case.id, "results": results})
    return report

def summarise(report, bar):
    passed = sum(1 for r in report
                 if sum(x["outcome"] and x["path_ok"] for x in r["results"]) >= bar.min_runs_passing)
    costs = [x["cost"] for r in report for x in r["results"]]
    return {
        "case_pass_rate": passed / len(report),
        "median_cost": statistics.median(costs),
        "p90_cost": statistics.quantiles(costs, n=10)[-1],
    }
```

Store every trace. When a model update lands, run the same harness again and compare
against the last accepted report. Treat any drop as a regression until proven otherwise.
[Prompts in production](../prompt-engineering/prompts-in-production.md) shows the same habit
applied to prompts. [Reliability & evals](../agentic-ai/reliability-and-evals.md) covers
trajectory grading in depth.

## Practitioner checklist

- [ ] Have we placed the product on the autonomy dial, and does the vendor's claim match?
- [ ] Are our acceptance thresholds written down before we see any results?
- [ ] Does the case set use our real cases, hard cases, hostile cases, and a hidden slice?
- [ ] Is each case run several times, and scored on outcome, path, and cost?
- [ ] Do we test failure behaviour: tool errors, caps, and escalation?
- [ ] Is the acceptance result tied to the contract, with the right to re-test after
      model updates?
- [ ] Do we know the exit path for our data and traces?

## Related lessons

- [When not to build an agent](./when-not-to-build-an-agent.md) — the economics to check
  before you test.
- [Running an agent in production](./running-an-agent-in-production.md) — the controls the
  acceptance test should verify.
- [Reliability & evals](../agentic-ai/reliability-and-evals.md) — grading trajectories in
  depth.
- [Agentic AI as a product](../agentic-ai/agentic-ai-as-a-product.md) — agent UX, unit
  economics, and business models.
- [Multi-tenant isolation](../content/05-safety-multitenancy/multi-tenant-isolation.md) — how
  a shared platform keeps one customer's data from another's.

## Sources

- Law360 Canada, [Air Canada chatbot decision commentary](https://www.law360.ca/ca/articles/1815402)
  (2024): the decision date of 14 February 2024, the citation *Moffatt v. Air Canada*, 2024
  BCCRT 149, and the British Columbia Civil Resolution Tribunal as the equivalent of a
  small-claims court. Checked 2026-10.
- Kirsten Thompson, Dentons Canada, via Mondaq, [Airline ordered to compensate a B.C. man because its chatbot provided inaccurate information](https://www.mondaq.com/canada/new-technology/1427926/airline-ordered-to-compensate-a-bc-man-because-its-chatbot-provided-inaccurate-information)
  (23 Feb 2024): the chatbot's wrong statement on bereavement fares, the "separate legal
  entity" argument and its rejection, and the award as reported. Checked 2026-10.
- The decision text itself was not opened. The tribunal's own pages could not be reached
  from our build environment, so these facts rest on the legal commentary above.
- The vendor claim, the test table, the results, and the code are invented and
  illustrative.
