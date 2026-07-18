"""Shared iBooks-style reader-settings widget for all generated reading pages.

Injected before </body> by build_html.py (AI engineering modules),
build_standalone.py (the craft tracks), and build_site.py (harness viewer).

The widget is a floating "Aa" button that opens a panel with:
  - Font: publisher default, Charter, Georgia, San Francisco, Tahoma, Helvetica
  - Size: A- / A+ over discrete steps (like iBooks)
  - Margins: narrow / default / wide reading column

Choices persist in localStorage under one key, so they follow the reader
across every module and track. The page renders with its original design
until a setting is changed: attributes (data-rf / data-rs / data-rm) are only
set on <html> for non-default choices, and all override CSS is gated on them.
Code blocks and mermaid diagrams keep their own fonts.
"""

READER = r"""
<style id="reader-css">
/* ---- font choices (only active when data-rf is set) ---- */
html[data-rf="charter"]{--rs-font:Charter,"Bitstream Charter","Iowan Old Style","Palatino Linotype",Georgia,serif}
html[data-rf="georgia"]{--rs-font:Georgia,"Times New Roman",serif}
html[data-rf="sf"]{--rs-font:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",system-ui,sans-serif}
html[data-rf="tahoma"]{--rs-font:Tahoma,Verdana,"Segoe UI",sans-serif}
html[data-rf="helvetica"]{--rs-font:"Helvetica Neue",Helvetica,Arial,sans-serif}
html[data-rf] main :is(h1,h2,h3,h4,h5,h6,p,li,blockquote,td,th,dt,dd,figcaption,summary,em,strong,.lede,.chip,a){font-family:var(--rs-font) !important}
html[data-rf] main :is(pre,code,kbd,samp),html[data-rf] main pre *,html[data-rf] main p code,html[data-rf] main li code{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace !important}
html[data-rf] main .mermaid,html[data-rf] main .mermaid *{font-family:inherit}
/* ---- size scaling (only active when data-rs is set) ---- */
html[data-rs] main{font-size:calc(16.5px * var(--rs-scale,1)) !important}
html[data-rs] main h1{font-size:2.35em !important;line-height:1.15 !important}
html[data-rs] main h2{font-size:1.7em !important}
html[data-rs] main h3{font-size:1.25em !important}
html[data-rs] main h4{font-size:1em !important}
html[data-rs] main .lede{font-size:1.2em !important}
html[data-rs] main table{font-size:.9em !important}
html[data-rs] main th,html[data-rs] main td{font-size:inherit !important}
html[data-rs] main .pm-callout p{font-size:.95em !important}
html[data-rs] main pre{font-size:.85em !important}
/* ---- margins / column width (only active when data-rm is set) ---- */
html[data-rm="n"] main{max-width:620px !important}
html[data-rm="w"] main{max-width:1120px !important}
/* ---- the widget ---- */
#rs-root{position:fixed;right:22px;bottom:22px;z-index:9999;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}
#rs-btn{width:44px;height:44px;border-radius:50%;border:1px solid #e4e0d5;background:#faf9f5;color:#1f1e1d;
  font-size:17px;font-weight:600;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.12);line-height:1}
#rs-btn:hover{border-color:#d97757;color:#bd5d3a}
#rs-panel{position:absolute;right:0;bottom:54px;width:264px;background:#faf9f5;border:1px solid #e4e0d5;
  border-radius:14px;box-shadow:0 8px 30px rgba(0,0,0,.16);padding:14px;display:none}
#rs-panel.open{display:block}
#rs-panel .rs-h{font-size:11px;letter-spacing:.7px;text-transform:uppercase;color:#8a8778;margin:10px 0 6px;font-weight:600}
#rs-panel .rs-h:first-child{margin-top:0}
.rs-fonts{display:flex;flex-direction:column;gap:4px}
.rs-fonts button{display:flex;justify-content:space-between;align-items:center;width:100%;padding:6px 10px;
  border:1px solid transparent;border-radius:8px;background:none;font-size:15px;color:#1f1e1d;cursor:pointer;text-align:left}
.rs-fonts button:hover{background:#f2f0e9}
.rs-fonts button.on{border-color:#d97757;background:#fbefe9}
.rs-fonts button .rs-check{color:#bd5d3a;font-weight:700;visibility:hidden}
.rs-fonts button.on .rs-check{visibility:visible}
.rs-row{display:flex;align-items:center;gap:8px}
.rs-row button{flex:1;padding:7px 0;border:1px solid #e4e0d5;border-radius:8px;background:#fff;
  cursor:pointer;color:#1f1e1d;font-size:14px}
.rs-row button:hover{border-color:#d97757}
.rs-row button.on{border-color:#d97757;background:#fbefe9;font-weight:600}
.rs-row .rs-val{flex:0 0 56px;text-align:center;font-size:13px;color:#8a8778;font-variant-numeric:tabular-nums}
#rs-sminus{font-size:13px}#rs-splus{font-size:17px}
#rs-reset{margin-top:12px;width:100%;padding:7px 0;border:none;border-radius:8px;background:#f2f0e9;
  color:#8a8778;font-size:13px;cursor:pointer}
#rs-reset:hover{color:#bd5d3a}
@media (max-width:640px){#rs-root{right:12px;bottom:12px}#rs-panel{width:240px}}
@media print{#rs-root{display:none}}
</style>
<div id="rs-root">
  <div id="rs-panel" role="dialog" aria-label="Reader settings">
    <div class="rs-h">Font</div>
    <div class="rs-fonts">
      <button data-f="" style="font-family:inherit">Original<span class="rs-check">✓</span></button>
      <button data-f="charter" style="font-family:Charter,'Bitstream Charter',Georgia,serif">Charter<span class="rs-check">✓</span></button>
      <button data-f="georgia" style="font-family:Georgia,serif">Georgia<span class="rs-check">✓</span></button>
      <button data-f="sf" style="font-family:-apple-system,BlinkMacSystemFont,'SF Pro Text','Segoe UI',system-ui,sans-serif">San Francisco<span class="rs-check">✓</span></button>
      <button data-f="tahoma" style="font-family:Tahoma,Verdana,sans-serif">Tahoma<span class="rs-check">✓</span></button>
      <button data-f="helvetica" style="font-family:'Helvetica Neue',Helvetica,Arial,sans-serif">Helvetica<span class="rs-check">✓</span></button>
    </div>
    <div class="rs-h">Size</div>
    <div class="rs-row">
      <button id="rs-sminus" aria-label="Decrease font size">A</button>
      <span class="rs-val" id="rs-sval">100%</span>
      <button id="rs-splus" aria-label="Increase font size">A</button>
    </div>
    <div class="rs-h">Margins</div>
    <div class="rs-row rs-margins">
      <button data-m="n" title="Narrow column">▮</button>
      <button data-m="" title="Default">▬</button>
      <button data-m="w" title="Wide column">▭</button>
    </div>
    <button id="rs-reset">Reset to defaults</button>
  </div>
  <button id="rs-btn" aria-label="Reader settings" aria-expanded="false" title="Reader settings — font, size, margins">Aa</button>
</div>
<script id="reader-js">
(function(){
  var KEY='ccrReaderSettings';
  var SIZES=[0.85,0.92,1,1.08,1.16,1.25,1.35,1.5,1.7];
  var st={f:'',s:2,m:''};
  try{var saved=JSON.parse(localStorage.getItem(KEY)||'{}');
      if(typeof saved.f==='string')st.f=saved.f;
      if(typeof saved.s==='number'&&saved.s>=0&&saved.s<SIZES.length)st.s=saved.s;
      if(typeof saved.m==='string')st.m=saved.m;}catch(e){}
  var h=document.documentElement,root=document.getElementById('rs-root'),
      btn=document.getElementById('rs-btn'),panel=document.getElementById('rs-panel'),
      sval=document.getElementById('rs-sval');
  function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
  function apply(){
    if(st.f)h.setAttribute('data-rf',st.f);else h.removeAttribute('data-rf');
    if(SIZES[st.s]!==1){h.setAttribute('data-rs','1');h.style.setProperty('--rs-scale',SIZES[st.s]);}
    else{h.removeAttribute('data-rs');h.style.removeProperty('--rs-scale');}
    if(st.m)h.setAttribute('data-rm',st.m);else h.removeAttribute('data-rm');
    sval.textContent=Math.round(SIZES[st.s]*100)+'%';
    panel.querySelectorAll('.rs-fonts button').forEach(function(b){
      b.classList.toggle('on',b.getAttribute('data-f')===st.f)});
    panel.querySelectorAll('.rs-margins button').forEach(function(b){
      b.classList.toggle('on',b.getAttribute('data-m')===st.m)});
  }
  btn.addEventListener('click',function(){
    var open=panel.classList.toggle('open');btn.setAttribute('aria-expanded',open)});
  document.addEventListener('click',function(e){
    if(!root.contains(e.target)){panel.classList.remove('open');btn.setAttribute('aria-expanded','false')}});
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){panel.classList.remove('open');btn.setAttribute('aria-expanded','false')}});
  panel.querySelectorAll('.rs-fonts button').forEach(function(b){
    b.addEventListener('click',function(){st.f=b.getAttribute('data-f');apply();save()})});
  panel.querySelectorAll('.rs-margins button').forEach(function(b){
    b.addEventListener('click',function(){st.m=b.getAttribute('data-m');apply();save()})});
  document.getElementById('rs-sminus').addEventListener('click',function(){
    if(st.s>0){st.s--;apply();save()}});
  document.getElementById('rs-splus').addEventListener('click',function(){
    if(st.s<SIZES.length-1){st.s++;apply();save()}});
  document.getElementById('rs-reset').addEventListener('click',function(){
    st={f:'',s:2,m:''};apply();save()});
  apply();
})();
</script>
"""


def inject(page: str) -> str:
    """Insert the reader widget just before </body>. Idempotent."""
    if 'id="rs-root"' in page or "</body>" not in page:
        return page
    return page.replace("</body>", READER + "</body>", 1)
