#!/usr/bin/env python3
"""Build the standalone "AI agents" module (Generative AI family, module 7).

A thin config wrapper around build_standalone.build_track. Source is ai-agents/;
output is ai-agents-html/. Deliberately 3 lessons, not 7 — see the module README for
why: agentic-ai/ already develops the loop, autonomy spectrum, planning & reasoning,
reliability, and agent economics in full depth, and two of the planned lessons (tools,
memory) are already the dedicated subject of the Tool calling and Memory & context
sibling modules in this family. See GENERATIVE_AI_ROADMAP.md.
Run:  python3 scripts/build_ai_agents.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "ai-agents"),
    "out": os.path.join(ROOT, "ai-agents-html"),
    "brand": "AI agents",
    "tagline": "a Generative AI module",
    "title": "AI agents for the product leader",
    "lede": "The loop behind every agent, how much autonomy a task actually needs, "
            "what keeps it reliable across many steps, and the economics that decide "
            "whether it's worth building at all.",
    "meta": ["3 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "what-an-agent-is-and-how-much-autonomy-it-needs",
        "planning-reasoning-and-reliability-across-a-run",
        "when-not-to-build-an-agent",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
