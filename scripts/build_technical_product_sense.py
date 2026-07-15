#!/usr/bin/env python3
"""Build the standalone "Technical product sense" track.

A thin config wrapper around build_standalone.build_track. Source is
technical-product-sense/; output is technical-product-sense-html/. Lessons carry
rendered mermaid diagrams. Run:  python3 scripts/build_technical_product_sense.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "technical-product-sense"),
    "out": os.path.join(ROOT, "technical-product-sense-html"),
    "brand": "Technical product sense",
    "tagline": "a standalone module",
    "title": "Technical product sense for the AI PM",
    "lede": "Reading systems like an engineer — architecture, data, latency, and failure — "
            "so you can build with them, not just around them.",
    "meta": ["7 lessons", "+ recap", "for APMs & PMs", "diagrams included"],
    "callout": "For the AI PM",
    "lessons": [
        "how-systems-are-built",
        "apis-and-contracts",
        "data-and-the-data-model",
        "latency-scale-performance",
        "reliability-and-failure",
        "tech-debt-and-estimation",
        "technical-sense-for-ai",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
