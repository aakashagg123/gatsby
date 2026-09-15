#!/usr/bin/env python3
"""Build the standalone "Generative AI: the big picture" module (Generative AI family).

A thin config wrapper around build_standalone.build_track. Source is generative-ai/;
output is generative-ai-html/. Lessons carry rendered mermaid diagrams, and the landing
page opens with a knowledge graph. This is module 1 of the Generative AI family —
see GENERATIVE_AI_ROADMAP.md.
Run:  python3 scripts/build_generative_ai.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "generative-ai"),
    "out": os.path.join(ROOT, "generative-ai-html"),
    "brand": "Generative AI",
    "tagline": "a Generative AI module",
    "title": "Generative AI: the big picture",
    "lede": "What makes AI \"generative,\" the five modalities, why output is "
            "probabilistic, the four-layer product stack, and build vs. buy vs. fine-tune.",
    "meta": ["6 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "what-is-generative-ai",
        "the-modalities",
        "probabilistic-software",
        "the-genai-product-stack",
        "build-buy-or-fine-tune",
        "where-value-is-created-and-destroyed",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
