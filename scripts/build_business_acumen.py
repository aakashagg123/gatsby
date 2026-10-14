#!/usr/bin/env python3
"""Build the standalone "Business acumen" track.

A thin config wrapper around build_standalone.build_track. Source is business-acumen/;
output is business-acumen-html/. The interactive self-assessment is an extra page built
from the HTML fragment diagrams/business-acumen/assessment.html (no markdown pass), styled
by design-system/site/61-assessment.css. Run:  python3 scripts/build_business_acumen.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "business-acumen"),
    "out": os.path.join(ROOT, "business-acumen-html"),
    "brand": "Business Acumen",
    "tagline": "a standalone module",
    "title": "Business acumen for the product leader",
    "lede": "Money, markets, organizations and influence for Group PMs, Heads of Product and "
            "VPs — grounded in FinTech, Payments, Lending, eCommerce, InsurTech and Retail.",
    "insight": "Every product decision is a bet on unit economics and cash, and it is judged "
               "against what would have happened anyway.",
    "meta": ["15 lessons", "+ recap", "interactive assessment", "6 domains"],
    "callout": "For the product leader",
    "lessons": [
        "foundations-and-assessment",
        "the-language-of-money",
        "unit-economics",
        "business-cases-and-valuation",
        "data-and-decisions",
        "markets-and-strategy",
        "competitive-advantage-and-strategy",
        "monetization-and-business-models",
        "products-and-marketing",
        "performance-and-growth",
        "portfolio-strategy-and-allocation",
        "navigating-the-organization",
        "teams-and-collaboration",
        "leading-leaders-and-org-design",
        "executive-influence-and-stakeholders",
    ],
    "extra_pages": [{
        "key": "assessment",
        "label": "Self-assessment",
        "chip": "Self-assessment",
        "badge": "✓",
        "title": "Business acumen self-assessment",
        "html": os.path.join(ROOT, "diagrams", "business-acumen", "assessment.html"),
    }],
}

if __name__ == "__main__":
    build_track(CFG)
