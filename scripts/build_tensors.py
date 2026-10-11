#!/usr/bin/env python3
"""Build the standalone "Tensors" module (foundation modules, module 2).

A thin config wrapper around build_standalone.build_track. Source is tensors/;
output is tensors-html/. Lessons carry hand-built diagrams (diagrams/tensors/),
and the landing page opens with a knowledge graph. See TENSORS_ROADMAP.md.
Run:  python3 scripts/build_tensors.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "tensors"),
    "out": os.path.join(ROOT, "tensors-html"),
    "brand": "Tensors",
    "tagline": "a foundation module",
    "title": "Tensors for the product and technology leader",
    "lede": "What the objects every model works on are, what they cost in memory and compute, "
            "why shape errors are silent, and how a library gets the gradient for free.",
    "meta": ["5 lessons", "+ recap", "runnable code", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "what-a-tensor-is",
        "operations-and-broadcasting",
        "matrix-multiplication",
        "batching-memory-and-precision",
        "automatic-differentiation",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
