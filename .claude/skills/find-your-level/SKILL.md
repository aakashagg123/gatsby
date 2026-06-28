---
name: find-your-level
version: 1.0.0
description: >
  Interactive placement quiz that maps your agent/harness knowledge to a starting
  point in the Harness Engineering from Scratch curriculum (20 phases).
  Trigger phrases: "where should I start", "find my level", "which phase",
  "assess my knowledge", "placement test", "skip ahead".
tags: [assessment, onboarding, curriculum, harness-engineering]
---

# Find Your Level

You administer a placement quiz for **Harness Engineering from Scratch** (20 phases,
~120 lessons; see `harness-engineering/ROADMAP.md`). Your job: find where the learner should begin so they
skip what they know and land where the challenge starts.

## Quiz Structure

5 knowledge areas, 2 questions each, 10 total. Present in rounds of 2 (one per area).
Score each area before moving on. Use **AskUserQuestion** for every question. Keep
commentary short; don't explain answers until the very end.

## Scoring → starting phase

- 0–2: start at **Phase 0/1** (Setup, LLM I/O).
- 3–4: start at **Phase 2** (The Agent Loop).
- 5–6: start at **Phase 4–6** (Context, Prompts, File Ops).
- 7–8: start at **Phase 8–12** (Permissions, Memory, Subagents, MCP).
- 9–10: start at **Phase 14+** (Reliability, Evals, Security, Production) and go
  straight for the Capstone.

After scoring, produce a personalized path: list the phases to do, in order, with the
~hours each (assume ~1–1.5h/lesson) and the first lesson to open.

---

### Round 1 — LLM I/O

**Q1.** What does a stateless model "remember" between two separate API calls?

- A) The full prior conversation automatically
- B) Nothing — the harness must resend history each call
- C) Only the system prompt
- D) The last tool result

**Correct: B**

**Q2.** Which is *not* something the harness controls (vs. the model)?

- A) Which tools actually execute
- B) The contents of the context window
- C) The next token's probability distribution
- D) Retries and fallbacks

**Correct: C**

---

### Round 2 — The Agent Loop & Tools

**Q3.** A model reply with `stop_reason == "tool_use"` means the loop should…

- A) return the text to the user and stop
- B) run the requested tools and call the model again with the results
- C) raise an error
- D) summarize the conversation

**Correct: B**

**Q4.** A side-effecting tool (e.g., "send email") should be made idempotent because…

- A) it's faster
- B) the loop may retry, and you don't want to send twice
- C) the model requires it
- D) it reduces tokens

**Correct: B**

---

### Round 3 — Context Engineering

**Q5.** When the conversation exceeds the context window, the safest first move is…

- A) drop the system prompt
- B) truncate the oldest messages without splitting a tool_use/tool_result pair
- C) lower the temperature
- D) switch models

**Correct: B**

**Q6.** "Context rot" refers to…

- A) expired API keys
- B) degraded answer quality as the window fills with stale/low-signal content
- C) cache eviction
- D) a streaming bug

**Correct: B**

---

### Round 4 — Permissions, Memory & Orchestration

**Q7.** Treating model output as *data, not control flow* primarily defends against…

- A) high latency
- B) prompt injection from tool results and files
- C) token overflow
- D) cache misses

**Correct: B**

**Q8.** A supervisor/worker (subagent) pattern is most useful when…

- A) the task is a single short prompt
- B) you need to parallelize independent subtasks and isolate their context
- C) you want lower temperature
- D) you need streaming

**Correct: B**

---

### Round 5 — Reliability, Evals & Production

**Q9.** A regression eval gate in CI exists to…

- A) speed up inference
- B) catch quality drops before a prompt/model change ships
- C) reduce token cost
- D) format JSON

**Correct: B**

**Q10.** The single most important guard against a runaway agent is…

- A) a bigger model
- B) hard ceilings on steps, tools, and tokens per request
- C) more examples in the prompt
- D) a longer system prompt

**Correct: B**

---

## Wrap-up

Report each area score (e.g. "Context Engineering: 2/2"), the total, the recommended
starting phase, and a 3–5 line personalized path with the first lesson link.
