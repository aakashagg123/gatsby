# Voice guide: the human teaching voice

This guide is for lessons that have been rewritten to sound like a good teacher talking to one reader.
It replaces `WRITING-STYLE.md` for those lessons only. Every other lesson keeps the old rules until its turn.
The measurable readability targets in `CONTENT_FRAMEWORK.md` (section 4) still apply. A human voice is not a harder read.

## The idea

Picture one smart PM, tired at the end of a day, who has asked you: "How do I actually do this?"
You would not hand them a template with a TL;DR and a boxed callout. You would say what the thing is,
tell them where it goes wrong, give them a situation to picture, and tell them what you would do on Monday.
Write that. The lesson should sound like someone who knows the subject, respects the reader and has a view.

## Who is speaking

- **A teacher, not a character.** Use "you", and "we" for something you walk through together.
- **No invented persona and no invented stories.** Do not write "when I was a PM at...", "in my experience",
  "a client once told me" or any other made-up past. Nobody here has that past, and readers can smell it.
- **Real people come from the show.** A real story or a real view from a guest is welcome, credited, and marked as theirs.
  See "Using The Growth Podcast" below.
- **An invented example is fine when it is labelled.** "Say you run onboarding for a travel app." That is a thought experiment, not a memory.

## Rhythm: sound like thinking, not like a script

Short sentences are easy to read, but a page made only of short sentences sounds like a presenter reading cue cards.
People think out loud, qualify themselves, and let a sentence run a little long when two ideas belong together.

- **Mix the lengths.** Most sentences run 12 to 22 words. Some are short. A few reach 28 when a cause and its effect belong in one breath.
  Join ideas the way people do, with "because", "which", "so", "though", "while", "and then".
- **Give paragraphs some body.** Three to five sentences is normal. A one-sentence paragraph is for the one line you want the reader to stop on, and it should be rare.
- **Don't answer your own question.** A question the writer asks and answers in the next breath ("So who's right? Both.") is a stage trick. Ask when the reader should stop and think, then let the reasoning unfold across a paragraph. Keep to one real question per section.
- **Don't run on signposts.** "Here's the thing", "Now decide", "Look at this again", "Let's be honest" are fine once in a while, never as the engine of a section.
- **No cadence by list.** Three parallel clauses used for rhythm, a punchy one-liner to close every section, and a pair of short sentences set against each other all give the page a pulse that sounds written. Let some sections just end when the point is made.
- **Qualify like a thinker.** "Teams tend to...", "it usually turns out...", "that depends on how much a wrong call costs you". Qualifying is not hedging when it says what the answer depends on. (Do not borrow experience you don't have: "in my experience" and "I've seen" are still out.)
- **Keep a concrete image in each section**, a situation or an artifact, so the sentences have something to hold on to.

## What to do

- **Open with a situation or a question**, not a definition. "You open the dashboard on Monday and sign-ups are down 8%. What do you do first?"
- **Speak plainly.** Contractions, short words, the occasional sentence that is five words long. Vary the rhythm. A page of 18-word sentences reads like a machine.
- **Ask the reader to decide.** "What would you cut?" Then answer it, and say why.
- **Say what you think.** Take a position when the evidence supports one. Say when reasonable people disagree, and who.
- **Admit what you don't know.** "Nobody has good data on this yet." That is more trustworthy than a confident sentence.
- **Name the cost of every advice.** Every choice gives something up. Say what.
- **Use an analogy only when it carries weight.** One good one beats three decorative ones.
- **Keep the useful parts of the old template as natural sections:** where it breaks, a short checklist, related lessons, a diagram when a picture helps. Give them human headings.
- **End on something to do**, not a summary of what was just said.

## What not to do

- **Don't invent anything about a person.** Not a quote, not an anecdote, not a job title, not a number a guest "said".
- **Don't imitate a guest or the host.** No pastiche of anyone's speech. A guest's words appear only as a short, credited quote.
- **Don't use the LLM tells.** If a sentence sounds like a slide, rewrite it:
  - openers such as "Let's dive in", "In today's fast-moving world", "It's important to note that"
  - the "It's not X, it's Y" and "Not just X, but Y" patterns
  - lists of exactly three adjectives, or three parallel clauses used as rhythm
  - long chains of em-dashes, and colons that set up a reveal
  - closing lines that restate the lesson ("In summary, ...", "Ultimately, ...")
  - "game-changer", "unlock", "leverage", "navigate", "landscape", "robust", "seamless"
  - bold on random phrases. Bold is for a term you define, or one warning.
- **Don't pad.** If a paragraph can lose a sentence without losing meaning, lose it.
- **Don't change a fact while changing the voice.** Numbers, dates, named products, versions and cited sources stay exactly as they are unless a fact-check says otherwise.

## Lesson shape

A human-voice lesson needs these things. The order and the headings are yours.

1. Title and the `*Part of ...*` line. Keep the review stamp line as it is.
2. **An opening situation or question** that makes the reader care.
3. **The teaching**: the idea, how it works, one worked example (labelled invented when invented), the tradeoffs.
4. **At least one "From the show" moment** when the topic has real practitioners behind it: a short credited quote, a real story, or a real disagreement.
5. **Where it goes wrong**: the failure modes, in plain words.
6. **What to do next**: a short checklist or a few concrete steps.
7. **Related lessons**: cross-links, not only within the track.
8. **Sources**: needed whenever the lesson makes versioned, numeric, vendor or attributed claims. Include the show credit below whenever a quote or story is used.

## Using The Growth Podcast

The transcripts come from The Growth Podcast with Aakash Gupta (https://www.news.aakashg.com), released under a licence that allows quotes
and building on them. The rules below follow that licence.

- **Credit every use.** Name the show and link the episode. Put this line in the lesson's Sources when it uses the show:
  "Quotes from The Growth Podcast with Aakash Gupta ([news.aakashg.com](https://www.news.aakashg.com)), used under its licence. The transcript text is machine-made and the quotes have not been checked against the audio."
- **Short quotes only.** One or two sentences, usually under 40 words. A lesson uses a handful at most, normally two to four. A quote earns its place: it adds a view, a human detail or a disagreement. Never use one as filler.
- **Quote exactly.** Copy the words as they appear in the transcript, with `[...]` for cuts and `[word]` for a clarification. Do not tidy a guest's grammar into a different sentence. `scripts/check_quotes.py` checks that a quote appears in the named episode.
- **Attribute every view.** "Teresa Torres argues..." "Marty Cagan's point is...". Write guest claims as what the guest says, never as established fact. If a number matters, check it against a primary source first, because the transcript may have misheard it.
- **Say where, roughly.** Format: `— Guest Name, *Episode title*, The Growth Podcast, around 12:30`, with the YouTube link on the episode title. Timestamps in the transcripts can drift from the video by a few minutes, so write "around", not "at".
- **Never imply endorsement.** A guest said a thing on a podcast. They did not endorse this course. Do not write "as X recommends in this course" or use a guest's name to sell anything.
- **Never copy transcript text beyond the quote.** The files themselves stay in their own repository. Link to it. Do not paste or re-host passages.
- **Skip sponsor reads** (the transcripts mark them with `<!-- sponsor -->`) and any host monologue about a product.

A quote in a lesson looks like this:

```markdown
> "If someone's telling you we tried it, it didn't work, don't stop there."
> — Stephanie Leue, [*How to Build High Performing Product Teams*](https://www.youtube.com/watch?v=VIDEO_ID), The Growth Podcast, around 00:58
```

(That example is only to show the layout. Real quotes come from `find_quotes.py` and are checked by `check_quotes.py`.)

## Before you hand a lesson in

- Read it aloud. Anywhere you would not say it to a colleague, change it.
- Count the quotes, check the credit line, check that nothing is presented as a guest's endorsement.
- Run `python3 scripts/check_module.py <track>` and `python3 scripts/check_quotes.py <track>`.
- List every fact you added or changed. Each one goes to the fact-checker.
