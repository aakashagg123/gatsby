#!/usr/bin/env python3
"""Build the standalone "Transformers" module (foundation modules, module 4).

A thin config wrapper around build_standalone.build_track. Source is transformers/;
output is transformers-html/. Lessons carry hand-built diagrams (diagrams/transformers/),
and the landing page opens with a knowledge graph.
Run:  python3 scripts/build_transformers.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "transformers"),
    "out": os.path.join(ROOT, "transformers-html"),
    "brand": "Transformers",
    "tagline": "a foundation module",
    "title": "Transformers for the product and technology leader",
    "lede": "The stack behind almost every language model: attention, the block, position and the cost of "
            "context, the KV cache, and how to read a model card as memory, compute and cost.",
    "insight": "A transformer is one block repeated, so almost every question about it is a counting question: parameters, multiply-adds and cache.",
    "meta": ["6 lessons", "+ recap", "runnable code", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "the-shape-of-a-transformer",
        "attention",
        "the-block",
        "position-and-the-cost-of-context",
        "generating-text-and-the-kv-cache",
        "variants-and-reading-a-model-card",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
