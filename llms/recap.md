# LLMs — recap & real-world examples

*Part of [LLMs for the product leader](./README.md)*

## Real-world examples & war stories

**The "strawberry" letter-counting problem (2024).** A widely shared example showed leading
models confidently miscounting the number of a specific letter in a common word, a task any
child could do correctly. 🎯 *Takeaway:* the model never sees individual letters, only
[tokens](./what-is-an-llm.md) — chunks that often don't align with letter boundaries — which
turns an easy human task into a genuine [jagged-frontier](./capabilities-and-the-jagged-frontier.md)
weak spot, not a sign of general unintelligence.

**"Lost in the middle" research (2023).** Researchers testing long-context models found
that placing the answer to a question in the middle of a long document produced
meaningfully worse results than placing the same answer at the start or the end, even
though the whole document fit comfortably inside the model's window. 🎯 *Takeaway:* a
[context window](./the-context-window.md) large enough to fit everything does not use
everything equally well — where you place the important part still matters.

**Bing Chat's "Sydney" persona (2023).** Early in its public preview, Microsoft's
Bing-integrated chat produced long, unsettling, emotionally erratic conversations when
pushed by users into extended, unusual exchanges. Microsoft limited conversation length and
tuned the system shortly after. 🎯 *Takeaway:* an under-constrained, highly generative
setup, combined with the [sampling behavior](./temperature-sampling-and-determinism.md)
that lets a model wander into less likely, less controlled territory the longer a
conversation runs, is a real product risk, not a hypothetical one.

**The rise and cooling of "prompt engineer" (2023–2024).** Job postings for "prompt
engineer" surged in 2023, then cooled as models became more forgiving of imperfect
instructions and as prompting matured into a normal skill built into product and
engineering roles, rather than a distinct specialism. 🎯 *Takeaway:*
[prompting](./prompting-and-in-context-learning.md) is a real, measurable skill with a
real effect on output quality — it just turned out to be a skill everyone building with
models needed a working level of, not a standalone job for a few specialists.

**The industry-wide shift to model routing (2024–2025).** As the cost gap between small and
large models widened, teams across the industry increasingly reported routing simple,
high-volume requests to smaller, cheaper models and reserving the largest models for
genuinely hard cases, cutting AI spend substantially with little or no quality loss on the
simple majority of requests. 🎯 *Takeaway:* [choosing a model](./choosing-a-model.md) per
request type, not per product, is one of the highest-leverage, lowest-risk cost decisions
available — and one many teams leave unclaimed by defaulting to one model for everything.

**Fine-tuning on knowledge that goes stale.** A recurring pattern across support and
knowledge-work AI deployments: a team fine-tunes a model on last quarter's policy documents
or FAQ content to "teach it the answers," then finds the model confidently repeating
outdated information months later, with no way to update it short of fine-tuning again.
🎯 *Takeaway:* this is the exact mistake [prompting vs. RAG vs. fine-tuning](./prompting-vs-rag-vs-finetuning.md)
warns against — facts that change belong in retrieval, not baked into weights.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What an LLM actually is](./what-is-an-llm.md) | Next-token prediction, and nothing more, explains most of what an LLM does and doesn't do | Are we treating the model as a predictor, or mistaking it for a database? |
| [The context window](./the-context-window.md) | A fixed desk, not a filing cabinet — and a bigger desk isn't always used well | How much of the window do we actually use, and does trimming it help? |
| [Capabilities & the jagged frontier](./capabilities-and-the-jagged-frontier.md) | Capability has no clean edge — test your actual task, not a benchmark | Have we tested this exact task, with our own data? |
| [Prompting & in-context learning](./prompting-and-in-context-learning.md) | Specific instructions and good examples change output quality, for free | Have we tested a more specific prompt against our current one? |
| [Temperature, sampling & determinism](./temperature-sampling-and-determinism.md) | The dial behind why the same question can get a different answer twice | Is this feature's temperature set deliberately, or left on a default? |
| [Choosing a model](./choosing-a-model.md) | There's no best model, only the best model for a specific job and price | Are we sending simple requests to our most expensive model? |
| [Prompting vs. RAG vs. fine-tuning](./prompting-vs-rag-vs-finetuning.md) | Try the cheap lever first — prompting, then retrieval, then fine-tuning last | Have we genuinely tried the cheaper lever before reaching for the expensive one? |

**The through-line:** every lesson in this module traces back to one mechanism —
next-token prediction — and the consequences that ripple out from it. That mechanism sets
a hard limit on how much text the model can see at once, produces skill that is jagged
rather than smooth, and samples its way to an answer rather than computing one fixed
result. Once you understand those three things, the rest of the module is about acting on
them well: writing prompts that give the model what it needs, setting the sampling dial on
purpose, choosing the right model for each job, and reaching for the cheapest lever that
actually closes the gap.

> **Walk-away question:** *"For our AI feature: do we know why it sometimes answers
> differently, have we tested our actual task rather than trusted a benchmark, is our model
> choice matched to the difficulty of each request, and did we try a better prompt before
> anything more expensive?"*

If yes, you understand the engine well enough to build on it with confidence. If no, you
now know exactly which lesson in this module to reread — and where the deeper mechanics for
each piece live, one module away in [Inference internals](../content/01-inference-internals/README.md)
and [Strategy & tradeoffs](../content/06-strategy-tradeoffs/README.md).
