# The context window

*Part of [LLMs for the product leader](./README.md)*

## TL;DR

A model can only consider a fixed amount of text at once, measured in tokens. This is its
**context window**. Everything the model needs for a given request — your instructions, the
conversation so far, any documents you supply — has to fit inside that one window,
because the model genuinely cannot see anything outside it. This is not a policy choice a
vendor could relax with a setting. It follows from how the model computes: comparing every
token to every other token gets more expensive the more tokens there are, so the window has
a real, engineered ceiling. Windows have grown from a few thousand tokens to a million over a few
years (as of October 2026, Anthropic lists 1M tokens for all its current models), and that growth changed what products are possible — but it
did not remove the limit, and it introduced a new problem: a model can technically fit a
huge amount of text in its window and still perform worse than you'd expect, because
attention spread across more text is attention divided. This lesson is about the window
itself, as a hard constraint. Managing what you deliberately put inside it, once you know
the size you're working with, is its own skill, covered in
[context engineering](../content/00-foundations/context-engineering.md).

> 🎯 **For the product leader**
>
> **Why it matters** — "Just give it more context" sounds like a free upgrade. It is not
> free: it costs more tokens, it costs more latency, and past a certain point it can cost
> you quality, because a model's attention to any one part of a stuffed window is weaker
> than its attention to a lean one.
>
> **What it changes in your decisions** — You treat context window size as a real
> engineering constraint with a real cost curve, the same way you'd treat a database's
> storage limit, instead of an implementation detail to wave away.
>
> **Ask yourself** — *"For our busiest feature, how much of the context window do we
> actually use, and have we tested whether trimming it improves the answer instead of just
> the bill?"*
>
> **Risk if ignored** — A team ships a feature that pastes in everything it might possibly
> need "to be safe," and discovers months later that the feature is both expensive and less
> accurate than a leaner version would have been.

## The mental model: a desk, not a filing cabinet

A context window is a desk, not a filing cabinet. A filing cabinet can hold as much as you
own; you just walk over and pull out what you need. A desk has a fixed surface. Whatever
does not fit on the desk right now is not part of the current work, no matter how relevant
it might be. Every request to a model starts by laying out everything relevant on that
desk — instructions, history, documents — and the model can only work with what is
currently laid out.

```mermaid
flowchart TB
  subgraph WINDOW["The context window — a fixed size, in tokens"]
    SYS["System instructions"]
    HIST["Conversation history<br/>so far"]
    DOCS["Any documents or<br/>retrieved passages supplied"]
    TASK["The current request"]
  end
  WINDOW --> MODEL["The model predicts<br/>the next token, using<br/>only what's on the desk"]
  OUT["Anything outside<br/>the window"] -.->|"invisible to<br/>this request"| MODEL
```

## Why the limit exists at all

Inside a model, every token is compared against every other token in the window to decide
what matters for predicting the next one. Double the number of tokens, and that comparison
work grows faster than double — which is why context windows did not simply start at
"unlimited" and why growing them takes real engineering effort, not a configuration change.
That comparison step is called attention, and
[What an LLM actually is](./what-is-an-llm.md#inside-the-model-attention) explains it in
plain words. The deep mechanics of that cost — attention, memory, and the tricks that make longer
windows practical — live in [Inference internals](../content/01-inference-internals/README.md).
The product-relevant fact is simpler: a bigger window is not free, and someone chose its
size for real, physical reasons.

## Bigger windows solved one problem and revealed another

Early models held a few thousand tokens, barely a few pages. Modern windows can hold
hundreds of thousands, enough for a whole codebase or a long report. That growth genuinely
unlocked new products: reading a full document instead of a fragment, holding a long
conversation without forgetting the start. But a second effect showed up alongside it,
often called "lost in the middle": a model given a huge window does not treat every part of
it equally well. Information placed at the very start or the very end tends to get more
reliable attention than information buried in the middle of a long stuffed prompt. A window
technically large enough to fit everything is not the same as a window that will use
everything equally well.

That 2023 result came from older models. Newer work shows a wider problem. Chroma tested
18 models in 2025. Accuracy fell as the input grew, even on simple tasks. Distractors made
it worse, and every model did better on a short, focused prompt than on a long one that
held the same facts. Anthropic's documentation now calls this **context rot**. The lesson
for a product leader: do not rely on position tricks alone. Measure quality at your real
input sizes.

Three more facts shape the budget. Everything counts toward the window: the system prompt,
tool definitions, tool results, and the model's own output. For a model that thinks before
it answers, the thinking tokens count too. Long inputs can also cost more per token on some
models; Anthropic's pricing page notes a higher rate above 100,000 tokens on Haiku 5.5.
Finally, for long-running agents, vendors now offer automatic compaction, which summarizes
older turns on the server. It saves space, and it can lose detail, so test it.

## The product consequence: window size is a budget, not a target

Treat the window the way you'd treat any limited, costed resource: a budget to spend
deliberately, not a target to fill because it's available. A lean, well-chosen set of
instructions and the specific, relevant passages a task needs will often outperform a
window stuffed with everything that might be relevant, at lower cost and lower latency.
This reframes a common instinct — "the model supports 200,000 tokens, so let's use them" —
into the sharper, more useful question: "what does this specific request actually need to
see, and does adding more help or quietly hurt?"

## Failure modes

- **Filling the window "to be safe"** — pasting in every document that might be relevant,
  paying for tokens the model barely uses well, and sometimes getting a worse answer for
  the extra cost.
- **Ignoring the window as a real limit** — designing a feature that assumes context can
  simply grow forever as the product's needs grow, without a plan for what happens when it
  doesn't fit.
- **Burying the important instruction in the middle** — placing the one instruction that
  matters most in the middle of a long prompt, where attention is weakest, instead of at
  the start or end.
- **Confusing window size with product quality** — choosing a model mainly because it
  advertises a bigger window, without testing whether the feature actually needs it or
  performs better because of it.

## Practitioner checklist

- [ ] Do we know, in tokens, how much of the context window our busiest feature actually
      uses?
- [ ] Have we tested a leaner version of our prompt against our current one, to check
      whether trimming helps quality as well as cost?
- [ ] Are our most important instructions placed at the start or end of the prompt, not
      buried in the middle?
- [ ] Have we measured answer quality at our largest real input, not only at a typical one?
- [ ] For long conversations or agents, do we know what is dropped or summarized when the
      window fills?
- [ ] When we picked a model partly for its window size, did we verify our feature actually
      benefits from that size?

## Related lessons

- [What an LLM actually is](./what-is-an-llm.md) — why the window is measured in tokens,
  not words.
- [Context engineering](../content/00-foundations/context-engineering.md) — the skill of
  deciding what to put in the window once you know its size.
- [Memory & context](../agentic-ai/context-and-memory.md) — the agent-side view of
  managing a window across a long-running task.

## Sources

- Anthropic, Claude documentation,
  [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows):
  1M-token windows on current models; everything in the request counts, including thinking
  tokens; "context rot"; server-side compaction in beta. Read 2026-10-25.
- Anthropic, Claude documentation,
  [Models overview](https://platform.claude.com/docs/en/models/overview): 1M context for
  Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5. Read 2026-10-25.
- Anthropic, Claude documentation,
  [Pricing](https://platform.claude.com/docs/en/about-claude/pricing): price table. The
  Haiku 5.5 long-prompt surcharge is from the Context windows page. Read 2026-10-25.
- Liu et al., [Lost in the Middle](https://arxiv.org/abs/2307.03172), TACL 2023:
  performance is often highest when relevant information is at the start or end of the
  input. Read 2026-10-25.
- Chroma, [Context Rot](https://www.trychroma.com/research/context-rot) (July 2025): 18
  models; performance falls with input length; focused prompts beat full prompts.
  Read 2026-10-25.
