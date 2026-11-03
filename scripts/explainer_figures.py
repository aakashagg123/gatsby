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


def layers(chip, title, sub, rows, note=""):
    """rows: (family, label, text), drawn top to bottom."""
    body = "".join(f'<div class="xf-box {_fam(f)}"><b>{_e(a)}</b><span>{_e(b)}</span></div>' for f, a, b in rows)
    return card(chip, title, sub, f'<div class="xf-layers">{body}</div>', note)


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


def bars(chip, title, sub, rows, vmax=1.0, note="", fmt="{:.2f}"):
    """rows: (label, value, family). Horizontal bars scaled to vmax."""
    out = []
    for label, v, f in rows:
        pct = max(0.0, min(100.0, 100.0 * v / vmax))
        out.append(f'<div class="xf-lbl">{_e(label)}</div>'
                   f'<div class="xf-fill"><div style="width:{pct:.1f}%;background:{_solid(f)}"></div></div>'
                   f'<div class="xf-val">{_e(fmt.format(v))}</div>')
    return card(chip, title, sub, f'<div class="xf-bars">{"".join(out)}</div>', note)


def grid(chip, title, sub, rows, cols_label=None, note=""):
    """rows: list of rows; each row is a list of (text, family or None). Equal-width cells."""
    ncols = max(len(r) for r in rows)
    cells = []
    for r in rows:
        for t, f in r:
            st = f' style="background:{_bg(f)}"' if f else ""
            cells.append(f'<div class="xf-cell {_fam(f)}"{st}>{_e(t)}</div>')
    return card(chip, title, sub, f'<div class="xf-grid" style="grid-template-columns:repeat({ncols},minmax(0,1fr))">{"".join(cells)}</div>', note)


def compare(chip, title, sub, left, right, note=""):
    """left and right: (family, heading, [bullets])."""
    def col(c):
        f, h, items = c
        li = "".join(f"<li>{_e(i)}</li>" for i in items)
        return f'<div class="xf-box {_fam(f)}"><b>{_e(h)}</b><ul>{li}</ul></div>'
    return card(chip, title, sub, f'<div class="xf-cmp">{col(left)}{col(right)}</div>', note)


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


def write(path, html):
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
