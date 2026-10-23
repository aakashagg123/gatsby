#!/usr/bin/env python3
"""Verify the compiled site in _site/ (run `python3 scripts/build_site.py` first).

Checks every built HTML page for:
  - no internal link to a raw .md file or a README.html (redirect stubs excepted)
  - no broken internal link (the target file, or the directory's index.html, must exist)
  - a <link rel="canonical"> that points under CANONICAL_BASE
  - no orphaned graph node (every node has at least one edge, and its page exists)

Run:  python3 scripts/check_site.py        (exit 1 if anything fails)
"""
import os
import re
import sys
from urllib.parse import unquote, urldefrag, urlparse

import build_graph
import build_site

SITE = build_site.SITE
HREF_RE = re.compile(r'<a\b[^>]*?\bhref="([^"]+)"', re.I)
CANON_RE = re.compile(r'<link rel="canonical" href="([^"]+)"')
SKIP = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:", "#")


def pages():
    for dp, _, files in os.walk(SITE):
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.join(dp, fn)


def resolve(page, href):
    """Absolute path of the file an internal href should land on, or None to skip."""
    path = unquote(urlparse(urldefrag(href)[0]).path)
    if not path:
        return None
    target = os.path.normpath(os.path.join(os.path.dirname(page), path))
    if os.path.isdir(target):
        target = os.path.join(target, "index.html")
    return target


def main():
    if not os.path.isdir(SITE):
        sys.exit("_site/ not found; run scripts/build_site.py first")
    md_links, readme_links, broken, no_canon, bad_canon = [], [], [], [], []
    n_pages = n_links = 0
    for page in pages():
        text = open(page, encoding="utf-8").read()
        rel = os.path.relpath(page, SITE)
        n_pages += 1
        m = CANON_RE.search(text)
        if not m:
            no_canon.append(rel)
        elif not m.group(1).startswith(build_site.CANONICAL_BASE):
            bad_canon.append(f"{rel} -> {m.group(1)}")
        is_stub = 'http-equiv="refresh"' in text
        for href in HREF_RE.findall(text):
            if href.startswith(SKIP) or any(c in href for c in "'+{}<>"):   # JS string templates
                continue
            n_links += 1
            base = urlparse(urldefrag(href)[0]).path
            if base.endswith(".md"):
                md_links.append(f"{rel} -> {href}")
            if base.endswith("README.html") and not is_stub:
                readme_links.append(f"{rel} -> {href}")
            target = resolve(page, href)
            if target and not os.path.exists(target):
                broken.append(f"{rel} -> {href}")

    data = build_graph.graph_data()
    degree = [0] * len(data["nodes"])
    for e in data["edges"]:
        degree[e[0]] += 1
        degree[e[1]] += 1
    orphans = [n["title"] for n, d in zip(data["nodes"], degree) if d == 0]
    missing = [n["url"] for n in data["nodes"]
               if not os.path.exists(os.path.join(SITE, n["url"].split("#")[0]))]

    failed = False
    for label, items in (("links to .md files", md_links), ("links to README.html", readme_links),
                         ("broken internal links", broken), ("pages without canonical", no_canon),
                         ("canonical outside base", bad_canon), ("orphaned graph nodes", orphans),
                         ("graph nodes with no page", missing)):
        if items:
            failed = True
            print(f"FAIL {label}: {len(items)}")
            for i in items[:15]:
                print("   ", i)
        else:
            print(f"ok   0 {label}")
    print(f"checked {n_pages} pages, {n_links} internal links, {len(data['nodes'])} graph nodes, "
          f"{sum(1 for e in data['edges'] if e[3] == 'link')} cross-references")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
