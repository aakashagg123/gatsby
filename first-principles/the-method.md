# The method: deconstruct, challenge, reconstruct

*Part of [07 · First Principles & the Polymath Mind](./README.md)*

## TL;DR

First-principles thinking isn't a flash of genius — it's a three-step loop you can run on
purpose. **Deconstruct** the problem into component claims; **challenge** each claim until
you find the few that are actually bedrock and the many that are merely inherited;
**reconstruct** a solution from the bedrock up. Three classic tools power the loop:
**Socratic questioning** to surface assumptions, the **5 Whys** to drill to root causes,
and **Fermi estimation** to sanity-check magnitudes from scratch. The output is not just an
answer but a *map of which constraints are real*.

> 🎯 **For the builder**
>
> **Why it matters** — "Think from first principles" is useless as advice without a
> procedure. A procedure makes the skill teachable, repeatable, and reviewable by other
> people — it turns insight into process.
>
> **What it changes in your decisions** — You can run the loop in a meeting, on a
> whiteboard, in a doc. You stop waiting for inspiration and start *operating* a method,
> which means juniors can do it too and you can audit where the reasoning broke.
>
> **Ask yourself** — *"Which of these requirements did we derive, and which did we just
> inherit and never re-check?"*
>
> **Risk if ignored** — Without an explicit method, "first principles" becomes a rhetorical
> flourish people attach to whatever they already wanted to do.

## The loop

```
        ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
   ─────▶  DECONSTRUCT  ─────▶   CHALLENGE   ─────▶ RECONSTRUCT   ─────▶ answer
        │  break into  │     │  test each   │     │  rebuild from│
        │  claims      │     │  assumption  │     │  what's true │
        └──────────────┘     └──────────────┘     └──────────────┘
                                     │                    │
                                     └────── iterate ◀────┘
```

It is a *loop*, not a line: reconstruction usually exposes a claim you mislabeled, sending
you back to challenge it again.

### 1 · Deconstruct — break the problem into claims

Write down everything the current answer assumes. Be ruthlessly explicit; the goal is to
drag invisible assumptions into the light where they can be examined. For "our onboarding
takes two weeks," the claims might be: *setup requires manual provisioning · provisioning
requires a human approval · approval takes a day · there are nine steps · each step needs
the previous one's output…*

The trick is **granularity**: keep splitting until each claim is something you could
independently mark true, false, or "actually a goal in disguise." A claim you can't
evaluate is still too coarse.

### 2 · Challenge — test each assumption to its root

Now interrogate every claim. For each, ask *why is this true?* and *what would have to be
the case for it to be false?* You're sorting claims into three bins:

- **Bedrock** — bottoms out in physics, math, a chosen goal, or observed fact. Keep.
- **Inherited** — true for some other context, copied into yours unexamined. *Suspect.*
- **Already false** — once stated plainly, obviously not true here. Discard.

Most "hard constraints" turn out to be inherited. The two workhorse tools below are how you
do the challenging.

### 3 · Reconstruct — build up from what survived

Take only the claims that survived as bedrock and ask: *given just these, what's the best
solution?* Crucially, you are no longer bound by the original answer's shape. The
reconstructed solution is allowed to look nothing like the thing you started with — that's
the entire point, and the source of any non-obvious result.

## Tool 1 · Socratic questioning — surface the assumption

Socratic questioning is structured doubt. A compact, reusable set:

| Question | What it flushes out |
| --- | --- |
| What exactly do I mean by this? | Vague terms hiding disagreement |
| How do I know it's true? | Borrowed beliefs with no evidence |
| What am I assuming to get here? | The invisible premise |
| What if the opposite were true? | Constraints that are really choices |
| Where did this belief come from? | "Best practice" with no owner |
| What would change my mind? | Unfalsifiable (and therefore useless) claims |

The single highest-yield question is **"how do I know this is true?"** Run it on the claim
that feels *most obvious*. Obviousness is exactly where unexamined assumptions hide.

## Tool 2 · The 5 Whys — drill to the root cause

Borrowed from Toyota's production system: ask "why?" roughly five times in a chain, each
answer becoming the next question, until you reach a root you can actually fix rather than a
symptom you'd keep patching.

```
The deploy failed.                         → why?
  The migration timed out.                 → why?
    It locked a 40M-row table.             → why?
      It rewrote every row.                → why?
        We added a column with a default.  → why?
          Nobody knew that rewrites the table on this DB version.  ← root cause
```

Patch at the top (retry the deploy) and it recurs forever. Fix at the root (add the column
without a row-rewrite) and the class of failure disappears. "Five" is a guideline, not a
ritual — stop when you hit something fundamental, which connects directly to
[production failure modes](../06-strategy-tradeoffs/production-failure-modes.md).

## Tool 3 · Fermi estimation — rebuild the number from scratch

Named for Enrico Fermi, who estimated the Trinity blast's yield by dropping scraps of paper
and watching how far the shockwave pushed them. A Fermi estimate decomposes an unknown
quantity into factors you *can* guess and multiplies them — deriving a number from
fundamentals rather than looking it up or trusting a vendor's claim.

The canonical interview version — *how many piano tuners are in Chicago?* — decomposes into
population ÷ people-per-household × fraction-with-pianos ÷ pianos-per-tuner-per-year, and
lands within a factor of a few of the truth. The point isn't piano tuners; it's the move:
**when someone hands you a number, can you reconstruct its order of magnitude from
components?** If you can't, you can't tell whether it's reasonable — and "this number is
off by 100×" is one of the most valuable things first-principles reasoning catches.

This is the quantitative twin of decomposition, and it pairs naturally with the
[opportunity-cost and second-order](./mental-models-latticework.md) models from the next
lesson.

## A worked pass

**Problem:** "We need a bigger server; the report takes 9 hours to generate."

1. **Deconstruct** — claims: the report scans the whole dataset · it runs single-threaded ·
   it recomputes everything nightly · users need it daily · "bigger server" = faster.
2. **Challenge** — *Do users need it daily?* (Socratic) → actually most read last week's.
   *Why 9 hours?* (5 Whys) → it re-derives from raw events every run because results were
   never cached. *Is a bigger server even the lever?* (Fermi) → 90% of the time is in one
   recompute that a cache eliminates; CPU is barely the bottleneck.
3. **Reconstruct** — from the survivors (most reads are stale-tolerant; the cost is
   recomputation, not hardware): cache incremental results, recompute only deltas. The "9
   hours" and the "bigger server" both evaporate — and neither was a real constraint.

## Failure modes

- **Stopping at the first satisfying answer** — the loop ended when you got the conclusion
  you wanted, not when you hit bedrock. Confirmation bias wearing the method's clothes
  (see [traps & limits](./traps-and-limits.md)).
- **Theatrical 5 Whys** — asking "why" five times mechanically and accepting shallow
  answers, reaching a fake root. Depth, not count, is the goal.
- **False-precision Fermi** — treating an order-of-magnitude estimate as a real forecast.
  It's a *sanity check*, not a budget.
- **Deconstructing forever** — analysis with no reconstruction. The method must terminate
  in a rebuilt answer or it was just procrastination.

## Practitioner checklist

- [ ] Have I written the inherited answer's assumptions down *explicitly*, not kept them in
      my head?
- [ ] Did I run "how do I know this is true?" on the claim that feels most obvious?
- [ ] Did at least one "why" chain reach something I'd call a root cause, not a symptom?
- [ ] Can I reconstruct the key numbers from components and have them roughly match
      reality?
- [ ] Did the loop actually *terminate* in a rebuilt solution, not an endless audit?

## Related lessons

- [What first-principles thinking actually is](./what-is-first-principles.md)
- [A latticework of mental models](./mental-models-latticework.md)
- [Traps & limits](./traps-and-limits.md)
- [Production failure modes](../06-strategy-tradeoffs/production-failure-modes.md)
