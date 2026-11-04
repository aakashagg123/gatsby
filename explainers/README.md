# Visual explainers

*Part of the [craft tracks](../README.md). Each explainer links to the lessons that go deeper.*

An explainer follows **one real example** through a system, one stage at a time. Every stage has a short plain block, a picture and one line to remember. There is no maths to do. Each takes about ten minutes.

The explainers sit beside the lessons, not in place of them. Read an explainer first to get the shape of a system. Then read the lessons for the detail, the numbers and the code.

## The explainers

1. [Inside one LLM request](./inside-one-llm-request.md) — follow the question "What is a mortgage rate?" from Enter to the last word: tokens, the context window, prefill, decode, the KV cache, streaming and batching.
2. [How a model learns](./how-a-model-learns.md) — follow "The cat sat on the ___" through the loss, the gradient and the update, then through pretraining, supervised tuning and preference tuning.
3. [One token through a transformer](./one-token-through-a-transformer.md) — follow "bank" in "the river bank" through attention, the feed-forward layer and the residual stream.
4. [How an image model draws](./how-an-image-model-draws.md) — follow "a red kite over a beach" from noise to picture: diffusion, guidance and the latent space.
5. [One agent run, step by step](./one-agent-run.md) — follow the goal "Refund order 55812 if eligible" through tools, a gateway, stop conditions and a human checkpoint.
6. [Anatomy of a guardrailed request](./anatomy-of-a-guardrailed-request.md) — follow a hostile request through the layers that stop it.

Then the [recap](./recap.md), with a self-test across all six.

## How the explainers connect to the lessons

| Explainer | The lessons that go deeper |
| --- | --- |
| Inside one LLM request | [Generating text and the KV cache](../transformers/generating-text-and-the-kv-cache.md), [GenAI and agent platforms](../system-design/genai-and-agent-platforms.md) |
| How a model learns | [Training: loss and gradient descent](../machine-learning/training-loss-and-gradient-descent.md), [From base model to assistant](../fine-tuning/from-base-model-to-assistant.md) |
| One token through a transformer | [Attention](../transformers/attention.md), [The block](../transformers/the-block.md) |
| How an image model draws | [The modalities](../generative-ai/the-modalities.md) |
| One agent run | [What an agent is](../ai-agents/what-an-agent-is-and-how-much-autonomy-it-needs.md), [Designing agentic flows](../building-ai-native-products/designing-agentic-flows.md) |
| A guardrailed request | [The threat model and guardrails](../ai-security-and-guardrails/the-threat-model-and-guardrails.md) |

## About the examples

The examples are made up or simplified so that each fits on a page. Where a number comes from this site's own code, the page says so. Real systems differ in detail. Every page lists its sources and says which ones were read.
