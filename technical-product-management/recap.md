# Technical product management — recap & real-world examples

*Part of [Technical product management for the AI PM](./README.md)*

## Real-world examples & war stories

**The quarter spent proving the obvious.** A team skips [discovery](./discovery-to-delivery.md)
because "the CEO already knows customers want this," builds for three months, and launches to
single-digit adoption — a result five prototype tests would have predicted for the cost of a
week. 🎯 *Takeaway:* the delivery track is the most expensive possible place to learn an idea
is wrong; discovery exists to make being wrong cheap.

**The spec with no non-goals.** A one-pager grows fourteen "small additions" between kickoff
and code freeze because [nothing was ever declared out of scope](./specs-prds-and-rfcs.md).
The feature ships a quarter late, doing ten things adequately instead of three things well.
🎯 *Takeaway:* non-goals are the highest-leverage sentences in a PRD — every scope fight you
don't have is a week you get back.

**The haggled estimate.** A PM talks a "six weeks" down to four in planning; the team ships
in six anyway, minus tests, plus a production incident. Every estimate thereafter arrives
[quietly pre-padded](./working-with-engineering.md). 🎯 *Takeaway:* negotiate scope, never
the number — the number is data, and haggling it just corrupts your instruments.

**Knight Capital's 45 minutes (2012).** A trading firm deploys new code to only seven of
eight servers; a repurposed feature flag activates dead code on the eighth, and with
[no rehearsed rollback](./launches-rollouts-and-migrations.md) the firm loses ~$440 million
in 45 minutes — more than its market cap. 🎯 *Takeaway:* deploy/release discipline, flag
hygiene, and a rehearsed rollback aren't process overhead; they're the difference between an
incident and an obituary.

**The A/B test that always won.** A growth team celebrates dozens of "significant" wins;
the annual retention number doesn't move. The culprits: [peeking, post-hoc hypotheses, and
segment fishing](./metrics-and-experimentation.md). 🎯 *Takeaway:* the point of
experimentation is to be *hard to fool* — a testing culture that never loses isn't testing.

**The silent model upgrade.** A provider ships a new model version; the team swaps it in as
a config change — no [eval diff, no staged ramp](./tpm-for-ai-products.md). Average quality
rises, but a template the biggest customer relies on breaks, and the first detector is an
angry email. 🎯 *Takeaway:* a model change is a migration wearing a config change's clothes;
score it, shadow it, ramp it, and keep the old version one re-pin away.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [The technical PM role](./the-technical-pm-role.md) | Own outcomes; influence without authority | Which decisions are mine, framed by me, or not mine? |
| [Discovery to delivery](./discovery-to-delivery.md) | Kill ideas cheaply, build the survivors | What's my evidence on valuable / usable / feasible / viable? |
| [Specs, PRDs & RFCs](./specs-prds-and-rfcs.md) | Write the what; read the how | Could the team define "done" without asking me? |
| [Prioritization & roadmaps](./prioritization-and-roadmaps.md) | Order is strategy; roadmaps are bets | What does this yes displace? |
| [Working with engineering](./working-with-engineering.md) | Rituals carry intent; trust carries truth | Am I negotiating scope or corrupting estimates? |
| [Metrics & experimentation](./metrics-and-experimentation.md) | Measure or you shipped an opinion | Which event proves this worked — and what guards the downside? |
| [Launches, rollouts & migrations](./launches-rollouts-and-migrations.md) | Ship gradually; finish the migration | What's the one action that restores yesterday? |
| [TPM for AI](./tpm-for-ai-products.md) | Evals are the spec; the flywheel is the moat | Can we tell, with evidence, whether any change helps? |

**The through-line:** technical product management is a loop, not a lane — discover cheaply,
specify clearly, prioritize honestly, build together, measure ruthlessly, release gradually,
and feed what production teaches you back into the next turn of the loop. AI products don't
change the loop; they raise its stakes, because a probabilistic product without evals,
feedback capture, and disciplined releases isn't a product — it's a demo with traffic. The
craft in this module is what turns the demo into a business.

> **Walk-away question:** *"For my current initiative, can I trace the loop end to end —
> the evidence it's worth building, the spec that defines done, the metric that will judge
> it, the rollout that protects it, and the feedback that improves it — and which link
> would snap first?"*

---

← Back to [module overview](./README.md)

## Test yourself

1. **What makes an estimate of "3 weeks for a form" credible, and what's the right response to it?**
   <details><summary>Answer</summary>The system around the form (migrations, backfills, old clients, dependent pipelines). The right response is "walk me through it" — decompose the estimate, then trade scope knowingly. (<a href="../technical-product-sense/tech-debt-and-estimation.md">Tech debt & estimation</a>)</details>
2. **During a SEV1, what comes first: root cause or rollback — and why?**
   <details><summary>Answer</summary>Rollback (mitigation). Users are paying for every minute of diagnosis; understand it fully after service is restored. (<a href="./incidents-and-postmortems.md">Incidents & postmortems</a>)</details>
3. **Why must the experiment hypothesis be written *before* launch?**
   <details><summary>Answer</summary>Because post-hoc, any result can be narrated into a win. Pre-registration — including "if wildly successful, what would that look like?" — sets the bar the result has to clear. (<a href="./metrics-and-experimentation.md">Metrics & experimentation</a>)</details>
4. **What are the three loops of eval-driven development?**
   <details><summary>Answer</summary>Inner: build ↔ eval (every change scored). Release: eval → staged rollout → production. Outer: production behaviour reshapes the spec. The PM's leverage is keeping the arrows back into the eval suite alive. (<a href="./tpm-for-ai-products.md">TPM for AI products</a>)</details>
5. **What turns a postmortem from ritual into learning?**
   <details><summary>Answer</summary>Blamelessness (so it hears the truth) plus action items with owners and dates, tracked like features — and escalation when a repeat incident finds one unshipped. (<a href="./incidents-and-postmortems.md">Incidents & postmortems</a>)</details>
