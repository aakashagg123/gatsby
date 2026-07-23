#!/usr/bin/env python3
"""Assemble the combined GitHub Pages site with separate top-level tracks.

  _site/
  ├── index.html         top landing → AI engineering | Harness engineering |
  │                                    First principles | Product sense
  ├── ai/                the AI engineering module (pre-rendered html/ editions)
  ├── first-principles/  the first principles module (pre-rendered)
  ├── product-sense/     the product sense module (pre-rendered)
  └── harness/           the harness engineering track (markdown rendered client-side)

The harness track is rendered at runtime with marked + mermaid (so GFM tables and
Mermaid diagrams render). This build step is pure stdlib — copy files and write a
viewer per markdown doc — so it never fails on a missing dependency.

Run:  python3 scripts/build_site.py
"""
import os
import shutil
import reader_widget

import build_graph
import build_glossary
import glossary_widget

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "_site")
HTML = os.path.join(ROOT, "html")                       # AI engineering editions
FP_HTML = os.path.join(ROOT, "first-principles-html")   # first principles editions
PS_HTML = os.path.join(ROOT, "product-sense-html")      # product sense editions
TPS_HTML = os.path.join(ROOT, "technical-product-sense-html")  # technical product sense
TPM_HTML = os.path.join(ROOT, "technical-product-management-html")  # technical product management
AAI_HTML = os.path.join(ROOT, "agentic-ai-html")        # agentic AI
KG_HTML = os.path.join(ROOT, "knowledge-graphs-html")   # knowledge graphs
# Markdown tracks rendered client-side, all sharing the phases/ folder shape:
# (source dir, site subdir, brand label shown in the viewer chrome)
MD_TRACKS = [
    ("harness-engineering", "harness", "Harness engineering"),
    ("flowable", "flowable", "Flowable"),
]

VIEWER = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {brand}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{{
    --bg:#faf9f5;--surface:#ffffff;--ink:#181818;--muted:#6c6a60;
    --accent:#d97757;--accent-deep:#bd5d3a;--line:#e8e6dd;--code-bg:#1c1b18;--soft:#f2f0e9;
  }}
  *{{box-sizing:border-box}}
  html{{-webkit-text-size-adjust:100%;text-size-adjust:100%}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font-family:Inter,system-ui,-apple-system,sans-serif;font-size:16px;line-height:1.7;
    -webkit-font-smoothing:antialiased;letter-spacing:-0.005em;overflow-x:hidden}}
  img,svg{{max-width:100%;height:auto}}
  .top{{position:sticky;top:0;z-index:10;background:rgba(250,249,245,.85);backdrop-filter:blur(10px);
    border-bottom:1px solid var(--line);padding:14px 24px;display:flex;align-items:center;gap:20px;font-size:.9rem}}
  .top a{{color:var(--ink);text-decoration:none;font-weight:500}}
  .top a:hover{{color:var(--accent-deep)}}
  .top .brand{{color:var(--accent-deep);font-weight:600}}
  main{{max-width:760px;margin:0 auto;padding:48px 24px 64px}}
  h1,h2,h3,h4{{line-height:1.2;letter-spacing:-0.02em;font-weight:600}}
  h1{{font-size:2.4rem;margin:0 0 .6em}}
  h2{{font-size:1.55rem;margin-top:2.2em;padding-bottom:.35em;border-bottom:1px solid var(--line)}}
  h3{{font-size:1.2rem;margin-top:1.8em}}
  a{{color:var(--accent-deep);text-decoration:none;text-underline-offset:3px}}
  a:hover{{text-decoration:underline}}
  p,li{{letter-spacing:-0.003em}}
  code{{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;background:var(--soft);
    padding:.12em .4em;border-radius:5px;font-size:.86em}}
  pre{{background:var(--code-bg);color:#f1efe8;padding:18px 20px;border-radius:12px;overflow:auto;
    font-size:.86em;line-height:1.6}}
  pre code{{background:none;color:inherit;padding:0;font-size:1em}}
  pre.mermaid{{background:linear-gradient(180deg,#fdfcf9,#faf8f2);color:var(--ink);
    border:1px solid #e7e3d8;border-radius:14px;padding:26px 20px;margin:26px 0;
    text-align:center;overflow-x:auto;box-shadow:0 1px 3px rgba(26,25,21,.05)}}
  pre.mermaid svg{{max-width:100%;height:auto;display:inline-block}}
  .mm-hint{{position:sticky;left:8px;display:block;width:max-content;
    font-size:11px;color:#8a8778;background:#f4f2ea;border:1px solid #e4e0d5;
    border-radius:20px;padding:2px 10px;margin:0 0 8px;text-align:left}}
  table{{border-collapse:collapse;width:100%;margin:1.4em 0;font-size:.92em}}
  th,td{{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}}
  th{{background:var(--soft);font-weight:600}}
  tr:nth-child(even) td{{background:rgba(242,240,233,.4)}}
  blockquote{{border-left:3px solid var(--accent);margin:1.4em 0;padding:.5em 1.2em;
    color:var(--muted);background:var(--soft);border-radius:0 8px 8px 0}}
  blockquote p{{margin:.3em 0}}
  details{{background:var(--surface);border:1px solid var(--line);border-radius:12px;
    padding:12px 18px;margin:.8em 0}}
  details[open]{{box-shadow:0 1px 3px rgba(0,0,0,.04)}}
  summary{{cursor:pointer;font-weight:600;color:var(--accent-deep)}}
  hr{{border:none;border-top:1px solid var(--line);margin:2.4em 0}}
  ::selection{{background:rgba(217,119,87,.22)}}
  .lessonnav{{max-width:760px;margin:8px auto 64px;padding:24px;
    display:flex;gap:14px;flex-wrap:wrap}}
  .lessonnav a{{flex:1;min-width:0;background:var(--surface);border:1px solid var(--line);
    border-radius:12px;padding:14px 16px;font-size:.92rem;font-weight:500;color:var(--ink);
    transition:border-color .15s,transform .15s,box-shadow .15s}}
  .lessonnav a:hover{{border-color:var(--accent);transform:translateY(-2px);
    box-shadow:0 6px 20px rgba(217,119,87,.1);text-decoration:none}}
  .lessonnav .up{{flex:0 0 auto;text-align:center}}
  .lessonnav .nx{{text-align:right}}
  .lessonnav .lbl{{display:block;color:var(--muted);font-size:.72rem;font-weight:600;
    text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px}}
  /* phone-first: high readability on iPhone-class widths */
  @media (max-width:600px){{
    body{{font-size:16.5px;line-height:1.72}}
    .top{{padding:12px 16px;gap:14px;font-size:.86rem}}
    main{{padding:28px 18px 48px}}
    h1{{font-size:1.85rem;line-height:1.18}}
    h2{{font-size:1.32rem;margin-top:1.8em}}
    h3{{font-size:1.12rem}}
    pre{{padding:14px 14px;font-size:.82em;border-radius:10px}}
    code{{word-break:break-word}}
    /* wide tables scroll instead of breaking the page */
    main table{{display:block;width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;
      white-space:nowrap;font-size:.86em}}
    blockquote{{margin:1.1em 0;padding:.5em 1em}}
    .lessonnav{{flex-direction:column;gap:10px;margin:4px auto 48px;padding:20px 18px}}
    .lessonnav a{{width:100%}}
    .lessonnav .up{{order:3}}
    .lessonnav .nx{{text-align:left}}
  }}
</style></head><body>
<div class="top"><a href="{root}index.html">← All courses</a><a class="brand" href="{track_root}index.html">{brand}</a></div>
<main id="content">Loading…</main>
{nav}
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({{startOnLoad:false, theme:'base', securityLevel:'loose',
  themeVariables:{{
    background:'#faf9f5',
    primaryColor:'#fbefe9', primaryTextColor:'#1f1e1d', primaryBorderColor:'#e0b29e',
    secondaryColor:'#f4f2ea', secondaryBorderColor:'#ddd8ca', secondaryTextColor:'#1f1e1d',
    tertiaryColor:'#ffffff', tertiaryBorderColor:'#e4e0d5', tertiaryTextColor:'#1f1e1d',
    lineColor:'#a89f8d', textColor:'#3d3c37', nodeTextColor:'#1f1e1d',
    clusterBkg:'#f6f4ed', clusterBorder:'#e0dccd', edgeLabelBackground:'#faf9f5',
    actorBkg:'#fbefe9', actorBorder:'#d97757', actorTextColor:'#1f1e1d',
    actorLineColor:'#c9c4b4', signalColor:'#57564f', signalTextColor:'#3d3c37',
    noteBkgColor:'#f9f1dd', noteBorderColor:'#e5d9b8',
    activationBkgColor:'#f4f2ea', activationBorderColor:'#d97757',
    fontFamily:'Inter, system-ui, sans-serif', fontSize:'14.5px'}},
  flowchart:{{useMaxWidth:false, htmlLabels:true, curve:'basis',
    nodeSpacing:36, rankSpacing:46, diagramPadding:12}},
  sequence:{{useMaxWidth:false, mirrorActors:false, actorMargin:56, messageMargin:34}},
  quadrantChart:{{useMaxWidth:false, chartWidth:640, chartHeight:440,
    quadrantLabelFontSize:13, pointLabelFontSize:12, pointRadius:4, titleFontSize:16}},
  themeCSS:'.node rect{{rx:9;ry:9}} .cluster rect{{rx:12;ry:12}} '+
    '.edgeLabel{{border-radius:6px;padding:1px 5px}} .label{{font-weight:500}} '+
    '.cluster-label .nodeLabel{{font-weight:600;letter-spacing:.02em}}'
}});
const md = await (await fetch('{md}')).text();
// protect mermaid fences so marked doesn't treat them as code
const blocks=[]; const stripped = md.replace(/```mermaid\\n([\\s\\S]*?)```/g,(m,c)=>{{
  blocks.push(c); return `<pre class="mermaid">__MERMAID_${{blocks.length-1}}__</pre>`;}});
let html = marked.parse(stripped);
html = html.replace(/__MERMAID_(\\d+)__/g,(m,i)=>blocks[+i]);
const el = document.getElementById('content'); el.innerHTML = html;
// rewrite intra-site .md links to their .html viewers. AI-engineering lessons
// deploy under ai/<module>.html#<lesson> (not content/), so remap those first.
el.querySelectorAll('a[href]').forEach(a=>{{
  let h=a.getAttribute('href');
  if(!h || /^https?:|^#/.test(h)) return;
  h = h.replace(/(^|\\/)content\\/(\\d\\d-[\\w-]+)\\/README\\.md/,'$1ai/$2.html')
       .replace(/(^|\\/)content\\/(\\d\\d-[\\w-]+)\\/([\\w-]+)\\.md/,'$1ai/$2.html#$3')
       .replace(/\\.md(#|$)/,'.html$1');
  a.setAttribute('href', h);
}});
await mermaid.run({{querySelector:'pre.mermaid'}});
document.querySelectorAll('pre.mermaid svg').forEach(s=>{{
  const w=(s.viewBox&&s.viewBox.baseVal&&s.viewBox.baseVal.width)||0;
  const cw=s.parentElement.clientWidth||0;
  if(cw&&w>cw*1.6){{s.style.maxWidth='none';
    const h=document.createElement('span');h.className='mm-hint';
    h.textContent='\u27f7 scroll';s.parentElement.insertBefore(h,s);}}
}});
</script></body></html>
"""

LANDING = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Engineering learning modules</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#faf9f5;--surface:#ffffff;--ink:#181818;--muted:#6c6a60;
    --accent:#d97757;--accent-deep:#bd5d3a;--line:#e8e6dd;--soft:#f2f0e9;
  }
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:Inter,system-ui,-apple-system,sans-serif;font-size:17px;line-height:1.7;
    -webkit-font-smoothing:antialiased;letter-spacing:-0.005em;overflow-x:hidden}
  .wrap{max-width:920px;margin:0 auto;padding:104px 24px 80px}
  .eyebrow{display:inline-block;font-size:.78rem;font-weight:600;letter-spacing:.08em;
    text-transform:uppercase;color:var(--accent-deep);margin-bottom:16px}
  h1{font-size:3.1rem;line-height:1.08;letter-spacing:-0.03em;font-weight:600;margin:0 0 .25em;max-width:14ch}
  p.sub{color:var(--muted);font-size:1.2rem;margin:0;max-width:54ch}
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:22px;margin-top:52px}
  @media(max-width:680px){
    .wrap{padding:64px 18px 64px}
    .cards{grid-template-columns:1fr;gap:16px;margin-top:36px}
    h1{font-size:2.2rem}
    p.sub{font-size:1.08rem}
    a.card{padding:24px;border-radius:16px}
  }
  a.card{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--surface);
    border:1px solid var(--line);border-radius:18px;padding:30px;
    transition:border-color .15s,transform .15s,box-shadow .15s}
  a.card:hover{border-color:var(--accent);transform:translateY(-3px);box-shadow:0 12px 32px rgba(217,119,87,.12)}
  a.card .tag{display:inline-block;font-size:.74rem;color:var(--accent-deep);font-weight:600;
    letter-spacing:.06em;text-transform:uppercase}
  a.card h2{margin:.5em 0 .35em;font-size:1.45rem;font-weight:600;letter-spacing:-0.02em}
  a.card p{color:var(--muted);margin:0;font-size:.98rem;line-height:1.6}
  footer{color:var(--muted);font-size:.85rem;margin-top:64px;border-top:1px solid var(--line);padding-top:24px}
  ::selection{background:rgba(217,119,87,.22)}
</style></head><body>
<div class="wrap">
  <span class="eyebrow">From scratch</span>
  <h1>Engineering learning modules</h1>
  <p class="sub">Nine separate, hands-on curricula — build each system from first principles, then use it for real.</p>
  <div class="cards">
    <a class="card" href="ai/index.html">
      <span class="tag">Module</span>
      <h2>AI engineering →</h2>
      <p>The engineering discipline under production LLM systems — inference, retrieval,
      evals, observability, safety, cost. Designed reading editions.</p>
    </a>
    <a class="card" href="harness/index.html">
      <span class="tag">Module</span>
      <h2>Harness engineering →</h2>
      <p>Build a coding agent's harness from scratch — loop, tools, context, memory,
      subagents — then use the real SDK. Build it / use it, ships an artifact each lesson.</p>
    </a>
    <a class="card" href="flowable/index.html">
      <span class="tag">Module</span>
      <h2>Flowable →</h2>
      <p>Process automation from scratch — build a token engine, wait states, and a job
      executor by hand, then run real BPMN on the Flowable engine. Concept-first for
      PMs, with a build layer for engineers.</p>
    </a>
    <a class="card" href="first-principles/index.html">
      <span class="tag">Module</span>
      <h2>First principles →</h2>
      <p>Reason from fundamentals and build range across disciplines — the method,
      a latticework of mental models, becoming a polymath, and learning how to learn.</p>
    </a>
    <a class="card" href="product-sense/index.html">
      <span class="tag">Module</span>
      <h2>Product sense →</h2>
      <p>The instinct for what makes a product succeed, for APMs & PMs moving into AI PM —
      motivation, empathy, creativity, communication, domain expertise, and product sense for AI.</p>
    </a>
    <a class="card" href="technical-product-sense/index.html">
      <span class="tag">Module</span>
      <h2>Technical product sense →</h2>
      <p>Read systems like an engineer — architecture, APIs, data, latency, reliability,
      and tech debt — with a diagram in every lesson. For APMs & PMs moving into AI PM.</p>
    </a>
    <a class="card" href="technical-product-management/index.html">
      <span class="tag">Module</span>
      <h2>Technical product management →</h2>
      <p>The operating discipline of shipping — the role, specs, prioritization, execution,
      metrics, and releases — with a diagram in every lesson. For APMs & PMs moving into AI PM.</p>
    </a>
    <a class="card" href="agentic-ai/index.html">
      <span class="tag">Module</span>
      <h2>Agentic AI →</h2>
      <p>What agents actually are — the loop, tools, memory, planning — plus reliability,
      security, and economics. Opens with a knowledge graph; a diagram in every lesson.</p>
    </a>
    <a class="card" href="knowledge-graphs/index.html">
      <span class="tag">Module</span>
      <h2>Knowledge graphs →</h2>
      <p>Treat what the company knows as a product — entities and ontologies, the
      construction pipeline, GraphRAG, governance, and the business case, in CPO language.</p>
    </a>
    <a class="card" href="graph/index.html" style="border-color:#d97757;background:linear-gradient(180deg,#fff,#fbefe9)">
      <span class="tag">Explore</span>
      <h2>Knowledge graph →</h2>
      <p>Every page across all nine modules as one interactive map — __NODES__ pages,
      __LINKS__ cross-references. Search it, filter by track, click any node to jump in.</p>
    </a>
  </div>
  <footer>Educational content. Use it, fork it, teach from it.</footer>
</div></body></html>
"""


GRAPH_BTN = (
    '<a href="{href}" title="Open the knowledge graph" aria-label="Open the knowledge graph" '
    'style="position:fixed;right:18px;bottom:18px;z-index:60;display:flex;align-items:center;'
    'justify-content:center;width:44px;height:44px;border-radius:50%;background:#ffffff;'
    'border:1px solid #e8e6dd;box-shadow:0 4px 16px rgba(26,25,21,.10);color:#bd5d3a">'
    '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" '
    'stroke-width="1.6"><circle cx="5" cy="5" r="2.4"/><circle cx="15" cy="7" r="2.4"/>'
    '<circle cx="9" cy="15" r="2.4"/><path d="M7.2 6l5.5.7M6 7.2l2.2 5.6M13.8 9l-3.4 4.2"/>'
    '</svg></a>'
)


def inject_graph_buttons(site, focus_map):
    """Add a floating 'open the knowledge graph' button to every content page."""
    injected = 0
    for dp, _, files in os.walk(site):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dp, fn)
            rel = os.path.relpath(path, site).replace(os.sep, "/")
            if rel in ("index.html", "graph/index.html"):
                continue
            with open(path, encoding="utf-8") as f:
                text = f.read()
            pos = text.rfind("</body>")
            if pos == -1 or 'aria-label="Open the knowledge graph"' in text:
                continue
            href = os.path.relpath("graph/index.html", os.path.dirname(rel) or ".")
            href = href.replace(os.sep, "/")
            key = focus_map.get(rel)
            if key:
                href += "?focus=" + key.replace("/", "%2F")
            btn = GRAPH_BTN.format(href=href)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text[:pos] + btn + text[pos:])
            injected += 1
    return injected


def inject_glossary(site):
    """Ship the glossary widget assets and reference them from every content
    page, with a per-page relative root so assets and lesson links resolve at
    any depth. Mirrors inject_graph_buttons (skips the two landing pages)."""
    assets = os.path.join(site, "assets")
    os.makedirs(assets, exist_ok=True)
    with open(os.path.join(assets, "glossary.css"), "w", encoding="utf-8") as f:
        f.write(glossary_widget.CSS)
    with open(os.path.join(assets, "glossary.js"), "w", encoding="utf-8") as f:
        f.write(glossary_widget.js_file(build_glossary.site_entries(),
                                        build_glossary.site_keyterms()))
    injected = 0
    for dp, _, files in os.walk(site):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dp, fn)
            rel = os.path.relpath(path, site).replace(os.sep, "/")
            if rel in ("index.html", "graph/index.html"):
                continue
            with open(path, encoding="utf-8") as f:
                text = f.read()
            pos = text.rfind("</body>")
            if pos == -1 or "window.__glossRoot" in text:
                continue
            root = os.path.relpath(site, os.path.dirname(path)).replace(os.sep, "/")
            root = "" if root == "." else root + "/"
            tags = glossary_widget.head_tags(root, rel)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text[:pos] + tags + text[pos:])
            injected += 1
    return injected


def rel_to_track_root(md_path, site_key):
    """'../' * depth from a track md file up to _site/<site_key>/."""
    rel = os.path.relpath(md_path, os.path.join(SITE, site_key))
    depth = rel.count(os.sep)
    return "../" * depth


def is_lesson(md_path):
    return md_path.replace(os.sep, "/").endswith("/docs/en.md") and "/phases/" in md_path.replace(os.sep, "/")


def lesson_order(dst_harness):
    """Ordered list of lesson en.md paths: by phase dir, then lesson dir."""
    lessons = []
    phases_dir = os.path.join(dst_harness, "phases")
    for phase in sorted(os.listdir(phases_dir)):
        pdir = os.path.join(phases_dir, phase)
        if not os.path.isdir(pdir):
            continue
        for lesson in sorted(os.listdir(pdir)):
            en = os.path.join(pdir, lesson, "docs", "en.md")
            if os.path.exists(en):
                lessons.append(en)
    return lessons


def _title_of(md_path):
    with open(md_path) as f:
        return f.readline().lstrip("# ").strip()


def nav_html(md_path, prev_md, next_md):
    """Prev / Up-to-phase / Next nav for a lesson page, links relative to its html."""
    here = md_path[:-3] + ".html"
    parts = []
    if prev_md:
        rel = os.path.relpath(prev_md[:-3] + ".html", os.path.dirname(here))
        parts.append(f'<a class="pv" href="{rel}"><span class="lbl">← Previous</span>{_title_of(prev_md)}</a>')
    # Up to the phase README
    up = os.path.relpath(os.path.join(os.path.dirname(md_path), "..", "..", "README.html"),
                         os.path.dirname(here))
    parts.append(f'<a class="up" href="{up}"><span class="lbl">Phase</span>Overview</a>')
    if next_md:
        rel = os.path.relpath(next_md[:-3] + ".html", os.path.dirname(here))
        parts.append(f'<a class="nx" href="{rel}"><span class="lbl">Next →</span>{_title_of(next_md)}</a>')
    return '<nav class="lessonnav">' + "".join(parts) + "</nav>"


def main():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE)

    # 1. AI engineering module: copy the pre-rendered editions.
    shutil.copytree(HTML, os.path.join(SITE, "ai"))

    # 1b. First principles module: copy its pre-rendered pages.
    if os.path.isdir(FP_HTML):
        shutil.copytree(FP_HTML, os.path.join(SITE, "first-principles"))

    # 1c. Product sense module: copy its pre-rendered pages.
    if os.path.isdir(PS_HTML):
        shutil.copytree(PS_HTML, os.path.join(SITE, "product-sense"))

    # 1d. Technical product sense module: copy its pre-rendered pages.
    if os.path.isdir(TPS_HTML):
        shutil.copytree(TPS_HTML, os.path.join(SITE, "technical-product-sense"))

    # 1e. Technical product management module: copy its pre-rendered pages.
    if os.path.isdir(TPM_HTML):
        shutil.copytree(TPM_HTML, os.path.join(SITE, "technical-product-management"))

    # 1f. Agentic AI module: copy its pre-rendered pages.
    if os.path.isdir(AAI_HTML):
        shutil.copytree(AAI_HTML, os.path.join(SITE, "agentic-ai"))

    # 1g. Knowledge graphs module: copy its pre-rendered pages.
    if os.path.isdir(KG_HTML):
        shutil.copytree(KG_HTML, os.path.join(SITE, "knowledge-graphs"))

    # 2. Markdown tracks (harness engineering, flowable): copy each tree
    # (md + code + outputs) and render a viewer next to every markdown file.
    pages = 0
    for src_dir, site_key, brand in MD_TRACKS:
        dst_track = os.path.join(SITE, site_key)
        shutil.copytree(os.path.join(ROOT, src_dir), dst_track)

        # 3. Lesson ordering for prev/next navigation.
        lessons = lesson_order(dst_track)
        prev_next = {}
        for i, md in enumerate(lessons):
            prev_next[md] = (lessons[i - 1] if i > 0 else None,
                             lessons[i + 1] if i < len(lessons) - 1 else None)

        # 4. Render a viewer next to every markdown file (sources stay browsable).
        for dp, _, files in os.walk(dst_track):
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                md_path = os.path.join(dp, fn)
                title = os.path.splitext(fn)[0]
                with open(md_path) as f:
                    first = f.readline().lstrip("# ").strip()
                title = first or title
                root = rel_to_track_root(md_path, site_key)   # up to _site/
                html_path = md_path[:-3] + ".html"
                md_url = "./" + fn
                nav = ""
                if is_lesson(md_path):
                    p, n = prev_next.get(md_path, (None, None))
                    nav = nav_html(md_path, p, n)
                with open(html_path, "w") as f:
                    f.write(reader_widget.inject(VIEWER.format(
                        title=title,
                        brand=brand,
                        md=md_url,
                        root="../" + root if root else "../",   # _site/ root
                        track_root=root or "./",
                        nav=nav,
                    )))
                pages += 1

        # Track landing = viewer for README.md.
        readme_html = os.path.join(dst_track, "README.html")
        if os.path.exists(readme_html):
            shutil.copyfile(readme_html, os.path.join(dst_track, "index.html"))

    # 5. Knowledge graph: extract nodes/edges from the markdown sources and
    # write the interactive graph page (Quartz-style).
    data = build_graph.graph_data()
    build_graph.write_graph_page(SITE, data)
    n_links = sum(1 for e in data["edges"] if e[3] == "link")

    # 6. Top landing (with live graph counts).
    landing = LANDING.replace("__NODES__", str(len(data["nodes"]))) \
                     .replace("__LINKS__", str(n_links))
    with open(os.path.join(SITE, "index.html"), "w") as f:
        f.write(landing)

    # 7. Every content page gets a floating button into the graph, focused on
    # that page's own node.
    injected = inject_graph_buttons(SITE, build_graph.page_focus_map(data))

    # 8. Clickable glossary terms + explainer sidebar on every content page.
    gloss = inject_glossary(SITE)

    print(f"built _site/ — ai module + md tracks ({pages} pages) + landing + "
          f"graph ({len(data['nodes'])} nodes, {n_links} links, "
          f"{injected} pages linked) + glossary "
          f"({len(build_glossary.site_entries())} terms, {gloss} pages)")


if __name__ == "__main__":
    main()
