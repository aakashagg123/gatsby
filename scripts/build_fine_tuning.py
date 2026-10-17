#!/usr/bin/env python3
"""Build the standalone "Fine-tuning and post-training" module (foundation modules).

A thin config wrapper around build_standalone.build_track. Source is fine-tuning/;
output is fine-tuning-html/. Lessons carry hand-built diagrams (diagrams/fine-tuning/),
and the landing page opens with a knowledge graph.
Run:  python3 scripts/build_fine_tuning.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "fine-tuning"),
    "out": os.path.join(ROOT, "fine-tuning-html"),
    "brand": "Fine-tuning",
    "tagline": "a foundation module",
    "title": "Fine-tuning and post-training for the product and technology leader",
    "lede": "How a base model becomes an assistant, what supervised tuning, LoRA and preference tuning "
            "change, why the dataset is the product, and how to test the break-even and gate the release.",
    "insight": "Tuning is a small push on a model that already knows most of what it knows, so it changes behaviour well, adds facts badly, and needs a test and a break-even before you start.",
    "meta": ["6 lessons", "+ recap", "runnable code", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "from-base-model-to-assistant",
        "supervised-fine-tuning",
        "lora-and-parameter-efficient-tuning",
        "preference-tuning-and-reward-hacking",
        "the-dataset",
        "deciding-costing-and-checking-a-fine-tune",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
