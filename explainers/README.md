# Visual explainers

*Part of the [craft tracks](../README.md). Each explainer links to the lessons that go deeper.*

An explainer follows **one example** through a system, a product decision or a learning path, one stage at a time. Every stage has a short plain block, a picture and one line to remember. There is no maths to do. Each takes about ten minutes.

The explainers sit beside the lessons, not in place of them. Read an explainer first to get the shape of a system. Then read the lessons for the detail, the numbers and the code.

## The explainers

### How AI systems work

1. [Inside one LLM request](./inside-one-llm-request.md) — follow the question "What is a mortgage rate?" from Enter to the last word: tokens, the context window, prefill, decode, the KV cache, streaming and batching.
2. [How a model learns](./how-a-model-learns.md) — follow "The cat sat on the ___" through the loss, the gradient and the update, then through pretraining, supervised tuning and preference tuning.
3. [One token through a transformer](./one-token-through-a-transformer.md) — follow "bank" in "the river bank" through attention, the feed-forward layer and the residual stream.
4. [How an image model draws](./how-an-image-model-draws.md) — follow "a red kite over a beach" from noise to picture: diffusion, guidance and the latent space.
5. [One agent run, step by step](./one-agent-run.md) — follow the goal "Refund order 55812 if eligible" through tools, a gateway, stop conditions and a human checkpoint.
6. [Anatomy of a guardrailed request](./anatomy-of-a-guardrailed-request.md) — follow a hostile request through the layers that stop it.

### How AI products are run

These six follow a product decision rather than a system. Each stage shows a decision, a number or a document that the product manager owns.

7. [One AI feature, from idea to launch](./one-ai-feature-from-idea-to-launch.md) — follow claim summaries at an insurer from the size of the prize to the first-month readout.
8. [One model change: cost, speed and quality](./one-model-change.md) — follow a retirement notice to a new model, and see why the bill moved more than the price list.
9. [From one AI task to gross margin](./one-ai-feature-p-and-l.md) — follow one task's tokens to the margin on a seat and the pricing choice that follows.
10. [One eval regression, traced to its cause](./one-eval-regression-traced.md) — follow a red eval gate through error bars, slices and layers to the cause and a new guard.
11. [One user story becomes an agent spec](./one-user-story-to-agent-spec.md) — follow a dispatcher's story to tools, limits, autonomy per action and a rule for more freedom.
12. [One AI incident, from alert to postmortem](./one-ai-incident-review.md) — follow a wrong fee answer from the first screenshot to the actions in the roadmap.

### How to learn this

These follow one learner through a [learning path](../learning-paths/README.md), stage by stage, to show what each stage changes in what the learner can do. The stage names and hours come from the path itself.

13. [A senior PM's path, one stage at a time](./one-senior-pm-path.md) — follow a senior PM from a VP's question to a one-page answer, through the four stages of the Senior PM path.
14. [An AI product lead's path, one stage at a time](./one-ai-product-lead-path.md) — follow a new AI product lead from decisions by instinct to an architecture review pack, through the five stages of the AI Product Lead path.
15. [An AI engineer's path, one stage at a time](./one-ai-engineer-path.md) — follow a backend engineer from a demo to a tested support agent, through the five stages of the AI Engineer path.
16. [An AI engineering lead's path, one stage at a time](./one-ai-engineering-lead-path.md) — follow an engineering lead from judging a demo to approving a design with conditions, through the five stages of the AI Engineering Lead path.

Then the [recap](./recap.md), with a self-test across all sixteen.

## How the explainers connect to the lessons

| Explainer | The lessons that go deeper |
| --- | --- |
| Inside one LLM request | [Generating text and the KV cache](../transformers/generating-text-and-the-kv-cache.md), [GenAI and agent platforms](../system-design/genai-and-agent-platforms.md) |
| How a model learns | [Training: loss and gradient descent](../machine-learning/training-loss-and-gradient-descent.md), [From base model to assistant](../fine-tuning/from-base-model-to-assistant.md) |
| One token through a transformer | [Attention](../transformers/attention.md), [The block](../transformers/the-block.md) |
| How an image model draws | [The modalities](../generative-ai/the-modalities.md) |
| One agent run | [What an agent is](../ai-agents/what-an-agent-is-and-how-much-autonomy-it-needs.md), [Designing agentic flows](../building-ai-native-products/designing-agentic-flows.md) |
| A guardrailed request | [The threat model and guardrails](../ai-security-and-guardrails/the-threat-model-and-guardrails.md) |
| One AI feature, idea to launch | [Capstone: ship one AI-native feature](../building-ai-native-products/capstone-ship-one-ai-native-feature.md), [Product sense for AI products](../product-sense/product-sense-for-ai.md) |
| One model change | [Choosing a model](../llms/choosing-a-model.md), [Prompts in production](../prompt-engineering/prompts-in-production.md) |
| From one AI task to gross margin | [FinOps for AI](../cost-optimization/finops-budgets-forecasting-and-the-cost-review.md), [Pricing and business models](../business-acumen/monetization-and-business-models.md) |
| One eval regression | [Building the eval stack in the right order](../evaluation-and-observability/building-the-eval-stack-in-the-right-order.md), [Technical product management for AI](../technical-product-management/tpm-for-ai-products.md) |
| One user story to an agent spec | [Specs, PRDs & RFCs](../technical-product-management/specs-prds-and-rfcs.md), [Practice: the agent spec and risk register](../building-ai-native-products/agentic-flows-practice.md) |
| One AI incident | [Incidents & postmortems](../technical-product-management/incidents-and-postmortems.md), [Reliability & failure](../technical-product-sense/reliability-and-failure.md) |
| A senior PM's path | [Senior PM path](../learning-paths/senior-product-manager.md), [Visual learning paths](../learning-paths/visual-paths.md) |
| An AI product lead's path | [AI Product Lead path](../learning-paths/ai-product-lead.md), [Visual learning paths](../learning-paths/visual-paths.md) |
| An AI engineer's path | [AI Engineer path](../learning-paths/ai-engineer.md), [Visual learning paths](../learning-paths/visual-paths.md) |
| An AI engineering lead's path | [AI Engineering Lead path](../learning-paths/ai-engineering-lead.md), [Visual learning paths](../learning-paths/visual-paths.md) |

## About the examples

The examples are made up or simplified so that each fits on a page. The companies in the product explainers are invented, and their prices are illustrative. Where a number comes from this site's own code, the page says so. Real systems differ in detail. Every page lists its sources and says which ones were read.
