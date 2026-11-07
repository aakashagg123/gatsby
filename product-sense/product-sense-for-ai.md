# Product sense for AI products

*Part of [Product sense for the AI PM](./README.md)*

## TL;DR

Everything in this module still applies when your product is powered by a model. But the
*material* changes, and product sense has to adapt. A model is **probabilistic,
non-stationary, and confidently wrong sometimes**. That reshapes five instincts. Quality
becomes something you *measure with evals* rather than eyeball. Trust has to be engineered
under **non-determinism**. **Latency and cost** become first-class UX, not back-end
details. The capability frontier is **jagged**, so scoping is a product skill. And
**feedback becomes a flywheel** you design on purpose. The AI PM's edge is knowing where a
model genuinely adds value, and where a boring deterministic feature wins.

> 🎯 **For the AI PM**
>
> **Why it matters** — This is the synthesis lesson. It takes motivation, empathy,
> creativity, communication, and domain expertise, and ports them into the one place they
> most often break: a product whose core component is a stochastic model.
>
> **What it changes in your decisions** — You stop treating "the model" as the product. You
> start treating the *system around it* — evals, guardrails, fallbacks, UX for failure — as
> the product. That system is exactly where taste and judgment live.
>
> **Ask yourself** — *"For this job, does a probabilistic model actually beat a deterministic
> feature — and if it does, how will the product stay trustworthy when the model is wrong?"*
>
> **Risk if ignored** — Shipping the demo, not the product: a magical first impression that
> can't be trusted, measured, or afforded at scale.

## Taste becomes evals

```mermaid
flowchart LR
  subgraph OLD["Deterministic product"]
    O1["Look at it —<br/>you can see 'right'"]
    O2["Latency & cost:<br/>engineering's problem"]
    O3["Capability: smooth —<br/>hard things are hard"]
  end
  subgraph AI["Model-powered product"]
    N1["'Right' is a distribution —<br/>taste becomes EVALS"]
    N2["Latency & cost<br/>are UX"]
    N3["Capability is JAGGED —<br/>scoping is the skill"]
  end
  O1 --> N1
  O2 --> N2
  O3 --> N3
  N1 & N2 & N3 --> TR["Trust is engineered,<br/>and feedback is a designed flywheel"]
```

With a normal feature you can look at it and know if it's right. With a model, "right" is a
distribution — the same prompt can produce a great answer today and a poor one tomorrow. So
product taste has to become **measurable**. The AI PM defines what "good" means as an
**eval**: a graded set of representative and adversarial cases the product must pass, run
continuously so quality doesn't silently regress. Your product sense — knowing what a great
output *feels* like for this user — is what makes the eval meaningful. Without it, you
optimize a number that doesn't map to value. And you exercise it trace by trace: read real
outputs and call pass or fail, rather than reviewing an aggregate score someone else
defined. The dashboard tells you *that* quality moved. The traces tell you *what good means
here*.

This is the same instinct as [measuring satisfaction](./motivation-and-behaviour.md), just
moved upstream into the model's outputs. (The engineering of this — golden sets,
LLM-as-judge, regression gates — is the subject of the AI Engineering track's
[evals lesson](../content/04-evals-observability/evals.md).)

## Trust under non-determinism

A confidently-wrong answer is worse than a visibly-broken feature, because the user can't
tell. Product sense for AI is largely **trust design**:

- **Show your work** — grounding answers in retrieved, citeable sources so users (and you) can
  check them, and saying *"I don't know"* when the context is silent rather than inventing.
- **Calibrate confidence** — signal uncertainty in the UX instead of presenting every output
  with the same authority. Microsoft's 18 guidelines for human-AI interaction (CHI 2019)
  and Google's People + AI Guidebook are good checklists for this.
- **Disclose the machine** — in the EU, the transparency rules say people must be made aware
  they are interacting with an AI system. The Commission's AI Act page gives August 2026 as
  the date these rules apply. Ask legal for any transition terms.
- **Check that your eval rewards "I don't know"** — OpenAI researchers argue models hallucinate
  partly because common benchmarks score a guess higher than an abstention, so models learn to
  be good test-takers (arXiv 2509.04664). An eval that gives no credit for abstaining trains
  the same habit into your product.
- **Design the failure, not just the success** — the [Hook-model reward](./motivation-and-behaviour.md)
  has an evil twin: a bad first output that breaks the habit forever. Graceful failure,
  easy correction, and "undo" are core, not polish.

The [cognitive-empathy](./cognitive-empathy.md) tools matter more here: simulate the user
who trusts a wrong answer, and the one who's been burned once and now distrusts every
answer.

## Latency and cost are UX

For a deterministic feature, latency and cost are engineering concerns. For an AI feature
they're **product** concerns, because they trade directly against quality:

| Lever | Buys you | Costs you |
| --- | --- | --- |
| Bigger / stronger model | Quality | Latency, $ |
| Smaller / quantized model | Speed, $ | Some quality |
| Streaming the response | *Perceived* speed | — |
| Caching | Speed, $ | Staleness risk |

The product-sense call is *which axis this user's job actually cares about* — code
autocomplete lives or dies on latency, while an agent that works for minutes on a whole
task is judged on whether the result is right. A legal-review tool can wait for accuracy.
Reasoning models blur the line: the same model can spend more thinking tokens, and more
time and money, on a hard request. (The
mechanics of these trade-offs are the AI Engineering track's
[stack-tradeoffs lesson](../content/06-strategy-tradeoffs/inference-stack-tradeoffs.md).) This is
[motivation theory](./motivation-and-behaviour.md) again: a slow or costly path is friction
that squanders the model's value.

## The jagged frontier — scoping as product sense

Model capability is **jagged**: a model can draft a legal argument yet miscount the words in
a sentence. There's no smooth "it's good at hard things and better at easy things" line. The best
evidence is the Harvard/BCG field study of 758 consultants (Dell'Acqua and colleagues,
2023). On a task inside the frontier, GPT-4 users scored about 40% above the control group.
On a task just outside it, they scored about 23% worse, because many took the tool's
misleading output at face value. Those models are old, but the lesson is current: you
cannot see the edge from the inside. So
the highest-leverage product decision is **scoping** — pointing the model at jobs inside its
reliable frontier and keeping it away from jobs where its failure is costly and invisible.

This is [strategic thinking](./creativity.md) applied to capability: the differentiation
isn't "we have AI," it's *"we found the job where this model is genuinely reliable and
valuable, for a user who cares."* Often the best AI product uses the model for the 20% that
delights and a deterministic system for the 80% that must be correct.

For enterprise products, plot the job on two axes: **task complexity** and the buyer's
**tolerance to task failure**. Most visible AI wins live where failure is cheap — a blog
outline that misses is just deleted. Enterprise value lives where failure is expensive —
a diagnosis, a payment. The way in is not to wait for a perfect model. Instead, take
jobs of modest complexity in low-tolerance domains and *wrap service checks around
them*: verification steps, human gates, escalation paths. The frontier then shifts
outward with the model, but the scoping discipline is what got you in the room.

## AI-enabled vs. AI-native

A distinction sharpens scoping conversations: an **AI-enabled** product bolts a
model onto an existing product — the photo editor that grows an "AI-enhance" button. An
**AI-native** product is built around the model — the generative image platform where,
without the model, there is no product. The test is one question: *turn the model off —
what's left?* Both are legitimate. The product-sense failure is building one while
pricing, roadmapping, or pitching the other. AI-enabled work is feature work: the
existing product's quality bar, margins, and UX conventions still govern. AI-native work
changes the question you start from. It's not *"how can AI enhance this feature?"* but
*"if intelligence were the core material, how would we solve this problem from
scratch?"* That reframing makes the eval, the failure UX, and the cost curve the
product itself, not accessories to it.

## The patterns users now expect

Product sense includes knowing the reference points users bring, and 2025 reset them.
Four patterns became the standard candles every AI product gets compared against:

- **Deep-research modes** — async, minutes-long jobs that return a *report*, not a
  chat reply. They taught users that waiting is acceptable when the output is worth
  it — and reset expectations for what "an answer" can be.
- **Proactive AI** — briefings and suggestions that arrive *unprompted* (ChatGPT's
  Pulse-style morning digest, which shipped in 2025; OpenAI announced on 17 June 2026 that it
  was retiring Pulse in favour of general-purpose scheduled tasks — the branded feature came and went, but the pattern it taught
  users to expect didn't). The pattern's product sense is consent and restraint:
  proactivity delights precisely until it presumes.
- **Persistent memory as a headline feature** — "it remembers me" moved from silent
  personalization to a marketed, user-visible, user-editable surface. Products that
  remember silently now read as creepy. Products that forget read as broken.
- **Visible thinking** — showing reasoning progress ("searching… comparing…
  reconsidering…") became a trust affordance. Users forgive latency they can watch.
  They distrust magic that arrives instantly and wrong.

None of these obligates you to build all four. But every user who's touched a 2025-era
assistant now carries them as priors, and your product is scored against those priors
whether you like it or not.

## Feedback is a flywheel you design

AI products get better with use — but only if you build the loop. Every correction,
thumbs-down, and edit is signal. The [Hook model's investment phase](./motivation-and-behaviour.md)
becomes literal: user effort improves the product's data, which improves outputs, which
earns more use. Product sense here is deciding **what feedback to capture, how to make giving
it feel worthwhile, and how to close the loop** without violating trust or privacy.

One caution from systems thinking: a flywheel is a *reinforcing* feedback loop.
Reinforcing loops amplify whatever is in them — engagement, but also bias (a model that
under-serves a group gets less engagement from that group, which further shrinks their
share of the training signal) and filter bubbles. Design the **balancing loops**
alongside the flywheel: monitoring for skew, ethical checks on what the loop optimizes,
and a metric of success that rewards long-term user value rather than whatever spins
fastest.

Two public cases show the risk. In April 2025 OpenAI shipped a GPT-4o update that made
ChatGPT more sycophantic, then began rolling it back three days later. OpenAI said its
internal testing had not explicitly checked for sycophancy and that it would add such evals.
In September 2025 the FTC sent orders to seven companies that offer AI companion chatbots,
including OpenAI, Meta and Character.AI. The orders ask how they monetize user engagement
and how they measure harm to children and teens. A loop tuned to approval or engagement can
reward the wrong behaviour.

## Keep a human in the loop where it counts

Domain sense ([domain expertise](./domain-expertise.md)) tells you where a wrong answer is
merely annoying (a playlist suggestion) versus genuinely harmful (a medical dosage, a
financial transaction). The former can be fully automated. The latter needs a human
checkpoint, clear provenance, and an audit trail. Matching the level of autonomy to the
**cost of being wrong** in this domain is one of the sharpest expressions of AI product
sense.

## The role is fragmenting too

The same forces reshaping the product are reshaping the job title. "AI PM" is no longer
one role. Some commentators describe a split into an **AI Product Owner** (who owns eval
bars, model behaviour, and human-in-the-loop boundaries — the deployment-facing half of this
lesson) and a **Data-Informed PM** (who uses AI tooling to keep a continuous read on the
flywheel above). Only blogs support these two titles, so treat them as a useful lens, not an
industry standard. ([The technical PM
role](../technical-product-management/the-technical-pm-role.md) maps this split against
the classic PM/TPM/EM spectrum.) Neither title obligates you to specialize today. But
naming the split matters, because the failure mode isn't picking the wrong one — it's not
noticing your job quietly became three jobs, and doing all three badly instead of one
well.

## Actionable steps

- **Write the eval before the feature** — define, in cases, what "good" means for this job.
- **Design the wrong-answer path** — grounding, "I don't know," easy correction, undo.
- **Name the axis that matters** — latency, quality, or cost — and optimize for the user's job,
  not all three.
- **Scope to the reliable frontier** — list the jobs the model does reliably and the ones it
  doesn't. Ship the first, and guard or defer the second.
- **Instrument the feedback loop** — capture corrections and close the loop into evals and,
  where appropriate, the product.
- **Match autonomy to stakes** — full automation where wrong is cheap; human-in-the-loop where
  wrong is costly.

> **📦 Mini-case — Air Canada's chatbot.** The airline's support bot confidently
> described a bereavement-refund policy that didn't exist. A tribunal made the company
> honor it. Every theme of this lesson in one incident: an ungrounded model given full
> authority in the UX (no citations, no "I don't know"), no eval that would have
> caught policy hallucination, and a failure whose cost was legal and reputational,
> not technical. The fix — answer only from real policy documents, with citations —
> was a *product* decision available the whole time.

## Failure modes

- **Demo-driven development** — a great first impression that can't be measured, trusted, or
  afforded at scale.
- **Confident hallucination in the UX** — every output presented with equal authority, wrong
  ones included.
- **AI where deterministic wins** — using a probabilistic model for a job that needed to be
  exactly right.
- **No feedback loop** — a product that never improves because the signal was never captured.
- **Ignoring cost/latency until launch** — a delightful feature that's unaffordable or too slow
  in production.

## Practitioner checklist

- [ ] Have I defined "good" as an eval, grounded in real product taste?
- [ ] Is there a designed, trustworthy path for when the model is wrong?
- [ ] Do I know which of latency / quality / cost this user's job actually prioritizes?
- [ ] Have I scoped the feature to the model's *reliable* frontier?
- [ ] Does my eval give credit for abstaining, and do I disclose that users face an AI?
- [ ] Is there a feedback loop that turns usage into improvement — and does it avoid
      optimizing for approval or engagement alone?
- [ ] Does the level of autonomy match the cost of a wrong answer in this domain?
- [ ] Can I name which slice of "AI PM" work I actually own today — and which I've
      quietly absorbed without deciding to?

## Related lessons

- [Motivation theory](./motivation-and-behaviour.md)
- [Cognitive empathy](./cognitive-empathy.md)
- [Creativity](./creativity.md)
- [Domain expertise](./domain-expertise.md)
- [Recap & real-world examples](./recap.md)
- [Reliability, evals & ops](../harness-engineering/phases/09-reliability-evals-and-ops/README.md) — where product taste for AI becomes an executable eval suite.
