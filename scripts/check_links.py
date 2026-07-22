#!/usr/bin/env python3
"""Verify that every relative markdown link in the curriculum resolves.

Scans all tracked .md files (content/, the standalone tracks, harness-engineering,
and the root docs) for [text](relative/path.md) links and reports any target that
does not exist on disk. Site-only links (http..., #anchors, mailto:) are ignored.

Run:  python3 scripts/check_links.py        (exit 1 if broken links found)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = [
    "content", "agentic-ai", "first-principles", "knowledge-graphs", "product-sense",
    "technical-product-management", "technical-product-sense",
    "harness-engineering", "flowable",
]
ROOT_FILES = ["README.md", "SUMMARY.md", "GLOSSARY.md"]

LINK_RE = re.compile(r"\]\(([^)\s]+?)(#[^)]*)?\)")


def md_files():
    for f in ROOT_FILES:
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            yield p
    for d in SCAN_DIRS:
        base = os.path.join(ROOT, d)
        for dirpath, _, files in os.walk(base):
            for fn in files:
                if fn.endswith(".md"):
                    yield os.path.join(dirpath, fn)


def main():
    broken = []
    total = 0
    for path in md_files():
        text = open(path, encoding="utf-8").read()
        # strip fenced blocks and inline code so `dict[str, Any]](**args)`-style
        # snippets aren't misread as markdown links
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text = re.sub(r"`[^`\n]*`", "", text)
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            total += 1
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                broken.append(f"{os.path.relpath(path, ROOT)} -> {target}")
            elif os.path.isdir(resolved) and os.path.basename(path) not in ROOT_FILES:
                # directory links render on GitHub's repo view but 404 on the
                # deployed site (no index.html is generated for bare folders)
                broken.append(f"{os.path.relpath(path, ROOT)} -> {target} (directory link; point at a file)")
    if broken:
        print(f"BROKEN LINKS ({len(broken)}):")
        for b in broken:
            print(" ", b)
        sys.exit(1)
    print(f"ok — {total} relative links verified across the curriculum")


if __name__ == "__main__":
    main()
