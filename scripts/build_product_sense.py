#!/usr/bin/env python3
"""Build the standalone "Product sense" track.

A thin config wrapper around build_standalone.build_track. Source is product-sense/;
output is product-sense-html/. Run:  python3 scripts/build_product_sense.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "product-sense"),
    "out": os.path.join(ROOT, "product-sense-html"),
    "brand": "Product sense",
    "tagline": "a standalone module",
    "title": "Product sense for the AI PM",
    "lede": "The instinct for what makes a product succeed — sharpened for the AI era.",
    "meta": ["6 lessons", "+ recap", "for APMs & PMs", "AI-native"],
    "callout": "For the AI PM",
    "lessons": [
        "motivation-and-behaviour",
        "cognitive-empathy",
        "creativity",
        "communication",
        "domain-expertise",
        "product-sense-for-ai",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
