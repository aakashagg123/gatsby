# Transformers — recap & real-world examples

*Part of [Transformers for the product and technology leader](./README.md)*

## Real-world examples

**The paper that started it (2017).** Eight researchers, most of them at Google, published *Attention Is All You Need*. It dropped the recurrent networks that read text one word at a time and used attention alone. The block they described, attention plus a feed-forward layer, is the one in almost every language model today. 🎯 *Takeaway:* the [shape](./the-shape-of-a-transformer.md) has barely changed. Most progress since is scale, data, and the tricks in [lesson 6](./variants-and-reading-a-model-card.md).

**Heads that copy (2022).** Anthropic researchers studied small trained models and found attention heads with clear jobs. One kind looks at the previous token. Another finishes a repeated pattern. They linked these heads to how models learn from examples in the prompt. 🎯 *Takeaway:* [attention](./attention.md) does real, nameable work. But its weights are not a safe explanation of an answer, as Jain and Wallace showed.

**Tiled attention (2022).** The FlashAttention authors kept the exact same maths and changed where the numbers live. They process attention in small tiles in fast memory and never store the full score matrix. Models trained and served faster, and longer inputs became practical. 🎯 *Takeaway:* [the score matrix is the cost of length](./position-and-the-cost-of-context.md). A kernel change cut it without changing the answer.

**Sharing key and value heads (2023).** The Llama 2 paper reports that its larger models use grouped-query attention, which shrinks the cache for keys and values. The motive was serving: a smaller cache means more requests per machine. 🎯 *Takeaway:* [the cache sets concurrency](./generating-text-and-the-kv-cache.md). An architecture choice became a capacity choice.

**Experts (2024).** The Mixtral model uses 8 feed-forward experts and sends each token to 2. Its authors report about 47 billion parameters in total and about 13 billion in use for each token. 🎯 *Takeaway:* a [model card](./variants-and-reading-a-model-card.md) has two sizes. One sets memory and the other sets compute.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [The shape of a transformer](./the-shape-of-a-transformer.md) | Five numbers on a spec sheet give parameters, memory and compute | What are the layers, width, heads, vocabulary and context, and what do they cost? |
| [Attention](./attention.md) | Each token blends the values of the tokens it matches | For our failures on long inputs, was the information missing or ignored? |
| [The block](./the-block.md) | Heads and feed-forward layers write notes into a shared stream, and the feed-forward layer holds two thirds of the weights | Where was this model compressed, and what did we test? |
| [Position and context](./position-and-the-cost-of-context.md) | Order must be added, and attention cost grows with the square of the length | What do latency, cost and accuracy look like at our longest input? |
| [Generation and the KV cache](./generating-text-and-the-kv-cache.md) | Keys and values are kept, so memory per request sets how many fit | How many requests fit beside the weights at our context length? |
| [Variants and the model card](./variants-and-reading-a-model-card.md) | Total parameters set memory, active parameters set compute, and key and value heads set the cache | What are total and active parameters and cache per token for each candidate? |

**The through-line.** A transformer is a stack of one repeated block, and almost every question about it is a counting question. Count the parameters, then the multiply-adds, then the cache. Spec sheets hide four different sizes behind one name. The leaders who choose well turn the card into bytes and operations before they compare models.

> **Walk-away question:** *"For the model we plan to serve, can I state its total and active parameters, its cache per token, and how many requests fit on one machine at our context length?"*

## Test yourself

1. **GPT-2 small has 12 layers, a hidden size of 768, a vocabulary of 50,257 and 1,024 positions. About how many parameters does it have, and what share is in the embeddings?**
   <details><summary>Answer</summary>About 124 million: 124,439,808 by formula. The embeddings (tokens and positions) hold 39,383,808, which is 31.6%. (<a href="./the-shape-of-a-transformer.md">Lesson 1</a>)</details>
2. **In one block, which holds more parameters, attention or the feed-forward layer, and by how much?**
   <details><summary>Answer</summary>The feed-forward layer. Attention has four matrices of d by d, which is 4d². The feed-forward layer has two matrices of d by 4d, which is 8d². So the feed-forward layer holds two thirds of a block. (<a href="./the-shape-of-a-transformer.md">Lesson 1</a>)</details>
3. **A team doubles a model's hidden size. What happens to the size of a block?**
   <details><summary>Answer</summary>It multiplies by four, because block parameters grow with d². Doubling the number of layers only doubles it. (<a href="./the-shape-of-a-transformer.md">Lesson 1</a>)</details>
4. **What are queries, keys and values, in one sentence each?**
   <details><summary>Answer</summary>A query says what a token is looking for. A key says what a token offers. A value is what the token hands over when matched. (<a href="./attention.md">Lesson 2</a>)</details>
5. **Why are attention scores divided by the square root of the key length?**
   <details><summary>Answer</summary>A dot product of d_k numbers has variance proportional to d_k. Large scores push the softmax toward one-hot and its gradient toward zero. In the lesson's test at d_k = 256, the largest weight over 8 keys averages 0.92 without the scale and 0.34 with it. (<a href="./attention.md">Lesson 2</a>)</details>
6. **What does the causal mask do, and what goes wrong without it in training?**
   <details><summary>Answer</summary>It sets the score for every later token to minus infinity, so those weights are zero. Without it, a token could read the one it is meant to predict, so training would look perfect and the model would fail when serving. (<a href="./attention.md">Lesson 2</a>)</details>
7. **Why can a new block be added to a trained model without breaking it?**
   <details><summary>Answer</summary>Residual connections add each part's output to its input. A block whose output matrices are zero returns its input exactly, so it starts as a no-op. (<a href="./the-block.md">Lesson 3</a>)</details>
8. **A model is compressed, and it still passes short tests. Why test long, multi-step tasks?**
   <details><summary>Answer</summary>The feed-forward layers hold most of the weights and much of the stored knowledge, so cuts there can lose rare facts. Long and multi-step tasks use many layers in sequence and expose small losses that short tests hide. (<a href="./the-block.md">Lesson 3</a>)</details>
9. **At what input length does attention start to cost more than the rest of a block, for a hidden size of 4,096?**
   <details><summary>Answer</summary>At about 6 times the hidden size, which is 24,576 tokens. Attention costs 2n²d multiply-adds and the rest costs 12nd², so they are equal at n = 6d. This assumes a feed-forward width of 4d. (<a href="./position-and-the-cost-of-context.md">Lesson 4</a>)</details>
10. **A vendor says a model supports 128,000 tokens. What do you ask?**
   <details><summary>Answer</summary>What latency, cost and accuracy are at that length, with the answer at the start, middle and end. Whether the limit is native or extended. And whether the serving stack uses tiled attention. A full score matrix at 131,072 tokens, 32 heads and 16-bit numbers would take 1 TiB per layer. (<a href="./position-and-the-cost-of-context.md">Lesson 4</a>)</details>
11. **What does a KV cache hold, and what is its size?**
   <details><summary>Answer</summary>One key and one value vector for each token in each layer. The size is 2 × layers × key-value heads × head size × tokens × bytes per number. For a 7B-class shape (32 layers, 32 heads of 128) at 8,192 tokens and 16-bit, that is 4.0 GiB per sequence. (<a href="./generating-text-and-the-kv-cache.md">Lesson 5</a>)</details>
12. **Why is decode limited by memory speed and prefill by compute?**
   <details><summary>Answer</summary>Decode makes one token per pass, so each 2-byte weight does one multiply-add: about 1 FLOP per byte. Prefill over 512 tokens reuses each weight 512 times: about 512 FLOPs per byte. (<a href="./generating-text-and-the-kv-cache.md">Lesson 5</a>)</details>
13. **One card has 32 key and value heads and another has 8, all else equal. What changes in serving?**
   <details><summary>Answer</summary>The cache per token falls to a quarter. On an 80 GiB accelerator in the lesson's example, 16 long requests fit with 32 heads and 68 with 8, which also trims the weights a little. (<a href="./variants-and-reading-a-model-card.md">Lesson 6</a>)</details>
14. **A mixture-of-experts model has 47 billion total and 13 billion active parameters. What does each number set?**
   <details><summary>Answer</summary>Total parameters set the memory needed to hold the weights. Active parameters set the compute per token. It needs the memory of a 47 billion model and computes like a 13 billion one. (<a href="./variants-and-reading-a-model-card.md">Lesson 6</a>)</details>

## Sources

- Vaswani et al., *Attention Is All You Need*, NeurIPS 2017 ([arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)).
- Olsson et al., *In-context Learning and Induction Heads*, Anthropic, 2022 ([arxiv.org/abs/2209.11895](https://arxiv.org/abs/2209.11895)).
- Jain and Wallace, *Attention is not Explanation*, NAACL 2019 ([arxiv.org/abs/1902.10186](https://arxiv.org/abs/1902.10186)).
- Dao et al., *FlashAttention*, NeurIPS 2022 ([arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135)).
- Touvron et al., *Llama 2: Open Foundation and Fine-Tuned Chat Models*, 2023 ([arxiv.org/abs/2307.09288](https://arxiv.org/abs/2307.09288)): grouped-query attention in the larger models.
- Jiang et al., *Mixtral of Experts*, 2024 ([arxiv.org/abs/2401.04088](https://arxiv.org/abs/2401.04088)).
- The numbers in the questions come from `transformers/code/`. They are invented or illustrative. This module's sources were not re-opened during the build, and its fact-check is pending.
