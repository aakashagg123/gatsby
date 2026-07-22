#!/usr/bin/env python3
"""Generic builder for a standalone, multi-page learning track.

A standalone track is a top-level course (sibling to the AI Engineering and Harness
Engineering tracks) rendered as an overview/landing page plus one page per lesson and a
recap page. It reuses the shared warm CSS and markdown helpers from build_html.py so the
aesthetic matches the rest of the site.

Both the First Principles and Product Sense tracks are thin config wrappers around
build_track(cfg). A cfg dict looks like:

    {
      "src": "<abs path to markdown source dir>",
      "out": "<abs path to output html dir>",
      "brand": "First principles",
      "tagline": "a standalone module",
      "title": "First principles & the polymath mind",
      "lede": "Reasoning from fundamentals — and building range across every discipline.",
      "meta": ["6 lessons", "+ recap", "first-principles", "polymath"],
      "callout": "For the builder",   # marker phrase that tags the styled briefing box
      "lessons": ["slug-1", "slug-2", ...],
    }
"""
import os
import re
import html as htmllib
import markdown

import reader_widget
import build_html as bh  # reuse CSS + markdown helpers (import-safe: main() is guarded)

# ---- mermaid (rendered client-side, matching the harness track) ---------------
# Diagrams render inside a soft card; the SVG scales down to the column when it is
# close to fitting, and the card scrolls horizontally when the diagram is genuinely
# wide — either way nothing ever bleeds outside the content column.
MERMAID_CSS = (
    "pre.mermaid{background:linear-gradient(180deg,#fdfcf9,#faf8f2);"
    "border:1px solid #e7e3d8;border-radius:14px;padding:26px 20px;margin:26px 0;"
    "text-align:center;overflow-x:auto;box-shadow:0 1px 3px rgba(26,25,21,.05)}"
    "pre.mermaid svg{max-width:100%;height:auto;display:inline-block}"
    ".mm-hint{position:sticky;left:8px;display:block;width:max-content;"
    "font-size:11px;color:#8a8778;background:#f4f2ea;border:1px solid #e4e0d5;"
    "border-radius:20px;padding:2px 10px;margin:0 0 8px;text-align:left}"
)
MERMAID_SCRIPT = """<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({startOnLoad:false, theme:'base', securityLevel:'loose',
  themeVariables:{
    background:'#faf9f5',
    primaryColor:'#fbefe9', primaryTextColor:'#1f1e1d', primaryBorderColor:'#e0b29e',
    secondaryColor:'#f4f2ea', secondaryBorderColor:'#ddd8ca', secondaryTextColor:'#1f1e1d',
    tertiaryColor:'#ffffff', tertiaryBorderColor:'#e4e0d5', tertiaryTextColor:'#1f1e1d',
    lineColor:'#a89f8d', textColor:'#3d3c37', nodeTextColor:'#1f1e1d',
    clusterBkg:'#f6f4ed', clusterBorder:'#e0dccd',
    edgeLabelBackground:'#faf9f5',
    actorBkg:'#fbefe9', actorBorder:'#d97757', actorTextColor:'#1f1e1d',
    actorLineColor:'#c9c4b4', signalColor:'#57564f', signalTextColor:'#3d3c37',
    labelBoxBkgColor:'#f4f2ea', labelBoxBorderColor:'#e0dccd',
    noteBkgColor:'#f9f1dd', noteBorderColor:'#e5d9b8',
    activationBkgColor:'#f4f2ea', activationBorderColor:'#d97757',
    quadrant1Fill:'#fbefe9', quadrant2Fill:'#f6f4ed', quadrant3Fill:'#f4f2ea',
    quadrant4Fill:'#fdf3ec', quadrantPointFill:'#bd5d3a', quadrantPointTextFill:'#1f1e1d',
    quadrantXAxisTextFill:'#6b6a64', quadrantYAxisTextFill:'#6b6a64',
    quadrantTitleFill:'#1f1e1d',
    quadrantInternalBorderStrokeFill:'#e4e0d5', quadrantExternalBorderStrokeFill:'#e0dccd',
    fontFamily:'Inter, system-ui, sans-serif', fontSize:'14.5px'},
  flowchart:{useMaxWidth:false, htmlLabels:true, curve:'basis',
    nodeSpacing:36, rankSpacing:46, diagramPadding:12},
  sequence:{useMaxWidth:false, mirrorActors:false, actorMargin:56, messageMargin:34},
  quadrantChart:{useMaxWidth:false, chartWidth:640, chartHeight:440,
    quadrantLabelFontSize:13, pointLabelFontSize:12, pointRadius:4, titleFontSize:16},
  themeCSS:'.node rect{rx:9;ry:9} .cluster rect{rx:12;ry:12} '+
    '.edgeLabel{border-radius:6px;padding:1px 5px} .label{font-weight:500} '+
    '.cluster-label .nodeLabel{font-weight:600;letter-spacing:.02em}'
});
await mermaid.run({querySelector:'pre.mermaid'});
// fit-or-scroll: genuinely wide diagrams keep natural size and scroll in the card
document.querySelectorAll('pre.mermaid svg').forEach(s=>{
  const w=(s.viewBox&&s.viewBox.baseVal&&s.viewBox.baseVal.width)||0;
  const cw=s.parentElement.clientWidth||0;
  if(cw&&w>cw*1.6){s.style.maxWidth='none';
    const h=document.createElement('span');h.className='mm-hint';
    h.textContent='\u27f7 scroll';s.parentElement.insertBefore(h,s);}
});
</script>"""


# ---- hand-built diagram overrides ---------------------------------------------
# The markdown keeps its ```mermaid fences (so GitHub renders them), but if a
# hand-crafted HTML figure exists at diagrams/<track>/<page-key>-<n>.html it
# replaces the n-th mermaid block of that page in the HTML edition.
def apply_diagram_overrides(body, src, key):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ddir = os.path.join(root, "diagrams", os.path.basename(src))
    if not os.path.isdir(ddir):
        return body
    idx = [-1]
    def _repl(m):
        idx[0] += 1
        p = os.path.join(ddir, f"{key}-{idx[0]}.html")
        if os.path.exists(p):
            with open(p) as f:
                return f.read()
        return m.group(0)
    return re.sub(r'<pre class="mermaid">.*?</pre>', _repl, body, flags=re.DOTALL)

def _inject_mermaid(page):
    """Add the mermaid runtime before </body> on pages that contain a diagram."""
    if 'class="mermaid"' in page:
        return page.replace("</body>", MERMAID_SCRIPT + "</body>")
    return page

# ---- link rewriting -----------------------------------------------------------
# Source links are written relative to a lesson's folder. Map them into the standalone
# track, and cross-link into the AI engineering track (which lives at ../ai/ in the
# combined site).
def rewrite_target(target):
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return target
    anchor = ""
    if "#" in target:
        target, anchor = target.split("#", 1)
        anchor = "#" + anchor
    if target.endswith(("SUMMARY.md", "GLOSSARY.md")):
        return "../index.html"
    if target in ("./README.md", "README.md"):
        return "index.html" + anchor
    m = re.match(r"\./([\w-]+)\.md$", target)
    if m:
        return f"{m.group(1)}.html{anchor}"
    # cross-track link into the AI engineering modules: ../NN-name/file.md
    # (also accepts the on-disk form ../content/NN-name/file.md)
    m = re.match(r"\.\./(?:content/)?(\d\d-[\w-]+)/(.+)$", target)
    if m:
        mod, fname = m.group(1), m.group(2)
        if fname == "README.md":
            return f"../ai/{mod}.html{anchor}"
        lesson = fname[:-3] if fname.endswith(".md") else fname
        return f"../ai/{mod}.html#{lesson}"
    # cross-link into a sibling standalone track: ../track-name/lesson.md
    m = re.match(r"\.\./([\w-]+)/([\w-]+)\.md$", target)
    if m:
        track, fname = m.group(1), m.group(2)
        page = "index" if fname == "README" else fname
        return f"../{track}/{page}.html{anchor}"
    return target + anchor

def rewrite_links(md):
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: f"[{m.group(1)}]({rewrite_target(m.group(2).strip())})", md)

# ---- markdown -> html fragment ------------------------------------------------
def convert(md, callout):
    lines = [l for l in md.split("\n") if not l.strip().startswith("*Part of ")]
    md = "\n".join(lines)
    md = rewrite_links(md)
    md = re.sub(r"\A\s*#\s+.*\n", "", md, count=1)          # drop the H1
    md = "\n".join(l for l in md.split("\n")
                   if not l.strip().startswith(("←", "→ Next", "↩")))
    md = bh.ensure_blank_before_lists(md)
    # stash ```mermaid fences so markdown doesn't render them as plain code
    mermaids = []
    def _stash(m):
        mermaids.append(m.group(1))
        return f"\n\nMERMAIDBLOCK{len(mermaids)-1}ENDBLOCK\n\n"
    md = re.sub(r"```mermaid[ \t]*\n(.*?)```", _stash, md, flags=re.DOTALL)
    body = markdown.markdown(
        md, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    body = re.sub(rf"<blockquote>(.*?{re.escape(callout)}.*?)</blockquote>",
                  r'<blockquote class="pm-callout">\1</blockquote>', body, flags=re.DOTALL)
    body = re.sub(r"<li>\[ \]\s*", '<li class="task todo">', body)
    body = re.sub(r"<li>\[x\]\s*", '<li class="task done">', body)
    for i, code in enumerate(mermaids):
        token = f"MERMAIDBLOCK{i}ENDBLOCK"
        pre = f'<pre class="mermaid">{htmllib.escape(code.rstrip())}</pre>'
        body = body.replace(f"<p>{token}</p>", pre).replace(token, pre)
    return body

# ---- page chrome --------------------------------------------------------------
def _head(title):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{htmllib.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{bh.CSS}{MERMAID_CSS}</style>
</head>
<body>"""

def _topbar(brand, tagline):
    return f"""<header class="topbar">
  <a class="brand" href="index.html">{bh.SPARK}<span>{htmllib.escape(brand)}</span><em>{htmllib.escape(tagline)}</em></a>
  <nav class="topnav"><a href="../index.html">← All courses</a></nav>
</header>"""

def _sidebar(active, nav):
    items = []
    for href, label, key in nav:
        cls = "modlink active" if key == active else "modlink"
        items.append(f'<a class="{cls}" href="{href}">{htmllib.escape(label)}</a>')
    return f'<aside class="sidebar"><div class="sticky">{"".join(items)}</div></aside>'

def _footer(prev, nxt):
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
def build_track(cfg):
    src, out = cfg["src"], cfg["out"]
    brand, tagline = cfg["brand"], cfg.get("tagline", "a standalone module")
    title, lede, callout = cfg["title"], cfg["lede"], cfg["callout"]
    lessons = cfg["lessons"]
    os.makedirs(out, exist_ok=True)

    def title_of(path):
        with open(path) as f:
            return bh.lesson_title(f.read())

    lesson_titles = [(slug, title_of(os.path.join(src, f"{slug}.md"))) for slug in lessons]

    nav = [("index.html", "Overview", "index")]
    for i, (slug, t) in enumerate(lesson_titles, 1):
        nav.append((f"{slug}.html", f"{i} · {t}", slug))
    nav.append(("recap.html", "Recap & examples", "recap"))

    order = [("index", "index.html", "Overview")]
    order += [(slug, f"{slug}.html", t) for slug, t in lesson_titles]
    order += [("recap", "recap.html", "Recap & examples")]

    def prevnext(key):
        idx = [o[0] for o in order].index(key)
        prev = (order[idx-1][1], order[idx-1][2]) if idx > 0 else None
        nxt = (order[idx+1][1], order[idx+1][2]) if idx < len(order)-1 else None
        return prev, nxt

    # --- overview / landing (index.html) ---
    with open(os.path.join(src, "README.md")) as f:
        intro_html = apply_diagram_overrides(convert(f.read(), callout), src, "index")
    cards = []
    for i, (slug, t) in enumerate(lesson_titles, 1):
        cards.append(
            f'<a class="card" href="{slug}.html"><span class="card-num">{i:02d}</span>'
            f'<h3>{htmllib.escape(t)}</h3><span class="card-go">Read lesson →</span></a>')
    cards.append(
        '<a class="card" href="recap.html"><span class="card-num">📌</span>'
        '<h3>Recap &amp; real-world examples</h3><span class="card-go">Read recap →</span></a>')
    meta = "".join(f"<span>{htmllib.escape(m)}</span>" for m in cfg["meta"])

    page = _head(title)
    page += _topbar(brand, tagline)
    page += f"""<main class="content index" id="top">
  <div class="index-hero">
    <span class="chip">A standalone module</span>
    <h1>{htmllib.escape(title)}</h1>
    <p class="lede">{htmllib.escape(lede)}</p>
    <div class="index-meta">{meta}</div>
  </div>
  <div class="intro">{intro_html}</div>
  <h2 class="sec">The lessons</h2>
  <div class="cards">{''.join(cards)}</div>
  <footer class="foot">Educational content. Use it, fork it, teach from it.</footer>
  </main></body></html>"""
    with open(os.path.join(out, "index.html"), "w") as f:
        f.write(reader_widget.inject(_inject_mermaid(page)))

    # --- one page per lesson + recap ---
    pages = [(slug, os.path.join(src, f"{slug}.md"), i)
             for i, slug in enumerate(lessons, 1)]
    pages.append(("recap", os.path.join(src, "recap.md"), None))

    for key, path, num in pages:
        with open(path) as f:
            raw = f.read()
        t = bh.lesson_title(raw)
        body = apply_diagram_overrides(convert(raw, callout), src, key)
        prev, nxt = prevnext(key)
        chip = f"Lesson {num:02d}" if num else "Recap"
        page = _head(f"{t} — {brand}")
        page += _topbar(brand, tagline)
        page += '<div class="layout">'
        page += _sidebar(key, nav)
        page += f"""<main class="content" id="top">
  <div class="hero">
    <span class="chip">{chip}</span>
    <h1>{htmllib.escape(t)}</h1>
  </div>
  {body}
  {_footer(prev, nxt)}
  </main></div></body></html>"""
        with open(os.path.join(out, f"{key}.html"), "w") as f:
            f.write(reader_widget.inject(_inject_mermaid(page)))

    print(f"Built {len(lessons)} lesson pages + recap + index.html into {out}/")
