# Tensors — recap & real-world examples

*Part of [Tensors for the product and technology leader](./README.md)*

## Real-world examples & war stories

These are documented practices from the sources, not incidents. Where a story is invented to show a failure, it says so.

**NumPy's own warning about broadcasting.** The NumPy documentation praises broadcasting for vectorizing array operations "without making needless copies of data". It also says there are cases where broadcasting is a bad idea, because it leads to inefficient use of memory that slows computation. 🎯 *Takeaway:* the feature that makes code short can make a result much larger than you meant. Check the output shape of any operation that mixes a column and a row. This is [lesson 2](./operations-and-broadcasting.md).

**Why mixed-precision training keeps a float32 copy.** The 2018 *Mixed Precision Training* paper trains with float16 for the forward and backward passes. It keeps a float32 master copy of the weights for the update, and it scales the loss so small gradients survive float16's limited range. 🎯 *Takeaway:* a smaller number format is a tradeoff with a known repair, not a free saving. Ask which parts of training stay in float32. This is [lesson 4](./batching-memory-and-precision.md).

**A format chosen for range.** Google describes bfloat16 as a 16-bit format with the same dynamic range as float32, which it uses for its TPU hardware. A study by Kalamkar and colleagues found that training with bfloat16 matched float32 results without hyper-parameter changes. 🎯 *Takeaway:* two 16-bit formats are not interchangeable. One keeps precision, and the other keeps range. [Lesson 4](./batching-memory-and-precision.md) shows the difference in numbers.

**Memory, counted by pile.** The ZeRO paper starts from an accounting: for mixed-precision training with the Adam optimizer, each parameter needs 2 bytes for its float16 weight, 2 for its float16 gradient and 12 for optimizer state. Memory for the model state is therefore about 16 bytes per parameter, before activations. 🎯 *Takeaway:* the file size of a model understates what it takes to train it by a large factor. Ask for the budget by pile.

**One input at a time is memory bound.** NVIDIA's matrix multiplication guide notes that a matrix-vector product, where one of the sizes is 1, has an arithmetic intensity below 1 for numbers of 2 or 4 bytes. It is limited by memory, not compute. 🎯 *Takeaway:* serving single requests wastes most of a modern accelerator. Batching is the lever. This is [lesson 3](./matrix-multiplication.md).

**The loss that averaged over the wrong axis (an illustration).** A team computes the squared error between predictions of shape `(n, 1)` and labels of shape `(n,)`. The code runs. The loss is 4.6 times the right value on the example data, and even a perfect model would score 0.295 under it, so progress is hidden. The story is invented, and the [numbers come from the lesson-2 code](./operations-and-broadcasting.md). 🎯 *Takeaway:* a shape bug can look like a hard problem. Assert shapes, and test on a non-square input.

**The layer that never trained (an illustration).** A team copies a hidden layer's output out of the autograd graph. Training loss falls, because the output layer learns. The hidden layer's gradient is zero, so it cannot change. The story is invented, and the [numbers come from the lesson-5 code](./automatic-differentiation.md). 🎯 *Takeaway:* log the gradient size per layer, and alarm on a zero.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What a tensor is](./what-a-tensor-is.md) | A tensor is a grid of numbers with a shape. Size times bytes per number is its memory. | What are the shapes and dtypes of our biggest tensors, and what do they cost in bytes? |
| [Operations and broadcasting](./operations-and-broadcasting.md) | Shapes line up from the right. A wrong axis can still be legal, and then the bug is silent. | Which operations rely on broadcasting, and what test fails if an axis is wrong? |
| [Matrix multiplication](./matrix-multiplication.md) | A layer is one multiply and a bias. It costs 2 FLOPs per weight per input. A batch reuses the weights. | What is our batch size, and how much of the hardware does it use? |
| [Batching, memory and precision](./batching-memory-and-precision.md) | Training keeps weights, gradients, optimizer state and activations. Smaller formats trade range or precision for bytes. | What is the memory budget by pile, and which format does each part use? |
| [Automatic differentiation](./automatic-differentiation.md) | The library records the forward pass and replays it backward. It costs memory and fails quietly when the graph is cut. | How do we know every parameter gets a gradient? |

**The through-line:** a model is arithmetic on tensors, so most questions about it are counting questions. How many numbers? How many bytes each? How many multiplies? How many of them do we keep for the backward pass? Shape errors and graph errors do not crash. They produce a model that is wrong in a way no log shows. Counting, asserting shapes and checking gradients are the habits that catch them.

> **Walk-away question:** *"For our biggest model: what are the shapes and formats of the large tensors, what is the memory budget by pile for training and for serving, what is the batch size and what does it buy, and how do we know every part of the model receives a gradient?"*

If you can answer all four, you can steer the work. If not, you know which lesson to reread.

## Test yourself

1. **A batch of 16 images, 3 colour channels, 256 by 256 pixels, is stored as float32. How many bytes is it?**
   <details><summary>Answer</summary>Shape (16, 3, 256, 256) has 16 × 3 × 256 × 256 = 3,145,728 numbers. At 4 bytes each that is 12,582,912 bytes, which is 12 MiB. At float16 it is 6 MiB. (<a href="./what-a-tensor-is.md">Lesson 1</a>)</details>
2. **What is the difference between reshaping a tensor and copying it?**
   <details><summary>Answer</summary>A reshape is a view when the layout allows it. It reads the same flat list of numbers with a new shape and strides, so it copies nothing, and a change through one name shows in the other. If the layout does not allow it, the library makes a copy. A copy duplicates the numbers. (<a href="./what-a-tensor-is.md">Lesson 1</a>)</details>
3. **State the broadcasting rule.**
   <details><summary>Answer</summary>Line the shapes up from the right. Each pair of sizes must be equal, or one must be 1, or one must be missing. The result takes the larger size. If any pair fails, the operation raises an error. (<a href="./operations-and-broadcasting.md">Lesson 2</a>)</details>
4. **Predictions of shape (n, 1) are subtracted from labels of shape (n,). What shape results, and why is that a problem?**
   <details><summary>Answer</summary>The result is (n, n). Each prediction is compared with every label. A loss averaged over it is wrong, and memory grows with n squared. Reshape the predictions to (n,) first. (<a href="./operations-and-broadcasting.md">Lesson 2</a>)</details>
5. **Why does a shape bug often hide on a square table?**
   <details><summary>Answer</summary>On a 4 by 4 table, a mean over rows and a mean over columns both have shape (4,). Subtracting either is legal, so a wrong axis raises no error. On a 5 by 4 table the same slip fails. Test with non-square inputs. (<a href="./operations-and-broadcasting.md">Lesson 2</a>)</details>
6. **How many FLOPs does a layer with 4,096 inputs and 4,096 outputs need for a batch of 8?**
   <details><summary>Answer</summary>2 × 8 × 4,096 × 4,096 = 268,435,456 FLOPs, about 0.27 billion. That is two FLOPs per weight per input. (<a href="./matrix-multiplication.md">Lesson 3</a>)</details>
7. **Why is one batched multiply cheaper than many single-input multiplies, if the FLOPs are the same?**
   <details><summary>Answer</summary>The weights are read from memory once for the whole batch, not once per input. The FLOPs per byte moved go up, so the hardware spends less time waiting on memory. A single input has an intensity below 1, so it is memory limited. (<a href="./matrix-multiplication.md">Lesson 3</a>)</details>
8. **A 1.5 billion parameter model is trained in mixed precision with Adam. About how much memory does the model state take?**
   <details><summary>Answer</summary>About 16 bytes per parameter: 2 for the float16 weight, 2 for the float16 gradient and 12 for optimizer state. That is about 24 GB, before activations. The weights alone at float16 are 3 GB. (<a href="./batching-memory-and-precision.md">Lesson 4</a>)</details>
9. **Which memory pile grows with the batch size, and which do not?**
   <details><summary>Answer</summary>Activations grow with the batch. Weights, gradients and optimizer state depend on the number of parameters only. Halving the batch frees activation memory and leaves the other three unchanged. (<a href="./batching-memory-and-precision.md">Lesson 4</a>)</details>
10. **How do float16 and bfloat16 differ, and what goes wrong with float16 in training?**
    <details><summary>Answer</summary>float16 has 5 exponent bits and 10 fraction bits: a small range and more precision. bfloat16 has 8 exponent bits and 7 fraction bits: the range of float32 and less precision. In float16, values above 65,504 overflow and tiny values round to zero, so gradients vanish. Loss scaling and a float32 master copy of the weights are the usual repairs. (<a href="./batching-memory-and-precision.md">Lesson 4</a>)</details>
11. **What does automatic differentiation record, and what does the backward pass do?**
    <details><summary>Answer</summary>It records each operation during the forward pass, and saves the values the backward rules will need. The backward pass starts at the loss with a gradient of 1 and passes gradients back through the operations in reverse order, using one small rule per operation. (<a href="./automatic-differentiation.md">Lesson 5</a>)</details>
12. **Training loss falls, but one layer's gradient is exactly zero at every step. What is the likely cause?**
    <details><summary>Answer</summary>The autograd graph is cut before that layer, for example by copying a value out of the graph. The layers after the cut learn, so the loss falls. The layers before it never change. Log the gradient size per layer and alarm on a zero. (<a href="./automatic-differentiation.md">Lesson 5</a>)</details>

## Sources

- NumPy documentation, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html): vectorizing "without making needless copies of data", and the warning that broadcasting can lead to inefficient use of memory. Read from the documentation source on GitHub, 2026-10.
- Micikevicius et al., *Mixed Precision Training*, ICLR 2018 ([arxiv.org/abs/1710.03740](https://arxiv.org/abs/1710.03740)): float16 forward and backward passes, a float32 master copy of the weights, and loss scaling. Checked through search-result excerpts, 2026-10.
- Google Cloud, [bfloat16: the secret to high performance on Cloud TPUs](https://cloud.google.com/blog/products/ai-machine-learning/bfloat16-the-secret-to-high-performance-on-cloud-tpus), and Kalamkar et al., *A Study of BFLOAT16 for Deep Learning Training*, 2019 ([arxiv.org/abs/1905.12322](https://arxiv.org/abs/1905.12322)): range equal to float32, and training that matched float32 without hyper-parameter changes. Checked through search-result excerpts, 2026-10.
- Rajbhandari et al., *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models*, 2020 ([arxiv.org/abs/1910.02054](https://arxiv.org/abs/1910.02054)): the 2 + 2 + 12 byte accounting for mixed-precision Adam. Checked through search-result excerpts, 2026-10.
- NVIDIA, [Matrix Multiplication Background User's Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html): matrix-vector products always have an arithmetic intensity below 1. Checked through search-result excerpts, 2026-10.
- The two illustrations are invented. All figures from the example data come from `tensors/code/`.

---

← Back to [module overview](./README.md)
