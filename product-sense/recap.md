# Product sense — recap & real-world examples

*Part of [Product sense for the AI PM](./README.md)*

<!-- voice: human -->

This page pulls the module together. It starts with real cases where the ideas showed up, then a
table with one idea and one decision per lesson, and it ends with a self-test you can use to check
what stuck.

## Real-world examples & war stories

**Amazon's Kindle vision and Working Backwards.** "Our vision for Kindle is every book ever printed in any
language, all available in less than 60 seconds." That is a vision specific enough to settle
arguments about scope. Amazon's Working Backwards process, as Werner Vogels describes it, defines a
product by writing the press release first and then the FAQ. Strong [communication
artifacts](./communication.md) turn product sense into alignment, and for an AI feature full of
uncertainty, a plain statement of what it is, what it isn't and how you'll know it worked is worth
more than any demo.

**Duolingo's Streak Freeze.** Duolingo's streak pushes learners to practise every day, and its
Streak Freeze lets a learner pause the streak for a day rather than lose it. That makes it an
[ethical nudge](./motivation-and-behaviour.md) rather than a dark pattern, because the line between
the two is whose goal the nudge serves. AI products cross that line easily when they optimise
engagement against the user's interest.

**Kodak and the digital camera.** Kodak invented the digital camera in 1975 and is remembered as the
company that missed digital, which makes it the usual warning about [intellectual
flexibility](./cognitive-empathy.md) and the sunk-cost fallacy. Scott Anthony argues that the
subtleties of what actually happened are being forgotten, so treat the short version as a prompt
rather than as history. The trap it points at is attachment to a winning bet, and in a field moving
as fast as AI, being willing to say "the ground shifted, so we should too" is a survival skill.

**The expert's trap in domain-heavy products.** Marty Cagan's warning that experts come to believe
they are more like their target customer than they really are applies from medical software to
developer tools. [Domain expertise](./domain-expertise.md) only pays off when it's paired with the
outsider's question of why something is done this way at all, and that same humility keeps an AI PM
checking the model's confidence, and their own.

## Three heuristics worth keeping

These are this module's own framing, three rules of thumb that tie the lessons together.

**"What is the user's goal, and how hard does this product make it?"** It is a two-question quality
model that needs no dashboard. Book a good place fast, get a car fast, find the
answer fast. Before any metric review, walk the product as a user with a goal and count the friction,
which is [motivation theory](./motivation-and-behaviour.md) compressed into a gut check.

**High-quality products do one thing exceptionally well.** Spread across many
domains, you're replaceable, while being exceptional at one makes you a category. It is the
[focused-strategy](./creativity.md) discipline stated as a quality bar, and it applies doubly to AI
products, where the reliable frontier is narrow.

**Product sense is built by dissection.** Close attention to detail, taking apart what
makes something good and what makes something not good, is how pattern-matching intuition gets
trained. It pairs with the [talk-to-your-users](./cognitive-empathy.md) habit, since exposure
supplies the patterns and dissection compresses them into taste.

## Module recap

| Lesson | The one idea | The decision it drives |
| --- | --- | --- |
| [Motivation theory](./motivation-and-behaviour.md) | Behaviour needs motivation, ability and a prompt together (B = MAP) | Where to cut friction and how to reward the core action |
| [Cognitive empathy](./cognitive-empathy.md) | Simulate the user, and doubt your own certainty | Which assumptions to test before you build |
| [User research](./user-research.md) | Trust what people did over what they predict | Which method fits the question, and how big a sample it needs |
| [Creativity](./creativity.md) | Strategy picks the battle, and execution wins it | What to focus on, and what to say no to |
| [Communication](./communication.md) | Product sense you can't convey can't move a team | How to earn buy-in and check that alignment is real |
| [Domain expertise](./domain-expertise.md) | Knowledge turns guessing into knowing | Which features truly matter in this world |
| [Product sense for AI](./product-sense-for-ai.md) | The material is probabilistic | Where a model beats a deterministic feature, and how to stay trustworthy |

**The through-line.** Product sense is six habits that compound rather than one talent. You read
behaviour, simulate the user, find out instead of guessing, choose a focused strategy, communicate
it, and ground it in domain reality. For the AI PM, the capstone puts all six to work on a new kind
of material, powerful, probabilistic and sometimes confidently wrong. The *product* is the
trustworthy system you build around the model.

> **Walk-away question:** *"For the job in front of me, what does the user actually want to
> achieve, and if I'm reaching for a model, does it serve that job better than a simpler, more
> predictable solution?"*

---

← Back to [module overview](./README.md)

## Test yourself

Eleven questions, at least one per lesson. The answers fold out, and each links back to its lesson.

1. **A feature has high motivation and a clear prompt, but users still don't act. What do you look at first?**
   <details><summary>Answer</summary>Ability, which in practice means friction. With B = MAP, if motivation and the prompt are present, ability is the bottleneck. Measure each step and remove the needless ones before you add more motivation. (<a href="./motivation-and-behaviour.md">Motivation & behaviour</a>)</details>
2. **Marketing wants three more fields on the signup form. How do you decide?**
   <details><summary>Answer</summary>Ask who each field serves. A field that protects the user is conscious friction and can stay. A field that only serves another team's data needs is selfish friction, so defer it until after the user's first win, or drop it. (<a href="./motivation-and-behaviour.md">Motivation & behaviour</a>)</details>
3. **Your team is sure the new onboarding step is obvious. What do you do before launch?**
   <details><summary>Answer</summary>Write the belief down as an assumption, ask what would prove it wrong, and watch a handful of first-time users try it with no instructions. Expert fluency is the curse of knowledge at work, so don't treat it as evidence. (<a href="./cognitive-empathy.md">Cognitive empathy</a>)</details>
4. **Why does "would you use this?" produce worse data than "tell me about the last time you…"?**
   <details><summary>Answer</summary>People are unreliable at predicting their own behaviour and much better at recalling what they did. A story about a past event gives you behaviour, while a hypothetical gives you a polite guess. (<a href="./user-research.md">User research</a>)</details>
5. **One colleague says five users is enough, another says twenty interviews plus a survey. Who's right?**
   <details><summary>Answer</summary>It depends on the question. Five users per round finds most problems in a usability test with similar users. Learning which needs are common across a market takes more conversations and a survey to size them. (<a href="./user-research.md">User research</a>)</details>
6. **You built one AI prototype this afternoon and it works. What should happen next?**
   <details><summary>Answer</summary>Build a few genuinely different alternatives, test each with a handful of users, and choose on evidence. A prototype that works first time is the easiest one to fall for. (<a href="./creativity.md">Creativity</a>)</details>
7. **Why keep the "new" part of a product isolated from the proven and better parts?**
   <details><summary>Answer</summary>So that if it fails, you know the idea failed rather than the basics around it. Mixing a novel idea with clumsy versions of everything users expect makes the result impossible to read. (<a href="./creativity.md">Creativity</a>)</details>
8. **A model drafted your one-pager and it reads well. What do you check before sending it?**
   <details><summary>Answer</summary>Mark every factual claim and check each against evidence you actually have. Look for small errors, invented metrics and stakeholder motives nobody confirmed, then turn the unsupported claims into open questions. (<a href="./communication.md">Communication</a>)</details>
9. **When is deep domain expertise a liability, and what's the antidote?**
   <details><summary>Answer</summary>When it becomes "I am the user" and validation stops. The antidote is to pair expertise with the outsider's question of why it's done this way at all, and to keep talking to users. (<a href="./domain-expertise.md">Domain expertise</a>)</details>
10. **Your AI feature demos beautifully. What does "taste becomes evals" say you must do before trusting it?**
    <details><summary>Answer</summary>Turn your judgment of "good" into a graded, representative eval set and run it continuously. Read traces and call pass or fail yourself, because a demo can't show you a distribution. (<a href="./product-sense-for-ai.md">Product sense for AI</a>)</details>
11. **Your assistant scores 91% on its eval, and every eval question has an answer in the documents. What's missing?**
    <details><summary>Answer</summary>Cases where the right answer is "I don't know". Without them, the eval can't see the model inventing answers, which is the failure that hurts users most. (<a href="./product-sense-for-ai.md">Product sense for AI</a>)</details>

## Sources

- Amazon, [*Kindle at 10*](https://www.aboutamazon.com/news/devices/kindle-at-10), About Amazon,
  19 November 2017 (as of 2026-11).
- Werner Vogels, [*Working Backwards*](https://www.allthingsdistributed.com/2006/11/working_backwards.html),
  All Things Distributed, 1 November 2006 (as of 2026-11).
- Jakob Nielsen, [*Why You Only Need to Test with 5
  Users*](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/), Nielsen Norman
  Group, 18 March 2000 (for question 5) (as of 2026-11-27).
- Joanna Goodrich, [*The First Digital Camera Was the Size of a
  Toaster*](https://spectrum.ieee.org/first-digital-camera-history), IEEE Spectrum, 6 April 2022, and
  Scott D. Anthony, [*Kodak's Downfall Wasn't About
  Technology*](https://hbr.org/2016/07/kodaks-downfall-wasnt-about-technology), Harvard Business
  Review, 15 July 2016 (as of 2026-11).
- Marty Cagan, [*The Role of Domain Experience*](https://www.svpg.com/the-role-of-domain-experience/),
  SVPG, 28 March 2005 (as of 2026-11).
- Duolingo, [*How the Duolingo streak builds habit*](https://blog.duolingo.com/how-duolingo-streak-builds-habit/),
  31 January 2022 (Streak Freeze pauses a streak for a day) (as of 2026-11-26).
