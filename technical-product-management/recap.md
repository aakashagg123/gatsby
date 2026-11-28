# Technical product management — recap & real-world examples

*Part of [Technical product management for the AI PM](./README.md)*

<!-- voice: human -->

This page pulls the module together. It starts with stories, two of them real and the rest
labelled illustrations, then a table with one idea and one question per lesson, and it ends with a
self-test you can use to check what stuck.

## Real-world examples & war stories

**The quarter spent proving the obvious (an illustration).** A team skips
[discovery](./discovery-to-delivery.md) because "the CEO already knows customers want this". It
builds for three months and launches to single-digit adoption, a result that a week of prototype
tests would probably have predicted. The delivery track is the most expensive place to learn that
an idea is wrong, and discovery exists to make being wrong cheap.

**The spec with no non-goals (an illustration).** A one-pager collects fourteen "small additions"
between kickoff and code freeze, because [nothing was ever declared out of
scope](./specs-prds-and-rfcs.md). The feature ships a quarter late, doing ten things adequately
instead of three things well. Every scope fight a non-goal prevents is time you get back.

**The haggled estimate (an illustration).** A PM talks a "six weeks" down to four in planning. The
team ships in six anyway, minus tests and plus a production incident, and every estimate after that
arrives [quietly padded](./working-with-engineering.md). Negotiate the scope and leave the number
alone, because the number is data.

**Knight Capital's 45 minutes (real, 2012).** The US Securities and Exchange Commission's order
describes a firm that deployed new trading code to seven of its eight order-routing servers, with
no second technician checking the deployment. The new code reused a flag that once switched on an
old function, and that old code was still on the eighth server. During the response, staff
uninstalled the new code from the seven correct servers, which spread the problem to them. In
about 45 minutes Knight lost more than $460 million. Deploy discipline, [flag hygiene and a
rehearsed rollback](./launches-rollouts-and-migrations.md) are what stand between an incident and
a company-ending event.

**Three bugs that the evals missed (real, 2025).** In September 2025, Anthropic published a
postmortem on three infrastructure bugs that intermittently degraded Claude's responses between
August and early September. Its evaluations didn't capture what users were reporting, and its
privacy controls limited how engineers could inspect the conversations. Its response included more
sensitive evaluations and continuous quality evaluations on production systems. A passing offline
suite isn't a [quality detector](./incidents-and-postmortems.md), so production sampling has to be
budgeted.

**The A/B test that always won (an illustration).** A growth team celebrates dozens of significant
wins while the annual retention number stays flat. The causes are [peeking, after-the-fact
hypotheses and segment fishing](./metrics-and-experimentation.md). The point of experimentation is
to be hard to fool, and a testing culture that never loses isn't really testing.

**The silent model upgrade (an illustration).** A provider ships a new model version, and the team
swaps it in as a config change with no [eval diff and no staged ramp](./tpm-for-ai-products.md).
Average quality rises, but a template the biggest customer relies on breaks, and the first detector
is an angry email. A model change is a migration that looks like a config change, so score it,
shadow it, ramp it, and keep the old version one re-pin away.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [The technical PM role](./the-technical-pm-role.md) | Own outcomes, and influence without authority | Which decisions are mine, which do I frame, and which aren't mine? |
| [Discovery to delivery](./discovery-to-delivery.md) | Kill ideas cheaply, and build the survivors | What's my evidence that it's valuable, usable, feasible and viable? |
| [Specs, PRDs & RFCs](./specs-prds-and-rfcs.md) | Write the what, and read the how | Could the team decide "done" without asking me? |
| [Prioritization & roadmaps](./prioritization-and-roadmaps.md) | The order is the strategy, and roadmaps are bets | What does this yes displace? |
| [Working with engineering](./working-with-engineering.md) | Rituals carry intent, and trust carries the truth | Am I changing the scope or corrupting the estimate? |
| [Metrics & experimentation](./metrics-and-experimentation.md) | If you can't measure it, you shipped an opinion | Which event proves this worked, and what guards the downside? |
| [Launches, rollouts & migrations](./launches-rollouts-and-migrations.md) | Ship gradually, and finish the migration | What one action restores yesterday? |
| [Incidents & postmortems](./incidents-and-postmortems.md) | Mitigate first, then learn without blame | Who decides, and what do users see, if this breaks at 2 a.m.? |
| [TPM for AI](./tpm-for-ai-products.md) | Evals are the spec, and the flywheel is the moat | Can we tell, with evidence, whether a change helps? |

**The through-line.** Technical product management is a loop rather than a lane. You discover
cheaply, specify clearly, prioritise honestly, build together, measure carefully, release
gradually, handle failure in the open, and feed what production teaches you into the next turn.
AI products don't change the loop, but they raise its stakes. A probabilistic product without
evals, feedback capture and disciplined releases is a demo with traffic, and the craft in this
module is what turns it into a business.

> **Walk-away question:** *"For my current initiative, can I trace the loop end to end, from the
> evidence it's worth building, through the spec that defines done, the metric that will judge it
> and the rollout that protects it, to the feedback that improves it? Which link would snap first?"*

---

← Back to [module overview](./README.md)

## Test yourself

Ten questions, at least one per lesson. The answers fold out, and each links back to its lesson.

1. **Your engineering lead asks you to choose between two search architectures. What's your part of that decision?**
   <details><summary>Answer</summary>The architecture is engineering's call, but the latency budget and the cost you can accept are yours. Frame the tradeoff in product terms, such as what three seconds does to frequent searchers and what the faster option costs at your volume, and the engineering choice usually follows. (<a href="./the-technical-pm-role.md">The technical PM role</a>)</details>
2. **A VP loves an AI feature idea and wants it built next quarter. What has to happen before it enters delivery?**
   <details><summary>Answer</summary>A feasibility spike against real inputs, with a quality bar agreed in advance, plus evidence on value, usability and viability. An executive's enthusiasm is an input to weigh, not validation. (<a href="./discovery-to-delivery.md">Discovery to delivery</a>)</details>
3. **Your PRD says the summariser must be "accurate". How do you rewrite it so an engineer can test it?**
   <details><summary>Answer</summary>Set a bar on a graded eval set, such as at least 90% acceptable on 200 cases with zero harmful, plus behavioural bounds and latency and cost budgets. Then "can we ship?" becomes a score. (<a href="./specs-prds-and-rfcs.md">Specs, PRDs & RFCs</a>)</details>
4. **An AI bet tops your RICE list at 50% confidence. What do you do before committing the quarter to it?**
   <details><summary>Answer</summary>Run a short spike. It usually changes the effective reach and the effort as well as the confidence, and it can move the item down the list, as the worked example shows. (<a href="./prioritization-and-roadmaps.md">Prioritization & roadmaps</a>)</details>
5. **Sales needs in six weeks what the team estimated at ten. What's the right next question?**
   <details><summary>Answer</summary>"What's the expensive part?" Then cut scope, for example by making a costly edge case a non-goal, and recompute against the team's velocity range. Haggling the number only gets you padded estimates later. (<a href="./working-with-engineering.md">Working with engineering</a>)</details>
6. **Your test was configured 50/50, and the arms came out 4,100 and 3,700. Do you read the result?**
   <details><summary>Answer</summary>No. That's a sample ratio mismatch, with a chi-square p-value far below 0.0005. Find out why users went missing from one arm before you trust anything the test says. (<a href="./metrics-and-experimentation.md">Metrics & experimentation</a>)</details>
7. **Why ship a new AI feature to 1% before everyone, if the offline evals pass?**
   <details><summary>Answer</summary>Because some failures only show on real inputs, at real volume. A canary caps how many users see a hidden bug while your abort criteria do their work, and it lets you rehearse the rollback. (<a href="./launches-rollouts-and-migrations.md">Launches, rollouts & migrations</a>)</details>
8. **During a top-severity incident, what comes first, root cause or rollback?**
   <details><summary>Answer</summary>Rollback, meaning mitigation. Users pay for every minute of diagnosis, so restore service first and find the causes, plural, in the postmortem. (<a href="./incidents-and-postmortems.md">Incidents & postmortems</a>)</details>
9. **What turns a postmortem from a ritual into learning?**
   <details><summary>Answer</summary>Blamelessness, so it hears the truth, plus action items with owners and dates, tracked like features, with escalation when a repeat incident finds one unshipped. (<a href="./incidents-and-postmortems.md">Incidents & postmortems</a>)</details>
10. **A replacement model scores 93% against your current model's 90%. Is it safe to switch?**
    <details><summary>Answer</summary>Not yet. Check the slices, because a higher total can hide a regression on the cases that matter most. Then run it as a migration, with a shadow run and a staged ramp, and start early enough to finish before the old model retires. (<a href="./tpm-for-ai-products.md">Technical product management for AI</a>)</details>

## Sources

- US Securities and Exchange Commission, [*In the Matter of Knight Capital Americas LLC*, Release
  No. 34-70694](https://www.sec.gov/litigation/admin/2013/34-70694.pdf), 16 October 2013 (as of
  2026-11).
- Anthropic, [*A postmortem of three recent
  issues*](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues), 17 September
  2025 (as of 2026-11).
- Aleksander Fabijan and colleagues, [*Diagnosing Sample Ratio Mismatch in A/B
  Testing*](https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/),
  Microsoft Research, 14 September 2020 (the p below 0.0005 threshold in question 6) (as of
  2026-11).
