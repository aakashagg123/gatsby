#!/usr/bin/env python3
"""Build glossary artifacts from scripts/glossary_data.py.

Two outputs, one source of truth:
  1. GLOSSARY.md  — the GitHub-readable, enriched glossary (regenerated).
  2. widget data  — entries with `see` mapped to deployed URLs, consumed by
     build_site.py to write _site/assets/glossary.js (see glossary_widget.py).

Run standalone to regenerate GLOSSARY.md and validate every entry:
    python3 scripts/build_glossary.py
Exits non-zero on a broken lesson link, duplicate slug, or dangling related key.
"""
import os
import re
import sys

from glossary_data import GLOSSARY

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Flat standalone tracks: <track>/<lesson>.md -> <track>/<lesson>.html
FLAT_TRACKS = {
    "agentic-ai", "first-principles", "product-sense", "technical-product-sense",
    "technical-product-management", "knowledge-graphs",
}
# Phased tracks share the harness folder shape; only README/foundations are linked.
PHASED = {"flowable": "flowable", "harness-engineering": "harness"}


def deployed_url(md):
    """Map a repo-relative .md lesson path to its deployed site URL."""
    anchor = ""
    if "#" in md:
        md, anchor = md.split("#", 1)
        anchor = "#" + anchor
    parts = md.split("/")
    top = parts[0]
    if top == "content":                       # content/<mod>/<file>.md -> ai/<mod>.html[#lesson]
        mod, fname = parts[1], parts[2]
        if fname == "README.md":
            return f"ai/{mod}.html{anchor}"
        return f"ai/{mod}.html#{fname[:-3]}"
    if top in FLAT_TRACKS:                      # <flat>/<file>.md
        fname = parts[1]
        page = "index" if fname == "README.md" else fname[:-3]
        return f"{top}/{page}.html{anchor}"
    if top in PHASED:                           # flowable/README.md, flowable/foundations/<x>.md
        prefix = PHASED[top]
        rest = parts[1:]
        if rest == ["README.md"]:
            return f"{prefix}/index.html{anchor}"
        return f"{prefix}/{'/'.join(rest)[:-3]}.html{anchor}"
    raise ValueError(f"don't know how to deploy-map: {md}")


def validate():
    errs = []
    seen = set()
    keys = {e["k"] for e in GLOSSARY}
    for e in GLOSSARY:
        k = e["k"]
        if k in seen:
            errs.append(f"duplicate slug: {k}")
        seen.add(k)
        for field in ("t", "cat", "short", "fp", "see"):
            if not e.get(field):
                errs.append(f"{k}: missing '{field}'")
        label, md = e["see"]
        if not os.path.exists(os.path.join(ROOT, md.split("#")[0])):
            errs.append(f"{k}: see-path does not exist: {md}")
        for rel in e.get("related", []):
            if rel not in keys:
                errs.append(f"{k}: dangling related key: {rel}")
    return errs


def site_entries():
    """dict keyed by slug for the widget (see -> deployed url + label)."""
    out = {}
    for e in GLOSSARY:
        label, md = e["see"]
        entry = {
            "t": e["t"],
            "cat": e["cat"],
            "fp": e["fp"],
            "example": e.get("example", ""),
            "uses": e.get("uses", []),
            "see": {"href": deployed_url(md), "label": label},
            "related": e.get("related", []),
        }
        if e.get("aliases"):
            entry["aliases"] = e["aliases"]
        if e.get("cs"):
            entry["cs"] = True
        if e.get("autolink") is False:
            entry["autolink"] = False
        out[e["k"]] = entry
    return out


def site_keyterms():
    """Map each home page URL (no anchor) -> its must-know term slugs.

    A term is must-know for the lesson it homes to (its `see`), which is the
    operational form of 'argument-critical' from GLOSSARY_FRAMEWORK.md. The
    widget renders these as a per-lesson 'Key terms' box.
    """
    tbyk = {e["k"]: e["t"] for e in GLOSSARY}
    out = {}
    for e in GLOSSARY:
        _, md = e["see"]
        url = deployed_url(md).split("#")[0]
        out.setdefault(url, set()).add(e["k"])
    return {url: sorted(keys, key=lambda k: tbyk[k].lower()) for url, keys in out.items()}


HEADER = """# Glossary

Plain-language definitions for the jargon used across the curriculum — written to be
understood from a product-leader lens. Each term has a first-principles explanation, a
concrete example, and a link to the lesson where it's developed in depth.

On the [live site](https://aakashagg123.github.io/gatsby/), these terms are **clickable
inside every lesson**: the first time a term appears on a page, click it to open a
sidebar with this same explanation, its use-cases, and related terms. Each lesson also
shows a **Key terms** box of the terms it develops.

Which words get an entry — and why — is defined by the rubric in
[`GLOSSARY_FRAMEWORK.md`](./GLOSSARY_FRAMEWORK.md).

> This file is generated from `scripts/glossary_data.py`. Edit the data there and run
> `python3 scripts/build_glossary.py` — don't hand-edit below this line.

---

"""


def render_markdown():
    entries = sorted(GLOSSARY, key=lambda e: e["t"].lower())
    out = [HEADER]
    for e in entries:
        label, md = e["see"]
        link = f"[{label}](./{md})"
        block = [f"**{e['t']}** — {e['short']}", ""]
        block.append(f"*In plain terms.* {e['fp']}")
        if e.get("example"):
            block.append("")
            block.append(f"*For example.* {e['example']}")
        if e.get("uses"):
            block.append("")
            block.append("*Where it shows up:* " + "; ".join(e["uses"]) + ".")
        block.append("")
        block.append(f"*See:* {link}.")
        out.append("\n".join(block))
    return "\n\n".join(out).rstrip() + "\n"


def main():
    errs = validate()
    if errs:
        print("GLOSSARY VALIDATION FAILED:")
        for x in errs:
            print("  ", x)
        sys.exit(1)
    # exercise the URL mapper so a bad mapping fails loudly here too
    site_entries()
    with open(os.path.join(ROOT, "GLOSSARY.md"), "w", encoding="utf-8") as f:
        f.write(render_markdown())
    print(f"GLOSSARY.md regenerated — {len(GLOSSARY)} terms, all links valid.")


if __name__ == "__main__":
    main()
