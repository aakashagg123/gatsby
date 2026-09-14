# Writing style: Simplified English

All prose in this repository follows the **spirit of ASD-STE100** (the aerospace
Simplified Technical English standard), adapted for a technical/product
curriculum rather than a maintenance manual. The goal is prose that a
non-native English speaker or a tired reader at 11pm can parse on the first
pass — without losing the tradeoffs, analogies, and judgment calls that make
the teaching useful.

## The rules

- **Short sentences.** Aim for 20–25 words. Split a sentence the moment it
  needs a semicolon or a third clause.
- **One idea per sentence.** If a sentence explains what something is *and*
  why it matters *and* when it fails, that's three sentences.
- **Active voice, concrete subjects.** "The load balancer routes requests,"
  not "requests are routed by the load balancer." Name the actor.
- **Plain, consistent vocabulary.** Use one word for one meaning throughout a
  lesson — don't alternate between "leverage" and "use," or "commence" and
  "start." Prefer the shorter, more common word.
- **Define a technical term once, then reuse it.** Don't introduce a
  synonym for a term already defined in the lesson.
- **Cut hedging and filler.** Drop "essentially," "basically," "in order to,"
  "it should be noted that." Say the thing.
- **Compound sentences are allowed when a concept genuinely needs one** —
  a tradeoff with two sides, a cause and its effect — but keep them to two
  clauses, joined by "and," "but," or "so," not buried in subordinate clauses.
- **Keep the house structure and voice.** TL;DR, the 🎯 PM callout, mental
  model, mechanics, tradeoffs, failure modes, checklist. Simplify the
  sentences inside each section — don't remove the sections, the tables, the
  worked examples, or the diagrams.
- **Numbers, code, commands, and named APIs stay exactly as they are.**
  Simplified English applies to explanatory prose, not to literal syntax.

## What this is not

This is not literal ASD-STE100: no fixed ~900-word approved vocabulary, no
20-word hard ceiling enforced sentence-by-sentence, no ban on all
subordinate clauses. The standard was built for aircraft maintenance
procedures, where ambiguity kills people. This curriculum teaches judgment
and tradeoffs, which sometimes need a longer sentence to hold two ideas in
tension. When in doubt, favor clarity and brevity over strict compliance.
