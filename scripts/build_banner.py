#!/usr/bin/env python3
"""Build the README banner in the site's design system, as a light and a dark SVG.

An SVG shown through <img> cannot read CSS variables, so the colours below are the resolved
values of the Apps SDK UI tokens (checked against the built site, light and dark). Google Sans
is embedded as a data URI, because an <img> SVG cannot load web fonts from a file. The font is
the same variable woff2 the site serves (SIL Open Font License 1.1, see
design-system/fonts/google-sans/OFL.txt).

The README picks the right file with <picture> and prefers-color-scheme.
Run:  python3 scripts/build_banner.py     # -> assets/banner-light.svg, assets/banner-dark.svg
"""
import base64
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "design-system", "fonts", "google-sans", "google-sans-latin-wght-normal.woff2")

# Resolved token values. Keys name the token they come from.
THEMES = {
    "light": {
        "surface": "#ffffff", "surface-secondary": "#f9f9f9", "surface-tertiary": "#f3f3f3",
        "text": "#0d0d0d", "text-secondary": "#5d5d5d", "text-tertiary": "#8f8f8f",
        "border": "#0a0a0a", "border-opacity": "0.10", "accent": "#0285ff",
    },
    "dark": {
        "surface": "#212121", "surface-secondary": "#181818", "surface-tertiary": "#131313",
        "text": "#ffffff", "text-secondary": "#afafaf", "text-tertiary": "#8f8f8f",
        "border": "#ffffff", "border-opacity": "0.12", "accent": "#0285ff",
    },
}

PILLS = ["Learning paths", "Foundations", "Generative AI", "Agents", "Quality and safety", "Systems", "Product craft"]
SPARK = "M50 8 L58 42 L92 50 L58 58 L50 92 L42 58 L8 50 L42 42 Z"       # the site's logo mark


def pill_row(t, x, y):
    out, cx = [], x
    for i, label in enumerate(PILLS):
        w = int(len(label) * 7.3 + 40)
        out.append(
            f'<rect x="{cx}" y="{y}" width="{w}" height="34" rx="17" fill="{t["surface-secondary"]}" '
            f'stroke="{t["border"]}" stroke-opacity="{t["border-opacity"]}"/>'
            f'<circle cx="{cx + 17}" cy="{y + 17}" r="3.5" fill="{t["accent"] if i == 0 else t["text-tertiary"]}"/>'
            f'<text x="{cx + 29}" y="{y + 22}" font-size="14" font-weight="500" fill="{t["text-secondary"]}">{label}</text>')
        cx += w + 8
    assert cx - 8 <= 1232, f"the pills run past the banner edge ({cx - 8})"
    return "\n  ".join(out)


def build(name, t, font_b64):
    return f'''<svg width="1280" height="340" viewBox="0 0 1280 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AI Engineering: from scratch to production. A linked curriculum for Senior and Principal PMs going AI-native.">
  <defs>
    <style>
      @font-face {{ font-family: "Google Sans"; font-style: normal; font-weight: 400 700;
        src: url(data:font/woff2;base64,{font_b64}) format("woff2"); }}
      text {{ font-family: "Google Sans", ui-sans-serif, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }}
    </style>
  </defs>
  <rect width="1280" height="340" rx="20" fill="{t["surface"]}"/>
  <rect x="0.5" y="0.5" width="1279" height="339" rx="19.5" fill="none" stroke="{t["border"]}" stroke-opacity="{t["border-opacity"]}"/>

  <g transform="translate(96,118)">
    <circle cx="52" cy="52" r="52" fill="{t["surface-tertiary"]}"/>
    <path d="{SPARK}" fill="{t["text"]}"/>
  </g>

  <text x="248" y="140" font-size="58" font-weight="600" letter-spacing="-1.2" fill="{t["text"]}">AI Engineering</text>
  <text x="250" y="186" font-size="30" font-weight="400" fill="{t["text-secondary"]}">From scratch to production</text>
  <text x="250" y="230" font-size="20" font-weight="400" fill="{t["text-tertiary"]}">A linked curriculum for Senior and Principal PMs going AI-native.</text>

  {pill_row(t, 250, 262)}
</svg>
'''


def main():
    with open(FONT, "rb") as f:
        font_b64 = base64.b64encode(f.read()).decode()
    for name, t in THEMES.items():
        path = os.path.join(ROOT, "assets", f"banner-{name}.svg")
        with open(path, "w") as f:
            f.write(build(name, t, font_b64))
        print(f"wrote {os.path.relpath(path, ROOT)} ({os.path.getsize(path) // 1024} KB)")


if __name__ == "__main__":
    main()
