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

# Same-site pages are prefetched when the pointer lingers on a link ("moderate" eagerness), so a lesson-to-lesson
# click finds the HTML already cached. Prefetch, not prerender: no page script runs early, so the glossary scan
# and mermaid never run twice. Browsers without Speculation Rules ignore the block.
SPECULATION_RULES = (
    '{"prefetch":[{"where":{"and":[{"href_matches":"/*"},{"not":{"href_matches":"/*/graph/*"}},'
    '{"not":{"href_matches":"/graph/*"}}]},"eagerness":"moderate"}]}'
)

# A short cross-fade between pages (cross-document view transitions). CSS only: no script, no scroll listeners.
# It holds rendering until the next page is ready, so keep it brief. Reduced-motion users and browsers without
# support navigate normally. The top bar and the desktop sidebar get their own layers, so they stay still while
# the page body fades. build_site.py leaves this block out of the graph page.
VIEW_TRANSITION_CSS = r"""
@media (prefers-reduced-motion:no-preference){
  @supports (view-transition-name:none){
    @view-transition{navigation:auto}
    .topbar{view-transition-name:site-topbar}
    @media (min-width:881px){.layout .sidebar{view-transition-name:site-sidebar}}
    ::view-transition-group(root){animation-duration:.15s}
    ::view-transition-old(root),::view-transition-new(root){animation-duration:.15s;animation-timing-function:ease}
    ::view-transition-group(site-topbar),::view-transition-group(site-sidebar){animation-duration:0s}
  }
}
"""

CSS = r"""
/* ---- anchors and programmatic scrolling ---- */
html{scroll-padding-top:84px}
@media (max-width:560px){html{scroll-padding-top:80px}}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto !important}}

/* ---- sticky bars: opaque, so the browser does not blend them over moving text ---- */
.topbar{background:var(--color-surface)}

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
  @supports (height:100dvh){.layout .sidebar{max-height:calc(100dvh - var(--topbar-height))}}
  .layout .sidebar{overscroll-behavior:contain}
}
@supports (height:100dvh){#gl-panel{height:100dvh}}

/* ---- taps: no double-tap wait, a quiet highlight ---- */
a,button,summary,label,[role=button],.navcard{touch-action:manipulation}
html{-webkit-tap-highlight-color:var(--color-background-primary-soft-alpha)}
"""
