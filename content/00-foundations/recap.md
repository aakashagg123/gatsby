# Foundations — recap & real-world examples

*Part of [00 · Foundations](./README.md)*

## Real-world examples & war stories

**Samsung's source-code leak (2023).** Within weeks of allowing ChatGPT, Samsung
engineers pasted confidential source code and internal meeting notes into it to debug
and summarize — and that data left the company's control. Samsung restricted the tool.
🎯 *PM takeaway:* what data is *allowed into the context* — and where it then goes — is a
product and policy boundary you own. That's [harness](./harness-engineering.md), not
prompting.

**"Lost in the Middle" (Liu et al., 2023).** A widely-cited study showed models reliably
use information at the *beginning and end* of a long context but "lose" facts buried in
the middle — even when the answer is right there. 🎯 *PM takeaway:* "just give the model
more context" can *lower* quality. Placement and trimming are real work — see
[context engineering](./context-engineering.md).

**The POC graveyard.** Industry surveys repeatedly find that the large majority of
generative-AI proof-of-concepts never reach production. The demo works; the *operational*
version — evals, guardrails, monitoring, cost control — is where projects stall. 🎯 *PM
takeaway:* the demo-to-prod gap is mostly [harness and ops](./infra-not-demos.md). Budget
for it explicitly, or you'll relaunch the same demo three times.

## Module recap

| Lesson | The one idea | The decision it drives |
| --- | --- | --- |
| [Harness engineering](./harness-engineering.md) | Reliability lives in the code *around* the model | Where you spend eng cycles; what "AI quality" means |
| [Context engineering](./context-engineering.md) | The context window is a budget, not a junk drawer | Cost-per-call; data you make retrievable |
| [Infra, not demos](./infra-not-demos.md) | Demos are judged best-case; infra is judged worst-case | Launch-readiness; definition of done |

**The through-line:** a production LLM feature is *a distributed system with a stochastic
component in the middle.* Engineer it like one. The model is one fast, unreliable,
stateless function call; everything that makes it useful and safe — assembly, validation,
budgets, fallbacks, observability — is yours to build.

> **Walk-away question:** *"If the model returns garbage on a single call, what does the
> user actually see — and who would notice?"* If you can't answer it, your gap is in the
> foundations.

---

← Back to [module index](./README.md) · → Next module: [01 · Inference Internals](../01-inference-internals/README.md)
