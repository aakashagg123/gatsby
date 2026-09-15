#!/usr/bin/env python3
"""Build the standalone "Memory & context" module (Generative AI family, module 5).

A thin config wrapper around build_standalone.build_track. Source is
memory-and-context/; output is memory-and-context-html/. Deliberately 4 lessons, not
6 — see the module README for why: the engineering mechanics of context/memory are
already developed in depth in content/00-foundations/context-engineering.md and
agentic-ai/context-and-memory.md, so this module stays at the product-decision altitude
those two don't lead with. See GENERATIVE_AI_ROADMAP.md.
Run:  python3 scripts/build_memory_and_context.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "memory-and-context"),
    "out": os.path.join(ROOT, "memory-and-context-html"),
    "brand": "Memory & context",
    "tagline": "a Generative AI module",
    "title": "Memory & context for the product leader",
    "lede": "Memory as a product decision, the three shapes it takes, retrieval as its "
            "most common implementation, and the trust failures it has to be designed "
            "against.",
    "meta": ["4 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "memory-as-a-product-decision",
        "session-user-and-organizational-memory",
        "retrieval-as-memory",
        "when-memory-goes-wrong",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
