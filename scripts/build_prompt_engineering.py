#!/usr/bin/env python3
"""Build the standalone "Prompt engineering" track.

A thin config wrapper around build_standalone.build_track. Source is
prompt-engineering/; output is prompt-engineering-html/.
Run:  python3 scripts/build_prompt_engineering.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "prompt-engineering"),
    "out": os.path.join(ROOT, "prompt-engineering-html"),
    "brand": "Prompt engineering",
    "tagline": "a standalone module",
    "title": "Prompt engineering, from productivity to coding agents",
    "lede": "The craft of writing input a model will reliably act on — from "
            "ChatGPT productivity patterns, through the classical techniques "
            "power users depend on, into the prompts that drive Claude Code, "
            "Cursor, and other coding agents.",
    "meta": ["9 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the AI PM (or coding-agent user)",
    "lessons": [
        "what-prompt-engineering-actually-is",
        "the-anatomy-of-a-prompt",
        "everyday-productivity-patterns",
        "structured-prompting",
        "few-shot-cot-self-consistency",
        "prompt-chaining-and-workflows",
        "prompting-for-tools-and-agents",
        "prompting-inside-coding-agents",
        "when-prompts-fail",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
