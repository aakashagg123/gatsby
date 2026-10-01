#!/usr/bin/env python3
"""Build the standalone "Access control" track (RBAC, ABAC, ReBAC and Keycloak).

A thin config wrapper around build_standalone.build_track. Source is access-control/;
output is access-control-html/. Lessons carry hand-crafted HTML diagrams that replace
mermaid fences via the diagram-override mechanism.
Run:  python3 scripts/build_access_control.py
"""
import os
from build_standalone import build_track

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG = {
    "src": os.path.join(ROOT, "access-control"),
    "out": os.path.join(ROOT, "access-control-html"),
    "brand": "Access control",
    "tagline": "a standalone module",
    "title": "Access control for the technical PM",
    "lede": "Who may do what, and where that is decided: authentication vs authorization, "
            "OAuth and tokens, RBAC, ABAC, relationship-based access, Keycloak, and "
            "access control for AI agents.",
    "meta": ["8 lessons", "+ recap", "Keycloak tested", "diagrams included"],
    "callout": "For the technical PM",
    "lessons": [
        "authentication-authorization-and-the-access-control-model",
        "oauth-openid-connect-and-tokens",
        "rbac-roles-groups-and-where-it-breaks",
        "abac-deciding-with-attributes-and-context",
        "rebac-and-policy-engines",
        "keycloak-realms-clients-roles-groups-and-tokens",
        "keycloak-authorization-services",
        "access-control-for-ai-agents",
    ],
}

if __name__ == "__main__":
    build_track(CFG)
