#!/usr/bin/env python3
"""Build the standalone "APIs & integrations" module (Generative AI family, module 3).

A thin config wrapper around build_standalone.build_track. Source is api-integrations/;
output is api-integrations-html/. Lessons carry rendered mermaid diagrams, and the
landing page opens with a knowledge graph. See GENERATIVE_AI_ROADMAP.md.
Run:  python3 scripts/build_api_integrations.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "api-integrations"),
    "out": os.path.join(ROOT, "api-integrations-html"),
    "brand": "APIs & integrations",
    "tagline": "a Generative AI module",
    "title": "APIs & integrations for the product leader",
    "lede": "The request/response contract, authentication, rate limits, streaming, "
            "retries, structured output, webhooks, and fitting a model call into a "
            "real system.",
    "meta": ["6 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "the-request-response-contract",
        "calling-an-llm-api",
        "structured-output-and-json-mode",
        "webhooks-and-async-patterns",
        "integrating-into-existing-systems",
        "mcp-and-standard-connectors",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
