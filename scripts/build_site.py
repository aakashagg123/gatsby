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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{{--ink:#1f1e1d;--bg:#fafaf5;--accent:#3553ff;--muted:#6b6a64;--line:#e7e6df;}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 Inter,system-ui,sans-serif}}
  .top{{position:sticky;top:0;background:rgba(250,250,245,.92);backdrop-filter:blur(6px);
    border-bottom:1px solid var(--line);padding:12px 20px;font-weight:600}}
  .top a{{color:var(--accent);text-decoration:none;margin-right:16px}}
  main{{max-width:820px;margin:0 auto;padding:32px 20px 80px}}
  h1,h2,h3{{line-height:1.25}} h1{{font-size:2rem}} h2{{margin-top:2em;border-bottom:1px solid var(--line);padding-bottom:.3em}}
  a{{color:var(--accent)}}
  code{{font-family:'JetBrains Mono',monospace;background:#eeede6;padding:.1em .35em;border-radius:4px;font-size:.9em}}
  pre{{background:#1f1e1d;color:#f3f2ec;padding:16px;border-radius:8px;overflow:auto}}
  pre code{{background:none;color:inherit;padding:0}}
  pre.mermaid{{background:#fff;border:1px solid var(--line);text-align:center}}
  table{{border-collapse:collapse;width:100%;margin:1em 0;font-size:.94em}}
  th,td{{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}}
  th{{background:#f0efe8}}
  blockquote{{border-left:3px solid var(--accent);margin:1em 0;padding:.3em 1em;color:var(--muted);background:#f3f2ec}}
  details{{background:#f3f2ec;border:1px solid var(--line);border-radius:8px;padding:10px 14px;margin:.6em 0}}
  summary{{cursor:pointer;font-weight:500}}
  hr{{border:none;border-top:1px solid var(--line);margin:2em 0}}
</style></head><body>
<div class="top"><a href="{root}index.html">← All courses</a><a href="{harness_root}index.html">Harness Engineering</a></div>
<main id="content">Loading…</main>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({{startOnLoad:false, theme:'neutral'}});
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500..600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{--ink:#1f1e1d;--bg:#fafaf5;--accent:#3553ff;--muted:#6b6a64;--line:#e7e6df;}
  body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Inter,system-ui,sans-serif}
  .wrap{max-width:880px;margin:0 auto;padding:80px 24px}
  h1{font-family:Fraunces,serif;font-size:2.6rem;margin:0 0 .2em}
  p.sub{color:var(--muted);font-size:1.15rem;margin-top:0}
  .cards{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:40px}
  @media(max-width:680px){.cards{grid-template-columns:1fr}}
  a.card{display:block;text-decoration:none;color:inherit;background:#fff;border:1px solid var(--line);
    border-radius:14px;padding:26px;transition:.15s}
  a.card:hover{border-color:var(--accent);transform:translateY(-2px);box-shadow:0 6px 24px rgba(53,83,255,.08)}
  a.card h2{margin:.1em 0 .3em;font-size:1.35rem}
  a.card .tag{display:inline-block;font-size:.78rem;color:var(--accent);font-weight:600;letter-spacing:.04em;text-transform:uppercase}
  a.card p{color:var(--muted);margin:.4em 0 0}
  footer{color:var(--muted);font-size:.85rem;margin-top:60px}
</style></head><body>
<div class="wrap">
  <h1>Engineering Learning Modules</h1>
  <p class="sub">Two separate, hands-on curricula.</p>
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


def main():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE)

    # 1. AI engineering module: copy the pre-rendered editions.
    shutil.copytree(HTML, os.path.join(SITE, "ai"))

    # 2. Harness engineering: copy the whole tree (md + code + outputs).
    dst_harness = os.path.join(SITE, "harness")
    shutil.copytree(HARNESS_SRC, dst_harness)

    # 3. Render a viewer next to every markdown file, then drop the .md is kept
    #    (so .py/.json/.md sources stay browsable; viewers are the .html).
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
            with open(html_path, "w") as f:
                f.write(VIEWER.format(
                    title=title,
                    md=md_url,
                    root="../" + root if root else "../",   # _site/ root
                    harness_root=root or "./",
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
