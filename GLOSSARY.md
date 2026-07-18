# Glossary

Quick definitions for terms used across the curriculum. Each entry links to the
lesson where it is developed in depth.

---

**A2A (Agent2Agent)** — A protocol (Google-initiated, Linux Foundation) for agents advertising
capabilities and delegating to each other across vendors; early but real. See
[Multi-agent systems & protocols](./agentic-ai/multi-agent-and-protocols.md).

**Agent loop** — Gather context → decide → act → observe → repeat until the goal is met
or a budget is hit; the core structure of every agent. See
[What is an agent?](./agentic-ai/what-is-an-agent.md).

**AI-native (vs. AI-enabled)** — An AI-enabled product bolts a model onto an
existing product; an AI-native product is built around the model, such that
without it there is no product. The test: turn the model off — what's left? See
[Product sense for AI products](./product-sense/product-sense-for-ai.md).

**Attribution** — Linking a generated claim back to the specific source
passage that supports it. See [Retrieval evals](./content/03-rag/retrieval-evals.md).

**Autonomy spectrum** — The range from a single LLM call through workflows and routers
to fully autonomous agents; the first agent design decision is how little autonomy
suffices. See [What is an agent?](./agentic-ai/what-is-an-agent.md).

**AWQ (Activation-aware Weight Quantization)** — A 4-bit weight quantization
method that protects the small fraction of weights tied to high-magnitude
activations, preserving quality better than naive rounding. See
[Quantization formats](./content/01-inference-internals/quantization-formats.md).

**Axial coding** — Clustering free-form failure labels from open coding into a
recurring-failure taxonomy — the second step of error analysis. See
[Evals](./content/04-evals-observability/evals.md).

**Behaviour equation (Fogg)** — Behaviour = Motivation × Ability × Trigger; a behaviour
happens when all three are present at once. See
[Motivation & behaviour](./product-sense/motivation-and-behaviour.md).

**Comb-shaped expertise** — Several deep spikes over a broad base — the mature form of
T-shaped range; the polymath's profile. See
[Becoming a polymath](./first-principles/becoming-a-polymath.md).

**Compaction** — Summarizing the oldest conversation turns to reclaim context-window
space while preserving decisions and constraints. See
[Context & memory](./agentic-ai/context-and-memory.md).

**Context engineering** — Deliberately deciding what information occupies the
model's limited context window, in what order, and in what form. See
[Context engineering](./content/00-foundations/context-engineering.md).

**Continuous batching** — Adding and removing requests from a running inference
batch at the token level instead of waiting for a whole batch to finish. See
[Continuous batching & paged attention](./content/01-inference-internals/batching-and-paged-attention.md).

**Control point** — A workflow step you own whose outputs downstream work consumes —
the position from which scope expands and moats form. See
[TPM for AI products](./technical-product-management/tpm-for-ai-products.md).

**Data flywheel** — Usage → captured feedback → better evals and data → safer iteration →
better product → more usage; the compounding asset of an AI product. See
[TPM for AI products](./technical-product-management/tpm-for-ai-products.md).

**Data store** — Agent-platform term for a corpus provided in its original form
(PDFs, docs, databases, websites), vector-indexed so an agent can query it at
runtime — the standard implementation of RAG in agent stacks. See
[Context & memory](./agentic-ai/context-and-memory.md).

**Decode** — The autoregressive phase of generation that produces output tokens
one at a time; memory-bandwidth bound. See
[Prefill vs. decode](./content/01-inference-internals/prefill-vs-decode.md).

**Distillation** — Training a smaller "student" model to imitate a larger
"teacher" model's behavior. See
[Speculative decoding vs. quantization vs. distillation](./content/01-inference-internals/speculative-quantization-distillation.md).

**Drift** — Gradual degradation of system quality over time as inputs, data,
models, or dependencies change underneath you. See
[Observability](./content/04-evals-observability/observability.md).

**Error analysis** — Reading real traces, labeling failures free-form (open coding),
clustering them into a taxonomy (axial coding), and iterating — the discipline that
precedes metric-picking. See [Evals](./content/04-evals-observability/evals.md).

**Eval-driven development** — Making a graded example set the spec, regression suite, and
launch gate for an AI feature; no change ships without a score. See
[TPM for AI products](./technical-product-management/tpm-for-ai-products.md).

**Fermi estimation** — Decomposing an unknown quantity into guessable factors to derive
its order of magnitude from fundamentals. See
[The method](./first-principles/the-method.md).

**FP8** — An 8-bit floating-point format (E4M3 / E5M2) with hardware support on
newer GPUs; keeps a wider dynamic range than INT8. See
[Quantization formats](./content/01-inference-internals/quantization-formats.md).

**Function calling** — A model emitting a structured request to invoke a named
tool with typed arguments. See
[Function calling](./content/02-reliable-outputs/function-calling.md).

**Golden set** — A curated, version-controlled set of inputs with known-good
expected outputs, used as the backbone of regression testing. See
[Evals](./content/04-evals-observability/evals.md).

**GPTQ** — A one-shot post-training quantization method using approximate
second-order (Hessian) information to minimize layer-wise error. See
[Quantization formats](./content/01-inference-internals/quantization-formats.md).

**Grounding** — Whether a model's output is actually supported by the retrieved
context rather than its parametric memory. See
[Retrieval evals](./content/03-rag/retrieval-evals.md).

**Guardrail (production)** — An inline, blocking check on model output before the user
sees it — fast, cheap, fail-closed; the runtime twin of offline evaluators. See
[Observability](./content/04-evals-observability/observability.md).

**Harness** — The code, control flow, retries, validators, tools, and budgets
that surround the model call. See
[Harness engineering](./content/00-foundations/harness-engineering.md).

**Hook model** — Trigger → Action → Variable reward → Investment; the loop by which
products build habits. See
[Motivation & behaviour](./product-sense/motivation-and-behaviour.md).

**Hybrid search** — Combining lexical (BM25/keyword) and dense (vector) retrieval
to get the strengths of both. See [RAG architecture](./content/03-rag/rag-architecture.md).

**Idempotency** — A property where performing an operation multiple times has the
same effect as performing it once; essential for safely retrying tool calls. See
[Function calling](./content/02-reliable-outputs/function-calling.md).

**INT4 / INT8** — 4-bit and 8-bit integer quantization of weights (and sometimes
activations). See [Quantization formats](./content/01-inference-internals/quantization-formats.md).

**Inversion** — Solving a problem backward — ask how to guarantee failure, then design
against that list. See
[A latticework of mental models](./first-principles/mental-models-latticework.md).

**Jagged frontier** — The uneven boundary of model capability — brilliant at some hard
tasks, unreliable at some easy ones — which makes scoping a core product skill. See
[Product sense for AI](./product-sense/product-sense-for-ai.md).

**KV cache** — The stored key/value tensors for already-processed tokens that let
attention avoid recomputing the whole sequence each step. See
[KV cache management](./content/01-inference-internals/kv-cache-management.md).

**Leverage point** — A place in a system where a small, well-placed intervention
produces outsized change — e.g. changing a model's metric of success rather than
tuning its hyperparameters. See
[A latticework of mental models](./first-principles/mental-models-latticework.md).

**LLM-as-judge** — Using a model to score or compare outputs against a rubric. See
[Evals](./content/04-evals-observability/evals.md).

**Loop budget** — A hard cap on how many reasoning/acting iterations an agent may
take before it must stop or escalate. See
[Agent guardrails](./content/02-reliable-outputs/agent-guardrails.md).

**MCP (Model Context Protocol)** — The adopted standard for plugging tools and data
sources into agents — one server, any MCP-capable client. See
[Tools & function calling](./agentic-ai/tools-and-function-calling.md).

**Open coding** — Labeling observed failures in your own words, without a predefined
taxonomy — the first step of error analysis. See
[Evals](./content/04-evals-observability/evals.md).

**Orchestration layer** — The cyclical process governing how an agent takes in
information, reasons, and picks its next action — the loop plus its budgets and exits.
See [What is an agent?](./agentic-ai/what-is-an-agent.md).

**Paged attention** — Managing the KV cache in fixed-size non-contiguous blocks
(like OS virtual memory) to eliminate fragmentation. See
[Continuous batching & paged attention](./content/01-inference-internals/batching-and-paged-attention.md).

**Prefill** — The phase that processes all input/prompt tokens in parallel to
build the initial KV cache; compute bound. See
[Prefill vs. decode](./content/01-inference-internals/prefill-vs-decode.md).

**Prompt caching** — Reusing the computed KV cache for an *exact* shared prompt
prefix across requests. See
[Prompt vs. semantic caching](./content/01-inference-internals/prompt-vs-semantic-caching.md).

**Prompt injection** — Adversarial instructions smuggled into model input
(directly or via retrieved/tool content) to override intended behavior. See
[Safety engineering](./content/05-safety-multitenancy/safety-engineering.md).

**ReAct** — A reasoning framework interleaving thought, action, and observation —
the default shape of an agent loop, taught to a model with a few in-context
examples. See [Planning & reasoning](./agentic-ai/planning-and-reasoning.md).

**Repair loop** — Feeding a validation error back to the model so it can fix a
malformed output. See [Structured output](./content/02-reliable-outputs/structured-output.md).

**Reranking** — A second-stage model that re-scores retrieved candidates for
relevance before they enter the prompt. See [RAG architecture](./content/03-rag/rag-architecture.md).

**Second-order effects** — The consequences of the consequences — 'and then what?';
where first-order-obvious decisions age badly. See
[A latticework of mental models](./first-principles/mental-models-latticework.md).

**Semantic caching** — Returning a cached *response* when a new query is
semantically similar (by embedding distance) to a previous one. See
[Prompt vs. semantic caching](./content/01-inference-internals/prompt-vs-semantic-caching.md).

**Service-as-a-Software** — Delivering the outcome of a workflow (the resolved ticket,
the booked trip) rather than software the customer operates; enabled by LLMs absorbing
knowledge work and agents absorbing goal-seeking. See
[Agentic AI as a product](./agentic-ai/agentic-ai-as-a-product.md).

**Span** — A single timed unit of work inside a trace (a retrieval, a model call,
a tool execution). See [Observability](./content/04-evals-observability/observability.md).

**Speculative decoding** — Using a small draft model to propose tokens that the
large model verifies in parallel, accelerating decode without changing the output
distribution. See
[Speculative decoding vs. quantization vs. distillation](./content/01-inference-internals/speculative-quantization-distillation.md).

**Supervised cost per task** — Agent cost per task plus the human checking cost plus the
expected cost of misses — the honest number an agent must beat against the old way of
working. See [Agentic AI as a product](./agentic-ai/agentic-ai-as-a-product.md).

**T-shaped expertise** — One deep spike of mastery over a broad working-level base — depth
that makes breadth credible. See
[Becoming a polymath](./first-principles/becoming-a-polymath.md).

**Tool budget** — A cap on how many (or which) tool calls an agent may make. See
[Agent guardrails](./content/02-reliable-outputs/agent-guardrails.md).

**Trace** — The end-to-end record of one request as it flows through every span of
your pipeline. See [Observability](./content/04-evals-observability/observability.md).

**Trajectory eval** — Grading the path an agent took — tools chosen, steps used, no
flailing — not just its final answer; paths rot before outcomes do. See
[Reliability & evals](./agentic-ai/reliability-and-evals.md).

**Tree-of-Thoughts** — A reasoning technique that explores multiple reasoning
branches with backtracking — deliberate search instead of a single
chain-of-thought. See
[Planning & reasoning](./agentic-ai/planning-and-reasoning.md).

**Workflow capture** — Owning an entire workflow end-to-end (not a tool within it), the
enterprise-AI strategy that erases adoption friction and compounds via rebundling. See
[Agentic AI as a product](./agentic-ai/agentic-ai-as-a-product.md).
