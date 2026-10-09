"""Shared iBooks-style reader-settings widget for all generated reading pages.

Injected before </body> by build_html.py (AI engineering modules),
build_standalone.py (the craft tracks), and build_site.py (harness viewer).

The widget is a floating "Aa" button that opens a panel with:
  - Theme: auto, light or dark (the SDK's data-theme)
  - Font: Google Sans (default), system, Tahoma, Arial, Verdana, Helvetica
  - Size: A- / A+ over discrete steps (like iBooks)
  - Margins: narrow / default / wide reading column

Choices persist in localStorage under one key, so they follow the reader
across every module and track. The page renders with its original design
until a setting is changed: attributes (data-rf / data-rs / data-rm) are only
set on <html> for non-default choices, and all override CSS is gated on them.
Code blocks and mermaid diagrams keep their own fonts.
Styling lives in design-system/site/60-widgets.css and 70-reader-prefs.css.
"""

READER = r"""
<div id="rs-root">
  <div id="rs-panel" class="Popover" role="dialog" aria-label="Reader settings">
    <div class="rs-h">Theme</div>
    <div class="SegmentedControl" id="rs-theme" data-size="md" data-pill role="radiogroup" aria-label="Theme">
      <div class="SegmentedControlThumb"></div>
      <button type="button" class="SegmentedControlOption" role="radio" data-value="auto"><span class="relative">Auto</span></button>
      <button type="button" class="SegmentedControlOption" role="radio" data-value="light"><span class="relative">Light</span></button>
      <button type="button" class="SegmentedControlOption" role="radio" data-value="dark"><span class="relative">Dark</span></button>
    </div>
    <div class="rs-h">Font</div>
    <div class="rs-fonts" role="radiogroup" aria-label="Font">
      <button type="button" class="MenuItem" role="radio" data-f="" style="font-family:var(--font-sans)"><span>Google Sans (Default)</span><span class="rs-check" aria-hidden="true">✓</span></button>
      <button type="button" class="MenuItem" role="radio" data-f="system" style="font-family:ui-sans-serif,system-ui,sans-serif"><span>System</span><span class="rs-check" aria-hidden="true">✓</span></button>
      <button type="button" class="MenuItem" role="radio" data-f="tahoma" style="font-family:Tahoma,Verdana,sans-serif"><span>Tahoma</span><span class="rs-check" aria-hidden="true">✓</span></button>
      <button type="button" class="MenuItem" role="radio" data-f="arial" style="font-family:Arial,'Helvetica Neue',Helvetica,sans-serif"><span>Arial</span><span class="rs-check" aria-hidden="true">✓</span></button>
      <button type="button" class="MenuItem" role="radio" data-f="verdana" style="font-family:Verdana,Geneva,sans-serif"><span>Verdana</span><span class="rs-check" aria-hidden="true">✓</span></button>
      <button type="button" class="MenuItem" role="radio" data-f="helvetica" style="font-family:'Helvetica Neue',Helvetica,Arial,sans-serif"><span>Helvetica</span><span class="rs-check" aria-hidden="true">✓</span></button>
    </div>
    <div class="rs-h">Size</div>
    <div class="rs-row">
      <button type="button" id="rs-sminus" class="Button" data-variant="outline" data-color="secondary" data-size="md" data-uniform data-pill aria-label="Decrease font size"><span class="ButtonInner" style="font-size:var(--font-text-xs-size)">A</span></button>
      <span class="rs-val" id="rs-sval">100%</span>
      <button type="button" id="rs-splus" class="Button" data-variant="outline" data-color="secondary" data-size="md" data-uniform data-pill aria-label="Increase font size"><span class="ButtonInner" style="font-size:var(--font-text-lg-size)">A</span></button>
    </div>
    <div class="rs-h">Margins</div>
    <div class="SegmentedControl" id="rs-margins" data-size="md" data-pill role="radiogroup" aria-label="Margins">
      <div class="SegmentedControlThumb"></div>
      <button type="button" class="SegmentedControlOption" role="radio" data-value="n"><span class="relative">Narrow</span></button>
      <button type="button" class="SegmentedControlOption" role="radio" data-value=""><span class="relative">Default</span></button>
      <button type="button" class="SegmentedControlOption" role="radio" data-value="w"><span class="relative">Wide</span></button>
    </div>
    <button type="button" id="rs-reset" class="Button" data-variant="ghost" data-color="secondary" data-size="md" data-pill><span class="ButtonInner">Reset to defaults</span></button>
  </div>
  <button type="button" id="rs-btn" class="Button fab" data-variant="outline" data-color="secondary" data-size="xl" data-uniform data-pill aria-label="Reader settings" aria-expanded="false" title="Reader settings: theme, font, size, margins"><span class="ButtonInner">Aa</span></button>
</div>
<script id="reader-js">
(function(){
  var KEY='ccrReaderSettings';
  var SIZES=[0.85,0.92,1,1.08,1.16,1.25,1.35,1.5,1.7];
  // Allowed font keys. Reset a returning reader's stored value if it points at a font
  // this build no longer supports, so the UI stays consistent with the CSS.
  var ALLOWED_F={'':1,system:1,tahoma:1,arial:1,verdana:1,helvetica:1};
  var st={f:'',s:2,m:''};
  try{var saved=JSON.parse(localStorage.getItem(KEY)||'{}');
      if(typeof saved.f==='string'&&ALLOWED_F.hasOwnProperty(saved.f))st.f=saved.f;
      if(typeof saved.s==='number'&&saved.s>=0&&saved.s<SIZES.length)st.s=saved.s;
      if(typeof saved.m==='string')st.m=saved.m;}catch(e){}
  var h=document.documentElement,root=document.getElementById('rs-root'),
      btn=document.getElementById('rs-btn'),panel=document.getElementById('rs-panel'),
      sval=document.getElementById('rs-sval'),segTheme=null,segMargins=null;
  function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
  function apply(){
    if(st.f)h.setAttribute('data-rf',st.f);else h.removeAttribute('data-rf');
    if(SIZES[st.s]!==1){h.setAttribute('data-rs','1');h.style.setProperty('--rs-scale',SIZES[st.s]);}
    else{h.removeAttribute('data-rs');h.style.removeProperty('--rs-scale');}
    if(st.m)h.setAttribute('data-rm',st.m);else h.removeAttribute('data-rm');
    sval.textContent=Math.round(SIZES[st.s]*100)+'%';
    panel.querySelectorAll('.rs-fonts .MenuItem').forEach(function(b){
      var on=b.getAttribute('data-f')===st.f;
      if(on)b.setAttribute('data-selected','');else b.removeAttribute('data-selected');
      b.setAttribute('aria-checked',on?'true':'false');});
    if(segMargins)segMargins.set(st.m);
  }
  function setOpen(open){
    panel.classList.toggle('open',open);btn.setAttribute('aria-expanded',open?'true':'false');
    // the thumb needs layout, so size it once the panel is visible
    if(open){if(segTheme)segTheme.sync();if(segMargins)segMargins.sync();}
  }
  function initSegments(){
    if(!window.DS||!DS.segmented)return;
    segTheme=DS.segmented(document.getElementById('rs-theme'),DS.theme.choice(),function(v){DS.theme.set(v)});
    segMargins=DS.segmented(document.getElementById('rs-margins'),st.m,function(v){st.m=v;apply();save()});
  }
  btn.addEventListener('click',function(){setOpen(!panel.classList.contains('open'))});
  document.addEventListener('click',function(e){if(!root.contains(e.target))setOpen(false)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')setOpen(false)});
  panel.querySelectorAll('.rs-fonts .MenuItem').forEach(function(b){
    b.addEventListener('click',function(){st.f=b.getAttribute('data-f');apply();save()})});
  document.getElementById('rs-sminus').addEventListener('click',function(){
    if(st.s>0){st.s--;apply();save()}});
  document.getElementById('rs-splus').addEventListener('click',function(){
    if(st.s<SIZES.length-1){st.s++;apply();save()}});
  document.getElementById('rs-reset').addEventListener('click',function(){
    st={f:'',s:2,m:''};apply();save();if(segTheme){DS.theme.set('auto');segTheme.set('auto')}});
  // ds.js is deferred, so wait for it before wiring the segmented controls
  if(window.DS)initSegments();else window.addEventListener('DOMContentLoaded',initSegments);
  apply();
})();
</script>
"""


def inject(page: str) -> str:
    """Insert the reader widget just before </body>. Idempotent."""
    if 'id="rs-root"' in page or "</body>" not in page:
        return page
    return page.replace("</body>", READER + "</body>", 1)
