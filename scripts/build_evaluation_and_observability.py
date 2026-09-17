#!/usr/bin/env python3
"""Build the standalone "Evaluation & observability" module (Generative AI family,
module 9).

A thin config wrapper around build_standalone.build_track. Source is
evaluation-and-observability/; output is evaluation-and-observability-html/.
Deliberately 2 lessons, not 7 — see the module README for why: this is the most
exhaustively covered topic in the curriculum, developed in full engineering depth
across content/04-evals-observability/evals.md, content/04-evals-observability/
observability.md, agentic-ai/reliability-and-evals.md, and technical-product-management/
tpm-for-ai-products.md. See GENERATIVE_AI_ROADMAP.md.
Run:  python3 scripts/build_evaluation_and_observability.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "evaluation-and-observability"),
    "out": os.path.join(ROOT, "evaluation-and-observability-html"),
    "brand": "Evaluation & observability",
    "tagline": "a Generative AI module",
    "title": "Evaluation & observability for the product leader",
    "lede": "Why treating the eval set as the product spec for a non-deterministic "
            "system is the job, not a nice-to-have, and the order to actually build "
            "the eval and observability stack in.",
    "meta": ["2 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "why-eval-investment-is-the-job",
        "building-the-eval-stack-in-the-right-order",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
