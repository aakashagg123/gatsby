# Learning path: AI Engineer

*Part of [Learning paths](./README.md)*

*Last reviewed: 2026-10 · Volatility: medium*

## TL;DR

This path is build-first. It starts with how models learn, then moves through models and APIs, grounding and memory, agents and the harness, and production. It is the longest path. The harness track is the core: you build a coding agent's parts by hand and end with a tested capstone.

**Who it is for:** a software engineer who builds AI-powered systems.

**Outcome:** You can build, test and run a retrieval-backed, tool-using agent, and explain how it fails.

**Before you start:** Comfortable Python and one backend stack. Basic linear algebra helps. The foundations stage covers what you need.

**Length:** about 68 hours, across 5 stages. The time is a rough estimate (see Under the hood).

**Terms:** a large language model (LLM) is a model like those behind chat assistants; the plural is large language models (LLMs); convolutional neural networks (CNNs) are a model type built for images; Extensible Markup Language (XML) is a tag-based text format.

> 🎯 **For the AI engineer**
>
> **Why it matters** — Calling an API is easy. Making the result reliable, safe and affordable is the job.
>
> **What it changes in your decisions** — You test before you tune. You put checks in code, not in prompts. You design for failure first.
>
> **Ask yourself** — *"If this step returns garbage, what stops it from doing damage?"*
>
> **Risk if ignored** — The demo works. Production loops, leaks or overspends, and nobody can say why.

## The path at a glance

Each stage ends with a checkpoint. Move on when you can do what the checkpoint says.

| Stage | Focus | About |
| --- | --- | --- |
| 1 | Foundations | about 1 hour (plus planned modules) |
| 2 | Models and APIs | about 6.5 hours |
| 3 | Grounding and memory | about 5 hours |
| 4 | Agents and the harness (build it) | about 29 hours |
| 5 | Production | about 26 hours |

## Stage 1: Foundations

Learn how a model is trained and what its data looks like. Everything later builds on it. (about 1 hour plus the planned modules)

- **Machine learning**: coming soon. A module on machine learning basics is planned. Skip this step until it is published.
- **Tensors**: coming soon. Shapes, broadcasting and batching. Planned.
- **CNNs**: coming soon. Optional branch for vision. Planned.
- **LLMs**: [1. What an LLM actually is](../llms/what-is-an-llm.md) · [2. The context window](../llms/the-context-window.md) · [5. Temperature, sampling & determinism](../llms/temperature-sampling-and-determinism.md)

**Ready to move on when:** You can explain what a token and a context window are, and how sampling changes the output. Until the machine learning module ships, add a training-loop primer of your own.

## Stage 2: Models and APIs

Call models well: contracts, streaming, retries, structured output and prompts that hold up. (about 6.5 hours)

- **LLMs**: [3. Capabilities & the jagged frontier](../llms/capabilities-and-the-jagged-frontier.md) · [6. Choosing a model](../llms/choosing-a-model.md) · [7. Prompting vs. RAG vs. fine-tuning](../llms/prompting-vs-rag-vs-finetuning.md)
- **APIs & integrations**: [1. The request/response contract](../api-integrations/the-request-response-contract.md) · [2. Calling an LLM API](../api-integrations/calling-an-llm-api.md) · [3. Structured output & JSON mode](../api-integrations/structured-output-and-json-mode.md) · [4. Webhooks & async patterns](../api-integrations/webhooks-and-async-patterns.md) · [5. Integrating into existing systems](../api-integrations/integrating-into-existing-systems.md) · [6. MCP & standard connectors](../api-integrations/mcp-and-standard-connectors.md)
- **Prompt engineering**: [2. The anatomy of a prompt](../prompt-engineering/the-anatomy-of-a-prompt.md) · [4. Structured prompting: XML, delimiters, scaffolds](../prompt-engineering/structured-prompting.md) · [5. Few-shot, chain-of-thought, and self-consistency](../prompt-engineering/few-shot-cot-self-consistency.md) · [6. Prompt chaining and multi-step workflows](../prompt-engineering/prompt-chaining-and-workflows.md) · [7. Prompting for tools and agents](../prompt-engineering/prompting-for-tools-and-agents.md) · [9. When prompts fail: the diagnostic playbook](../prompt-engineering/when-prompts-fail.md) · [10. Prompts in production: versioning, testing, and model upgrades](../prompt-engineering/prompts-in-production.md)

**Ready to move on when:** You can call a model with retries and a typed output, and you can diagnose a failing prompt.

## Stage 3: Grounding and memory

Give the model the right data, in the right shape, at the right time. (about 5 hours)

- **RAG & vector databases**: [1. Why RAG?](../rag-vector-databases/why-rag.md) · [2. Embeddings & semantic search](../rag-vector-databases/embeddings-and-semantic-search.md) · [3. Vector databases](../rag-vector-databases/vector-databases.md) · [4. Chunking & ingestion](../rag-vector-databases/chunking-and-ingestion.md) · [5. Retrieval quality](../rag-vector-databases/retrieval-quality.md) · [7. Beyond flat RAG: GraphRAG & structured retrieval](../rag-vector-databases/graphrag-and-structured-retrieval.md)
- **AI engineering: RAG**: [RAG architecture: chunking, embeddings, hybrid search, reranking, and freshness](../content/03-rag/rag-architecture.md) · [Retrieval evals: recall, precision, grounding, attribution, and citation quality](../content/03-rag/retrieval-evals.md)
- **Memory & context**: [3. Writing and maintaining memory](../memory-and-context/writing-and-maintaining-memory.md) · [4. Retrieval as memory](../memory-and-context/retrieval-as-memory.md)
- **Context engineering**: [3. The anatomy of a context pipeline](../context-engineering/the-anatomy-of-a-context-pipeline.md) · [6. Evaluating context quality](../context-engineering/evaluating-context-quality.md)

**Ready to move on when:** You can build a retrieval pipeline and measure its quality with a test set.

## Stage 4: Agents and the harness (build it)

Build the parts of an agent by hand. This is the core of the path. (about 29 hours)

- **Tool calling**: [2. Tool contracts & reliability](../tool-calling/tool-contracts-and-reliability.md) · [3. Permissions, blast radius & the trust boundary](../tool-calling/permissions-blast-radius-and-the-trust-boundary.md)
- **AI engineering: reliable outputs**: [Function calling reliability, tool contracts, argument validation, and idempotency](../content/02-reliable-outputs/function-calling.md)
- **AI agents**: [2. Planning, reasoning & reliability across a run](../ai-agents/planning-reasoning-and-reliability-across-a-run.md)
- **Agentic workflows**: [1. Choosing a workflow pattern](../agentic-workflows/choosing-a-workflow-pattern.md) · [2. Orchestrating more than one agent](../agentic-workflows/orchestrating-more-than-one-agent.md) · [3. Making a workflow durable, and worth owning](../agentic-workflows/making-a-workflow-durable-and-worth-owning.md)
- **Harness engineering**: [Phase 01 — Foundations and the Loop](../harness-engineering/phases/01-foundations-and-the-loop/README.md) (5 lessons, build it)
- **Harness engineering**: [Phase 02 — Tools](../harness-engineering/phases/02-tools/README.md) (3 lessons, build it)
- **Harness engineering**: [Phase 03 — Context and memory](../harness-engineering/phases/03-context-and-memory/README.md) (5 lessons, build it)
- **Harness engineering**: [Phase 04 — Prompts and instructions](../harness-engineering/phases/04-prompts-and-instructions/README.md) (3 lessons, build it)
- **Harness engineering**: [Phase 05 — Files and Shell](../harness-engineering/phases/05-files-and-shell/README.md) (6 lessons, build it)
- **Harness engineering**: [Phase 06 — Permissions and Security](../harness-engineering/phases/06-permissions-and-security/README.md) (4 lessons, build it)

**Ready to move on when:** You have a working loop with tools, a permission gate and a context budget, and tests that fail when you break them.

## Stage 5: Production

Plan for failure: extend, test, observe, secure and scale. (about 26 hours)

- **Harness engineering**: [Phase 07 — Planning and Subagents](../harness-engineering/phases/07-planning-and-subagents/README.md) (4 lessons, build it)
- **Harness engineering**: [Phase 08 — Extending: MCP, Skills, Retrieval](../harness-engineering/phases/08-extending-mcp-skills-retrieval/README.md) (5 lessons, build it)
- **Harness engineering**: [Phase 09 — Reliability, evals, and ops](../harness-engineering/phases/09-reliability-evals-and-ops/README.md) (5 lessons, build it)
- **Harness engineering**: [Phase 10 — Capstone](../harness-engineering/phases/10-capstone/README.md) (1 lessons, build it). Allow about 3 hours: the capstone plus your own evals, traces and cost.
- **AI agents**: [4. Running an agent in production](../ai-agents/running-an-agent-in-production.md) · [5. Choosing and acceptance-testing an agent](../ai-agents/choosing-and-acceptance-testing-an-agent.md)
- **AI engineering: inference internals**: [Prefill vs. decode latency](../content/01-inference-internals/prefill-vs-decode.md) · [Continuous batching & paged attention](../content/01-inference-internals/batching-and-paged-attention.md) · [KV cache management: eviction, reuse, and memory pressure at scale](../content/01-inference-internals/kv-cache-management.md) · [Prompt caching vs. semantic caching](../content/01-inference-internals/prompt-vs-semantic-caching.md)
- **AI engineering: reliable outputs**: [Model routing, graceful fallback logic, and degraded-mode UX](../content/02-reliable-outputs/model-routing.md) · [Structured output: validation, repair loops, and fallback chains](../content/02-reliable-outputs/structured-output.md) · [Agent guardrails: loop budgets, tool budgets, and termination conditions](../content/02-reliable-outputs/agent-guardrails.md)
- **AI engineering: evals & observability**: [Evals: golden sets, regression tests, adversarial tests, LLM-as-judge, and human evals](../content/04-evals-observability/evals.md) · [LLM observability: traces, spans, tokens, latency, errors, and drift](../content/04-evals-observability/observability.md) · [Cost attribution per feature, workflow, tenant, and user journey — not just per model](../content/04-evals-observability/cost-attribution.md)
- **AI engineering: safety & multi-tenancy**: [Safety engineering: prompt injection defense, data leakage prevention, and permission boundaries](../content/05-safety-multitenancy/safety-engineering.md) · [Multi-tenant isolation, cache safety, and cross-user context contamination prevention](../content/05-safety-multitenancy/multi-tenant-isolation.md)
- **AI security & guardrails**: [1. The threat model, and guardrails as architecture](../ai-security-and-guardrails/the-threat-model-and-guardrails.md) · [2. Red-teaming: testing your defenses](../ai-security-and-guardrails/red-teaming-and-proving-your-defenses.md)
- **Access control**: [1. Authentication, authorization and the access-control model](../access-control/authentication-authorization-and-the-access-control-model.md) · [2. OAuth 2.0, OpenID Connect and tokens](../access-control/oauth-openid-connect-and-tokens.md) · [8. Access control for AI agents](../access-control/access-control-for-ai-agents.md)
- **System design**: [1. Foundations & framework](../system-design/foundations-and-framework.md) · [2. Core building blocks](../system-design/core-building-blocks.md) · [7. Data infrastructure](../system-design/data-infrastructure.md)

**Ready to move on when:** Your capstone passes its tests, and you can show its evals, traces, permission rules and cost.

## Skip-ahead rules

- If you know machine learning, skip the foundations stage and start at models and APIs.
- If you only work with hosted models, read the inference lessons as background and skip the deep ones.
- If you want a faster tour, build harness phases 1, 2, 3 and 6 and skim the rest.

## Worked example: a week-by-week plan

*This example is invented, to show the method.*

An AI engineer with nine hours a week spreads the path over 8 weeks. Each week ends with something you can show.

| Week | Stage | What you do |
| --- | --- | --- |
| 1 | Stage 2 | Call a model through an API with retries and a typed output. |
| 2 | Stage 3 | Add retrieval over your own documents and measure it with ten questions. |
| 3 | Stage 4 | Build harness phase 1: the loop. Run its asserts. |
| 4 | Stage 4 | Build harness phases 2 and 3: tools and context. |
| 5 | Stage 4 | Build harness phases 4 and 5: prompts, files and shell. |
| 6 | Stage 4 | Build harness phase 6: permissions and security. |
| 7 | Stage 5 | Build harness phases 7 and 8: planning, subagents and MCP. |
| 8 | Stage 5 | Build phase 9 and the capstone. Break the capstone on purpose and watch it fail. |

## Tradeoffs

- **Build vs. read.** The harness lessons ask you to type the code. Skimming saves time and loses the failures you would have hit.
- **Depth vs. breadth.** The inference lessons go deep on serving. Read them if you run models, skim them if you call hosted ones.
- **Frameworks vs. from scratch.** Building by hand first makes later framework choices easier to judge.

## Failure modes

- **Tuning before testing.** Build the eval set first. Tuning without one is guessing.
- **Checks in prompts.** A rule in a prompt is a request. A rule in code is a control.
- **Skipping the permission gate.** An agent without one is a security incident waiting for a trigger.
- **No failure tests.** Break your agent on purpose and watch the tests catch it.

## Practitioner checklist

- [ ] Does every model call have a timeout, a retry rule and a typed output?
- [ ] Do I have a test set for retrieval and for the agent?
- [ ] Is every tool call behind a permission check in code?
- [ ] Is there a budget on steps and cost?
- [ ] Can I trace one request from input to answer?

## Under the hood: how this path was built

Lesson links come from the track build configs, so a renamed lesson is caught by the link check. Time is the number of lessons times 25 minutes for a reading lesson, times 60 minutes for a harness lesson that you build, and 120 minutes to skim a harness phase. Add time for exercises. Modules marked "coming soon" are planned and not counted.

## Related lessons

- [AI Engineering Lead path](./ai-engineering-lead.md)
- [AI Product Lead path](./ai-product-lead.md)
- [Choose your path](./README.md)
- [Recap: paths compared](./recap.md)

## Sources

Lesson counts and titles come from the track overview pages and build configs in this repository. The time estimates are this course's rule of thumb, not measured results. The week plan is invented.
