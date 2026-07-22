#!/usr/bin/env python3
"""Build the standalone "Knowledge graphs" track.

A thin config wrapper around build_standalone.build_track. Source is
knowledge-graphs/; output is knowledge-graphs-html/. Lessons carry rendered mermaid
diagrams, and the landing page opens with a knowledge graph (about knowledge graphs).
Run:  python3 scripts/build_knowledge_graphs.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "knowledge-graphs"),
    "out": os.path.join(ROOT, "knowledge-graphs-html"),
    "brand": "Knowledge graphs",
    "tagline": "a standalone module",
    "title": "Knowledge graphs for the product leader",
    "lede": "Treat what the company knows as a product — entities, relationships, "
            "ontologies, GraphRAG, governance, and the business case, in CPO language.",
    "meta": ["8 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "what-is-a-knowledge-graph",
        "ontologies-and-data-modeling",
        "building-the-graph",
        "storage-and-querying",
        "reasoning-and-analytics",
        "knowledge-graphs-and-llms",
        "governance-quality-and-trust",
        "knowledge-graphs-as-a-product",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
