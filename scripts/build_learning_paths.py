#!/usr/bin/env python3
"""Build the standalone "Learning paths" track.

A thin config wrapper around build_standalone.build_track. Source is learning-paths/;
output is learning-paths-html/. The four path pages are generated from the track build
configs so their lesson links and time estimates stay in step with the tracks.
Run:  python3 scripts/build_learning_paths.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "learning-paths"),
    "out": os.path.join(ROOT, "learning-paths-html"),
    "brand": "Learning paths",
    "tagline": "start here",
    "title": "Learning paths for four roles",
    "lede": "The tracks, put in order for a senior product manager, an AI product lead, "
            "an AI engineer, or an AI engineering lead. Each path says which lessons to read, "
            "what to skip, and when to move on.",
    "meta": ["4 paths", "+ recap", "time estimates", "checkpoints"],
    "callout": "For your role",
    "lessons": [
        "senior-product-manager",
        "ai-product-lead",
        "ai-engineer",
        "ai-engineering-lead",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
