# Context engineering — recap & real-world examples

*Part of [Context engineering for the product leader](./README.md)*

## Real-world examples & war stories

**Customer support bots that answer the FAQ, not the question.** A recurring pattern
across support-AI rollouts: a bot answers fluently and confidently, but with the wrong
policy — because it was tuned against a handful of common phrasings and the customer
asked the same question a different way. 🎯 *Takeaway:*
[fragility, not model quality](./why-prompt-engineering-doesnt-scale.md), is the usual
cause — the fix is retrieval and structured instructions, not a bigger model.

**An internal AI assistant that "knew" a policy that had changed.** Companies grounding
assistants on internal wikis or handbooks repeatedly hit the same incident: the
assistant states a rule with total confidence months after the underlying policy
changed, because nothing tracked that the source document was now stale. 🎯 *Takeaway:*
[an unowned seam](./the-anatomy-of-a-context-pipeline.md) in the pipeline — a policy
source with no freshness check — produced a wrong answer that every individual
component reported as healthy.

**Two support bots from the same company, two different refund answers.** As
organizations shipped multiple AI features off the same policies, a familiar failure
emerged: one feature's prompt encoded last year's refund window, another's encoded this
year's, and a customer who asked both got contradictory answers. 🎯 *Takeaway:*
[context governance](./context-governance-at-scale.md) exists exactly to prevent this —
one shared, versioned source with a registry of consumers, not three independent copies.

**An AI feature that "regressed" for weeks before anyone found the real bug.** A common
debugging story: a quality drop gets blamed on the model, prompts get rewritten
repeatedly with no improvement, and the actual cause turns out to be a retrieval index
that silently stopped updating. 🎯 *Takeaway:*
[checking context before blaming the model](./evaluating-context-quality.md) would have
found this in an afternoon instead of weeks.

**An AI feature that demoed perfectly and needed a second, quieter rebuild.** A frequent
post-launch story: the demo script worked because the context it needed happened to be
ready; real users asked questions that needed a retrieval corpus or a memory feature
nobody had built yet, because context infrastructure was sequenced after the model work
instead of alongside it. 🎯 *Takeaway:*
[context work has a different job at each project phase](./context-across-the-product-lifecycle.md),
and skipping the discovery-phase audit is how this happens.

**The assistant that got worse when we gave it everything (an illustration).** Picture a
team that fixes a wrong answer by adding the whole policy handbook to every request.
Anthropic's engineering guidance warns that model quality can degrade as context grows,
and that context has diminishing returns. So answers can get worse while cost and
latency rise. The better fix is smaller: retrieve the relevant paragraphs and drop the
rest. 🎯 *Takeaway:*
[the goal is the smallest useful context](./what-is-context-engineering.md), not the
largest one you can fit.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What is context engineering, for a product leader?](./what-is-context-engineering.md) | The right question is "what does this decision need to see," not "what data do we have" — and the answer is the smallest useful context | Could I name what our riskiest AI feature is shown before it answers, and what we could remove? |
| [Why prompt engineering doesn't scale](./why-prompt-engineering-doesnt-scale.md) | Fragility, no reuse, no memory are structural, not wording problems. The prompt still owns wording | Is our last "prompt fix" actually a retrieval, memory, or tool-state gap? |
| [The anatomy of a context pipeline](./the-anatomy-of-a-context-pipeline.md) | Every stage has an owner; the seams between stages usually don't. Agents rebuild their context at every step | Do I know which named stage to check first, and what compaction must keep? |
| [Context as a spec-able requirement](./context-as-a-spec-able-requirement.md) | Context needs its own section in the spec, next to the eval bar, with a size budget | Does our spec name what the model must know, remember, and retrieve, and how much? |
| [Context governance at scale](./context-governance-at-scale.md) | Shared sources need one version, a registry of consumers, a trust label, and access rules | Could two of our features contradict each other today, and could untrusted text reach one of them? |
| [Evaluating context quality](./evaluating-context-quality.md) | Grade whether the context was right, clean, and conflict-free, separately from whether the answer was good | Did we check the context before we started rewriting the prompt? |
| [Context across the product lifecycle](./context-across-the-product-lifecycle.md) | Context work has a different job at discovery, delivery, and launch | Did we audit context before scoping behavior, or discover the gaps after launch? |

**The through-line:** almost every AI quality problem that gets escalated as "the model
is bad" is, on inspection, a context problem wearing a model problem's clothes. The
model answered exactly as well as it could with what it was shown; the fix was never in
the model, it was in what got assembled in front of it. Product leaders who internalize
this stop funding bigger models and cleverer prompts to solve problems that were never
either one's to solve, and start funding the unglamorous, high-leverage work — retrieval
quality, memory scoping, governance, and a spec that names context requirements out
loud — that actually moves the number. The same leaders also learn to remove context:
more is not better, and the best context is the smallest set that makes the decision
right.

> **Walk-away question:** *"The next time an AI feature gives a wrong answer, will the
> first question in the room be 'what did the model see?' — or will it be 'let's rewrite
> the prompt'?"*

If it's the first, this module did its job. If it's the second, you now know exactly
which lesson to reread — and which of the four context inputs to go check first.
