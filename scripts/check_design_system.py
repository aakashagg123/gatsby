#!/usr/bin/env python3
"""Lint: the site must use Apps SDK UI tokens, not literal design values.

Checks, exit 1 on any hit:
  1. design-system/site/*.css and diagrams/**/*.html contain no literal colour
     (hex, rgb(), rgba(), hsl(), named). HTML comments are ignored.
  2. Page templates (scripts/*.py, scripts/graph_page.html) contain no hex colour. The graph's
     per-track data colours live in build_graph.py and are exempt.
  3. No legacy variables (--bg, --ink, --accent, --line, --mut, --panel) are referenced.
  4. design-system/site/*.css sets no font-size in px or rem. Use --font-* tokens.
  5. The vendored SDK files match design-system/vendor/apps-sdk-ui/CHECKSUMS.

Run: python3 scripts/check_design_system.py
"""
import glob
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEX = re.compile(r"#[0-9A-Fa-f]{3}\b|#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{8}\b")
FUNC = re.compile(r"\b(?:rgba?|hsla?)\((?!\s*var\()")
NAMED = re.compile(r"[A-Za-z-]+\s*:\s*(?:[^;{}\"']*\s)?(white|black|red|green|blue|gray|grey|orange|purple|yellow)\s*(?=[;}\"'])")
LEGACY = re.compile(r"var\(--(?:bg|bg2|ink|ink2|accent|accent-d|accent-soft|line|line2|mut|panel|muted|surface|soft)\b")
FONT_PX = re.compile(r"font-size\s*:\s*[\d.]+\s*(?:px|rem)\b")
EXEMPT_SCRIPTS = {"build_graph.py", "tokenize_colors.py", "check_design_system.py", "gen_learning_paths.py"}

problems = []


def rel(p):
    return os.path.relpath(p, ROOT)


def strip_comments(text, kind):
    if kind == "css":
        return re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def scan(path, kind, color_checks=True, font_check=False, legacy=True):
    text = strip_comments(open(path, encoding="utf-8").read(), "css" if kind == "css" else "html")
    for no, line in enumerate(text.split("\n"), 1):
        if color_checks:
            for rx, what in ((HEX, "hex colour"), (FUNC, "rgb/hsl colour"), (NAMED, "named colour")):
                for m in rx.finditer(line):
                    problems.append(f"{rel(path)}:{no}: {what} {m.group(0)!r}")
        if legacy and LEGACY.search(line):
            problems.append(f"{rel(path)}:{no}: legacy variable {LEGACY.search(line).group(0)!r}")
        if font_check and FONT_PX.search(line):
            problems.append(f"{rel(path)}:{no}: font-size literal; use a --font-* token")


for p in sorted(glob.glob(os.path.join(ROOT, "design-system", "site", "*.css"))):
    scan(p, "css", font_check=True)
for p in sorted(glob.glob(os.path.join(ROOT, "diagrams", "**", "*.html"), recursive=True)):
    scan(p, "html")
for p in sorted(glob.glob(os.path.join(ROOT, "scripts", "*.py"))):
    if os.path.basename(p) in EXEMPT_SCRIPTS:
        continue
    scan(p, "html", color_checks=False)
    text = open(p, encoding="utf-8").read()
    for no, line in enumerate(text.split("\n"), 1):
        if HEX.search(line) and "color" in line.lower() and "https://" not in line:
            problems.append(f"{rel(p)}:{no}: hex colour {HEX.search(line).group(0)!r}")
scan(os.path.join(ROOT, "scripts", "graph_page.html"), "html", color_checks=False)

sums = os.path.join(ROOT, "design-system", "vendor", "apps-sdk-ui", "CHECKSUMS")
if os.path.exists(sums):
    for line in open(sums):
        digest, name = line.split(None, 1)
        path = os.path.join(ROOT, "design-system", "vendor", "apps-sdk-ui", name.strip())
        if not os.path.exists(path) or hashlib.sha256(open(path, "rb").read()).hexdigest() != digest:
            problems.append(f"vendor drift: {name.strip()} differs from CHECKSUMS (vendored files are read-only)")
else:
    problems.append("design-system/vendor/apps-sdk-ui/CHECKSUMS is missing")

if problems:
    print("\n".join(problems[:80]))
    print(f"\n{len(problems)} problem(s). Use SDK tokens (see design-system/README.md).")
    sys.exit(1)
print("ok — site CSS, diagrams and templates use design-system tokens only")
