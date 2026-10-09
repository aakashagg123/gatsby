# Learning path: AI Product Lead

*Part of [Learning paths](./README.md)*

*Last reviewed: 2026-10 · Volatility: medium*

## TL;DR

This path covers the layers between a model and a product: grounding, context, memory, tools, agents, workflows, trust and cost. It is wider and deeper than the Senior PM path. It stays at the decision level. You read enough mechanics to ask sharp questions, not to build.

**Who it is for:** a product leader who owns an AI product line or a team of PMs shipping AI features.

**Outcome:** You set direction for how the product grounds its answers, remembers, acts, stays safe and stays affordable. You can review a design with engineering and ask informed questions.

**Before you start:** This path builds on the Senior PM path, stages 1 to 3, or equivalent experience. Lessons marked ↺ repeat that path, so skip them if you did it. You have shipped or closely reviewed one AI feature.

**Length:** about 24 hours, across 5 stages. If you did the Senior PM path, about 14 hours, because lessons marked ↺ repeat it. The time is a rough estimate (see Under the hood).

**Terms:** a large language model (LLM) is a model like those behind chat assistants; the plural is large language models (LLMs).

> 🎯 **For the AI product lead**
>
> **Why it matters** — At this level your decisions set the architecture. A weak call on grounding or autonomy is expensive to reverse.
>
> **What it changes in your decisions** — You choose retrieval, memory and agent scope on purpose. You set the autonomy dial per task. You fund evals and guardrails as roadmap items.
>
> **Ask your eng team** — *"Which layer fails first, and how would we see it in production?"*
>
> **Risk if ignored** — You ship an agent with the wrong autonomy or a memory that leaks. You find out from a customer.

## The path at a glance

Each stage ends with a checkpoint. Move on when you can do what the checkpoint says.

| Stage | Focus | About |
| --- | --- | --- |
| 1 | Model and data foundations | about 6.5 hours (plus planned modules) |
| 2 | Context and memory | about 5 hours |
| 3 | Action: tools, agents, workflows | about 5.5 hours |
| 4 | Trust, access and cost | about 4 hours |
| 5 | Run the product | about 2.5 hours |

## Stage 1: Model and data foundations

You decide how the product grounds answers. That choice drives quality and cost. (about 6.5 hours plus the planned modules)

- **LLMs**: [1. What an LLM actually is](../llms/what-is-an-llm.md) ↺ · [2. The context window](../llms/the-context-window.md) ↺ · [3. Capabilities & the jagged frontier](../llms/capabilities-and-the-jagged-frontier.md) ↺ · [5. Temperature, sampling & determinism](../llms/temperature-sampling-and-determinism.md) ↺ · [6. Choosing a model](../llms/choosing-a-model.md) ↺ · [7. Prompting vs. RAG vs. fine-tuning](../llms/prompting-vs-rag-vs-finetuning.md) ↺
- **Generative AI**: [3. Probabilistic software](../generative-ai/probabilistic-software.md) ↺ · [4. The generative AI product stack](../generative-ai/the-genai-product-stack.md) ↺ · [5. Build, buy, or fine-tune](../generative-ai/build-buy-or-fine-tune.md) ↺
- **Machine learning**: coming soon. A module on machine learning basics is planned. Skip this step until it is published.
- **RAG & vector databases**: [1. Why RAG?](../rag-vector-databases/why-rag.md) ↺ · [5. Retrieval quality](../rag-vector-databases/retrieval-quality.md) ↺ · [6. RAG vs. long-context vs. fine-tuning](../rag-vector-databases/rag-vs-long-context-vs-finetuning.md) ↺ · [7. Beyond flat RAG: GraphRAG & structured retrieval](../rag-vector-databases/graphrag-and-structured-retrieval.md)
- **Knowledge graphs**: [1. What is a knowledge graph?](../knowledge-graphs/what-is-a-knowledge-graph.md) · [6. Knowledge graphs & LLMs](../knowledge-graphs/knowledge-graphs-and-llms.md) · [8. Knowledge graphs as a product](../knowledge-graphs/knowledge-graphs-as-a-product.md)

**Ready to move on when:** You can compare prompting, retrieval and fine-tuning for a feature and pick one with reasons.

## Stage 2: Context and memory

What the model sees is a product decision. So is what it remembers. (about 5 hours)

- **Context engineering**: [1. What is context engineering, for a product leader?](../context-engineering/what-is-context-engineering.md) · [3. The anatomy of a context pipeline](../context-engineering/the-anatomy-of-a-context-pipeline.md) · [4. Context as a spec-able requirement](../context-engineering/context-as-a-spec-able-requirement.md) · [5. Context governance at scale](../context-engineering/context-governance-at-scale.md) · [6. Evaluating context quality](../context-engineering/evaluating-context-quality.md) · [7. Context engineering across the product lifecycle](../context-engineering/context-across-the-product-lifecycle.md)
- **Memory & context**: [1. Memory as a product decision](../memory-and-context/memory-as-a-product-decision.md) ↺ · [2. Session, user & organizational memory](../memory-and-context/session-user-and-organizational-memory.md) · [3. Writing and maintaining memory](../memory-and-context/writing-and-maintaining-memory.md) · [4. Retrieval as memory](../memory-and-context/retrieval-as-memory.md) · [5. When memory goes wrong](../memory-and-context/when-memory-goes-wrong.md) ↺
- **Prompt engineering**: [10. Prompts in production: versioning, testing, and model upgrades](../prompt-engineering/prompts-in-production.md)

**Ready to move on when:** You can write the context spec for a feature: sources, owners, freshness and how quality is measured.

## Stage 3: Action: tools, agents, workflows

The line between talking and doing carries the most risk and the most value. (about 5.5 hours)

- **Tool calling**: [1. What tool calling is](../tool-calling/what-tool-calling-is.md) ↺ · [2. Tool contracts & reliability](../tool-calling/tool-contracts-and-reliability.md) · [3. Permissions, blast radius & the trust boundary](../tool-calling/permissions-blast-radius-and-the-trust-boundary.md)
- **AI agents**: [1. What an agent is, and how much autonomy it needs](../ai-agents/what-an-agent-is-and-how-much-autonomy-it-needs.md) · [2. Planning, reasoning & reliability across a run](../ai-agents/planning-reasoning-and-reliability-across-a-run.md) · [3. When not to build an agent](../ai-agents/when-not-to-build-an-agent.md) · [4. Running an agent in production](../ai-agents/running-an-agent-in-production.md) · [5. Choosing and acceptance-testing an agent](../ai-agents/choosing-and-acceptance-testing-an-agent.md)
- **Agentic workflows**: [1. Choosing a workflow pattern](../agentic-workflows/choosing-a-workflow-pattern.md) · [2. Orchestrating more than one agent](../agentic-workflows/orchestrating-more-than-one-agent.md) · [3. Making a workflow durable, and worth owning](../agentic-workflows/making-a-workflow-durable-and-worth-owning.md)
- **Agentic AI**: [6. Reliability & evals](../agentic-ai/reliability-and-evals.md) · [8. Agentic AI as a product](../agentic-ai/agentic-ai-as-a-product.md) ↺

**Ready to move on when:** You can set the autonomy level for a task, justify it, and say what would make you lower it.

## Stage 4: Trust, access and cost

Evals, security, permissions and spend decide whether the feature survives contact with real use. (about 4 hours)

- **Evaluation & observability**: [1. Why eval investment is the job](../evaluation-and-observability/why-eval-investment-is-the-job.md) ↺ · [2. Building the eval stack in the right order](../evaluation-and-observability/building-the-eval-stack-in-the-right-order.md) ↺
- **AI security & guardrails**: [1. The threat model, and guardrails as architecture](../ai-security-and-guardrails/the-threat-model-and-guardrails.md) ↺ · [2. Red-teaming: testing your defenses](../ai-security-and-guardrails/red-teaming-and-proving-your-defenses.md) · [3. Governance, audit & compliance](../ai-security-and-guardrails/governance-audit-and-compliance.md) ↺
- **Access control**: [1. Authentication, authorization and the access-control model](../access-control/authentication-authorization-and-the-access-control-model.md) · [8. Access control for AI agents](../access-control/access-control-for-ai-agents.md)
- **Cost optimization**: [1. The cost stack, and the build-vs-buy breakeven](../cost-optimization/the-cost-stack-and-the-build-vs-buy-breakeven.md) ↺ · [2. FinOps for AI: budgets, forecasting & the cost review](../cost-optimization/finops-budgets-forecasting-and-the-cost-review.md) ↺
- **Technical product sense**: [8. The economics of infrastructure](../technical-product-sense/economics-of-infrastructure.md)

**Ready to move on when:** You can show a reviewer your eval results, your threat model and your cost per task.

## Stage 5: Run the product

Turn the above into specs, launches and a response plan. (about 2.5 hours)

- **Technical product management**: [3. Specs, PRDs & RFCs](../technical-product-management/specs-prds-and-rfcs.md) · [6. Metrics & experimentation](../technical-product-management/metrics-and-experimentation.md) · [7. Launches, rollouts & migrations](../technical-product-management/launches-rollouts-and-migrations.md) · [8. Incidents & postmortems](../technical-product-management/incidents-and-postmortems.md) · [9. Technical product management for AI](../technical-product-management/tpm-for-ai-products.md) ↺
- **Product sense**: [7. Product sense for AI products](../product-sense/product-sense-for-ai.md) ↺

**Ready to move on when:** You can write the spec, the launch gate and the incident plan for an AI feature.

## Skip-ahead rules

- If you ran the Senior PM path, skip the LLMs and generative AI lessons you have already read.
- If your product has no agents yet, read the agent lessons in stage 3 as risk reading, not as design reading.
- If you do not work with regulated customers, skim the governance lesson.

## Worked example: a week-by-week plan

*This example is invented, to show the method.*

An AI product lead with four hours a week spreads the path over 6 weeks. Each week ends with something you can show.

| Week | Stage | What you do |
| --- | --- | --- |
| 1 | Stage 1 | Pick one feature and write which of prompting, retrieval or fine-tuning it should use. |
| 2 | Stage 2 | Write its context spec. |
| 3 | Stage 2 | Review its memory design with a privacy owner. |
| 4 | Stage 3 | Set its autonomy level and the trigger to lower it. |
| 5 | Stage 4 | Run a tabletop review of its threat model, evals and cost. |
| 6 | Stage 5 | Write the launch gate and incident plan. |

## Tradeoffs

- **Coverage vs. time.** This is a long path. Each stage ends with a checkpoint, so you can stop at the layer you own.
- **Product depth vs. engineering depth.** You read mechanics only to ask better questions. The engineer path covers building.
- **Standards vs. speed.** Stage 4 slows early work and speeds later work.

## Failure modes

- **Treating agents as the default.** Read "when not to build an agent" before you commit.
- **Memory without a privacy owner.** Memory is a data product with a retention policy.
- **No eval owner.** Every layer in this path needs a quality measure and a person who owns it.
- **Reading without reviewing.** Take each stage to a real design review.

## Practitioner checklist

- [ ] Does every AI feature have a grounding choice with a written reason?
- [ ] Is there a context spec for each feature?
- [ ] Is the autonomy level of each agent written down?
- [ ] Can I show evals, a threat model and a cost per task for each feature?
- [ ] Is there a launch gate and an incident plan?

## Under the hood: how this path was built

Lesson links come from the track build configs, so a renamed lesson is caught by the link check. Time is the number of lessons times 25 minutes for a reading lesson, times 60 minutes for a harness lesson that you build, and 120 minutes to skim a harness phase. Add time for exercises. Modules marked "coming soon" are planned and not counted.

## Related lessons

- [Senior PM path](./senior-product-manager.md)
- [AI Engineering Lead path](./ai-engineering-lead.md)
- [Choose your path](./README.md)
- [Recap: paths compared](./recap.md)

## Sources

Lesson counts and titles come from the track overview pages and build configs in this repository. The time estimates are this course's rule of thumb, not measured results. The week plan is invented.
