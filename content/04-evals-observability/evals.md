# Evals: Golden Sets, Regression Tests, Adversarial Tests, LLM-as-Judge, and Human Evals

*Part of [04 · Evals & Observability](./README.md)*

## TL;DR

Evals are the test suite for a non-deterministic system. Because you can't assert exact
equality, you build **golden sets** (curated inputs with known-good outputs), run them
as **regression tests** in CI to block quality drops, add **adversarial tests** for the
ways you expect it to break, and score open-ended outputs with **LLM-as-judge**
(calibrated against **human evals**). Without evals you're flying blind: every prompt
tweak, model swap, or [quantization](../01-inference-internals/quantization-formats.md)
change is a coin flip, and regressions ship silently.

## Mental model

Traditional tests assert `f(x) == expected`. LLM outputs are variable and open-ended,
so you shift from exact-match to **graded quality over a representative distribution**:
- For closed tasks (classification, extraction, structured output) you *can* use
  exact/structural checks.
- For open tasks (summaries, answers, code) you grade against a **rubric** with a judge
  (model or human), and track *aggregate* scores and *regressions*, not single outputs.

Evals turn "it feels better" into a number you can gate on.

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
