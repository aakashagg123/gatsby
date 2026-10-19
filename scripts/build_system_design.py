#!/usr/bin/env python3
"""Build the standalone "System Design" track.

A thin config wrapper around build_standalone.build_track. Source is system-design/;
output is system-design-html/. Lessons carry hand-crafted HTML diagrams that replace
mermaid fences via the diagram-override mechanism. Run:  python3 scripts/build_system_design.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "system-design"),
    "out": os.path.join(ROOT, "system-design-html"),
    "brand": "System Design",
    "tagline": "a systems module",
    "title": "System design for the technical PM",
    "lede": "How real systems are designed at scale — from rate limiters to stock exchanges — "
            "with the architecture, tradeoffs, and failure modes that shape product decisions.",
    "insight": "Start with the constraints, not the technology. The numbers drive the architecture, and every design must choose between correctness and throughput.",
    "meta": ["13 lessons", "+ recap", "28 systems", "runnable code", "diagrams included"],
    "callout": "For the technical PM",
    "lessons": [
        "foundations-and-framework",
        "numbers-and-formulas",
        "traffic-caching-apis-and-storage-choice",
        "core-building-blocks",
        "distributed-data-and-consistency",
        "web-scale-services",
        "real-time-systems",
        "storage-and-sync",
        "location-and-geo-services",
        "data-infrastructure",
        "transactional-and-financial",
        "reliability-and-operations",
        "question-bank",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
