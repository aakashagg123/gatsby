#!/usr/bin/env python3
"""Check that every quote from The Growth Podcast in a lesson is real (read-only).

    python3 scripts/check_quotes.py product-sense            # every lesson in a track
    python3 scripts/check_quotes.py path/to/lesson.md ...    # specific files

A quote block in a lesson looks like this (see VOICE-GUIDE.md):

    > "If someone's telling you we tried it, it didn't work, don't stop there."
    > — Stephanie Leue, [*Episode title*](https://www.youtube.com/watch?v=ID), The Growth Podcast, around 00:58

For each block the script checks that
  1. the episode exists in index.json (matched by title and by the YouTube video id),
  2. the quoted words appear in that episode's transcript, in order (a [...] in the quote is a cut),
  3. the speaker named in the credit said them (the transcript's speaker label contains the name),
  4. the "around mm:ss" time is within 3 minutes of where the transcript puts the words,
  5. the quote is short (warns above 40 words) and a lesson has at most 5 quotes (warns above).
It does NOT check the audio: the transcripts are machine-made. Names and numbers still need a human check.

The transcripts are a separate repository. Set GROWTH_PODCAST_DIR to its clone (default
/home/user/aakashg/growth-podcast-transcripts). If it is missing the script says so and exits 0,
so CI is not affected. Exit code 1 means at least one quote failed.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from find_quotes import transcripts_dir, load_index, turns  # noqa: E402

CREDIT_RE = re.compile(
    r"^>\s*[—–-]\s*(?P<guest>[^,\[]+?),\s*\[\*?(?P<title>[^\]]+?)\*?\]\((?P<url>[^)]+)\)"
    r"(?:,[^\n]*?around\s+(?P<time>\d{1,2}:\d\d(?::\d\d)?))?", re.M)


def norm(s):
    s = s.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def to_seconds(t):
    parts = [int(x) for x in t.split(":")]
    if len(parts) == 2:
        parts = [0] + parts
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def video_id(url):
    m = re.search(r"(?:v=|youtu\.be/)([\w-]{6,})", url or "")
    return m.group(1) if m else None


def blocks(text):
    """Yield (quote_text, credit_match) for each credited blockquote."""
    for m in CREDIT_RE.finditer(text):
        start = text.rfind("\n\n", 0, m.start()) + 2 if "\n\n" in text[:m.start()] else 0
        quote_lines = [ln[1:].strip() for ln in text[start:m.start()].splitlines() if ln.startswith(">")]
        q = " ".join(quote_lines).strip()
        q = q.strip('"“”').strip()
        if q:
            yield q, m


def find_episode(index, title, url):
    vid = video_id(url)
    for ep in index:
        if vid and video_id(ep.get("youtube_url")) == vid:
            return ep
    want = norm(title)
    for ep in index:
        if want and (want in norm(ep["title"]) or norm(ep["title"]) in want):
            return ep
    return None


def locate(quote, ep_path):
    """Return (speaker, 'HH:MM:SS') of the turn containing the quote, or None."""
    segs = [norm(x) for x in re.split(r"\[\s*(?:\.\.\.|…)\s*\]", quote) if norm(x)]
    if not segs:
        return None
    for speaker, ts, text, _ in turns(ep_path):
        t = norm(text)
        pos, ok = 0, True
        for seg in segs:
            i = t.find(seg, pos)
            if i < 0:
                ok = False
                break
            pos = i + len(seg)
        if ok:
            return speaker, ts
    # a quote may run across two turns of the same speaker: join consecutive turns
    prev = None
    for speaker, ts, text, _ in turns(ep_path):
        if prev and prev[0] == speaker:
            t = norm(prev[2] + " " + text)
            if all(seg in t for seg in segs):
                return speaker, prev[1]
        prev = (speaker, ts, text)
    return None


def check_file(path, index, root):
    text = open(path, encoding="utf-8").read()
    problems, warns, n = [], [], 0
    for quote, cm in blocks(text):
        n += 1
        words = len(quote.split())
        label = f'"{quote[:50]}..."'
        if words > 40:
            warns.append(f"{label}: {words} words (aim for under 40)")
        ep = find_episode(index, cm.group("title"), cm.group("url"))
        if not ep:
            problems.append(f"{label}: episode not found in index.json ({cm.group('title')[:40]})")
            continue
        hit = locate(quote, os.path.join(root, ep["file"]))
        if not hit:
            problems.append(f"{label}: words not found in '{ep['title'][:50]}'")
            continue
        speaker, ts = hit
        guest = norm(cm.group("guest"))
        if guest and not any(p in norm(speaker) for p in guest.split() if len(p) > 2):
            problems.append(f"{label}: credited to {cm.group('guest').strip()} but the transcript says {speaker}")
        if cm.group("time"):
            if abs(to_seconds(cm.group("time")) - to_seconds(ts)) > 180:
                problems.append(f"{label}: credit says around {cm.group('time')}, transcript has it at {ts}")
        else:
            warns.append(f"{label}: no 'around mm:ss' in the credit (transcript time {ts})")
        if "growth podcast" not in cm.group(0).lower():
            warns.append(f"{label}: credit line does not name The Growth Podcast")
    if n > 5:
        warns.append(f"{n} quotes in one lesson (a handful at most)")
    if n and "growth podcast with aakash gupta" not in text.lower():
        warns.append("lesson has quotes but no show credit line in Sources (see VOICE-GUIDE.md)")
    return n, problems, warns


def main(argv):
    root = transcripts_dir()
    if not os.path.exists(os.path.join(root, "index.json")):
        print(f"check_quotes: transcripts not found at {root}; skipping (set GROWTH_PODCAST_DIR to check quotes).")
        return 0
    targets = []
    for a in argv or ["."]:
        if a.endswith(".md"):
            targets.append(a)
        else:
            targets += sorted(glob.glob(os.path.join(ROOT, a, "*.md")))
    index = load_index(root)
    total, bad = 0, 0
    for p in targets:
        n, problems, warns = check_file(p, index, root)
        total += n
        if problems:
            bad += len(problems)
        if n or problems or warns:
            print(f"{os.path.relpath(p, ROOT)}: {n} quote(s)")
            for x in problems:
                print(f"  FAIL  {x}")
            for x in warns:
                print(f"  warn  {x}")
    print(f"check_quotes: {total} quote(s) checked, {bad} failure(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
