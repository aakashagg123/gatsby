#!/usr/bin/env python3
"""Assemble the combined GitHub Pages site with two separate landings.

  _site/
  ├── index.html        top landing → AI Engineering | Harness Engineering
  ├── ai/               the AI engineering module (pre-rendered html/ editions)
  └── harness/          the harness engineering track (markdown rendered client-side)

The harness track is rendered at runtime with marked + mermaid (so GFM tables and
Mermaid diagrams render). This build step is pure stdlib — copy files and write a
viewer per markdown doc — so it never fails on a missing dependency.

Run:  python3 scripts/build_site.py
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "_site")
HTML = os.path.join(ROOT, "html")                       # AI engineering editions
HARNESS_SRC = os.path.join(ROOT, "harness-engineering")

VIEWER = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Harness Engineering</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{{
    --bg:#faf9f5;--surface:#ffffff;--ink:#181818;--muted:#6c6a60;
    --accent:#d97757;--accent-deep:#bd5d3a;--line:#e8e6dd;--code-bg:#1c1b18;--soft:#f2f0e9;
  }}
  *{{box-sizing:border-box}}
  html{{-webkit-text-size-adjust:100%}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font-family:Inter,system-ui,-apple-system,sans-serif;font-size:16px;line-height:1.7;
    -webkit-font-smoothing:antialiased;letter-spacing:-0.005em}}
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
  pre.mermaid{{background:var(--surface);color:var(--ink);border:1px solid var(--line);
    padding:22px;text-align:center}}
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
</style></head><body>
<div class="top"><a href="{root}index.html">← All courses</a><a class="brand" href="{harness_root}index.html">Harness Engineering</a></div>
<main id="content">Loading…</main>
{nav}
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({{startOnLoad:false, theme:'base', themeVariables:{{
  primaryColor:'#f2f0e9', primaryTextColor:'#181818', primaryBorderColor:'#d97757',
  lineColor:'#bd5d3a', fontFamily:'Inter, system-ui, sans-serif', fontSize:'15px'
}}}});
const md = await (await fetch('{md}')).text();
// protect mermaid fences so marked doesn't treat them as code
const blocks=[]; const stripped = md.replace(/```mermaid\\n([\\s\\S]*?)```/g,(m,c)=>{{
  blocks.push(c); return `<pre class="mermaid">__MERMAID_${{blocks.length-1}}__</pre>`;}});
let html = marked.parse(stripped);
html = html.replace(/__MERMAID_(\\d+)__/g,(m,i)=>blocks[+i]);
const el = document.getElementById('content'); el.innerHTML = html;
// rewrite intra-site .md links to their .html viewers
el.querySelectorAll('a[href]').forEach(a=>{{
  const h=a.getAttribute('href');
  if(h && !/^https?:|^#/.test(h)) a.setAttribute('href', h.replace(/\\.md(#|$)/,'.html$1'));
}});
await mermaid.run({{querySelector:'pre.mermaid'}});
</script></body></html>
"""

LANDING = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Engineering Learning Modules</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#faf9f5;--surface:#ffffff;--ink:#181818;--muted:#6c6a60;
    --accent:#d97757;--accent-deep:#bd5d3a;--line:#e8e6dd;--soft:#f2f0e9;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:Inter,system-ui,-apple-system,sans-serif;font-size:17px;line-height:1.7;
    -webkit-font-smoothing:antialiased;letter-spacing:-0.005em}
  .wrap{max-width:920px;margin:0 auto;padding:104px 24px 80px}
  .eyebrow{display:inline-block;font-size:.78rem;font-weight:600;letter-spacing:.08em;
    text-transform:uppercase;color:var(--accent-deep);margin-bottom:16px}
  h1{font-size:3.1rem;line-height:1.08;letter-spacing:-0.03em;font-weight:600;margin:0 0 .25em;max-width:14ch}
  p.sub{color:var(--muted);font-size:1.2rem;margin:0;max-width:54ch}
  .cards{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:52px}
  @media(max-width:680px){.cards{grid-template-columns:1fr}h1{font-size:2.4rem}}
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
  <span class="eyebrow">From Scratch</span>
  <h1>Engineering Learning Modules</h1>
  <p class="sub">Two separate, hands-on curricula — build each system from first principles, then use it for real.</p>
  <div class="cards">
    <a class="card" href="ai/index.html">
      <span class="tag">Module</span>
      <h2>AI Engineering →</h2>
      <p>The engineering discipline under production LLM systems — inference, retrieval,
      evals, observability, safety, cost. Designed reading editions.</p>
    </a>
    <a class="card" href="harness/index.html">
      <span class="tag">Module</span>
      <h2>Harness Engineering →</h2>
      <p>Build a coding agent's harness from scratch — loop, tools, context, memory,
      subagents — then use the real SDK. Build It / Use It, ships an artifact each lesson.</p>
    </a>
  </div>
  <footer>Educational content. Use it, fork it, teach from it.</footer>
</div></body></html>
"""


def rel_to_harness_root(md_path):
    """'../' * depth from a harness md file up to _site/harness/."""
    rel = os.path.relpath(md_path, os.path.join(SITE, "harness"))
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

    # 2. Harness engineering: copy the whole tree (md + code + outputs).
    dst_harness = os.path.join(SITE, "harness")
    shutil.copytree(HARNESS_SRC, dst_harness)

    # 3. Lesson ordering for prev/next navigation.
    lessons = lesson_order(dst_harness)
    prev_next = {}
    for i, md in enumerate(lessons):
        prev_next[md] = (lessons[i - 1] if i > 0 else None,
                         lessons[i + 1] if i < len(lessons) - 1 else None)

    # 4. Render a viewer next to every markdown file (sources stay browsable).
    pages = 0
    for dp, _, files in os.walk(dst_harness):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            md_path = os.path.join(dp, fn)
            title = os.path.splitext(fn)[0]
            with open(md_path) as f:
                first = f.readline().lstrip("# ").strip()
            title = first or title
            root = rel_to_harness_root(md_path)            # up to _site/
            html_path = md_path[:-3] + ".html"
            md_url = "./" + fn
            nav = ""
            if is_lesson(md_path):
                p, n = prev_next.get(md_path, (None, None))
                nav = nav_html(md_path, p, n)
            with open(html_path, "w") as f:
                f.write(VIEWER.format(
                    title=title,
                    md=md_url,
                    root="../" + root if root else "../",   # _site/ root
                    harness_root=root or "./",
                    nav=nav,
                ))
            pages += 1

    # 4. Harness landing = viewer for README.md.
    readme_html = os.path.join(dst_harness, "README.html")
    if os.path.exists(readme_html):
        shutil.copyfile(readme_html, os.path.join(dst_harness, "index.html"))

    # 5. Top landing.
    with open(os.path.join(SITE, "index.html"), "w") as f:
        f.write(LANDING)

    print(f"built _site/ — ai module + harness ({pages} pages) + landing")


if __name__ == "__main__":
    main()
