# Reliable outputs & tool use — recap & real-world examples

*Part of [02 · Reliable Outputs & Tool Use](./README.md)*

## Real-world examples & war stories

**The $1 Chevy Tahoe (December 2023).** A Chevrolet dealership's ChatGPT-powered website
bot was prompt-injected by users into "agreeing" to sell a Tahoe for $1 and stating the
offer was "legally binding, no takesies-backsies." It went viral. 🎯 *PM takeaway:* never
let raw model output be *authoritative* for a commitment or action — that's
[guardrails](./agent-guardrails.md) plus [tool-side authority](./function-calling.md),
and it's exactly what [adversarial evals](../04-evals-observability/evals.md) exist to
catch before launch.

**DPD's bot swears at a customer (January 2024).** After a system update, the parcel
company's chatbot was goaded into swearing and writing a poem about how terrible DPD is.
The clip spread widely. 🎯 *PM takeaway:* a model update is a *change that needs
regression + adversarial testing* and live [guardrails](./agent-guardrails.md) — "it
worked before the update" is not a safety property.

**Air Canada must honor its bot's invented policy (2024).** A tribunal held the airline
responsible after its chatbot fabricated a bereavement-refund policy. 🎯 *PM takeaway:*
ungrounded, unvalidated output is a *liability*, not just a bad answer — push toward
[structured, grounded responses](./structured-output.md) and own what the AI says.

**The industry standardizes structured output.** Providers shipped JSON mode,
function-calling schemas, and constrained/structured decoding precisely because
"usually-valid JSON" kept breaking real workflows. 🎯 *PM takeaway:* schema validation +
repair + fallback is now table stakes, not a nice-to-have. See
[structured output](./structured-output.md).

## Module recap

| Lesson | The one idea | The decision it drives |
| --- | --- | --- |
| [Structured output](./structured-output.md) | Treat output as untrusted: validate → repair → fall back | Integration commitments; error budget |
| [Function calling](./function-calling.md) | Tools cause effects; demand contracts + idempotency | What the AI may do autonomously |
| [Agent guardrails](./agent-guardrails.md) | Loops need budgets and termination | Whether to ship agents; cost ceilings |
| [Model routing](./model-routing.md) | Decouple reliability/cost from any one model | Vendor strategy; the SLA you can offer |

**The through-line:** **never trust model output as if it were a typed return value.**
Validate it, bound it, authorize it, and have a fallback. Reliability is a property your
[harness](../00-foundations/harness-engineering.md) provides — the model is a brilliant,
manipulable, occasionally-wrong component in the middle.

> **Walk-away question:** *"When the model is wrong — and it will be — what catches it
> before the user, the database, or the press does?"*

---

← Back to [module index](./README.md) · → Next module: [03 · RAG & Retrieval](../03-rag/README.md)
