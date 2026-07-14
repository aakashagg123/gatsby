#!/usr/bin/env python3
"""Build the standalone "First Principles & the Polymath Mind" track.

A thin config wrapper around build_standalone.build_track. Source is first-principles/;
output is first-principles-html/. Run:  python3 scripts/build_first_principles.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "first-principles"),
    "out": os.path.join(ROOT, "first-principles-html"),
    "brand": "First principles",
    "tagline": "a standalone module",
    "title": "First principles & the polymath mind",
    "lede": "Reasoning from fundamentals — and building range across every discipline.",
    "meta": ["6 lessons", "+ recap", "first-principles", "polymath"],
    "callout": "For the builder",
    "lessons": [
        "what-is-first-principles",
        "the-method",
        "mental-models-latticework",
        "becoming-a-polymath",
        "learning-how-to-learn",
        "traps-and-limits",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
