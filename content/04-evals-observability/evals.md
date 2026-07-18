# Evals: golden sets, regression tests, adversarial tests, LLM-as-judge, and human evals

*Part of [04 · Evals & Observability](./README.md)*

## TL;DR

Evals are the test suite for a non-deterministic system. Because you can't assert exact
equality, you build **golden sets** (curated inputs with known-good outputs), run them
as **regression tests** in CI to block quality drops, add **adversarial tests** for the
ways you expect it to break, and score open-ended outputs with **LLM-as-judge**
(calibrated against **human evals**). Without evals you're flying blind: every prompt
tweak, model swap, or [quantization](../01-inference-internals/quantization-formats.md)
change is a coin flip, and regressions ship silently.

> 🎯 **For the AI-native PM**
>
> **Why it matters** — Evals are the difference between "we think it got better" and "we know." For an AI-native PM, the eval set *is* the product spec — it encodes what "good" actually means.
>
> **What it changes in your decisions** — Your release gates, how you compare model options, and how you prove improvement to stakeholders.
>
> **Ask your eng team** — *"What's our regression eval, and does it run before every model or prompt change ships?"*
>
> **Product risk if ignored** — A model update silently regresses 5% of cases and you hear about it from users, not from CI.


## Mental model

Traditional tests assert `f(x) == expected`. LLM outputs are variable and open-ended,
so you shift from exact-match to **graded quality over a representative distribution**:
- For closed tasks (classification, extraction, structured output) you *can* use
  exact/structural checks.
- For open tasks (summaries, answers, code) you grade against a **rubric** with a judge
  (model or human), and track *aggregate* scores and *regressions*, not single outputs.

Evals turn "it feels better" into a number you can gate on.

## Error analysis — look at your traces first

Before choosing metrics or building graders, practice **error analysis** — the
discipline (borrowed from qualitative research) that turns raw production behaviour
into an eval suite that measures *your* failures, not generic ones:

1. **Create a dataset** — pull real traces: random samples plus anything flagged by
   users, cheap screens, or your own suspicion.
2. **Open coding** — read traces one by one and label failures free-form, in your own
   words ("ignored the date constraint," "cited the wrong doc"). No taxonomy yet.
3. **Axial coding** — cluster those labels into a failure taxonomy: the five or ten
   recurring modes that actually matter.
4. **Iterate** — build automated evaluators for the *recurring, high-impact* modes only,
   then re-run the analysis on fresh production traces regularly; the taxonomy rots as
   users find new ways to use (and break) the product.

This is also the minimum viable eval setup: a spreadsheet of traces, pass/fail labels,
and notes beats a metrics dashboard you haven't validated. Most teams over-invest in
scoring infrastructure and under-invest in the hours of reading traces that tell you
what's worth scoring.

## Golden sets — the backbone

A golden set is a curated, **version-controlled** collection of inputs paired with
known-good outputs or acceptance criteria.
- **Representative.** Mirror real production traffic — common cases *and* the long tail,
  per feature and per [tenant](./cost-attribution.md) segment where behavior differs.
- **Labeled with intent.** Store *why* an output is correct (criteria/rubric), not just
  the string, so judges and humans can grade consistently.
- **Living.** Grow it from production: every incident and bug becomes a new golden case
  so the same regression can't recur (this is how evals compound in value).
- **Stratified.** Tag cases by capability (math, extraction, refusal, multi-hop) so you
  see *where* quality moves, not just an aggregate.

## Regression tests — gate every change

Run the golden set automatically before prompt, model, retrieval, or infra changes
ship; block on score drops.
- Catches the silent killers: a model upgrade that helps 95% and breaks 5%, a prompt
  edit with side effects, a [quantization](../01-inference-internals/quantization-formats.md)
  step that hurts strict-format tasks.
- Report per-stratum deltas, not one number — a flat average can hide a category falling
  off a cliff.
- This is the CI gate referenced throughout the curriculum
  ([structured output](../02-reliable-outputs/structured-output.md),
  [retrieval evals](../03-rag/retrieval-evals.md),
  [routing](../02-reliable-outputs/model-routing.md) portability).

## Adversarial tests — break it on purpose

Beyond "does it work," test "how does it fail":
- **Prompt injection / jailbreaks** — does retrieved or user content hijack behavior?
  (see [safety engineering](../05-safety-multitenancy/safety-engineering.md)).
- **Edge inputs** — empty, huge, malformed, multilingual, contradictory, out-of-scope.
- **Hallucination bait** — questions whose answer isn't in context; does it say "I don't
  know" or fabricate? ([grounding](../03-rag/retrieval-evals.md)).
- **Format stress** — does structured output stay valid under weird inputs?
- **Tool misuse** — does it call dangerous tools when goaded?
Adversarial cases join the golden set and run in regression.

## LLM-as-judge — scoring at scale

Use a model to grade outputs against a rubric (correctness, grounding, helpfulness,
style). Powerful but it has failure modes you must control:
- **Calibrate against humans.** Establish agreement between judge and human labels
  before trusting it; re-check periodically.
- **Known biases:** position bias (favoring the first option), verbosity bias (longer =
  better), self-preference (favoring its own family), leniency. Mitigate with
  randomized order, pairwise comparison, clear rubrics, and reference answers.
- **Prefer comparative grading** (A vs. B) over absolute scores where possible — it's
  more reliable.
- **Don't judge with the same model under test** for safety-critical evals; a separate
  judge avoids blind spots.
- The judge is itself a system to evaluate — its accuracy is a metric you monitor.

## Human evals — the ground truth

The anchor everything else calibrates to.
- **Use for:** establishing rubrics, calibrating judges, ambiguous/subjective quality,
  high-stakes decisions, and sampling production for blind spots.
- **Make it rigorous:** clear guidelines, multiple raters, inter-rater agreement,
  blind/randomized presentation to avoid bias.
- Expensive and slow, so spend it where it matters most and let calibrated judges scale
  the rest.

## Grading choices that keep evals honest

- **Binary beats Likert.** Prefer pass/fail judgments over 1–5 scales: forced decisions
  are more consistent across annotators, trivially aggregable, and map directly to a
  launch bar. A 3.7 average hides exactly the disagreement a pass/fail split exposes.
- **Skip generic similarity metrics.** BERTScore, ROUGE, and off-the-shelf "quality"
  metric packs correlate poorly with what *your* users consider good; a custom evaluator
  per failure mode (from your error analysis) is worth a dozen ready-made scores.
- **Don't automate everything.** An evaluator per failure mode you've ever seen is
  maintenance debt; automate the recurring, high-impact modes and keep the long tail in
  periodic human review.
- **Annotation is product judgment — keep it in-house.** Outsourced labelers apply
  *their* judgment of good, not yours, and the learning (what's failing and why)
  leaves with the vendor. PM and eng should label traces together — disagreements
  between them are requirement discoveries, not noise. A minimal custom review
  interface (render the trace intelligently, keyboard shortcuts, cluster/filter) pays
  for itself in review throughput.

## How the layers fit

```
human evals ──calibrate──▶ LLM-as-judge ──scores──▶ golden set ──runs in──▶ regression CI gate
     ▲                                                   ▲
     └──────────── production sampling & incidents ──────┘  (adversarial cases added here)
```

## Tradeoffs

| Method | Strength | Cost / risk |
| --- | --- | --- |
| Exact/structural | Cheap, objective | Only for closed tasks |
| Golden + regression | Catches drift, gateable | Curation effort; must stay representative |
| Adversarial | Finds failure modes | Needs creativity; never "complete" |
| LLM-as-judge | Scales, cheap-ish | Bias; needs calibration |
| Human | Ground truth | Slow, expensive |

## Failure modes

- **No regression gate** — silent quality drop after a model/prompt change.
- **Unrepresentative golden set** — green evals, unhappy users; the set doesn't match
  reality.
- **Trusting an uncalibrated judge** — confident, biased scores.
- **Aggregate hides a cliff** — average flat while a category collapses; stratify.
- **Stale evals** — the set rots as the product evolves; prune and grow it.

## Practitioner checklist

- [ ] Is there a version-controlled, representative, stratified golden set?
- [ ] Do regression evals gate prompt/model/retrieval/infra changes in CI?
- [ ] Do adversarial cases (injection, hallucination bait, format stress) run too?
- [ ] Is any LLM judge calibrated against humans and checked for bias?
- [ ] Do incidents and bugs get added back as permanent eval cases?
- [ ] Do you report per-capability deltas, not just one average?

## Related lessons

- [Observability](./observability.md)
- [Retrieval evals](../03-rag/retrieval-evals.md)
- [Structured output](../02-reliable-outputs/structured-output.md)
- [Quantization formats](../01-inference-internals/quantization-formats.md)
- [Production failure modes](../06-strategy-tradeoffs/production-failure-modes.md)
