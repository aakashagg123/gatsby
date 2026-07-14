# Motivation theory: friction, satisfaction, and nudges

*Part of [Product sense for the AI PM](./README.md)*

## TL;DR

Users act when **motivation is high and friction is low** — the Fogg behaviour model puts
it as *Behaviour = Motivation × Ability × Trigger*. Product sense starts with reading that
equation in your own product: hunt down needless friction, make the core action
**rewarding** so satisfaction feeds motivation (the Hook model's Trigger → Action → Reward
→ Investment loop), and use **ethical nudges** — defaults, reminders, social proof — to make
the beneficial path the path of least resistance. The discipline is *conscious* friction:
add it only where it creates value, remove it everywhere else.

> 🎯 **For the AI PM**
>
> **Why it matters** — AI features fail less often because the model is dumb and more often
> because users never build the habit: the magic moment is buried behind friction, or the
> first output disappoints and they never return. The behaviour equation is how you find
> that gap.
>
> **What it changes in your decisions** — You measure and remove steps between "user arrives"
> and "user feels the model's value," and you design the *reward* after the first successful
> prompt as deliberately as the model itself.
>
> **Ask yourself** — *"What is the friction between a new user and their first genuinely
> useful model output — and how fast does that first win arrive?"*
>
> **Risk if ignored** — A technically impressive model with great demos and terrible
> retention, because nobody engineered the motivation-and-friction path around it.

## The behaviour equation

The **Fogg behaviour model** — *B = M × A × T* — says a behaviour happens only when
motivation, ability (ease), and a trigger converge. As a multiplication, if any term is
near zero, the behaviour doesn't happen. The practical corollary: **if you want to
encourage an activity, make it easy.** High friction — complex steps, confusing UI — stifles
even a motivated user; reducing friction lets existing motivation convert into action.

Picture a fintech signup. The motivation is there (the user *wants* the savings account),
but a 10-field form with poor guidance means many abandon — friction overrides motivation.
A 2-field signup or a federated login lets that motivation translate into action. So map
the journey, **measure drop-off at each step**, and prioritize the steps where users
struggle.

**But not all friction is bad.** A little friction can ensure quality or commitment — an
email verification yields a higher-quality user base; a confirmation step prevents costly
mistakes. The principle is **conscious friction**: add it only when it adds value
(security, thoughtfulness, safety) and eliminate it when it doesn't.

## Satisfaction and habit

**Satisfaction** is the fulfilment a user gets from your product — and it's what turns a
one-time user into a returning one, because a satisfying experience *increases* intrinsic
motivation to come back. Satisfaction and motivation are a loop, not two separate things.

Nir Eyal's **Hook model** shows how that loop hardens into a habit:

```
   ┌─────────▶ TRIGGER ──▶ ACTION ──▶ REWARD ──▶ INVESTMENT ──┐
   │            (cue)      (do it)   (payoff)   (put in effort) │
   └──────────────────────  habit forms  ─────────────────────┘
```

The **reward** phase is where satisfaction lands — a sense of accomplishment, useful
information, delight. That burst reinforces the behaviour; then the **investment** phase
(the user adds data, preferences, effort) raises commitment and loads the next trigger. So
ask: *what is actually rewarding about our core action?* Make sure each critical action is
followed by clear value or positive feedback — a friendly confirmation, a progress bar, a
checkmark. A satisfied user tolerates minor friction; a frustrated one drops off at the
first hurdle.

## Nudges — influence without coercion

**Nudges** are subtle design cues that steer behaviour *without restricting choice* (Thaler
& Sunstein). Common techniques:

| Nudge | How it works | Example |
| --- | --- | --- |
| **Defaults** | People stick with the pre-selected option | Sensible option pre-checked |
| **Prompts & reminders** | External trigger when motivation is likely | "It's been a week since your last workout" |
| **Social proof** | Herd behaviour builds trust | "Join 5,000+ peers using this" |
| **Gamification** | Streaks, points, badges boost motivation | Progress streaks |
| **Framing & personalization** | Highlight the benefit; tailor the choice | "Recommended for you" |

The rule is **ethics first**: the goal is to help users reach *their* goals with less
friction, not to manipulate them toward *your* metrics. Always ask, *"is this nudge helping
the user, or just helping us?"* Ethical nudges build trust; dark patterns destroy it.
LinkedIn's profile-completeness bar is the canonical good nudge — it shows progress and
rewards a "100% complete" state that genuinely benefits the user.

## Actionable steps

- **Identify friction hotspots** — map the journey, find drop-off, simplify (fewer fields,
  tooltips, cleaner navigation).
- **Engineer quick wins** — make new users hit the core value within the first minutes.
- **Add one ethical nudge** where users hesitate — a friendly default, a timely reminder,
  social proof — and watch both usage *and* sentiment.
- **Measure satisfaction** at key touchpoints (NPS, CSAT); where it's low, look for
  friction; where it's high, amplify the moment.
- **Run a behavioural-design audit** on new features: does the copy and flow reduce needless
  friction and reward the right action?

## Failure modes

- **Friction you never measured** — the drop-off is in a step you assumed was fine; instrument
  it before you defend it.
- **Action without reward** — users complete the core action and feel nothing, so no habit
  forms.
- **Manipulative nudges** — short-term metric wins that erode trust (the dark-pattern trap).
- **Frictionless where friction was protecting quality** — removing a confirmation that
  prevented costly errors.

## Practitioner checklist

- [ ] Have I mapped the journey and *measured* drop-off at each step, not guessed it?
- [ ] Does a new user reach a genuine "win" within the first few minutes?
- [ ] Is each critical action followed by a clear reward or positive feedback?
- [ ] Is every nudge in the product defensibly in the *user's* interest?
- [ ] Have I removed friction that serves no purpose — and kept the friction that protects
      quality or safety?

## Related lessons

- [Cognitive empathy](./cognitive-empathy.md)
- [Product sense for AI products](./product-sense-for-ai.md)
- [Communication](./communication.md)
