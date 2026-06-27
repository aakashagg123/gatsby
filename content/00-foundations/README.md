# Module 00 · Foundations

The hardest part of AI engineering is not the model. It is everything *around* the
model: the control flow, the context you feed it, the validation you wrap it in,
and the operational discipline that turns a clever demo into a system people can
depend on.

This module establishes the three mindset shifts that the rest of the curriculum
assumes:

1. **[Harness engineering, not just prompt engineering](./harness-engineering.md)**
   — the value lives in the code around the model, not only the words you send it.
2. **[Context engineering, not just long prompts](./context-engineering.md)**
   — managing the context window is an active engineering problem, not "paste more."
3. **[Shipping LLM systems as infrastructure, not demos](./infra-not-demos.md)**
   — reliability, observability, and cost are features, not afterthoughts.

If you internalize only one idea from this whole repository, make it this: **a
production LLM feature is a distributed system with a stochastic component in the
middle.** Engineer it like one.

---

→ Next module: [01 · Inference Internals](../01-inference-internals/README.md)
