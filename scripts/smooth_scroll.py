#!/usr/bin/env python3
"""Shared scroll-smoothness layer, injected into every page of the built site.

Why a separate asset: the pre-rendered track pages (`<track>-html/`) are committed and
copied verbatim into `_site/`. `build_site.py` already post-processes every page there
(graph button, glossary, favicon). This module adds one more stylesheet the same way, so
one change reaches the landing page, the AI pages, every flat track, both viewers and the
graph page, with no need to regenerate the committed pages.

The rules are inlined as a <style> last in <head> (no extra request), so they win the
cascade over each page's own <style> at equal specificity.

Design rules (iOS first):
  * Native scrolling only. iOS Safari scrolls on the compositor thread. A JS smoother
    would fight it. So this layer adds no scroll listeners and no scroll library.
  * Keep the main thread free and avoid per-frame blending, containment surprises and
    scroll chaining.
  * Every rule is guarded (`@supports`, `@media`) so an older browser ignores it.
"""

CSS = r"""
/* ---- anchors and programmatic scrolling ---- */
html{scroll-padding-top:84px}
@media (max-width:560px){html{scroll-padding-top:80px}}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto !important}}

/* ---- sticky bars: opaque, so the browser does not blend them over moving text ---- */
.topbar,.top,header.bar{background:#ffffff}

/* ---- text rendering: let the browser pick; optimizeLegibility slows long pages ---- */
body{text-rendering:auto}

/* ---- horizontal overflow: clip instead of making body a scroll container ---- */
@supports (overflow:clip){body{overflow-x:clip}}

/* ---- scroll chaining and iOS back-swipe: keep inner scrollers to themselves ---- */
pre,pre.mermaid,table{overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
#gl-panel,#panel,#card,#rs-panel{overscroll-behavior:contain;-webkit-overflow-scrolling:touch}
@media (max-width:880px){
  .sidebar{overscroll-behavior:contain;-webkit-overflow-scrolling:touch;will-change:transform}
}
#gl-panel{will-change:transform}

/* ---- page lock while a drawer or the glossary panel is open ---- */
html:has(#sb-scrim.open),html:has(#gl-scrim.open),html:has(body.gl-open){overflow:hidden}
/* keep the page from jumping when the desktop scrollbar disappears under the lock */
@media (hover:hover) and (pointer:fine){html:has(.layout){scrollbar-gutter:stable}}

/* ---- viewport units: iOS toolbars collapse, so 100vh is taller than what is visible ---- */
@media (min-width:881px){
  @supports (height:100dvh){.layout .sidebar{max-height:calc(100dvh - 49px)}}
  .layout .sidebar{overscroll-behavior:contain}
}
@supports (height:100dvh){#gl-panel{height:100dvh}}

/* ---- taps: no double-tap wait, a quiet highlight ---- */
a,button,summary,label,[role=button],.menu-btn,.navcard{touch-action:manipulation}
html{-webkit-tap-highlight-color:rgba(9,105,218,.10)}
"""
