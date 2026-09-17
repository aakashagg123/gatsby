#!/usr/bin/env python3
"""Build the standalone "Agentic workflows" module (Generative AI family, module 8).

A thin config wrapper around build_standalone.build_track. Source is
agentic-workflows/; output is agentic-workflows-html/. Deliberately 2 lessons, not
6 — see the module README for why: agentic-ai/multi-agent-and-protocols.md already
develops orchestration topologies and the MCP/A2A protocol landscape in full depth,
the workflow-vs-agent distinction is already covered in the AI agents module, durable
execution is the entire subject of the Flowable track, and workflow capture as strategy
is already a full section of agentic-ai-as-a-product.md. See GENERATIVE_AI_ROADMAP.md.
Run:  python3 scripts/build_agentic_workflows.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "agentic-workflows"),
    "out": os.path.join(ROOT, "agentic-workflows-html"),
    "brand": "Agentic workflows",
    "tagline": "a Generative AI module",
    "title": "Agentic workflows for the product leader",
    "lede": "Orchestrating more than one agent when a single loop isn't enough, and "
            "what it takes to make a workflow durable enough — and valuable enough — "
            "to be worth owning end to end.",
    "meta": ["2 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "orchestrating-more-than-one-agent",
        "making-a-workflow-durable-and-worth-owning",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
