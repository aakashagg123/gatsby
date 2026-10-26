# Evaluation & observability — recap & real-world examples

*Part of [Evaluation & observability for the product leader](./README.md)*

## Real-world examples & war stories

**A model provider's silent weight update changing production behavior.** Providers change
what runs behind an endpoint, and behavior can shift with no code change on the customer's
side. Two documented cases show both sides. In 2023, Chen, Zaharia and Zou reported large
shifts in GPT-4 and GPT-3.5 between March and June (for example, prime-number accuracy
falling from 84% to 51%) and called for continuous monitoring. Narayanan and Kapoor
replied that much of this was behavior drift and test design, not lost capability: every
test number was prime, and extra explanatory text counted as a code failure. In 2025,
Anthropic's postmortem of three infrastructure bugs said its own evals were too noisy to
catch the degradation, and it added continuous production checks. The lesson holds either
way: a balanced, repeatable regression suite is how you tell real change from a
measurement artifact. 🎯 *Takeaway:*
[a regression gate](./why-eval-investment-is-the-job.md) is what turns an invisible
provider-side change into something a team can actually detect.

**Support and coding assistants graded only on final answers, not the path taken.** An
outcome-only eval cannot see an agent that reaches the right answer through a wasteful
path and burns far more cost and time than a clean run. This is a common risk, not a
single documented incident. Anthropic's guidance adds a limit: grade the outcome, because
rigid checks on an exact step sequence punish valid solutions. Track cost and step budgets,
and read the first wrong step in failing traces. 🎯 *Takeaway:*
[trajectory evals, not just outcome evals](./building-the-eval-stack-in-the-right-order.md),
are what catch a path quietly degrading before the destination does.

**Teams that built eval dashboards nobody trusted.** A recurring failure pattern in
early AI eval tooling adoption: a team invests in a polished scoring dashboard early,
skipping the unglamorous work of reading real traces first, and ends up with metrics
nobody on the team actually believes reflect real quality. 🎯 *Takeaway:*
[reading real traces before scoring them](./building-the-eval-stack-in-the-right-order.md)
is the step that makes every later investment trustworthy — skipping it doesn't save
time, it just moves the real work later and adds a layer of false confidence on top.

**A quantization or infrastructure change that quietly hurt one task category.** A
peer-reviewed study of quantized multilingual models (Marchisio et al., EMNLP 2024
Findings) found that automatic metrics understate the harm. In Japanese, a 1.7% average
drop on automatic tasks matched a 16.0% drop in human ratings on realistic prompts.
Harder tasks such as math reasoning degraded fastest. The same pattern applies to any
serving change: an averaged score can hide a task category falling off a cliff. 🎯 *Takeaway:*
[an aggregate number can hide a category falling off a cliff](./why-eval-investment-is-the-job.md);
only a stratified eval catches it before users do.

**LLM-as-judge grading systems found to favor their own model family.** LLM judges show
position, verbosity and self-enhancement bias (Zheng et al., 2023). Panickssery et al.
(2024) found that a model's ability to recognize its own output tracks how strongly it
favors that output. Such bias only surfaces when judge scores are checked against human
labels. 🎯 *Takeaway:* [an uncalibrated judge](./building-the-eval-stack-in-the-right-order.md)
produces confident, biased numbers that look exactly like real measurement until someone
checks them against ground truth.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [Why eval investment is the job](./why-eval-investment-is-the-job.md) | The eval set is the closest thing a non-deterministic system has to a spec | If a change quietly regressed 5% of cases, would we find out from a dashboard or from a customer? |
| [Building the eval stack in the right order](./building-the-eval-stack-in-the-right-order.md) | Reading real traces earns every later stage of the stack; skipping ahead produces tooling nobody trusts | Has anyone actually read real traces, or did we go straight to building a scoring pipeline? |

**The through-line:** an AI system's biggest risk is that it fails quietly, and the only
real defense is measurement built in the right order — starting with reading real
failures, not with sophisticated tooling. This module deliberately stayed at that
decision altitude rather than re-deriving the mechanics already developed in full depth
in [Evals](../content/04-evals-observability/evals.md),
[Observability](../content/04-evals-observability/observability.md), and
[Reliability & evals](../agentic-ai/reliability-and-evals.md), because the mistake that
actually sinks eval investment is rarely a wrong technique. It's the wrong order — a
dashboard built before anyone read a trace, or a judge trusted before anyone calibrated
it.

> **Walk-away question:** *"For this AI feature: has anyone read real failures before we
> built anything to score them, does a regression gate actually block a bad change from
> shipping, and would we know about a quiet regression from our own system before a user
> tells us?"*

If yes, this feature's quality is something the team can actually stand behind. If no,
you now know exactly which lesson in this module to reread — and where the deeper
engineering lives, one module away in
[Evals](../content/04-evals-observability/evals.md) and
[Observability](../content/04-evals-observability/observability.md).
