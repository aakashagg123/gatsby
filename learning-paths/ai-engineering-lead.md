# Learning path: AI Engineering Lead

*Part of [Learning paths](./README.md)*

*Last reviewed: 2026-10 · Volatility: medium*

## TL;DR

This path is the engineer path in short form, plus what a lead adds: economics, architecture review, governance, and working with product. You read for judgement. You skim the build lessons, so you can ask your team the right questions, and you read the decision lessons in full.

**Who it is for:** an engineering manager or tech lead who runs a team that builds AI systems.

**Outcome:** You review AI architecture, set quality and safety standards, control cost, and work well with product.

**Before you start:** Years of engineering and some time running a team. You may not have shipped an AI feature yet.

**Length:** about 33 hours, across 5 stages. The time is a rough estimate (see Under the hood).

**Terms:** a large language model (LLM) is a model like those behind chat assistants; the plural is large language models (LLMs).

> 🎯 **For the AI engineering lead**
>
> **Why it matters** — Your team will build what you can review. If you cannot read an architecture, an eval report or a threat model, you cannot lead the work.
>
> **What it changes in your decisions** — You set standards for evals, safety and cost before the build. You approve designs by their failure handling.
>
> **Ask your team** — *"Show me how this fails, how we would notice, and what it costs per request."*
>
> **Risk if ignored** — The team ships fast and unsafe. Review happens after an incident.

## The path at a glance

Each stage ends with a checkpoint. Move on when you can do what the checkpoint says.

| Stage | Focus | About |
| --- | --- | --- |
| 1 | How models behave and what they cost | about 5 hours (plus planned modules) |
| 2 | Architecture you can review | about 14 hours |
| 3 | Quality, safety and access | about 6 hours |
| 4 | Systems at scale | about 2.5 hours |
| 5 | Work with product and run the team | about 5.5 hours |

## Stage 1: How models behave and what they cost

Cost and latency come from model and serving choices. Know the levers. (about 5 hours plus the planned modules)

- **LLMs**: [1. What an LLM actually is](../llms/what-is-an-llm.md) · [2. The context window](../llms/the-context-window.md) · [3. Capabilities & the jagged frontier](../llms/capabilities-and-the-jagged-frontier.md) · [6. Choosing a model](../llms/choosing-a-model.md) · [7. Prompting vs. RAG vs. fine-tuning](../llms/prompting-vs-rag-vs-finetuning.md)
- **Machine learning**: coming soon. A module on machine learning basics is planned. Skip this step until it is published.
- **AI engineering: inference internals**: [Prefill vs. decode latency](../content/01-inference-internals/prefill-vs-decode.md) · [Continuous batching & paged attention](../content/01-inference-internals/batching-and-paged-attention.md) · [Prompt caching vs. semantic caching](../content/01-inference-internals/prompt-vs-semantic-caching.md)
- **AI engineering: strategy & tradeoffs**: [Fine-tuning vs. in-context learning vs. RAG vs. distillation — and when each is the wrong tool](../content/06-strategy-tradeoffs/finetune-vs-icl-vs-rag.md) · [Latency, quality, cost, and reliability across the full inference stack](../content/06-strategy-tradeoffs/inference-stack-tradeoffs.md)
- **Cost optimization**: [1. The cost stack, and the build-vs-buy breakeven](../cost-optimization/the-cost-stack-and-the-build-vs-buy-breakeven.md) · [2. FinOps for AI: budgets, forecasting & the cost review](../cost-optimization/finops-budgets-forecasting-and-the-cost-review.md)

**Ready to move on when:** You can explain where a request's time and money go and name the three levers that change them.

## Stage 2: Architecture you can review

Know the shapes: grounding, context, memory, agents, workflows. Skim the build lessons. (about 14 hours)

- **RAG & vector databases**: [1. Why RAG?](../rag-vector-databases/why-rag.md) · [5. Retrieval quality](../rag-vector-databases/retrieval-quality.md) · [6. RAG vs. long-context vs. fine-tuning](../rag-vector-databases/rag-vs-long-context-vs-finetuning.md)
- **Context engineering**: [1. What is context engineering, for a product leader?](../context-engineering/what-is-context-engineering.md) · [3. The anatomy of a context pipeline](../context-engineering/the-anatomy-of-a-context-pipeline.md) · [5. Context governance at scale](../context-engineering/context-governance-at-scale.md)
- **Memory & context**: [1. Memory as a product decision](../memory-and-context/memory-as-a-product-decision.md) · [5. When memory goes wrong](../memory-and-context/when-memory-goes-wrong.md)
- **AI agents**: [1. What an agent is, and how much autonomy it needs](../ai-agents/what-an-agent-is-and-how-much-autonomy-it-needs.md) · [3. When not to build an agent](../ai-agents/when-not-to-build-an-agent.md) · [4. Running an agent in production](../ai-agents/running-an-agent-in-production.md)
- **Agentic workflows**: [1. Choosing a workflow pattern](../agentic-workflows/choosing-a-workflow-pattern.md) · [2. Orchestrating more than one agent](../agentic-workflows/orchestrating-more-than-one-agent.md) · [3. Making a workflow durable, and worth owning](../agentic-workflows/making-a-workflow-durable-and-worth-owning.md)
- **Harness engineering**: [Phase 01 — Foundations and the Loop](../harness-engineering/phases/01-foundations-and-the-loop/README.md) (5 lessons, skim it)
- **Harness engineering**: [Phase 06 — Permissions and Security](../harness-engineering/phases/06-permissions-and-security/README.md) (4 lessons, skim it)
- **Harness engineering**: [Phase 07 — Planning and Subagents](../harness-engineering/phases/07-planning-and-subagents/README.md) (4 lessons, skim it)
- **Harness engineering**: [Phase 09 — Reliability, evals, and ops](../harness-engineering/phases/09-reliability-evals-and-ops/README.md) (5 lessons, skim it)

**Ready to move on when:** You can review a design doc for an agent: its loop, tools, permissions, budgets and failure handling.

## Stage 3: Quality, safety and access

Set the standards. Evals, threat models and access control are yours to require. (about 6 hours)

- **Evaluation & observability**: [1. Why eval investment is the job](../evaluation-and-observability/why-eval-investment-is-the-job.md) · [2. Building the eval stack in the right order](../evaluation-and-observability/building-the-eval-stack-in-the-right-order.md)
- **AI engineering: evals & observability**: [Evals: golden sets, regression tests, adversarial tests, LLM-as-judge, and human evals](../content/04-evals-observability/evals.md) · [LLM observability: traces, spans, tokens, latency, errors, and drift](../content/04-evals-observability/observability.md)
- **AI security & guardrails**: [1. The threat model, and guardrails as architecture](../ai-security-and-guardrails/the-threat-model-and-guardrails.md) · [2. Red-teaming: testing your defenses](../ai-security-and-guardrails/red-teaming-and-proving-your-defenses.md) · [3. Governance, audit & compliance](../ai-security-and-guardrails/governance-audit-and-compliance.md)
- **Access control**: [1. Authentication, authorization and the access-control model](../access-control/authentication-authorization-and-the-access-control-model.md) · [2. OAuth 2.0, OpenID Connect and tokens](../access-control/oauth-openid-connect-and-tokens.md) · [5. ReBAC and policy engines](../access-control/rebac-and-policy-engines.md) · [8. Access control for AI agents](../access-control/access-control-for-ai-agents.md)
- **AI engineering: safety & multi-tenancy**: [Safety engineering: prompt injection defense, data leakage prevention, and permission boundaries](../content/05-safety-multitenancy/safety-engineering.md) · [Multi-tenant isolation, cache safety, and cross-user context contamination prevention](../content/05-safety-multitenancy/multi-tenant-isolation.md)
- **AI engineering: strategy & tradeoffs**: [Production failure modes & how to engineer around them](../content/06-strategy-tradeoffs/production-failure-modes.md)

**Ready to move on when:** You can name the release gate for an AI feature, who owns it, and what evidence a buyer would ask for.

## Stage 4: Systems at scale

AI features still run on ordinary systems. Hold the same bar for reliability. (about 2.5 hours)

- **System design**: [1. Foundations & framework](../system-design/foundations-and-framework.md) · [2. Core building blocks](../system-design/core-building-blocks.md) · [3. Web-scale services](../system-design/web-scale-services.md) · [7. Data infrastructure](../system-design/data-infrastructure.md)
- **Technical product sense**: [5. Reliability & failure](../technical-product-sense/reliability-and-failure.md) · [8. The economics of infrastructure](../technical-product-sense/economics-of-infrastructure.md)

**Ready to move on when:** You can run a design review for scale, failure and cost on any service in the stack.

## Stage 5: Work with product and run the team

Turn standards into process: specs, launches, incidents and how product and engineering share ownership. (about 5.5 hours)

- **Technical product management**: [3. Specs, PRDs & RFCs](../technical-product-management/specs-prds-and-rfcs.md) · [4. Prioritization & roadmaps](../technical-product-management/prioritization-and-roadmaps.md) · [5. Working with engineering](../technical-product-management/working-with-engineering.md) · [6. Metrics & experimentation](../technical-product-management/metrics-and-experimentation.md) · [7. Launches, rollouts & migrations](../technical-product-management/launches-rollouts-and-migrations.md) · [8. Incidents & postmortems](../technical-product-management/incidents-and-postmortems.md) · [9. Technical product management for AI](../technical-product-management/tpm-for-ai-products.md)
- **Product sense**: [7. Product sense for AI products](../product-sense/product-sense-for-ai.md)
- **Knowledge graphs**: [1. What is a knowledge graph?](../knowledge-graphs/what-is-a-knowledge-graph.md) · [8. Knowledge graphs as a product](../knowledge-graphs/knowledge-graphs-as-a-product.md)
- **Flowable**: [Process automation from scratch](../flowable/README.md) (read the overview and the concept lessons)

**Ready to move on when:** You and your PM share one definition of done, one quality bar and one incident process.

## Skip-ahead rules

- If you came from machine learning, skip the first stage's model lessons and read the cost lessons.
- If your team already runs evals in CI, read the evaluation lessons as a gap check.
- If you want hands-on depth, add the build lessons from the AI Engineer path.

## Worked example: a week-by-week plan

*This example is invented, to show the method.*

An AI engineering lead with three hours a week spreads the path over 5 weeks. Each week ends with something you can show.

| Week | Stage | What you do |
| --- | --- | --- |
| 1 | Stage 1 | Pull one month of cost and latency numbers for your busiest model call. Find the biggest lever. |
| 2 | Stage 2 | Review one agent design doc against the loop, tools, permissions and budget. |
| 3 | Stage 3 | Write the release gate for one feature and name its owner. |
| 4 | Stage 4 | Run a failure review on one service. |
| 5 | Stage 5 | Agree a definition of done with your PM. |

## Tradeoffs

- **Judgement vs. hands-on skill.** Skimming the build lessons keeps you fast. It also means you rely on your team's account of how things fail.
- **Standards first vs. build first.** Standards slow the first feature and speed the next ten.
- **One path vs. two.** Pair this path with the engineer path if you still write code.

## Failure modes

- **Approving by demo.** Review by failure handling, not by the happy path.
- **No owner for the eval set.** An eval set with no owner decays.
- **Treating safety as a security-team task.** Product and engineering own the design that makes it hold.
- **Skipping the economics.** Cost surprises arrive after launch.

## Practitioner checklist

- [ ] Do we have a written release gate for each AI feature?
- [ ] Does every agent design show permissions, budgets and a kill switch?
- [ ] Do we track cost and latency per request?
- [ ] Do we have an incident process that covers model failures?
- [ ] Do product and engineering share one quality bar?

## Under the hood: how this path was built

Lesson links come from the track build configs, so a renamed lesson is caught by the link check. Time is the number of lessons times 25 minutes for a reading lesson, times 60 minutes for a harness lesson that you build, and 120 minutes to skim a harness phase. Add time for exercises. Modules marked "coming soon" are planned and not counted.

## Related lessons

- [AI Engineer path](./ai-engineer.md)
- [AI Product Lead path](./ai-product-lead.md)
- [Choose your path](./README.md)
- [Recap: paths compared](./recap.md)

## Sources

Lesson counts and titles come from the track overview pages and build configs in this repository. The time estimates are this course's rule of thumb, not measured results. The week plan is invented.
