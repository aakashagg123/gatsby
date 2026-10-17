# AI-assisted development — recap & real-world examples

*Part of [AI-assisted development for the product and technology leader](./README.md)*

## Real-world examples

**A controlled trial: faster on a defined task (2023).** Peng and colleagues gave developers a task, with and without an AI pair programmer, and measured completion time. The group with the assistant finished faster. 🎯 *Takeaway:* on a [well-defined task](./when-an-agent-writes-the-code.md) with a clear check, the gain is real. Do not assume it carries to all work.

**An RCT with the opposite result (2025).** METR ran a randomized trial with experienced open-source developers working on their own repositories. They were slower with the AI tools, though they had expected to be faster. 🎯 *Takeaway:* [perception is not measurement](./measuring-and-governing.md). Context, codebase familiarity and review cost change the answer.

**Anthropic's own guidance: give the agent a way to check.** The Claude Code best-practice pages say the single most useful thing is to give the agent a way to verify its work, such as tests or a script. 🎯 *Takeaway:* [verification is the product](./verification-is-the-product.md). Name the check in every spec.

**Documented limits of command rules.** The Claude Code permissions page states that a Bash rule matches the command as written and lists forms it does not catch. 🎯 *Takeaway:* [rules are guardrails, not walls](./control-permissions-modes-and-hooks.md). Use a sandbox for unattended work.

**A published cost anchor.** The Claude Code cost page reports about $13 per developer per active day on average across enterprise deployments, and under $30 for 90% of users. 🎯 *Takeaway:* [cost is per task and per session](./running-at-scale.md), and a pilot gives your own number.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [The bottleneck moves](./when-an-agent-writes-the-code.md) | Generation gets cheap, so specifying and verifying dominate | Which step grew, and what do our checks look like? |
| [Specs and the context file](./specs-and-the-context-file.md) | A short standing brief and a spec with a check | Who owns the file, and does each spec name a check? |
| [Verification](./verification-is-the-product.md) | "Done" must be an exit code, not a sentence | What command proves it, and must the agent run it? |
| [Control](./control-permissions-modes-and-hooks.md) | Modes, rules and hooks guard honest mistakes; a sandbox guards the rest | What can the agent reach, and what if it is misled? |
| [Running at scale](./running-at-scale.md) | Cost and review capacity, not agents, set throughput | What does a batch cost, and who reviews it? |
| [Measuring and governing](./measuring-and-governing.md) | Outcome metrics, split by kind of work, and a one-page policy | Is the gain real on hard work, and who owns the policy? |

**The through-line.** A coding agent moves the work from writing to deciding and checking. Leaders who get value write precise specs, make "done" a fact, limit what the agent can touch, plan for the review queue, and measure outcomes without being fooled by averages.

> **Walk-away question:** *"For our agent rollout: can I name the check that proves a change works, what the agent cannot touch, the cost of a batch and its review hours, and the outcome metric split by difficulty?"*

## Test yourself

1. **An agent cuts run time to zero. Why does a task not get ten times faster?**
   <details><summary>Answer</summary>Specifying and reviewing remain, and rejected attempts repeat them. In the model, an instant agent with weak checks reached only 2.19 times the speed of working by hand. (<a href="./when-an-agent-writes-the-code.md">Lesson 1</a>)</details>
2. **Which helps more in the model: a faster agent or stronger checks?**
   <details><summary>Answer</summary>Stronger checks. Strong checks took the task from 146 to 84 minutes. An instant agent with weak checks only reached 132. (<a href="./when-an-agent-writes-the-code.md">Lesson 1</a>)</details>
3. **What four parts does a good task spec have?**
   <details><summary>Answer</summary>The goal, the scope, the constraint that matters, and a way to check the result. (<a href="./specs-and-the-context-file.md">Lesson 2</a>)</details>
4. **Why does splitting a long context file into imports not cut its cost?**
   <details><summary>Answer</summary>Imported files load at launch with the main file. To cut cost, move content into path-scoped rules or skills, which load only when relevant. (<a href="./specs-and-the-context-file.md">Lesson 2</a>)</details>
5. **What should and should not go in a context file?**
   <details><summary>Answer</summary>Include commands and rules the agent cannot infer from the code. Leave out descriptions of the code, vague advice, duplicates and long explanations. (<a href="./specs-and-the-context-file.md">Lesson 2</a>)</details>
6. **Why is an agent's "all tests pass" not evidence?**
   <details><summary>Answer</summary>It is a sentence, and the agent may not have run the tests or may have weakened them. A command that exits with pass or fail is evidence. (<a href="./verification-is-the-product.md">Lesson 3</a>)</details>
7. **How does a Stop hook enforce a check, and what prevents an endless loop?**
   <details><summary>Answer</summary>It runs the check when the agent tries to stop and exits 2 with a message if it fails, which keeps the agent working. A guard on `stop_hook_active` and a cap on consecutive blocks end the loop. (<a href="./verification-is-the-product.md">Lesson 3</a>)</details>
8. **In what order are permission rules evaluated?**
   <details><summary>Answer</summary>Deny, then ask, then allow. The first match wins, so a broad deny beats a narrow allow. (<a href="./control-permissions-modes-and-hooks.md">Lesson 4</a>)</details>
9. **A rule denies `curl`. Does that stop `/usr/bin/curl` or `sh -c 'curl …'`?**
   <details><summary>Answer</summary>No. A Bash rule matches the command as written. Use a sandbox when you need a real boundary. (<a href="./control-permissions-modes-and-hooks.md">Lesson 4</a>)</details>
10. **When is bypass mode acceptable?**
    <details><summary>Answer</summary>Only in an isolated environment, such as a container with no secrets and a limited network. (<a href="./control-permissions-modes-and-hooks.md">Lesson 4</a>)</details>
11. **Five unrelated tasks run in one long session cost $14.88 of input. In five fresh sessions they cost $5.28. Why?**
    <details><summary>Answer</summary>Every turn re-reads the whole history. A long session carries earlier tasks along. Clear the context between unrelated tasks. (<a href="./running-at-scale.md">Lesson 5</a>)</details>
12. **Three attempts instead of one raised cost from $300 to $417 for 200 tasks. What else changed?**
    <details><summary>Answer</summary>Accepted tasks rose from 140 to 195 and hand-offs fell from 60 to 5. Review hours also rose from 14 to 19, so the review team is the limit. (<a href="./running-at-scale.md">Lesson 5</a>)</details>
13. **A dashboard shows cycle time down from 23 to 7.1 hours. What do you check before celebrating?**
    <details><summary>Answer</summary>The mix of work. Split by difficulty. Here, easy work went from 50% to 86% of pull requests, hard work improved only 20%, and its rework doubled. (<a href="./measuring-and-governing.md">Lesson 6</a>)</details>
14. **Name five outcome metrics and two activity metrics to avoid.**
    <details><summary>Answer</summary>Lead time, change failure rate, rework, review time and cost per accepted change. Avoid lines of code and pull-request counts. (<a href="./measuring-and-governing.md">Lesson 6</a>)</details>

## Sources

- Peng et al., *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot*, 2023 ([arxiv.org/abs/2302.06590](https://arxiv.org/abs/2302.06590)).
- METR, *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity*, 2025 ([arxiv.org/abs/2507.09089](https://arxiv.org/abs/2507.09089)).
- Claude Code documentation (code.claude.com/docs), read 2026-10: best practices, memory, hooks, permissions, permission modes, costs and headless mode.
- The numbers in the questions come from `ai-assisted-development/code/`. They are invented. The trial results are quoted from memory and were not re-opened. This module's fact-check is pending.
