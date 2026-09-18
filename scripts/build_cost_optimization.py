#!/usr/bin/env python3
"""Build the standalone "Cost optimization" module (Generative AI family, module 11 —
the final module in the family).

A thin config wrapper around build_standalone.build_track. Source is
cost-optimization/; output is cost-optimization-html/.
Deliberately 2 lessons, not 6 — see the module README for why: token economics,
caching, routing, context cost, and unit economics are already developed in full
engineering depth across content/01-inference-internals/prefill-vs-decode.md,
content/01-inference-internals/batching-and-paged-attention.md,
content/01-inference-internals/prompt-vs-semantic-caching.md,
content/02-reliable-outputs/model-routing.md,
content/04-evals-observability/cost-attribution.md, and
agentic-ai/agentic-ai-as-a-product.md. See GENERATIVE_AI_ROADMAP.md.
Run:  python3 scripts/build_cost_optimization.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "cost-optimization"),
    "out": os.path.join(ROOT, "cost-optimization-html"),
    "brand": "Cost optimization",
    "tagline": "a Generative AI module",
    "title": "Cost optimization for the product leader",
    "lede": "Which lever fixes which cost driver, the build-vs-buy breakeven done as "
            "arithmetic, and the FinOps practice that turns attribution into "
            "governance before the invoice, not after.",
    "meta": ["2 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "the-cost-stack-and-the-build-vs-buy-breakeven",
        "finops-budgets-forecasting-and-the-cost-review",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
