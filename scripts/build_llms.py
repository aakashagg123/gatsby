#!/usr/bin/env python3
"""Build the standalone "LLMs" module (Generative AI family, module 2).

A thin config wrapper around build_standalone.build_track. Source is llms/; output is
llms-html/. Lessons carry rendered mermaid diagrams, and the landing page opens with a
knowledge graph. See GENERATIVE_AI_ROADMAP.md.
Run:  python3 scripts/build_llms.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "llms"),
    "out": os.path.join(ROOT, "llms-html"),
    "brand": "LLMs",
    "tagline": "a Generative AI module",
    "title": "LLMs for the product leader",
    "lede": "Tokens, the context window, the jagged frontier, prompting, sampling, "
            "choosing a model, and the order to reach for prompting, RAG, or fine-tuning.",
    "meta": ["7 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "what-is-an-llm",
        "the-context-window",
        "capabilities-and-the-jagged-frontier",
        "prompting-and-in-context-learning",
        "temperature-sampling-and-determinism",
        "choosing-a-model",
        "prompting-vs-rag-vs-finetuning",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
