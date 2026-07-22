#!/usr/bin/env python3
"""Build the site-wide knowledge graph (digital-garden style).

Scans the markdown sources of every track, extracts pages (nodes) and the
cross-links between them (edges), and writes an interactive force-directed
graph page into _site/graph/index.html. Pure stdlib, like build_site.py.

Nodes map to their deployed URLs:
  content/<mod>/<lesson>.md                       -> ai/<mod>.html#<lesson>
  content/<mod>/README.md                         -> ai/<mod>.html
  <flat-track>/<lesson>.md                        -> <flat-track>/<lesson>.html
  <flat-track>/README.md                          -> <flat-track>/index.html
  harness-engineering/phases/<p>/<l>/docs/en.md   -> harness/phases/<p>/<l>/docs/en.html
  harness-engineering/phases/<p>/README.md        -> harness/phases/<p>/README.html
  harness-engineering/foundations/*.md            -> harness/foundations/*.html
  harness-engineering/README.md                   -> harness/index.html

Edges come in two kinds:
  "link"      a real cross-reference written in the lesson prose
  "structure" curriculum hierarchy (track -> module/phase -> lesson)

Run standalone for stats:  python3 scripts/build_graph.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Fixed categorical slot order (validated against the site surface #faf9f5).
TRACKS = [
    ("ai", "AI engineering", "#2a78d6", "content"),
    ("harness", "Harness engineering", "#008300", "harness-engineering"),
    ("first-principles", "First principles", "#e87ba4", "first-principles"),
    ("product-sense", "Product sense", "#eda100", "product-sense"),
    ("technical-product-sense", "Technical product sense", "#1baf7a", "technical-product-sense"),
    ("technical-product-management", "Technical product management", "#eb6834", "technical-product-management"),
    ("agentic-ai", "Agentic AI", "#4a3aa7", "agentic-ai"),
    ("knowledge-graphs", "Knowledge graphs", "#00879e", "knowledge-graphs"),
    ("flowable", "Flowable", "#a63d40", "flowable"),
]
FLAT_TRACKS = {"first-principles", "product-sense", "technical-product-sense",
               "technical-product-management", "agentic-ai", "knowledge-graphs"}
# Phased tracks share the harness-engineering folder shape:
# (track id, source dir, site prefix, track title)
PHASED_TRACKS = [
    ("harness", "harness-engineering", "harness", "Harness engineering"),
    ("flowable", "flowable", "flowable", "Flowable"),
]

MD_LINK = re.compile(r"\]\(([^)\s]+?\.md)(?:#[^)]*)?\)")


def _title_of(md_path, fallback):
    try:
        with open(md_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    t = line.lstrip("#").strip()
                    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)   # links
                    t = re.sub(r"[*_`]", "", t)                       # emphasis
                    t = re.sub(r"^Lesson\s+[\d.]+\s*[—:-]\s*", "", t)
                    return t or fallback
    except OSError:
        pass
    return fallback


def collect():
    """Return (nodes, edges). Node = dict keyed by repo-relative md path."""
    nodes = {}   # key -> node dict
    edges = []   # (src_key, dst_key, weight, kind)

    def add(key, title, url, track, kind):
        nodes[key] = {"key": key, "title": title, "url": url,
                      "track": track, "kind": kind}

    # ---- AI engineering (content/ modules, deployed as ai/<mod>.html) ----
    add("__ai__", "AI engineering", "ai/index.html", "ai", "track")
    content = os.path.join(ROOT, "content")
    for mod in sorted(os.listdir(content)):
        mdir = os.path.join(content, mod)
        if not os.path.isdir(mdir):
            continue
        mkey = f"content/{mod}/README.md"
        add(mkey, _title_of(os.path.join(mdir, "README.md"), mod),
            f"ai/{mod}.html", "ai", "module")
        edges.append(("__ai__", mkey, 1, "structure"))
        for fn in sorted(os.listdir(mdir)):
            if not fn.endswith(".md") or fn == "README.md":
                continue
            slug = fn[:-3]
            key = f"content/{mod}/{fn}"
            add(key, _title_of(os.path.join(mdir, fn), slug),
                f"ai/{mod}.html#{slug}", "ai", "lesson")
            edges.append((mkey, key, 1, "structure"))

    # ---- Flat tracks ----
    for track in sorted(FLAT_TRACKS):
        tdir = os.path.join(ROOT, track)
        tkey = f"{track}/README.md"
        add(tkey, _title_of(os.path.join(tdir, "README.md"), track),
            f"{track}/index.html", track, "track")
        for fn in sorted(os.listdir(tdir)):
            if not fn.endswith(".md") or fn == "README.md":
                continue
            key = f"{track}/{fn}"
            add(key, _title_of(os.path.join(tdir, fn), fn[:-3]),
                f"{track}/{fn[:-3]}.html", track, "lesson")
            edges.append((tkey, key, 1, "structure"))

    # ---- Phased tracks (harness engineering, flowable) ----
    for track, src, prefix, title in PHASED_TRACKS:
        tdir = os.path.join(ROOT, src)
        tkey = f"{src}/README.md"
        add(tkey, title, f"{prefix}/index.html", track, "track")
        fdir = os.path.join(tdir, "foundations")
        if os.path.isdir(fdir):
            for fn in sorted(os.listdir(fdir)):
                if not fn.endswith(".md"):
                    continue
                fkey = f"{src}/foundations/{fn}"
                add(fkey, _title_of(os.path.join(fdir, fn), fn[:-3].replace("-", " ")),
                    f"{prefix}/foundations/{fn[:-3]}.html", track, "module")
                edges.append((tkey, fkey, 1, "structure"))
        phases = os.path.join(tdir, "phases")
        for phase in sorted(os.listdir(phases)):
            pdir = os.path.join(phases, phase)
            if not os.path.isdir(pdir):
                continue
            pkey = f"{src}/phases/{phase}/README.md"
            ptitle = _title_of(os.path.join(pdir, "README.md"),
                               phase.split("-", 1)[-1].replace("-", " ").title())
            add(pkey, ptitle, f"{prefix}/phases/{phase}/README.html", track, "module")
            edges.append((tkey, pkey, 1, "structure"))
            for lesson in sorted(os.listdir(pdir)):
                en = os.path.join(pdir, lesson, "docs", "en.md")
                if not os.path.exists(en):
                    continue
                key = f"{src}/phases/{phase}/{lesson}/docs/en.md"
                add(key, _title_of(en, lesson.split("-", 1)[-1].replace("-", " ")),
                    f"{prefix}/phases/{phase}/{lesson}/docs/en.html", track, "lesson")
                edges.append((pkey, key, 1, "structure"))

    # ---- Content cross-links ----
    link_counts = {}
    for key, node in nodes.items():
        if key.startswith("__"):
            continue
        src = os.path.join(ROOT, key)
        if not os.path.exists(src):
            continue
        base = os.path.dirname(key)
        with open(src, encoding="utf-8") as f:
            text = f.read()
        for target in MD_LINK.findall(text):
            if target.startswith(("http:", "https:")):
                continue
            resolved = os.path.normpath(os.path.join(base, target)).replace(os.sep, "/")
            if resolved.startswith(".."):
                continue
            if resolved not in nodes:
                # first-principles etc. reference AI-engineering lessons as if
                # content/ modules sat at the repo root — retry with the prefix
                if f"content/{resolved}" in nodes:
                    resolved = f"content/{resolved}"
                else:
                    continue
            if resolved == key:
                continue
            pair = (key, resolved)
            link_counts[pair] = link_counts.get(pair, 0) + 1
    for (s, t), w in sorted(link_counts.items()):
        edges.append((s, t, w, "link"))

    return nodes, edges


def graph_data():
    nodes, raw_edges = collect()
    order = list(nodes)
    index = {k: i for i, k in enumerate(order)}
    # merge a->b and b->a link edges; drop structure edges that duplicate links
    linked = set()
    out_edges = []
    for s, t, w, kind in raw_edges:
        if kind != "link":
            continue
        a, b = sorted((index[s], index[t]))
        if (a, b) in linked:
            for e in out_edges:
                if e[0] == a and e[1] == b:
                    e[2] += w
            continue
        linked.add((a, b))
        out_edges.append([a, b, w, "link"])
    for s, t, w, kind in raw_edges:
        if kind != "structure":
            continue
        a, b = sorted((index[s], index[t]))
        if (a, b) not in linked:
            out_edges.append([a, b, w, "structure"])
    data = {
        "tracks": [{"id": t, "label": lbl, "color": c} for t, lbl, c, _ in TRACKS],
        "nodes": [nodes[k] for k in order],
        "edges": out_edges,
    }
    return data


def page_focus_map(data):
    """site-relative html path -> node key, for the per-page graph button."""
    m = {}
    for n in data["nodes"]:
        page = n["url"].split("#")[0]
        # page-level focus: prefer the page's own node (no anchor), keep first
        if "#" not in n["url"] or page not in m:
            m.setdefault(page, n["key"])
    for n in data["nodes"]:
        if "#" not in n["url"]:
            m[n["url"].split("#")[0]] = n["key"]
    return m


def write_graph_page(site_dir, data):
    gdir = os.path.join(site_dir, "graph")
    os.makedirs(gdir, exist_ok=True)
    tmpl_path = os.path.join(ROOT, "scripts", "graph_page.html")
    with open(tmpl_path, encoding="utf-8") as f:
        page = f.read()
    page = page.replace("/*__GRAPH_DATA__*/null",
                        json.dumps(data, separators=(",", ":")))
    with open(os.path.join(gdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


if __name__ == "__main__":
    d = graph_data()
    links = sum(1 for e in d["edges"] if e[3] == "link")
    structs = sum(1 for e in d["edges"] if e[3] == "structure")
    print(f"{len(d['nodes'])} nodes, {links} cross-link edges, {structs} structure edges")
    by_track = {}
    for n in d["nodes"]:
        by_track[n["track"]] = by_track.get(n["track"], 0) + 1
    for t, c in by_track.items():
        print(f"  {t}: {c}")
