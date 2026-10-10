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

# Styling lives in design-system/site/60-widgets.css (one stylesheet for the whole site).

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

  function allowed(child){
    var t = child.tagName, c = child.className || '';
    return !SKIP[t] && (typeof c !== 'string' || (c.indexOf('gloss-term') < 0 && c.indexOf('mermaid') < 0))
           && child.id !== 'gl-panel' && child.id !== 'gl-scrim' && child.id !== 'rs-root';
  }

  // Scan <main> in short slices so a long page never blocks the main thread (the first
  // swipes after load stay smooth). Same document order and first-occurrence rule as
  // a single pass. A newer scan request supersedes an unfinished one; re-scans are
  // idempotent because `used` and the skip rules stay in force.
  var scanGen = 0;
  var later = window.requestIdleCallback
    ? function(fn){ window.requestIdleCallback(fn, {timeout:300}); }
    : function(fn){ setTimeout(fn, 16); };
  function scan(root, done){
    var gen = ++scanGen;
    var stack = [root.firstChild];
    function slice(){
      if(gen !== scanGen) return;
      var t0 = performance.now();
      while(stack.length){
        var child = stack[stack.length - 1];
        if(!child){ stack.pop(); continue; }
        stack[stack.length - 1] = child.nextSibling;   // advance first: scanText replaces the node
        if(child.nodeType === 3) scanText(child);
        else if(child.nodeType === 1 && allowed(child)) stack.push(child.firstChild);
        if(performance.now() - t0 > 6){ later(slice); return; }
      }
      if(done) done();
    }
    slice();
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
      if(tgt.closest && tgt.closest('#gl-close')){ close(); return; }   // the click lands on the inner span
      var r = tgt.closest && tgt.closest('[data-goto]');
      if(r){ e.preventDefault(); open(r.getAttribute('data-goto')); }
    });
  }
  function open(key){
    var e = entries[key]; if(!e) return;
    if(!panel.classList.contains('open')) lastFocus = document.activeElement;
    var uses = (e.uses||[]).map(function(u){ return '<li>'+escapeHtml(u)+'</li>'; }).join('');
    var rel = (e.related||[]).filter(function(k){ return entries[k]; }).map(function(k){
      return '<button class="Button gl-rel" data-variant="soft" data-color="secondary" data-size="sm" data-pill data-goto="'+escapeHtml(k)+'"><span class="ButtonInner">'+escapeHtml(entries[k].t)+'</span></button>'; }).join('');
    var see = e.see ? '<a class="Button gl-see" data-variant="solid" data-color="primary" data-size="md" data-pill href="'+ROOT+escapeHtml(e.see.href)+'"><span class="ButtonInner">Read the lesson: '+escapeHtml(e.see.label)+' &rarr;</span></a>' : '';
    panel.innerHTML =
      '<button id="gl-close" class="Button" data-variant="ghost" data-color="secondary" data-size="md" data-uniform data-pill aria-label="Close explanation"><span class="ButtonInner">&#10005;</span></button>' +
      (e.cat ? '<span class="Badge" data-color="secondary" data-variant="soft" data-size="md" data-pill>'+escapeHtml(e.cat)+'</span>' : '') +
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

  function keyBox(){
    var km = G.keyterms || {};
    var list = km[window.__glossPage || ''];
    if(!list || !list.length) return;
    var main = document.querySelector('main');
    if(!main || document.getElementById('gl-keybox')) return;
    if(main.textContent.replace(/Loading/,'').trim().length < 40) return;  // not yet rendered
    var chips = list.filter(function(k){ return entries[k]; }).map(function(k){
      return '<button class="Button gl-keyterm" data-variant="outline" data-color="secondary" data-size="sm" data-pill data-gk="'+k+'"><span class="ButtonInner">'+escapeHtml(entries[k].t)+'</span></button>'; }).join('');
    if(!chips) return;
    var box = document.createElement('aside');
    box.id = 'gl-keybox';
    box.setAttribute('aria-label', 'Key terms');
    box.innerHTML = '<div class="gl-keylab">Key terms</div><div class="gl-keychips">'+chips+'</div>';
    var hero = main.querySelector('.hero, .index-hero'), h1 = main.querySelector('h1');
    if(hero && hero.parentNode === main) hero.insertAdjacentElement('afterend', box);
    else if(h1) h1.insertAdjacentElement('afterend', box);
    else main.insertBefore(box, main.firstChild);
  }

  function start(){
    var main = document.querySelector('main') || document.body;
    build();
    scan(main, keyBox);
    keyBox();
    document.addEventListener('click', function(e){
      var b = e.target.closest && e.target.closest('.gloss-term, .gl-keyterm');
      if(b){ e.preventDefault(); open(b.getAttribute('data-gk')); }
    });
    // Harness & Flowable tracks render their markdown into <main> AFTER load
    // (fetch + marked). Re-walk when that content is swapped in. Observing only
    // direct children of <main> avoids re-firing on our own edits and on
    // mermaid's internal SVG changes. The `used` set keeps first-occurrence
    // correct and makes re-walks idempotent.
    if(window.MutationObserver){
      var mo = new MutationObserver(function(){ scan(main, keyBox); keyBox(); });
      mo.observe(main, {childList:true});
    }
  }
  if(document.readyState !== 'loading') start();
  else document.addEventListener('DOMContentLoaded', start);
})();
"""


def js_file(entries: dict, keyterms: dict) -> str:
    """The full glossary.js: inlined data (terms + must-know map) + behaviour."""
    data = json.dumps({"entries": entries, "keyterms": keyterms},
                      ensure_ascii=False, separators=(",", ":"))
    return "window.CCR_GLOSSARY=" + data + ";\n" + JS_LOGIC


def head_tags(root: str, page: str) -> str:
    """Per-page tags injected before </body>. `root` is the relative path to the
    site root (e.g. '../') so assets/lesson links resolve at any depth; `page` is
    the site-relative path of this page (e.g. 'ai/03-rag.html') so the widget can
    look up this lesson's Key terms."""
    r = root or ""
    return (
        '<script>window.__glossRoot=' + json.dumps(r)
        + ';window.__glossPage=' + json.dumps(page) + '</script>'
        '<script defer src="' + r + 'assets/glossary.js"></script>'
    )
