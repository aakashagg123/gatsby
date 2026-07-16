#!/usr/bin/env python3
"""Build the standalone "Agentic AI" track.

A thin config wrapper around build_standalone.build_track. Source is agentic-ai/;
output is agentic-ai-html/. Lessons carry rendered mermaid diagrams, and the landing
page opens with a knowledge graph. Run:  python3 scripts/build_agentic_ai.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "agentic-ai"),
    "out": os.path.join(ROOT, "agentic-ai-html"),
    "brand": "Agentic AI",
    "tagline": "a standalone module",
    "title": "Agentic AI for the AI PM",
    "lede": "What agents actually are — the loop, tools, memory, and planning — and the "
            "reliability, security, and economics that turn demos into products.",
    "meta": ["8 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the AI PM",
    "lessons": [
        "what-is-an-agent",
        "tools-and-function-calling",
        "context-and-memory",
        "planning-and-reasoning",
        "multi-agent-and-protocols",
        "reliability-and-evals",
        "safety-security-and-governance",
        "agentic-ai-as-a-product",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
