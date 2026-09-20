#!/usr/bin/env python3
"""Build the standalone "Context engineering" track.

A thin config wrapper around build_standalone.build_track. Source is
context-engineering/; output is context-engineering-html/.
Run:  python3 scripts/build_context_engineering.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "context-engineering"),
    "out": os.path.join(ROOT, "context-engineering-html"),
    "brand": "Context engineering",
    "tagline": "a standalone module",
    "title": "Context engineering for the product leader",
    "lede": "Treat what the model gets to see as a product decision — instructions, "
            "retrieval, memory, and live state, spec'd, governed, and evaluated "
            "with the same rigor as the output it produces.",
    "meta": ["7 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "what-is-context-engineering",
        "why-prompt-engineering-doesnt-scale",
        "the-anatomy-of-a-context-pipeline",
        "context-as-a-spec-able-requirement",
        "context-governance-at-scale",
        "evaluating-context-quality",
        "context-across-the-product-lifecycle",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
