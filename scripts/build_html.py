#!/usr/bin/env python3
"""
Build beautified, self-contained HTML editions of the curriculum in a warm,
Anthropic-inspired UX. One comprehensive page per module, plus a landing index.

Source of truth is the markdown in content/. Run:  python3 scripts/build_html.py
"""
import os
import re
import html as htmllib
import markdown
import reader_widget
import design_system as ds

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
OUT = os.path.join(ROOT, "html")

# ---- module / lesson ordering -------------------------------------------------
MODULES = [
    ("00-foundations", "00", "Foundations",
     "The mindset shift from “writing prompts” to “engineering systems.”",
     ["harness-engineering", "context-engineering", "infra-not-demos"]),
    ("01-inference-internals", "01", "Inference internals",
     "What happens between your request and the tokens that come back.",
     ["prompt-vs-semantic-caching", "kv-cache-management", "prefill-vs-decode",
      "batching-and-paged-attention", "speculative-quantization-distillation",
      "quantization-formats"]),
    ("02-reliable-outputs", "02", "Reliable outputs & tool use",
     "Making models produce things downstream systems can trust.",
     ["structured-output", "function-calling", "agent-guardrails", "model-routing"]),
    ("03-rag", "03", "RAG & retrieval",
     "Grounding models in your data — and proving they actually used it.",
     ["rag-architecture", "retrieval-evals"]),
    ("04-evals-observability", "04", "Evals & observability",
     "You cannot operate what you cannot measure.",
     ["evals", "observability", "cost-attribution"]),
    ("05-safety-multitenancy", "05", "Safety & multi-tenancy",
     "Keeping tenants, users, and data from leaking into each other.",
     ["safety-engineering", "multi-tenant-isolation"]),
    ("06-strategy-tradeoffs", "06", "Strategy & tradeoffs",
     "Picking the right tool, and naming the cost of every choice.",
     ["finetune-vs-icl-vs-rag", "inference-stack-tradeoffs", "production-failure-modes"]),
]
SLUG_TO_PAGE = {m[0]: f"{m[0]}.html" for m in MODULES}

# ---- link rewriting -----------------------------------------------------------
def rewrite_target(target, cur_mod):
    """Rewrite a markdown link target (relative) to the HTML site."""
    if target.startswith(("http://", "https://", "mailto:")):
        return target
    if target.startswith("#"):
        return target
    base, _, frag = target.partition("#")
    anchor = ("#" + frag) if frag else ""
    resolved = os.path.normpath(os.path.join("content", cur_mod, base))
    resolved = resolved.replace("\\", "/")
    if resolved in ("README.md", "SUMMARY.md", "GLOSSARY.md"):
        return "index.html"
    m = re.match(r"content/(\d\d-[\w-]+)/(.+)$", resolved)
    if m:
        mod, fname = m.group(1), m.group(2)
        if fname == "README.md":
            return SLUG_TO_PAGE.get(mod, "index.html")
        lesson = fname[:-3] if fname.endswith(".md") else fname
        if mod == cur_mod:
            return f"#{lesson}"
        return f"{SLUG_TO_PAGE.get(mod, 'index.html')}#{lesson}"
    # cross-track link into a sibling track. AI editions live at _site/ai/, so a
    # single ../ climbs to the site root where the other tracks sit. Flat tracks
    # flatten to one page per lesson; phased tracks (harness, flowable) keep their tree.
    FLAT = ("agentic-ai", "first-principles", "product-sense",
            "technical-product-sense", "technical-product-management", "knowledge-graphs",
            "system-design", "rag-vector-databases", "generative-ai", "llms",
            "api-integrations", "memory-and-context", "tool-calling", "ai-agents",
            "agentic-workflows", "evaluation-and-observability", "ai-security-and-guardrails",
            "cost-optimization", "access-control", "context-engineering", "prompt-engineering",
            "learning-paths")
    PHASED = {"harness-engineering": "harness", "flowable": "flowable"}
    top, _, rest = resolved.partition("/")
    if rest.endswith(".md"):
        rest = rest[:-3]
        if top in FLAT:
            leaf = rest.rsplit("/", 1)[-1]
            page = "index" if leaf == "README" else leaf
            return f"../{top}/{page}.html{anchor}"
        if top in PHASED:
            if rest == "README":
                return f"../{PHASED[top]}/index.html{anchor}"
            return f"../{PHASED[top]}/{rest}.html{anchor}"
    return target  # leave anything unexpected alone

def rewrite_links_in_md(md, cur_mod):
    def repl(m):
        text, target = m.group(1), m.group(2).strip()
        return f"[{text}]({rewrite_target(target, cur_mod)})"
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, md)

_MARKER = re.compile(r"^([-*+]\s+|\d+\.\s+)")
def ensure_blank_before_lists(md):
    """CommonMark lets a bullet list interrupt a paragraph; python-markdown does
    not. Insert the blank line a col-0 list needs when it follows a col-0
    non-list line (e.g. a bold '**Properties:**' lead-in)."""
    out, in_fence = [], False
    for line in md.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line); continue
        if not in_fence and _MARKER.match(line) and out:
            prev = out[-1]
            if prev.strip() and not prev[:1].isspace() and not _MARKER.match(prev):
                out.append("")
        out.append(line)
    return "\n".join(out)

# ---- markdown -> styled html fragment -----------------------------------------
def convert_lesson(md, cur_mod):
    # strip the "*Part of [..](./README.md)*" breadcrumb line (redundant in HTML)
    lines = [l for l in md.split("\n") if not l.strip().startswith("*Part of ")]
    md = "\n".join(lines)
    md = rewrite_links_in_md(md, cur_mod)
    # drop the leading H1 (lesson title is rendered by the section header)
    md = re.sub(r"\A\s*#\s+.*\n", "", md, count=1)
    md = ensure_blank_before_lists(md)
    body = markdown.markdown(
        md, extensions=["tables", "fenced_code", "sane_lists", "attr_list", "toc"]
    )
    # PM callout: tag the blockquote that holds the PM briefing
    body = re.sub(
        r"<blockquote>(.*?For the AI-native PM.*?)</blockquote>",
        r'<blockquote class="pm-callout">\1</blockquote>',
        body, flags=re.DOTALL,
    )
    # task-list checkboxes
    body = re.sub(r"<li>\[ \]\s*", '<li class="task todo">', body)
    body = re.sub(r"<li>\[x\]\s*", '<li class="task done">', body)
    return body

# ---- "on this page" outline (right rail) --------------------------------------
# The "toc" extension gives every h2/h3 a slugified id; pull those out to build a
# sticky, scroll-spy outline of a single lesson page's own sections.
_HEAD_RE = re.compile(r'<h([23])\s+id="([^"]+)"[^>]*>(.*?)</h\1>', re.DOTALL)

def extract_outline(body_html):
    heads = []
    for level, hid, text in _HEAD_RE.findall(body_html):
        heads.append((int(level), hid, re.sub(r"<[^>]+>", "", text).strip()))
    return heads

def render_outline(heads):
    if len(heads) < 2:
        return "", False
    rows = "".join(
        f'<a class="{"h3" if lvl == 3 else "h2"}" href="#{hid}">{htmllib.escape(t)}</a>'
        for lvl, hid, t in heads
    )
    html = (f'<aside class="outline"><div class="sticky">'
            f'<div class="outline-h">On this page</div>{rows}</div></aside>')
    return html, True

OUTLINE_SCRIPT = """<script>
(function(){
  var links = document.querySelectorAll('.outline a');
  if(!links.length) return;
  var heads = [];
  links.forEach(function(a){
    var el = document.getElementById(a.getAttribute('href').slice(1));
    if(el) heads.push({el:el, link:a});
  });
  if(!heads.length) return;
  function onScroll(){
    var y = window.scrollY + 130, current = heads[0];
    heads.forEach(function(h){ if(h.el.offsetTop <= y) current = h; });
    links.forEach(function(a){ a.classList.remove('active'); });
    current.link.classList.add('active');
  }
  document.addEventListener('scroll', onScroll, {passive:true});
  onScroll();
})();
</script>"""

def lesson_title(md):
    m = re.search(r"\A\s*#\s+(.*)", md)
    return m.group(1).strip() if m else "Lesson"

# ---- page chrome --------------------------------------------------------------
SPARK = ('<svg class="spark" viewBox="0 0 100 100" width="22" height="22" aria-hidden="true">'
         '<path d="M50 8 L58 42 L92 50 L58 58 L50 92 L42 58 L8 50 L42 42 Z" fill="currentColor"/></svg>')

def head(title, depth_note=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{htmllib.escape(title)}</title>
</head>
<body>"""


def topbar(with_menu=False):
    links = "".join(
        f'<a class="Button" data-variant="ghost" data-color="secondary" data-size="sm" data-pill '
        f'href="{SLUG_TO_PAGE[s]}"><span class="ButtonInner">{num}</span></a>' for (s, num, *_ ) in MODULES
    )
    menu_btn = ('<button class="Button menu-btn" id="sbToggle" data-variant="ghost" data-color="secondary" '
                'data-size="lg" data-uniform data-pill aria-expanded="false" aria-controls="sbNav" '
                'aria-label="Open module menu"><span class="ButtonInner">'+ds.MENU_ICON+'</span></button>') if with_menu else ""
    scrim = '<div id="sb-scrim"></div>' if with_menu else ""
    return f"""<header class="topbar">
  {menu_btn}<a class="brand" href="index.html">{SPARK}<span>AI&nbsp;engineering</span><em>for AI-native PMs</em></a>
  <nav class="topnav">{links}</nav>
</header>{scrim}"""

def sidebar(cur_mod, nav_items):
    items = []
    for (slug, num, title, _desc, _lessons) in MODULES:
        active = " active" if slug == cur_mod else ""
        sub = ""
        if slug == cur_mod and nav_items:
            sub_items = "".join(
                f'<a href="#{anchor}">{htmllib.escape(t)}</a>' for anchor, t in nav_items
            )
            sub = f'<div class="sub">{sub_items}</div>'
        items.append(
            f'<a class="modlink{active}" href="{SLUG_TO_PAGE[slug]}">'
            f'<span class="num">{num}</span>{htmllib.escape(title)}</a>{sub}'
        )
    return f'<aside class="sidebar" id="sbNav"><div class="sticky">{"".join(items)}</div></aside>'

SIDEBAR_TOGGLE_JS = """<script>
(function(){
  var btn=document.getElementById('sbToggle'), nav=document.getElementById('sbNav'),
      scrim=document.getElementById('sb-scrim');
  if(!btn||!nav) return;
  function open(){nav.classList.add('open');if(scrim)scrim.classList.add('open');btn.setAttribute('aria-expanded','true')}
  function close(){nav.classList.remove('open');if(scrim)scrim.classList.remove('open');btn.setAttribute('aria-expanded','false')}
  btn.addEventListener('click',function(){nav.classList.contains('open')?close():open()});
  if(scrim)scrim.addEventListener('click',close);
  document.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
  nav.addEventListener('click',function(e){if(e.target.closest('a'))close()});
})();
</script>"""

def footer(prev_mod, next_mod):
    def card(mod, dir_):
        if not mod:
            return "<span></span>"
        slug, num, title, *_ = mod
        arrow = "←" if dir_ == "prev" else "→"
        label = "Previous" if dir_ == "prev" else "Next"
        return (f'<a class="navcard {dir_}" href="{SLUG_TO_PAGE[slug]}">'
                f'<span class="lbl">{arrow} {label}</span>'
                f'<span class="ttl">{num} · {htmllib.escape(title)}</span></a>')
    return (f'<div class="pagenav">{card(prev_mod,"prev")}{card(next_mod,"next")}</div>'
            '<footer class="foot">Educational content · part of the '
            '<a href="index.html">AI engineering</a> curriculum for AI-native PMs.</footer>')

# ---- build one module page ----------------------------------------------------
def build_module(idx):
    slug, num, title, desc, lessons = MODULES[idx]
    folder = os.path.join(CONTENT, slug)
    # module intro (README) — convert, drop nav arrows line
    with open(os.path.join(folder, "README.md")) as f:
        readme = f.read()
    readme = "\n".join(
        l for l in readme.split("\n")
        if not l.strip().startswith("←") and not l.strip().startswith("→ Next")
        and not l.strip().startswith("↩")
    )
    readme = re.sub(r"\A\s*#\s+.*\n", "", readme, count=1)  # drop H1
    intro_html = markdown.markdown(
        ensure_blank_before_lists(rewrite_links_in_md(readme, slug)),
        extensions=["tables", "fenced_code", "sane_lists"])

    lessons_meta, sections = [], []
    for i, lid in enumerate(lessons, 1):
        with open(os.path.join(folder, f"{lid}.md")) as f:
            md = f.read()
        t = lesson_title(md)
        lessons_meta.append((lid, t))
        body = convert_lesson(md, slug)
        sections.append(
            f'<section class="lesson MarkdownContent" id="{lid}">'
            f'<div class="lesson-head">{ds.badge(f"{num}.{i}", size="lg")}'
            f'<h2>{htmllib.escape(t)}</h2></div>{body}'
            f'<a class="totop" href="#top">↑ back to top</a></section>'
        )

    prev_mod = MODULES[idx-1] if idx > 0 else None
    next_mod = MODULES[idx+1] if idx < len(MODULES)-1 else None

    # interactive widget + recap
    iw = INTERACTIVES.get(slug)
    iw_html, iw_js = ("", "")
    if iw:
        iw_html = (f'<section class="interactive" id="interactive">'
                   f'<div class="iw-head">{ds.badge("Interactive", color="info", size="md")}'
                   f'<h3>{htmllib.escape(iw["title"])}</h3></div>'
                   f'<div class="iw-body">{iw["html"]}</div></section>')
        iw_js = f"<script>{iw['js']}</script>"

    recap_html = ""
    recap_path = os.path.join(folder, "recap.md")
    if os.path.exists(recap_path):
        with open(recap_path) as f:
            rmd = f.read()
        recap_body = convert_lesson(rmd, slug)
        recap_html = (f'<section class="recap MarkdownContent" id="recap">'
                      f'<div class="recap-head"><span class="recap-ic">📌</span>'
                      f'<h2>Recap &amp; real-world examples</h2></div>{recap_body}'
                      f'<a class="totop" href="#top">↑ back to top</a></section>')

    # nav items (sidebar sub-list + TOC)
    nav_items = []
    if iw_html:
        nav_items.append(("interactive", "◆ Interactive demo"))
    nav_items += lessons_meta
    if recap_html:
        nav_items.append(("recap", "Recap & examples"))

    toc_rows = ""
    if iw_html:
        toc_rows += '<a href="#interactive"><span>◆</span>Interactive demo</a>'
    toc_rows += "".join(
        f'<a href="#{lid}"><span>{num}.{i}</span>{htmllib.escape(t)}</a>'
        for i, (lid, t) in enumerate(lessons_meta, 1)
    )
    if recap_html:
        toc_rows += '<a href="#recap"><span>📌</span>Recap &amp; real-world examples</a>'

    page = head(f"{num} · {title} — AI engineering for PMs")
    page += topbar(with_menu=True)
    page += '<div class="layout">'
    page += sidebar(slug, nav_items)
    page += f"""<main class="content" id="top">
  <div class="hero">
    {ds.badge(f"Module {num}", size="lg", pill=True)}
    <h1>{htmllib.escape(title)}</h1>
    <p class="lede">{htmllib.escape(desc)}</p>
    <div class="hero-meta">{len(lessons)} lessons · interactive demo · every lesson includes a
      <strong>🎯 For the AI-native PM</strong> briefing</div>
  </div>
  <div class="intro MarkdownContent">{intro_html}</div>
  <nav class="toc"><div class="toc-h">In this module</div>{toc_rows}</nav>
  {iw_html}
  {''.join(sections)}
  {recap_html}
  {footer(prev_mod, next_mod)}
  </main></div>{SIDEBAR_TOGGLE_JS}{iw_js}</body></html>"""
    with open(os.path.join(OUT, SLUG_TO_PAGE[slug]), "w") as f:
        f.write(reader_widget.inject(page))

# ---- build the landing index --------------------------------------------------
def build_index():
    cards = []
    for (slug, num, title, desc, lessons) in MODULES:
        lis = "".join(f"<li>{htmllib.escape(l.replace('-', ' '))}</li>" for l in lessons[:3])
        more = f"<li class='more'>+{len(lessons)-3} more…</li>" if len(lessons) > 3 else ""
        cards.append(f"""<a class="card" href="{SLUG_TO_PAGE[slug]}">
        {ds.badge(num, size="md")}
        <h3>{htmllib.escape(title)}</h3>
        <p>{htmllib.escape(desc)}</p>
        <ul>{lis}{more}</ul>
        <span class="card-iw">◆ interactive demo + recap</span>
        <span class="card-go">Open module →</span></a>""")

    threads = [
        ("💰 Caching &amp; cost", "How spend and latency hide in the inference layer — and how a cache can become a privacy incident."),
        ("🛡️ Reliability", "From valid JSON to bounded agents: making stochastic output safe for downstream systems."),
        ("⚡ Latency", "Why “it feels slow” has two different causes, and which lever fixes which."),
        ("🎯 Quality", "Context → retrieval → grounding → evals: where trustworthy answers actually come from."),
        ("🧰 Which tool?", "Fine-tune vs. ICL vs. RAG vs. distillation — the highest-leverage early decision."),
    ]
    thread_html = "".join(
        f'<div class="thread"><div class="thread-t">{t}</div><p>{d}</p></div>'
        for t, d in threads
    )

    page = head("AI engineering — a curriculum for AI-native PMs")
    page += topbar()
    page += f"""<main class="content index" id="top">
  <div class="index-hero">
    {ds.badge("A linked curriculum", size="lg", pill=True)}
    <h1>AI engineering,<br/><em>from scratch to production.</em></h1>
    <p class="lede">The engineering discipline underneath production LLM systems —
      inference, retrieval, evaluation, observability, safety, and cost — taught through
      the lens of the decisions a <strong>Senior or Principal PM</strong> has to make.</p>
    <div class="index-meta">{"".join(ds.badge(t, size="lg", pill=True) for t in ("7 modules", "23 lessons", "PM-native", "production-grade"))}</div>
  </div>

  <div class="pm-band">{ds.alert("🎯 Built for the AI-native PM", "Every lesson pairs the real mechanics with a briefing: why it matters to the product, what it changes in your decisions, the question to ask your eng team, and the product risk if you ignore it.", color="primary", icon=False)}</div>

  <h2 class="sec">The modules</h2>
  <div class="cards">{''.join(cards)}</div>

  <h2 class="sec">Threads — follow one concern across the whole stack</h2>
  <div class="threads">{thread_html}</div>

  <footer class="foot">Educational content. Use it, fork it, teach from it.</footer>
  </main></body></html>"""
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(reader_widget.inject(page))

INTERACTIVES = {
# ---------------------------------------------------------------- module 00
"00-foundations": {
 "title": "Harness vs. prompt — what catches a bad model call?",
 "html": r'''<p class="iw-note" style="margin-top:0">The model is one fast, unreliable function call. Watch what the <strong>harness</strong> around it does when the model misbehaves — and what happens without it.</p>
<div class="iw-btns">
  <button class="Button" data-variant="solid" data-color="primary" data-size="sm" data-pill id="hz-good">▶ Run a good call</button>
  <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill id="hz-bad">▶ Run a bad call (model returns garbage)</button>
  <label class="iw-toggle" style="margin-left:6px"><input type="checkbox" id="hz-harness" checked> Harness enabled</label>
</div>
<div class="iw-stages" id="hz-stages"></div>
<div class="iw-out"><div class="iw-verdict" id="hz-verdict">Ready.</div><div class="iw-note" id="hz-detail">Pick a scenario above.</div></div>''',
 "js": r'''(function(){var root=document.getElementById('interactive');
var stagesEl=root.querySelector('#hz-stages'),verdict=root.querySelector('#hz-verdict'),detail=root.querySelector('#hz-detail'),harness=root.querySelector('#hz-harness');
function render(st){stagesEl.innerHTML='';st.forEach(function(s,i){if(i){var a=document.createElement('span');a.className='iw-arrow';a.textContent='→';stagesEl.appendChild(a);}var d=document.createElement('span');d.className='iw-stage '+s.cls;d.textContent=s.label;stagesEl.appendChild(d);});}
function run(bad){var on=harness.checked,st=[];
if(on){st.push({label:'Assemble context',cls:'on'});st.push({label:'Model call',cls:bad?'kill':'on'});st.push({label:'Validate',cls:'on'});if(bad)st.push({label:'Repair loop',cls:'on'});st.push({label:'Tools (idempotent)',cls:'on'});st.push({label:'Budgets',cls:'on'});st.push({label:'Response',cls:'on'});
if(bad){verdict.innerHTML='<span class="iw-good">✅ Caught &amp; repaired</span>';detail.textContent='The model returned malformed output — Validate flagged it, the bounded repair loop fixed it, and a clean, schema-valid result reached the user. Worst case, the fallback chain returns a typed error — never a crash.';}
else{verdict.innerHTML='<span class="iw-good">✅ Valid response delivered</span>';detail.textContent='Every stage did its job. The same path is what protects you on the calls that go wrong.';}}
else{st.push({label:'Assemble context',cls:'on'});st.push({label:'Model call',cls:bad?'kill':'on'});st.push({label:'Response',cls:bad?'kill':'on'});
if(bad){verdict.innerHTML='<span class="iw-bad">💥 Broken output reaches the user</span>';detail.textContent='No validation, no repair, no fallback. The garbage flows straight through — the JSON fails to parse downstream and the workflow breaks. This is the demo that wowed on stage and pages you at 2am.';}
else{verdict.innerHTML='<span class="iw-good">✅ Worked… this time</span>';detail.textContent='With no harness it is fine until the first bad call. Your reliability is just whatever the model happened to do.';}}
render(st);}
root.querySelector('#hz-good').onclick=function(){run(false);};root.querySelector('#hz-bad').onclick=function(){run(true);};harness.onchange=function(){run(false);};run(false);})();''',
},
# ---------------------------------------------------------------- module 01
"01-inference-internals": {
 "title": "Latency & cost playground — prefill vs. decode",
 "html": r'''<div class="iw-controls">
  <div class="iw-field"><label>Input tokens <span class="v" id="lc-inv"></span></label><input type="range" id="lc-in" min="0" max="32000" step="500" value="3000"></div>
  <div class="iw-field"><label>Output tokens <span class="v" id="lc-outv"></span></label><input type="range" id="lc-out" min="0" max="4000" step="50" value="300"></div>
  <div class="iw-field"><label>Cached prefix <span class="v" id="lc-cv"></span></label><input type="range" id="lc-cache" min="0" max="100" step="5" value="0"></div>
</div>
<div class="iw-btns">
  <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-p="rag">Long input · short answer</button>
  <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-p="chat">Chatbot reply</button>
  <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-p="agent">Cached agent step</button>
</div>
<div class="iw-out">
  <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:5px"><strong>Latency</strong><span class="v" id="lc-total"></span></div>
  <div class="iw-stack" id="lc-stack"><span id="lc-pre" style="background:var(--color-background-info-solid)"></span><span id="lc-dec" style="background:var(--color-background-success-solid)"></span></div>
  <div class="iw-legend"><span><i style="background:var(--color-background-info-solid)"></i>Prefill (input) <span class="v" id="lc-prems"></span></span><span><i style="background:var(--color-background-success-solid)"></i>Decode (output) <span class="v" id="lc-decms"></span></span></div>
  <div class="iw-metric" style="margin-top:14px"><span class="ml">Cost / request</span><span class="mv" id="lc-cost"></span></div>
  <div class="iw-note" id="lc-note"></div>
</div>
<div class="iw-note">Illustrative model: ~60&nbsp;ms per 1k input tokens (prefill), 12&nbsp;ms per output token (decode), $3 / $15 per Mtok in/out, cached input at 10% price. Your real numbers vary by model &amp; hardware — the <em>shape</em> is the lesson.</div>''',
 "js": r'''(function(){var root=document.getElementById('interactive');
var $=function(id){return root.querySelector(id);};
var inEl=$('#lc-in'),outEl=$('#lc-out'),cacheEl=$('#lc-cache');
function calc(){var i=+inEl.value,o=+outEl.value,c=+cacheEl.value/100;
var unc=i*(1-c);var prefill=unc/1000*60+ (i>0?40:0);var decode=o*12;var total=prefill+decode||1;
var cost=unc/1e6*3 + (i*c)/1e6*0.3 + o/1e6*15;
$('#lc-inv').textContent=i.toLocaleString();$('#lc-outv').textContent=o.toLocaleString();$('#lc-cv').textContent=(c*100)+'%';
$('#lc-pre').style.width=(prefill/total*100)+'%';$('#lc-dec').style.width=(decode/total*100)+'%';
$('#lc-total').textContent=(total/1000).toFixed(2)+' s';
$('#lc-prems').textContent=Math.round(prefill)+' ms';$('#lc-decms').textContent=Math.round(decode)+' ms';
$('#lc-cost').textContent='$'+cost.toFixed(4);
var note;if(prefill>decode*1.4)note='<strong>Prefill-dominated.</strong> Your latency is mostly the input. Biggest wins: shorter/compressed context and <em>prompt caching</em> — try the cached slider.';
else if(decode>prefill*1.4)note='<strong>Decode-dominated.</strong> Your latency is mostly generation. Biggest wins: speculative decoding, a smaller/quantized model, more bandwidth.';
else note='<strong>Balanced.</strong> Both phases matter — measure TTFT and TPOT separately before optimizing.';
$('#lc-note').innerHTML=note;}
var presets={rag:[15000,25,0],chat:[700,800,0],agent:[12000,150,80]};
root.querySelectorAll('[data-p]').forEach(function(b){b.onclick=function(){var p=presets[b.dataset.p];inEl.value=p[0];outEl.value=p[1];cacheEl.value=p[2];root.querySelectorAll('[data-p]').forEach(function(x){x.removeAttribute('data-selected');});b.setAttribute('data-selected','');calc();};});
[inEl,outEl,cacheEl].forEach(function(e){e.oninput=function(){root.querySelectorAll('[data-p]').forEach(function(x){x.removeAttribute('data-selected');});calc();};});
calc();})();''',
},
# ---------------------------------------------------------------- module 02
"02-reliable-outputs": {
 "title": "Agent budget simulator — what stops a runaway?",
 "html": r'''<div class="iw-controls">
 <div class="iw-field"><label>Max steps (budget) <span class="v" id="ab-msv"></span></label><input type="range" id="ab-ms" min="2" max="30" step="1" value="8"></div>
 <div class="iw-field"><label>Cost ceiling <span class="v" id="ab-ccv"></span></label><input type="range" id="ab-cc" min="20" max="500" step="10" value="100"></div>
 <div class="iw-field"><label>Task difficulty <span class="v" id="ab-dv"></span></label><input type="range" id="ab-d" min="5" max="60" step="5" value="25"></div>
</div>
<div class="iw-btns">
 <label class="iw-toggle"><input type="checkbox" id="ab-g" checked> Guardrails (budgets + no-progress)</label>
 <button class="Button" data-variant="solid" data-color="primary" data-size="sm" data-pill id="ab-run">▶ Run agent</button>
</div>
<div class="iw-out">
 <div class="iw-stages" id="ab-tl"></div>
 <div class="iw-verdict" id="ab-verdict" style="margin-top:10px">Press “Run agent”.</div>
 <div class="iw-note" id="ab-detail">Each step costs ~8¢ and makes a tool call. Difficulty = chance of finishing per step.</div>
</div>''',
 "js": r'''(function(){var root=document.getElementById('interactive');var $=function(id){return root.querySelector(id);};
var ms=$('#ab-ms'),cc=$('#ab-cc'),d=$('#ab-d'),g=$('#ab-g');
function lbl(){$('#ab-msv').textContent=ms.value;$('#ab-ccv').textContent='$'+(+cc.value/100).toFixed(2);$('#ab-dv').textContent=d.value+'%';}
[ms,cc,d].forEach(function(e){e.oninput=lbl;});lbl();
function run(){var guard=g.checked,maxSteps=+ms.value,ceil=+cc.value,diff=+d.value/100,stepC=8;
var hard=50,cost=0,steps=0,reps=0,tl=[],reason='',cls='';
while(steps<hard){steps++;cost+=stepC;var r=Math.random();
if(r<diff){tl.push({label:'✓ '+steps,cls:'on'});reason='success';break;}
if(r>0.82){reps++;tl.push({label:'↻ '+steps,cls:'kill'});}else{reps=0;tl.push({label:'· '+steps,cls:'on'});}
if(guard){if(reps>=3){reason='noprogress';break;}if(cost>ceil){reason='cost';break;}if(steps>=maxSteps){reason='steps';break;}}}
if(!reason)reason='hardcap';
var el=$('#ab-tl');el.innerHTML='';tl.forEach(function(s){var x=document.createElement('span');x.className='iw-stage '+s.cls;x.textContent=s.label;el.appendChild(x);});
var v=$('#ab-verdict'),det=$('#ab-detail'),C='$'+(cost/100).toFixed(2);
if(reason==='success'){v.innerHTML='<span class="iw-good">✅ Completed in '+steps+' steps · '+C+'</span>';det.textContent='The task converged before any budget was hit. Guardrails were never needed here — but they are what makes the bad runs safe.';}
else if(reason==='steps'){v.innerHTML='<span class="iw-bad">⛔ Hit step budget ('+maxSteps+') · '+C+'</span>';det.textContent='The loop budget fired. The agent returns its best partial result or escalates to a human — bounded, predictable, no runaway.';}
else if(reason==='cost'){v.innerHTML='<span class="iw-bad">⛔ Hit cost ceiling · '+C+'</span>';det.textContent='Spend crossed the ceiling, so the agent stopped. This is what turns “bill shock” into a known, capped number.';}
else if(reason==='noprogress'){v.innerHTML='<span class="iw-bad">🔁 No-progress detector fired · '+C+'</span>';det.textContent='Three repeated/looping actions in a row — the detector broke the loop instead of letting it run to the cap.';}
else{v.innerHTML='<span class="iw-bad">💥 No guardrails: ran '+steps+' steps · '+C+'</span>';det.textContent='With guardrails off there is no termination logic — the agent thrashed to the hard ceiling, burning cost with nothing to stop it. This is the runaway-agent incident.';}}
$('#ab-run').onclick=run;})();''',
},
# ---------------------------------------------------------------- module 03
"03-rag": {
 "title": "Retrieval tradeoff — top-k and reranking",
 "html": r'''<div class="iw-controls">
 <div class="iw-field"><label>Retrieved (top-k) <span class="v" id="rg-kv"></span></label><input type="range" id="rg-k" min="1" max="50" step="1" value="8"></div>
 <label class="iw-toggle" style="margin-bottom:7px"><input type="checkbox" id="rg-rr"> Add reranking (keep top 5)</label>
</div>
<div class="iw-grid" id="rg-grid"></div>
<div class="iw-out">
 <div class="iw-metric"><span class="ml">Recall@k</span><span class="iw-track"><span class="iw-fill" id="rg-rcf"></span></span><span class="mv" id="rg-rc"></span></div>
 <div class="iw-metric"><span class="ml">Precision@k</span><span class="iw-track"><span class="iw-fill" id="rg-prf" style="background:var(--color-background-success-solid)"></span></span><span class="mv" id="rg-pr"></span></div>
 <div class="iw-metric"><span class="ml">Context tokens</span><span class="mv" id="rg-tok"></span></div>
 <div class="iw-note" id="rg-note"></div>
</div>
<div class="iw-legend"><span><i style="background:var(--color-background-info-solid)"></i>relevant</span><span><i style="background:var(--color-background-primary-soft-alpha)"></i>noise</span><span><i style="background:var(--color-surface);outline:2px solid var(--color-text)"></i>kept after rerank</span></div>''',
 "js": r'''(function(){var root=document.getElementById('interactive');var $=function(id){return root.querySelector(id);};
var R=8,k=$('#rg-k'),rr=$('#rg-rr');
function calc(){var K=+k.value,rerank=rr.checked;
var found=Math.round(R*(1-Math.exp(-K/12)));if(found>K)found=K;
var keep=rerank?Math.min(5,K):K;var keptRel=rerank?Math.min(keep,found):found;
var recall=found/R;var precision=(rerank?keptRel/keep:found/K);var tokens=keep*250;
$('#rg-kv').textContent=K;$('#rg-rc').textContent=Math.round(recall*100)+'%';$('#rg-pr').textContent=Math.round(precision*100)+'%';
$('#rg-rcf').style.width=(recall*100)+'%';$('#rg-prf').style.width=(precision*100)+'%';
$('#rg-tok').textContent=tokens.toLocaleString()+' tok';
var grid=$('#rg-grid');grid.innerHTML='';var order=[];for(var i=0;i<K;i++)order.push(i<found);
if(rerank)order.sort(function(a,b){return (b?1:0)-(a?1:0);});
order.forEach(function(isRel,i){var c=document.createElement('span');c.className='iw-chunk'+(isRel?' rel':'');if(rerank&&i<keep)c.className+=' kept';grid.appendChild(c);});
var note;if(rerank)note='<strong>Reranked.</strong> You still retrieved widely (recall held), but kept only the few best chunks — precision jumps, context shrinks, the generator is less distracted, and you pay fewer tokens.';
else if(K<=4)note='<strong>Low k.</strong> Precision is high but you may miss relevant chunks — recall is the ceiling on the whole system.';
else if(K>=18)note='<strong>High k, no rerank.</strong> Recall is near-max but precision craters — the answer is buried in noise and you pay for junk tokens. This is “lost in the middle.”';
else note='<strong>Mid k.</strong> Reasonable — but turn on reranking to get high recall <em>and</em> high precision at once.';
$('#rg-note').innerHTML=note;}
k.oninput=calc;rr.onchange=calc;calc();})();''',
},
# ---------------------------------------------------------------- module 04
"04-evals-observability": {
 "title": "Trace waterfall — one request, span by span",
 "html": r'''<div class="iw-btns">
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-selected data-s="healthy">Healthy</button>
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-s="slow">Slow retrieval</button>
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-s="repair">Repair loop</button>
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-s="timeout">Tool timeout</button>
</div>
<div id="tr-rows" style="margin:8px 0 4px"></div>
<div class="iw-out" style="display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap">
 <div><div style="font-size:12px;color:var(--color-text-secondary)">Total latency</div><div class="mv" id="tr-lat"></div></div>
 <div><div style="font-size:12px;color:var(--color-text-secondary)">Total cost</div><div class="mv" id="tr-cost"></div></div>
 <div><div style="font-size:12px;color:var(--color-text-secondary)">Tokens in/out</div><div class="mv" id="tr-tok"></div></div>
 <div style="flex:1;min-width:180px"><div style="font-size:12px;color:var(--color-text-secondary)">Selected span</div><div class="iw-note" id="tr-sel" style="margin-top:2px">Click a span to inspect tokens, latency &amp; cost.</div></div>
</div>''',
 "js": r'''(function(){var root=document.getElementById('interactive');var $=function(id){return root.querySelector(id);};
var SC={
healthy:{lat:1040,cost:0.0046,tok:'3,100 / 180',spans:[['retrieve',0,42,'8 chunks · vector+BM25',false],['rerank',42,18,'kept 3 of 8',false],['model.generate',60,900,'ttft 210ms · 180 out tok · $0.0042',false],['validate',960,4,'schema OK · 0 repairs',false],['tool.create_note',964,76,'idempotent · 200 OK',false]]},
slow:{lat:1680,cost:0.0048,tok:'3,100 / 180',spans:[['retrieve',0,690,'cold index · 690ms (!)',true],['rerank',690,18,'kept 3 of 8',false],['model.generate',708,900,'ttft 210ms · 180 out tok',false],['validate',1608,4,'schema OK',false],['tool.create_note',1612,68,'200 OK',false]]},
repair:{lat:1890,cost:0.0079,tok:'3,100 / 410',spans:[['retrieve',0,42,'8 chunks',false],['rerank',42,18,'kept 3',false],['model.generate',60,900,'180 tok · returned malformed JSON',true],['validate',960,5,'✗ missing field “priority”',true],['model.generate#2',965,840,'repair · 190 tok · valid',false],['validate#2',1805,4,'schema OK',false],['tool.create_note',1809,80,'200 OK',false]]},
timeout:{lat:4120,cost:0.0050,tok:'3,100 / 180',spans:[['retrieve',0,42,'8 chunks',false],['rerank',42,18,'kept 3',false],['model.generate',60,900,'180 tok',false],['validate',960,4,'schema OK',false],['tool.create_note',964,3000,'⏱ timeout 3s → fallback',true]]}};
function render(key){var s=SC[key],max=s.lat,rows=$('#tr-rows');rows.innerHTML='';
s.spans.forEach(function(sp){var row=document.createElement('div');row.className='iw-span';
var name=document.createElement('span');name.className='sn';name.textContent=sp[0];
var wrap=document.createElement('span');wrap.className='iw-spanbar-wrap';
var bar=document.createElement('span');bar.className='iw-spanbar';bar.style.left=(sp[1]/max*100)+'%';bar.style.width=Math.max(1.2,sp[2]/max*100)+'%';if(sp[4])bar.style.background='var(--color-background-danger-solid)';
wrap.appendChild(bar);row.appendChild(name);row.appendChild(wrap);
row.onclick=function(){rows.querySelectorAll('.iw-span').forEach(function(x){x.classList.remove('sel');});row.classList.add('sel');
$('#tr-sel').innerHTML='<strong>'+sp[0]+'</strong> · '+sp[2]+' ms — '+sp[3];};
rows.appendChild(row);});
$('#tr-lat').textContent=(s.lat/1000).toFixed(2)+' s';$('#tr-cost').textContent='$'+s.cost.toFixed(4);$('#tr-tok').textContent=s.tok;
$('#tr-sel').innerHTML='Click a span to inspect tokens, latency &amp; cost.';}
root.querySelectorAll('[data-s]').forEach(function(b){b.onclick=function(){root.querySelectorAll('[data-s]').forEach(function(x){x.removeAttribute('data-selected');});b.setAttribute('data-selected','');render(b.dataset.s);};});
render('healthy');})();''',
},
# ---------------------------------------------------------------- module 05
"05-safety-multitenancy": {
 "title": "The lethal trifecta — and cache safety",
 "html": r'''<p class="iw-note" style="margin-top:0">An agent is exploitable for data <strong>exfiltration</strong> only when it has all three legs. Break any one and the whole attack class is defused.</p>
<div class="iw-btns">
 <label class="iw-toggle"><input type="checkbox" id="lt-a" checked> ① Reads untrusted content</label>
 <label class="iw-toggle"><input type="checkbox" id="lt-b" checked> ② Can access private data</label>
 <label class="iw-toggle"><input type="checkbox" id="lt-c" checked> ③ Can communicate externally</label>
</div>
<div class="iw-out"><div class="iw-verdict" id="lt-v"></div><div class="iw-note" id="lt-d"></div></div>
<hr>
<p class="iw-note" style="margin-top:0"><strong>Bonus — cache safety.</strong> A semantic cache keyed only on the query text leaks answers across tenants.</p>
<label class="iw-toggle"><input type="checkbox" id="lt-k" checked> Cache key includes tenant&nbsp;+&nbsp;permission scope</label>
<div class="iw-out" style="margin-top:10px"><div class="iw-verdict" id="lt-kv"></div></div>''',
 "js": r'''(function(){var root=document.getElementById('interactive');var $=function(id){return root.querySelector(id);};
var a=$('#lt-a'),b=$('#lt-b'),c=$('#lt-c'),k=$('#lt-k');
var legs=[['① reads untrusted content','stop feeding it untrusted/retrieved content (or sandbox what it reads)'],['② accesses private data','remove its access to sensitive data for this path'],['③ can communicate externally','remove its outbound channel / egress, or require human approval to send']];
function trifecta(){var on=[a.checked,b.checked,c.checked],n=on.filter(Boolean).length,v=$('#lt-v'),d=$('#lt-d');
if(n===3){v.innerHTML='<span class="iw-bad">⚠ Data exfiltration possible</span>';d.innerHTML='All three legs present: a poisoned document or email can instruct the agent to read private data and send it out — the user never typed anything malicious. <strong>Break one leg below.</strong>';}
else{var broken=[];on.forEach(function(o,i){if(!o)broken.push(legs[i][1]);});
v.innerHTML='<span class="iw-good">✓ Contained</span>';d.innerHTML='With only '+n+' of 3 legs, the exfiltration path is broken. You’ve mitigated by: <em>'+broken.join('; ')+'</em>. This is why permission boundaries live in code, not the prompt.';}}
function cache(){var v=$('#lt-kv');if(k.checked){v.innerHTML='<span class="iw-good">✓ Isolated</span> — identical questions from two tenants are different cache entries. No cross-tenant leak.';}
else{v.innerHTML='<span class="iw-bad">⚠ Cross-tenant leak</span> — Tenant&nbsp;B asks a similar question and receives Tenant&nbsp;A’s cached answer (and data). The ChatGPT-style contamination incident.';}}
[a,b,c].forEach(function(e){e.onchange=trifecta;});k.onchange=cache;trifecta();cache();})();''',
},
# ---------------------------------------------------------------- module 06
"06-strategy-tradeoffs": {
 "title": "Four-axis tradeoff explorer",
 "html": r'''<p class="iw-note" style="margin-top:0">Toggle levers and watch the four axes move. <strong>Higher is better on every bar</strong> — notice you can never push them all up at once.</p>
<div class="iw-btns" id="fx-levers">
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-l="bigger">Bigger model</button>
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-l="smaller">Smaller model</button>
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-l="quant">Quantize INT4</button>
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-l="spec">Speculative decoding</button>
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-l="batch">Bigger batches</button>
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-l="cache">Prompt caching</button>
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-l="rerank">Add reranking</button>
 <button class="Button" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-l="fallback">Multi-provider fallback</button>
</div>
<div class="iw-out">
 <div class="iw-metric"><span class="ml">⚡ Speed</span><span class="iw-track"><span class="iw-fill" id="fx-speed"></span></span><span class="mv" id="fx-speedv"></span></div>
 <div class="iw-metric"><span class="ml">✨ Quality</span><span class="iw-track"><span class="iw-fill" id="fx-quality" style="background:var(--color-background-success-solid)"></span></span><span class="mv" id="fx-qualityv"></span></div>
 <div class="iw-metric"><span class="ml">💰 Cost-efficiency</span><span class="iw-track"><span class="iw-fill" id="fx-cost" style="background:var(--color-background-caution-solid)"></span></span><span class="mv" id="fx-costv"></span></div>
 <div class="iw-metric"><span class="ml">🛡 Reliability</span><span class="iw-track"><span class="iw-fill" id="fx-rel" style="background:var(--color-background-discovery-solid)"></span></span><span class="mv" id="fx-relv"></span></div>
 <div class="iw-note" id="fx-note">Baseline. Toggle one or more levers above.</div>
</div>''',
 "js": r'''(function(){var root=document.getElementById('interactive');var $=function(id){return root.querySelector(id);};
var D={bigger:{speed:-18,quality:22,cost:-20,rel:4},smaller:{speed:18,quality:-18,cost:22,rel:2},quant:{speed:12,quality:-8,cost:18,rel:0},spec:{speed:20,quality:0,cost:-4,rel:0},batch:{speed:-10,quality:0,cost:18,rel:-2},cache:{speed:14,quality:0,cost:16,rel:2},rerank:{speed:-6,quality:16,cost:-6,rel:2},fallback:{speed:-4,quality:-2,cost:-8,rel:22}};
var active={};
function clamp(x){return Math.max(8,Math.min(96,x));}
function recompute(){var v={speed:50,quality:50,cost:50,rel:50};
for(var key in active){if(active[key]){var d=D[key];v.speed+=d.speed;v.quality+=d.quality;v.cost+=d.cost;v.rel+=d.rel;}}
['speed','quality','cost','rel'].forEach(function(ax){var val=clamp(v[ax]);$('#fx-'+ax).style.width=val+'%';$('#fx-'+ax+'v').textContent=Math.round(val);});
var on=Object.keys(active).filter(function(k){return active[k];});
var note;if(!on.length)note='Baseline. Toggle one or more levers above.';
else note='Active: <strong>'+on.length+'</strong> lever(s). Every lever pays for a gain on one axis with a loss on another — there is no globally best config, only the best one <em>for your SLO</em>.';
$('#fx-note').innerHTML=note;}
root.querySelectorAll('[data-l]').forEach(function(b){b.onclick=function(){var key=b.dataset.l;active[key]=!active[key];if(active[key])b.setAttribute('data-selected','');else b.removeAttribute('data-selected');recompute();};});
recompute();})();''',
},
}

def main():
    os.makedirs(OUT, exist_ok=True)
    for i in range(len(MODULES)):
        build_module(i)
    build_index()
    print(f"Built {len(MODULES)} module pages + index.html into {OUT}/")

if __name__ == "__main__":
    main()
