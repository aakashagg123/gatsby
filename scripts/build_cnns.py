#!/usr/bin/env python3
"""Build the standalone "Convolutional networks" module (foundation modules, module 3).

A thin config wrapper around build_standalone.build_track. Source is cnns/;
output is cnns-html/. Lessons carry hand-built diagrams (diagrams/cnns/),
and the landing page opens with a knowledge graph.
Run:  python3 scripts/build_cnns.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "cnns"),
    "out": os.path.join(ROOT, "cnns-html"),
    "brand": "Convolutional networks",
    "tagline": "a foundation module",
    "title": "Convolutional networks for the product and technology leader",
    "lede": "How a vision model sees, what resolution and depth cost, when to reuse a pre-trained "
            "or foundation model, and why vision features break in production.",
    "insight": "A vision product is a chain of choices, each with a price, and the cheapest test is to measure on your own images before you commit.",
    "meta": ["7 lessons", "+ recap", "runnable code", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "what-computer-vision-does",
        "how-a-convolution-sees",
        "from-edges-to-objects",
        "transfer-learning-and-labels",
        "cnns-vs-vision-transformers",
        "vision-foundation-models",
        "shipping-vision-in-production",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
