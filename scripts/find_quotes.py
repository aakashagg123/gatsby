#!/usr/bin/env python3
"""Find candidate quotes in The Growth Podcast transcripts (read-only).

The transcripts are a separate repository (github.com/aakashg/growth-podcast-transcripts). Clone it
anywhere and point GROWTH_PODCAST_DIR at it. Default: /home/user/aakashg/growth-podcast-transcripts.

    python3 scripts/find_quotes.py "north star metric"
    python3 scripts/find_quotes.py "continuous discovery" --guest Torres --max 8
    python3 scripts/find_quotes.py "evals" --episode "AI Evals" --words 40

For every match it prints the speaker, the episode, the transcript time (mm:ss from the file), the
YouTube link and a short window of text, so a lesson can quote it with credit. Sponsor reads are skipped.
Transcript timestamps can differ from the video by a few minutes: always write "around", never "at".
Quotes are machine-made text: check names and numbers before you rely on them. See VOICE-GUIDE.md.
"""
import argparse
import json
import os
import re
import sys

DEFAULT_DIR = "/home/user/aakashg/growth-podcast-transcripts"
TURN_RE = re.compile(r"^\*\*(.+?)\*\* \((\d\d:\d\d:\d\d)\)\s*$")


def transcripts_dir():
    return os.environ.get("GROWTH_PODCAST_DIR", DEFAULT_DIR)


def load_index(root):
    with open(os.path.join(root, "index.json"), encoding="utf-8") as f:
        return json.load(f)


def turns(path):
    """Yield (speaker, 'HH:MM:SS', text, is_sponsor) for each speaker turn."""
    speaker = ts = None
    buf, sponsor = [], False
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = TURN_RE.match(line.rstrip("\n"))
            if m:
                if speaker is not None and buf:
                    yield speaker, ts, " ".join(buf).strip(), sponsor
                speaker, ts, buf, sponsor = m.group(1), m.group(2), [], False
                continue
            if "<!-- sponsor -->" in line:
                sponsor = True
                continue
            if speaker is not None and line.strip() and not line.startswith("---"):
                buf.append(line.strip())
    if speaker is not None and buf:
        yield speaker, ts, " ".join(buf).strip(), sponsor


def window(text, match, words):
    toks = text.split()
    pos = len(text[: match.start()].split())
    lo = max(0, pos - words // 2)
    return ("... " if lo else "") + " ".join(toks[lo: lo + words]) + (" ..." if lo + words < len(toks) else "")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", help="regular expression, case-insensitive")
    ap.add_argument("--guest", help="only turns whose speaker name contains this")
    ap.add_argument("--episode", help="only episodes whose title contains this")
    ap.add_argument("--max", type=int, default=12, help="maximum matches to print (default 12)")
    ap.add_argument("--words", type=int, default=45, help="words of context per match (default 45)")
    ap.add_argument("--after", help="only episodes dated on or after YYYY-MM")
    a = ap.parse_args()

    root = transcripts_dir()
    if not os.path.exists(os.path.join(root, "index.json")):
        sys.exit(f"transcripts not found at {root}. Clone https://github.com/aakashg/growth-podcast-transcripts "
                 "and set GROWTH_PODCAST_DIR.")
    rx = re.compile(a.query, re.I)
    shown = 0
    for ep in load_index(root):
        if a.episode and a.episode.lower() not in ep["title"].lower():
            continue
        if a.after and ep["date"][:7] < a.after:
            continue
        path = os.path.join(root, ep["file"])
        if not os.path.exists(path):
            continue
        for speaker, ts, text, sponsor in turns(path):
            if sponsor or (a.guest and a.guest.lower() not in speaker.lower()):
                continue
            m = rx.search(text)
            if not m:
                continue
            print(f"[{ep['date'][:10]}] {ep['title'][:90]}")
            print(f"  {speaker} around {ts[3:] if ts.startswith('00:') else ts}   {ep.get('youtube_url', '')}")
            print(f"  \"{window(text, m, a.words)}\"")
            print()
            shown += 1
            if shown >= a.max:
                return
    if not shown:
        print("no matches")


if __name__ == "__main__":
    main()
