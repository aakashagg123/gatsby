#!/usr/bin/env python3
"""Build the standalone "Tool calling" module (Generative AI family, module 6).

A thin config wrapper around build_standalone.build_track. Source is tool-calling/;
output is tool-calling-html/. Deliberately 3 lessons, not 5 — see the module README
for why: the engineering mechanics are already developed in depth across
agentic-ai/tools-and-function-calling.md, content/02-reliable-outputs/function-calling.md,
and api-integrations/mcp-and-standard-connectors.md, so this module stays at the
product-decision altitude those three don't lead with. See GENERATIVE_AI_ROADMAP.md.
Run:  python3 scripts/build_tool_calling.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "tool-calling"),
    "out": os.path.join(ROOT, "tool-calling-html"),
    "brand": "Tool calling",
    "tagline": "a Generative AI module",
    "title": "Tool calling for the product leader",
    "lede": "The line where an AI product stops talking and starts doing: what tool "
            "calling is, how to design a tool worth trusting, and how to keep the "
            "permission and trust boundary around it real.",
    "meta": ["3 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "what-tool-calling-is",
        "tool-contracts-and-reliability",
        "permissions-blast-radius-and-the-trust-boundary",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
