#!/usr/bin/env python3
"""Build the standalone "AI security & guardrails" module (Generative AI family,
module 10).

A thin config wrapper around build_standalone.build_track. Source is
ai-security-and-guardrails/; output is ai-security-and-guardrails-html/.
Deliberately 2 lessons, not 7 — see the module README for why: prompt injection, the
lethal trifecta, data leakage, multi-tenant isolation, least privilege, human-in-the-loop,
and governance are already developed in full engineering depth across
content/05-safety-multitenancy/safety-engineering.md,
content/05-safety-multitenancy/multi-tenant-isolation.md, and
agentic-ai/safety-security-and-governance.md. See GENERATIVE_AI_ROADMAP.md.
Run:  python3 scripts/build_ai_security_and_guardrails.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "ai-security-and-guardrails"),
    "out": os.path.join(ROOT, "ai-security-and-guardrails-html"),
    "brand": "AI security & guardrails",
    "tagline": "a Generative AI module",
    "title": "AI security & guardrails for the product leader",
    "lede": "Jailbreak, injection, extraction, and poisoning are four different attacks, "
            "not one — and why governance only counts once it becomes compliance "
            "evidence a regulator or an enterprise buyer can actually check.",
    "meta": ["2 lessons", "+ recap", "knowledge graph", "diagrams included"],
    "callout": "For the product leader",
    "lessons": [
        "the-threat-model-and-guardrails",
        "governance-audit-and-compliance",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
