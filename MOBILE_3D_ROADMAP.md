# Mobile-first fluid design + 3D knowledge graph

Two-workstream initiative: fix confirmed mobile-layout bugs site-wide, then
convert the knowledge graph from a hand-rolled 2D canvas into a real 3D
visualization with an automatic 2D fallback. Full scoping context lives in
the plan history for this session; this file tracks execution.

## Workstream 1 — Mobile-first fluid design pass

Scope: fix real bugs pragmatically (no formal WCAG audit).

- [x] `scripts/reader_widget.py` — mobile `@media` block mapping
      Narrow/Default/Wide to side-padding instead of `max-width` (a no-op
      below ~620-1120px today).
- [x] `scripts/build_site.py` — phased-track (`harness-engineering/`,
      `flowable/`) sidebar: hamburger button + off-canvas drawer + scrim,
      replacing the current `display:none` below 880px.
- [x] `scripts/build_html.py` — same hamburger+drawer pattern for the
      AI-engineering module's `.topnav`/`.sidebar` (identical bug, same fix
      shape, different selectors).
- [x] Rebuild everything, `check_links.py`, screenshot-verify at mobile +
      desktop widths, commit/push/PR/merge.

## Workstream 2 — 3D knowledge graph

Scope: `scripts/graph_page.html` only; `scripts/build_graph.py` needs no
changes (its data payload is renderer-agnostic).

- [x] Wrap the existing hand-rolled 2D canvas implementation into a
      `boot2D()` function, unchanged internally — the permanent fallback.
- [x] Add capability detection (WebGL support, `prefers-reduced-motion`,
      low-power-mobile heuristic). A pre-show FPS trial turned out to need
      an instance-teardown API the library doesn't document, so this
      shipped as a live post-show frame-time monitor instead (see PR body).
- [x] Add `boot3D()` using `3d-force-graph` (three.js + d3-force-3d) via
      CDN, reusing the shared node/edge/legend/search/card/list-view state
      and DOM chrome.
- [x] Mobile bottom-sheet layout for `#card`/`#legend` in the existing
      `@media (max-width:720px)` block, for both renderers.
- [x] Verify: confirmed unpkg/cdnjs/jsdelivr are all blocked in this sandbox
      by org policy (not just jsdelivr) — code-reviewed the 3D data-mapping
      against the library's published API docs, fully screenshot- and
      interaction-tested the 2D fallback path (including the exact
      CDN-failure -> fallback trigger, live), commit/push/PR/merge.

Ship order: Workstream 1 first (lower risk, affects every page), then
Workstream 2.
