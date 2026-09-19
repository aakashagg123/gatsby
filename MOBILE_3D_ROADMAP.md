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

- [ ] Wrap the existing hand-rolled 2D canvas implementation into a
      `boot2D()` function, unchanged internally — the permanent fallback.
- [ ] Add capability detection (WebGL support, `prefers-reduced-motion`,
      low-power-mobile heuristic, a frame-rate trial before first paint).
- [ ] Add `boot3D()` using `3d-force-graph` (three.js + d3-force-3d) via
      CDN, reusing the shared node/edge/legend/search/card/list-view state
      and DOM chrome.
- [ ] Mobile bottom-sheet layout for `#card`/`#legend` in the existing
      `@media (max-width:720px)` block, for both renderers.
- [ ] Verify: try alternate CDN hosts (unpkg/cdnjs — jsdelivr is blocked in
      this sandbox), code-review the 3D data-mapping against the library's
      docs, fully screenshot-test the 2D fallback path, commit/push/PR/merge.

Ship order: Workstream 1 first (lower risk, affects every page), then
Workstream 2.
