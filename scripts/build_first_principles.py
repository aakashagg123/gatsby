#!/usr/bin/env python3
"""Build the standalone "First Principles & the Polymath Mind" track.

A separate top-level course (sibling to the AI Engineering and Harness Engineering
tracks), rendered as a small multi-page site: an overview/landing page plus one page
per lesson and a recap page. Reuses the shared warm CSS and markdown helpers from
build_html.py so the aesthetic matches the rest of the site.

Source of truth is the markdown in first-principles/. Run:
    python3 scripts/build_first_principles.py
"""
import os
import re
import html as htmllib
import markdown

import build_html as bh  # reuse CSS + markdown helpers (import-safe: main() is guarded)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "first-principles")
OUT = os.path.join(ROOT, "first-principles-html")

BRAND = "First principles"
TITLE = "First principles & the polymath mind"
LEDE = "Reasoning from fundamentals — and building range across every discipline."

# lesson slug order (titles are read from each file's H1)
LESSONS = [
    "what-is-first-principles",
    "the-method",
    "mental-models-latticework",
    "becoming-a-polymath",
    "learning-how-to-learn",
    "traps-and-limits",
]

# ---- link rewriting -----------------------------------------------------------
# Source links are written relative to the lesson's old home in content/07-*.
# Map them into the standalone track (and cross-link to the AI engineering track,
# which lives at ../ai/ in the combined site).
def rewrite_target(target):
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return target
    anchor = ""
    if "#" in target:
        target, anchor = target.split("#", 1)
        anchor = "#" + anchor
    # curriculum index / summary -> top landing
    if target.endswith(("SUMMARY.md", "GLOSSARY.md")):
        return "../index.html"
    # same-track overview
    if target in ("./README.md", "README.md"):
        return "index.html" + anchor
    # same-track lesson: ./slug.md
    m = re.match(r"\./([\w-]+)\.md$", target)
    if m:
        return f"{m.group(1)}.html{anchor}"
    # cross-track link into the AI engineering modules: ../NN-name/file.md
    m = re.match(r"\.\./(\d\d-[\w-]+)/(.+)$", target)
    if m:
        mod, fname = m.group(1), m.group(2)
        if fname == "README.md":
            return f"../ai/{mod}.html{anchor}"
        lesson = fname[:-3] if fname.endswith(".md") else fname
        # AI engineering renders each lesson as an anchor on its module page
        return f"../ai/{mod}.html#{lesson}"
    return target + anchor

def rewrite_links(md):
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: f"[{m.group(1)}]({rewrite_target(m.group(2).strip())})", md)

# ---- markdown -> html fragment ------------------------------------------------
def convert(md):
    lines = [l for l in md.split("\n") if not l.strip().startswith("*Part of ")]
    md = "\n".join(lines)
    md = rewrite_links(md)
    md = re.sub(r"\A\s*#\s+.*\n", "", md, count=1)          # drop the H1
    # drop trailing nav arrows lines from README/recap
    md = "\n".join(l for l in md.split("\n")
                   if not l.strip().startswith(("←", "→ Next", "↩")))
    md = bh.ensure_blank_before_lists(md)
    body = markdown.markdown(
        md, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    body = re.sub(r"<blockquote>(.*?For the builder.*?)</blockquote>",
                  r'<blockquote class="pm-callout">\1</blockquote>', body, flags=re.DOTALL)
    body = re.sub(r"<li>\[ \]\s*", '<li class="task todo">', body)
    body = re.sub(r"<li>\[x\]\s*", '<li class="task done">', body)
    return body

def title_of(path):
    with open(path) as f:
        return bh.lesson_title(f.read())

# ---- page chrome --------------------------------------------------------------
def head(title):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{htmllib.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{bh.CSS}</style>
</head>
<body>"""

def topbar():
    return f"""<header class="topbar">
  <a class="brand" href="index.html">{bh.SPARK}<span>{htmllib.escape(BRAND)}</span><em>a standalone module</em></a>
  <nav class="topnav"><a href="../index.html">← All courses</a></nav>
</header>"""

def sidebar(active, nav):
    """active: 'index' | slug | 'recap'.  nav: list of (href, label, key)."""
    items = []
    for href, label, key in nav:
        cls = "modlink active" if key == active else "modlink"
        items.append(f'<a class="{cls}" href="{href}">{htmllib.escape(label)}</a>')
    return f'<aside class="sidebar"><div class="sticky">{"".join(items)}</div></aside>'

def nav_items(lesson_titles):
    nav = [("index.html", "Overview", "index")]
    for i, (slug, t) in enumerate(lesson_titles, 1):
        nav.append((f"{slug}.html", f"{i} · {t}", slug))
    nav.append(("recap.html", "Recap & examples", "recap"))
    return nav

def footer(prev, nxt):
    def card(item, dir_):
        if not item:
            return "<span></span>"
        href, label = item
        arrow = "←" if dir_ == "prev" else "→"
        lbl = "Previous" if dir_ == "prev" else "Next"
        return (f'<a class="navcard {dir_}" href="{href}">'
                f'<span class="lbl">{arrow} {lbl}</span>'
                f'<span class="ttl">{htmllib.escape(label)}</span></a>')
    return (f'<div class="pagenav">{card(prev,"prev")}{card(nxt,"next")}</div>'
            '<footer class="foot">A standalone module · part of the '
            '<a href="../index.html">learning modules</a> collection.</footer>')

# ---- build --------------------------------------------------------------------
def build():
    os.makedirs(OUT, exist_ok=True)
    lesson_titles = [(slug, title_of(os.path.join(SRC, f"{slug}.md"))) for slug in LESSONS]
    nav = nav_items(lesson_titles)

    # a linear order of (key, href, label) for prev/next across overview→lessons→recap
    order = [("index", "index.html", "Overview")]
    order += [(slug, f"{slug}.html", t) for slug, t in lesson_titles]
    order += [("recap", "recap.html", "Recap & examples")]

    def prevnext(key):
        idx = [o[0] for o in order].index(key)
        prev = (order[idx-1][1], order[idx-1][2]) if idx > 0 else None
        nxt = (order[idx+1][1], order[idx+1][2]) if idx < len(order)-1 else None
        return prev, nxt

    # --- overview / landing (index.html) ---
    with open(os.path.join(SRC, "README.md")) as f:
        intro_html = convert(f.read())
    cards = []
    for i, (slug, t) in enumerate(lesson_titles, 1):
        cards.append(
            f'<a class="card" href="{slug}.html"><span class="card-num">{i:02d}</span>'
            f'<h3>{htmllib.escape(t)}</h3><span class="card-go">Read lesson →</span></a>')
    cards.append(
        '<a class="card" href="recap.html"><span class="card-num">📌</span>'
        '<h3>Recap &amp; real-world examples</h3><span class="card-go">Read recap →</span></a>')

    page = head(f"{TITLE}")
    page += topbar()
    page += f"""<main class="content index" id="top">
  <div class="index-hero">
    <span class="chip">A standalone module</span>
    <h1>{htmllib.escape(TITLE)}</h1>
    <p class="lede">{htmllib.escape(LEDE)}</p>
    <div class="index-meta"><span>6 lessons</span><span>+ recap</span>
      <span>first-principles</span><span>polymath</span></div>
  </div>
  <div class="intro">{intro_html}</div>
  <h2 class="sec">The lessons</h2>
  <div class="cards">{''.join(cards)}</div>
  <footer class="foot">Educational content. Use it, fork it, teach from it.</footer>
  </main></body></html>"""
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(page)

    # --- one page per lesson + recap ---
    pages = [(slug, os.path.join(SRC, f"{slug}.md"), i)
             for i, slug in enumerate(LESSONS, 1)]
    pages.append(("recap", os.path.join(SRC, "recap.md"), None))

    for key, path, num in pages:
        with open(path) as f:
            raw = f.read()
        t = bh.lesson_title(raw)
        body = convert(raw)
        prev, nxt = prevnext(key)
        chip = f"Lesson {num:02d}" if num else "Recap"
        page = head(f"{t} — {BRAND}")
        page += topbar()
        page += '<div class="layout">'
        page += sidebar(key, nav)
        page += f"""<main class="content" id="top">
  <div class="hero">
    <span class="chip">{chip}</span>
    <h1>{htmllib.escape(t)}</h1>
  </div>
  {body}
  {footer(prev, nxt)}
  </main></div></body></html>"""
        with open(os.path.join(OUT, f"{key}.html"), "w") as f:
            f.write(page)

    print(f"Built {len(LESSONS)} lesson pages + recap + index.html into {OUT}/")

if __name__ == "__main__":
    build()
