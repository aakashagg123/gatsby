#!/usr/bin/env python3
"""Build the standalone "Building AI-native products" module (craft tracks).

A thin config wrapper around build_standalone.build_track. Source is building-ai-native-products/;
output is building-ai-native-products-html/. Lessons carry hand-built diagrams
(diagrams/building-ai-native-products/), and the landing page opens with a knowledge graph.
Run:  python3 scripts/build_building_ai_native_products.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "building-ai-native-products"),
    "out": os.path.join(ROOT, "building-ai-native-products-html"),
    "brand": "Building AI-native products",
    "tagline": "a craft track",
    "title": "Building AI-native products",
    "lede": "Five skills for the AI product leader: opinionated UX for ambiguous interaction, model intuition, "
            "the loop from pixels to evals to hill climbing, agentic flows, and how users really behave with agents. "
            "Each skill has a judgement lesson and a practice lesson with templates.",
    "insight": "An AI-native product is designed around uncertainty: you decide what the model should do, measure it with evals, and shape the flow so people can trust and correct it.",
    "meta": ["11 lessons", "+ recap", "templates and teardowns", "knowledge graph", "diagrams included"],
    "callout": "For the AI product leader",
    "lessons": [
        "designing-for-ambiguity",
        "ux-practice-the-ai-feature-spec",
        "model-intuition",
        "model-intuition-practice",
        "from-pixels-to-evals",
        "hill-climbing-in-practice",
        "designing-agentic-flows",
        "agentic-flows-practice",
        "how-users-behave-with-agents",
        "researching-agent-interactions",
        "capstone-ship-one-ai-native-feature",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
