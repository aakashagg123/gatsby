#!/usr/bin/env python3
"""Build the standalone "Machine learning" module (foundation modules, module 1).

A thin config wrapper around build_standalone.build_track. Source is machine-learning/;
output is machine-learning-html/. Lessons carry hand-built diagrams (diagrams/machine-learning/),
and the landing page opens with a knowledge graph. See MACHINE_LEARNING_ROADMAP.md.
Run:  python3 scripts/build_machine_learning.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "machine-learning"),
    "out": os.path.join(ROOT, "machine-learning-html"),
    "brand": "Machine learning",
    "tagline": "a foundation module",
    "title": "Machine learning for the product and technology leader",
    "lede": "What a learned system is, what it learns from, how it learns, how to trust its "
            "score, which kind of model to pick, and how to keep it working after launch.",
    "meta": ["8 lessons", "+ recap", "runnable code", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "what-machine-learning-is",
        "data-features-labels-and-leakage",
        "training-loss-and-gradient-descent",
        "generalization-overfitting-and-bias-variance",
        "measuring-a-model",
        "model-families",
        "ml-in-production",
        "learning-and-doing-ml-with-claude-code",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
