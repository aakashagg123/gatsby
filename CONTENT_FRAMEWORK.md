# Content framework — how any module is written, reviewed, and improved

This is the standard for improving a module. It exists so that every module is treated the
same way, and so that "this module is fine" is a measured result, not an opinion.

It sits on top of three existing documents. It does not replace them.

| Document | What it governs |
| --- | --- |
| [`CLAUDE.md`](./CLAUDE.md) | The house skeleton of a lesson, the build, and the deploy |
| [`WRITING-STYLE.md`](./WRITING-STYLE.md) | Sentence-level style (Simplified English in spirit) |
| [`GLOSSARY_FRAMEWORK.md`](./GLOSSARY_FRAMEWORK.md) | Which terms get a glossary entry |
| **This document** | Measurable targets, accuracy, freshness, depth, and the improvement process |

The checker for the measurable rules is [`scripts/check_module.py`](./scripts/check_module.py).

---

## 1. The reader: two layers

Every lesson serves two readers. The **body** is written for a product leader who is not
deeply technical. A short **Under the hood** section is written for an engineer.

- **Body.** Plain language. The reader bar in `GLOSSARY_FRAMEWORK.md` applies: explain
  engineering and AI jargon, assume product vocabulary. A reader can follow the whole
  body without reading code.
- **Under the hood.** One section per lesson. It shows the mechanism: a config, a schema,
  a short code sample, a protocol detail, or a formula. Technical terms are allowed here.
  Each term still links to the glossary or to the spoke lesson on first use.
- The body never depends on the Under the hood section. An engineer who skips the body
  loses the decision context. A PM who skips the section loses nothing needed to decide.

## 2. Lesson anatomy

Keep the house skeleton from `CLAUDE.md`. Add the four marked items.

1. Title, then the `*Part of ...*` line.
2. **Review stamp** *(new)*: `*Last reviewed: 2026-09 · Volatility: fast*`
3. **TL;DR**: the topic, the core tradeoff, the scale.
4. **🎯 briefing**: why it matters, what it changes, a question to ask, the risk.
5. **Mental model**: one diagram or analogy.
6. **Mechanics**: how it works.
7. **Worked example** *(new)*: one concrete case, followed step by step, with numbers or
   a real artifact. Label it a *worked example*. If it is invented, say so.
8. **Tradeoffs and decisions**: named tradeoffs with costs.
9. **Failure modes**: how it breaks in production.
10. **Under the hood** *(new)*: see section 1.
11. **Practitioner checklist**.
12. **Related lessons**: cross-links to other tracks, not only within the track.
13. **Sources** *(new, when needed)*: required when the lesson makes versioned, numeric,
    vendor, or attributed claims (section 5). Each entry has a link and an "as of" date.

## 3. Module anatomy

- **README.** Scope note, knowledge-graph diagram, lesson list, and a **Where the depth
  lives** map: for each idea the module only summarises, name the lesson that covers it in
  full.
- **Recap.** Real-world examples, a table (one idea and one question per lesson), a
  through-line, a walk-away question, and **Test yourself**.
- **Test yourself.** At least one question per lesson. Each has a short answer in a
  collapsed `<details>` block and a link back to the lesson.
- **War stories.** Each one is either real and sourced, or labelled "(an illustration)".
  Do not present an invented incident as fact.

## 4. Comprehension rules

Comprehension is measured on the prose of a module, not judged by feel. The checker
computes these on module averages, so one dense paragraph does not fail a module.

| Metric | Pass | Warn | Fail |
| --- | --- | --- | --- |
| Average sentence length (words) | <= 20 | 21-24 | >= 25 |
| Sentences over 30 words | <= 12% | 13-19% | >= 20% |
| Flesch reading ease | >= 50 | 45-49 | < 45 |

**Calibration.** These limits came from measuring all 20 flat tracks in September 2026.
The strongest tracks average 13-16 words per sentence, with 2-10% long sentences and a
Flesch score of 48-67. The weakest average 24-28 words, with 25-40% long sentences and a
Flesch score of 34-48. A score below 45 means most readers will reread sentences.

Other comprehension rules:

- **One idea per sentence.** Split a sentence at the second clause.
- **Define once.** Define a technical term the first time it appears, or link it to the
  glossary. Expand an acronym on first use. The checker lists acronyms that are neither
  defined in the lesson nor in the glossary.
- **One worked example per lesson** (section 2).
- **A self-test in every recap** (section 3).

## 5. Accuracy rules

Most errors found in this curriculum were claims that were true once, or never true.
These rules target them.

**Claims that need a source.** Each of these needs a link to a primary source and an
"as of" date, in the lesson's Sources list or inline:

- model or product versions and their behaviour ("Claude 4.6 does not support prefill")
- vendor features, prices, limits, and file or setting names
- statistics and benchmark results
- attributions of a technique or idea to a paper or person
- dated events (laws, incidents, releases)

**Primary source** means the vendor's own documentation or engineering post, the paper, the
specification, the law, or the court record. A blog summary is not a primary source.

**Not allowed:** an unsourced number ("prevents 30% of sprawl"), an invented incident
presented as real, or a claim about a named model that was not checked against the
vendor's current documentation.

**General principles need no citation.** "A model has no memory between calls" is a
principle. Cite it only if you attach a number or a version to it.

**When in doubt, soften or remove.** A vague true sentence is better than a precise
false one.

### Independent fact-check

The author cannot fact-check their own edits reliably. Before a module ships, a separate
agent checks it with no knowledge of the edits.

1. Give the agent only: the final lesson files, section 5 of this document, and web
   access. Do not give it a summary of what changed or why.
2. Ask for a table: **claim, location, primary source found, verdict** (`OK`, `WRONG`,
   `UNSUPPORTED`, `STALE`), and the correct statement for any non-OK row.
3. Every `WRONG` and `STALE` row blocks the PR until fixed. Each `UNSUPPORTED` row is
   fixed by adding a source or removing the claim.
4. Re-run the agent on the fixed files. Record the final result in the PR.

## 6. Freshness

Each lesson carries a review stamp (section 2). The stamp says when a person last checked
the lesson against current sources, and how fast its topic moves.

| Volatility | Review every | Tracks |
| --- | --- | --- |
| **fast** | 3 months | `llms`, `generative-ai`, `ai-agents`, `agentic-ai`, `agentic-workflows`, `tool-calling`, `api-integrations`, `prompt-engineering`, `context-engineering`, `memory-and-context`, `evaluation-and-observability`, `ai-security-and-guardrails`, `cost-optimization` |
| **medium** | 6 months | `rag-vector-databases`, `knowledge-graphs`, `technical-product-management`, `product-sense` |
| **stable** | 12 months | `system-design`, `technical-product-sense`, `first-principles` |

The checker reports a lesson as overdue when its stamp is older than its cadence. Updating
a stamp without re-checking the lesson is not allowed: the stamp is a claim that the
process in section 8 was followed.

## 7. Depth floor and the overlap gate

Some modules are short on purpose. They are compact front doors that point to deeper
lessons. That is allowed. A short module must still meet this floor:

- a worked example in each lesson
- an Under the hood section in each lesson
- a Test yourself section in the recap
- a **Where the depth lives** map in the README
- sources and a review stamp

**The overlap gate.** Before adding a lesson to any module, do this:

1. List what the sibling and spoke lessons already cover on the topic.
2. Name the **delta**: a decision framework, worked example, table, or runbook that does
   not exist elsewhere.
3. If the delta is thin, do not add the lesson. Fold the delta into an existing lesson and
   link to the spoke for the rest.

The delta test is what stops the same idea being restated in three modules.

## 8. The improvement workflow

Follow these steps in order for any module.

1. **Baseline.** Run `python3 scripts/check_module.py <track>`. Save the numbers.
2. **Read every lesson.** Read the whole text. Do not rely on the README summaries.
3. **Research.** Check the topic against primary sources. Record each source and date.
4. **Gap table.** For each change, one row: *Improve / Add / Remove*, the lesson, the
   change, the evidence, and the source.
5. **Approval.** Show the table to the owner and wait for approval before editing.
6. **Edit.** Apply the table. Keep the house skeleton and the diagrams.
7. **Check.** Rebuild the track and the site. Run `scripts/check_links.py` and
   `scripts/check_module.py`. Register any new lesson (see `CLAUDE.md`: build script,
   `SUMMARY.md`, README tables, landing card, glossary, diagram overrides).
8. **Independent fact-check** (section 5). Fix every blocking row.
9. **Re-check.** Re-run steps 7 and 8 on the fixed files.
10. **Ship.** One consolidated pull request. Put the before and after metrics and the
    fact-check result in the description. Update the tracker in
    [`SITE_QUALITY_ROADMAP.md`](./SITE_QUALITY_ROADMAP.md).

## 9. Definition of done

A module is done when all of these hold:

- [ ] Readability: all three metrics pass, or a warning is explained in the PR.
- [ ] Every lesson has a review stamp, a worked example, and an Under the hood section.
- [ ] Every claim in section 5's list has a primary source and an "as of" date.
- [ ] The independent fact-check has no `WRONG` or `STALE` rows.
- [ ] The recap has Test yourself with at least one question per lesson.
- [ ] The README has a Where the depth lives map.
- [ ] Any added lesson passed the overlap gate.
- [ ] `check_links.py` passes and the track builds.
- [ ] The tracker in `SITE_QUALITY_ROADMAP.md` is updated with the new metrics.

## 10. Why this exists: lessons from the first audit

The first site-quality program audited every track with a voice grep (hedging and filler
words) and a spoke-link check. Nearly every track passed with "no material gaps". A
review in September 2026 then found:

- a technique taught as best practice that current models no longer support
- a technique credited to the wrong paper
- unsourced statistics and invented incidents presented as real
- tracks that were hard to read (Flesch score as low as 34) and had no self-test
- no dates, so nobody could tell which lessons were stale

The lesson: a grep for style cannot find a wrong fact or an unreadable paragraph. This
framework adds the missing checks, and it adds a second pair of eyes that did not write
the edits.

## 11. Scope and limits

- `scripts/check_module.py` covers the flat tracks. `harness-engineering` and `flowable`
  use a different lesson format (phases, code, outputs) and need their own profile.
- The checker's claim and acronym checks are heuristics. They raise warnings for a person
  to judge. They never prove a claim is right.
- Modules that have no review stamp yet are reported with warnings, not failures, for the
  new requirements. Adding a stamp opts a module in to the full standard.
