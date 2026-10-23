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
import html as htmllib
import os
import re
import shutil
import reader_widget
import build_html as bh
import design_system

import build_graph
import build_glossary
import glossary_widget
import landing
import lesson_status
import smooth_scroll

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "_site")
HTML = os.path.join(ROOT, "html")                       # AI engineering editions
FP_HTML = os.path.join(ROOT, "first-principles-html")   # first principles editions
PS_HTML = os.path.join(ROOT, "product-sense-html")      # product sense editions
TPS_HTML = os.path.join(ROOT, "technical-product-sense-html")  # technical product sense
TPM_HTML = os.path.join(ROOT, "technical-product-management-html")  # technical product management
AAI_HTML = os.path.join(ROOT, "agentic-ai-html")        # agentic AI
KG_HTML = os.path.join(ROOT, "knowledge-graphs-html")   # knowledge graphs
GAI_HTML = os.path.join(ROOT, "generative-ai-html")     # Generative AI: the big picture (GenAI family)
LLM_HTML = os.path.join(ROOT, "llms-html")              # LLMs (GenAI family, module 2)
API_HTML = os.path.join(ROOT, "api-integrations-html")  # APIs & integrations (GenAI family, module 3)
MEM_HTML = os.path.join(ROOT, "memory-and-context-html")  # Memory & context (GenAI family, module 5)
TOOL_HTML = os.path.join(ROOT, "tool-calling-html")     # Tool calling (GenAI family, module 6)
AGENTS_HTML = os.path.join(ROOT, "ai-agents-html")      # AI agents (GenAI family, module 7)
WORKFLOWS_HTML = os.path.join(ROOT, "agentic-workflows-html")  # Agentic workflows (GenAI family, module 8)
EVALOBS_HTML = os.path.join(ROOT, "evaluation-and-observability-html")  # Evaluation & observability (GenAI family, module 9)
SECURITY_HTML = os.path.join(ROOT, "ai-security-and-guardrails-html")  # AI security & guardrails (GenAI family, module 10)
COST_HTML = os.path.join(ROOT, "cost-optimization-html")  # Cost optimization (GenAI family, module 11)
RAG_HTML = os.path.join(ROOT, "rag-vector-databases-html")  # RAG & vector databases (GenAI family)
SD_HTML = os.path.join(ROOT, "system-design-html")      # system design
AC_HTML = os.path.join(ROOT, "access-control-html")     # access control (RBAC, ABAC, Keycloak)
LP_HTML = os.path.join(ROOT, "learning-paths-html")     # learning paths by role
CE_HTML = os.path.join(ROOT, "context-engineering-html")  # context engineering
PE_HTML = os.path.join(ROOT, "prompt-engineering-html")  # prompt engineering
ML_HTML = os.path.join(ROOT, "machine-learning-html")   # machine learning (foundation modules)
TENSORS_HTML = os.path.join(ROOT, "tensors-html")        # tensors (foundation modules)
CNNS_HTML = os.path.join(ROOT, "cnns-html")              # convolutional networks (foundation modules)
TRANSFORMERS_HTML = os.path.join(ROOT, "transformers-html")  # transformers (foundation modules)
AI_ASSISTED_HTML = os.path.join(ROOT, "ai-assisted-development-html")  # ai-assisted-development
FINE_TUNING_HTML = os.path.join(ROOT, "fine-tuning-html")  # fine-tuning
BUSINESS_ACUMEN_HTML = os.path.join(ROOT, "business-acumen-html")  # business acumen (product leaders)
# Markdown tracks rendered client-side, all sharing the phases/ folder shape:
# (source dir, site subdir, brand label shown in the viewer chrome)
# Canonical home of every page. One constant, so moving the site is a one-line change.
CANONICAL_BASE = "https://aakashagg123.github.io/gatsby/"
SOURCE_URL = "https://github.com/aakashagg123/gatsby"
PROVENANCE = (
    '<footer class="provenance" data-nosnippet>Compiled via <code>gatsby</code> '
    '(open-source pure-Python knowledge graph engine by Aakash Aggarwal) · '
    '<a href="' + SOURCE_URL + '">View source on GitHub →</a></footer>'
)
MD_TRACKS = [
    ("harness-engineering", "harness", "Harness engineering"),
    ("flowable", "flowable", "Flowable"),
]

VIEWER = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {brand}</title>
</head><body>
<header class="topbar">{menu_btn}<a class="brand" href="{track_root}index.html">{spark}<span>{brand}</span></a>
<nav class="topnav"><a class="Button" data-variant="ghost" data-color="secondary" data-size="sm" data-pill href="{root}index.html"><span class="ButtonInner">← All courses</span></a></nav></header>
<div id="sb-scrim"></div>
<div class="layout{layout_cls}">
{sidebar}
<div><main class="content MarkdownContent" id="content">Loading…</main>
{nav}
</div>
</div>
<script>
(function(){{
  var btn=document.getElementById('sbToggle'), nav=document.getElementById('sbNav'),
      scrim=document.getElementById('sb-scrim');
  if(!btn||!nav) return;
  function open(){{nav.classList.add('open');if(scrim)scrim.classList.add('open');btn.setAttribute('aria-expanded','true')}}
  function close(){{nav.classList.remove('open');if(scrim)scrim.classList.remove('open');btn.setAttribute('aria-expanded','false')}}
  btn.addEventListener('click',function(){{nav.classList.contains('open')?close():open()}});
  if(scrim)scrim.addEventListener('click',close);
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')close()}});
  nav.addEventListener('click',function(e){{if(e.target.closest('a'))close()}});
}})();
</script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.10.0/highlight.min.js"></script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize(DS.mermaidConfig());
window.addEventListener('ds-themechange',()=>DS.mermaidRerender(mermaid));
const md = await (await fetch('{md}')).text();
// protect mermaid fences so marked doesn't treat them as code
const blocks=[]; const stripped = md.replace(/```mermaid\\n([\\s\\S]*?)```/g,(m,c)=>{{
  blocks.push(c); return `<pre class="mermaid">__MERMAID_${{blocks.length-1}}__</pre>`;}});
let html = marked.parse(stripped);
html = html.replace(/__MERMAID_(\\d+)__/g,(m,i)=>blocks[+i]);
const el = document.getElementById('content'); el.innerHTML = html;
el.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{{
  const lab=b.querySelector('.ButtonInner')||b;
  const done=t=>{{lab.textContent=t;setTimeout(()=>{{lab.textContent='Copy command'}},1600)}};
  (navigator.clipboard?navigator.clipboard.writeText(b.getAttribute('data-copy')):Promise.reject())
    .then(()=>done('Copied'),()=>done('Select the text and copy'));
}}));
// Highlight code one block per idle slot so a long lesson never blocks the first scroll.
const codes=[...el.querySelectorAll('pre code[class*="language-"]')];
(function step(){{
  const c=codes.shift(); if(!c||!window.hljs) return;
  try{{hljs.highlightElement(c)}}catch(e){{}}
  (window.requestIdleCallback||setTimeout)(step);
}})();
// rewrite intra-site .md links to their .html viewers. AI-engineering lessons
// deploy under ai/<module>.html#<lesson> (not content/), so remap those first.
el.querySelectorAll('a[href]').forEach(a=>{{
  let h=a.getAttribute('href');
  if(!h || /^https?:|^#/.test(h)) return;
  h = h.replace(/(^|\\/)content\\/(\\d\\d-[\\w-]+)\\/README\\.md/,'$1ai/$2.html')
       .replace(/(^|\\/)content\\/(\\d\\d-[\\w-]+)\\/([\\w-]+)\\.md/,'$1ai/$2.html#$3')
       .replace(/(^|\\/)harness-engineering\\/README\\.md/,'$1harness/index.html')
       .replace(/(^|\\/)flowable\\/README\\.md/,'$1flowable/index.html')
       .replace(/(^|\\/)harness-engineering\\//,'$1harness/')
       .replace(/(^|\\/)(agentic-ai|first-principles|product-sense|technical-product-sense|technical-product-management|knowledge-graphs|generative-ai|llms|api-integrations|rag-vector-databases|memory-and-context|tool-calling|ai-agents|agentic-workflows|evaluation-and-observability|ai-security-and-guardrails|cost-optimization|system-design|access-control|context-engineering|prompt-engineering|learning-paths|machine-learning|tensors|cnns|transformers|fine-tuning|ai-assisted-development|business-acumen)\\/README\\.md/,'$1$2/index.html')
       .replace(/(^|\\/)README\\.md(#|$)/,'$1index.html$2')
       .replace(/\\.md(#|$)/,'.html$1');
  a.setAttribute('href', h);
}});
// Render each diagram when it nears the viewport, one at a time, so a long page does not
// block the main thread while the reader starts to scroll. Unrendered diagrams hold a
// fixed height (see the CSS) so nothing jumps when they appear.
const mer=[...el.querySelectorAll('pre.mermaid')];
let chain=Promise.resolve();
function fitOne(pre){{
  const s=pre.querySelector('svg'); if(!s) return;
  const w=(s.viewBox&&s.viewBox.baseVal&&s.viewBox.baseVal.width)||0;
  const cw=pre.clientWidth||0;
  if(cw&&w>cw*1.6){{s.style.maxWidth='none';
    const h=document.createElement('span');h.className='mm-hint';
    h.textContent='\u27f7 scroll';pre.insertBefore(h,s);}}
}}
function renderOne(pre){{
  chain=chain.then(async()=>{{ try{{ if(document.fonts&&document.fonts.ready)await document.fonts.ready; DS.mermaidRemember(pre); await mermaid.run({{nodes:[pre]}}); fitOne(pre); }}catch(e){{}} }});
}}
if('IntersectionObserver' in window && mer.length>1){{
  const io=new IntersectionObserver(es=>{{es.forEach(e=>{{
    if(e.isIntersecting){{ io.unobserve(e.target); renderOne(e.target); }} }});}},{{rootMargin:'900px 0px'}});
  mer.forEach(p=>io.observe(p));
}} else mer.forEach(renderOne);
</script></body></html>
"""

LANDING = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Supercharge your AI learning</title>
</head><body>
__BODY__
</body></html>
"""


GRAPH_BTN = (
    '<a class="Button fab fab-graph" href="{href}" title="Open the knowledge graph" '
    'aria-label="Open the knowledge graph" data-variant="outline" data-color="secondary" '
    'data-size="xl" data-uniform data-pill><span class="ButtonInner">'
    '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" '
    'stroke-width="1.6" data-no-autosize><circle cx="5" cy="5" r="2.4"/><circle cx="15" cy="7" r="2.4"/>'
    '<circle cx="9" cy="15" r="2.4"/><path d="M7.2 6l5.5.7M6 7.2l2.2 5.6M13.8 9l-3.4 4.2"/>'
    '</svg></span></a>'
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


FAVICON_SRC_DIR = os.path.join(ROOT, "assets", "favicon")


def inject_favicon(site):
    """Ship the sitewide favicon and reference it from every page (landing
    pages included, unlike inject_glossary), with a per-page relative root so
    it resolves at any depth."""
    assets = os.path.join(site, "assets")
    os.makedirs(assets, exist_ok=True)
    shutil.copy(os.path.join(FAVICON_SRC_DIR, "favicon-32.png"),
                os.path.join(assets, "favicon-32.png"))
    shutil.copy(os.path.join(FAVICON_SRC_DIR, "favicon-180.png"),
                os.path.join(assets, "favicon-180.png"))
    injected = 0
    for dp, _, files in os.walk(site):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dp, fn)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            pos = text.find("<head>")
            if pos == -1 or "rel=\"icon\"" in text:
                continue
            pos += len("<head>")
            root = os.path.relpath(site, os.path.dirname(path)).replace(os.sep, "/")
            root = "" if root == "." else root + "/"
            tags = (
                f'<link rel="icon" type="image/png" sizes="32x32" href="{root}assets/favicon-32.png">'
                f'<link rel="apple-touch-icon" sizes="180x180" href="{root}assets/favicon-180.png">'
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(text[:pos] + tags + text[pos:])
            injected += 1
    return injected


def inject_design_system(site):
    """Ship ds.css and ds.js and link them from every page, first thing in <head>, with a
    per-page relative root so they resolve at any depth. The theme boot script sets
    data-theme before first paint. See design_system.py."""
    design_system.write_assets(os.path.join(site, "assets"))
    injected = 0
    for dp, _, files in os.walk(site):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dp, fn)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            pos = text.find("<head>")
            if pos == -1 or "assets/ds.css" in text:
                continue
            pos += len("<head>")
            root = os.path.relpath(site, os.path.dirname(path)).replace(os.sep, "/")
            root = "" if root == "." else root + "/"
            with open(path, "w", encoding="utf-8") as f:
                f.write(text[:pos] + design_system.head_tags(root) + text[pos:])
            injected += 1
    return injected


def inject_smooth_scroll(site):
    """Add the shared scroll-smoothness rules to every page, landing pages and the
    graph included. They go in an inline <style> just before </head>, so they load
    after each page's own <style> (and win the cascade) without an extra request.
    See smooth_scroll.py."""
    tag = ('<style id="smooth-scroll">' + smooth_scroll.CSS.strip() + '</style>'
           '<script type="speculationrules">' + smooth_scroll.SPECULATION_RULES + '</script>')
    fade = '<style id="page-fade">' + smooth_scroll.VIEW_TRANSITION_CSS.strip() + '</style>'
    injected = 0
    for dp, _, files in os.walk(site):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dp, fn)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            pos = text.find("</head>")
            if pos == -1 or 'id="smooth-scroll"' in text:
                continue
            page_tag = tag if 'class="graph-page"' in text else tag + fade
            with open(path, "w", encoding="utf-8") as f:
                f.write(text[:pos] + page_tag + text[pos:])
            injected += 1
    return injected


def inject_reader_widget(site):
    """Give every page the current reader-settings widget (old pre-rendered pages carry a
    copy baked in at their build time)."""
    swapped = 0
    for dp, _, files in os.walk(site):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dp, fn)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            new = reader_widget.replace(text)
            if new != text:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
                swapped += 1
    return swapped


def inject_canonical_and_provenance(site):
    """Add <link rel=canonical> to <head> of every page, and a provenance footer to every
    content page (not the full-screen graph app). The footer goes before the reader
    widget, so it stays inside <body> but outside <main>. Idempotent."""
    tagged = 0
    for dp, _, files in os.walk(site):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dp, fn)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            if 'rel="canonical"' in text or "</head>" not in text:
                continue
            tag = f'<link rel="canonical" href="{canonical_url(site, path)}">'
            text = text.replace("</head>", tag + "</head>", 1)
            if 'class="graph-page"' not in text and 'class="provenance"' not in text:
                anchor = '<div id="rs-root">' if '<div id="rs-root">' in text else "</body>"
                text = text.replace(anchor, PROVENANCE + anchor, 1)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            tagged += 1
    return tagged


def html_for(md_path):
    """Deployed viewer path for a markdown file: README.md -> index.html in its own
    folder (clean directory URLs), every other file.md -> file.html."""
    if os.path.basename(md_path) == "README.md":
        return os.path.join(os.path.dirname(md_path), "index.html")
    return md_path[:-3] + ".html"


REDIRECT_STUB = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="noindex">
<title>Moved</title>
</head><body><p>This page moved to <a href="{target}">{target}</a>.</p></body></html>
"""


def canonical_url(site, path):
    """Absolute canonical URL of a built page: index.html collapses to its directory URL."""
    rel = os.path.relpath(path, site).replace(os.sep, "/")
    if rel == "index.html":
        return CANONICAL_BASE
    if rel.endswith("/index.html"):
        rel = rel[:-len("index.html")]
    return CANONICAL_BASE + rel


def write_redirect_stub(old_html, target="index.html"):
    """Leave a meta-refresh stub where a README.html used to be, so old links still work.
    The stub's canonical is the page it points to."""
    canonical = canonical_url(SITE, os.path.join(os.path.dirname(old_html), target))
    with open(old_html, "w") as f:
        f.write(REDIRECT_STUB.format(target=target, canonical=canonical))


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


MERMAID_FENCE_RE = re.compile(r"```mermaid\n.*?```", re.DOTALL)


def apply_phased_diagram_overrides(dst_track, site_key):
    """Swap raw mermaid fences in copied markdown for hand-crafted HTML overrides.

    Runs once, right after the track is copied into _site/, so an override lands as
    a plain HTML block with no mermaid fence left behind -- invisible to the
    client-side marked/mermaid pipeline in the VIEWER template, no JS changes needed.
    Overrides are keyed by lesson directory name for lesson docs (phases/*/*/docs/en.md,
    unique across a track), or by filename for any other markdown file (e.g. a track-root
    ROADMAP.md) -- 0-indexed per file: diagrams/<site_key>/<key>-<n>.html. Source files
    under <track>/... are never touched -- only the copies inside _site/.
    """
    ddir = os.path.join(ROOT, "diagrams", site_key)
    if not os.path.isdir(ddir):
        return
    for dp, _, files in os.walk(dst_track):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            md_path = os.path.join(dp, fn)
            if is_lesson(md_path):
                key = os.path.basename(os.path.dirname(os.path.dirname(md_path)))
            else:
                key = os.path.splitext(fn)[0]
            with open(md_path) as f:
                text = f.read()
            idx = [-1]

            def _repl(m):
                idx[0] += 1
                p = os.path.join(ddir, f"{key}-{idx[0]}.html")
                if os.path.exists(p):
                    with open(p) as f:
                        return f.read()
                return m.group(0)

            new_text = MERMAID_FENCE_RE.sub(_repl, text)
            if new_text != text:
                with open(md_path, "w") as f:
                    f.write(new_text)


def apply_lesson_status(dst_track, src_dir, records):
    """Back every Build/Use claim with evidence, in the copied markdown only.

    Tables: the hand-typed check after a lesson link becomes the badge lesson_status earned.
    Lesson pages: a panel under the H1 with the run command, source links, the source in a
    collapsible block and the output of the run this build made. Sources are never touched.
    """
    changed = 0
    for dp, _, files in os.walk(dst_track):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            md_path = os.path.join(dp, fn)
            md_dir = os.path.join(src_dir, os.path.relpath(dp, dst_track)).replace(os.sep, "/")
            md_dir = os.path.normpath(md_dir)
            with open(md_path, encoding="utf-8") as f:
                text = f.read()
            new = lesson_status.rewrite_tables(text, md_dir, records)
            if is_lesson(md_path):
                rec = records.get(os.path.normpath(os.path.join(md_dir, "..")).replace(os.sep, "/"))
                if rec is not None and rec["state"] != "concept":
                    new = lesson_status.add_panel(new, rec)
            if new != text:
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(new)
                changed += 1
    return changed


def _title_of(md_path):
    with open(md_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("# ").strip()
        return os.path.splitext(os.path.basename(md_path))[0]


def phase_tree(dst_track):
    """Phase -> lessons tree: [{title, readme (en.md path), lessons: [(title, en.md path)]}].

    Mirrors lesson_order()'s walk (phase dir, then lesson dir, both sorted) so the
    tree and the prev/next sequence always agree on lesson order.
    """
    tree = []
    phases_dir = os.path.join(dst_track, "phases")
    if not os.path.isdir(phases_dir):
        return tree
    for phase in sorted(os.listdir(phases_dir)):
        pdir = os.path.join(phases_dir, phase)
        if not os.path.isdir(pdir):
            continue
        readme = os.path.join(pdir, "README.md")
        lessons = []
        for lesson in sorted(os.listdir(pdir)):
            en = os.path.join(pdir, lesson, "docs", "en.md")
            if os.path.exists(en):
                lessons.append((_title_of(en), en))
        tree.append({
            "dir": pdir,
            "title": _title_of(readme) if os.path.exists(readme) else phase,
            "readme": readme if os.path.exists(readme) else None,
            "lessons": lessons,
        })
    return tree


def sidebar_html(md_path, tree, top_href):
    """Two-level Phase -> Lesson sidebar. The phase containing md_path (if any) is
    expanded with its lesson links; every other phase collapses to a single link to
    its own README. Links are relative to md_path's own directory. Markup matches the
    flat tracks: .modlink for a phase, .sub for its lessons.
    """
    if not tree:
        return ""
    here_dir = os.path.dirname(md_path)
    rows = [f'<a class="modlink" href="{top_href}">← Track overview</a>']
    for phase in tree:
        active = md_path == phase["readme"] or any(md_path == en for _, en in phase["lessons"])
        readme_href = (os.path.relpath(html_for(phase["readme"]), here_dir)
                        if phase["readme"] else "#")
        cls = "modlink active" if active else "modlink"
        rows.append(f'<a class="{cls}" href="{readme_href}">{htmllib.escape(phase["title"])}</a>')
        if active and phase["lessons"]:
            rows.append('<div class="sub">')
            for title, en in phase["lessons"]:
                href = os.path.relpath(en[:-3] + ".html", here_dir)
                cur = ' class="active" aria-current="page"' if en == md_path else ""
                rows.append(f'<a{cur} href="{href}">{htmllib.escape(title)}</a>')
            rows.append('</div>')
    return '<aside class="sidebar" id="sbNav"><div class="sticky">' + "".join(rows) + "</div></aside>"


def nav_html(md_path, prev_md, next_md):
    """Prev / Up-to-phase / Next cards for a lesson page, links relative to its html."""
    here = md_path[:-3] + ".html"
    parts = []
    if prev_md:
        rel = os.path.relpath(prev_md[:-3] + ".html", os.path.dirname(here))
        parts.append(f'<a class="navcard prev" href="{rel}"><span class="lbl">← Previous</span>'
                     f'<span class="ttl">{htmllib.escape(_title_of(prev_md))}</span></a>')
    up = os.path.relpath(os.path.join(os.path.dirname(md_path), "..", "..", "index.html"),
                         os.path.dirname(here))
    parts.append(f'<a class="navcard up" href="{up}"><span class="lbl">Phase</span>'
                 f'<span class="ttl">Overview</span></a>')
    if next_md:
        rel = os.path.relpath(next_md[:-3] + ".html", os.path.dirname(here))
        parts.append(f'<a class="navcard next" href="{rel}"><span class="lbl">Next →</span>'
                     f'<span class="ttl">{htmllib.escape(_title_of(next_md))}</span></a>')
    return '<nav class="pagenav">' + "".join(parts) + "</nav>"


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

    # 1h. Generative AI: the big picture (Generative AI family, module 1): copy its pages.
    if os.path.isdir(GAI_HTML):
        shutil.copytree(GAI_HTML, os.path.join(SITE, "generative-ai"))

    # 1i. LLMs (Generative AI family, module 2): copy its pages.
    if os.path.isdir(LLM_HTML):
        shutil.copytree(LLM_HTML, os.path.join(SITE, "llms"))

    # 1j. APIs & integrations (Generative AI family, module 3): copy its pages.
    if os.path.isdir(API_HTML):
        shutil.copytree(API_HTML, os.path.join(SITE, "api-integrations"))

    # 1k. RAG & vector databases module (Generative AI family): copy its pages.
    if os.path.isdir(RAG_HTML):
        shutil.copytree(RAG_HTML, os.path.join(SITE, "rag-vector-databases"))

    # 1l. Memory & context (Generative AI family, module 5): copy its pages.
    if os.path.isdir(MEM_HTML):
        shutil.copytree(MEM_HTML, os.path.join(SITE, "memory-and-context"))

    # 1m. Tool calling (Generative AI family, module 6): copy its pages.
    if os.path.isdir(TOOL_HTML):
        shutil.copytree(TOOL_HTML, os.path.join(SITE, "tool-calling"))

    # 1n. AI agents (Generative AI family, module 7): copy its pages.
    if os.path.isdir(AGENTS_HTML):
        shutil.copytree(AGENTS_HTML, os.path.join(SITE, "ai-agents"))

    # 1o. Agentic workflows (Generative AI family, module 8): copy its pages.
    if os.path.isdir(WORKFLOWS_HTML):
        shutil.copytree(WORKFLOWS_HTML, os.path.join(SITE, "agentic-workflows"))

    # 1p. Evaluation & observability (Generative AI family, module 9): copy its pages.
    if os.path.isdir(EVALOBS_HTML):
        shutil.copytree(EVALOBS_HTML, os.path.join(SITE, "evaluation-and-observability"))

    # 1p2. AI security & guardrails (Generative AI family, module 10): copy its pages.
    if os.path.isdir(SECURITY_HTML):
        shutil.copytree(SECURITY_HTML, os.path.join(SITE, "ai-security-and-guardrails"))

    # 1p3. Cost optimization (Generative AI family, module 11): copy its pages.
    if os.path.isdir(COST_HTML):
        shutil.copytree(COST_HTML, os.path.join(SITE, "cost-optimization"))

    # 1q. System design module: copy its pre-rendered pages.
    if os.path.isdir(SD_HTML):
        shutil.copytree(SD_HTML, os.path.join(SITE, "system-design"))

    # 1q2. Access control module: copy its pre-rendered pages.
    if os.path.isdir(AC_HTML):
        shutil.copytree(AC_HTML, os.path.join(SITE, "access-control"))

    # 1q3. Learning paths: copy its pre-rendered pages.
    if os.path.isdir(LP_HTML):
        shutil.copytree(LP_HTML, os.path.join(SITE, "learning-paths"))

    # 1r. Context engineering module: copy its pre-rendered pages.
    if os.path.isdir(CE_HTML):
        shutil.copytree(CE_HTML, os.path.join(SITE, "context-engineering"))

    # 1s. Prompt engineering module: copy its pre-rendered pages.
    if os.path.isdir(PE_HTML):
        shutil.copytree(PE_HTML, os.path.join(SITE, "prompt-engineering"))

    # 1t. Machine learning module: copy its pre-rendered pages.
    if os.path.isdir(ML_HTML):
        shutil.copytree(ML_HTML, os.path.join(SITE, "machine-learning"))

    # 1u. Tensors module: copy its pre-rendered pages.
    if os.path.isdir(TENSORS_HTML):
        shutil.copytree(TENSORS_HTML, os.path.join(SITE, "tensors"))

    # 1v. Convolutional networks module: copy its pre-rendered pages.
    if os.path.isdir(CNNS_HTML):
        shutil.copytree(CNNS_HTML, os.path.join(SITE, "cnns"))

    # 1x. Transformers module: copy its pre-rendered pages.
    if os.path.isdir(TRANSFORMERS_HTML):
        shutil.copytree(TRANSFORMERS_HTML, os.path.join(SITE, "transformers"))

    # 1y. AI-assisted development module: copy its pre-rendered pages.
    if os.path.isdir(AI_ASSISTED_HTML):
        shutil.copytree(AI_ASSISTED_HTML, os.path.join(SITE, "ai-assisted-development"))

    # 1y. Fine-tuning module: copy its pre-rendered pages.
    if os.path.isdir(FINE_TUNING_HTML):
        shutil.copytree(FINE_TUNING_HTML, os.path.join(SITE, "fine-tuning"))

    # 1w. Business acumen module: copy its pre-rendered pages.
    if os.path.isdir(BUSINESS_ACUMEN_HTML):
        shutil.copytree(BUSINESS_ACUMEN_HTML, os.path.join(SITE, "business-acumen"))

    # 2. Markdown tracks (harness engineering, flowable): copy each tree
    # (md + code + outputs) and render a viewer next to every markdown file.
    pages = 0
    legacy_readmes = []
    records = lesson_status.collect(run=True)
    bad = [r for r in records if records[r]["state"] == "failing"]
    for r in bad:
        print(f"WARNING: lesson code failing: {r}")
    for src_dir, site_key, brand in MD_TRACKS:
        dst_track = os.path.join(SITE, site_key)
        shutil.copytree(os.path.join(ROOT, src_dir), dst_track)
        apply_phased_diagram_overrides(dst_track, site_key)
        apply_lesson_status(dst_track, src_dir, records)

        # 3. Lesson ordering for prev/next navigation.
        lessons = lesson_order(dst_track)
        prev_next = {}
        for i, md in enumerate(lessons):
            prev_next[md] = (lessons[i - 1] if i > 0 else None,
                             lessons[i + 1] if i < len(lessons) - 1 else None)

        # 3b. Phase -> lesson tree for the two-level left sidebar (Workstream 2b).
        tree = phase_tree(dst_track)

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
                html_path = html_for(md_path)
                md_url = "./" + fn
                nav = ""
                if is_lesson(md_path):
                    p, n = prev_next.get(md_path, (None, None))
                    nav = nav_html(md_path, p, n)
                sidebar = sidebar_html(md_path, tree, (root or "./") + "index.html")
                layout_cls = "" if sidebar else " no-sidebar"
                menu_btn = ('<button class="Button menu-btn" id="sbToggle" data-variant="ghost" '
                            'data-color="secondary" data-size="lg" data-uniform data-pill '
                            'aria-expanded="false" aria-controls="sbNav" aria-label="Open lesson menu">'
                            '<span class="ButtonInner">'+design_system.MENU_ICON+'</span></button>'
                            if sidebar else "")
                with open(html_path, "w") as f:
                    f.write(reader_widget.inject(VIEWER.format(
                        title=title,
                        brand=brand,
                        md=md_url,
                        root="../" + root if root else "../",   # _site/ root
                        track_root=root or "./",
                        nav=nav,
                        sidebar=sidebar,
                        layout_cls=layout_cls,
                        menu_btn=menu_btn,
                        spark=bh.SPARK,
                    )))
                pages += 1

        # Every README.md already rendered to index.html (the track landing is
        # <track>/index.html). Remember the legacy README.html paths; the stubs are
        # written last (step 12) so the page injectors never touch them.
        for dp, _, files in os.walk(dst_track):
            if "README.md" in files:
                legacy_readmes.append(os.path.join(dp, "README.html"))

    # 5. Knowledge graph: extract nodes/edges from the markdown sources and
    # write the interactive graph page (Quartz-style).
    data = build_graph.graph_data()
    build_graph.write_graph_page(SITE, data)
    n_links = sum(1 for e in data["edges"] if e[3] == "link")

    # 6. Top landing (with live graph counts).
    n_tracks = len({n["track"] for n in data["nodes"]})
    body = landing.render(len(data["nodes"]), n_links, n_tracks)
    with open(os.path.join(SITE, "index.html"), "w") as f:
        f.write(LANDING.replace("__BODY__", body))

    # 7. Every content page gets a floating button into the graph, focused on
    # that page's own node.
    injected = inject_graph_buttons(SITE, build_graph.page_focus_map(data))

    # 8. Clickable glossary terms + explainer sidebar on every content page.
    gloss = inject_glossary(SITE)

    # 9. Sitewide favicon, every page including both landing pages.
    fav = inject_favicon(SITE)

    # 10. Shared scroll-smoothness layer, every page.
    smooth = inject_smooth_scroll(SITE)

    # 11. The design system: tokens, SDK components and the site layer, every page.
    ds_pages = inject_design_system(SITE)

    # 11a. Current reader widget on every page (before the provenance footer anchors on it).
    widgets = inject_reader_widget(SITE)

    # 11b. Canonical URL on every page, provenance footer on content pages.
    canon = inject_canonical_and_provenance(SITE)

    # 12. Redirect stubs at the legacy README.html paths (after every injector).
    for old in legacy_readmes:
        write_redirect_stub(old)

    print(f"built _site/ — ai module + md tracks ({pages} pages) + landing + "
          f"graph ({len(data['nodes'])} nodes, {n_links} links, "
          f"{injected} pages linked) + glossary "
          f"({len(build_glossary.site_entries())} terms, {gloss} pages) + "
          f"favicon ({fav} pages) + smooth-scroll ({smooth} pages) + "
          f"design-system ({ds_pages} pages) + canonical ({canon} pages) + reader-widget ({widgets} pages)")


if __name__ == "__main__":
    main()
