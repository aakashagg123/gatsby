# Building AI-native products — recap & real-world examples

*Part of [Building AI-native products](./README.md)*

*Last reviewed: 2026-10 · Volatility: fast*

## Real-world examples

**Eighteen guidelines for human-AI interaction (2019).** Researchers at Microsoft proposed 18 design guidelines for human-AI interaction and published them as an interactive library. They include "Make clear what the system can do", "Make clear how well the system can do what it can do", "Support efficient correction" and "Scope services when in doubt". 🎯 *Takeaway:* the practices in [designing for ambiguity](./designing-for-ambiguity.md) are written down and testable. Use them as a review checklist.

**Workflows and agents are different things (2024).** Anthropic's engineering team describes workflows as systems where models and tools follow code paths set in advance, and agents as systems where the model directs its own process and tool use. It advises finding the simplest solution and adding complexity only when it demonstrably improves outcomes, and notes that agents bring higher costs and the potential for compounding errors. 🎯 *Takeaway:* [start with a workflow](./designing-agentic-flows.md), and add agent freedom where the task needs it.

**Tool design is interface design (2024).** The same post reports that, for a coding benchmark, changing a tool so that it always required absolute file paths made the model use it flawlessly. It also advises giving tools the same prompt-engineering care as prompts and making mistakes hard. 🎯 *Takeaway:* the [tool table](./agentic-flows-practice.md) is a design artifact, not an engineering detail.

**Capability is uneven (2023).** A Harvard Business School working paper on consultants using a language model described a "jagged technological frontier": tasks that look similar can fall on either side of what the model does well. This source was not re-opened for this track. 🎯 *Takeaway:* [probe on your own tasks](./model-intuition-practice.md), because a general score will not tell you where your edge lies.

## Module recap

| Skill | Judgement lesson | Practice lesson | The question it makes you ask |
| --- | --- | --- | --- |
| 1. Vision and opinionated UX | [Designing for ambiguity](./designing-for-ambiguity.md) | [The AI feature spec](./ux-practice-the-ai-feature-spec.md) | What does the user see first, and what happens when the model is wrong? |
| 2. Model intuition | [Model intuition](./model-intuition.md) | [Probing and choosing models](./model-intuition-practice.md) | Where does this model fail on our inputs, and what does the fix cost? |
| 3. Pixels to evals to hill climbing | [From pixels to evals](./from-pixels-to-evals.md) | [Hill climbing](./hill-climbing-in-practice.md) | Which user action tells us the output was right, and is the gain bigger than the noise? |
| 4. Agentic flows | [Designing agentic flows](./designing-agentic-flows.md) | [The agent spec and risk register](./agentic-flows-practice.md) | What is the worst thing it can do, and what stops it? |
| 5. User understanding for agents | [How users behave with agents](./how-users-behave-with-agents.md) | [Researching agent interactions](./researching-agent-interactions.md) | When the agent is wrong, do users notice? |

**The through-line.** An AI-native product is designed around uncertainty. You decide what the model should do. You measure it with evals and improve it step by step. You shape the flow so that people can trust it, check it and correct it. And you keep watching how real people behave, because their trust moves.

> **Walk-away question:** *"For our feature, can I show the spec, the model choice, the eval set with a holdout, the agent's limits and risks, the research findings and the launch gate, and name the weakest of the five?"*

## Test yourself

1. **A new AI feature opens with a blank chat box. What is the likely problem, and what do you do first?**
   <details><summary>Answer</summary>Users do not know what to ask or what the system can do. Make it opinionated: set the scope, offer a starting point such as a ready draft, and design how uncertainty and correction appear. (<a href="./designing-for-ambiguity.md">Lesson 1</a>)</details>
2. **Name the parts of a one-page AI feature spec that a classic spec leaves out.**
   <details><summary>Answer</summary>Examples of accepted and rejected outputs, what happens when the model is unsure or wrong, a quality bar with a definition of pass, and a launch gate. (<a href="./ux-practice-the-ai-feature-spec.md">Lesson 2</a>)</details>
3. **What is the jagged frontier, and how do you find it for your product?**
   <details><summary>Answer</summary>Capability is uneven: a model can do a hard task and fail at an easy-looking one. You find the edge by probing on real inputs and reading the failures. (<a href="./model-intuition.md">Lesson 3</a>)</details>
4. **A model fails because it lacks a policy fact. What is the first lever to try?**
   <details><summary>Answer</summary>Retrieval and context, not tuning and not a bigger model. Name the failure cause before you choose the fix. (<a href="./model-intuition.md">Lesson 3</a>)</details>
5. **In a bake-off, what do you set before you look at any result?**
   <details><summary>Answer</summary>The constraints: the quality bar, the latency the user will tolerate, the cost per use, and the must-not-fail cases. Then pick the cheapest model that meets all of them. (<a href="./model-intuition-practice.md">Lesson 4</a>)</details>
6. **61% of drafts are sent with no edit. Is that good?**
   <details><summary>Answer</summary>Not necessarily. It may mean the output is good or that users did not look. Sample and read the no-edit cases. In the example, 6 of 40 held a wrong detail. (<a href="./from-pixels-to-evals.md">Lesson 5</a>)</details>
7. **Why is a 2-point gain on a 200-case eval not a win?**
   <details><summary>Answer</summary>With 200 cases and an 80% pass rate, the rough 95% band is about plus or minus 5.5 points, so 2 points is inside the noise. Add cases or compare pairs. (<a href="./from-pixels-to-evals.md">Lesson 5</a>)</details>
8. **Why use offline evals and A/B tests together?**
   <details><summary>Answer</summary>Offline evals are fast and controlled, so they pick what to try. A/B tests measure real value, so they confirm what ships. (<a href="./from-pixels-to-evals.md">Lesson 5</a>)</details>
9. **The dev score rose from 80% to 88%, and the holdout barely moved. What happened?**
   <details><summary>Answer</summary>The prompt was overfitted to the dev set, in the example by copying dev-like cases into it. Trust the holdout, refresh the dev set from production and keep the log. (<a href="./hill-climbing-in-practice.md">Lesson 6</a>)</details>
10. **Workflow or agent: how do you choose?**
    <details><summary>Answer</summary>Use a workflow when you can write the steps in advance. Use an agent when the number of steps is unknown and the path cannot be fixed. Add complexity only when it demonstrably helps. (<a href="./designing-agentic-flows.md">Lesson 7</a>)</details>
11. **What are the four levels of autonomy, and how does a product move up?**
    <details><summary>Answer</summary>Suggest, act with approval, act and notify, act silently. Move up only on evidence, such as approval and edit rates and zero severe errors over a stated volume. (<a href="./designing-agentic-flows.md">Lesson 7</a>)</details>
12. **What makes an approval prompt protect users?**
    <details><summary>Answer</summary>A plain preview of who, what and how much, with the reason and source, a safe default and no prompts on low-risk actions. Track approval and edit rates. (<a href="./agentic-flows-practice.md">Lesson 8</a>)</details>
13. **Define over-reliance and under-reliance, and say what the goal is.**
    <details><summary>Answer</summary>Over-reliance is accepting output without checking. Under-reliance is ignoring or redoing good output. The goal is calibrated trust: reliance that matches reliability on each task. (<a href="./how-users-behave-with-agents.md">Lesson 9</a>)</details>
14. **Why ask "tell me about the last time the agent was wrong" instead of "do you trust it"?**
    <details><summary>Answer</summary>Specific past episodes show real behaviour. Opinions about trust do not predict what people do. (<a href="./researching-agent-interactions.md">Lesson 10</a>)</details>
15. **What are the three parts of a launch gate?**
    <details><summary>Answer</summary>Ship, widen and roll back, each with numbers: quality on the holdout, severe incidents, rates such as light-edit, cost and latency, and a named kill-switch owner. (<a href="./capstone-ship-one-ai-native-feature.md">Capstone</a>)</details>

## Sources

- Saleema Amershi et al., *Guidelines for Human-AI Interaction*, CHI 2019, and Microsoft's HAX Toolkit design library (microsoft.com/en-us/haxtoolkit/library), read 2026-10.
- Anthropic, "Building effective agents", anthropic.com/engineering/building-effective-agents, 2024-12-19, read 2026-10. The page notes that much of its tooling description has changed since December 2024.
- Fabrizio Dell'Acqua et al., *Navigating the Jagged Technological Frontier*, Harvard Business School working paper, 2023. Not re-opened.
- Relay and all numbers in the questions come from invented teaching examples. This track's fact-check is pending.
