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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
OUT = os.path.join(ROOT, "html")

# ---- module / lesson ordering -------------------------------------------------
MODULES = [
    ("00-foundations", "00", "Foundations",
     "The mindset shift from “writing prompts” to “engineering systems.”",
     ["harness-engineering", "context-engineering", "infra-not-demos"]),
    ("01-inference-internals", "01", "Inference Internals",
     "What happens between your request and the tokens that come back.",
     ["prompt-vs-semantic-caching", "kv-cache-management", "prefill-vs-decode",
      "batching-and-paged-attention", "speculative-quantization-distillation",
      "quantization-formats"]),
    ("02-reliable-outputs", "02", "Reliable Outputs & Tool Use",
     "Making models produce things downstream systems can trust.",
     ["structured-output", "function-calling", "agent-guardrails", "model-routing"]),
    ("03-rag", "03", "RAG & Retrieval",
     "Grounding models in your data — and proving they actually used it.",
     ["rag-architecture", "retrieval-evals"]),
    ("04-evals-observability", "04", "Evals & Observability",
     "You cannot operate what you cannot measure.",
     ["evals", "observability", "cost-attribution"]),
    ("05-safety-multitenancy", "05", "Safety & Multi-tenancy",
     "Keeping tenants, users, and data from leaking into each other.",
     ["safety-engineering", "multi-tenant-isolation"]),
    ("06-strategy-tradeoffs", "06", "Strategy & Tradeoffs",
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
    base_anchor = target.split("#")[0]
    resolved = os.path.normpath(os.path.join("content", cur_mod, base_anchor))
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
        md, extensions=["tables", "fenced_code", "sane_lists", "attr_list"]
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

def lesson_title(md):
    m = re.search(r"\A\s*#\s+(.*)", md)
    return m.group(1).strip() if m else "Lesson"

# ---- page chrome --------------------------------------------------------------
SPARK = ('<svg class="spark" viewBox="0 0 100 100" width="22" height="22" aria-hidden="true">'
         '<path d="M50 8 L58 42 L92 50 L58 58 L50 92 L42 58 L8 50 L42 42 Z" fill="#D97757"/></svg>')

def head(title, depth_note=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{htmllib.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>"""

def topbar():
    links = "".join(
        f'<a href="{SLUG_TO_PAGE[s]}">{num}</a>' for (s, num, *_ ) in MODULES
    )
    return f"""<header class="topbar">
  <a class="brand" href="index.html">{SPARK}<span>AI&nbsp;Engineering</span><em>for AI-native PMs</em></a>
  <nav class="topnav">{links}</nav>
</header>"""

def sidebar(cur_mod, lessons_meta):
    items = []
    for (slug, num, title, _desc, _lessons) in MODULES:
        active = " active" if slug == cur_mod else ""
        sub = ""
        if slug == cur_mod and lessons_meta:
            sub_items = "".join(
                f'<a href="#{lid}">{htmllib.escape(t)}</a>' for lid, t in lessons_meta
            )
            sub = f'<div class="sub">{sub_items}</div>'
        items.append(
            f'<a class="modlink{active}" href="{SLUG_TO_PAGE[slug]}">'
            f'<span class="num">{num}</span>{htmllib.escape(title)}</a>{sub}'
        )
    return f'<aside class="sidebar"><div class="sticky">{"".join(items)}</div></aside>'

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
            '<a href="index.html">AI Engineering</a> curriculum for AI-native PMs.</footer>')

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
            f'<section class="lesson" id="{lid}">'
            f'<div class="lesson-head"><span class="lesson-num">{num}.{i}</span>'
            f'<h2>{htmllib.escape(t)}</h2></div>{body}'
            f'<a class="totop" href="#top">↑ back to top</a></section>'
        )

    prev_mod = MODULES[idx-1] if idx > 0 else None
    next_mod = MODULES[idx+1] if idx < len(MODULES)-1 else None

    toc = "".join(
        f'<a href="#{lid}"><span>{num}.{i}</span>{htmllib.escape(t)}</a>'
        for i, (lid, t) in enumerate(lessons_meta, 1)
    )

    page = head(f"{num} · {title} — AI Engineering for PMs")
    page += topbar()
    page += '<div class="layout">'
    page += sidebar(slug, lessons_meta)
    page += f"""<main class="content" id="top">
  <div class="hero">
    <span class="chip">Module {num}</span>
    <h1>{htmllib.escape(title)}</h1>
    <p class="lede">{htmllib.escape(desc)}</p>
    <div class="hero-meta">{len(lessons)} lessons · every lesson includes a
      <strong>🎯 For the AI-native PM</strong> briefing</div>
  </div>
  <div class="intro">{intro_html}</div>
  <nav class="toc"><div class="toc-h">In this module</div>{toc}</nav>
  {''.join(sections)}
  {footer(prev_mod, next_mod)}
  </main></div></body></html>"""
    with open(os.path.join(OUT, SLUG_TO_PAGE[slug]), "w") as f:
        f.write(page)

# ---- build the landing index --------------------------------------------------
def build_index():
    cards = []
    for (slug, num, title, desc, lessons) in MODULES:
        lis = "".join(f"<li>{htmllib.escape(l.replace('-', ' '))}</li>" for l in lessons[:3])
        more = f"<li class='more'>+{len(lessons)-3} more…</li>" if len(lessons) > 3 else ""
        cards.append(f"""<a class="card" href="{SLUG_TO_PAGE[slug]}">
        <span class="card-num">{num}</span>
        <h3>{htmllib.escape(title)}</h3>
        <p>{htmllib.escape(desc)}</p>
        <ul>{lis}{more}</ul>
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

    page = head("AI Engineering — A Curriculum for AI-native PMs")
    page += topbar()
    page += f"""<main class="content index" id="top">
  <div class="index-hero">
    <span class="chip">A linked curriculum</span>
    <h1>AI Engineering,<br/><em>from scratch to production.</em></h1>
    <p class="lede">The engineering discipline underneath production LLM systems —
      inference, retrieval, evaluation, observability, safety, and cost — taught through
      the lens of the decisions a <strong>Senior or Principal PM</strong> has to make.</p>
    <div class="index-meta"><span>7 modules</span><span>23 lessons</span>
      <span>PM-native</span><span>production-grade</span></div>
  </div>

  <div class="pm-band">
    <span class="pm-ic">🎯</span>
    <div><strong>Built for the AI-native PM.</strong> Every lesson pairs the real
    mechanics with a briefing: why it matters to the product, what it changes in your
    decisions, the question to ask your eng team, and the product risk if you ignore it.</div>
  </div>

  <h2 class="sec">The modules</h2>
  <div class="cards">{''.join(cards)}</div>

  <h2 class="sec">Threads — follow one concern across the whole stack</h2>
  <div class="threads">{thread_html}</div>

  <footer class="foot">Educational content. Use it, fork it, teach from it. ·
    Inspired by the topic list at
    <a href="https://aiengineeringfromscratch.com">aiengineeringfromscratch.com</a></footer>
  </main></body></html>"""
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(page)

CSS = r"""
:root{
  --bg:#FAF9F5; --bg2:#F4F2EA; --panel:#FFFFFF; --line:#E7E2D5; --line2:#EFEBE0;
  --ink:#1A1915; --ink2:#3D3B35; --mut:#6F6C62; --accent:#D97757; --accent-d:#C2613F;
  --accent-soft:#FBEFE9; --green:#3F7A52; --radius:14px;
  --serif:'Fraunces','Iowan Old Style',Palatino,Georgia,serif;
  --sans:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
  --mono:'SF Mono',ui-monospace,'JetBrains Mono',Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink2);font-family:var(--sans);
  font-size:16.5px;line-height:1.72;-webkit-font-smoothing:antialiased;}
a{color:var(--accent-d);text-decoration:none}
a:hover{text-decoration:underline}

/* top bar */
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:24px;
  padding:14px 26px;background:rgba(250,249,245,.86);backdrop-filter:blur(10px);
  border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:9px;color:var(--ink);font-weight:600}
.brand:hover{text-decoration:none}
.brand span{font-size:16px;letter-spacing:.2px}
.brand em{font-style:normal;color:var(--mut);font-weight:400;font-size:13px;
  padding-left:9px;margin-left:3px;border-left:1px solid var(--line)}
.spark{flex:0 0 auto}
.topnav{margin-left:auto;display:flex;gap:4px;flex-wrap:wrap}
.topnav a{font-variant-numeric:tabular-nums;font-size:13px;font-weight:500;color:var(--mut);
  padding:5px 10px;border-radius:8px}
.topnav a:hover{background:var(--bg2);color:var(--accent-d);text-decoration:none}

/* layout */
.layout{display:grid;grid-template-columns:268px minmax(0,1fr);gap:0;
  max-width:1240px;margin:0 auto}
.sidebar{border-right:1px solid var(--line);padding:30px 18px 60px}
.sticky{position:sticky;top:74px}
.modlink{display:flex;gap:10px;align-items:baseline;padding:8px 12px;border-radius:10px;
  color:var(--ink2);font-size:14.5px;font-weight:500}
.modlink:hover{background:var(--bg2);text-decoration:none}
.modlink.active{background:var(--accent-soft);color:var(--accent-d)}
.modlink .num{font-family:var(--mono);font-size:12px;color:var(--accent);font-weight:600}
.sub{display:flex;flex-direction:column;margin:2px 0 10px 34px;
  border-left:1px solid var(--line);padding-left:12px}
.sub a{color:var(--mut);font-size:13px;padding:4px 0;line-height:1.4}
.sub a:hover{color:var(--accent-d);text-decoration:none}

/* content column */
.content{padding:46px 56px 90px;max-width:880px}
.hero{border-bottom:1px solid var(--line);padding-bottom:30px;margin-bottom:14px}
.chip{display:inline-block;font-family:var(--mono);font-size:12px;letter-spacing:.6px;
  text-transform:uppercase;color:var(--accent-d);background:var(--accent-soft);
  padding:5px 11px;border-radius:999px;margin-bottom:18px}
.hero h1{font-family:var(--serif);font-weight:600;font-size:42px;line-height:1.1;
  color:var(--ink);margin:.1em 0 .25em}
.lede{font-size:20px;color:var(--ink2);margin:.2em 0 .6em;line-height:1.5}
.hero-meta{font-size:14px;color:var(--mut)}
.hero-meta strong{color:var(--accent-d);font-weight:600}

.intro{color:var(--ink2)}
.intro blockquote{margin:18px 0}

/* table of contents */
.toc{margin:30px 0 8px;background:var(--panel);border:1px solid var(--line);
  border-radius:var(--radius);padding:18px 20px}
.toc-h{font-family:var(--mono);font-size:11.5px;letter-spacing:.8px;text-transform:uppercase;
  color:var(--mut);margin-bottom:10px}
.toc a{display:flex;gap:12px;padding:6px 0;color:var(--ink2);font-size:15px;
  border-bottom:1px solid var(--line2)}
.toc a:last-child{border-bottom:none}
.toc a:hover{color:var(--accent-d);text-decoration:none}
.toc a span{font-family:var(--mono);font-size:12.5px;color:var(--accent);min-width:32px}

/* lessons */
.lesson{padding:46px 0 8px;border-top:1px solid var(--line);margin-top:30px}
.lesson:first-of-type{border-top:none}
.lesson-head{display:flex;align-items:baseline;gap:14px;margin-bottom:6px}
.lesson-num{font-family:var(--mono);font-size:14px;color:#fff;background:var(--accent);
  padding:3px 9px;border-radius:7px;font-weight:600}
.lesson h2{font-family:var(--serif);font-weight:600;font-size:29px;line-height:1.18;
  color:var(--ink);margin:0}
.lesson h3{font-family:var(--serif);font-weight:600;font-size:21px;color:var(--ink);
  margin:1.8em 0 .5em}
.lesson h4{font-size:16px;font-weight:600;color:var(--ink);margin:1.4em 0 .4em;
  letter-spacing:.2px}
.lesson p{margin:.85em 0}
.lesson ul,.lesson ol{padding-left:1.35em;margin:.7em 0}
.lesson li{margin:.32em 0}
.lesson strong{color:var(--ink);font-weight:600}
.lesson em{color:var(--ink2)}
hr{border:none;border-top:1px solid var(--line);margin:2em 0}

/* PM callout */
.pm-callout{position:relative;background:linear-gradient(180deg,#FBF0EA,#FBEEE7);
  border:1px solid #F0D3C4;border-left:4px solid var(--accent);
  border-radius:var(--radius);padding:20px 24px 14px;margin:26px 0}
.pm-callout > p:first-child{font-family:var(--sans);font-weight:600;color:var(--accent-d);
  font-size:13px;letter-spacing:.5px;text-transform:uppercase;margin:0 0 .5em}
.pm-callout p{margin:.5em 0;font-size:15.5px}
.pm-callout strong{color:var(--ink)}

/* generic blockquote */
blockquote{margin:18px 0;padding:4px 20px;border-left:3px solid var(--accent);
  color:var(--ink2);background:var(--bg2);border-radius:0 10px 10px 0}
blockquote p{margin:.5em 0}

/* tables */
table{width:100%;border-collapse:collapse;margin:20px 0;font-size:14.5px;
  background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  overflow:hidden}
th{text-align:left;background:var(--bg2);color:var(--ink);font-weight:600;
  padding:11px 14px;border-bottom:1px solid var(--line);font-size:13.5px}
td{padding:11px 14px;border-bottom:1px solid var(--line2);vertical-align:top}
tr:last-child td{border-bottom:none}
td code,th code{font-size:12.5px}

/* code */
code{font-family:var(--mono);font-size:13.5px;background:var(--bg2);color:var(--accent-d);
  padding:2px 6px;border-radius:6px}
pre{background:#211F1B;color:#EDE9DF;border-radius:var(--radius);padding:18px 20px;
  overflow-x:auto;margin:18px 0;border:1px solid #2c2a25;line-height:1.6}
pre code{background:none;color:inherit;padding:0;font-size:13px}

/* task lists */
.lesson li.task{list-style:none;margin-left:-1.1em;padding-left:1.9em;position:relative}
.lesson li.task:before{position:absolute;left:0;top:0;width:1.2em;height:1.2em}
.lesson li.todo:before{content:"☐";color:var(--mut);font-size:1.05em}
.lesson li.done:before{content:"☑";color:var(--green)}

.totop{display:inline-block;margin-top:24px;font-size:12.5px;color:var(--mut);
  font-family:var(--mono)}
.totop:hover{color:var(--accent-d);text-decoration:none}

/* page nav + footer */
.pagenav{display:flex;justify-content:space-between;gap:16px;margin:54px 0 30px;
  flex-wrap:wrap}
.navcard{flex:1 1 240px;display:flex;flex-direction:column;gap:4px;padding:16px 20px;
  background:var(--panel);border:1px solid var(--line);border-radius:var(--radius)}
.navcard:hover{border-color:var(--accent);text-decoration:none}
.navcard.next{text-align:right;align-items:flex-end}
.navcard .lbl{font-size:12px;color:var(--mut);font-family:var(--mono)}
.navcard .ttl{font-family:var(--serif);font-size:17px;color:var(--ink);font-weight:600}
.foot{margin-top:30px;padding-top:22px;border-top:1px solid var(--line);
  color:var(--mut);font-size:13.5px}

/* ---- index page ---- */
.index{max-width:1080px;margin:0 auto;padding:60px 40px 90px}
.index-hero{text-align:center;padding:20px 0 30px}
.index-hero h1{font-family:var(--serif);font-weight:600;font-size:56px;line-height:1.08;
  color:var(--ink);margin:.15em 0 .3em}
.index-hero h1 em{font-style:italic;color:var(--accent)}
.index-hero .lede{max-width:720px;margin:0 auto;font-size:20px}
.index-meta{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:22px}
.index-meta span{font-size:13px;color:var(--ink2);background:var(--panel);
  border:1px solid var(--line);padding:6px 14px;border-radius:999px;
  font-family:var(--mono)}
.pm-band{display:flex;gap:16px;align-items:flex-start;max-width:860px;margin:36px auto;
  background:linear-gradient(180deg,#FBF0EA,#FBEEE7);border:1px solid #F0D3C4;
  border-left:4px solid var(--accent);border-radius:var(--radius);padding:20px 24px}
.pm-band .pm-ic{font-size:24px;line-height:1.2}
.pm-band strong{color:var(--ink)}
.sec{font-family:var(--serif);font-weight:600;font-size:26px;color:var(--ink);
  text-align:center;margin:60px 0 26px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.card{position:relative;display:flex;flex-direction:column;background:var(--panel);
  border:1px solid var(--line);border-radius:18px;padding:24px 24px 22px;color:var(--ink2)}
.card:hover{border-color:var(--accent);transform:translateY(-2px);text-decoration:none;
  box-shadow:0 10px 30px -18px rgba(120,70,40,.45);transition:.18s}
.card-num{font-family:var(--mono);font-size:13px;color:#fff;background:var(--accent);
  width:fit-content;padding:3px 10px;border-radius:7px;font-weight:600;margin-bottom:12px}
.card h3{font-family:var(--serif);font-weight:600;font-size:21px;color:var(--ink);margin:0 0 .35em}
.card p{font-size:14.5px;color:var(--mut);margin:0 0 .9em}
.card ul{margin:0;padding-left:1.1em;font-size:13.5px;color:var(--ink2)}
.card li{margin:.2em 0}
.card li.more{list-style:none;margin-left:-1.1em;color:var(--mut);font-style:italic}
.card-go{margin-top:auto;padding-top:14px;color:var(--accent-d);font-weight:600;font-size:14px}
.threads{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;
  max-width:920px;margin:0 auto}
.thread{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px}
.thread-t{font-weight:600;color:var(--ink);margin-bottom:6px;font-size:15.5px}
.thread p{margin:0;font-size:14px;color:var(--mut)}

@media (max-width:880px){
  .layout{grid-template-columns:1fr}
  .sidebar{display:none}
  .content{padding:32px 22px 70px}
  .hero h1{font-size:34px}.index-hero h1{font-size:38px}
  .topnav{display:none}
}
"""

def main():
    os.makedirs(OUT, exist_ok=True)
    for i in range(len(MODULES)):
        build_module(i)
    build_index()
    print(f"Built {len(MODULES)} module pages + index.html into {OUT}/")

if __name__ == "__main__":
    main()
