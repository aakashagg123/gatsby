# Prompt engineering — recap & real-world examples

*Part of [Prompt engineering, from productivity to coding agents](./README.md)*

## Real-world examples & war stories

**The prompt no one owned.** A support team standardized on ChatGPT for reply drafting.
Everyone had a slightly different "good" prompt in their private notes, and every one
of them was five months old. Quality varied by author. The fix, embarrassingly cheap:
one saved, versioned prompt scaffold in a shared doc, revisited quarterly. 🎯
*Takeaway:* a prompt that lives in one person's ChatGPT sidebar is not an asset — it's
a single point of failure. Versioned scaffolds are the difference between "we use AI"
and "we use AI *reliably*."

**The model swap that fixed nothing.** A team blamed their retrieval feature's quality
on the model and moved from one provider to another over a weekend. Quality was
identical. The failure was a missing `<document>` boundary letting user-supplied text
override the instructions — a five-token structural fix that would have cost half an
hour, versus a weekend of migration work. 🎯 *Takeaway:* rule out prompt structure
before you rule in a model change. Structured prompting is often the "bigger model"
you were looking for.

**The single-prompt hero that couldn't scale.** An enterprise team tried to do
"extract action items, classify by urgency, then draft outreach emails" in one
1,400-token prompt. It worked on the demo dataset. On real inbox threads, it either
hallucinated priorities, drifted between two output shapes, or dropped emails
entirely. Splitting into a three-step chain — extract, classify, draft — took a
morning and fixed everything. 🎯 *Takeaway:* one prompt with two verbs is two
prompts pretending to be one, and the pretence breaks under real load.

**The coding agent that helpfully "cleaned up" the whole file.** A developer asked
a coding agent to "fix the null-pointer bug in this function." The agent fixed the
bug and reformatted 200 lines of surrounding code, renamed three unrelated variables,
and split the file into two. The PR was three days of code review for a
five-line fix. The prompt was missing one sentence: *"Do not touch any code outside
the named function."* 🎯 *Takeaway:* coding-agent prompts read like tickets to a
contractor who will do exactly what you wrote — and everything you didn't rule out
they'll also do, helpfully.

**The extraction that fabricated a due date.** A workflow pipeline extracted meeting
action items from transcripts. The model helpfully filled in a `due_date` when the
transcript never mentioned one, guessing "Friday" or "next week." Every downstream
Jira ticket got a plausible fake deadline. The fix was one sentence in the prompt:
*"If a field is not present in the transcript, use `null`. Do not invent values."*
🎯 *Takeaway:* the null contract is a required sentence in every extraction prompt.
Absence of it invites hallucination in exactly the slots you least want it.

**The agent that couldn't stop.** An internal research agent was set loose on
"find every mention of our competitor in the last quarter's earnings calls." Ten
minutes in, it had made 47 search calls and burned through the token budget without
producing an answer, because nothing in the prompt said when to stop. The fix:
*"After 10 searches, stop and summarize what you found, even if incomplete."* 🎯
*Takeaway:* termination is a prompt-engineering decision, not just a runtime cap.
The runtime cap is the safety net; the prompt is the intent.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What prompt engineering actually is](./what-prompt-engineering-actually-is.md) | You are steering a probability distribution, not talking to a person | If a colleague ran my prompt cold, would they get the same output? |
| [The anatomy of a prompt](./the-anatomy-of-a-prompt.md) | Six named parts: role, task, context, constraints, format, examples | Which of the six is my prompt leaving to the model to guess? |
| [Everyday productivity patterns](./everyday-productivity-patterns.md) | Six canonical shapes cover 80% of real work | Which of the six patterns is this task, and am I using its canonical shape? |
| [Structured prompting](./structured-prompting.md) | Structure is what stops the model confusing instructions for content | If the document tripled in length, would the model still know it's a document? |
| [Few-shot, CoT, self-consistency](./few-shot-cot-self-consistency.md) | Show, don't tell; think, don't guess; vote, don't gamble | Have I actually shown the model what "good" looks like, or only described it? |
| [Prompt chaining and workflows](./prompt-chaining-and-workflows.md) | Two verbs is two prompts | Am I asking one prompt to do two jobs at once? |
| [Prompting for tools and agents](./prompting-for-tools-and-agents.md) | Tool descriptions are API contracts; termination is a prompt decision | If two tools could plausibly serve, does the description say which one? |
| [Prompting inside coding agents](./prompting-inside-coding-agents.md) | The prompt is the spec; the project context file is the always-on system prompt | Does this prompt read like a ticket or a text message? |
| [When prompts fail: the diagnostic playbook](./when-prompts-fail.md) | Seven named failure modes with seven specific fixes | Which of the seven did this output fail into? |

**The through-line:** prompt engineering is not a set of clever tricks. It's a
craft with a small vocabulary — six prompt parts, six everyday patterns, three
reasoning techniques, one loop, seven failure modes — and the leverage comes from
knowing the vocabulary well enough to reach for the right piece under pressure. The
beginner uses one part unconsciously and gets a lucky output. The intermediate uses
all six on purpose. The advanced practitioner adds tools, chains, and coding agents,
and diagnoses failures against a shared list instead of blaming the model. The
[context engineering module](../context-engineering/README.md) is the layer above
this — what the prompt operates on. The [TPM for AI products
lesson](../technical-product-management/tpm-for-ai-products.md) is the layer above
that — how you evaluate whether the prompt is good enough to ship. This module is
the middle: the writing itself.

> **Walk-away question:** *"For the most important prompt in my current work — is
> it a versioned artifact I could hand a colleague cold, structured with named
> boundaries, matched to the right technique for its task, and diagnosable against
> the seven failure modes when it drifts?"*

---

← Back to [module overview](./README.md)

## Test yourself

1. **What are the six named parts of a prompt, in order?**
   <details><summary>Answer</summary>Role, task, context, constraints, format, examples. The order matters — role frames every later instruction; examples anchor the whole prompt. (<a href="./the-anatomy-of-a-prompt.md">The anatomy of a prompt</a>)</details>
2. **When should you reach for few-shot before reaching for a bigger model?**
   <details><summary>Answer</summary>Almost always. Three well-chosen examples often lift a smaller model above a bigger one at a fraction of the cost. Examples are the highest-leverage part of a prompt. (<a href="./few-shot-cot-self-consistency.md">Few-shot, CoT, self-consistency</a>)</details>
3. **What is the single sentence that stops a coding agent from touching files you didn't ask about?**
   <details><summary>Answer</summary>"Do not touch any file outside [the named ones]." Or the tighter version scoped to a function. Coding agents do exactly what the prompt allows — and everything else you didn't rule out. (<a href="./prompting-inside-coding-agents.md">Prompting inside coding agents</a>)</details>
4. **Why does structured prompting (XML tags) matter more in production than in a chat playground?**
   <details><summary>Answer</summary>User-supplied text in production can contain instructions the model may follow. Tagged boundaries make the model treat that text as content, not as an instruction. Structure also prevents drift when input length grows. (<a href="./structured-prompting.md">Structured prompting</a>)</details>
5. **When a prompt underperforms, what should you do before rewriting it?**
   <details><summary>Answer</summary>Diagnose which of the seven failure modes it hit. A targeted fix at the specific sentence that failed clears the failure without introducing a variant of the same problem in a rewrite. (<a href="./when-prompts-fail.md">When prompts fail</a>)</details>
