# CLAUDE.md

Guidance for working in this repository.

## What this is

A multi-track educational curriculum, primarily for Senior/Principal PMs
moving into AI product leadership, plus a couple of hands-on build tracks
for engineers. Ten tracks, all cross-linked, all deployed as one static
site on GitHub Pages at https://aakashagg123.github.io/gatsby/.

There is no app, no server, no JS framework build. Everything is markdown
in this repo, rendered to static HTML by pure-stdlib Python scripts.

## Repo layout

Three different shapes of track live side by side:

1. **`content/`** — the original "AI engineering" module. Numbered
   subfolders (`00-foundations/`, `01-inference-internals/`, …), each a
   set of lesson `.md` files plus a `README.md`. Built by `build_html.py`
   into `html/`.

2. **Flat standalone tracks** — `agentic-ai/`, `first-principles/`,
   `product-sense/`, `technical-product-sense/`,
   `technical-product-management/`, `knowledge-graphs/`, `system-design/`.
   Each is a flat folder: `README.md` (track landing) + one `.md` per
   lesson + `recap.md`. Built by `scripts/build_standalone.py`, invoked
   through a thin per-track config wrapper (`build_agentic_ai.py`,
   `build_system_design.py`, etc.) into `<track>-html/`.

3. **Phased tracks** — `harness-engineering/` and `flowable/`. Hands-on
   build-it-yourself tracks with a deep folder tree:
   `phases/<NN-name>/<lesson>/docs/en.md`, each lesson often paired with
   starter code, tests, and an `outputs/*.md` worked example. These are
   **not** pre-rendered — `build_site.py` copies the tree as-is and
   renders a lightweight HTML viewer next to every `.md` file at build
   time (client-side marked + mermaid).

`scripts/build_site.py` assembles all of it into `_site/`, one subfolder
per track, plus a top-level landing page, the knowledge graph
(`scripts/build_graph.py` → `_site/graph/`), and the glossary
(`scripts/build_glossary.py`).

## Build commands

```bash
# Build one standalone track's pre-rendered HTML edition
python3 scripts/build_system_design.py     # -> system-design-html/
python3 scripts/build_agentic_ai.py        # -> agentic-ai-html/
# ...one script per flat track, same pattern

# Build the AI engineering module
python3 scripts/build_html.py              # -> html/

# Verify every relative markdown link resolves (run before every commit)
python3 scripts/check_links.py

# Assemble the full deployed site (also regenerates the knowledge graph
# and glossary) — this is what CI runs on every push to master
python3 scripts/build_site.py              # -> _site/
```

`_site/` and every `<track>-html/` other than the committed pre-rendered
editions are build output — check `.gitignore` before assuming something
is disposable. The pre-rendered `<track>-html/` folders for the flat
tracks **are** committed (they're copied straight into `_site/` at deploy
time), so if you edit a flat track's markdown, re-run its build script
and commit the regenerated HTML alongside the markdown.

## Adding a new standalone (flat) track

1. Create `<track>/README.md` + one `.md` per lesson + `recap.md`,
   following the house style below.
2. Add hand-crafted diagram overrides under `diagrams/<track>/` if the
   lessons need diagrams (see below) — or leave mermaid fences in the
   markdown and let them render as-is.
3. Write `scripts/build_<track>.py`: a thin config dict (`src`, `out`,
   `brand`, `tagline`, `title`, `lede`, `meta`, `callout`, `lessons`)
   passed to `build_standalone.build_track`. Copy an existing one
   (`build_system_design.py` is a clean recent example).
4. Wire it into `scripts/build_site.py`: add a `<TRACK>_HTML` constant, a
   `copytree` block, and a landing-page card. Bump the module count in the
   landing hero copy.
5. Add `"<track>"` to `build_html.py`'s `FLAT` tuple (cross-track link
   rewriting) and to `check_links.py`'s `SCAN_DIRS`.
6. Add `"<track>"` to `build_graph.py`'s `TRACKS` and `FLAT_TRACKS` (or
   `PHASED_TRACKS` for a phased track) — **this is easy to forget**; a
   track missing here is invisible in the site-wide knowledge graph even
   though its pages deploy and link correctly.
7. Add the track to `SUMMARY.md` and to the craft-tracks table in
   `README.md`.
8. Build (`build_<track>.py` then `build_site.py`), run `check_links.py`,
   commit the markdown, the diagrams, and the regenerated `<track>-html/`.

## House style for lesson content

Every lesson in every track follows the same shape:

- **TL;DR** — the topic in a paragraph, the core tradeoff, the scale.
- **🎯 For the [audience] PM** callout — why it matters to the product,
  what it changes in the reader's decisions, a sharp question to ask the
  eng team, the product risk if ignored.
- **Mental model** — the one diagram or analogy that makes it click.
- **Mechanics** — how it actually works: components, data flow, protocols.
- **Tradeoffs & decisions** — named tradeoffs with costs.
- **Failure modes** — how it breaks in production.
- **Practitioner checklist** — what to verify before shipping or betting
  on it.
- **Related lessons** — cross-links to other tracks, not just within-track.

Read **`WRITING-STYLE.md`** before writing or editing any prose in this
repo — it defines the Simplified-English-spirit rules (short sentences,
one idea per sentence, active voice, plain consistent vocabulary) that all
lesson content should follow. It applies to prose only: code, commands,
mermaid syntax, numbers, and named APIs are untouched.

## Diagrams

Two options, both fine:

- **Mermaid fences** (` ```mermaid `) in the markdown — rendered client-side
  for phased tracks, or via injected CDN script for flat tracks with no
  override.
- **Hand-crafted HTML overrides** — preferred when a diagram needs real
  visual design (pills, grids, styled boxes) rather than a flowchart.
  Drop a file at `diagrams/<track>/<page-key>-<n>.html` (0-indexed, nth
  mermaid block in that page) and `build_standalone.py`'s
  `apply_diagram_overrides()` swaps it in at build time, replacing the
  mermaid fence entirely. See `diagrams/agentic-ai/` or
  `diagrams/system-design/` for the visual pattern (warm cream gradient
  card, `.kg-pill`/`.sd-chip` style chips, no Mermaid look).

## Deploy

`.github/workflows/pages.yml` runs `check_links.py` (non-blocking) then
`build_site.py` on every push to `master`, and deploys `_site/` to GitHub
Pages. There's no separate staging environment — a push to `master` is
live within a couple of minutes. Land changes through a PR from a
`claude/*` branch rather than pushing to `master` directly.

## Before committing

- `python3 scripts/check_links.py` — must exit 0.
- If you touched a flat track's markdown, re-run its `build_<track>.py`
  and commit the regenerated `<track>-html/` output.
- If you added or renamed a track, verify it shows up in
  `python3 scripts/build_graph.py`'s per-track node counts.
