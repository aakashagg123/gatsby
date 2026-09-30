# Memory & context — recap & real-world examples

*Part of [Memory & context for the product leader](./README.md)*

## Real-world examples & war stories

**ChatGPT memory shipped with controls (2024).** In February 2024 OpenAI began testing a
memory feature for ChatGPT with a small share of users. Users could tell it to remember or
forget something, view what it remembered, and turn memory off. 🎯 *Takeaway:* ship
visibility and control with the capability, not after it. See
[memory as a product decision](./memory-as-a-product-decision.md). The date and controls
come from press coverage in search results. OpenAI's own page could not be opened.

**A caching bug showed one user's data to another (2023).** On March 20, 2023, a bug in an
open-source library used by ChatGPT let some users see other users' chat titles. OpenAI
said a small share of ChatGPT Plus subscribers could also see some billing details. It
took the service offline to fix it. 🎯 *Takeaway:* a leak needs no attacker. Any shared
store can cross a boundary under load. Enforce the boundary in the system, and
[test it directly](./when-memory-goes-wrong.md). This was a caching fault, not a memory
feature. Details come from press coverage in search results.

**A planted memory that kept working (2024).** Security researcher Johann Rehberger showed
that a crafted web page or document could get ChatGPT to save a hostile instruction in its
long-term memory. The instruction sent later conversations to an outside server. OpenAI
released a partial fix, and the work was published in September 2024. 🎯 *Takeaway:* if a
model can write to memory, an injection can outlive the session. Hold writes from
untrusted content for confirmation. See
[poisoning](./when-memory-goes-wrong.md#poisoning-a-planted-memory-that-keeps-working) and
[the write path](./writing-and-maintaining-memory.md). Details come from press coverage
in search results.

**Who owns the store (Claude API).** The Claude memory tool runs on the developer's side.
Claude asks for a file operation, and the application performs it. Anthropic's docs say
memory "lives entirely in your application," and put path checks, size caps and expiry on
the developer. 🎯 *Takeaway:* you own the store, and so you own its boundary and its
deletion duty. See [session, user & organizational memory](./session-user-and-organizational-memory.md).

**The stale preference (an illustration).** A shopping assistant learns "vegetarian" in
January. In June the customer starts eating fish and says so, but the store only appends.
Retrieval returns the January note first, and the assistant keeps offering vegetarian
options. Nothing crashed. 🎯 *Takeaway:* staleness is a write-path problem. Give facts a
replace rule and a review date. See [writing and maintaining memory](./writing-and-maintaining-memory.md).

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [Memory as a product decision](./memory-as-a-product-decision.md) | Memory is a set of promises you choose to make, not a free default. | What do we remember, for whom, for how long, and who can edit it? |
| [Session, user & organizational memory](./session-user-and-organizational-memory.md) | Three shapes carry three different stakes. Name the shape first. | Which shape is this, and is the boundary enforced by the system? |
| [Writing and maintaining memory](./writing-and-maintaining-memory.md) | Memory quality is set when a memory is written. | What happens to the old fact when a new one contradicts it? |
| [Retrieval as memory](./retrieval-as-memory.md) | Load, retrieve, or keep notes. Pick by size and kind of data. | Is this small enough to load, large enough to search, or task progress? |
| [When memory goes wrong](./when-memory-goes-wrong.md) | Stale, leaked, uncorrectable and poisoned memory each need a test. | Would monitoring find a memory failure, or would a user? |

**The through-line:** memory is never something a model gives you. Your product builds it
as a set of promises. The mistakes that sink memory features are rarely engineering
mistakes. They are decisions nobody made: a shape left unnamed, a boundary assumed instead
of tested, a write path with no rule, a deletion path never built. The engineering depth
lives in [Context engineering](../content/00-foundations/context-engineering.md) and
[Context & memory](../agentic-ai/context-and-memory.md). This module stays at the decision
altitude.

> **Walk-away question:** *"For our AI feature's memory: could we tell a user exactly what
> we remember, could they see and correct it, do we have a rule for how memories are
> written and expire, and have we tested the boundary against the store, not just the
> chat?"*

If yes, this is a memory feature your product can stand behind. If no, you know which
lesson to reread.

## Test yourself

1. **Why is memory a product decision and not a default?**
   <details><summary>Answer</summary>The model keeps nothing between calls. Your team builds every bit of memory, and it makes promises about what is kept and for how long. It has a cost and a risk that someone must own. (<a href="./memory-as-a-product-decision.md">Lesson 1</a>)</details>
2. **What are the four parts of the question that scopes a memory feature?**
   <details><summary>Answer</summary>What is remembered, for whom, for how long, and who can see or edit it. If any part is "we will decide later", the feature is not ready to build. (<a href="./memory-as-a-product-decision.md">Lesson 1</a>)</details>
3. **Name the three memory shapes and the main risk of each.**
   <details><summary>Answer</summary>Session memory (low risk, may be dropped when a long chat is summarised). User memory (a personal data store with duties to show, correct and delete). Organizational memory (the boundary of who is inside). (<a href="./session-user-and-organizational-memory.md">Lesson 2</a>)</details>
4. **Why must the identity used to filter memories come from the session and not from the model?**
   <details><summary>Answer</summary>A model can be tricked into asking for another user's data. The store must filter by the authenticated caller before anything reaches the model. (<a href="./session-user-and-organizational-memory.md">Lesson 2</a>)</details>
5. **A user says "I moved to Pune." The store says "lives in Delhi." What should the write policy do?**
   <details><summary>Answer</summary>Replace the old value, because the newer fact wins, and keep the old one in history for audit. If the change is ambiguous or sensitive, ask the user. (<a href="./writing-and-maintaining-memory.md">Lesson 3</a>)</details>
6. **A user has forty stable preferences and three years of chat history. How do you serve each?**
   <details><summary>Answer</summary>Load the forty preferences directly on every request. Search the history and add only the few relevant pieces. Filter to the user's own records before ranking. (<a href="./retrieval-as-memory.md">Lesson 4</a>)</details>
7. **How is memory poisoning different from an ordinary prompt injection?**
   <details><summary>Answer</summary>An ordinary injection ends when the session ends. If it writes itself into memory, it persists and acts in later sessions. Defend by holding writes from untrusted content for confirmation. (<a href="./when-memory-goes-wrong.md">Lesson 5</a>)</details>
8. **Why is asking the chatbot "do you know other users' data?" a weak leakage test?**
   <details><summary>Answer</summary>The model may refuse while the store still returns the data. Test the store directly, as an attacker would. (<a href="./when-memory-goes-wrong.md">Lesson 5</a>)</details>

## Sources

- OpenAI, [Memory and new controls for ChatGPT](https://openai.com/index/memory-and-new-controls-for-chatgpt/)
  (Feb 2024). Confirmed through press coverage in search results; the page could not be
  opened when this recap was written.
- OpenAI, [March 20 ChatGPT outage: here's what happened](https://openai.com/index/march-20-chatgpt-outage/)
  (Mar 2023). Same status: search results only.
- Johann Rehberger, ChatGPT long-term memory injection research (Sep 2024). Press coverage
  in search results only.
- Anthropic, [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
  (Claude API docs). Checked 2026-09.
- The stale-preference story is an invented illustration.

---

← Back to [module overview](./README.md)
