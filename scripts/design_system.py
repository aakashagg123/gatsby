#!/usr/bin/env python3
"""The site's design system: OpenAI's Apps SDK UI, plus a thin site layer.

Why this module exists
----------------------
Every page of the site is styled from ONE stylesheet, `assets/ds.css`, built here.
It has three parts, in cascade-layer order:

  1. `theme`      OpenAI Apps SDK UI design tokens (colour, type, radius, shadow,
                  control sizes), light and dark. Vendored verbatim.
  2. `base`       A Tailwind-preflight subset the SDK assumes (design-system/preflight.css),
                  then the SDK's own resets.
  3. `components` The SDK's own component CSS (Button, Badge, Alert, TextLink, Menu,
                  Popover, Tooltip, SegmentedControl, Switch, Input, CodeBlock,
                  Markdown). Vendored verbatim. Pages use the SDK markup and class names.
  4. `site`       Our layout and prose, written only with SDK tokens. See design-system/site/.

Rules for site CSS (see design-system/README.md):
  * No hex, rgb() or named colours. Use a semantic token such as --color-text.
  * No new font sizes. Use --font-text-*-size or --font-heading-*-size.
  * Radii come from --radius-*. Spacing is a multiple of --spacing (4px).
  * A new surface, control or message uses an SDK component before custom CSS.

Why `data-theme`: the tokens switch on [data-theme="light"|"dark"] on <html>.
`THEME_BOOT` sets it before first paint from the saved choice or the system setting.
"""
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS = os.path.join(ROOT, "design-system")
VENDOR = os.path.join(DS, "vendor", "apps-sdk-ui")
SITE = os.path.join(DS, "site")

TOKEN_FILES = ["variables-primitive.css", "variables-semantic.css", "variables-components.css"]
GLOBAL_FILES = ["base.css", "globals.css"]
COMPONENTS = ["Alert", "Badge", "Button", "CodeBlock", "EmptyMessage", "Indicator", "Input",
              "Markdown", "Menu", "Popover", "SegmentedControl", "Switch", "TextLink", "Tooltip"]

# The SDK ships CSS Modules with unhashed names. Three class names exist in two components
# each. We concatenate every component into one sheet, so we prefix the clashing ones.
CLASH = {("Input", "Container"): "InputContainer", ("Switch", "Container"): "SwitchContainer",
         ("EmptyMessage", "Title"): "EmptyMessageTitle",
         ("EmptyMessage", "Description"): "EmptyMessageDescription"}

# Tailwind v4 default tracking scale. The SDK's heading tokens reference --tracking-*,
# which Tailwind supplies in the SDK's own build. We have no Tailwind, so we define it.
TAILWIND_GAPS = """
@layer theme{
  :root{
    --tracking-tighter:-0.05em;--tracking-tight:-0.025em;--tracking-normal:0em;
    --tracking-wide:0.025em;--tracking-wider:0.05em;--tracking-widest:0.1em;
    --leading-tight:1.25;--leading-snug:1.375;--leading-normal:1.5;--leading-relaxed:1.625;
  }
}
"""

# Runs in <head> before first paint. Saved choice wins; otherwise follow the system.
# Choices: "light", "dark" or absent (= follow the system).
THEME_BOOT = ("<script>(function(){var d=document.documentElement,t=null;"
              "try{t=localStorage.getItem('ds-theme')}catch(e){}"
              "if(t!=='light'&&t!=='dark'){t=(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light'}"
              "d.setAttribute('data-theme',t)})()</script>")


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _strip_blocks(css, header_re):
    """Remove `@something ... { ... }` blocks (balanced braces) and one-line at-rules."""
    out, i = [], 0
    rx = re.compile(header_re)
    while True:
        m = rx.search(css, i)
        if not m:
            out.append(css[i:])
            break
        out.append(css[i:m.start()])
        j = css.find("{", m.end() - 1) if css[m.end() - 1] != "{" else m.end() - 1
        depth, k = 0, j
        while k < len(css):
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        i = k + 1
    return "".join(out)


def _tailwind_to_plain(css):
    """The SDK ships a few Tailwind-only directives. Make them plain CSS."""
    css = _strip_blocks(css, r"@custom-variant\b[^{;]*\{")
    css = re.sub(r"@custom-variant\b[^;{]*;", "", css)
    # @theme static holds the SDK's font, radius and spacing tokens. Keep them in the theme layer
    # so the site layer can override them (an unlayered :root rule would beat every layer).
    i = css.find("@theme static {")
    if i != -1:
        depth, k = 0, css.find("{", i)
        j = k
        while j < len(css):
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        css = css[:i] + "@layer theme {\n:root {" + css[k + 1:j] + "}\n}" + css[j + 1:]
    # `--font-weight-*: initial;` resets a Tailwind namespace. It is not valid CSS here.
    css = re.sub(r"^\s*--[a-z0-9-]*\*:\s*initial;\s*$", "", css, flags=re.M)
    return css


def build_css():
    """Return the full ds.css text."""
    parts = ["/* ds.css — generated by scripts/design_system.py. Do not edit. */\n"
             "/* Tokens and components: OpenAI Apps SDK UI 0.2.2, MIT. See design-system/vendor. */\n"
             "@layer theme, base, components, site;\n",
             _read(os.path.join(DS, "fonts", "google-sans.css")), TAILWIND_GAPS]
    for f in TOKEN_FILES:
        parts.append(_tailwind_to_plain(_read(os.path.join(VENDOR, "styles", f))))
    parts.append(_read(os.path.join(DS, "preflight.css")))
    for f in GLOBAL_FILES:
        parts.append(_tailwind_to_plain(_read(os.path.join(VENDOR, "styles", f))))
    for c in COMPONENTS:
        css = _tailwind_to_plain(_read(os.path.join(VENDOR, "components", c + ".css")))
        for (comp, old), new in CLASH.items():
            if comp == c:
                css = re.sub(rf"\.{old}\b", "." + new, css)
        parts.append(css)
    site = sorted(f for f in os.listdir(SITE) if f.endswith(".css"))
    parts.append("@layer site{\n" + "\n".join(_read(os.path.join(SITE, f)) for f in site) + "\n}\n")
    return "\n".join(parts)


def head_tags(root):
    """Tags injected at the top of <head> on every page. `root` is the relative path
    from the page to the site root, such as '' or '../'."""
    return (f'<link rel="preload" as="font" type="font/woff2" crossorigin '
            f'href="{root}assets/fonts/google-sans-latin-wght-normal.woff2">'
            f'<link rel="stylesheet" href="{root}assets/ds.css">' + THEME_BOOT
            + f'<script defer src="{root}assets/ds.js"></script>')


FONT_FILES = ["google-sans-latin-wght-normal.woff2", "google-sans-latin-wght-italic.woff2",
              "google-sans-latin-ext-wght-normal.woff2", "google-sans-latin-ext-wght-italic.woff2"]


def write_assets(assets_dir):
    os.makedirs(assets_dir, exist_ok=True)
    fonts_out = os.path.join(assets_dir, "fonts")
    os.makedirs(fonts_out, exist_ok=True)
    for f in FONT_FILES:
        shutil.copy(os.path.join(DS, "fonts", "google-sans", f), os.path.join(fonts_out, f))
    css = build_css()
    with open(os.path.join(assets_dir, "ds.css"), "w", encoding="utf-8") as f:
        f.write(css)
    with open(os.path.join(assets_dir, "ds.js"), "w", encoding="utf-8") as f:
        f.write(_read(os.path.join(DS, "ds.js")))
    return len(css)


# ---- SDK markup helpers ----------------------------------------------------------
# These emit the same DOM the React components render, so the vendored CSS applies as is.

def badge(text, color="secondary", variant="soft", size="sm", pill=False, extra=""):
    p = ' data-pill=""' if pill else ""
    return (f'<span class="Badge" data-color="{color}" data-size="{size}" '
            f'data-variant="{variant}"{p}{extra}>{text}</span>')


def button_link(text, href, color="primary", variant="solid", size="md", pill=True, extra=""):
    p = ' data-pill=""' if pill else ""
    return (f'<a class="Button" href="{href}" data-color="{color}" data-variant="{variant}" '
            f'data-size="{size}"{p}{extra}><span class="ButtonInner">{text}</span></a>')


def text_link(text, href, primary=False):
    attrs = ' data-primary=""' if primary else ' data-underline=""'
    return f'<a class="TextLink" href="{href}"{attrs}>{text}</a>'


INFO_ICON = ('<svg viewBox="0 0 20 20" width="20" height="20" fill="currentColor" aria-hidden="true">'
             '<path d="M10 2a8 8 0 1 0 0 16 8 8 0 0 0 0-16Zm0 3.25a1 1 0 1 1 0 2 1 1 0 0 1 0-2Zm1.25 9.25h-2.5a.75.75 0 0 1 0-1.5h.5v-3h-.5a.75.75 0 0 1 0-1.5h1.25a.75.75 0 0 1 .75.75V13h.5a.75.75 0 0 1 0 1.5Z"/></svg>')


MENU_ICON = ('<svg viewBox="0 0 20 20" width="20" height="20" fill="none" stroke="currentColor" '
             'stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M3.5 5.5h13M3.5 10h13M3.5 14.5h13"/></svg>')


def alert(title, description, color="secondary", variant="soft", icon=True):
    ind = f'<div class="Indicator">{INFO_ICON}</div>' if icon else ""
    t = f'<div class="Title">{title}</div>' if title else ""
    d = f'<div class="Description">{description}</div>' if description else ""
    return (f'<div class="Alert" data-variant="{variant}" data-color="{color}">{ind}'
            f'<div class="Content"><div class="Message">{t}{d}</div></div></div>')


if __name__ == "__main__":
    out = os.path.join(ROOT, "_site", "assets")
    n = write_assets(out)
    print(f"wrote {out}/ds.css ({n // 1024} KB)")
