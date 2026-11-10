#!/usr/bin/env python3
"""Figure builders for the Visual explainers section.

Each function returns one self-contained HTML fragment (a <style> block and a card) that replaces a mermaid fence
through diagrams/explainers/<page-key>-<n>.html. Colours use design-system tokens only, so every figure follows the
light and dark themes. Figures wrap on a phone, and never need horizontal scrolling.

Families (by meaning): info, success, caution, danger, discovery, warning, plain.
"""
import html as _h

FAMILIES = {
    "info": ("info-surface", "info-surface", "info"),
    "success": ("success-surface", "success-surface", "success"),
    "caution": ("caution-surface", "caution-outline", "caution"),
    "danger": ("danger-surface", "danger-surface", "danger"),
    "discovery": ("discovery-surface", "discovery-surface", "discovery"),
    "warning": ("warning-surface", "warning-surface", "warning"),
}
CYCLE = ["info", "discovery", "success", "caution", "warning", "danger"]


def _e(s):
    return _h.escape(str(s), quote=False)


CSS = """<style>
.xf{background:var(--color-surface);border:1px solid var(--color-border);border-top:3px solid var(--color-border-discovery-outline);
  border-radius:16px;padding:28px 24px 20px;box-shadow:0 1px 3px rgb(var(--shadow-color) / 0.04),0 8px 24px rgb(var(--shadow-color) / 0.04);
  margin:26px 0;max-width:100%;font-family:inherit;text-align:left;position:relative;color:var(--color-text)}
.xf-chip{position:absolute;top:-11px;left:22px;background:var(--color-background-discovery-solid);color:var(--white);
  font-size:10.5px;font-weight:700;letter-spacing:1px;text-transform:uppercase;border-radius:20px;padding:3px 12px}
.xf h4{margin:0 0 4px;font-size:11px;font-weight:700;letter-spacing:.4px;text-transform:uppercase;color:var(--color-text-secondary)}
.xf-sub{font-size:12px;color:var(--color-text-secondary);margin:0 0 14px;line-height:1.45}
.xf-note{margin:14px 0 0;font-size:11px;color:var(--color-text-tertiary);text-align:center;line-height:1.45}
.xf-box{border-radius:12px;padding:10px 12px;border:1px solid var(--color-border);background:var(--color-surface-secondary);min-width:0}
.xf-box b{display:block;font-size:12px;margin-bottom:3px;line-height:1.3}
.xf-box span{display:block;font-size:10.5px;line-height:1.4;color:var(--color-text-secondary)}
.xf-info{background:var(--color-background-info-surface);border-color:var(--color-border-info-surface)}
.xf-success{background:var(--color-background-success-surface);border-color:var(--color-border-success-surface)}
.xf-caution{background:var(--color-background-caution-surface);border-color:var(--color-border-caution-outline)}
.xf-danger{background:var(--color-background-danger-surface);border-color:var(--color-border-danger-surface)}
.xf-discovery{background:var(--color-background-discovery-surface);border-color:var(--color-border-discovery-surface)}
.xf-warning{background:var(--color-background-warning-surface);border-color:var(--color-border-warning-surface)}
.xf-flow{display:flex;flex-wrap:nowrap;align-items:stretch;gap:6px}
.xf-flow .xf-box{flex:1 1 0}
.xf-ar{flex:0 0 auto;align-self:center;color:var(--color-text-tertiary);font-size:14px;line-height:1}
.xf-ar::before{content:"\\2192"}
.xf-toks{display:flex;flex-wrap:wrap;gap:8px}
.xf-tok{display:flex;flex-direction:column;align-items:center;gap:3px}
.xf-tok i{font-style:normal;font-weight:700;font-size:13px;border-radius:8px;padding:5px 9px;border:1px solid var(--color-border);white-space:pre}
.xf-tok em{font-style:normal;font-size:10px;color:var(--color-text-tertiary);font-variant-numeric:tabular-nums}
.xf-layers{display:flex;flex-direction:column;gap:6px;align-items:stretch}
.xf-layers .xf-box{display:flex;gap:10px;align-items:baseline;justify-content:space-between}
.xf-layers .xf-box b{margin:0;flex:0 0 auto}
.xf-layers .xf-box span{text-align:right}
.xf-lanes{display:grid;grid-template-columns:auto 1fr;gap:6px 10px;align-items:center}
.xf-lbl{font-size:11px;font-weight:700;color:var(--color-text-secondary)}
.xf-track{display:flex;gap:3px;min-width:0}
.xf-seg{border-radius:6px;padding:6px 4px;font-size:10px;text-align:center;border:1px solid var(--color-border);background:var(--color-surface-secondary);min-width:0;overflow:hidden}
.xf-mem{display:flex;height:34px;border-radius:8px;overflow:hidden;border:1px solid var(--color-border)}
.xf-mem div{display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;min-width:0;overflow:hidden;white-space:nowrap}
.xf-mkey{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:10px;font-size:10.5px;color:var(--color-text-secondary)}
.xf-mkey b{color:var(--color-text)}
.xf-bars{display:grid;grid-template-columns:minmax(0,auto) minmax(0,1fr) auto;gap:6px 10px;align-items:center}
.xf-bars .xf-lbl{white-space:nowrap}
.xf-fill{height:16px;border-radius:5px;border:1px solid var(--color-border);background:var(--color-surface-secondary);overflow:hidden}
.xf-fill div{height:100%;border-radius:4px}
.xf-val{font-size:11px;font-variant-numeric:tabular-nums;color:var(--color-text-secondary)}
.xf-grid{display:grid;gap:3px}
.xf-cell{border-radius:5px;min-height:22px;font-size:10px;display:flex;align-items:center;justify-content:center;border:1px solid var(--color-border);background:var(--color-surface-secondary);color:var(--color-text-secondary);font-variant-numeric:tabular-nums}
.xf-cmp{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.xf-cmp ul{margin:6px 0 0;padding-left:16px;font-size:10.5px;color:var(--color-text-secondary);line-height:1.5}
.xf-heat{display:grid;gap:3px;font-variant-numeric:tabular-nums}
.xf-hh{font-size:10.5px;font-weight:700;color:var(--color-text-secondary);display:flex;align-items:center;justify-content:center;padding:2px}
@media (max-width:640px){
  .xf{padding:24px 14px 16px}
  .xf-flow{flex-direction:column}
  .xf-ar{align-self:center}
  .xf-ar::before{content:"\\2193"}
  .xf-cmp{grid-template-columns:1fr}
  .xf-layers .xf-box{flex-direction:column;gap:2px}
  .xf-layers .xf-box span{text-align:left}
}
</style>
"""


def _fam(f):
    return f"xf-{f}" if f in FAMILIES else ""


def _bg(f):
    return f"var(--color-background-{FAMILIES[f][0]})" if f in FAMILIES else "var(--color-surface-secondary)"


def _solid(f):
    return f"var(--color-background-{FAMILIES[f][2]}-solid)" if f in FAMILIES else "var(--color-background-discovery-solid)"


def card(chip, title, sub, body, note=""):
    out = f'<div class="xf"><span class="xf-chip">{_e(chip)}</span><h4>{_e(title)}</h4>'
    if sub:
        out += f'<p class="xf-sub">{_e(sub)}</p>'
    out += body
    if note:
        out += f'<p class="xf-note">{_e(note)}</p>'
    return CSS + out + "</div>\n"


def flow(chip, title, sub, nodes, note=""):
    """nodes: (family, title, text). Boxes joined by arrows."""
    parts = []
    for i, (f, t, x) in enumerate(nodes):
        if i:
            parts.append('<span class="xf-ar" aria-hidden="true"></span>')
        parts.append(f'<div class="xf-box {_fam(f)}"><b>{_e(t)}</b><span>{_e(x)}</span></div>')
    return card(chip, title, sub, f'<div class="xf-flow">{"".join(parts)}</div>', note)


def tokens(chip, title, sub, toks, note="", ids=True):
    """toks: list of (text, id). Chips cycle through colour families."""
    cells = []
    for i, (t, n) in enumerate(toks):
        f = CYCLE[i % len(CYCLE)]
        idtxt = f"<em>{_e(n)}</em>" if ids else ""
        cells.append(f'<div class="xf-tok"><i class="{_fam(f)}" style="background:{_bg(f)}">{_e(t)}</i>{idtxt}</div>')
    return card(chip, title, sub, f'<div class="xf-toks">{"".join(cells)}</div>', note)


def layers_body(rows):
    """The inner markup of layers(), for figures that combine more than one view in one card."""
    body = "".join(f'<div class="xf-box {_fam(f)}"><b>{_e(a)}</b><span>{_e(b)}</span></div>' for f, a, b in rows)
    return f'<div class="xf-layers">{body}</div>'


def layers(chip, title, sub, rows, note=""):
    """rows: (family, label, text), drawn top to bottom."""
    return card(chip, title, sub, layers_body(rows), note)


def lanes(chip, title, sub, rows, note=""):
    """rows: (label, [(family, text, weight)]). Segment widths follow the weights."""
    out = []
    for label, segs in rows:
        out.append(f'<div class="xf-lbl">{_e(label)}</div>')
        s = "".join(f'<div class="xf-seg {_fam(f)}" style="flex:{w} 1 0">{_e(t)}</div>' for f, t, w in segs)
        out.append(f'<div class="xf-track">{s}</div>')
    return card(chip, title, sub, f'<div class="xf-lanes">{"".join(out)}</div>', note)


def membar(chip, title, sub, segs, note=""):
    """segs: (family, label, value, legend). A stacked bar whose widths follow the values."""
    total = sum(v for _, _, v, _ in segs) or 1
    # Small segments cannot fit a label; the legend below names every segment.
    bar = "".join(
        f'<div style="flex:{v} 1 0;background:{_bg(f)}">{_e(lbl) if v / total >= 0.12 else ""}</div>'
        for f, lbl, v, _ in segs)
    key = "".join(f'<span><b>{_e(lbl)}</b> {_e(leg)}</span>' for _, lbl, _, leg in segs)
    return card(chip, title, sub, f'<div class="xf-mem">{bar}</div><div class="xf-mkey">{key}</div>', note)


def bars_body(rows, vmax=1.0, fmt="{:.2f}"):
    """The inner markup of bars(), for figures that combine more than one view in one card."""
    out = []
    for label, v, f in rows:
        pct = max(0.0, min(100.0, 100.0 * v / vmax))
        out.append(f'<div class="xf-lbl">{_e(label)}</div>'
                   f'<div class="xf-fill"><div style="width:{pct:.1f}%;background:{_solid(f)}"></div></div>'
                   f'<div class="xf-val">{_e(fmt.format(v))}</div>')
    return f'<div class="xf-bars">{"".join(out)}</div>'


def bars(chip, title, sub, rows, vmax=1.0, note="", fmt="{:.2f}"):
    """rows: (label, value, family). Horizontal bars scaled to vmax."""
    return card(chip, title, sub, bars_body(rows, vmax, fmt), note)


def grid(chip, title, sub, rows, cols_label=None, note=""):
    """rows: list of rows; each row is a list of (text, family or None). Equal-width cells."""
    ncols = max(len(r) for r in rows)
    cells = []
    for r in rows:
        for t, f in r:
            st = f' style="background:{_bg(f)}"' if f else ""
            cells.append(f'<div class="xf-cell {_fam(f)}"{st}>{_e(t)}</div>')
    return card(chip, title, sub, f'<div class="xf-grid" style="grid-template-columns:repeat({ncols},minmax(0,1fr))">{"".join(cells)}</div>', note)


def compare_body(left, right):
    """The inner markup of compare(), for figures that combine more than one view in one card."""
    def col(c):
        f, h, items = c
        li = "".join(f"<li>{_e(i)}</li>" for i in items)
        return f'<div class="xf-box {_fam(f)}"><b>{_e(h)}</b><ul>{li}</ul></div>'
    return f'<div class="xf-cmp">{col(left)}{col(right)}</div>'


def compare(chip, title, sub, left, right, note=""):
    """left and right: (family, heading, [bullets])."""
    return card(chip, title, sub, compare_body(left, right), note)


def heat(chip, title, sub, row_labels, col_labels, values, note="", fmt="{:.2f}"):
    """A table of weights; cell shade follows the value (0..1)."""
    n = len(col_labels)
    cells = ['<div class="xf-hh"></div>'] + [f'<div class="xf-hh">{_e(c)}</div>' for c in col_labels]
    for lbl, row in zip(row_labels, values):
        cells.append(f'<div class="xf-hh" style="justify-content:flex-end">{_e(lbl)}</div>')
        for v in row:
            if v is None:
                cells.append('<div class="xf-cell" style="opacity:.45">·</div>')
            else:
                pct = int(round(100 * min(1.0, v)))
                cells.append(f'<div class="xf-cell" style="background:color-mix(in srgb, var(--color-background-discovery-solid) {pct}%, var(--color-surface));'
                             f'color:{"var(--white)" if pct > 55 else "var(--color-text)"}">{_e(fmt.format(v))}</div>')
    return card(chip, title, sub, f'<div class="xf-heat" style="grid-template-columns:auto repeat({n},minmax(0,1fr))">{"".join(cells)}</div>', note)


# ---------------------------------------------------------------- Sketch infographic
# A hand-drawn "whiteboard" summary: numbered steps left to right with doodle icons, dashed
# connectors, a caption per step, optional labelled sub-icons, an optional progress arrow and a
# summary band. Ink is the info blue and the paper is the surface mixed toward the warning (cream)
# surface, so both follow the light and dark themes. Text uses --font-hand, which falls back to the
# site sans font. Icons live in sketch_icons.py; a small SVG filter wobbles the strokes.

SKETCH_CSS = """<style>
.xs{--xs-ink:var(--color-text-info);--xs-paper:color-mix(in srgb,var(--color-background-warning-surface) 45%,var(--color-surface));
  background:var(--xs-paper);color:var(--xs-ink);border:2px dashed color-mix(in srgb,var(--xs-ink) 40%,transparent);border-radius:18px;
  padding:30px 22px 22px;margin:26px 0;max-width:100%;position:relative;font-family:var(--font-hand);text-align:left}
[data-theme="dark"] .xs{--xs-paper:color-mix(in srgb,var(--color-surface-secondary) 70%,var(--color-surface))}
.xs-defs{position:absolute;width:0;height:0;overflow:hidden}
.xs li{margin:0}
.xs svg{fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;overflow:visible}
.xs-ico,.xs-subs svg,.xs-conn svg,.xs-prog svg,.xs-sum svg{filter:url(#xs-rough)}
.xs-chip{position:absolute;top:-12px;left:22px;background:var(--xs-paper);color:var(--xs-ink);border:2px solid var(--xs-ink);border-radius:20px;
  padding:1px 12px;font-size:var(--font-text-sm-size);line-height:1.4}
.xs-title{margin:0;color:inherit;text-align:center;font-weight:400;font-size:var(--font-heading-md-size);line-height:1.2}
.xs-sub{margin:4px 0 18px;text-align:center;font-size:var(--font-text-md-size);line-height:1.3;color:color-mix(in srgb,var(--xs-ink) 75%,var(--color-text))}
.xs-steps{display:flex;align-items:stretch;gap:2px}
.xs-step{flex:1 1 0;min-width:0;display:flex;flex-direction:column;align-items:center;text-align:center}
.xs-num{width:32px;height:32px;border:2px solid currentColor;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:var(--font-text-md-size);line-height:1}
.xs-ico{width:58px;height:58px;margin:8px 0 6px}
.xs-step b{font-weight:400;font-size:var(--font-text-lg-size);line-height:1.15;overflow-wrap:break-word}
.xs-step p{margin:4px 0 0;font-size:var(--font-text-sm-size);line-height:1.3;color:color-mix(in srgb,var(--xs-ink) 70%,var(--color-text));overflow-wrap:break-word}
.xs-subs{list-style:none;margin:10px 0 0;padding:8px 0 0;border-top:2px dotted color-mix(in srgb,var(--xs-ink) 45%,transparent);
  display:flex;flex-direction:column;gap:7px;width:100%}
.xs-subs li{display:flex;align-items:center;gap:6px;min-width:0;text-align:left;font-size:var(--font-text-xs-size);line-height:1.15;overflow-wrap:break-word}
.xs-subs svg{flex:0 0 auto;width:24px;height:24px}
.xs-subs span{min-width:0}
.xs-conn{flex:0 0 24px;align-self:flex-start;margin-top:52px;display:flex;justify-content:center}
.xs-conn svg{width:24px;height:16px}
.xs-prog{margin-top:22px}
.xs-prog ol{list-style:none;margin:0 0 2px;padding:0;display:flex;justify-content:space-between;gap:6px;flex-wrap:wrap;font-size:var(--font-text-md-size)}
.xs-prog svg{display:block;width:100%;height:16px}
.xs-sum{margin-top:18px;border:2px solid currentColor;border-radius:16px;padding:10px 16px;display:flex;align-items:center;gap:14px}
.xs-sum svg{flex:0 0 auto;width:40px;height:40px}
.xs-sum div{min-width:0}
.xs-sum strong{display:block;font-weight:400;font-size:var(--font-text-lg-size);line-height:1.25}
.xs-sum span{display:block;margin-top:6px;padding-top:6px;border-top:2px dashed color-mix(in srgb,var(--xs-ink) 45%,transparent);
  font-size:var(--font-text-sm-size);line-height:1.3;color:color-mix(in srgb,var(--xs-ink) 70%,var(--color-text))}
.xs-note{margin:12px 0 0;text-align:center;font-size:var(--font-text-sm-size);color:color-mix(in srgb,var(--xs-ink) 65%,var(--color-text))}
@media (max-width:640px){
  .xs{padding:28px 14px 16px}
  .xs-steps{flex-direction:column;align-items:stretch}
  .xs-conn{align-self:center;margin:2px 0;transform:rotate(90deg)}
  .xs-subs{flex-direction:row;flex-wrap:wrap;justify-content:center;gap:8px 6px}
  .xs-subs li{flex-direction:column;flex:0 1 72px;gap:2px;text-align:center}
  .xs-prog ol{justify-content:center;gap:4px 10px}
}
</style>
"""

_ROUGH = ('<filter id="xs-rough" x="-10%" y="-10%" width="120%" height="120%">'
          '<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/>'
          '<feDisplacementMap in="SourceGraphic" scale="2.2"/></filter>')


def _icon(key, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 48 48" aria-hidden="true"><use href="#xs-i-{key}"/></svg>'


def sketch(chip, title, sub, steps, progress=None, summary=None, note=""):
    """steps: 3 to 5 dicts with heading, caption, icon and optional subs [(icon, label)] (3 to 4).
    progress: optional list of stage names for the bottom arrow. summary: optional (trophy line, so-far note or "")."""
    import sketch_icons as SI
    assert 3 <= len(steps) <= 5, "a sketch has 3 to 5 steps"
    keys = []
    for st in steps:
        keys.append(st["icon"])
        keys += [k for k, _ in st.get("subs", [])]
    if summary:
        keys.append("trophy")
    seen = []
    for k in keys:
        if k not in seen:
            seen.append(k)
    defs = (f'<svg class="xs-defs" aria-hidden="true" focusable="false"><defs>{_ROUGH}'
            + "".join(SI.symbol(k) for k in seen) + "</defs></svg>")
    parts = []
    arrow = '<div class="xs-conn" aria-hidden="true"><svg viewBox="0 0 24 16"><path d="M2 8h18" stroke-dasharray="3 4"/><path d="M15 3l6 5-6 5"/></svg></div>'
    for i, st in enumerate(steps, 1):
        if i > 1:
            parts.append(arrow)
        subs = st.get("subs", [])
        sub_html = ""
        if subs:
            sub_html = '<ul class="xs-subs">' + "".join(f"<li>{_icon(k)}<span>{_e(lbl)}</span></li>" for k, lbl in subs) + "</ul>"
        parts.append(f'<div class="xs-step"><div class="xs-num">{i}</div>{_icon(st["icon"], "xs-ico")}'
                     f'<b>{_e(st["heading"])}</b><p>{_e(st["caption"])}</p>{sub_html}</div>')
    out = [SKETCH_CSS, f'<div class="xs" role="group" aria-label="{_h.escape(title)}">', defs,
           f'<span class="xs-chip">{_e(chip)}</span><h4 class="xs-title">{_e(title)}</h4>']
    if sub:
        out.append(f'<p class="xs-sub">{_e(sub)}</p>')
    out.append(f'<div class="xs-steps">{"".join(parts)}</div>')
    if progress:
        out.append('<div class="xs-prog"><ol>' + "".join(f"<li>{_e(n)}</li>" for n in progress) + "</ol>"
                   '<svg viewBox="0 0 400 16" preserveAspectRatio="none" aria-hidden="true">'
                   '<path d="M4 8h384" stroke-dasharray="6 6" vector-effect="non-scaling-stroke"/>'
                   '<path d="M380 2l14 6-14 6" vector-effect="non-scaling-stroke"/></svg></div>')
    if summary:
        line, sofar = summary
        so = f"<span>{_e(sofar)}</span>" if sofar else ""
        out.append(f'<div class="xs-sum">{_icon("trophy")}<div><strong>{_e(line)}</strong>{so}</div></div>')
    if note:
        out.append(f'<p class="xs-note">{_e(note)}</p>')
    out.append("</div>\n")
    return "".join(out)


def write(path, html):
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
