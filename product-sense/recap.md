# Product sense — recap & real-world examples

*Part of [Product sense for the AI PM](./README.md)*

## Real-world examples & war stories

**Slack's behavioural segmentation.** Rather than "team communication for everyone," Slack
targeted engineering teams already chatting in IRC — a segment defined by *behaviour*, not
demographics — and won a beachhead that then expanded. 🎯 *Takeaway:* the sharp
[strategic-thinking](./creativity.md) move is segmenting by what people already *do*, which
is exactly the instinct an AI PM needs to find the job a model reliably nails.

**Amazon's Kindle vision and the PRFAQ.** *"Every book ever printed, in any language, all
available in under 60 seconds"* is a vision that made thousands of decisions for the team;
the PRFAQ format forced every proposal to start from the customer. 🎯 *Takeaway:* strong
[communication artifacts](./communication.md) turn product sense into alignment — and for an
AI feature drowning in uncertainty, an explicit "what it is / isn't / how we'll know it
worked" is worth more than any demo.

**LinkedIn's profile-completeness bar.** A progress nudge that shows how far you've come and
rewards a "100%" state that genuinely benefits the user — an [ethical nudge](./motivation-and-behaviour.md),
not a dark pattern. 🎯 *Takeaway:* the line between a helpful nudge and a manipulative one is
"whose goal does it serve?" — a line AI products cross easily when optimizing engagement
metrics against user interest.

**Kodak and the digital camera.** Kodak *invented* the digital camera and clung to film
anyway — a failure of [intellectual flexibility](./cognitive-empathy.md) and the sunk-cost
fallacy, not a lack of evidence. 🎯 *Takeaway:* the incumbent's trap is emotional attachment
to a winning bet; in a field moving as fast as AI, the willingness to say "the ground
shifted, so we should too" is a survival skill.

**Air Canada's chatbot invented a refund policy (2024).** A support bot confidently stated a
refund policy that didn't exist, and a tribunal made the airline honor it. 🎯 *Takeaway:* the
canonical [product-sense-for-AI](./product-sense-for-ai.md) failure — a confidently-wrong
output with no grounding, no "I don't know," and full authority in the UX. The fix was
architectural (answer only from real policy, with citations), which is a *product* decision
before it's an engineering one.

**The "expert's trap" in domain-heavy products.** Marty Cagan's warning that experts assume
they *are* the user shows up everywhere from EMRs to developer tools. 🎯 *Takeaway:*
[domain expertise](./domain-expertise.md) is a turbocharger only if paired with the outsider
question "why is it done this way at all?" — the same humility that keeps an AI PM validating
instead of trusting the model's (or their own) confidence.

## Field notes from working PMs

Three durable heuristics from PM-interview collections (Carl Shan's *Product Manager
Handbook* interviews with PMs at Google, Twitter, Facebook, Yammer):

**"What is the user's goal — and how hard does this product make it?"** (Jason Shah,
Yammer). The two-question quality model that needs no dashboard: book a good place fast,
get a car fast, find the answer fast. 🎯 *Takeaway:* before any metric review, walk the
product as a user with a goal and count the friction — it's [motivation theory](./motivation-and-behaviour.md)
compressed into a gut check.

**High-quality products do one thing exceptionally well** (Avichal Garg, Facebook).
Spread across many domains, you're replaceable; exceptional at one, you're a category.
🎯 *Takeaway:* the same [focused-strategy](./creativity.md) discipline, stated as a
quality bar — and doubly true for AI products, where the reliable frontier is narrow.

**Product sense is built by dissection** (Garg again). Extreme attention to detail —
dissect what makes something good and what makes something not good — is how
pattern-matching intuition is trained. 🎯 *Takeaway:* pairs with the
[talk-to-your-users](./cognitive-empathy.md) mechanism: exposure supplies the patterns,
deliberate dissection compresses them into taste.

## Module recap

| Lesson | The one idea | The decision it drives |
| --- | --- | --- |
| [Motivation theory](./motivation-and-behaviour.md) | Behaviour = motivation × ability × trigger | Where to cut friction and how to reward the core action |
| [Cognitive empathy](./cognitive-empathy.md) | Simulate the user; doubt your own certainty | Which assumptions to test before you build |
| [Creativity](./creativity.md) | Strategy picks the battle; execution wins it | What to focus on — and what to say no to |
| [Communication](./communication.md) | Product sense you can't convey can't move a team | How to earn buy-in and keep everyone aligned |
| [Domain expertise](./domain-expertise.md) | Knowledge turns guessing into knowing | Which features truly matter in this world |
| [Product sense for AI](./product-sense-for-ai.md) | The material is probabilistic | Where a model beats a deterministic feature — and how to stay trustworthy |

**The through-line:** product sense is not one talent but five habits that compound —
reading behaviour, simulating the user, choosing a focused strategy, communicating it, and
grounding it in domain reality. For the AI PM, a sixth habit sits on top: knowing that the
model is a new kind of material — powerful, probabilistic, and confidently wrong — and that
the *product* is the trustworthy system you build around it, not the model itself.

> **Walk-away question:** *"For the job in front of me, what does the user actually want to
> achieve — and if I'm reaching for a model, does it genuinely serve that job better than a
> simpler, more predictable solution?"*

---

← Back to [module overview](./README.md)

## Test yourself

Five questions; answers fold out. If one stumps you, the link takes you back.

1. **A feature has high motivation and a strong trigger but users still don't act. What's the first suspect, per the behaviour equation?**
   <details><summary>Answer</summary>Ability — friction. B = M × A × T: if two factors are present, the third is the bottleneck. Hunt the needless steps before adding more motivation. (<a href="./motivation-and-behaviour.md">Motivation & behaviour</a>)</details>
2. **Why does "would you use this?" produce worse data than "tell me about the last time you…"?**
   <details><summary>Answer</summary>People are unreliable futurists but decent historians — statements about hypothetical behaviour barely predict real behaviour; accounts of past behaviour do. (<a href="./user-research.md">User research</a>)</details>
3. **What's the one-question test for whether a nudge is ethical?**
   <details><summary>Answer</summary>"Whose goal does it serve?" A nudge aligned with the user's own goal is help; one serving only the metric is a dark pattern. (<a href="./motivation-and-behaviour.md">Motivation & behaviour</a>)</details>
4. **Your AI feature demos beautifully. What does "taste becomes evals" say you must do before trusting it?**
   <details><summary>Answer</summary>Turn your judgment of "good" into a graded, representative eval set and run it continuously — read traces and call pass/fail yourself; a distribution can't be eyeballed from a demo. (<a href="./product-sense-for-ai.md">Product sense for AI</a>)</details>
5. **When is deep domain expertise a liability, and what's the antidote?**
   <details><summary>Answer</summary>When it becomes "I am the user" and validation stops. The antidote is pairing expertise with the outsider question — "why is it done this way at all?" — and continued user contact. (<a href="./domain-expertise.md">Domain expertise</a>)</details>
