#!/usr/bin/env python3
"""Doodle icons for the sketch infographics (explainer_figures.sketch).

Each icon is the inner markup of an SVG <symbol> on a 48 x 48 grid, drawn with simple lines and
shapes in `currentColor`, no fill unless marked. They are written for this site; nothing is traced
or copied. The sketch builder puts only the icons a figure uses into one <defs> block and refers
to them with <use>, and a small SVG filter makes the strokes look hand-drawn.

Add an icon: pick a short key, draw it on the 48 x 48 grid with round line caps in mind, keep the
strokes inside 4..44 so the wobble filter does not clip them.
"""

ICONS = {
    # people and places
    "person": '<circle cx="24" cy="14" r="7"/><path d="M10 42c1-9 7-14 14-14s13 5 14 14"/>',
    "building": '<path d="M10 42V12l14-6 14 6v30"/><path d="M6 42h36"/><path d="M17 18h4M27 18h4M17 26h4M27 26h4"/><path d="M21 42v-8h6v8"/>',
    "box": '<path d="M8 16l16-8 16 8v18l-16 8-16-8z"/><path d="M8 16l16 8 16-8"/><path d="M24 24v18"/><path d="M16 12l16 8"/>',
    "screen": '<rect x="6" y="9" width="36" height="24" rx="3"/><path d="M18 40h12M24 33v7"/><path d="M12 16h14M12 22h20"/>',
    # documents and data
    "document": '<path d="M12 6h17l9 9v27H12z"/><path d="M29 6v9h9"/><path d="M17 23h15M17 29h15M17 35h10"/>',
    "tag": '<path d="M6 24L22 8h18v18L24 42z"/><circle cx="32" cy="16" r="3"/>',
    "database": '<ellipse cx="24" cy="11" rx="14" ry="5"/><path d="M10 11v26c0 3 6 5 14 5s14-2 14-5V11"/><path d="M10 20c0 3 6 5 14 5s14-2 14-5M10 29c0 3 6 5 14 5s14-2 14-5"/>',
    "chart": '<path d="M7 41h34"/><path d="M11 41V27h6v14M21 41V17h6v24M31 41V9h6v32"/>',
    "image": '<rect x="6" y="9" width="36" height="30" rx="3"/><circle cx="17" cy="19" r="4"/><path d="M8 36l11-11 8 7 5-5 8 8"/>',
    "tokens": '<rect x="4" y="16" width="11" height="16" rx="3"/><rect x="18.5" y="16" width="11" height="16" rx="3"/><rect x="33" y="16" width="11" height="16" rx="3"/><path d="M9.5 21v6M24 21v6M38.5 21v6"/>',
    "window": '<rect x="6" y="8" width="36" height="32" rx="3"/><path d="M6 15h36"/><path d="M11 21h9M11 27h14M11 33h7"/><path d="M28 21h9v12h-9z"/>',
    # time, control, measurement
    "clock": '<circle cx="24" cy="24" r="16"/><path d="M24 14v10l7 5"/>',
    "gear": '<circle cx="24" cy="24" r="6"/><path d="M24 6v6M24 36v6M6 24h6M36 24h6M11 11l4 4M33 33l4 4M37 11l-4 4M15 33l-4 4"/><circle cx="24" cy="24" r="12"/>',
    "dial": '<path d="M8 32a16 16 0 0 1 32 0"/><path d="M24 32l9-11"/><circle cx="24" cy="32" r="2.5"/><path d="M12 26l2 1M24 16v3M36 26l-2 1"/>',
    "loop": '<path d="M36 20a13 13 0 1 0 1 9"/><path d="M38 12v9h-9"/>',
    "dice": '<rect x="9" y="9" width="30" height="30" rx="5"/><circle cx="17" cy="17" r="2"/><circle cx="31" cy="31" r="2"/><circle cx="24" cy="24" r="2"/><circle cx="31" cy="17" r="2"/><circle cx="17" cy="31" r="2"/>',
    # safety and access
    "shield": '<path d="M24 6l15 6v10c0 10-6 17-15 20C15 39 9 32 9 22V12z"/><path d="M17 24l5 5 9-10"/>',
    "lock": '<rect x="10" y="21" width="28" height="20" rx="3"/><path d="M16 21v-6a8 8 0 0 1 16 0v6"/><path d="M24 29v5"/>',
    "gateway": '<path d="M8 42V18a16 16 0 0 1 32 0v24"/><path d="M15 42V20a9 9 0 0 1 18 0v22"/><path d="M4 42h40"/><path d="M20 30l3 3 6-7"/>',
    "check": '<circle cx="24" cy="24" r="16"/><path d="M16 24l6 6 11-12"/>',
    "magnifier": '<circle cx="20" cy="20" r="11"/><path d="M28 28l12 12"/>',
    # machines and models
    "bot": '<rect x="10" y="15" width="28" height="22" rx="6"/><path d="M24 15V8"/><circle cx="24" cy="7" r="2"/><circle cx="18" cy="25" r="2.5"/><circle cx="30" cy="25" r="2.5"/><path d="M19 31h10"/>',
    "chip": '<rect x="13" y="13" width="22" height="22" rx="3"/><rect x="19" y="19" width="10" height="10"/><path d="M19 13V7M29 13V7M19 41v-6M29 41v-6M13 19H7M13 29H7M41 19h-6M41 29h-6"/>',
    "network": '<circle cx="10" cy="14" r="3.5"/><circle cx="10" cy="34" r="3.5"/><circle cx="24" cy="24" r="3.5"/><circle cx="38" cy="14" r="3.5"/><circle cx="38" cy="34" r="3.5"/><path d="M13 15l8 7M13 33l8-7M27 22l8-7M27 26l8 7M10 18v12M38 18v12"/>',
    "memory": '<path d="M8 14l16-7 16 7-16 7z"/><path d="M8 22l16 7 16-7"/><path d="M8 30l16 7 16-7"/>',
    "queue": '<circle cx="11" cy="17" r="4"/><circle cx="24" cy="17" r="4"/><circle cx="37" cy="17" r="4"/><path d="M5 34c0-5 3-8 6-8s6 3 6 8M18 34c0-5 3-8 6-8s6 3 6 8M31 34c0-5 3-8 6-8s6 3 6 8"/><path d="M5 40h38"/>',
    "batch": '<rect x="6" y="8" width="36" height="7" rx="2"/><rect x="6" y="20" width="26" height="7" rx="2"/><rect x="6" y="32" width="32" height="7" rx="2"/>',
    "stream": '<path d="M6 16h22M6 24h30M6 32h18"/><path d="M32 12l8 4-8 4M40 28l4 4-4 4"/>',
    "lightning": '<path d="M27 5L12 27h11l-3 16 16-23H25z"/>',
    # direction and reward
    "arrow": '<path d="M6 24h34"/><path d="M30 14l10 10-10 10"/>',
    "trophy": '<path d="M15 8h18v9a9 9 0 0 1-18 0z"/><path d="M15 11H8c0 7 4 10 8 10M33 11h7c0 7-4 10-8 10"/><path d="M24 26v8"/><path d="M16 42h16l-2-8H18z"/>',
}


def symbol(key):
    """One <symbol> element for an icon key."""
    return f'<symbol id="xs-i-{key}" viewBox="0 0 48 48">{ICONS[key]}</symbol>'
