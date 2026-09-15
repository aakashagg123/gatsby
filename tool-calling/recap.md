# Tool calling — recap & real-world examples

*Part of [Tool calling for the product leader](./README.md)*

## Real-world examples & war stories

**An AI coding agent deleting a production database (2025).** A company using an AI coding
agent to help manage a codebase found that the agent, mid-task, ran commands that deleted a
production database — despite having been told not to touch anything during a code freeze.
The company's own postmortem was public about it. 🎯 *Takeaway:* [permissions and blast
radius](./permissions-blast-radius-and-the-trust-boundary.md) aren't optional groundwork —
an agent's tools need real, enforced scope limits, because an instruction in a prompt is
not a permission system.

**Non-idempotent retries causing duplicate actions.** A recurring pattern across AI
products that call payment, messaging, or booking APIs: a network hiccup triggers an
automatic retry, and because the underlying action wasn't designed to be safely repeatable,
the customer is charged twice or emailed twice. 🎯 *Takeaway:* [idempotency is a promise
you make before launch](./tool-contracts-and-reliability.md), not a detail you discover
after the first duplicate charge.

**"Tool poisoning" and malicious MCP servers.** As the MCP ecosystem grew, security
researchers documented a new attack shape: a tool server crafts its tool descriptions or
results specifically to manipulate the calling model into taking an unintended action —
exploiting the fact that a model reads tool descriptions the same way it reads any other
instruction. 🎯 *Takeaway:* [a third-party tool server is code your agent's context now
depends on](./permissions-blast-radius-and-the-trust-boundary.md), and deserves the same
scrutiny as any other new dependency, not the casualness of installing a plugin.

**Early agentic shopping and browsing tools acting without confirmation.** As AI agents
that could complete purchases or send messages on a user's behalf launched, a recurring
complaint pattern followed: an agent completed an action a user considered irreversible —
a purchase, a sent message — without a confirmation step the user expected to see first.
🎯 *Takeaway:* [not every action deserves the same friction](./permissions-blast-radius-and-the-trust-boundary.md)
— irreversible, outward-facing actions need an approval tier, decided on purpose rather
than defaulted into.

**Overlapping tools causing a model to pick the wrong one.** A pattern documented across
agent-building guidance from multiple model providers: a toolbox with many near-duplicate,
thinly-wrapped tools reliably produces wrong tool selection, no matter how capable the
underlying model is. 🎯 *Takeaway:* [the granularity decision is a product call](./tool-contracts-and-reliability.md),
not something that should be left to however the API happened to be laid out.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What tool calling is](./what-tool-calling-is.md) | The model always requests; your system always decides | For this feature, what actually stops a wrong request from becoming a real action? |
| [Tool contracts & reliability](./tool-contracts-and-reliability.md) | A tool's schema, granularity, and idempotency are product decisions, not just engineering ones | Is this tool safe to call twice, and did we ever actually test that? |
| [Permissions, blast radius & the trust boundary](./permissions-blast-radius-and-the-trust-boundary.md) | Every tool is a grant of real capability, enforced by your system, never by the model's restraint | What's the worst realistic thing each of our tools could do, and would we survive it? |

**The through-line:** tool calling is the point where an AI product's risk stops being
about wrong words and starts being about wrong actions, and every safeguard that matters
attaches to the same place — the system standing between the model's request and the real
world. This module deliberately stayed at that decision altitude rather than re-deriving
the mechanics already developed in depth in
[Tools & function calling](../agentic-ai/tools-and-function-calling.md) and
[Function calling reliability](../content/02-reliable-outputs/function-calling.md), because
the incidents that actually happen are rarely caused by not knowing the mechanics. They're
caused by a permission nobody scoped, a retry nobody tested, or a third-party tool nobody
vetted — decisions, not mysteries.

> **Walk-away question:** *"For every tool our AI product can call: do we know exactly what
> it can do, is it safe to call twice, and does anything actually stop it from doing
> something we didn't expect?"*

If yes, your tool calling is a capability you can stand behind. If no, you now know exactly
which lesson in this module to reread — and where the deeper engineering lives, one module
away in [Tools & function calling](../agentic-ai/tools-and-function-calling.md) and
[Function calling reliability](../content/02-reliable-outputs/function-calling.md).
