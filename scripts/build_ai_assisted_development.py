#!/usr/bin/env python3
"""Build the standalone "AI-assisted development" module (craft tracks).

A thin config wrapper around build_standalone.build_track. Source is ai-assisted-development/;
output is ai-assisted-development-html/. Lessons carry hand-built diagrams
(diagrams/ai-assisted-development/), and the landing page opens with a knowledge graph.
Run:  python3 scripts/build_ai_assisted_development.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "ai-assisted-development"),
    "out": os.path.join(ROOT, "ai-assisted-development-html"),
    "brand": "AI-assisted development",
    "tagline": "a craft track",
    "title": "AI-assisted development for the product and technology leader",
    "lede": "What changes when a coding agent writes the code: specifying, verifying, controlling and "
            "measuring the work, with runnable examples and one real Stop-hook script.",
    "insight": "When an agent writes the code, the scarce work is specifying and verifying, so speed comes from the checks you build, not from the agent.",
    "meta": ["6 lessons", "+ recap", "runnable code", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "when-an-agent-writes-the-code",
        "specs-and-the-context-file",
        "verification-is-the-product",
        "control-permissions-modes-and-hooks",
        "running-at-scale",
        "measuring-and-governing",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
