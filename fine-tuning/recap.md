# Fine-tuning and post-training — recap & real-world examples

*Part of [Fine-tuning and post-training for the product and technology leader](./README.md)*

## Real-world examples

**A small tuned model beats a huge base model (2022).** OpenAI's InstructGPT paper reports that human raters preferred the outputs of a 1.3 billion parameter model, tuned on human feedback, to those of the 175 billion parameter base model. It also reports that the tuning took a small fraction of the pretraining compute. 🎯 *Takeaway:* [post-training](./from-base-model-to-assistant.md) shapes behaviour far more cheaply than pretraining builds it. It also moves other things, so test what you did not mean to change.

**A thousand examples (2023).** The LIMA authors tuned a model on 1,000 carefully chosen examples and reported strong results. They argue that most of a model's knowledge comes from pretraining and that tuning mainly teaches the format. 🎯 *Takeaway:* [quality beats quantity in SFT](./supervised-fine-tuning.md). Spend on checking examples, not on collecting more.

**One 48 GB accelerator for a 65 billion parameter model (2023).** The QLoRA authors kept the frozen weights in 4 bits, trained a small adapter, and tuned a 65 billion parameter model on a single 48 GB accelerator. 🎯 *Takeaway:* [LoRA and its variants](./lora-and-parameter-efficient-tuning.md) moved tuning from a cluster job to a workstation job.

**A reward model that overshoots (2022).** Gao and colleagues pushed models against reward models and measured the true quality with a stronger reference. The proxy reward rose steadily, and the true quality rose and then fell. 🎯 *Takeaway:* [over-optimizing a proxy](./preference-tuning-and-reward-hacking.md) is a measured effect, not a worry. Track an independent metric.

**New facts are learned slowly, and bring hallucination (2024).** Gekhman and colleagues found that models learn examples containing facts they do not know more slowly than examples they do know, and that learning them raises the rate of hallucination. 🎯 *Takeaway:* [tune for behaviour and retrieve for facts](./the-dataset.md).

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [The pipeline](./from-base-model-to-assistant.md) | Post-training shapes behaviour cheaply, with side effects | Which stage are we changing, and what else moved? |
| [Supervised fine-tuning](./supervised-fine-tuning.md) | Four dials: quantity, speed, replay and label quality | Who checked the examples, and what happened to general ability? |
| [LoRA](./lora-and-parameter-efficient-tuning.md) | A small, removable patch on a frozen model | How does each adapter compare with the base on a general test? |
| [Preference tuning](./preference-tuning-and-reward-hacking.md) | A reward is a proxy, and optimizing it hard breaks it | What independent metric tells us we are over-optimizing? |
| [The dataset](./the-dataset.md) | The model is a mirror of its data | What did the audit find, and is there a leak? |
| [Decide, cost and gate](./deciding-costing-and-checking-a-fine-tune.md) | A fixed cost against a saving per request, then a release gate | At what volume does it pay, and what must it not break? |

**The through-line.** Tuning is a push on a model that already has most of what it knows. The push has a size, a direction and a cost. Leaders who get it right choose the smallest push that works, measure what it changed beyond the target, and keep the data clean. They also decide whether it was worth doing at all, in numbers.

> **Walk-away question:** *"For our tuning project: can I name the behaviour we are changing, the test that measures it, what general ability we will not trade, the break-even volume, and the audit that cleared the data?"*

## Test yourself

1. **What does a base model do that an assistant does not, and what makes the difference?**
   <details><summary>Answer</summary>A base model continues text. It does not follow instructions. Post-training, supervised fine-tuning and preference tuning, teaches it to answer instructions in a useful format. (<a href="./from-base-model-to-assistant.md">Lesson 1</a>)</details>
2. **In the toy model, supervised tuning raised the target behaviour from 0.083 to 0.987. What else happened, and why?**
   <details><summary>Answer</summary>The loss on ordinary text more than doubled, from 1.103 to 2.280. The weights are shared, so a push that makes one behaviour likely changes others. (<a href="./from-base-model-to-assistant.md">Lesson 1</a>)</details>
3. **Five examples did almost nothing, and fifty did a lot. What does that say about planning a tuning run?**
   <details><summary>Answer</summary>The effect appears once there are enough steps, and below that nothing changes. A tuning run that stops too early can wrongly conclude that tuning does not work. Measure the behaviour at several data sizes. (<a href="./supervised-fine-tuning.md">Lesson 2</a>)</details>
4. **How do a higher learning rate and mixing in general data each change forgetting?**
   <details><summary>Answer</summary>A higher learning rate forgets more: general loss rose from 1.108 to 2.809 across the sweep. Mixing in general text removed most of the damage: 2.280 fell to 0.980 with 240 general pairs, while the behaviour stayed above 0.9. (<a href="./supervised-fine-tuning.md">Lesson 2</a>)</details>
5. **12 of 50 training labels are wrong. What does the model learn?**
   <details><summary>Answer</summary>It learns the mistake. The chance of the wrong answer rose from 0.091 to 0.411. A model matches the distribution of its examples. (<a href="./supervised-fine-tuning.md">Lesson 2</a>)</details>
6. **Why does LoRA need far less memory than full tuning?**
   <details><summary>Answer</summary>It trains only two thin matrices per adapted weight matrix, and the frozen weights need no gradients or optimizer state. Full tuning pays about 16 bytes per weight: weight, gradient and optimizer state. For a 7B-class model that is about 100 GiB, against about 12.7 GiB with a rank 16 adapter. (<a href="./lora-and-parameter-efficient-tuning.md">Lesson 3</a>)</details>
7. **Does LoRA protect general ability?**
   <details><summary>Answer</summary>No. In the toy, the adapter took general loss from 1.103 to 7.650. LoRA limits what can change and makes the change removable: with the adapter dropped, the loss returned to exactly 1.103. (<a href="./lora-and-parameter-efficient-tuning.md">Lesson 3</a>)</details>
8. **What is a reward model, and how can it go wrong?**
   <details><summary>Answer</summary>It scores answers, trained so that chosen answers outscore rejected ones. It learns whatever separates them in the data, including bias. Fit to judges who liked long answers, it put a weight of 1.53 on length, against 0.08 for unbiased judges. (<a href="./preference-tuning-and-reward-hacking.md">Lesson 4</a>)</details>
9. **Best-of-n selection against a noisy proxy gave true quality of 0.87 at n = 16 and 0.05 at n = 512, while the proxy kept rising. What is the lesson?**
   <details><summary>Answer</summary>Optimizing a proxy harder helps and then hurts. The proxy score cannot show the turn. Track an independent measure of real quality and limit how far the model may be pushed. (<a href="./preference-tuning-and-reward-hacking.md">Lesson 4</a>)</details>
10. **How does DPO differ from RLHF?**
    <details><summary>Answer</summary>DPO updates the model directly from pairs of better and worse answers, relative to a frozen reference model. There is no separate reward model and no reinforcement learning loop. (<a href="./preference-tuning-and-reward-hacking.md">Lesson 4</a>)</details>
11. **Name four problems a data audit finds before training.**
    <details><summary>Answer</summary>Exact and near duplicates, conflicting answers to the same question, empty or outlier examples, and leaks where a test input appears in training. In the lesson's example, all six planted problems were found. (<a href="./the-dataset.md">Lesson 5</a>)</details>
12. **Why can synthetic data be risky?**
    <details><summary>Answer</summary>The model that writes it passes on its own errors and style. It may also have terms of use that restrict training other models. Sample and read it, and check the licence. (<a href="./the-dataset.md">Lesson 5</a>)</details>
13. **A large model with a 1,800-token prompt costs $8.40 per 1,000 requests, and a tuned small model with a 150-token prompt costs $0.43. For a $2,000 project, what is the break-even?**
    <details><summary>Answer</summary>The saving is $7.97 per 1,000 requests, so the break-even is about 251,000 requests. These prices are invented for the arithmetic. (<a href="./deciding-costing-and-checking-a-fine-tune.md">Lesson 6</a>)</details>
14. **A tuned candidate scores 0.91 against a baseline of 0.84, and general ability falls from 0.80 to 0.74. Do you ship?**
    <details><summary>Answer</summary>No. The gain clears the bar, and the drop in general ability is far above the allowed 0.01. A release gate needs both. (<a href="./deciding-costing-and-checking-a-fine-tune.md">Lesson 6</a>)</details>

## Sources

- Ouyang et al., *Training language models to follow instructions with human feedback*, NeurIPS 2022 ([arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155)).
- Zhou et al., *LIMA: Less Is More for Alignment*, NeurIPS 2023 ([arxiv.org/abs/2305.11206](https://arxiv.org/abs/2305.11206)).
- Dettmers et al., *QLoRA*, NeurIPS 2023 ([arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)).
- Gao, Schulman and Hilton, *Scaling Laws for Reward Model Overoptimization*, ICML 2023 ([arxiv.org/abs/2210.10760](https://arxiv.org/abs/2210.10760)).
- Gekhman et al., *Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?*, EMNLP 2024 ([arxiv.org/abs/2405.05904](https://arxiv.org/abs/2405.05904)).
- The numbers in the questions come from `fine-tuning/code/`. They are invented or illustrative. This module's sources were not re-opened during the build, and its fact-check is pending.
