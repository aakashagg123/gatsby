# Learning path: Senior Product Manager

*Part of [Learning paths](./README.md)*

*Last reviewed: 2026-10 · Volatility: medium*

## TL;DR

This path takes a working product manager from "AI is a black box" to "I can make the calls only the PM can make." It starts with a technical footing, adds plain-language model literacy, and then spends most of its time on four decisions: build, buy or fine-tune; the quality bar; the cost; and the risk. It skips engineering internals on purpose.

**Who it is for:** a product manager with several years of experience who is starting to own AI features.

**Outcome:** You can lead an AI feature end to end. You choose the approach, set the quality bar, price it, and judge the risk.

**Before you start:** Several years in product. No machine learning background is needed.

**Length:** about 16.5 hours, across 4 stages. The time is a rough estimate (see Under the hood).

**Terms:** a large language model (LLM) is a model like those behind chat assistants; the plural is large language models (LLMs); machine learning (ML) is the practice of training models from data.

> 🎯 **For the senior product manager**
>
> **Why it matters** — AI features fail in ways ordinary features do not. A PM who cannot read a quality report or a cost line cannot steer.
>
> **What it changes in your decisions** — You ask for an eval plan before a build starts. You ask for cost per task before a launch. You treat risk as a spec section.
>
> **Ask your eng team** — *"What does a bad answer look like, how often does it happen, and how would we know?"*
>
> **Risk if ignored** — You ship on a demo. The first real users find the failure modes, and the team has no way to measure them.

## The path at a glance

Each stage ends with a checkpoint. Move on when you can do what the checkpoint says.

| Stage | Focus | About |
| --- | --- | --- |
| 1 | Technical footing | about 2 hours |
| 2 | AI literacy | about 6.5 hours |
| 3 | The decisions only you own | about 4.5 hours |
| 4 | Go deeper where your product needs it (optional) | about 3.5 hours |

## Stage 1: Technical footing

AI products sit on ordinary systems. You need the same words your engineers use. (about 2 hours)

- **Technical product sense**: [1. How systems are built](../technical-product-sense/how-systems-are-built.md) · [2. APIs & contracts](../technical-product-sense/apis-and-contracts.md) · [4. Latency, scale & performance](../technical-product-sense/latency-scale-performance.md) · [5. Reliability & failure](../technical-product-sense/reliability-and-failure.md) · [9. Technical sense for AI systems](../technical-product-sense/technical-sense-for-ai.md)

**Ready to move on when:** You can explain a request path, an API contract and where latency comes from. You can name what changes when one component is a model.

## Stage 2: AI literacy

Learn what a model is, what it does well, and what it does badly. Plain language, no maths. (about 6.5 hours)

- **Machine learning**: [1. What machine learning is, and when to use it](../machine-learning/what-machine-learning-is.md) · [2. Data: features, labels, splits and leakage](../machine-learning/data-features-labels-and-leakage.md) · [5. Measuring a model: metrics, thresholds and baselines](../machine-learning/measuring-a-model.md)
- **Generative AI**: [1. What makes AI "generative"?](../generative-ai/what-is-generative-ai.md) · [2. The five modalities](../generative-ai/the-modalities.md) · [3. Probabilistic software](../generative-ai/probabilistic-software.md) · [4. The generative AI product stack](../generative-ai/the-genai-product-stack.md)
- **LLMs**: [1. What an LLM actually is](../llms/what-is-an-llm.md) · [2. The context window](../llms/the-context-window.md) · [3. Capabilities & the jagged frontier](../llms/capabilities-and-the-jagged-frontier.md) · [5. Temperature, sampling & determinism](../llms/temperature-sampling-and-determinism.md) · [6. Choosing a model](../llms/choosing-a-model.md)
- **Prompt engineering**: [1. What prompt engineering actually is](../prompt-engineering/what-prompt-engineering-actually-is.md) · [2. The anatomy of a prompt](../prompt-engineering/the-anatomy-of-a-prompt.md) · [7. Prompting for tools and agents](../prompt-engineering/prompting-for-tools-and-agents.md) · [9. When prompts fail: the diagnostic playbook](../prompt-engineering/when-prompts-fail.md)

**Ready to move on when:** You can say why the same prompt gives different answers, what a context window limits, and when a bad result is a prompt problem and when it is not.

## Stage 3: The decisions only you own

Pick the approach, set the bar, count the cost, and accept the risk. (about 4.5 hours)

- **Generative AI**: [5. Build, buy, or fine-tune](../generative-ai/build-buy-or-fine-tune.md) · [6. Where generative AI creates and destroys value](../generative-ai/where-value-is-created-and-destroyed.md)
- **LLMs**: [7. Prompting vs. RAG vs. fine-tuning](../llms/prompting-vs-rag-vs-finetuning.md)
- **Product sense**: [7. Product sense for AI products](../product-sense/product-sense-for-ai.md)
- **Technical product management**: [9. Technical product management for AI](../technical-product-management/tpm-for-ai-products.md)
- **Evaluation & observability**: [1. Why eval investment is the job](../evaluation-and-observability/why-eval-investment-is-the-job.md) · [2. Building the eval stack in the right order](../evaluation-and-observability/building-the-eval-stack-in-the-right-order.md)
- **Cost optimization**: [1. The cost stack, and the build-vs-buy breakeven](../cost-optimization/the-cost-stack-and-the-build-vs-buy-breakeven.md) · [2. FinOps for AI: budgets, forecasting & the cost review](../cost-optimization/finops-budgets-forecasting-and-the-cost-review.md)
- **AI security & guardrails**: [1. The threat model, and guardrails as architecture](../ai-security-and-guardrails/the-threat-model-and-guardrails.md) · [3. Governance, audit & compliance](../ai-security-and-guardrails/governance-audit-and-compliance.md)

**Ready to move on when:** You can write a one-page case for build, buy or fine-tune. It has an eval plan, a cost per task and the top three risks.

## Stage 4: Go deeper where your product needs it (optional)

Read only what your roadmap touches. Retrieval, memory and agents each change the product shape. (about 3.5 hours)

- **RAG & vector databases**: [1. Why RAG?](../rag-vector-databases/why-rag.md) · [5. Retrieval quality](../rag-vector-databases/retrieval-quality.md) · [6. RAG vs. long-context vs. fine-tuning](../rag-vector-databases/rag-vs-long-context-vs-finetuning.md)
- **Memory & context**: [1. Memory as a product decision](../memory-and-context/memory-as-a-product-decision.md) · [5. When memory goes wrong](../memory-and-context/when-memory-goes-wrong.md)
- **Agentic AI**: [1. What is an agent?](../agentic-ai/what-is-an-agent.md) · [8. Agentic AI as a product](../agentic-ai/agentic-ai-as-a-product.md)
- **Tool calling**: [1. What tool calling is](../tool-calling/what-tool-calling-is.md)

**Ready to move on when:** You can tell when a feature needs retrieval, memory or an agent, and when it does not.

## Skip-ahead rules

- If you have shipped an ML-backed feature, skip stage 1 and start stage 2 at the LLMs lessons.
- If a launch is close, start at stage 3. Read `What an LLM actually is` and `The context window` first, because the decision lessons assume them.
- If your product is not agentic, skip the agent lessons in stage 4.
- If you already run evals with your team, read the two evaluation lessons as a check, not as new material.

## Worked example: a week-by-week plan

*This example is invented, to show the method.*

A senior PM with three hours a week plans 6 weeks of work. Each week ends with something you can show. At this pace the full path (about 16.5 hours) takes about 6 weeks.

| Week | Stage | What you do |
| --- | --- | --- |
| 1 | Stage 1 | Write a one-page request path for your product, marking where a model would sit. |
| 2 | Stage 2 | Take one bad model answer from your own product and explain it using the LLM lessons. |
| 3 | Stage 3 (decisions) | Draft the build, buy or fine-tune case for one feature. |
| 4 | Stage 3 (quality and cost) | Add an eval plan and a cost per task to the draft. |
| 5 | Stage 3 (risk) | List the top three risks and the guardrail for each. Review with your engineering lead. |
| 6 | Stage 4 | Pick the one deep topic your roadmap needs and read it. |

## Tradeoffs

- **Breadth vs. depth.** This path reads many tracks shallowly. You gain vocabulary. You do not gain engineering skill, and that is the point.
- **Order vs. urgency.** If a launch is close, jump to stage 3 and come back. The checkpoints tell you what you missed.
- **Reading vs. doing.** The decisions stage only works if you apply it to a real feature.

## Failure modes

- **Reading the whole library.** The path picks lessons within tracks. Do not read every lesson in every track.
- **Stopping at stage 2.** Literacy without the decisions stage leaves you able to talk about AI but not to steer it.
- **Skipping evaluation.** The most common gap is shipping with no way to measure quality.
- **Reading in a vacuum.** Apply each stage to a real feature or the knowledge fades.

## Practitioner checklist

- [ ] Can I explain how our feature works to a new engineer without saying "the AI does it"?
- [ ] Is there an eval plan with a named owner?
- [ ] Do I know the cost per task, and what happens to it at ten times the traffic?
- [ ] Have I listed the top three risks and a guardrail for each?
- [ ] Do I know which of retrieval, memory and agents our product needs?

## Under the hood: how this path was built

Lesson links come from the track build configs, so a renamed lesson is caught by the link check. Time is the number of lessons times 25 minutes for a reading lesson, times 60 minutes for a harness lesson that you build, and 120 minutes to skim a harness phase. Add time for exercises. Modules marked "coming soon" are planned and not counted.

## Related lessons

- [AI Product Lead path](./ai-product-lead.md)
- [AI Engineering Lead path](./ai-engineering-lead.md)
- [Choose your path](./README.md)
- [Recap: paths compared](./recap.md)

## Sources

Lesson counts and titles come from the track overview pages and build configs in this repository. The time estimates are this course's rule of thumb, not measured results. The week plan is invented.
