#!/usr/bin/env python3
"""Rewrite literal colours in hand-built diagram HTML into Apps SDK UI semantic tokens.

Diagrams under diagrams/<track>/ are small self-contained HTML figures. They were written
with literal hex colours, which cannot follow the dark theme. This tool replaces each colour
with the semantic token that matches its role:

    hue family   -> info | success | warning | caution | danger | discovery   (SDK colour families)
    CSS property -> text colour, background, border, or shadow
    lightness    -> tint (surface) or solid

Run it on a file set to migrate it. Run `check_design_system.py` to find any literal colour
that is left. Dry run: `tokenize_colors.py --dry`. It is idempotent: tokens are not colours.
"""
import colorsys
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FG = {"color", "fill", "stroke", "caret-color", "text-decoration-color", "-webkit-text-fill-color"}
BG = {"background", "background-color", "stop-color"}
SHADOW = {"box-shadow", "text-shadow", "filter", "drop-shadow"}

HEX = r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b"
RGBA = r"rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(?:,\s*[\d.]+\s*)?\)"
COLOR = re.compile(f"{HEX}|{RGBA}")


def parse(c):
    c = c.strip()
    if c.startswith("#"):
        h = c[1:]
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        return r, g, b, 1.0
    nums = re.findall(r"[\d.]+", c)
    r, g, b = (int(float(n)) for n in nums[:3])
    a = float(nums[3]) if len(nums) > 3 else 1.0
    return r, g, b, a


def family(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    h *= 360
    if s < 0.14 or l > 0.985 or l < 0.03:
        return "neutral", l
    if h >= 345 or h < 15:
        return "danger", l
    if h < 40:
        return "warning", l
    if h < 70:
        return "caution", l
    if h < 200:
        return "success", l
    if h < 240:
        return "info", l
    return "discovery", l


def token_for(color, role):
    """role in fg | bg | bd | sh | attr_fg | attr_bg"""
    r, g, b, a = parse(color)
    fam, l = family(r, g, b)
    if role == "sh":
        if fam == "neutral" and l < 0.5:
            return f"rgb(var(--shadow-color) / {a:g})"
        if fam == "neutral":
            return f"color-mix(in oklab, var(--color-surface) {round(a * 100)}%, transparent)"
        return f"color-mix(in oklab, var(--color-background-{fam}-solid) {round(a * 100)}%, transparent)"
    if a < 1.0:   # translucent fills and borders: keep the alpha, swap the base colour
        if fam == "neutral" and l > 0.9:
            base = "var(--white)"
        elif fam == "neutral":
            base = "var(--color-text)"
        else:
            base = f"var(--color-background-{fam}-solid)"
        return f"color-mix(in oklab, {base} {round(a * 100)}%, transparent)"
    if fam == "neutral":
        if role == "fg":
            if l >= 0.97:
                return "var(--white)"
            if l < 0.22:
                return "var(--color-text)"
            return "var(--color-text-secondary)" if l < 0.5 else "var(--color-text-tertiary)"
        if role == "bg":
            if l >= 0.99:
                return "var(--color-surface)"
            if l >= 0.965:
                return "var(--color-surface-secondary)"
            if l >= 0.945:
                return "var(--color-surface-tertiary)"
            if l >= 0.85:
                return "var(--color-background-primary-soft)"
            if l >= 0.55:
                return "var(--color-background-primary-soft-active)"
            return "var(--color-background-primary-solid)" if l < 0.3 else "var(--color-background-secondary-solid)"
        # border
        if l >= 0.85:
            return "var(--color-border)"
        if l >= 0.55:
            return "var(--color-border-strong)"
        return "var(--color-text-secondary)"
    if role == "fg":
        return "var(--white)" if l >= 0.82 else f"var(--color-text-{fam})"
    if role == "bg":
        return f"var(--color-background-{fam}-surface)" if l >= 0.80 else f"var(--color-background-{fam}-solid)"
    return (f"var(--color-border-{fam}-surface)" if l >= 0.78 else f"var(--color-border-{fam}-outline)")


def role_of(prop):
    p = prop.lower()
    if p in FG:
        return "fg"
    if p in BG:
        return "bg"
    if p.startswith("border") or p.startswith("outline"):
        return "bd"
    if p in SHADOW:
        return "sh"
    return None


DECL = re.compile(r"([A-Za-z-]+)(\s*:\s*)([^;{}\"]*)")


def convert_css(text, stats):
    def one(m):
        prop, sep, val = m.group(1), m.group(2), m.group(3)
        role = role_of(prop)
        if role is None or not COLOR.search(val):
            return m.group(0)
        def sub(cm):
            t = token_for(cm.group(0), role)
            stats[(role, cm.group(0).lower(), t)] = stats.get((role, cm.group(0).lower(), t), 0) + 1
            return t
        return prop + sep + COLOR.sub(sub, val)
    return DECL.sub(one, text)


ATTR = re.compile(r'<(\w+)([^>]*?)\b(fill|stroke|stop-color)="(#[0-9A-Fa-f]{3,6})"')


def convert_attrs(text, stats):
    def one(m):
        tag, mid, attr, col = m.group(1), m.group(2), m.group(3), m.group(4)
        if attr == "stroke":
            role = "bd"
        elif tag == "text":
            role = "fg"
        else:
            role = "bg"
        t = token_for(col, role)
        stats[(role, col.lower(), t)] = stats.get((role, col.lower(), t), 0) + 1
        return f'<{tag}{mid}{attr}="{t}"'
    return ATTR.sub(one, text)


def convert(text, stats):
    text = convert_css(text, stats)
    while True:   # an element can carry several colour attributes; the pattern takes one per pass
        nxt = convert_attrs(text, stats)
        if nxt == text:
            return text
        text = nxt


def main(argv):
    dry = "--dry" in argv
    files = sorted(glob.glob(os.path.join(ROOT, "diagrams", "**", "*.html"), recursive=True))
    stats, changed = {}, 0
    for f in files:
        s = open(f, encoding="utf-8").read()
        n = convert(s, stats)
        if n != s:
            changed += 1
            if not dry:
                open(f, "w", encoding="utf-8").write(n)
    print(f"{changed}/{len(files)} files {'would change' if dry else 'rewritten'}; {sum(stats.values())} colours")
    if dry:
        by = {}
        for (role, col, tok), n in stats.items():
            by.setdefault((col, tok, role), 0)
            by[(col, tok, role)] += n
        for (col, tok, role), n in sorted(by.items(), key=lambda kv: -kv[1])[:60]:
            print(f"{n:5d} {role} {col:>10} -> {tok}")


if __name__ == "__main__":
    main(sys.argv[1:])
