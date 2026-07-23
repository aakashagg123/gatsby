# Glossary framework — which words get an explanation, and how

This is the rule for deciding **which terms across the curriculum get a glossary entry**,
what tier they sit in, and how each entry is written. It exists so term selection is a
*repeatable standard* — not one author's judgment — and so every module is treated the
same way.

The glossary powers two things: the enriched [`GLOSSARY.md`](./GLOSSARY.md), and the
**clickable terms + explainer sidebar** on the [live site](https://aakashagg123.github.io/gatsby/).
All of it is generated from one source of truth: [`scripts/glossary_data.py`](./scripts/glossary_data.py).

---

## 1. The reader bar — who we explain *for*

**The reader is a product head / CPO:** business- and product-fluent, but not deeply
technical. This single assumption sets the bar for "needs explaining."

| Explain it | Assume they know it |
| --- | --- |
| Technical / engineering jargon — KV cache, idempotency, eventual consistency, backpressure | Product & strategy vocabulary — roadmap, MVP, churn, stakeholder, backlog |
| AI/ML jargon — RAG, quantization, embeddings, hallucination | Basic business terms — revenue, margin, segment |
| Specialist-domain jargon — BPMN, saga/compensation, entity resolution, ontology | Plain English |
| Named methods & eponyms — Fogg behaviour model, ReAct, PageRank, Jobs-to-be-Done | |

> **The test:** *"Would a smart CPO with no engineering background stumble on this word?"*
> If yes, it's a candidate. If it's vocabulary they use in their own planning docs, it's not.

Borderline product-strategy terms (e.g. *north star*, *PRD*, *jobs-to-be-done*) sit right
at the bar. We keep them only where a lesson gives them a **specific, non-obvious framing**
a CPO wouldn't already have; otherwise they're assumed known.

## 2. What qualifies — the four inclusion categories

A word is in scope if it falls into any of these:

1. **Acronyms & technical jargon** — `RAG`, `KV cache`, `BPMN`, `p99`, `MCP`, `FP8`.
2. **Terms a lesson coins or redefines** — words given a specific meaning here: *ontology*
   as a product contract, *harness*, *lethal trifecta*, *jagged frontier*.
3. **Borrowed cross-domain concepts** — ideas imported from another field and used as-is:
   *inversion*, *second-order effects*, *saga*, *backpressure*, *circle of competence*.
4. **Named frameworks, laws & people** — *Fogg behaviour model*, *Jobs-to-be-Done*,
   *ReAct*, *PageRank*.

### Exclusions
- Product/strategy vocabulary the reader already owns (see the bar).
- Plain English and general business terms.
- Words that appear once, in passing, and don't carry weight in any lesson's argument.

## 3. Two tiers — must-know vs. nice-to-know

Density is **tiered**, not uniform, and **calibrated per module** (technical modules run
denser than thinking/craft modules because they simply contain more true jargon). We set
**no per-module quotas** — the right count falls out of the rule below.

- **Must-know** = **argument-critical**: you cannot follow the lesson's core point without
  it. In practice these are the terms in the lesson's **TL;DR** and its **🎯 briefing** —
  i.e. *the terms the lesson develops*. Operationally, a term is must-know for the lesson
  it calls **home** (its `see` link).
- **Nice-to-know** = other in-scope jargon that appears but isn't load-bearing for *this*
  lesson's thesis.

Because term identity is global (§5) but "argument-critical" is per lesson, the tier is
recorded **per lesson × term**: a term is must-know in its home lesson and nice-to-know
where it's merely mentioned.

**Reader-facing use:** each lesson shows a **"Key terms" box** listing its must-know terms
(clickable, opens the sidebar) — a study aid derived automatically from the home mapping.
In prose, every linked term looks the same regardless of tier (no visual noise).

## 4. How candidates are found — hybrid, then curated

1. **Auto-scan** the lesson markdown for signals already present in the text:
   - **bolded** terms (`**like this**`),
   - acronyms / CamelCase (`RAG`, `GraphRAG`, `A2A`),
   - "**term** — definition" em-dash patterns (the house style for introducing a concept).
2. **Human curate**: keep only what clears the reader bar (§1) and fits a category (§2);
   cut basics; add any coined phrase the scan missed.

The scan produces the candidate list; judgment produces the glossary. Neither alone.

## 5. Term identity — one global definition

Each term has **one canonical entry**, linked wherever it appears, always pointing to its
**home lesson** (where it's developed). We do *not* fork a term into module-specific
variants — consistency and low maintenance win over per-module nuance.

## 6. The entry template — every entry ships all five

Written for the CPO lens: plain first, jargon never used to explain jargon.

| Part | What it is |
| --- | --- |
| **In plain terms** | A first-principles explanation in plain English (2–4 sentences). |
| **For example** | One concrete, specific illustration. |
| **Where it shows up** | 2–3 use-cases — the product decisions the term touches. |
| **Related** | Neighbouring terms (clickable), so the glossary reads like a small graph. |
| **See** | The lesson where it's developed in depth. |

Plus metadata used by the linker: `aliases` (extra surface forms), `cs` (match
case-sensitively — for acronyms/CamelCase like `RAG`, `ReAct`), and `autolink:false`
(keep in the glossary but don't auto-link in prose — for words too common in ordinary
English to link safely, e.g. *tool*, *trace*, *span*).

## 7. Authoring checklist (new module or lesson)

- [ ] Run the candidate scan over the new markdown (bold / acronym / em-dash signals).
- [ ] Curate against the reader bar (§1) and the four categories (§2); cut basics.
- [ ] For each kept term: add an entry to `scripts/glossary_data.py` with all five parts
      (§6), the correct `see` home lesson, and `related` slugs.
- [ ] Set `cs:true` for acronyms/CamelCase; `autolink:false` for common-English collisions.
- [ ] The lesson's must-know terms are simply the terms that now home to it — they'll
      appear in its "Key terms" box automatically.
- [ ] Run `python3 scripts/build_glossary.py` (validates entries + links, regenerates
      `GLOSSARY.md`) and `python3 scripts/check_links.py`.

## 8. Where it all lives

| File | Role |
| --- | --- |
| [`scripts/glossary_data.py`](./scripts/glossary_data.py) | Single source of truth — every term and its five parts. |
| [`scripts/build_glossary.py`](./scripts/build_glossary.py) | Validates, maps home lessons to URLs, regenerates `GLOSSARY.md`, exposes widget data + the must-know (Key-terms) map. |
| [`scripts/glossary_widget.py`](./scripts/glossary_widget.py) | The clickable-term linker, the sidebar, and the per-lesson Key-terms box. |
| [`GLOSSARY.md`](./GLOSSARY.md) | The generated, human-readable glossary. |
| This file | The rule for what goes in, and why. |
