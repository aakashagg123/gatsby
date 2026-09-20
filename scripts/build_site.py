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
CE_HTML = os.path.join(ROOT, "context-engineering-html")  # context engineering
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
<style>
  :root{{
    --bg:#ffffff;--surface:#ffffff;--ink:#1f2328;--muted:#59636e;
    --accent:#0969da;--accent-deep:#0550ae;--line:#d1d9e0;--code-bg:#f6f8fa;--soft:#f6f8fa;
  }}
  *{{box-sizing:border-box}}
  html{{-webkit-text-size-adjust:100%;text-size-adjust:100%}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;
    font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
  img,svg{{max-width:100%;height:auto}}
  .top{{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.9);backdrop-filter:blur(10px);
    border-bottom:1px solid var(--line);padding:14px 24px;display:flex;align-items:center;gap:20px;font-size:.9rem}}
  .top a{{color:var(--ink);text-decoration:none;font-weight:500}}
  .top a:hover{{color:var(--accent-deep)}}
  .top .brand{{color:var(--accent-deep);font-weight:600}}
  .menu-btn{{display:none;width:44px;height:44px;align-items:center;justify-content:center;
    border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink);
    font-size:18px;line-height:1;cursor:pointer;flex:0 0 auto;padding:0}}
  .menu-btn:hover{{border-color:var(--accent)}}
  #sb-scrim{{position:fixed;inset:0;background:rgba(31,35,40,.30);opacity:0;visibility:hidden;
    transition:opacity .2s;z-index:34}}
  #sb-scrim.open{{opacity:1;visibility:visible}}
  .layout{{display:grid;grid-template-columns:268px minmax(0,1fr)}}
  .layout.no-sidebar{{grid-template-columns:minmax(0,1fr)}}
  .sidebar{{border-right:1px solid var(--line);padding:26px 16px 60px;font-size:.86rem;
    max-height:calc(100vh - 49px);overflow-y:auto;position:sticky;top:49px;align-self:start}}
  .sidebar .sb-top{{display:block;color:var(--muted);font-weight:600;font-size:.78rem;
    letter-spacing:.02em;padding:6px 10px;margin-bottom:8px}}
  .sb-phase{{margin-bottom:2px}}
  .sb-phase-title{{display:block;padding:7px 10px;border-radius:6px;color:var(--ink);
    font-weight:500;line-height:1.35}}
  .sb-phase-title:hover{{background:var(--soft);text-decoration:none}}
  .sb-phase.active > .sb-phase-title{{color:var(--accent-deep);font-weight:600;background:var(--soft)}}
  .sb-lessons{{display:flex;flex-direction:column;margin:2px 0 10px;padding-left:10px;
    border-left:1px solid var(--line)}}
  .sb-lesson{{display:block;padding:6px 12px;border-radius:6px;color:var(--muted);
    font-size:.85rem;line-height:1.35}}
  .sb-lesson:hover{{background:var(--soft);color:var(--ink);text-decoration:none}}
  .sb-lesson.current{{color:var(--accent-deep);font-weight:600;background:#ddf4ff}}
  main{{max-width:760px;margin:0 auto;padding:48px 24px 64px}}
  .layout main{{margin:0}}
  .layout .lessonnav{{margin:8px 0 64px;max-width:760px}}
  @media (max-width:880px){{
    .layout{{grid-template-columns:minmax(0,1fr)}}
    .menu-btn{{display:inline-flex}}
    .sidebar{{display:block;position:fixed;top:0;left:0;bottom:0;z-index:35;
      width:280px;max-width:86vw;background:var(--bg);
      box-shadow:12px 0 40px rgba(31,35,40,.16);
      transform:translateX(-100%);transition:transform .22s ease;
      max-height:100%;padding:26px 16px 60px}}
    .sidebar.open{{transform:translateX(0)}}
    .layout main{{padding:32px 20px 40px}}
  }}
  h1,h2,h3,h4{{line-height:1.25;letter-spacing:-0.01em;font-weight:600}}
  h1{{font-size:2.2rem;margin:0 0 .6em}}
  h2{{font-size:1.5rem;margin-top:2.2em;padding-bottom:.35em;border-bottom:1px solid var(--line)}}
  h3{{font-size:1.18rem;margin-top:1.8em}}
  a{{color:var(--accent);text-decoration:none;text-underline-offset:3px}}
  a:hover{{text-decoration:underline}}
  code{{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;background:var(--soft);color:var(--ink);
    padding:.12em .4em;border-radius:5px;font-size:.86em}}
  pre{{background:var(--code-bg);color:var(--ink);padding:16px 18px;border-radius:6px;overflow:auto;
    font-size:.86em;line-height:1.55;border:1px solid var(--line)}}
  pre code{{background:none;color:inherit;padding:0;font-size:1em}}
  pre.mermaid{{background:#ffffff;color:var(--ink);
    border:1px solid var(--line);border-radius:6px;padding:26px 20px;margin:26px 0;
    text-align:center;overflow-x:auto}}
  pre.mermaid svg{{max-width:100%;height:auto;display:inline-block}}
  .mm-hint{{position:sticky;left:8px;display:block;width:max-content;
    font-size:11px;color:#59636e;background:#f6f8fa;border:1px solid #d1d9e0;
    border-radius:20px;padding:2px 10px;margin:0 0 8px;text-align:left}}
  table{{border-collapse:collapse;width:100%;margin:1.4em 0;font-size:.92em}}
  th,td{{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}}
  th{{background:var(--soft);font-weight:600}}
  tr:nth-child(even) td{{background:var(--soft)}}
  blockquote{{border-left:.25em solid var(--line);margin:1.4em 0;padding:0 1em;
    color:var(--muted);background:none}}
  blockquote p{{margin:.3em 0}}
  details{{background:var(--surface);border:1px solid var(--line);border-radius:6px;
    padding:12px 18px;margin:.8em 0}}
  summary{{cursor:pointer;font-weight:600;color:var(--accent-deep)}}
  hr{{border:none;border-top:1px solid var(--line);margin:2.4em 0}}
  ::selection{{background:#ddf4ff}}
  .lessonnav{{max-width:760px;margin:8px auto 64px;padding:24px;
    display:flex;gap:14px;flex-wrap:wrap}}
  .lessonnav a{{flex:1;min-width:0;background:var(--surface);border:1px solid var(--line);
    border-radius:6px;padding:14px 16px;font-size:.92rem;font-weight:500;color:var(--ink);
    transition:border-color .15s}}
  .lessonnav a:hover{{border-color:var(--accent);text-decoration:none}}
  .lessonnav .up{{flex:0 0 auto;text-align:center}}
  .lessonnav .nx{{text-align:right}}
  .lessonnav .lbl{{display:block;color:var(--muted);font-size:.72rem;font-weight:600;
    letter-spacing:.03em;margin-bottom:3px}}
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
<div class="top">{menu_btn}<a href="{root}index.html">← All courses</a><a class="brand" href="{track_root}index.html">{brand}</a></div>
<div id="sb-scrim"></div>
<div class="layout{layout_cls}">
{sidebar}
<div><main id="content">Loading…</main>
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
mermaid.initialize({{startOnLoad:false, theme:'base', securityLevel:'loose',
  themeVariables:{{
    background:'#ffffff',
    primaryColor:'#f6f8fa', primaryTextColor:'#1f2328', primaryBorderColor:'#d1d9e0',
    secondaryColor:'#eaeef2', secondaryBorderColor:'#d1d9e0', secondaryTextColor:'#1f2328',
    tertiaryColor:'#ffffff', tertiaryBorderColor:'#d1d9e0', tertiaryTextColor:'#1f2328',
    lineColor:'#59636e', textColor:'#1f2328', nodeTextColor:'#1f2328',
    clusterBkg:'#f6f8fa', clusterBorder:'#d1d9e0', edgeLabelBackground:'#ffffff',
    actorBkg:'#ddf4ff', actorBorder:'#0969da', actorTextColor:'#1f2328',
    actorLineColor:'#d1d9e0', signalColor:'#59636e', signalTextColor:'#1f2328',
    noteBkgColor:'#f6f8fa', noteBorderColor:'#d1d9e0',
    activationBkgColor:'#eaeef2', activationBorderColor:'#0969da',
    fontFamily:'-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif', fontSize:'14.5px'}},
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
<title>Supercharge your AI learning</title>
<style>
  :root{
    --bg:#ffffff;--surface:#ffffff;--ink:#1f2328;--muted:#59636e;
    --accent:#0969da;--accent-deep:#0550ae;--line:#d1d9e0;--soft:#f6f8fa;
  }
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
  body{margin:0;color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;
    font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden;
    background:
      radial-gradient(1000px 620px at 40px 10px, rgba(1,106,151,.40), transparent 60%),
      radial-gradient(900px 560px at calc(100% - 60px) 0px, rgba(1,132,152,.34), transparent 58%),
      radial-gradient(950px 560px at 50% 340px, rgba(197,152,1,.28), transparent 62%),
      var(--bg);
    background-repeat:no-repeat}
  .wrap{max-width:1400px;margin:0 auto;padding:104px 32px 80px}
  .eyebrow{display:inline-block;font-size:.78rem;font-weight:600;letter-spacing:.02em;
    color:var(--accent-deep);margin-bottom:16px}
  h1{font-size:clamp(1.15rem,calc(6.8vw - 2.5px),3rem);line-height:1.1;letter-spacing:-0.02em;
    font-weight:600;margin:0 0 .3em;white-space:nowrap}
  p.sub{color:var(--muted);font-size:1.2rem;margin:0;max-width:54ch}
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:22px;margin-top:52px}
  @media(max-width:680px){
    .wrap{padding:64px 18px 64px}
    .cards{grid-template-columns:1fr;gap:16px;margin-top:36px}
    p.sub{font-size:1.08rem}
    a.card{padding:24px;border-radius:6px}
  }
  a.card{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--surface);
    border:1px solid var(--line);border-radius:6px;padding:30px;
    transition:border-color .15s}
  a.card:hover{border-color:var(--accent)}
  a.card .tag{display:inline-block;font-size:.74rem;color:var(--accent-deep);font-weight:600;
    letter-spacing:.02em}
  a.card h2{margin:.5em 0 .35em;font-size:1.4rem;font-weight:600;letter-spacing:-0.01em}
  a.card p{color:var(--muted);margin:0;font-size:.98rem;line-height:1.6}
  footer{color:var(--muted);font-size:.85rem;margin-top:64px;border-top:1px solid var(--line);padding-top:24px}
  ::selection{background:#ddf4ff}
</style></head><body>
<div class="wrap">
  <h1>Supercharge your AI learning</h1>
  <p class="sub">Hands-on tracks for PMs and engineers moving into AI — from first principles to production.</p>
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
      construction pipeline, GraphRAG, governance, and the business case, in product leader language.</p>
    </a>
    <a class="card" href="generative-ai/index.html">
      <span class="tag">Generative AI</span>
      <h2>Generative AI: the big picture →</h2>
      <p>What makes AI "generative," the five modalities, why output is probabilistic, the
      four-layer product stack, and build vs. buy vs. fine-tune. Opens the
      Generative AI family.</p>
    </a>
    <a class="card" href="llms/index.html">
      <span class="tag">Generative AI</span>
      <h2>LLMs →</h2>
      <p>Tokens, the context window, the jagged frontier, prompting, sampling, choosing a
      model, and the order to reach for prompting, RAG, or fine-tuning.</p>
    </a>
    <a class="card" href="api-integrations/index.html">
      <span class="tag">Generative AI</span>
      <h2>APIs &amp; integrations →</h2>
      <p>The request/response contract, authentication, rate limits, streaming, retries,
      structured output, webhooks, and fitting a model call into a real system.</p>
    </a>
    <a class="card" href="rag-vector-databases/index.html">
      <span class="tag">Generative AI</span>
      <h2>RAG &amp; vector databases →</h2>
      <p>Grounding models in your data — embeddings, vector databases, chunking, retrieval
      quality, and when to reach for long-context, fine-tuning, or a graph.</p>
    </a>
    <a class="card" href="memory-and-context/index.html">
      <span class="tag">Generative AI</span>
      <h2>Memory &amp; context →</h2>
      <p>Memory as a product decision, the three shapes it takes, retrieval as its most
      common implementation, and the trust failures it has to be designed against.</p>
    </a>
    <a class="card" href="tool-calling/index.html">
      <span class="tag">Generative AI</span>
      <h2>Tool calling →</h2>
      <p>The line where an AI product stops talking and starts doing: designing a tool
      worth trusting, and keeping the permission boundary around it real.</p>
    </a>
    <a class="card" href="ai-agents/index.html">
      <span class="tag">Generative AI</span>
      <h2>AI agents →</h2>
      <p>The loop behind every agent, how much autonomy a task needs, what keeps it
      reliable across many steps, and when not to build one at all.</p>
    </a>
    <a class="card" href="agentic-workflows/index.html">
      <span class="tag">Generative AI</span>
      <h2>Agentic workflows →</h2>
      <p>Orchestrating more than one agent when a single loop isn't enough, and what
      it takes to make a workflow durable enough, and valuable enough, to own end to
      end.</p>
    </a>
    <a class="card" href="evaluation-and-observability/index.html">
      <span class="tag">Generative AI</span>
      <h2>Evaluation &amp; observability →</h2>
      <p>Why the eval set is the product spec for a non-deterministic system, and the
      order to actually build the eval and observability stack in.</p>
    </a>
    <a class="card" href="ai-security-and-guardrails/index.html">
      <span class="tag">Generative AI</span>
      <h2>AI security &amp; guardrails →</h2>
      <p>Jailbreak, injection, extraction, and poisoning are four different attacks —
      and why governance only counts once it becomes compliance evidence a regulator
      or buyer can check.</p>
    </a>
    <a class="card" href="cost-optimization/index.html">
      <span class="tag">Generative AI</span>
      <h2>Cost optimization →</h2>
      <p>Which lever fixes which cost driver, the build-vs-buy breakeven done as
      arithmetic, and the FinOps practice that turns attribution into governance
      before the invoice, not after.</p>
    </a>
    <a class="card" href="system-design/index.html">
      <span class="tag">Module</span>
      <h2>System design →</h2>
      <p>How real systems are designed at scale — from rate limiters to stock exchanges —
      with the architecture, tradeoffs, and failure modes that shape product decisions.
      28 systems across 8 lessons, diagrams included.</p>
    </a>
    <a class="card" href="context-engineering/index.html">
      <span class="tag">Module</span>
      <h2>Context engineering →</h2>
      <p>Treat what the model gets to see as a product decision — instructions,
      retrieval, memory, and live state, spec'd, governed, and evaluated with the same
      rigor as the output it produces.</p>
    </a>
    <a class="card" href="graph/index.html" style="border-color:#0d8fa5;background:linear-gradient(135deg,#e6f4f6 0%,#fdf3d9 100%)">
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
    'border:1px solid #d1d9e0;box-shadow:0 4px 16px rgba(31,35,40,.10);color:#0969da">'
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
    its own README. Links are relative to md_path's own directory.
    """
    if not tree:
        return ""
    here_dir = os.path.dirname(md_path)
    rows = [f'<a class="sb-top" href="{top_href}">← Track overview</a>']
    for phase in tree:
        active = md_path == phase["readme"] or any(md_path == en for _, en in phase["lessons"])
        readme_href = (os.path.relpath(phase["readme"][:-3] + ".html", here_dir)
                        if phase["readme"] else "#")
        cls = "sb-phase active" if active else "sb-phase"
        rows.append(f'<div class="{cls}"><a class="sb-phase-title" href="{readme_href}">'
                    f'{htmllib.escape(phase["title"])}</a>')
        if active and phase["lessons"]:
            rows.append('<div class="sb-lessons">')
            for title, en in phase["lessons"]:
                href = os.path.relpath(en[:-3] + ".html", here_dir)
                lcls = "sb-lesson current" if en == md_path else "sb-lesson"
                rows.append(f'<a class="{lcls}" href="{href}">{htmllib.escape(title)}</a>')
            rows.append('</div>')
        rows.append('</div>')
    return '<nav class="sidebar" id="sbNav">' + "".join(rows) + "</nav>"


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

    # 1r. Context engineering module: copy its pre-rendered pages.
    if os.path.isdir(CE_HTML):
        shutil.copytree(CE_HTML, os.path.join(SITE, "context-engineering"))

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
                menu_btn = ('<button class="menu-btn" id="sbToggle" aria-expanded="false" '
                            'aria-controls="sbNav" aria-label="Open lesson menu">☰</button>'
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

    print(f"built _site/ — ai module + md tracks ({pages} pages) + landing + "
          f"graph ({len(data['nodes'])} nodes, {n_links} links, "
          f"{injected} pages linked) + glossary "
          f"({len(build_glossary.site_entries())} terms, {gloss} pages) + "
          f"favicon ({fav} pages)")


if __name__ == "__main__":
    main()
