# Design system

The site uses **OpenAI's Apps SDK UI** as its design system: its design tokens, its component
CSS and its markup conventions. Nothing here is a re-creation of the look. The tokens and
components are the SDK's own files, vendored unchanged.

- Source: [`@openai/apps-sdk-ui`](https://www.npmjs.com/package/@openai/apps-sdk-ui) 0.2.2, MIT licence.
- Light and dark themes come with it. The reader picks one in the "Aa" panel. The default follows the system.

## Layout

```
design-system/
  vendor/apps-sdk-ui/   Verbatim copy of the SDK's CSS. Read-only. See CHECKSUMS and VERSION.
  preflight.css         The part of Tailwind's reset that the SDK components assume.
  site/                 Our layer. Layout and prose written only with SDK tokens.
    00-foundation.css     canvas, type defaults, spacing steps
    10-chrome.css         top bar, sidebar, outline rail, page nav
    20-prose.css          reading column: Markdown, code, callouts
    30-compose.css        hero, contents list, recap, cards
    40-interactive.css    in-page demos
    50-landing-diagrams.css  landing page and Mermaid figure card
    60-widgets.css        reader panel, graph button, glossary sheet, graph page
    70-reader-prefs.css   font, size and margin choices
  ds.js                 Theme switch, SegmentedControl thumb, Mermaid colours
scripts/design_system.py   Builds assets/ds.css from the above. Also emits SDK markup.
scripts/check_design_system.py   Lint. Run before every commit.
scripts/tokenize_colors.py       Migrates literal colours in diagrams to tokens.
```

`build_site.py` writes `_site/assets/ds.css` and `ds.js`, then links them first in `<head>` on every page.
Page generators emit markup only. They carry no CSS.

## Rules for site CSS

1. **Colour:** use a semantic token, such as `--color-text`, `--color-surface-secondary`,
   `--color-border`, `--color-background-info-surface`. No hex, `rgb()` or named colours.
2. **Type:** use `font: weight var(--font-text-md-size)/var(--font-text-md-line-height) var(--font-sans)`
   or the `--font-heading-*` equivalents. No `px` or `rem` font sizes.
3. **Shape and space:** `--radius-*` for corners, `--space-*` (multiples of the SDK's 4px `--spacing`)
   for gaps, `--shadow-hairline` and `--shadow-*` for elevation.
4. **Components first:** a button is `.Button`, a tag is `.Badge`, a message is `.Alert`, a switch uses
   the Switch tokens, a segmented choice is `.SegmentedControl`, a menu row is `.MenuItem`, a floating
   panel is `.Popover`. Use the SDK's attributes (`data-variant`, `data-color`, `data-size`, `data-pill`).
   `design_system.py` has helpers: `badge()`, `button_link()`, `alert()`, `text_link()`.
5. **Diagrams:** hand-built figures under `diagrams/` use the same tokens. Pick the colour family by
   meaning: `info` (blue), `success` (green), `warning` (orange), `caution` (yellow), `danger` (red),
   `discovery` (purple). Never write a hex.
6. **Do not edit `vendor/`.** To update the SDK, replace the files, bump `VERSION` and regenerate `CHECKSUMS`.

## Two small gaps we fill

- The SDK is built on Tailwind. It assumes Tailwind's reset and defines `--tracking-*` in Tailwind's
  theme. We supply both (`preflight.css` and `TAILWIND_GAPS` in `design_system.py`).
- Three SDK class names clash when all components share one sheet (`Container`, `Title`, `Description`).
  `design_system.py` renames them (`InputContainer`, `SwitchContainer`, `EmptyMessage*`).

## Not from the SDK

- The font is the SDK's system stack. OpenAI's brand typeface is not licensed for reuse, so it is not used.
- The knowledge graph keeps one hue per track. These are data colours in `build_graph.py`, not UI colour.

## Checks

```bash
python3 scripts/check_design_system.py   # no literal design values; vendored files unchanged
python3 scripts/build_site.py            # also writes assets/ds.css
```
