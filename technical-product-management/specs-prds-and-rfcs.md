# Specs, PRDs & RFCs

*Part of [Technical product management for the AI PM](./README.md)*

## TL;DR

Writing is the PM's power tool. The documents form a stack: **vision** (why we exist)
→ **strategy** (where we'll win) → **roadmap** (what, in what order) → **PRD** (what
exactly, for one initiative) → **RFC / design doc** (how, written by engineering) →
**tickets** (the work itself). Each layer answers questions the layer below shouldn't have
to re-litigate. The PRD is yours. A good one nails the *problem*, *goals and non-goals*,
*requirements with acceptance criteria*, *non-functional requirements*, and *how we'll
measure success* — and stays silent on implementation. The RFC is engineering's. Your job
there is to be its sharpest *reader*, checking the design against the product intent it
claims to serve.

> 🎯 **For the AI PM**
>
> **Why it matters** — Deterministic features can be specified by enumerating behaviour:
> "clicking X does Y." An AI feature can't — you can't enumerate every input. The spec has
> to define *quality* instead of *behaviour*.
>
> **What it changes in your decisions** — Your PRD gains new mandatory sections: example
> inputs and *graded* ideal outputs (the seed of an eval set), explicit tolerance for being
> wrong ("what's the cost of a bad answer, and what does the user see?"), and latency/cost
> budgets as first-class NFRs.
>
> **Ask yourself** — *"Could an engineer read this spec and know how good is good enough —
> without asking me?"*
>
> **Risk if ignored** — The team builds to "make the AI answer questions," discovers
> "good enough" was never defined, and the launch decision becomes a vibes-based argument
> in week eleven.

## The document stack

```mermaid
flowchart TB
  V["Vision<br/>why we exist — years"] --> S["Strategy<br/>where we play & win — year"]
  S --> R["Roadmap<br/>ordered bets — quarters"]
  R --> P["PRD<br/>one initiative: what & why — weeks"]
  P --> F["RFC / design doc<br/>how — written by engineering"]
  F --> T["Tickets<br/>sliced, estimated work"]
  P -. "acceptance criteria<br/>trace down" .-> T
  F -. "constraints & risks<br/>feed back up" .-> P
```

Two arrows matter most. Acceptance criteria written in the PRD should be traceable all the
way into tickets — if a ticket can't be traced to a requirement, ask why it exists. And
RFCs feed *back*: engineering's design work routinely uncovers a constraint ("that data
doesn't exist", "that latency is impossible without precomputation") that must flow back up
and change the PRD, not get silently absorbed.

## Anatomy of a PRD engineers respect

Length is not quality — one to four pages beats twenty. The sections that earn their place:

- **Problem & evidence** — whose problem, how you know it's real, what it costs today.
  This is the section engineers actually read to decide if the project is worth caring
  about. Write it best.
- **Goals and non-goals** — non-goals are the highest-leverage sentence in the document.
  "V1 does not support bulk import" kills a hundred Slack threads in advance.
- **Requirements with acceptance criteria** — each requirement testable: *given* a
  context, *when* the user acts, *then* this observable result. "The search should be
  fast" is an opinion. "Search returns first results within 500 ms at p95" is a
  requirement.
- **Non-functional requirements (NFRs)** — the ones that get forgotten until they're
  emergencies: latency and availability targets, scale assumptions, privacy and data
  residency, accessibility, localization, security review, support/admin tooling. NFRs are
  where the [technical product sense](../technical-product-sense/README.md) track cashes in.
- **Edge cases and unhappy paths** — what happens on empty state, failure, retry, abuse.
  If the PRD only describes the happy path, the engineers design the unhappy ones alone.
- **Success metrics** — the numbers that will move if this works, and when you'll check
  ([Metrics & experimentation](./metrics-and-experimentation.md)).
- **Open questions** — an explicit list. Pretending certainty you don't have costs trust.
  A visible open-questions section *builds* it.

What a PRD should *not* contain: database schemas, API designs, technology choices, or a
solution disguised as a requirement. ("Build a Redis cache" is a design. "Repeat visits
must load in under a second" is the requirement behind it.)

## Reading an AI-drafted PRD

A model can produce a structurally perfect PRD from a two-line prompt — problem statement,
goals and non-goals, requirements, success metrics, all present, all readable. That speed
changes the job. Writing the first draft used to be the hard part; now catching what the
draft got wrong is. Read an AI draft the way the next section teaches you to read an RFC —
as a skeptic, not a proofreader:

- **Invented specificity** — a fabricated latency number, a "success metric" nobody agreed
  on, an edge case named with total confidence and zero evidence behind it. Numbers with no
  source are the tell.
- **Missing non-goals** — models default to comprehensive-sounding scope, because "no"
  isn't in the training signal the way "yes, and" is. The highest-leverage sentence in a
  PRD is usually the one the draft never wrote.
- **Silently dropped edge cases and cross-team dependencies** — the draft answers the
  question you asked, not the ones you forgot to ask. A model has no way to know which
  other team's roadmap this touches; you do.
- **A plausible tone standing in for a real decision** — confident, well-formatted prose is
  easy to mistake for a decision that was actually made. If you can't trace a requirement
  back to real evidence — a user quote, a support-ticket count, a spike result — cut it or
  mark it an open question.

The upside is real: a model can turn "here's what I roughly mean" into a structured draft
in minutes, freeing your time for the part that was always the actual job — deciding
what's true and what's missing. Use it to draft faster. Don't use it to skip the review
that makes the document yours.

## Reading an RFC like a PM

The RFC (design doc) is where engineering proposes *how*. You won't judge the
architecture — but you're the only reader checking it against product intent. Read for:

- **Does the design serve the requirements it cites?** RFCs sometimes quietly relax a
  requirement ("we'll refresh nightly instead of real-time"). Nightly might be fine — but
  that's your call, made in the open.
- **The trade-offs section** — every honest RFC lists rejected alternatives. Check the
  rejection reasons against product priorities. Engineers optimize for elegance and
  operability, which *usually* aligns with users, but not always.
- **The migration/rollout plan** — how the world moves from old to new
  ([Launches, rollouts & migrations](./launches-rollouts-and-migrations.md)). Missing
  rollout plan = risk landing on your launch date.
- **New promises being made** — an RFC that exposes a new API or data contract is creating
  something other teams will depend on, which is product surface, whether or not it has a UI.

Comment with questions, not directives. "What happens to requirement 4's p95 target under
this design?" moves the conversation. "Use Postgres instead" ends it.

## Acceptance criteria for probabilistic features

The AI-specific craft deserves its own pattern. You can't write "the summary is always
accurate." You *can* write:

- **Eval-based criteria** — "on the 200-example eval set, ≥90% of summaries are graded
  *acceptable or better* by the rubric in appendix A; zero examples in the *harmful*
  category." The eval set becomes part of the spec.
- **Behavioural bounds** — "when confidence is low or retrieval returns nothing, the
  feature says it can't answer rather than guessing; it never fabricates a citation."
- **Budgets** — "p95 end-to-end latency ≤ 3 s; marginal cost ≤ $0.02 per request at
  projected volume."

This is the bridge into [eval-driven development](./tpm-for-ai-products.md) — the AI
capstone builds on exactly this section.

## Failure modes

- **The write-once PRD** — treated as done when circulated, never updated as reality
  arrives. A stale spec is worse than none. People follow it.
- **Solutioneering** — specifying implementation in the PRD. You get your design *and*
  full blame when it underperforms — and you taught the engineers not to think.
- **The unread masterpiece** — twenty pages nobody finishes. If the team can't recall the
  goals and non-goals, the document failed regardless of quality.
- **NFRs by default** — no latency, privacy, or scale targets stated, so the system
  inherits whatever the implementation happened to produce.
- **Consensus-by-silence** — circulating a doc, hearing nothing, calling it alignment.
  Silence means *unread*. Review meetings exist for a reason.
- **Rubber-stamped AI draft** — a fluent, structurally complete PRD shipped without
  checking its specifics against real evidence. The format made it look reviewed.

## Practitioner checklist

- [ ] Does my current PRD have explicit non-goals — and have they killed at least one
      scope argument?
- [ ] Is every requirement testable — could QA (or an eval) verify it without asking me?
- [ ] Are latency, privacy, scale, and failure behaviour stated, or defaulted?
- [ ] Have I read the RFC for my current build and traced each requirement into it?
- [ ] For AI features: does the spec include graded examples and a "how good is good
      enough" threshold?
- [ ] For any AI-drafted section of this PRD: have I traced its specific claims (metrics,
      edge cases, non-goals) back to real evidence, not just fluent prose?

## Related lessons

- [Discovery to delivery](./discovery-to-delivery.md)
- [Working with engineering](./working-with-engineering.md)
- [Technical product management for AI](./tpm-for-ai-products.md)
