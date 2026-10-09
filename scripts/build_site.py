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
       .replace(/(^|\\/)(agentic-ai|first-principles|product-sense|technical-product-sense|technical-product-management|knowledge-graphs|generative-ai|llms|api-integrations|rag-vector-databases|memory-and-context|tool-calling|ai-agents|agentic-workflows|evaluation-and-observability|ai-security-and-guardrails|cost-optimization|system-design|access-control|context-engineering|prompt-engineering|learning-paths)\\/README\\.md/,'$1$2/index.html')
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
  chain=chain.then(async()=>{{ try{{ DS.mermaidRemember(pre); await mermaid.run({{nodes:[pre]}}); fitOne(pre); }}catch(e){{}} }});
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
<main class="index landing">
  <h1>Supercharge your AI learning</h1>
  <p class="lede">Hands-on tracks for PMs and engineers moving into AI — from first principles to production.</p>
  <div class="group">Choose your path <a class="TextLink" data-primary="" href="learning-paths/index.html">Compare the paths →</a></div>
  <div class="cards">
    <a class="card" href="learning-paths/senior-product-manager.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Path</span>
      <h3>Senior Product Manager →</h3>
      <p>Lead an AI feature end to end: the approach, the quality bar, the cost and the risk.</p>
    </a>
    <a class="card" href="learning-paths/ai-product-lead.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Path</span>
      <h3>AI Product Lead →</h3>
      <p>Own grounding, context, memory, agents, trust and cost across an AI product line.</p>
    </a>
    <a class="card" href="learning-paths/ai-engineer.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Path</span>
      <h3>AI Engineer →</h3>
      <p>Build, test and run a retrieval-backed, tool-using agent, and explain how it fails.</p>
    </a>
    <a class="card" href="learning-paths/ai-engineering-lead.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Path</span>
      <h3>AI Engineering Lead →</h3>
      <p>Review architecture, set quality and safety standards, and control cost.</p>
    </a>
  </div>
  <div class="group">All modules</div>
  <div class="cards">
    <a class="card" href="ai/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>AI engineering →</h3>
      <p>The engineering discipline under production LLM systems — inference, retrieval,
      evals, observability, safety, cost. Designed reading editions.</p>
    </a>
    <a class="card" href="harness/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>Harness engineering →</h3>
      <p>Build a coding agent's harness from scratch — loop, tools, context, permissions,
      subagents — then use the real SDK. 10 phases, 41 lessons, one tested capstone.</p>
    </a>
    <a class="card" href="flowable/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>Flowable →</h3>
      <p>Process automation from scratch — build a token engine, wait states, and a job
      executor by hand, then run real BPMN on the Flowable engine. Concept-first for
      PMs, with a build layer for engineers.</p>
    </a>
    <a class="card" href="first-principles/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>First principles →</h3>
      <p>Reason from fundamentals and build range across disciplines — the method,
      a latticework of mental models, becoming a polymath, and learning how to learn.</p>
    </a>
    <a class="card" href="product-sense/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>Product sense →</h3>
      <p>The instinct for what makes a product succeed, for APMs & PMs moving into AI PM —
      motivation, empathy, creativity, communication, domain expertise, and product sense for AI.</p>
    </a>
    <a class="card" href="technical-product-sense/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>Technical product sense →</h3>
      <p>Read systems like an engineer — architecture, APIs, data, latency, reliability,
      and tech debt — with a diagram in every lesson. For APMs & PMs moving into AI PM.</p>
    </a>
    <a class="card" href="technical-product-management/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>Technical product management →</h3>
      <p>The operating discipline of shipping — the role, specs, prioritization, execution,
      metrics, and releases — with a diagram in every lesson. For APMs & PMs moving into AI PM.</p>
    </a>
    <a class="card" href="agentic-ai/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>Agentic AI →</h3>
      <p>What agents actually are — the loop, tools, memory, planning — plus reliability,
      security, and economics. Opens with a knowledge graph; a diagram in every lesson.</p>
    </a>
    <a class="card" href="knowledge-graphs/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>Knowledge graphs →</h3>
      <p>Treat what the company knows as a product — entities and ontologies, the
      construction pipeline, GraphRAG, governance, and the business case, in product leader language.</p>
    </a>
    <a class="card" href="generative-ai/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>Generative AI: the big picture →</h3>
      <p>What makes AI "generative," the five modalities, why output is probabilistic, the
      four-layer product stack, and build vs. buy vs. fine-tune. Opens the
      Generative AI family.</p>
    </a>
    <a class="card" href="llms/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>LLMs →</h3>
      <p>Tokens, the context window, the jagged frontier, prompting, sampling, choosing a
      model, and the order to reach for prompting, RAG, or fine-tuning.</p>
    </a>
    <a class="card" href="api-integrations/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>APIs &amp; integrations →</h3>
      <p>The request/response contract, authentication, rate limits, streaming, retries,
      structured output, webhooks, and fitting a model call into a real system.</p>
    </a>
    <a class="card" href="rag-vector-databases/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>RAG &amp; vector databases →</h3>
      <p>Grounding models in your data — embeddings, vector databases, chunking, retrieval
      quality, and when to reach for long-context, fine-tuning, or a graph.</p>
    </a>
    <a class="card" href="memory-and-context/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>Memory &amp; context →</h3>
      <p>Memory as a product decision, the three shapes it takes, how memories are written
      and kept, the designs for reading them back, and the trust failures it has to be
      designed against.</p>
    </a>
    <a class="card" href="tool-calling/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>Tool calling →</h3>
      <p>The line where an AI product stops talking and starts doing: designing a tool
      worth trusting, and keeping the permission boundary around it real.</p>
    </a>
    <a class="card" href="ai-agents/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>AI agents →</h3>
      <p>The loop behind every agent, how much autonomy a task needs, what keeps it
      reliable across many steps, when not to build one, how to run one safely, and how to
      choose one.</p>
    </a>
    <a class="card" href="agentic-workflows/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>Agentic workflows →</h3>
      <p>Choosing a workflow pattern, when more than one agent earns its cost, and what
      it takes to make a workflow durable enough to own end to end.</p>
    </a>
    <a class="card" href="evaluation-and-observability/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>Evaluation &amp; observability →</h3>
      <p>Why the eval set is the product spec for a non-deterministic system, and the
      order to actually build the eval and observability stack in.</p>
    </a>
    <a class="card" href="ai-security-and-guardrails/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>AI security &amp; guardrails →</h3>
      <p>Jailbreak, injection, extraction, and poisoning are four different attacks.
      How to test your defenses, and how governance becomes compliance evidence a
      regulator or buyer can check.</p>
    </a>
    <a class="card" href="cost-optimization/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Generative AI</span>
      <h3>Cost optimization →</h3>
      <p>Which lever fixes which cost driver, the build-vs-buy breakeven done as
      arithmetic, and the FinOps practice that turns attribution into governance
      before the invoice, not after.</p>
    </a>
    <a class="card" href="system-design/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>System design →</h3>
      <p>How real systems are designed at scale — from rate limiters to stock exchanges —
      with the architecture, tradeoffs, and failure modes that shape product decisions.
      28 systems across 8 lessons, diagrams included.</p>
    </a>
    <a class="card" href="access-control/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>Access control →</h3>
      <p>Who may do what, and where that is decided: authentication vs authorization,
      OAuth and tokens, RBAC, ABAC, relationship-based access, Keycloak, and access
      control for AI agents. 8 lessons.</p>
    </a>
    <a class="card" href="context-engineering/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>Context engineering →</h3>
      <p>Treat what the model gets to see as a product decision — instructions,
      retrieval, memory, and live state, spec'd, governed, and evaluated with the same
      rigor as the output it produces.</p>
    </a>
    <a class="card" href="prompt-engineering/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Module</span>
      <h3>Prompt engineering →</h3>
      <p>The craft of writing input a model will reliably act on — from ChatGPT
      productivity patterns, through few-shot and chain-of-thought, into the prompts
      that drive Claude Code and other coding agents. 10 lessons.</p>
    </a>
    <a class="card" href="graph/index.html">
      <span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>Explore</span>
      <h3>Knowledge graph →</h3>
      <p>Every page across all nine modules as one interactive map — __NODES__ pages,
      __LINKS__ cross-references. Search it, filter by track, click any node to jump in.</p>
    </a>
  </div>
  <footer class="foot">Educational content. Use it, fork it, teach from it.</footer>
</main></body></html>
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
    tag = '<style id="smooth-scroll">' + smooth_scroll.CSS.strip() + '</style>'
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
            with open(path, "w", encoding="utf-8") as f:
                f.write(text[:pos] + tag + text[pos:])
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
        readme_href = (os.path.relpath(phase["readme"][:-3] + ".html", here_dir)
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
    up = os.path.relpath(os.path.join(os.path.dirname(md_path), "..", "..", "README.html"),
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

    # 2. Markdown tracks (harness engineering, flowable): copy each tree
    # (md + code + outputs) and render a viewer next to every markdown file.
    pages = 0
    for src_dir, site_key, brand in MD_TRACKS:
        dst_track = os.path.join(SITE, site_key)
        shutil.copytree(os.path.join(ROOT, src_dir), dst_track)
        apply_phased_diagram_overrides(dst_track, site_key)

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
                html_path = md_path[:-3] + ".html"
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

    # 9. Sitewide favicon, every page including both landing pages.
    fav = inject_favicon(SITE)

    # 10. Shared scroll-smoothness layer, every page.
    smooth = inject_smooth_scroll(SITE)

    # 11. The design system: tokens, SDK components and the site layer, every page.
    ds_pages = inject_design_system(SITE)

    print(f"built _site/ — ai module + md tracks ({pages} pages) + landing + "
          f"graph ({len(data['nodes'])} nodes, {n_links} links, "
          f"{injected} pages linked) + glossary "
          f"({len(build_glossary.site_entries())} terms, {gloss} pages) + "
          f"favicon ({fav} pages) + smooth-scroll ({smooth} pages) + "
          f"design-system ({ds_pages} pages)")


if __name__ == "__main__":
    main()
