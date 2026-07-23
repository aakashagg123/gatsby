#!/usr/bin/env python3
"""Client-side glossary widget: clickable terms + an explainer sidebar.

Shipped once to _site/assets/ and referenced from every content page (the
per-page relative root is injected inline so the lesson links resolve at any
depth). On load, the script scans the page's <main>, wraps the *first
occurrence per page* of each known glossary term in a small button, and opens a
right-hand sidebar — plain-terms explanation, an example, where-it-shows-up
use-cases, related terms (themselves clickable), and a link to the lesson.

Pure vanilla JS + CSS, no build step, no external requests (the term data is
inlined into glossary.js by build_glossary.py). Palette matches the warm
Anthropic-inspired site chrome.
"""
import json

# ---- styling -----------------------------------------------------------------
# Authored as a concatenated plain string (no f-string) so CSS braces need no escaping.
CSS = (
    ".gloss-term{appearance:none;background:none;border:0;padding:0 .5px;margin:0;font:inherit;"
    "color:inherit;cursor:pointer;text-decoration:underline;text-decoration-style:dotted;"
    "text-decoration-color:#d6a48f;text-underline-offset:2.5px;text-decoration-thickness:1px;"
    "transition:color .12s,background .12s}"
    ".gloss-term:hover{color:#bd5d3a;text-decoration-color:#bd5d3a;background:rgba(217,119,87,.09);"
    "border-radius:3px}"
    ".gloss-term:focus-visible{outline:2px solid #d97757;outline-offset:1px;border-radius:2px}"
    "body.gl-open{overflow:hidden}"
    "#gl-scrim{position:fixed;inset:0;background:rgba(28,25,20,.30);opacity:0;visibility:hidden;"
    "transition:opacity .2s;z-index:10000}"
    "#gl-scrim.open{opacity:1;visibility:visible}"
    "#gl-panel{position:fixed;top:0;right:0;height:100%;width:390px;max-width:92vw;background:#faf9f5;"
    "border-left:1px solid #e4e0d5;box-shadow:-8px 0 40px rgba(26,25,21,.16);transform:translateX(102%);"
    "transition:transform .24s cubic-bezier(.4,0,.2,1);z-index:10001;overflow-y:auto;"
    "padding:30px 26px 48px;font-family:Inter,system-ui,-apple-system,sans-serif;color:#1f1e1d;"
    "-webkit-font-smoothing:antialiased}"
    "#gl-panel.open{transform:translateX(0)}"
    "#gl-close{position:absolute;top:15px;right:15px;width:32px;height:32px;border-radius:8px;"
    "border:1px solid #e4e0d5;background:#fff;color:#6c6a60;cursor:pointer;font-size:13px;line-height:1}"
    "#gl-close:hover{border-color:#d97757;color:#bd5d3a}"
    "#gl-panel .gl-cat{display:inline-block;font-size:.66rem;font-weight:600;letter-spacing:.06em;"
    "text-transform:uppercase;color:#bd5d3a;background:#fbefe9;border:1px solid #f0d9cd;border-radius:20px;"
    "padding:3px 10px;margin:2px 0 12px}"
    "#gl-panel .gl-term-h{font-size:1.5rem;font-weight:600;letter-spacing:-.02em;margin:0 0 2px;line-height:1.2;"
    "padding-right:36px}"
    "#gl-panel .gl-sec{margin-top:18px}"
    "#gl-panel .gl-lab{font-size:.68rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;"
    "color:#9a9788;margin-bottom:5px}"
    "#gl-panel .gl-sec p{margin:0;font-size:.95rem;line-height:1.62;color:#33322e}"
    "#gl-panel .gl-sec ul{margin:0;padding-left:18px}"
    "#gl-panel .gl-sec li{font-size:.92rem;line-height:1.55;color:#33322e;margin:4px 0}"
    "#gl-panel .gl-rels{display:flex;flex-wrap:wrap;gap:7px}"
    "#gl-panel .gl-rel{font:inherit;font-size:.82rem;color:#3d3c37;background:#f2f0e9;border:1px solid #e4e0d5;"
    "border-radius:20px;padding:4px 11px;cursor:pointer;line-height:1.3}"
    "#gl-panel .gl-rel:hover{border-color:#d97757;color:#bd5d3a;background:#fbefe9}"
    "#gl-panel .gl-see{display:inline-block;margin-top:26px;font-size:.9rem;font-weight:600;color:#bd5d3a;"
    "text-decoration:none;border-bottom:1px solid transparent}"
    "#gl-panel .gl-see:hover{border-bottom-color:#bd5d3a}"
    "@media (max-width:520px){#gl-panel{width:100%;max-width:100%;border-left:none;padding:26px 20px 40px}}"
    "@media print{.gloss-term{text-decoration:none}#gl-panel,#gl-scrim{display:none}}"
)

# ---- behaviour ---------------------------------------------------------------
JS_LOGIC = r"""
(function(){
  var G = window.CCR_GLOSSARY;
  if(!G || !G.entries) return;
  var ROOT = window.__glossRoot || '';
  var entries = G.entries;

  var forms = [];
  Object.keys(entries).forEach(function(key){
    var e = entries[key];
    if(e.autolink === false) return;
    [e.t].concat(e.aliases||[]).forEach(function(s){ forms.push({s:s, key:key, cs:!!e.cs}); });
  });
  forms.sort(function(a,b){ return b.s.length - a.s.length; });
  var byLower = {};
  forms.forEach(function(f){
    var lk = f.s.toLowerCase();
    if(!(lk in byLower)) byLower[lk] = {key:f.key, cs:f.cs, canon:f.s};
  });
  function esc(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }
  if(!forms.length) return;
  // case-insensitive; case-sensitive terms (cs:true) are filtered exactly, post-match
  var re = new RegExp('(^|[^A-Za-z0-9_-])(' + forms.map(function(f){return esc(f.s);}).join('|') + ')(?![A-Za-z0-9_-])', 'gi');

  var SKIP = {A:1,BUTTON:1,CODE:1,PRE:1,KBD:1,SAMP:1,SCRIPT:1,STYLE:1,SVG:1,TEXTAREA:1,
              INPUT:1,SELECT:1,OPTION:1,H1:1,H2:1,H3:1,H4:1,H5:1,H6:1};
  var used = {};

  function scanText(node){
    var text = node.nodeValue;
    if(!text || text.length < 2) return;
    re.lastIndex = 0;
    var m, matches = [];
    while((m = re.exec(text))){
      var pre = m[1], surf = m[2];
      var info = byLower[surf.toLowerCase()];
      if(!info) continue;
      if(info.cs && surf !== info.canon) continue;
      if(used[info.key]) continue;
      var start = m.index + pre.length;
      matches.push({start:start, end:start+surf.length, key:info.key, surf:surf});
      used[info.key] = true;
    }
    if(!matches.length) return;
    var frag = document.createDocumentFragment(), pos = 0;
    matches.forEach(function(mt){
      if(mt.start > pos) frag.appendChild(document.createTextNode(text.slice(pos, mt.start)));
      var b = document.createElement('button');
      b.className = 'gloss-term'; b.type = 'button';
      b.setAttribute('data-gk', mt.key);
      b.setAttribute('aria-label', 'What is ' + mt.surf + '? Open explanation');
      b.textContent = mt.surf;
      frag.appendChild(b);
      pos = mt.end;
    });
    if(pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
    node.parentNode.replaceChild(frag, node);
  }

  function walk(node){
    var child = node.firstChild;
    while(child){
      var next = child.nextSibling;
      if(child.nodeType === 3) scanText(child);
      else if(child.nodeType === 1){
        var t = child.tagName, c = child.className || '';
        if(!SKIP[t] && (typeof c !== 'string' || (c.indexOf('gloss-term') < 0 && c.indexOf('mermaid') < 0))
           && child.id !== 'gl-panel' && child.id !== 'gl-scrim' && child.id !== 'rs-root')
          walk(child);
      }
      child = next;
    }
  }

  function escapeHtml(s){ return (s==null?'':String(s)).replace(/[&<>"]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

  var panel, scrim, lastFocus;
  function build(){
    scrim = document.createElement('div'); scrim.id = 'gl-scrim';
    panel = document.createElement('aside'); panel.id = 'gl-panel';
    panel.setAttribute('role','dialog'); panel.setAttribute('aria-label','Term explanation');
    panel.setAttribute('tabindex','-1');
    document.body.appendChild(scrim); document.body.appendChild(panel);
    scrim.addEventListener('click', close);
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') close(); });
    panel.addEventListener('click', function(e){
      var tgt = e.target;
      if(tgt.id === 'gl-close'){ close(); return; }
      var r = tgt.closest && tgt.closest('[data-goto]');
      if(r){ e.preventDefault(); open(r.getAttribute('data-goto')); }
    });
  }
  function open(key){
    var e = entries[key]; if(!e) return;
    if(!panel.classList.contains('open')) lastFocus = document.activeElement;
    var uses = (e.uses||[]).map(function(u){ return '<li>'+escapeHtml(u)+'</li>'; }).join('');
    var rel = (e.related||[]).filter(function(k){ return entries[k]; }).map(function(k){
      return '<button class="gl-rel" data-goto="'+escapeHtml(k)+'">'+escapeHtml(entries[k].t)+'</button>'; }).join('');
    var see = e.see ? '<a class="gl-see" href="'+ROOT+escapeHtml(e.see.href)+'">Read the lesson: '+escapeHtml(e.see.label)+' &rarr;</a>' : '';
    panel.innerHTML =
      '<button id="gl-close" aria-label="Close explanation">&#10005;</button>' +
      (e.cat ? '<span class="gl-cat">'+escapeHtml(e.cat)+'</span>' : '') +
      '<h2 class="gl-term-h">'+escapeHtml(e.t)+'</h2>' +
      '<div class="gl-sec"><div class="gl-lab">In plain terms</div><p>'+escapeHtml(e.fp)+'</p></div>' +
      (e.example ? '<div class="gl-sec"><div class="gl-lab">For example</div><p>'+escapeHtml(e.example)+'</p></div>' : '') +
      (uses ? '<div class="gl-sec"><div class="gl-lab">Where it shows up</div><ul>'+uses+'</ul></div>' : '') +
      (rel ? '<div class="gl-sec"><div class="gl-lab">Related</div><div class="gl-rels">'+rel+'</div></div>' : '') +
      see;
    document.body.classList.add('gl-open');
    scrim.classList.add('open'); panel.classList.add('open');
    panel.scrollTop = 0; panel.focus();
  }
  function close(){
    if(panel) panel.classList.remove('open');
    if(scrim) scrim.classList.remove('open');
    document.body.classList.remove('gl-open');
    if(lastFocus && lastFocus.focus){ try{ lastFocus.focus(); }catch(e){} }
  }

  function start(){
    var main = document.querySelector('main') || document.body;
    walk(main);
    build();
    document.addEventListener('click', function(e){
      var b = e.target.closest && e.target.closest('.gloss-term');
      if(b){ e.preventDefault(); open(b.getAttribute('data-gk')); }
    });
    // Harness & Flowable tracks render their markdown into <main> AFTER load
    // (fetch + marked). Re-walk when that content is swapped in. Observing only
    // direct children of <main> avoids re-firing on our own edits and on
    // mermaid's internal SVG changes. The `used` set keeps first-occurrence
    // correct and makes re-walks idempotent.
    if(window.MutationObserver){
      var mo = new MutationObserver(function(){ walk(main); });
      mo.observe(main, {childList:true});
    }
  }
  if(document.readyState !== 'loading') start();
  else document.addEventListener('DOMContentLoaded', start);
})();
"""


def js_file(entries: dict) -> str:
    """The full glossary.js: inlined data + behaviour."""
    data = json.dumps({"entries": entries}, ensure_ascii=False, separators=(",", ":"))
    return "window.CCR_GLOSSARY=" + data + ";\n" + JS_LOGIC


def head_tags(root: str) -> str:
    """Per-page tags injected before </body>. `root` is the relative path to the
    site root (e.g. '../'), so assets and lesson links resolve at any depth."""
    r = root or ""
    return (
        '<link rel="stylesheet" href="' + r + 'assets/glossary.css">'
        '<script>window.__glossRoot=' + json.dumps(r) + '</script>'
        '<script defer src="' + r + 'assets/glossary.js"></script>'
    )
