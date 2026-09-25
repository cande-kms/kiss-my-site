(function(){
  var canvas = document.getElementById('galaxy');
  var gl = canvas.getContext('webgl2', {alpha:false, premultipliedAlpha:false, antialias:false}) ||
           canvas.getContext('webgl', {alpha:false, premultipliedAlpha:false, antialias:false});
  if(!gl){ canvas.style.background = '#05050b'; return; }

  var vertSrc = [
    'attribute vec2 uv;',
    'attribute vec2 position;',
    'varying vec2 vUv;',
    'void main() {',
    '  vUv = uv;',
    '  gl_Position = vec4(position, 0.0, 1.0);',
    '}'
  ].join('\n');

  var fragSrc = [
    'precision highp float;',
    '',
    'uniform float uTime;',
    'uniform vec3 uResolution;',
    'uniform vec2 uFocal;',
    'uniform vec2 uRotation;',
    'uniform float uStarSpeed;',
    'uniform float uDensity;',
    'uniform float uHueShift;',
    'uniform float uScrollMix;',
    'uniform vec3 uMixColor;',
    'uniform float uSpeed;',
    'uniform vec2 uMouse;',
    'uniform float uGlowIntensity;',
    'uniform float uSaturation;',
    'uniform bool uMouseRepulsion;',
    'uniform float uTwinkleIntensity;',
    'uniform float uRotationSpeed;',
    'uniform float uRepulsionStrength;',
    'uniform float uMouseActiveFactor;',
    'uniform float uAutoCenterRepulsion;',
    'uniform bool uTransparent;',
    '',
    'varying vec2 vUv;',
    '',
    '#define NUM_LAYER 4.0',
    '#define STAR_COLOR_CUTOFF 0.2',
    '#define MAT45 mat2(0.7071, -0.7071, 0.7071, 0.7071)',
    '#define PERIOD 3.0',
    '',
    'float Hash21(vec2 p) {',
    '  p = fract(p * vec2(123.34, 456.21));',
    '  p += dot(p, p + 45.32);',
    '  return fract(p.x * p.y);',
    '}',
    '',
    'float tri(float x) {',
    '  return abs(fract(x) * 2.0 - 1.0);',
    '}',
    '',
    'float tris(float x) {',
    '  float t = fract(x);',
    '  return 1.0 - smoothstep(0.0, 1.0, abs(2.0 * t - 1.0));',
    '}',
    '',
    'float trisn(float x) {',
    '  float t = fract(x);',
    '  return 2.0 * (1.0 - smoothstep(0.0, 1.0, abs(2.0 * t - 1.0))) - 1.0;',
    '}',
    '',
    'vec3 hsv2rgb(vec3 c) {',
    '  vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);',
    '  vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);',
    '  return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);',
    '}',
    '',
    'float Star(vec2 uv, float flare) {',
    '  float d = length(uv);',
    '  float m = (0.05 * uGlowIntensity) / d;',
    '  float rays = smoothstep(0.0, 1.0, 1.0 - abs(uv.x * uv.y * 1000.0));',
    '  m += rays * flare * uGlowIntensity;',
    '  uv *= MAT45;',
    '  rays = smoothstep(0.0, 1.0, 1.0 - abs(uv.x * uv.y * 1000.0));',
    '  m += rays * 0.3 * flare * uGlowIntensity;',
    '  m *= smoothstep(1.0, 0.2, d);',
    '  return m;',
    '}',
    '',
    'vec3 StarLayer(vec2 uv) {',
    '  vec3 col = vec3(0.0);',
    '',
    '  vec2 gv = fract(uv) - 0.5;',
    '  vec2 id = floor(uv);',
    '',
    '  for (int y = -1; y <= 1; y++) {',
    '    for (int x = -1; x <= 1; x++) {',
    '      vec2 offset = vec2(float(x), float(y));',
    '      vec2 si = id + vec2(float(x), float(y));',
    '      float seed = Hash21(si);',
    '      float size = fract(seed * 345.32);',
    '      float glossLocal = tri(uStarSpeed / (PERIOD * seed + 1.0));',
    '      float flareSize = smoothstep(0.9, 1.0, size) * glossLocal;',
    '',
    '      float red = smoothstep(STAR_COLOR_CUTOFF, 1.0, Hash21(si + 1.0)) + STAR_COLOR_CUTOFF;',
    '      float blu = smoothstep(STAR_COLOR_CUTOFF, 1.0, Hash21(si + 3.0)) + STAR_COLOR_CUTOFF;',
    '      float grn = min(red, blu) * seed;',
    '      vec3 base = vec3(red, grn, blu);',
    '',
    '      float hue = atan(base.g - base.r, base.b - base.r) / (2.0 * 3.14159) + 0.5;',
    '      hue = fract(uHueShift / 360.0 + (hue - 0.5) * 0.1);',
    '      float sat = length(base - vec3(dot(base, vec3(0.299, 0.587, 0.114)))) * uSaturation;',
    '      float val = max(max(base.r, base.g), base.b);',
    '      base = hsv2rgb(vec3(hue, sat, val));',
    '      base = mix(base, uMixColor, uScrollMix);',
    '',
    '      vec2 pad = vec2(tris(seed * 34.0 + uTime * uSpeed / 10.0), tris(seed * 38.0 + uTime * uSpeed / 30.0)) - 0.5;',
    '',
    '      float star = Star(gv - offset - pad, flareSize);',
    '      vec3 color = base;',
    '',
    '      float twinkle = trisn(uTime * uSpeed + seed * 6.2831) * 0.5 + 1.0;',
    '      twinkle = mix(1.0, twinkle, uTwinkleIntensity);',
    '      star *= twinkle;',
    '',
    '      col += star * size * color;',
    '    }',
    '  }',
    '',
    '  return col;',
    '}',
    '',
    'void main() {',
    '  vec2 focalPx = uFocal * uResolution.xy;',
    '  vec2 uv = (vUv * uResolution.xy - focalPx) / uResolution.y;',
    '',
    '  vec2 mouseNorm = uMouse - vec2(0.5);',
    '',
    '  if (uAutoCenterRepulsion > 0.0) {',
    '    vec2 centerUV = vec2(0.0, 0.0);',
    '    float centerDist = length(uv - centerUV);',
    '    vec2 repulsion = normalize(uv - centerUV) * (uAutoCenterRepulsion / (centerDist + 0.1));',
    '    uv += repulsion * 0.05;',
    '  } else if (uMouseRepulsion) {',
    '    vec2 mousePosUV = (uMouse * uResolution.xy - focalPx) / uResolution.y;',
    '    float mouseDist = length(uv - mousePosUV);',
    '    vec2 repulsion = normalize(uv - mousePosUV) * (uRepulsionStrength / (mouseDist + 0.1));',
    '    uv += repulsion * 0.05 * uMouseActiveFactor;',
    '  } else {',
    '    vec2 mouseOffset = mouseNorm * 0.1 * uMouseActiveFactor;',
    '    uv += mouseOffset;',
    '  }',
    '',
    '  float autoRotAngle = uTime * uRotationSpeed;',
    '  mat2 autoRot = mat2(cos(autoRotAngle), -sin(autoRotAngle), sin(autoRotAngle), cos(autoRotAngle));',
    '  uv = autoRot * uv;',
    '',
    '  uv = mat2(uRotation.x, -uRotation.y, uRotation.y, uRotation.x) * uv;',
    '',
    '  vec3 col = vec3(0.0);',
    '',
    '  for (float i = 0.0; i < 1.0; i += 1.0 / NUM_LAYER) {',
    '    float depth = fract(i + uStarSpeed * uSpeed);',
    '    float scale = mix(20.0 * uDensity, 0.5 * uDensity, depth);',
    '    float fade = depth * smoothstep(1.0, 0.9, depth);',
    '    col += StarLayer(uv * scale + i * 453.32) * fade;',
    '  }',
    '',
    '  if (uTransparent) {',
    '    float alpha = length(col);',
    '    alpha = smoothstep(0.0, 0.3, alpha);',
    '    alpha = min(alpha, 1.0);',
    '    gl_FragColor = vec4(col, alpha);',
    '  } else {',
    '    gl_FragColor = vec4(col, 1.0);',
    '  }',
    '}'
  ].join('\n');

  function compile(type, src){
    var s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if(!gl.getShaderParameter(s, gl.COMPILE_STATUS)){
      console.error(gl.getShaderInfoLog(s));
    }
    return s;
  }
  var vs = compile(gl.VERTEX_SHADER, vertSrc);
  var fs = compile(gl.FRAGMENT_SHADER, fragSrc);
  var program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if(!gl.getProgramParameter(program, gl.LINK_STATUS)){
    console.error(gl.getProgramInfoLog(program));
  }
  gl.useProgram(program);

  var positions = new Float32Array([-1,-1, 3,-1, -1,3]);
  var uvs = new Float32Array([0,0, 2,0, 0,2]);

  var posBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
  gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
  var posLoc = gl.getAttribLocation(program, 'position');
  gl.enableVertexAttribArray(posLoc);
  gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

  var uvBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, uvBuf);
  gl.bufferData(gl.ARRAY_BUFFER, uvs, gl.STATIC_DRAW);
  var uvLoc = gl.getAttribLocation(program, 'uv');
  gl.enableVertexAttribArray(uvLoc);
  gl.vertexAttribPointer(uvLoc, 2, gl.FLOAT, false, 0, 0);

  var u = {};
  ['uTime','uResolution','uFocal','uRotation','uStarSpeed','uDensity','uHueShift','uSpeed','uMouse',
   'uGlowIntensity','uSaturation','uMouseRepulsion','uTwinkleIntensity','uRotationSpeed',
   'uRepulsionStrength','uMouseActiveFactor','uAutoCenterRepulsion','uTransparent',
   'uScrollMix','uMixColor'].forEach(function(name){
    u[name] = gl.getUniformLocation(program, name);
  });

  var params = {
    focal:[0.5,0.5], rotation:[1.0,0.0], starSpeed:0.5, density:1.5,
    speed:1.0, glowIntensity:0.21, saturation:0.62,
    mouseRepulsion:true, repulsionStrength:2, twinkleIntensity:0.3,
    rotationSpeed:0.1, autoCenterRepulsion:0, transparent:false
  };

  gl.uniform2fv(u.uFocal, params.focal);
  gl.uniform2fv(u.uRotation, params.rotation);
  gl.uniform1f(u.uDensity, params.density);
  gl.uniform1f(u.uSpeed, params.speed);
  gl.uniform1f(u.uGlowIntensity, params.glowIntensity);
  gl.uniform1f(u.uSaturation, params.saturation);
  gl.uniform1i(u.uMouseRepulsion, params.mouseRepulsion ? 1 : 0);
  gl.uniform1f(u.uTwinkleIntensity, params.twinkleIntensity);
  gl.uniform1f(u.uRotationSpeed, params.rotationSpeed);
  gl.uniform1f(u.uRepulsionStrength, params.repulsionStrength);
  gl.uniform1f(u.uAutoCenterRepulsion, params.autoCenterRepulsion);
  gl.uniform1i(u.uTransparent, params.transparent ? 1 : 0);
  gl.uniform3f(u.uMixColor, 166/255, 183/255, 255/255);

  var DPR = Math.min(window.devicePixelRatio || 1, 1.5);
  var W, H;
  function resize(){
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = Math.round(W*DPR); canvas.height = Math.round(H*DPR);
    canvas.style.width = W+'px'; canvas.style.height = H+'px';
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform3f(u.uResolution, canvas.width, canvas.height, canvas.width/canvas.height);
  }
  window.addEventListener('resize', resize);
  resize();
  gl.clearColor(0.02, 0.02, 0.043, 1.0);

  var hue = 260, targetHue = 260;
  var mouse = {x:0.5,y:0.5}, targetMouse = {x:0.5,y:0.5};
  var mouseActive = 0, targetMouseActive = 0;

  window.addEventListener('mousemove', function(e){
    targetMouse.x = e.clientX / W;
    targetMouse.y = 1.0 - e.clientY / H;
    targetMouseActive = 1.0;
  });
  window.addEventListener('mouseleave', function(){ targetMouseActive = 0.0; });
  window.addEventListener('touchmove', function(e){
    if(e.touches && e.touches[0]){
      targetMouse.x = e.touches[0].clientX / W;
      targetMouse.y = 1.0 - e.touches[0].clientY / H;
      targetMouseActive = 1.0;
    }
  }, {passive:true});

  var zones = document.querySelectorAll('[data-hue]');
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting && en.intersectionRatio > 0.35){
          targetHue = parseFloat(en.target.getAttribute('data-hue'));
        }
      });
    }, {threshold:[0.35,0.5,0.65]});
    zones.forEach(function(z){ io.observe(z); });
  }

  function frame(t){
    requestAnimationFrame(frame);
    hue += (targetHue - hue) * 0.02;
    document.documentElement.style.setProperty('--accent-h', hue.toFixed(1));

    mouse.x += (targetMouse.x - mouse.x) * 0.05;
    mouse.y += (targetMouse.y - mouse.y) * 0.05;
    mouseActive += (targetMouseActive - mouseActive) * 0.05;

    var time = (t || 0) * 0.001;
    gl.uniform1f(u.uTime, time);
    gl.uniform1f(u.uStarSpeed, (time * params.starSpeed) / 10.0);
    gl.uniform1f(u.uHueShift, hue);
    gl.uniform2f(u.uMouse, mouse.x, mouse.y);
    gl.uniform1f(u.uMouseActiveFactor, mouseActive);

    var scrollable = document.documentElement.scrollHeight - window.innerHeight;
    var scrollProgress = scrollable > 0 ? Math.min(1, Math.max(0, window.scrollY / scrollable)) : 0;
    gl.uniform1f(u.uScrollMix, scrollProgress * scrollProgress);

    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
  requestAnimationFrame(frame);
})();

(function(){
  var GRADIENT_POSITIONS = ['80% 55%','69% 34%','8% 6%','41% 38%','86% 85%','82% 18%','51% 4%'];
  var GRADIENT_KEYS = ['--gradient-one','--gradient-two','--gradient-three','--gradient-four','--gradient-five','--gradient-six','--gradient-seven'];
  var COLOR_MAP = [0,1,2,0,1,2,1];

  function hueColorSet(h){
    return [
      'hsl('+(((h)%360+360)%360)+' 85% 68%)',
      'hsl('+(((h+45)%360+360)%360)+' 85% 62%)',
      'hsl('+(((h-45)%360+360)%360)+' 85% 62%)'
    ];
  }

  function applyGradientVars(el, colors){
    for(var i=0;i<7;i++){
      var c = colors[COLOR_MAP[i]];
      el.style.setProperty(GRADIENT_KEYS[i], 'radial-gradient(at '+GRADIENT_POSITIONS[i]+', '+c+' 0px, transparent 50%)');
    }
    el.style.setProperty('--gradient-base', 'linear-gradient('+colors[0]+' 0 100%)');
  }

  function applyGlowVars(el, hue, intensity){
    var base = (((hue%360)+360)%360)+'deg 85% 68%';
    var opac = [100,60,50,40,30,20,10];
    var keys = ['','-60','-50','-40','-30','-20','-10'];
    for(var i=0;i<opac.length;i++){
      el.style.setProperty('--glow-color'+keys[i], 'hsl('+base+' / '+Math.min(opac[i]*intensity,100)+'%)');
    }
  }

  var cards = Array.prototype.slice.call(document.querySelectorAll('.glow-card'));
  cards.forEach(function(card){
    var span = document.createElement('span');
    span.className = 'edge-light';
    card.appendChild(span);
    card.style.setProperty('--card-bg', 'rgba(5,5,11,0.92)');

    function centerOf(){ var r = card.getBoundingClientRect(); return [r.width/2, r.height/2]; }
    function edgeProximity(x,y){
      var c = centerOf(), cx=c[0], cy=c[1];
      var dx = x-cx, dy = y-cy;
      var kx = Infinity, ky = Infinity;
      if(dx!==0) kx = cx/Math.abs(dx);
      if(dy!==0) ky = cy/Math.abs(dy);
      return Math.min(Math.max(1/Math.min(kx,ky), 0), 1);
    }
    function cursorAngle(x,y){
      var c = centerOf(), cx=c[0], cy=c[1];
      var dx = x-cx, dy = y-cy;
      if(dx===0 && dy===0) return 0;
      var deg = Math.atan2(dy,dx)*(180/Math.PI)+90;
      if(deg<0) deg += 360;
      return deg;
    }
    card.addEventListener('pointermove', function(e){
      var rect = card.getBoundingClientRect();
      var x = e.clientX - rect.left, y = e.clientY - rect.top;
      card.style.setProperty('--edge-proximity', (edgeProximity(x,y)*100).toFixed(3));
      card.style.setProperty('--cursor-angle', cursorAngle(x,y).toFixed(3)+'deg');
    });
  });

  function refreshGlowColors(){
    var hue = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--accent-h')) || 260;
    var colors = hueColorSet(hue);
    cards.forEach(function(card){
      applyGradientVars(card, colors);
      applyGlowVars(card, hue, 1.0);
    });
  }
  refreshGlowColors();
  setInterval(refreshGlowColors, 300);
})();

(function(){
  var nav = document.getElementById('siteNav');
  var feImage = document.getElementById('navGlassMap');
  if(!nav || !feImage) return;

  function supportsSVGFilters(){
    var ua = navigator.userAgent;
    var isWebkit = /Safari/.test(ua) && !/Chrome/.test(ua);
    var isFirefox = /Firefox/.test(ua);
    if(isWebkit || isFirefox) return false;
    var div = document.createElement('div');
    div.style.backdropFilter = 'url(#navGlassFilter)';
    return div.style.backdropFilter !== '';
  }

  function buildDisplacementURI(w, h){
    var borderWidth = 0.07, borderRadius = 0, brightness = 50, opacity = 0.93, blur = 11;
    var edgeSize = Math.min(w, h) * (borderWidth * 0.5);
    var svg =
      '<svg viewBox="0 0 '+w+' '+h+'" xmlns="http://www.w3.org/2000/svg">'+
        '<defs>'+
          '<linearGradient id="navRedGrad" x1="100%" y1="0%" x2="0%" y2="0%"><stop offset="0%" stop-color="#0000"/><stop offset="100%" stop-color="red"/></linearGradient>'+
          '<linearGradient id="navBlueGrad" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" stop-color="#0000"/><stop offset="100%" stop-color="blue"/></linearGradient>'+
        '</defs>'+
        '<rect x="0" y="0" width="'+w+'" height="'+h+'" fill="black"></rect>'+
        '<rect x="0" y="0" width="'+w+'" height="'+h+'" rx="'+borderRadius+'" fill="url(#navRedGrad)" />'+
        '<rect x="0" y="0" width="'+w+'" height="'+h+'" rx="'+borderRadius+'" fill="url(#navBlueGrad)" style="mix-blend-mode:difference" />'+
        '<rect x="'+edgeSize+'" y="'+edgeSize+'" width="'+(w-edgeSize*2)+'" height="'+(h-edgeSize*2)+'" rx="'+borderRadius+'" fill="hsl(0 0% '+brightness+'% / '+opacity+')" style="filter:blur('+blur+'px)" />'+
      '</svg>';
    return 'data:image/svg+xml,'+encodeURIComponent(svg);
  }

  function updateDisplacementMap(){
    var rect = nav.getBoundingClientRect();
    var w = rect.width || 400, h = rect.height || 64;
    var uri = buildDisplacementURI(w, h);
    feImage.setAttribute('href', uri);
    feImage.setAttributeNS('http://www.w3.org/1999/xlink', 'href', uri);
  }

  if(supportsSVGFilters()){
    nav.classList.add('nav-glass-svg');
    updateDisplacementMap();
    if('ResizeObserver' in window){
      new ResizeObserver(function(){ updateDisplacementMap(); }).observe(nav);
    } else {
      window.addEventListener('resize', updateDisplacementMap);
    }
  }
})();

(function(){
var burger = document.getElementById('navBurger');
var mobileMenu = document.getElementById('mobileMenu');
var closeBtn = document.getElementById('mobileMenuClose');
function openMenu(){ mobileMenu.classList.add('open'); burger.setAttribute('aria-expanded','true'); }
function closeMenu(){ mobileMenu.classList.remove('open'); burger.setAttribute('aria-expanded','false'); }
burger.addEventListener('click', openMenu);
closeBtn.addEventListener('click', closeMenu);
mobileMenu.querySelectorAll('[data-close]').forEach(function(el){ el.addEventListener('click', closeMenu); });
document.addEventListener('keydown', function(e){ if(e.key === 'Escape'){ closeMenu(); } });
})();

(function(){
  document.querySelectorAll('.pill').forEach(function(btn){
    Array.prototype.slice.call(btn.childNodes).forEach(function(node){
      if(node.nodeType === Node.TEXT_NODE && node.textContent.trim().length){
        var span = document.createElement('span');
        span.className = 'shiny-text';
        span.textContent = node.textContent;
        btn.replaceChild(span, node);
      }
    });
  });
})();

(function(){
  var STAGGER = 0.03;

  function wrapChars(node){
    if(node.nodeType === Node.TEXT_NODE){
      var frag = document.createDocumentFragment();
      var words = node.textContent.split(' ');
      words.forEach(function(word, wi){
        if(word.length){
          var wordSpan = document.createElement('span');
          wordSpan.className = 'sf-word';
          for(var i=0;i<word.length;i++){
            var span = document.createElement('span');
            span.className = 'sf-char';
            span.textContent = word[i];
            wordSpan.appendChild(span);
          }
          frag.appendChild(wordSpan);
        }
        if(wi < words.length-1){
          frag.appendChild(document.createTextNode(' '));
        }
      });
      node.parentNode.replaceChild(frag, node);
    } else if(node.nodeType === Node.ELEMENT_NODE){
      Array.prototype.slice.call(node.childNodes).forEach(wrapChars);
    }
  }

  var headings = Array.prototype.slice.call(document.querySelectorAll('.sf-heading'));
  headings.forEach(function(h){ wrapChars(h); });

  var groups = headings.map(function(h){
    return { el: h, chars: Array.prototype.slice.call(h.querySelectorAll('.sf-char')) };
  });

  function easeBackInOut(x){
    var c1 = 1.70158 * 1.525;
    return x < 0.5
      ? (Math.pow(2*x, 2) * ((c1+1) * 2*x - c1)) / 2
      : (Math.pow(2*x-2, 2) * ((c1+1) * (x*2-2) + c1) + 2) / 2;
  }

  var ticking = false;
  function update(){
    ticking = false;
    var vh = window.innerHeight;
    var start = vh * 0.92, end = vh * 0.42;
    groups.forEach(function(g){
      var rect = g.el.getBoundingClientRect();
      if(rect.bottom < -200 || rect.top > vh + 200) return;
      var p = (start - rect.top) / (start - end);
      p = Math.max(0, Math.min(1, p));
      var n = g.chars.length;
      var span = 1 / (1 + (n-1) * STAGGER);
      g.chars.forEach(function(c, i){
        var charStart = i * STAGGER * span;
        var localP = (p - charStart) / span;
        localP = Math.max(0, Math.min(1, localP));
        var e = easeBackInOut(localP);
        var ty = (1-e) * 120;
        var sy = 1 + (1-e) * 1.3;
        var sx = 1 - (1-e) * 0.3;
        c.style.opacity = Math.max(0, Math.min(1, localP*2)).toFixed(3);
        c.style.transform = 'translateY('+ty.toFixed(2)+'%) scaleY('+sy.toFixed(3)+') scaleX('+sx.toFixed(3)+')';
      });
    });
  }
  function onScroll(){
    if(!ticking){ ticking = true; requestAnimationFrame(update); }
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll);
  update();
})();

(function(){
  var WA_PHONE = '5491131652844';
  var el = document.getElementById('whatsappFloat');
  if(el) el.href = 'https://wa.me/' + WA_PHONE + '?text=' + encodeURIComponent("Hi KMS, I'm visiting from your site and I have a question");
})();

var WEB3FORMS_KEYS = ['e7a0904a-a886-49a3-b9e7-2c716fe8b3b2', '81a34f81-7dc3-4089-b3d2-a4e7aaec9344'];

// URL del receptor de leads (planilla "Kiss My Site — Leads")
var LEADS_ENDPOINT = 'https://script.google.com/macros/s/AKfycby765oYYaSRyrRdJYjCElgZ8Of9y3vm5f2w9gzYllQlE-G7SCm6hStGH4j_yzQU2JxK/exec';

function submitToWeb3Forms(formEl, subject){
  var payload = {};
  new FormData(formEl).forEach(function(value, key){ payload[key] = value; });
  payload.subject = subject;
  payload.from_name = 'Kiss My Site website';

  try {
    var slug = formEl.id.replace('svc2form-', '');
    var attr = window.Atribucion ? window.Atribucion.get() : {};
    var eventId = 'lead-' + Date.now() + '-' + Math.random().toString(36).slice(2, 10);
    var cookie = function(n){ var m = document.cookie.match('(?:^|; )' + n + '=([^;]*)'); return m ? decodeURIComponent(m[1]) : ''; };
    var copia = Object.assign({}, payload, attr, {
      servicio: slug, url: location.href, event_id: eventId,
      fbp: cookie('_fbp'), fbc: cookie('_fbc'), user_agent: navigator.userAgent
    });
    delete copia.access_key; delete copia.subject; delete copia.from_name;
    fetch(LEADS_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(copia)
    }).catch(function(){});

    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'generate_lead', servicio: slug, currency: 'ARS', event_id: eventId });
  } catch (e) {}

  return Promise.all(WEB3FORMS_KEYS.map(function(key){
    var body = Object.assign({}, payload, { access_key: key });
    return fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(body)
    }).catch(function(err){ return { ok:false, error: err }; });
  }));
}

var pageLoadedAt = Date.now();
var MIN_SUBMIT_MS = 2000;
function looksLikeSpam(formEl){
  var hp = formEl.querySelector('[name="_hp"]');
  if(hp && hp.value) return true;
  var bc = formEl.querySelector('[name="botcheck"]');
  if(bc && bc.checked) return true;
  if(Date.now() - pageLoadedAt < MIN_SUBMIT_MS) return true;
  return false;
}

document.querySelectorAll('.svc2-form').forEach(function(f){
  f.addEventListener('submit', function(e){
    e.preventDefault();
    var card = f.closest('.svc2-form-card');
    if(looksLikeSpam(f)){
      f.style.display = 'none';
      var okSpam = card && card.querySelector('.svc2-success');
      if(okSpam) okSpam.classList.add('show');
      return;
    }
    var btn = f.querySelector('button[type="submit"]');
    if(btn) btn.disabled = true;
    var slug = f.id.replace('svc2form-', '');
    submitToWeb3Forms(f, 'New pSEO lead — ' + slug).then(function(){
      f.style.display = 'none';
      var ok = card && card.querySelector('.svc2-success');
      if(ok) ok.classList.add('show');
    }).finally(function(){ if(btn) btn.disabled = false; });
  });
});
