#!/usr/bin/env python3
"""Build the standalone "RAG & vector databases" module (Generative AI family).

A thin config wrapper around build_standalone.build_track. Source is
rag-vector-databases/; output is rag-vector-databases-html/. Lessons carry rendered
mermaid diagrams, and the landing page opens with a knowledge graph.
Run:  python3 scripts/build_rag_vector_databases.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "rag-vector-databases"),
    "out": os.path.join(ROOT, "rag-vector-databases-html"),
    "brand": "RAG & vector databases",
    "tagline": "a Generative AI module",
    "title": "RAG & vector databases for the product leader",
    "lede": "Grounding models in your data — embeddings, vector databases, chunking, "
            "retrieval quality, and when to reach for long-context, fine-tuning, or a graph.",
    "meta": ["7 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "why-rag",
        "embeddings-and-semantic-search",
        "vector-databases",
        "chunking-and-ingestion",
        "retrieval-quality",
        "rag-vs-long-context-vs-finetuning",
        "graphrag-and-structured-retrieval",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
