#!/usr/bin/env python3
"""Build the standalone "Technical product management" track.

A thin config wrapper around build_standalone.build_track. Source is
technical-product-management/; output is technical-product-management-html/. Lessons
carry rendered mermaid diagrams. Run:  python3 scripts/build_technical_product_management.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "technical-product-management"),
    "out": os.path.join(ROOT, "technical-product-management-html"),
    "brand": "Technical product management",
    "tagline": "a standalone module",
    "title": "Technical product management for the AI PM",
    "lede": "The operating discipline of shipping — the role, specs, prioritization, "
            "execution, metrics, and releases that carry an idea into production.",
    "meta": ["8 lessons", "+ recap", "for APMs & PMs", "diagrams included"],
    "callout": "For the AI PM",
    "lessons": [
        "the-technical-pm-role",
        "discovery-to-delivery",
        "specs-prds-and-rfcs",
        "prioritization-and-roadmaps",
        "working-with-engineering",
        "metrics-and-experimentation",
        "launches-rollouts-and-migrations",
        "incidents-and-postmortems",
        "tpm-for-ai-products",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
