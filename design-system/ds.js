/* Tiny runtime for the design system. No scroll listeners, no layout reads on scroll. */
(function(){
  var root=document.documentElement, DS=window.DS=window.DS||{}, mq=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)');
  function stored(){try{var t=localStorage.getItem('ds-theme');return t==='light'||t==='dark'?t:null}catch(e){return null}}
  function apply(){
    var t=stored()||((mq&&mq.matches)?'dark':'light');
    root.setAttribute('data-theme',t);
    try{window.dispatchEvent(new CustomEvent('ds-themechange',{detail:t}))}catch(e){}
  }
  DS.theme={
    choice:function(){return stored()||'auto'},
    set:function(c){try{if(c==='light'||c==='dark')localStorage.setItem('ds-theme',c);else localStorage.removeItem('ds-theme')}catch(e){}apply()}
  };
  if(mq&&mq.addEventListener)mq.addEventListener('change',function(){if(!stored())apply()});

  /* SegmentedControl: move the thumb under the selected option, as the SDK component does. */
  DS.segmented=function(el,value,onChange){
    var thumb=el.querySelector('.SegmentedControlThumb'),opts=[].slice.call(el.querySelectorAll('.SegmentedControlOption'));
    function sync(animate){
      var on=el.querySelector('[data-state="on"]');if(!on||!thumb)return;
      if(!animate)thumb.style.transition='none';
      thumb.style.width=Math.floor(on.offsetWidth)+'px';
      thumb.style.transform='translateX('+on.offsetLeft+'px)';
      if(!animate){void thumb.offsetWidth;thumb.style.transition='width 300ms var(--cubic-enter), transform 300ms var(--cubic-enter)'}
    }
    function select(v,fire){
      opts.forEach(function(o){var on=o.getAttribute('data-value')===v;o.setAttribute('data-state',on?'on':'off');o.setAttribute('aria-checked',on?'true':'false')});
      sync(true);if(fire&&onChange)onChange(v);
    }
    opts.forEach(function(o){o.addEventListener('click',function(){select(o.getAttribute('data-value'),true)})});
    select(value,false);
    return {set:function(v){select(v,false)},sync:function(){sync(false)}};
  };

  /* Mermaid reads colour values, not CSS variables. Resolve the SDK semantic tokens for the
     current theme into concrete colours, so diagrams match the page in light and dark. */
  var cv=document.createElement('canvas');cv.width=cv.height=1;cv=cv.getContext('2d',{willReadFrequently:true});
  /* Computed colours may be oklab(); paint one pixel and read it back as plain sRGB. */
  function tokenColor(name){
    var el=document.createElement('span');el.style.color='var('+name+')';el.style.display='none';
    document.body.appendChild(el);var c=getComputedStyle(el).color;document.body.removeChild(el);
    cv.clearRect(0,0,1,1);cv.fillStyle=c;cv.fillRect(0,0,1,1);
    var d=cv.getImageData(0,0,1,1).data;
    return d[3]===255?'rgb('+d[0]+','+d[1]+','+d[2]+')':'rgba('+d[0]+','+d[1]+','+d[2]+','+(d[3]/255).toFixed(3)+')';
  }
  DS.mermaidConfig=function(){
    var t=function(n){return tokenColor(n)}, cs=getComputedStyle(document.documentElement);
    var surface=t('--color-surface'),raised=t('--color-surface-secondary'),text=t('--color-text'),
        sub=t('--color-text-secondary'),line=t('--color-border-strong'),soft=t('--color-border'),
        info=t('--color-background-info-surface'),accent=t('--color-text-info'),tint=t('--color-surface-tertiary');
    return {startOnLoad:false,theme:'base',securityLevel:'loose',
      themeVariables:{background:surface,primaryColor:surface,primaryTextColor:text,primaryBorderColor:line,
        secondaryColor:surface,secondaryBorderColor:line,secondaryTextColor:text,
        tertiaryColor:raised,tertiaryBorderColor:line,tertiaryTextColor:text,
        lineColor:sub,textColor:text,nodeTextColor:text,clusterBkg:tint,clusterBorder:soft,
        edgeLabelBackground:raised,actorBkg:info,actorBorder:accent,actorTextColor:text,
        actorLineColor:line,signalColor:sub,signalTextColor:text,labelBoxBkgColor:surface,
        labelBoxBorderColor:line,noteBkgColor:surface,noteBorderColor:line,
        activationBkgColor:surface,activationBorderColor:accent,
        quadrant1Fill:info,quadrant2Fill:raised,quadrant3Fill:soft,quadrant4Fill:raised,
        quadrantPointFill:accent,quadrantPointTextFill:text,quadrantXAxisTextFill:sub,
        quadrantYAxisTextFill:sub,quadrantTitleFill:text,quadrantInternalBorderStrokeFill:line,
        quadrantExternalBorderStrokeFill:line,
        fontFamily:cs.getPropertyValue('--font-sans').trim(),fontSize:cs.getPropertyValue('--font-text-md-size').trim()},
      flowchart:{useMaxWidth:false,htmlLabels:true,curve:'basis',nodeSpacing:36,rankSpacing:46,diagramPadding:12},
      sequence:{useMaxWidth:false,mirrorActors:false,actorMargin:56,messageMargin:34},
      quadrantChart:{useMaxWidth:false,chartWidth:640,chartHeight:440,quadrantLabelFontSize:13,
        pointLabelFontSize:12,pointRadius:4,titleFontSize:16},
      themeCSS:'.node rect{rx:9;ry:9} .cluster rect{rx:12;ry:12} .edgeLabel{border-radius:8px;padding:1px 5px} '+
        '.label{font-weight:500} .cluster-label .nodeLabel{font-weight:600}'};
  };
  /* Re-render diagrams after a theme change. Each diagram keeps its source in data-src. */
  DS.mermaidRemember=function(pre){if(!pre.hasAttribute('data-src'))pre.setAttribute('data-src',pre.textContent)};
  DS.mermaidRerender=function(mermaid){
    var nodes=[].slice.call(document.querySelectorAll('pre.mermaid[data-processed]'));
    if(!nodes.length)return;
    mermaid.initialize(DS.mermaidConfig());
    nodes.forEach(function(n){n.removeAttribute('data-processed');n.textContent=n.getAttribute('data-src')||n.textContent;
      var h=n.querySelector('.mm-hint');if(h)h.remove()});
    return mermaid.run({nodes:nodes});
  };
})();
