/* mcq-ideate: the "ideated" learner-colours standalone (_concept-mcq-ideate.html), layered on the kids design.
   Murci, 2026-09-29: a second standalone to present beside the learner-colours one, with
   1 · the TopoField prompt's background (MengTo/threeui, MIT): a faint 48 px grid and thin contour lines from 2D simplex
       noise, drifting. Drawn TRANSPARENT over the kids page's own colours (Murci: "the same colour as the first kids
       design"): its charcoal and its corner lights stay; the lines are light and faint (the prompt's black page and
       black vignettes are not used).
   Murci, same day: "make the background animation change colours": the lines drift through the four choice cards'
   colours (over time, a lap in 40 s, and across the screen), no red and no green (they mean wrong and right).
   2 · the tunnel-hero prompt's idea in each choice card, refit (Murci: it must "fit the cards whole and not center", and
       must not change the cards' look or colour): the prompt draws CIRCULAR rings, which on a wide card can only be a
       disc in the middle, and its white points with a "screen" blend turned every card grey. Here each ring is the
       card's own rounded rectangle: the largest is the card's edge, smaller ones fall back to a vanishing point that
       drifts along a winding path (the prompt's TunnelPath idea), dotted like the prompt's points, with dotted lines
       from the card's corners to it, so the card reads as a hollow 3D box. Drawn in the card's OWN colour (--c).
   ?cards=tunnel (Murci: "more like the one from the prompt ... in terms of shape ... but it had a lot of particles"):
   the prompt's own shape instead: CIRCULAR rings of points coming toward you along its winding path (TunnelPath),
   brighter as they near, every other pair dimmer (its POINT_COLOR_A / B). 14 rings x 24 points (the prompt: 96 x 128),
   scaled to the card's WIDTH so the near rings run past its edges (scaled to its height, as the first cut was, the
   biggest ring could not reach the sides: a disc in the middle), in the card's colour, at about a third of its speed.
   ?page=tunnel (Murci: "another design that now uses the choice card animation background as its background and the
   choice cards to have no background animation", then "the exact [colour] as the one in the prompt ... as many
   particles as it has"): the prompt's own shader, unchanged, full screen on black; plain cards; no TopoField lines.
   Cost: the background is one WebGL canvas (the prompt's shader, per pixel); the cards are plain 2D canvases, a dozen
   dotted outlines each (not the prompt's 96 layers per pixel). 30 frames a second, paused while the tab is hidden;
   reduced motion: one still frame.
   Murci, same day: "slow and not that fast, seamless ... not a lot of particles because the cards are small": 5 rings, a new
   one about every 5 s; 30 dots per ring (22 at first; Murci: "increase ... just a bit"), 8 per corner line (6) spaced by the ring's own perimeter (a fixed spacing made the dots crawl along
   the outline as the ring grew: now they only spread apart, as perspective does); smooth fades; a slow drift. */
(function () {
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- 1 · the background: TopoField's fragment shader, with its colour output made transparent and faint ----
  const VS = "attribute vec2 a; void main() { gl_Position = vec4(a, 0.0, 1.0); }";
  const TOPO_FS = `precision highp float;
uniform vec2 u_resolution; uniform float u_time; uniform float u_dpr; uniform float u_mono;
vec3 permute(vec3 x) { return mod(((x*34.0)+1.0)*x, 289.0); }
float snoise(vec2 v){
  const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
  vec2 i = floor(v + dot(v, C.yy)); vec2 x0 = v - i + dot(i, C.xx);
  vec2 i1; i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz; x12.xy -= i1; i = mod(i, 289.0);
  vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));
  vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0); m = m*m; m = m*m;
  vec3 x = 2.0 * fract(p * C.www) - 1.0; vec3 h = abs(x) - 0.5; vec3 ox = floor(x + 0.5); vec3 a0 = x - ox;
  m *= 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);
  vec3 g; g.x = a0.x * x0.x + h.x * x0.y; g.yz = a0.yz * x12.xz + h.yz * x12.yw; return 130.0 * dot(m, g); }
void main() {
  vec2 st = gl_FragCoord.xy / u_resolution.xy; st.x *= u_resolution.x / u_resolution.y;
  float gridSize = 48.0 * u_dpr; vec2 gridFract = fract(gl_FragCoord.xy / gridSize); float lineThickness = 1.0 / gridSize;
  float gridLines = clamp(step(1.0 - lineThickness, gridFract.x) + step(1.0 - lineThickness, gridFract.y), 0.0, 1.0) * 0.05;
  vec2 noisePos = st * 1.4 + vec2(u_time * 0.015, u_time * 0.025); float n = snoise(noisePos) * 0.5 + 0.5;
  float triangleWave = abs(fract(n * 10.0) - 0.5) * 2.0; float topoLines = smoothstep(0.02, 0.00, triangleWave) * 0.30;
  // The lines' colour: the four choice cards' colours in turn (violet, sky, amber, pink), drifting over time (a lap in
  // 40 s) and across the screen (a soft diagonal band), smoothly blended; the grid stays a neutral white.
  float h = fract(u_time * 0.025 + st.x * 0.22 + st.y * 0.12) * 4.0;
  vec3 c0 = vec3(0.486, 0.227, 0.929), c1 = vec3(0.055, 0.647, 0.914), c2 = vec3(0.961, 0.620, 0.043), c3 = vec3(0.859, 0.153, 0.467);
  float f = smoothstep(0.0, 1.0, fract(h));
  vec3 lineCol = h < 1.0 ? mix(c0, c1, f) : h < 2.0 ? mix(c1, c2, f) : h < 3.0 ? mix(c2, c3, f) : mix(c3, c0, f);
  lineCol = mix(lineCol, vec3(1.0), 0.25);   // a touch of white: lines read as light, not as paint
  if (u_mono > 0.5) { lineCol = vec3(1.0); topoLines *= 0.6; }   // ?cards=tunnel, on its dark blue page: white and fainter (coloured lines vanish or clash on blue)
  float a = clamp(gridLines + topoLines, 0.0, 1.0);
  gl_FragColor = vec4(vec3(1.0) * gridLines + lineCol * topoLines, a); }`;   // premultiplied: coloured lines and a white grid over the page's own colours

  // ?cards=tunnel: the tunnel in the cards, on a dark blue page. ?page=tunnel: the tunnel is the PAGE's background (full
  // screen, behind everything), the cards have none, and there are no TopoField lines (one background, not two).
  const Q = new URLSearchParams(location.search), PAGE_TUNNEL = Q.get("page") === "tunnel", BLUE = Q.get("cards") === "tunnel";
  if (BLUE) document.body.classList.add("page-blue");   // its page is a dark blue (mcq-ideate.css .page-blue)
  if (PAGE_TUNNEL) document.body.classList.add("page-prompt");   // its page is the prompt's: black (mcq-ideate.css .page-prompt)
  const bg = document.createElement("canvas"); bg.className = "topo"; bg.setAttribute("aria-hidden", "true"); if (!PAGE_TUNNEL) document.body.prepend(bg);
  const gl = PAGE_TUNNEL ? null : bg.getContext("webgl", { alpha: true, premultipliedAlpha: true, antialias: false, depth: false });
  let topo = null;
  if (gl) try {
    const mk = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error("mcq-ideate shader: " + gl.getShaderInfoLog(s)); return s; };
    const p = gl.createProgram(); gl.attachShader(p, mk(gl.VERTEX_SHADER, VS)); gl.attachShader(p, mk(gl.FRAGMENT_SHADER, TOPO_FS)); gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error("mcq-ideate link: " + gl.getProgramInfoLog(p));
    gl.useProgram(p); gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer()); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const at = gl.getAttribLocation(p, "a"); gl.enableVertexAttribArray(at); gl.vertexAttribPointer(at, 2, gl.FLOAT, false, 0, 0);
    topo = { res: gl.getUniformLocation(p, "u_resolution"), time: gl.getUniformLocation(p, "u_time"), dpr: gl.getUniformLocation(p, "u_dpr") };
    gl.uniform1f(gl.getUniformLocation(p, "u_mono"), BLUE ? 1 : 0);
  } catch (e) { console.error(e); }
  function sizeTopo() { if (!topo) return; const d = Math.min(devicePixelRatio || 1, 1.5); bg.width = Math.round(innerWidth * d); bg.height = Math.round(innerHeight * d);
    gl.viewport(0, 0, bg.width, bg.height); gl.uniform2f(topo.res, bg.width, bg.height); gl.uniform1f(topo.dpr, d); }
  sizeTopo(); addEventListener("resize", sizeTopo);

  // ---- 2 · the hollow box in each choice card ----
  // Every choice card gets a canvas as its first child (the component rebuilds the cards for each question).
  function addCanvases() { document.querySelectorAll(".mcqp #mq-tiles .tile .face, .mcqp #mq-heroLayer .tile .face").forEach(f => {
    if (f.querySelector(":scope > .tun")) return; const c = document.createElement("canvas"); c.className = "tun"; c.setAttribute("aria-hidden", "true"); f.prepend(c); }); }
  if (!PAGE_TUNNEL) { new MutationObserver(addCanvases).observe(document.body, { childList: true, subtree: true }); addCanvases(); }   // ?page=tunnel: the cards have none

  // ALPHA: a dot is at most 0.45 of its card's colour, so the words over it stay readable. Computed: white text over a
  // full dot on the dark card (#151419) is 5.9:1 on amber, the worst (sky 6.9, pink 9.3, violet 10.1); at 0.6-0.62 amber
  // fell to 4.1 / 3.9:1, under WCAG's 4.5.
  const D = Math.min(devicePixelRatio || 1, 2), RINGS = 5, DOTS = 30, CYCLE = 26, R = 18;   // CYCLE: seconds for a ring from the back to the edge   // R: the card's corner radius (mcq-play.css .side)
  function box(x, w, h, cx, cy, s, rad) {                                  // a rounded rectangle, the card shrunk by s toward (cx, cy)
    const bw = w * s, bh = h * s, x0 = cx + (w / 2 - cx) * s - bw / 2, y0 = cy + (h / 2 - cy) * s - bh / 2;
    const r = Math.max(1, rad * s); x.beginPath(); if (x.roundRect) x.roundRect(x0, y0, bw, bh, r); else x.rect(x0, y0, bw, bh);   /* roundRect: Safari 16+, Chrome 99+ */ return 2 * (bw + bh) - (8 - 2 * Math.PI) * r; }   // its perimeter
  const ease = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u);
  function drawCard(c, t) {
    const w = c.offsetWidth, h = c.offsetHeight; if (!w || !h) return;
    const pw = Math.round(w * D), ph = Math.round(h * D); if (c.width !== pw || c.height !== ph) { c.width = pw; c.height = ph; }
    const tile = c.closest(".tile"), i = +(tile && tile.dataset.i) || 0;
    if (!c._rgb) c._rgb = (getComputedStyle(tile || c).getPropertyValue("--c").trim() || "255,255,255");   // the card's own colour
    const x = c.getContext("2d"); x.setTransform(D, 0, 0, D, 0, 0); x.clearRect(0, 0, w, h); x.lineCap = "round"; x.lineWidth = 1.7;
    // The vanishing point wanders along a winding path (the prompt's TunnelPath: two sines per axis), each card its own.
    const z = t * 0.11 + i * 1.7, cx = w / 2 + w * 0.07 * (Math.sin(z * 1.3) + 0.6 * Math.sin(z * 0.5 + 0.3)), cy = h / 2 + h * 0.12 * (Math.cos(z * 0.9) + 0.5 * Math.cos(z * 0.3));
    // Depth lines: from the card's corners toward the vanishing point, dotted, fading as they go in.
    const inner = [cx + (w / 2 - cx) * 0.06 - w * 0.03, cy + (h / 2 - cy) * 0.06 - h * 0.03, w * 0.06, h * 0.06];
    [[R * 0.3, R * 0.3, inner[0], inner[1]], [w - R * 0.3, R * 0.3, inner[0] + inner[2], inner[1]], [R * 0.3, h - R * 0.3, inner[0], inner[1] + inner[3]], [w - R * 0.3, h - R * 0.3, inner[0] + inner[2], inner[1] + inner[3]]].forEach(([ax, ay, bx, by]) => {
      const g = x.createLinearGradient(ax, ay, bx, by); g.addColorStop(0, `rgba(${c._rgb},0.34)`); g.addColorStop(1, `rgba(${c._rgb},0)`);
      x.strokeStyle = g; x.setLineDash([0.01, Math.hypot(bx - ax, by - ay) / 8]); x.beginPath(); x.moveTo(ax, ay); x.lineTo(bx, by); x.stroke(); });   // 8 dots a line
    // The rings: the card's outline at every depth, moving toward you (a ring is born at the vanishing point, grows to the
    // card's edge and fades there); perspective: s = p^2, so they speed up as they come near, and their dots spread out.
    for (let k = 0; k < RINGS; k++) {
      const p = ((t / CYCLE + k / RINGS) % 1), s = 0.05 + p * p * 0.95;
      const a = ease(p / 0.25) * ease((1 - p) / 0.2) * (0.17 + 0.28 * p);   // fades in deep and out at the edge, smoothly; max 0.45 (ALPHA)
      if (a <= 0.01) continue;
      x.strokeStyle = `rgba(${c._rgb},${a.toFixed(3)})`; const per = box(x, w, h, cx, cy, s, R); x.setLineDash([0.01, per / DOTS]); x.stroke(); }
  }

  // ?cards=tunnel: the prompt's circular tunnel, few points, in the card's colour.
  const TUNNEL = new URLSearchParams(location.search).get("cards") === "tunnel", LAYERS = 14, POINTS = 24, TAU = Math.PI * 2;
  const path = z => [0.2 * Math.sin(TAU * z * 0.5) + 0.4 * Math.sin(TAU * z * 0.2 + 0.3), 0.3 * Math.cos(TAU * z * 0.3) + 0.2 * Math.cos(TAU * z * 0.1)];   // the prompt's TunnelPath
  // The rings: LAYERS rings of `points` dots coming toward you (depth pz 1 -> 0), the prompt's radius curve and winding,
  // brighter as they near, every other pair dimmer (its POINT_COLOR_A / B). U: one tunnel unit in pixels.
  function rings(x, w, h, U, t, seed, colourOf, maxA, points, layers, dot0, dotK, wind) {
    const cam = t * 0.12 + seed, co = path(cam), spin = t * 0.05;
    for (let k = 0; k < layers; k++) {
      const pz = 1 - ((k / layers + cam * 0.35) % 1);
      const r = 0.15 / Math.pow(pz * 0.8 + 0.4, 2) * U;
      const o = path(cam + pz), ox = (o[0] - co[0]) * U * wind, oy = (o[1] - co[1]) * U * wind;
      const a = (1 - pz) * Math.min(1, pz / 0.1) * Math.min(1, (1 - pz) / 0.15) * (Math.floor(k / 2) % 2 ? 0.7 : 1) * maxA;   // fades at both ends
      if (a <= 0.01) continue;
      const dot = dot0 + dotK * (1 - pz), cx = w / 2 - ox, cy = h / 2 - oy;
      x.fillStyle = `rgba(${colourOf(k)},${a.toFixed(3)})`; x.beginPath();
      for (let j = 0; j < points; j++) { const q = spin + j / points * TAU, px = cx + Math.cos(q) * r, py = cy + Math.sin(q) * r;
        if (px < -dot || px > w + dot || py < -dot || py > h + dot) continue; x.moveTo(px + dot, py); x.arc(px, py, dot, 0, TAU); }
      x.fill(); }
  }
  function drawTunnel(c, t) {   // in a card: its colour, half its width a unit, max 0.45 (ALPHA)
    const w = c.offsetWidth, h = c.offsetHeight; if (!w || !h) return;
    const pw = Math.round(w * D), ph = Math.round(h * D); if (c.width !== pw || c.height !== ph) { c.width = pw; c.height = ph; }
    const tile = c.closest(".tile"), i = +(tile && tile.dataset.i) || 0;
    if (!c._rgb) c._rgb = (getComputedStyle(tile || c).getPropertyValue("--c").trim() || "255,255,255");
    const x = c.getContext("2d"); x.setTransform(D, 0, 0, D, 0, 0); x.clearRect(0, 0, w, h);
    rings(x, w, h, w * 0.5, t, i * 2.3, () => c._rgb, 0.45, POINTS, LAYERS, 0.6, 1.1, 0.35);
  }
  // ?page=tunnel: the tunnel-hero prompt EXACTLY (Murci: "the exact [colour] as the one in the prompt and ... the same
  // animation with as many particles as it has"): its fragment shader as given (96 rings x 128 points, white / 0.7 grey
  // points, SPEED 0.7), iTime advanced at 0.5 x real time (its demo's speedMultiplier), pixel ratio capped at 2 (its
  // renderer), on black. Only ported from three.js to raw WebGL 1 (three's ShaderMaterial adds the precision line).
  // Then (Murci: "slow the speed ... lighter black not that pure black"): its clock at 0.12 x (asked twice), and a softer black #17171b.
  // The one change in its shader: points faded toward black (ptColor * shade), which on a lighter base would show the far
  // ones as DARK dots, so they now fade from the base toward white (mix(u_bg, ptColor, shade)); shape and count as given.
  const PROMPT_FS = `precision highp float;
uniform float iTime;
uniform vec3 iResolution;
uniform vec3 u_bg;
#define TAU 6.2831853071795865
#define TUNNEL_LAYERS 96
#define RING_POINTS 128
#define POINT_SIZE 1.8
#define POINT_COLOR_A vec3(1.0)
#define POINT_COLOR_B vec3(0.7)
#define SPEED 0.7
float sq(float x){ return x*x; }
vec2 AngRep(vec2 uv, float angle){
  vec2 polar = vec2(atan(uv.y, uv.x), length(uv));
  polar.x = mod(polar.x + angle/2.0, angle) - angle/2.0;
  return polar.y * vec2(cos(polar.x), sin(polar.x));
}
float sdCircle(vec2 uv, float r){ return length(uv) - r; }
vec3 MixShape(float sd, vec3 fill, vec3 target){
  float blend = smoothstep(0.0, 1.0/iResolution.y, sd);
  return mix(fill, target, blend);
}
vec2 TunnelPath(float x){
  vec2 offs = vec2(
    0.2 * sin(TAU * x * 0.5) + 0.4 * sin(TAU * x * 0.2 + 0.3),
    0.3 * cos(TAU * x * 0.3) + 0.2 * cos(TAU * x * 0.1)
  );
  offs *= smoothstep(1.0, 4.0, x);
  return offs;
}
void main(){
  vec2 res = iResolution.xy / iResolution.y;
  vec2 uv = gl_FragCoord.xy / iResolution.y - res/2.0;
  vec3 color = u_bg;
  float repAngle = TAU / float(RING_POINTS);
  float pointSize = POINT_SIZE / (2.0 * iResolution.y);
  float camZ = iTime * SPEED;
  vec2 camOffs = TunnelPath(camZ);
  for(int i = 1; i <= TUNNEL_LAYERS; i++){
    float pz = 1.0 - (float(i) / float(TUNNEL_LAYERS));
    pz -= mod(camZ, 4.0 / float(TUNNEL_LAYERS));
    vec2 offs = TunnelPath(camZ + pz) - camOffs;
    float ringRad = 0.15 * (1.0 / sq(pz * 0.8 + 0.4));
    if(abs(length(uv + offs) - ringRad) < pointSize * 1.5){
      vec2 aruv = AngRep(uv + offs, repAngle);
      float pdist = sdCircle(aruv - vec2(ringRad, 0), pointSize);
      vec3 ptColor = (mod(float(i/2), 2.0) == 0.0) ? POINT_COLOR_A : POINT_COLOR_B;
      float shade = (1.0 - pz);
      color = MixShape(pdist, mix(u_bg, ptColor, shade), color);
    }
  }
  gl_FragColor = vec4(color, 1.0);
}`;
  let pageT = null;
  if (PAGE_TUNNEL) {
    const pc = document.createElement("canvas"); pc.className = "pagetun"; pc.setAttribute("aria-hidden", "true"); document.body.prepend(pc);
    const pg = pc.getContext("webgl", { antialias: true });                 // the prompt's renderer: antialias true
    if (pg) try {
      const mk = (type, src) => { const sh = pg.createShader(type); pg.shaderSource(sh, src); pg.compileShader(sh);
        if (!pg.getShaderParameter(sh, pg.COMPILE_STATUS)) throw new Error("mcq-ideate tunnel shader: " + pg.getShaderInfoLog(sh)); return sh; };
      const pp = pg.createProgram(); pg.attachShader(pp, mk(pg.VERTEX_SHADER, VS)); pg.attachShader(pp, mk(pg.FRAGMENT_SHADER, PROMPT_FS)); pg.linkProgram(pp);
      if (!pg.getProgramParameter(pp, pg.LINK_STATUS)) throw new Error("mcq-ideate tunnel link: " + pg.getProgramInfoLog(pp));
      pg.useProgram(pp); pg.bindBuffer(pg.ARRAY_BUFFER, pg.createBuffer()); pg.bufferData(pg.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), pg.STATIC_DRAW);
      const at = pg.getAttribLocation(pp, "a"); pg.enableVertexAttribArray(at); pg.vertexAttribPointer(at, 2, pg.FLOAT, false, 0, 0);
      pageT = { c: pc, gl: pg, time: pg.getUniformLocation(pp, "iTime"), res: pg.getUniformLocation(pp, "iResolution"), iTime: 0, lastS: 0 };
      pg.uniform3f(pg.getUniformLocation(pp, "u_bg"), 0x17 / 255, 0x17 / 255, 0x1b / 255);   // #17171b: a softer black than the prompt's
      const size = () => { const d = Math.min(devicePixelRatio || 1, 2); pc.width = Math.round(innerWidth * d); pc.height = Math.round(innerHeight * d);
        pg.viewport(0, 0, pc.width, pc.height); pg.uniform3f(pageT.res, pc.width, pc.height, 1); };
      size(); addEventListener("resize", size);
    } catch (e) { console.error(e); }
  }
  function drawPage(sec) {   // the prompt's clock (iTime += delta * 0.5), slowed to 0.12 (Murci, twice: "slow the speed", "slower"): 24% of its pace
    const d = sec - (pageT.lastS || sec); pageT.lastS = sec; pageT.iTime += d * 0.12;
    pageT.gl.uniform1f(pageT.time, pageT.iTime); pageT.gl.drawArrays(pageT.gl.TRIANGLE_STRIP, 0, 4);
  }

  const t0 = performance.now(); let last = 0;
  function frame(now) {
    if (!reduced) requestAnimationFrame(frame);
    if (document.hidden || now - last < 33) return; last = now;                                   // 30 fps: backgrounds, not a game
    const t = (now - t0) / 1000;
    if (topo) { gl.uniform1f(topo.time, t); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); }
    if (pageT) drawPage(t);
    document.querySelectorAll(".mcqp .face > .tun").forEach(c => { if (getComputedStyle(c).opacity !== "0") (TUNNEL ? drawTunnel : drawCard)(c, t); });   // a faded card (right, or dark) is not drawn
  }
  requestAnimationFrame(frame);
  if (reduced) setTimeout(() => frame(performance.now() + 1000), 600);   // reduced motion: one still frame once the cards are in
  window.MQ_IDEATE = { topo: !!topo, cards: PAGE_TUNNEL ? "none" : TUNNEL ? "tunnel" : "box", page: PAGE_TUNNEL ? "tunnel" : "topo" };
})();
