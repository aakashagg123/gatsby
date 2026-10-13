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
    "lede": "Grounding models in your data — when to use RAG and when not to, embeddings, "
            "vector databases, chunking, retrieval quality, the alternatives, and a hands-on "
            "build with Claude Code, pgvector and Pinecone.",
    "insight": "Use RAG only when the answer is a passage in knowledge too big, too fresh or too private to send whole. Then retrieval quality is the product.",
    "meta": ["10 lessons", "+ recap", "runnable code", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "when-to-use-rag",
        "why-rag",
        "embeddings-and-semantic-search",
        "vector-databases",
        "chunking-and-ingestion",
        "retrieval-quality",
        "rag-vs-long-context-vs-finetuning",
        "graphrag-and-structured-retrieval",
        "building-rag-with-claude-code",
        "rag-terms",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
