# Generative AI: the big picture — recap & real-world examples

*Part of [Generative AI: the big picture](./README.md)*

## Real-world examples & war stories

**The Air Canada chatbot (2024).** A customer asked Air Canada's website chatbot about
bereavement fares. The chatbot invented a refund policy that did not exist. Air Canada
argued in court that the chatbot was "a separate legal entity" responsible for its own
words. A tribunal disagreed and made the airline honor the invented policy. 🎯 *Takeaway:*
a company is responsible for what its generative model says, the same way it is
responsible for what an employee says. [Probabilistic output](./probabilistic-software.md)
that reaches a customer with no check in between is not a technical detail — it is a
policy your company now holds.

**GitHub Copilot's growth (2021 onward).** Code generation became one of the fastest,
widest adoptions of any generative AI tool, inside engineering teams that are usually
skeptical of new tools. 🎯 *Takeaway:* code is [checkable by running it](./the-modalities.md)
— tests pass or fail, the type checker accepts or rejects — which gives engineers a fast,
cheap way to catch a bad output before it ships. That tight feedback loop is exactly the
[value-creating pattern](./where-value-is-created-and-destroyed.md) this module names.

**Google's Gemini image generation (2024).** An image-generation feature, tuned to
represent diversity across historical images, produced clearly inaccurate results —
including historically White figures depicted with different skin tones. Google paused
the feature within days. 🎯 *Takeaway:* [each modality carries its own failure
pattern](./the-modalities.md), and a fix applied broadly, without enough testing on the
specific modality's edge cases, can create a new, more visible failure than the one it
was meant to solve.

**Klarna's AI customer service reversal (2024).** Klarna announced its AI assistant was
doing the work of seven hundred customer service agents, then later said it would hire
humans again after acknowledging the AI-only approach hurt the quality customers actually
wanted. 🎯 *Takeaway:* a use case can clear the "slow and expensive by hand" gate and still
fail the ["is checking or correcting it acceptable" gate](./where-value-is-created-and-destroyed.md)
— the choice between an AI-only, a human-only, and a blended service was a
[build-or-buy-shaped decision](./build-buy-or-fine-tune.md) the company had to revisit
in public.

**AI-generated content corrections at major outlets (2023–2024).** Several news and media
organizations published AI-generated articles that contained factual errors, requiring
public corrections. 🎯 *Takeaway:* text generation is mature and cheap, but
[maturity is not the same as zero error rate](./the-modalities.md) — publishing generated
text with no fact-check step treats a probabilistic tool as if it were deterministic.

**Fast food AI drive-thru pilots (2024).** More than one large fast-food chain piloted
generative voice ordering at the drive-thru, then scaled the pilots back after
error rates on real, noisy, in-person orders proved too high for the format. 🎯 *Takeaway:*
a demo run in a quiet room and a product run in a loud drive-thru lane are different
[probabilistic environments](./probabilistic-software.md) — the failure rate that looked
acceptable in testing did not hold in the real, noisy input the product actually faced.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What makes AI "generative"?](./what-is-generative-ai.md) | A judge and a maker do different jobs — know which one your task needs | Does this task need a judgment, or something new to be made? |
| [The five modalities](./the-modalities.md) | Five factories, five maturity levels, five failure patterns | Which modality does this feature need, and is it mature enough? |
| [Probabilistic software](./probabilistic-software.md) | The same input can give a different output — testing becomes measuring | What is the acceptable range of outcomes, and have we measured it? |
| [The generative AI product stack](./the-genai-product-stack.md) | The model is one of four layers — price all four | Have we budgeted grounding, action, and operations, not just the model? |
| [Build, buy, or fine-tune](./build-buy-or-fine-tune.md) | Buy by default; build or fine-tune only with a clear reason | Is the model itself our product, or the system we build around it? |
| [Where value is created and destroyed](./where-value-is-created-and-destroyed.md) | Three gates decide the outcome: slow by hand, cheap to check, safe to sometimes get wrong | Does this use case actually clear all three gates? |

**The through-line:** every lesson in this module is one piece of a single shift.
Generative AI does a different job than the predictive AI that came before it. That job
spans five modalities, each with its own maturity. The output is probabilistic, which
changes what testing, support, and trust mean. The model is one layer in a larger stack,
most of which a product team builds itself. Buying the model and building the system
around it beats training your own, in almost every real case. And the use cases that
actually pay off are the ones that clear three honest gates — slow by hand, cheap to
check, safe to sometimes get wrong — not the ones with the best demo.

> **Walk-away question:** *"For our next generative AI proposal: which modality does it
> need, what is its measured pass rate across many runs, have we priced all four layers of
> the stack, can we justify build or fine-tune over buy, and does it clear all three value
> gates?"*

If yes, you are scoping a real product decision. If no, you now know exactly which lesson
in this module to reread — and where the deeper mechanics for each layer live, one module
away in [RAG & vector databases](../rag-vector-databases/README.md) and
[Agentic AI](../agentic-ai/README.md).
