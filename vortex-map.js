import * as THREE from "three";

// <vortex-map>: the exam map as a road that runs back across nexera-hero's dotted wave to a finish line and dives into
// a whirlpool at the front, over the start card (brief 22; designed in _concept-map-portal.html).
//
// The page stays the source of truth. Its own layout (mapVals) places every mission; this element projects that
// same geometry onto the wave. Contract (attributes, all set by the page):
//   geom    JSON { nodes:[{ i, x, y }], fin:{ x, y }, caps:[{ y, label }] } — road-local px, as the page lays them out
//   paint   JSON [{ i, id, title, chip, chipBg, chipColor, tags, titleColor, fill, ring, lip, num, big, halo, badge,
//           anim, aria }] — each mission's medal as the page paints it (the element never re-derives a status)
//   finish  JSON { title, sub, aria }   the pill over the finish arch
//   next    the next mission's index (its label always shows; the arrow follows it)
//   lit     0..1 of the road lit (the score), eased over 1.3s like the page's own dash
//   road    CSS selector of the page's road box (its position is the road's origin; default [data-road])
//   anchor  CSS selector of the start card (the vortex's core sits 16px above its top; its border turns with the road)
//   hdr     px of sticky bars at the top      active  "false" hides it and stops its clock
//   bg      CSS background under the field     fade    "#rrggbb" the dots dissolve into (the background's base colour)
// Hooks the page already uses keep working: each medal is a light-DOM <button data-node="i">, the arch is
// [data-finishbadge], so focus return, bursts and "is it on screen" checks find them where they are DRAWN.
// Events (window): "vortex-open" { index }   "vortex-dir" { where: "up" | "down" | "here" }
// Methods: scrollToMission(i, smooth) · scrollToFinish(smooth) · ready · where
//
// Drawn from ONE value per frame (scrollY) on fixed layers: 0 the WebGL field (the hero's wave + the drain) · 1 the
// vortex · 2 the road (SVG) · 3 the medals (HTML, slotted) · 4 front. The host is an invisible absolute column that
// guarantees the page can scroll the first mission down onto the vortex.

const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const TIER = (() => { const q = (location.search.match(/[?&]tier=(high|mid|low)/) || [])[1]; if (q) return q;
  const cores = navigator.hardwareConcurrency || 8, mem = navigator.deviceMemory || 8, save = navigator.connection && navigator.connection.saveData;
  return save || cores <= 2 || mem <= 2 ? "low" : cores <= 4 || mem <= 4 ? "mid" : "high"; })();
const E = t => t * t * (3 - 2 * t), clamp = (v, a, b) => Math.max(a, Math.min(b, v)), clamp01 = v => v < 0 ? 0 : v > 1 ? 1 : v;
const TAU = 6.2832;

// ══ The field: nexera-hero's dotted wave (components/particle-field.tsx + lib/wave.ts), ported as-is ════════════════
// 40 × 60 dots, 150 apart, on a plane inclined by 0.15; wave = sin((ix + phase)·0.3)·50 + sin((iy + phase)·0.5)·50;
// colour rides the wave from blue (troughs) to violet (crests); camera fov 75 at (0, 355, 1220) looking at the origin.
const AX = 40, AY = 60, SEP = 150, SLOPE = 0.15, FX = 0.3, FY = 0.5, AMP = 50;
const BLUE = [50 / 255, 120 / 255, 1], PURPLE = [150 / 255, 60 / 255, 1];
// The drain. Units: the hole's rim = 1. The flow keeps the water's area (r² falls at a steady rate), so a ring of dots
// keeps its density as it cycles; with a free vortex's swirl each dot's path is a log spiral θ = θ₀ + B·ln(r₀/r), the
// pitch of the vortex's own arms (B = 1.9). Past the rim dots follow the funnel down, are swallowed, and re-enter.
const SPIRAL_B = 1.9, FLOW_C = 3.5, R_CORE = 0.2, R_EDGE = 4, INFL = 3, R_ARM = 2.6, SECTOR = TAU / 5, LOG_EDGE = Math.log(R_EDGE);
const ARM_W = [0.62, 0.44, 0.7, 0.5, 0.58], ARM_L = [1, 0.7, 0.9, 0.6, 0.8], ARM_OUT = 1.8;
const squeeze = r => { if (r <= 1 || r >= R_EDGE) return r; const t = r - 1; return 1 + t * (0.45 + t * (0.36667 - 0.06111 * t)); };

// Quality: the tier is a guess from cores and memory; the governor corrects it from real frame times, once per session.
//   1: the scene draws at 30fps   2: 1x resolution, no in-between dots   3: the wave moves only with the scroll, no streaks
let Q = TIER === "low" ? 1 : 0;

// ONE field per page, created on the first visit to the map and re-attached on every return: the map remounts on
// each visit, and a new WebGL context per visit is how pages run into the browser's context cap.
let FIELD = null;
function makeField() {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, innerWidth / innerHeight, 1, 10000);
  camera.position.set(0, 355, 1220); camera.lookAt(0, 0, 0);
  const renderer = new THREE.WebGLRenderer({ antialias: TIER !== "low", alpha: true, powerPreference: "low-power" });
  const ratio = low => low ? 1 : Math.min(devicePixelRatio, TIER === "high" ? 2 : TIER === "mid" ? 1.5 : 1);
  renderer.setPixelRatio(ratio(Q >= 2)); renderer.setSize(innerWidth, innerHeight); renderer.setClearColor(0x000000, 0);
  const count = AX * AY, pos = new Float32Array(count * 3), col = new Float32Array(count * 3);
  for (let ix = 0, i = 0; ix < AX; ix++) for (let iy = 0; iy < AY; iy++, i++) { pos[i * 3] = ix * SEP - (AX * SEP) / 2; pos[i * 3 + 2] = iy * SEP - (AY * SEP) / 2; }
  // grid: (ix, iy, gpu). gpu = 1: the hero's wave, computed on the GPU; 0: placed and coloured by the drain (CPU).
  const grid = new Float32Array(count * 3);
  for (let ix = 0, i = 0; ix < AX; ix++) for (let iy = 0; iy < AY; iy++, i++) { grid[i * 3] = ix; grid[i * 3 + 1] = iy; grid[i * 3 + 2] = 1; }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3)); geo.setAttribute("color", new THREE.BufferAttribute(col, 3)); geo.setAttribute("grid", new THREE.BufferAttribute(grid, 3));
  // The hero's crisp round dot: solid to 0.78 of the radius, then a thin anti-aliased edge.
  const dc = document.createElement("canvas"); dc.width = dc.height = 64; const dx = dc.getContext("2d"), gr = dx.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.78, "rgba(255,255,255,1)"); gr.addColorStop(1, "rgba(255,255,255,0)"); dx.fillStyle = gr; dx.fillRect(0, 0, 64, 64);
  const uni = { phase: { value: 0 }, size: { value: 10 * renderer.getPixelRatio() }, scale: { value: innerHeight * 0.5 }, map: { value: new THREE.CanvasTexture(dc) },
    fogNear: { value: 3200 }, fogFar: { value: 11000 }, fogColor: { value: new THREE.Vector3(0, 0, 0) } };
  let BG = [0, 0, 0];                                                 // the fade colour, linear (the drain's thinning dots)
  const mat = new THREE.ShaderMaterial({ uniforms: uni, transparent: true, depthWrite: false,
    vertexShader: `attribute vec3 color; attribute vec3 grid; uniform float phase, size, scale; varying vec3 vColor; varying float vFog;
      void main() {
        vec3 p = position; vec3 c = color;
        if (grid.z > 0.5) {                                   // nexera-hero's wave (lib/wave.ts) and its blue-to-violet colour
          float w = sin((grid.x + phase) * ${FX.toFixed(2)}) * ${AMP.toFixed(1)} + sin((grid.y + phase) * ${FY.toFixed(2)}) * ${AMP.toFixed(1)};
          p.y = w - p.z * ${SLOPE.toFixed(2)};
          c = mix(vec3(${BLUE.map(v => v.toFixed(6)).join(",")}), vec3(${PURPLE.map(v => v.toFixed(6)).join(",")}), clamp(0.5 + w / 140.0, 0.0, 1.0));
        }
        vec4 mv = modelViewMatrix * vec4(p, 1.0);
        gl_PointSize = size * (scale / -mv.z);
        gl_Position = projectionMatrix * mv; vColor = c; vFog = -mv.z;
      }`,
    fragmentShader: `uniform sampler2D map; uniform float fogNear, fogFar; uniform vec3 fogColor; varying vec3 vColor; varying float vFog;
      void main() {
        vec4 t = texture2D(map, vec2(gl_PointCoord.x, 1.0 - gl_PointCoord.y));
        gl_FragColor = linearToOutputTexel(vec4(vColor * t.rgb, t.a));
        gl_FragColor.rgb = mix(gl_FragColor.rgb, fogColor, smoothstep(fogNear, fogFar, vFog));
      }` });
  const pts = new THREE.Points(geo, mat); pts.frustumCulled = false; scene.add(pts);
  const BX = new Float32Array(count), BZ = new Float32Array(count);
  for (let j = 0; j < count; j++) { BX[j] = pos[j * 3]; BZ[j] = pos[j * 3 + 2]; }

  const ray = new THREE.Raycaster(), plane = new THREE.Plane(new THREE.Vector3(0, 1, SLOPE).normalize(), 0), hA = new THREE.Vector3(), hB = new THREE.Vector3();
  const PV = new THREE.Matrix4(), IPV = new THREE.Matrix4(), v4a = new THREE.Vector4(), v4b = new THREE.Vector4(), PN = new THREE.Vector3(0, 1, SLOPE).normalize();
  let vRx = 1, vRf = 1, vRn = 1, vOn = false, vx = 0, vz = 0, last = [0, 0, 0], ex = 0, ey = 0, erx = 1, ery = 1;
  let SPAN = 16, FUN = { R0: 1, sf: 0.57, cf: 0.82, HD: 1 }, staticDirty = true, lastPhase = NaN;
  const GD = new Float32Array(count), GT = new Float32Array(count), GL = new Float32Array(count);
  let DR = new Int32Array(0);                                         // the dots the drain owns (simulated on the CPU)
  const polar = (bx, bz, D, T, L, j) => { const dz = bz - vz, nx = (bx - vx) / vRx, nz = dz / (dz < 0 ? vRf : vRn), d = Math.max(1e-3, Math.hypot(nx, nz)); D[j] = d; T[j] = Math.atan2(nz, nx); L[j] = Math.log(d); };
  // A dot's screen position, to keep every dot out of the hole's outline (a world circle is a different oval on screen).
  const outside = (x, y, z) => { const e = PV.elements, w = e[3] * x + e[7] * y + e[11] * z + e[15];
    const sx = ((e[0] * x + e[4] * y + e[8] * z + e[12]) / w + 1) / 2 * innerWidth, sy = (1 - (e[1] * x + e[5] * y + e[9] * z + e[13]) / w) / 2 * innerHeight;
    return clamp01((Math.hypot((sx - ex) / erx, (sy - ey) / ery) - 1.0) / 0.14); };
  // A screen point → the field plane under it, pushed back along the camera ray (deeper = smaller and fogged).
  function onRay(sx, sy, push, P, j) {
    const nx = sx / innerWidth * 2 - 1, ny = -(sy / innerHeight) * 2 + 1;
    v4a.set(nx, ny, -1, 1).applyMatrix4(IPV); v4a.divideScalar(v4a.w); v4b.set(nx, ny, 1, 1).applyMatrix4(IPV); v4b.divideScalar(v4b.w);
    const dx = v4b.x - v4a.x, dy = v4b.y - v4a.y, dz = v4b.z - v4a.z, den = PN.x * dx + PN.y * dy + PN.z * dz;
    const t = den ? -(PN.x * v4a.x + PN.y * v4a.y + PN.z * v4a.z) / den : 0, cp = camera.position;
    P[j * 3] = cp.x + (v4a.x + dx * t - cp.x) * push; P[j * 3 + 1] = cp.y + (v4a.y + dy * t - cp.y) * push; P[j * 3 + 2] = cp.z + (v4a.z + dz * t - cp.z) * push;
  }
  // One dot, placed and coloured. d0/th0/ld0: its precomputed place relative to the vortex.
  function shade(P, C, j, bx, bz, fx, fy, d0, th0, ld0, phase, flowT, spin, bg, inBetween) {
    const wave = Math.sin((fx + phase) * FX) * AMP + Math.sin((fy + phase) * FY) * AMP;
    let m = clamp01(0.5 + wave / 140), fade = 1, foam = 0;
    if (!vOn || d0 >= R_EDGE) { P[j * 3] = bx; P[j * 3 + 1] = wave - bz * SLOPE; P[j * 3 + 2] = bz; if (inBetween) fade = 0; }   // beyond the drain: the hero's grid
    else {
      let X = d0 * d0 - FLOW_C * flowT, lrs = ld0;
      if (X < R_CORE * R_CORE) { X = R_CORE * R_CORE + ((X - R_CORE * R_CORE) % SPAN + SPAN) % SPAN; lrs = LOG_EDGE; fade *= clamp01((R_EDGE - Math.sqrt(X)) / 0.5); }  // re-entering: fade in
      const r = Math.sqrt(X), rd = squeeze(r);
      let a = th0 + SPIRAL_B * (lrs - 0.5 * Math.log(X)), trough = 0;
      const u = clamp01((rd - 1) / (INFL - 1)), w = (1 - u) * (1 - u);
      // The arms begin out here, made of the dots themselves: each dot is drawn toward the centreline of its nearest arm,
      // so the dots stream along the arms in tight lines while the troughs between them thin and darken.
      if (rd < R_ARM) { const pull = 0.5 * clamp01((R_ARM - rd) / 1.4);
        let psi = (a - spin + SPIRAL_B * Math.log(Math.max(rd, 0.2))) % TAU; if (psi < 0) psi += TAU;
        let b = Math.min(4, Math.floor(psi / SECTOR)), dl = psi - b * SECTOR - ARM_W[b] / 2;
        const nb = (b + 1) % 5, dn = psi - (b + 1) * SECTOR - ARM_W[nb] / 2;
        if (Math.abs(dn) < Math.abs(dl)) { b = nb; dl = dn; }
        a -= dl * pull; dl *= 1 - pull;
        const wd = ARM_W[b] * (rd < 1 ? 1 - (1 - rd) * 0.75 : 1), along = Math.abs(dl) / (wd / 2);
        const weight = ARM_L[b] * (0.8 + 0.2 * Math.sin(spin * 0.9 + b * 1.7)) * clamp01((R_ARM - rd) / 1.3);
        if (along < 1) foam = Math.cos(along * Math.PI / 2) * weight; else trough = Math.min(1, (along - 1) * 1.5) * clamp01((R_ARM - rd) / 1.3); }
      if (rd >= 1) {
        const NX = rd * Math.cos(a), NZ = rd * Math.sin(a), x = vx + NX * vRx, z = vz + NZ * (NZ < 0 ? vRf : vRn);
        // Deep flow: near the lip the far side curves down into the hole; the wave calms as the water is drawn in.
        const sink = Math.pow(w, 1.5), far = clamp01(0.5 - 0.6 * Math.sin(a)), y = wave * (1 - w) - z * SLOPE - 0.3 * vRx * sink * far;
        P[j * 3] = x; P[j * 3 + 1] = y; P[j * 3 + 2] = z;
        m = m + (1 - m) * w * 0.45; fade *= 1 - 0.25 * sink; if (rd < 1.7) fade *= outside(x, y, z);
      } else {
        // Inside: the dot follows the vortex's own funnel on screen, down the far wall, to the core.
        const f = Math.min(1, Math.pow((1 - rd) / 0.8, 1.3889)), sx = ex + rd * FUN.R0 * Math.cos(a), sy = ey + FUN.HD * Math.pow(f, 1.15) * FUN.cf + rd * FUN.R0 * FUN.sf * Math.sin(a);
        onRay(sx, sy, 1 + 1.6 * f, P, j);
        m = m + (1 - m) * (0.45 + 0.4 * f);
        fade *= (1 - 0.8 * f * f) * (Math.sin(a) > 0 ? clamp01(1 - 3 * f) : 1) * clamp01((rd - R_CORE) / 0.1);
      }
      m = m + (1 - m) * 0.6 * foam; fade *= 1 - 0.45 * trough;
    }
    for (let c = 0; c < 3; c++) { let v = BLUE[c] + (PURPLE[c] - BLUE[c]) * m; v += (1 - v) * 0.28 * foam; C[j * 3 + c] = bg[c] + (v - bg[c]) * fade; }
  }
  // The in-between dots: fractional steps along the grid's own rows and columns, wherever the drain reaches, so the
  // lines stay readable close to the camera. Finer on phones; coarser on modest devices.
  let fine = [], FD = null, FT = null, FL = null, fPos = null, fCol = null, fPts = null;
  function buildFine() {
    const phone = innerWidth < 600, n = TIER === "low" ? 2 : TIER === "mid" ? 3 : phone ? 4 : 3, st = 1 / n;
    fine = [];
    for (let i = 0; i <= (AX - 1) * n; i++) for (let k = 0; k <= (AY - 1) * n; k++) {
      if (i % n === 0 && k % n === 0) continue;
      const fx = i * st, fy = k * st, bx = fx * SEP - (AX * SEP) / 2, bz = fy * SEP - (AY * SEP) / 2, dz = bz - vz;
      if (Math.hypot((bx - vx) / vRx, dz / (dz < 0 ? vRf : vRn)) < R_EDGE) fine.push(bx, bz, fx, fy); }
    const nF = fine.length / 4; FD = new Float32Array(nF); FT = new Float32Array(nF); FL = new Float32Array(nF);
    for (let i = 0; i < nF; i++) polar(fine[i * 4], fine[i * 4 + 1], FD, FT, FL, i);
    fPos = new Float32Array(nF * 3); fCol = new Float32Array(nF * 3);
    if (fPts) { scene.remove(fPts); fPts.geometry.dispose(); }
    const g2 = new THREE.BufferGeometry(); g2.setAttribute("position", new THREE.BufferAttribute(fPos, 3)); g2.setAttribute("color", new THREE.BufferAttribute(fCol, 3));
    g2.setAttribute("grid", new THREE.BufferAttribute(new Float32Array(nF * 3), 3));                         // all on the CPU (they only exist in the drain)
    fPts = new THREE.Points(g2, mat); fPts.frustumCulled = false; scene.add(fPts);
  }
  // The vortex, located on the field: rays from its screen centre and rims onto the field's inclined plane.
  function setVortex(sx, sy, rpx, rpy, funnel) {
    ex = sx; ey = sy; erx = rpx; ery = rpy || rpx; FUN = funnel || FUN;
    const ndc = (x, y) => new THREE.Vector2(x / innerWidth * 2 - 1, -(y / innerHeight) * 2 + 1);
    camera.updateMatrixWorld();
    ray.setFromCamera(ndc(sx, sy), camera); if (!ray.ray.intersectPlane(plane, hA)) { vOn = false; return; }
    ray.setFromCamera(ndc(sx + rpx, sy), camera); if (!ray.ray.intersectPlane(plane, hB)) { vOn = false; return; }
    vx = hA.x; vz = hA.z; vRx = Math.max(1, Math.abs(hB.x - hA.x)); vOn = true;
    // A world circle comes out much flatter on screen than the hole, so the pull is shaped to the hole's real oval.
    ray.setFromCamera(ndc(sx, sy - ery), camera); vRf = ray.ray.intersectPlane(plane, hB) ? Math.max(1, Math.abs(hB.z - vz)) : vRx;
    ray.setFromCamera(ndc(sx, sy + ery), camera); vRn = ray.ray.intersectPlane(plane, hB) ? Math.max(1, Math.abs(hB.z - vz)) : vRx;
    SPAN = R_EDGE * R_EDGE - R_CORE * R_CORE;
    for (let j = 0; j < count; j++) polar(BX[j], BZ[j], GD, GT, GL, j);
    const own = []; for (let j = 0; j < count; j++) { const cpu = GD[j] < R_EDGE; grid[j * 3 + 2] = cpu ? 0 : 1; if (cpu) own.push(j); else { pos[j * 3] = BX[j]; pos[j * 3 + 2] = BZ[j]; } }
    DR = Int32Array.from(own); geo.attributes.grid.needsUpdate = true; geo.attributes.position.needsUpdate = true;
    buildFine(); staticDirty = true;
    draw(...last);
  }
  // phase: the wave. flowT: the drain's clock. spin: the vortex's turn. The grid beyond the drain is recomputed only
  // when the wave moved.
  function draw(phase, flowT = 0, spin = 0) {
    last = [phase, flowT, spin];
    camera.updateMatrixWorld(); PV.multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse); IPV.copy(PV).invert();
    const bg = BG; uni.phase.value = phase;
    if (vOn) { for (let n = 0, N = DR.length; n < N; n++) { const j = DR[n];
        shade(pos, col, j, BX[j], BZ[j], (j / AY) | 0, j % AY, GD[j], GT[j], GL[j], phase, flowT, spin, bg, false); }
      if (DR.length) { geo.attributes.position.needsUpdate = true; geo.attributes.color.needsUpdate = true; } }
    if (fPts) fPts.visible = Q < 2;
    if (fPts && Q < 2) { for (let i = 0, nF = FD.length; i < nF; i++) shade(fPos, fCol, i, fine[i * 4], fine[i * 4 + 1], fine[i * 4 + 2], fine[i * 4 + 3], FD[i], FT[i], FL[i], phase, flowT, spin, bg, true);
      fPts.geometry.attributes.position.needsUpdate = true; fPts.geometry.attributes.color.needsUpdate = true; }
    lastPhase = phase; staticDirty = false;
    renderer.render(scene, camera);
  }
  const sizeUni = () => { uni.size.value = 10 * renderer.getPixelRatio(); uni.scale.value = innerHeight * 0.5; };
  function resize() { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); sizeUni(); staticDirty = true; }
  function lowRes(on) { renderer.setPixelRatio(ratio(on)); renderer.setSize(innerWidth, innerHeight); sizeUni(); staticDirty = true; }
  // The road lies on this same surface: it is projected with this camera (PV) around this vortex.
  const geoOf = () => vOn ? { e: PV.elements, vx, vz, vRx, vRf, vRn } : null;
  // "#rrggbb": the colour the dots dissolve into (the page's background under the field).
  function setFade(hex) { const m = /^#?([0-9a-f]{6})$/i.exec(hex || ""); const v = m ? [0, 2, 4].map(i => parseInt(m[1].substr(i, 2), 16) / 255) : [0, 0, 0];
    uni.fogColor.value.set(v[0], v[1], v[2]); BG = v.map(c => c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)); draw(...last); }
  return { draw, setVortex, resize, lowRes, setFade, geo: geoOf, canvas: renderer.domElement, renderer };
}

// ══ Styles ═══════════════════════════════════════════════════════════════════════════════════════════════════════
// Stages live in the shadow root. The medals are light-DOM children (slotted into the medal stage), so the page's own
// code can find them by [data-node]; their styles go into the document once, scoped under vortex-map.
const SHADOW_CSS = `
/* No contain/transform/filter here: any of them would make the host the containing block of the fixed stages. */
:host { position:absolute; left:0; top:0; width:1px; pointer-events:none; display:block; }
:host([active="false"]) .vm { display:none; }
.vm { --n1:#00b5ff; --n2:#1c62ff; --n3:#3839ff; --n4:#5d22ff; --n5:#8911ff; --surface:#1f2226; --surface2:#2a2e34; --text:#eceded; --muted:#9aa0a6;
  --hair:rgba(255,255,255,0.08); --card-shadow:0 14px 34px rgba(0,0,0,0.5); --road-shadow:rgba(0,0,0,0.42); --road-edge:#121418; --road-top:#2f343d;
  --road-dash:rgba(255,255,255,0.10); --lbl-shadow:0 2px 8px rgba(0,0,0,0.8); color:var(--text); }
.stage { position:fixed; left:0; top:0; width:100vw; height:100vh; pointer-events:none; }
.bg { z-index:0; background:#0a0a0a; }                       /* overridden by the bg attribute */ .bg canvas { display:block; width:100% !important; height:100% !important; }
.back { z-index:1; } .road { z-index:2; overflow:visible; } .nodes { z-index:3; } .front { z-index:4; }
`;
const DOC_CSS = `
@property --a { syntax:"<angle>"; inherits:true; initial-value:0deg; }
vortex-map .vm-node { position:absolute; left:0; top:0; width:180px; display:flex; flex-direction:column; align-items:center; gap:8px; will-change:transform; pointer-events:none; }
vortex-map .vm-orb { pointer-events:auto; position:relative; width:62px; height:62px; flex:none; border-radius:50%; display:flex; align-items:center; justify-content:center; padding:0; border:4px solid; cursor:pointer;
  font-size:16px; font-weight:800; letter-spacing:-0.02em;
  box-shadow:0 7px 0 var(--lip), 0 16px 24px rgba(0,0,0,0.35), inset 0 -9px 14px rgba(0,0,0,0.3), inset 0 7px 12px rgba(255,255,255,0.16); transition:transform 160ms cubic-bezier(0.34,1.56,0.64,1); }
vortex-map .vm-orb:hover { transform:translateY(-2px); } vortex-map .vm-orb:active { transform:scale(0.95); }
vortex-map .vm-orb::before { content:""; position:absolute; left:16%; top:9%; width:46%; height:30%; border-radius:50%; background:radial-gradient(closest-side, rgba(255,255,255,0.5), rgba(255,255,255,0)); pointer-events:none; }
vortex-map .vm-node.big .vm-orb { width:86px; height:86px; font-size:20px; }
vortex-map .vm-halo { position:absolute; inset:-12px; border-radius:50%; border:2px solid var(--n3); pointer-events:none; animation:halo 2.4s ease-out infinite; }
vortex-map .vm-tick { position:absolute; right:-7px; bottom:-7px; width:24px; height:24px; border-radius:50%; border:2px solid #191b1e; display:flex; align-items:center; justify-content:center; }
vortex-map .vm-num { position:relative; }
vortex-map .vm-lbl, vortex-map .vm-chips { will-change:transform, opacity; }
vortex-map .vm-lbl { font-size:12.5px; font-weight:700; text-align:center; line-height:1.3; text-shadow:var(--lbl-shadow); white-space:nowrap; border-radius:8px; padding:1px 7px; transition:background-color 200ms ease; }
vortex-map .vm-node.big .vm-lbl { font-size:14px; }
vortex-map .vm-node.plate .vm-lbl { background:var(--surface); box-shadow:0 0 0 1px var(--hair); text-shadow:none; }
/* Far down the road a medal is too small for its number: it becomes a plain bead of its colour. */
vortex-map .vm-node.far .vm-num, vortex-map .vm-node.far .vm-tick, vortex-map .vm-node.far .vm-orb::before { visibility:hidden; }
vortex-map .vm-chips { display:flex; gap:4px; white-space:nowrap; }
vortex-map .vm-chip { font-size:12px; font-weight:700; padding:2px 7px; border-radius:6px; white-space:nowrap; }
vortex-map .vm-tag { background:rgba(129,177,255,0.14); color:var(--tint, #81b1ff); letter-spacing:0.05em; }
vortex-map .vm-cap { position:absolute; left:0; top:0; width:220px; text-align:center; will-change:transform, opacity; padding:9px 12px; border-radius:16px; background:var(--surface); border:1px solid var(--hair);
  font-size:12px; font-weight:800; letter-spacing:0.12em; text-transform:uppercase; box-shadow:var(--card-shadow); pointer-events:none; white-space:nowrap; }
/* The finish: a marathon arch (checkered banner, posts, tape), the cup on its podium, and the paper's pill. */
vortex-map .vm-fin { position:absolute; left:0; top:0; width:320px; height:250px; will-change:transform; pointer-events:none; transform-origin:50% 236px; }
vortex-map .fin-xp { position:absolute; left:50%; top:0; transform:translateX(-50%); display:flex; align-items:center; gap:10px; padding:7px 14px 7px 8px; border-radius:16px; background:var(--surface); border:1px solid var(--hair); box-shadow:var(--card-shadow); white-space:nowrap; }
vortex-map .fin-xp .bolt { width:32px; height:32px; border-radius:10px; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg, var(--n1), var(--n3) 55%, var(--n5)); }
vortex-map .fin-xp b { display:block; font-size:14px; } vortex-map .fin-xp small { display:block; font-size:12px; color:var(--muted); font-weight:600; }
vortex-map .fin-banner { position:absolute; left:34px; right:34px; top:62px; height:40px; display:flex; align-items:stretch; overflow:hidden; border-radius:12px; background:var(--surface); box-shadow:var(--card-shadow); }
vortex-map .fin-banner::before { content:""; position:absolute; inset:0; border-radius:inherit; padding:1.5px; pointer-events:none;
  background:conic-gradient(from var(--a), var(--n1), var(--n2), var(--n3), var(--n4), var(--n5), var(--n4), var(--n3), var(--n2), var(--n1));
  -webkit-mask:linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite:xor; mask-composite:exclude; }
vortex-map .fin-banner .chk { flex:none; width:40px; background:repeating-conic-gradient(var(--text) 0 25%, var(--surface) 0 50%) 0 0 / 10px 10px; opacity:0.9; }
vortex-map .fin-banner span { flex:1; display:flex; align-items:center; justify-content:center; font-size:15px; font-weight:800; letter-spacing:0.34em; padding-left:0.34em; }
vortex-map .fin-post { position:absolute; top:96px; width:14px; height:140px; border-radius:7px; border:1px solid var(--hair); background:linear-gradient(90deg, rgba(255,255,255,0.22), rgba(255,255,255,0.03) 60%), var(--surface2); }
vortex-map .fin-post.l { left:44px; } vortex-map .fin-post.r { right:44px; }
vortex-map .fin-cup { position:absolute; left:50%; top:112px; width:86px; height:104px; margin-left:-43px; }
vortex-map .fin-cup::before { content:""; position:absolute; left:-30px; right:-30px; top:-18px; height:110px; border-radius:50%; background:radial-gradient(closest-side, rgba(251,227,154,0.35), rgba(251,227,154,0)); }
vortex-map .fin-cup .shine { animation:vmcupshine 4.8s ease-in-out infinite 1s; }
@keyframes vmcupshine { 0%, 62% { transform:translateX(-70px); } 86%, 100% { transform:translateX(90px); } }
vortex-map .fin-tape { position:absolute; left:0; top:0; width:320px; height:250px; overflow:visible; }
vortex-map .fin-line { position:absolute; left:50%; top:230px; width:150px; height:12px; margin-left:-75px; border-radius:3px; background:repeating-conic-gradient(var(--text) 0 25%, var(--surface) 0 50%) 0 0 / 12px 12px; box-shadow:0 2px 8px rgba(0,0,0,0.25); }
/* The start card's border: the Nexera logo's colours, turning only while the road moves (its angle is set per frame). */
.vm-lux { --n1:#00b5ff; --n2:#1c62ff; --n3:#3839ff; --n4:#5d22ff; --n5:#8911ff; }
.vm-lux::before { content:""; position:absolute; inset:0; border-radius:inherit; padding:1.5px; pointer-events:none;
  background:conic-gradient(from var(--a), var(--n1), var(--n2), var(--n3), var(--n4), var(--n5), var(--n4), var(--n3), var(--n2), var(--n1));
  -webkit-mask:linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite:xor; mask-composite:exclude; }
/* The companion stands at the start card's left edge, on its top edge (the image's feet sit 3.4% above its bottom). */
.vm-standee { position:absolute; left:-6px; bottom:calc(100% - 4px); height:118px; width:auto; pointer-events:none; filter:drop-shadow(0 6px 8px rgba(0,0,0,0.35)); }
@media (max-width: 599px) { .vm-standee { height:96px; left:-4px; } }
@media (prefers-reduced-motion: reduce) { vortex-map *, vortex-map *::before { animation:none !important; transition:none !important; } }
`;
const CUP = '<svg viewBox="0 0 86 104" width="86" height="104" aria-hidden="true"><defs><linearGradient id="vmGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbe39a"/><stop offset="0.45" stop-color="#dca834"/><stop offset="1" stop-color="#8a6414"/></linearGradient><clipPath id="vmCup"><path d="M21 8 H65 V32 C65 49 55 60 43 60 C31 60 21 49 21 32 Z"/></clipPath></defs>'
  + '<path d="M21 14 H11 C6 14 5 33 21 39" fill="none" stroke="url(#vmGold)" stroke-width="5" stroke-linecap="round"/><path d="M65 14 H75 C80 14 81 33 65 39" fill="none" stroke="url(#vmGold)" stroke-width="5" stroke-linecap="round"/>'
  + '<path d="M21 8 H65 V32 C65 49 55 60 43 60 C31 60 21 49 21 32 Z" fill="url(#vmGold)"/><g clip-path="url(#vmCup)"><rect class="shine" x="10" y="0" width="14" height="70" fill="rgba(255,255,255,0.55)" transform="skewX(-18)"/></g>'
  + '<path d="M43 20 l3.2 6.6 7.2 1 -5.2 5 1.3 7.2 -6.5 -3.4 -6.5 3.4 1.3 -7.2 -5.2 -5 7.2 -1z" fill="rgba(255,255,255,0.85)"/><rect x="38" y="59" width="10" height="12" fill="#b8871f"/><rect x="27" y="70" width="32" height="8" rx="3" fill="#8a6414"/>'
  + '<rect x="13" y="80" width="60" height="20" rx="5" fill="var(--surface2)" stroke="var(--hair)"/><rect x="13" y="80" width="60" height="4" rx="2" fill="rgba(255,255,255,0.14)"/></svg>';
const TAPE = '<svg class="fin-tape" viewBox="0 0 320 250" aria-hidden="true"><defs><linearGradient id="vmTape" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#00b5ff"/><stop offset="0.5" stop-color="#3839ff"/><stop offset="1" stop-color="#8911ff"/></linearGradient></defs><path d="M58 214 Q160 232 262 214" fill="none" stroke="url(#vmTape)" stroke-width="6" stroke-linecap="round"/><path d="M58 212.5 Q160 230 262 212.5" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="1.2" stroke-linecap="round"/></svg>';
const TICK = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#191b1e" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
// The page's runtime renders its template once with the raw {{ bindings }} before it binds them: not an error.
const json = (s, d) => { if (!s || s.charAt(0) === "{" && s.charAt(1) === "{") return d; try { return JSON.parse(s); } catch (e) { console.error("vortex-map: bad JSON attribute", e); return d; } };

// ══ The road model ═══════════════════════════════════════════════════════════════════════════════════════════════
const ELEV = 35;                  // the vortex seen from 35° above
const LIP_S = 0.62;               // a medal's size by the time it reaches the vortex's centre
const FIELD_FAR = -4500, Z_FIN = -3300;   // the field's far edge; the finish's depth at the start (far back, still in the haze)
const waveH = (x, z, ph) => Math.sin(((x + AX * SEP / 2) / SEP + ph) * FX) * AMP + Math.sin(((z + AY * SEP / 2) / SEP + ph) * FY) * AMP;

class VortexMap extends HTMLElement {
  static get observedAttributes() { return ["geom", "paint", "finish", "next", "lit", "anchor", "hdr", "active", "road", "bg", "fade"]; }
  // bg: the CSS background painted under the field (the page's own); fade: the "#rrggbb" its dots dissolve into.
  _colours() { const bg = this.getAttribute("bg"), fade = this.getAttribute("fade"), ok = v => v && !(v.charAt(0) === "{" && v.charAt(1) === "{");
    this._r.bg.style.background = ok(bg) ? bg : ""; if (FIELD) FIELD.setFade(ok(fade) ? fade : "#000000"); }
  connectedCallback() {
    if (!document.getElementById("vortex-map-css")) { const st = document.createElement("style"); st.id = "vortex-map-css"; st.textContent = DOC_CSS; document.head.appendChild(st); }
    if (!this.shadowRoot) {
      const root = this.attachShadow({ mode: "open" });
      root.innerHTML = '<style>' + SHADOW_CSS + '</style><div class="col"></div><div class="vm">'
        + '<div class="stage bg" aria-hidden="true"></div><canvas class="stage back" aria-hidden="true"></canvas>'
        + '<canvas class="stage road" aria-hidden="true"></canvas>'
        + '<div class="stage nodes"><slot></slot></div><canvas class="stage front" aria-hidden="true"></canvas></div>';
      const $ = s => root.querySelector(s);
      this._r = { col: $(".col"), vm: $(".vm"), bg: $(".bg"), back: $(".back"), road: $(".road") };
      this._xb = this._r.back.getContext("2d"); this._xr = this._r.road.getContext("2d");
      this._S = { SY: 0, spin: 0, drift: 0, boost: 0, poke: 0, bgPhase: null, bgScroll: null, roadPhase: null, lastY: -1, last: performance.now(), frame: 0,
        roadDirty: true, vortexSet: false, G: null, LUT: [], y1: 0, finY: 0, total: 0, els: [], RG: null, VX: null, dpr: 1, cTop: 0, cH: 0, where: "",
        borderA: null, litNow: null, litFrom: 0, litTo: 0, litT0: 0, geomKey: "", trackTop: 0 };
      this._gov = { ema: 16.7, slow: 0, calm: 4000 };
      this._tick = this._tick.bind(this);
    }
    if (!FIELD) FIELD = makeField();
    this._r.bg.appendChild(FIELD.canvas);                                                    // the page's one field, re-attached
    this._colours();
    this._S.vortexSet = false; this._S.RG = null;
    // Per-visit listeners, removed again on disconnect.
    this._onPoke = () => { this._S.poke = Math.min(this._S.poke + 0.03, 0.2); };
    this._onResize = () => { this._S.trackTop = 0; FIELD.resize(); this._build(true); };
    this._onScrollR = () => { if (this._running) requestAnimationFrame(t => this._frame(t)); };
    ["pointermove", "pointerdown", "touchmove", "keydown", "wheel"].forEach(t => addEventListener(t, this._onPoke, { passive: true }));
    addEventListener("resize", this._onResize);
    if (reduced) addEventListener("scroll", this._onScrollR, { passive: true });
    this._build(true); this._start();
  }
  disconnectedCallback() {
    this._stop();
    ["pointermove", "pointerdown", "touchmove", "keydown", "wheel"].forEach(t => removeEventListener(t, this._onPoke));
    removeEventListener("resize", this._onResize); removeEventListener("scroll", this._onScrollR);
  }
  attributeChangedCallback(name, a, b) {
    if (!this._S || a === b) return;
    if (name === "active") { b === "false" ? this._stop() : this._start(); return; }
    if (name === "bg" || name === "fade") { this._colours(); return; }
    if (name === "lit") { const S = this._S, to = clamp(+b || 0, 0, 1); S.litFrom = S.litNow == null ? to : S.litNow; S.litTo = to; S.litT0 = performance.now(); if (S.litNow == null) S.litNow = to; S.roadDirty = true; return; }
    this._build(false);
  }
  get _active() { return this.getAttribute("active") !== "false"; }
  get ready() { return !!(this._S && this._S.G && this._S.els.length); }
  get where() { return this._S ? this._S.where : ""; }
  _start() { if (this._running || !this._active || !this._S || !this.isConnected) return; this._running = true; this._S.last = performance.now(); this._S.lastY = -1; this._S.roadDirty = true; requestAnimationFrame(this._tick); }
  _stop() { this._running = false; }

  // ── Geometry: the page's road box gives the origin; the vortex sits over the start card ──
  _roadBox() { if (!this._road || !this._road.isConnected) this._road = document.querySelector(this.getAttribute("road") || "[data-road]"); return this._road; }
  _metrics() {
    const S = this._S, phone = innerWidth < 600, sf = Math.sin(ELEV * Math.PI / 180), cf = Math.cos(ELEV * Math.PI / 180);
    const R0 = Math.min(phone ? 190 : innerHeight < 700 ? 240 : 270, innerWidth / 2 - 4), HD = R0 * 0.38;      // the funnel's mouth and depth
    // The start card's top, measured while it is up (it steps aside for the mission card; the vortex must not jump).
    const a = this.getAttribute("anchor"), el = a && document.querySelector(a), r = el && el.getBoundingClientRect();
    if (r && r.height) S.trackTop = r.top; if (!S.trackTop) S.trackTop = innerHeight - 84;
    const cy = S.trackTop - 16 - HD * cf;                                                            // the core's light sits 16px above the card
    const box = this._roadBox(), br = box ? box.getBoundingClientRect() : { top: 0, left: 0 };
    S.G = { phone, sf, cf, R0, HD, cx: innerWidth / 2, cy, throatY: cy + HD * cf, RW: phone ? 18 : 22, BEND: phone ? 150 : 180, ZS: 240, trackTop: S.trackTop,
      top: br.top + scrollY, left: br.left, hdr: +this.getAttribute("hdr") || 64 };
  }
  _build(force) {
    const S = this._S; this._metrics(); const G = S.G;
    const geom = json(this.getAttribute("geom"), null), paint = json(this.getAttribute("paint"), []), F = json(this.getAttribute("finish"), {});
    this._next = +this.getAttribute("next"); if (!(this._next >= 0)) this._next = -1;
    if (!geom || !geom.nodes || !geom.nodes.length) { this._r.col.style.height = "0px"; this.replaceChildren(); S.els = []; return; }
    const key = JSON.stringify(geom) + "|" + innerWidth + "x" + innerHeight;
    if (force || key !== S.geomKey || !S.els.length) { S.geomKey = key; this._layout(geom, F); }
    this._paint(paint, F);
  }
  // The road through every mission (bottom = the first, on the vortex) up to the finish, and one element per stop.
  _layout(geom, F) {
    const S = this._S, G = S.G, nodes = geom.nodes.slice().sort((a, b) => b.y - a.y), fin = geom.fin || { x: nodes[0].x, y: nodes[nodes.length - 1].y - 170 };
    S.y1 = nodes[0].y; S.finY = fin.y;
    const pts = nodes.map(n => ({ x: n.x, y: n.y })).concat([{ x: fin.x, y: fin.y }]);
    const LUT = [{ x: pts[0].x, y: pts[0].y, l: 0 }]; let l = 0;
    for (let k = 1; k < pts.length; k++) { const a = pts[k - 1], b = pts[k], my = (a.y + b.y) / 2;
      for (let s = 1; s <= 60; s++) { const t = s / 60, u = 1 - t;
        const px = u * u * u * a.x + 3 * u * u * t * a.x + 3 * u * t * t * b.x + t * t * t * b.x, py = u * u * u * a.y + 3 * u * u * t * my + 3 * u * t * t * my + t * t * t * b.y;
        const p = LUT[LUT.length - 1]; l += Math.hypot(px - p.x, py - p.y); LUT.push({ x: px, y: py, l }); } }
    S.LUT = LUT; S.total = l;
    // The column: the page can always scroll far enough to bring the first mission down onto the vortex.
    this._r.col.style.height = Math.ceil(G.top + S.y1 - G.cy + innerHeight) + "px";
    S.els.forEach(e => e.remove()); S.els = [];
    const add = (e, ry, w, ay) => { e._ry = ry; e._w = w; e._ay = ay; e.style.transformOrigin = (w / 2) + "px " + ay + "px"; e.style.zIndex = String(Math.round(ry / 10)); this.appendChild(e); S.els.push(e); return e; };
    const fe = document.createElement("div"); fe.className = "vm-fin"; fe.setAttribute("data-finishbadge", "true"); fe.setAttribute("role", "img");
    fe.innerHTML = '<div class="fin-xp"><span class="bolt"><svg width="16" height="16" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg></span><span><b class="fin-t"></b><small class="fin-s"></small></span></div>'
      + '<div class="fin-banner"><i class="chk"></i><span>FINISH</span><i class="chk"></i></div><i class="fin-post l"></i><i class="fin-post r"></i><div class="fin-cup">' + CUP + '</div>' + TAPE + '<i class="fin-line"></i>';
    add(fe, fin.y, 320, 236)._fin = true; fe._txt = [];
    (geom.caps || []).forEach(c => { const e = document.createElement("div"); e.className = "vm-cap"; e.setAttribute("aria-hidden", "true"); e.textContent = c.label; add(e, c.y, 220, 18)._cap = true; });
    geom.nodes.forEach(n => { const e = document.createElement("div"); e.className = "vm-node";
      e.innerHTML = '<button class="vm-orb" data-node="' + n.i + '" data-orb="true" aria-haspopup="dialog"><span class="vm-num"></span></button><div class="vm-lbl"></div><div class="vm-chips"></div>';
      e.firstChild.onclick = () => dispatchEvent(new CustomEvent("vortex-open", { detail: { index: n.i } }));
      add(e, n.y, 180, 31)._i = n.i; e._txt = [e.children[1], e.children[2]]; });
    this._sizeCanvas(); S.RG = null; S.roadDirty = true; S.vortexSet = false;
  }
  // Each medal as the page paints it (status colours, label, chips, tick, halo, the celebration's stamp), in place.
  _paint(paint, F) {
    const S = this._S, byI = {}; paint.forEach(p => { byI[p.i] = p; });
    S.els.forEach(e => {
      if (e._fin) { e.querySelector(".fin-t").textContent = F.title || ""; e.querySelector(".fin-s").textContent = F.sub || ""; e.setAttribute("aria-label", F.aria || "Finish line"); return; }
      const p = e._i != null && byI[e._i]; if (!p) return;
      const sig = JSON.stringify(p); if (sig === e._sig) return; e._sig = sig;
      const b = e.firstChild, big = !!p.big; e.classList.toggle("big", big); e.style.zIndex = String(Math.round(e._ry / 10) + (big ? 100000 : 0)); e._ay = big ? 43 : 31; e.style.transformOrigin = "90px " + e._ay + "px";
      b.setAttribute("aria-label", p.aria || ""); b.style.cssText = "--lip:" + p.lip + "; background:" + p.fill + "; border-color:" + p.ring + "; color:" + p.num + (p.anim && p.anim !== "none" ? "; animation:" + p.anim : "");
      b.innerHTML = (p.halo ? '<span class="vm-halo" aria-hidden="true"></span>' : "") + '<span class="vm-num" style="text-shadow:' + (p.num === "#ffffff" ? "0 1px 2px rgba(0,0,0,0.55)" : "0 1px 0 rgba(255,255,255,0.35)") + '">' + esc(p.id) + '</span>'
        + (p.badge ? '<span class="vm-tick" aria-hidden="true" style="background:radial-gradient(circle at 35% 30%, #ffffff55, transparent 55%), ' + p.ring + '; box-shadow:0 3px 0 ' + p.lip + '">' + TICK + '</span>' : "");
      e.children[1].textContent = p.title || ""; e.children[1].style.color = p.titleColor || "";
      e.children[2].innerHTML = '<span class="vm-chip" style="background:' + p.chipBg + '; color:' + p.chipColor + '">' + esc(p.chip) + '</span>' + (p.tags || []).map(t => '<span class="vm-chip vm-tag">' + esc(t) + '</span>').join("");
      e._lw = null; });                                                                             // the label's measured size is stale
    S.roadDirty = true;
  }
  _sizeCanvas() {
    const S = this._S, G = S.G, c = this._r.back;
    S.dpr = Q >= 2 ? 1 : Math.min(TIER === "high" ? 1.5 : TIER === "mid" ? 1.25 : 1, devicePixelRatio || 1); S.VX = null;
    S.cTop = G.cy - G.R0 * 1.85 * G.sf - 24; S.cH = Math.max(G.throatY + G.R0 * 0.6 + 30, G.cy + G.R0 * 1.85 * G.sf) - S.cTop;   // room for the arms' tips
    c.width = Math.round(innerWidth * S.dpr); c.height = Math.round(S.cH * S.dpr); c.style.width = innerWidth + "px"; c.style.height = S.cH + "px"; c.style.top = S.cTop + "px";
    const rc = this._r.road; rc.width = Math.round(innerWidth * S.dpr); rc.height = Math.round(innerHeight * S.dpr);
  }
  _at(ry) { const LUT = this._S.LUT; ry = clamp(ry, LUT[LUT.length - 1].y, LUT[0].y); let lo = 0, hi = LUT.length - 1;
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (LUT[m].y > ry) lo = m; else hi = m; }
    const a = LUT[lo], b = LUT[hi], k = a.y === b.y ? 0 : (ry - a.y) / (b.y - a.y), o = this._atO || (this._atO = { x: 0, l: 0 });
    o.x = a.x + (b.x - a.x) * k; o.l = a.l + (b.l - a.l) * k; return o; }                    // a scratch result: read it before the next call
  // The road lies on the wave: each point is put on the dotted surface in 3D (depth from its distance ahead of the
  // vortex's lip, across from the road's own curve, height from the hero's wave, calmed near the hole as the field is)
  // and projected with the field's own camera. At the lip one pixel of scroll moves the road one pixel on screen.
  _roadGeo() {
    const S = this._S, G = S.G, g = FIELD && FIELD.geo(); if (!g) return null;
    const key = innerWidth + "x" + innerHeight + ":" + G.cx + "," + G.cy + ":" + S.y1 + "," + S.finY;
    if (S.RG && S.RG.key === key && S.RG.g.vz === g.vz) return S.RG;
    const pr = (x, y, z, o) => { const e = g.e, w = e[3] * x + e[7] * y + e[11] * z + e[15]; o = o || [0, 0];
      o[0] = ((e[0] * x + e[4] * y + e[8] * z + e[12]) / w + 1) / 2 * innerWidth; o[1] = (1 - (e[1] * x + e[5] * y + e[9] * z + e[13]) / w) / 2 * innerHeight; return o; };
    const a = pr(g.vx, -g.vz * SLOPE, g.vz), b = pr(g.vx, -(g.vz - 10) * SLOPE, g.vz - 10), c = pr(g.vx + 10, -g.vz * SLOPE, g.vz);
    const RG = { g, pr, key, s1: [0, 0], s2: [0, 0], s3: [0, 0], s4: [0, 0], KZ: 10 / Math.max(0.01, Math.abs(a[1] - b[1])), KX: 10 / Math.max(0.01, Math.abs(c[0] - a[0])) };
    // Depth = KZ·D0·ln(1 + d/D0): 1:1 at the lip; D0 solved (bisection) so the whole road spans the vortex → Z_FIN.
    const dmax = Math.max(1, S.y1 - S.finY), want = g.vz - Z_FIN, span = D0 => RG.KZ * D0 * Math.log(1 + dmax / D0);
    if (span(1e7) <= want) RG.D0 = 1e7; else { let lo = 20, hi = 1e7; for (let i = 0; i < 60; i++) { const m = Math.sqrt(lo * hi); if (span(m) < want) lo = m; else hi = m; } RG.D0 = Math.sqrt(lo * hi); }
    S.roadDirty = true; S.RG = RG; return RG;
  }
  _place(ry, o) {
    o = o || {}; const S = this._S, G = S.G, p0 = this._at(ry), sx = G.left + p0.x, l0 = p0.l, ryLip = G.cy - G.top + S.SY, zBend = ryLip - G.BEND;
    if (ry <= ryLip) { const k = E(clamp((ry - zBend) / G.BEND, 0, 1)), rimTop = G.cy - G.R0 * G.sf, rg = this._roadGeo();
      let x, y, persp = 1, fog = 1;
      if (!rg) { x = sx + (G.cx - sx) * k; y = G.top + ry - S.SY; }                                   // before the field is ready: the flat map
      else { const d = ryLip - ry, g = rg.g, wz = g.vz - rg.KZ * rg.D0 * Math.log(1 + d / rg.D0);
        // The bends narrow with distance at ~65% of true perspective: near medals swing wide, the far road still winds.
        const C = rg.pr(g.vx, -wz * SLOPE, wz, rg.s1), C2 = rg.pr(g.vx + 10, -wz * SLOPE, wz, rg.s2), perspC = Math.hypot(C2[0] - C[0], C2[1] - C[1]) / 10 * rg.KX;
        const wx = g.vx + (sx - G.cx) * (1 - k) * rg.KX * Math.pow(Math.max(perspC, 0.05), -0.35);
        const dn = (g.vz - wz) / g.vRf, calm = dn <= 1 ? 0 : 1 - Math.pow(1 - clamp((dn - 1) / 2, 0, 1), 2);   // the wave calms near the hole
        const wy = waveH(wx, wz, S.bgPhase || 0) * calm - wz * SLOPE + 6 * calm, P = rg.pr(wx, wy, wz, rg.s3), P2 = rg.pr(wx + 10, wy, wz, rg.s4);
        x = P[0]; y = P[1]; persp = Math.hypot(P2[0] - P[0], P2[1] - P[1]) / 10 * rg.KX;
        const dist = Math.hypot(wx, wy - 355, wz - 1220); fog = clamp((wz - FIELD_FAR) / 1500, 0, 1) * (1 - 0.6 * clamp((dist - 3200) / 7800, 0, 1)); }
      const u = clamp((y - rimTop) / (G.cy - rimTop), 0, 1), s = 1 - (1 - LIP_S) * (1 - (1 - u) * (1 - u));   // shrinks at once on contact with the rim
      // Medals shrink a little slower than true perspective (far ones stay legible); the road keeps its true width (rs).
      const pp = Math.pow(persp, 0.75); o.x = x; o.y = y; o.s = s * pp; o.rs = s * persp; o.persp = pp; o.fog = fog; o.p = 0; o.w = 1; o.l = l0; return o; }
    // Past the lip: down the vortex's axis into the core, shrinking, twisting and orbiting.
    const p = clamp((ry - ryLip) / G.ZS, 0, 1), depth = G.throatY - G.cy, kx = G.ZS / depth;
    const F = 1 - Math.pow(1 - p, kx), rho = G.R0 * 0.16 * Math.sin(Math.PI * p), th = p * 2.6 * Math.PI + S.spin;
    o.x = G.cx + rho * Math.cos(th); o.y = G.cy + depth * F + rho * Math.sin(th) * G.sf; o.s = LIP_S * (1 - 0.88 * E(p)); o.rs = null; o.persp = 1; o.fog = 1; o.p = p;
    o.w = 0.42 + 0.58 * Math.abs(Math.cos(p * 1.6 * Math.PI)); o.l = l0; return o;
  }
  _band(x, P, extra, dy, from) {
    const i0 = from || 0, n = P.length; x.beginPath(); if (n - i0 < 2) return false; const G = this._S.G;
    const R = this._bandR && this._bandR.length >= n * 2 ? this._bandR : (this._bandR = new Float64Array(n * 2 + 256));
    for (let i = i0; i < n; i++) { const q = P[i], a = P[Math.max(i0, i - 1)], c = P[Math.min(n - 1, i + 1)], tx = c.x - a.x, ty = c.y - a.y, tl = Math.hypot(tx, ty) || 1;
      const qs = q.rs != null ? q.rs : q.s, nx = -ty / tl, ny = tx / tl, hw = (G.RW + extra) * qs * q.w / 2, yy = q.y + dy * qs;
      i > i0 ? x.lineTo(q.x - nx * hw, yy - ny * hw) : x.moveTo(q.x - nx * hw, yy - ny * hw); R[i * 2] = q.x + nx * hw; R[i * 2 + 1] = yy + ny * hw; }
    for (let i = n - 1; i >= i0; i--) x.lineTo(R[i * 2], R[i * 2 + 1]);
    x.closePath(); return true;
  }
  _drawRoad() {
    const S = this._S, G = S.G, r = this._r; if (!S.els.length) return;
    const ryLip = G.cy - G.top + S.SY, flatEnd = Math.min(S.y1, ryLip), P = S.P || (S.P = []), far = S.far || (S.far = []); let top = flatEnd;
    P.length = 0; far.length = 0; const pool = S.pool || (S.pool = []); let pi = 0; const take = ry => this._place(ry, pool[pi] || (pool[pi] = {}), pi++);
    // From the lip out toward the horizon; steps grow with distance, and stop at the fog.
    for (let d = 0, ry = flatEnd; ry >= S.finY; ) { const q = take(ry); if (q.fog <= 0) break; far.push(q); top = ry; d += 5 + d * 0.018; ry = flatEnd - d; }
    if (top > S.finY && far.length && far[far.length - 1].fog > 0) { const q = take(S.finY); if (q.fog > 0) { far.push(q); top = S.finY; } }
    for (let i = far.length - 1; i >= 0; i--) P.push(far[i]);
    if (flatEnd === ryLip) { const end = Math.min(S.y1, ryLip + G.ZS); for (let k = 0; k <= 40; k++) { const ry = ryLip + (end - ryLip) * k / 40; if (ry <= S.y1) P.push(take(ry)); } }
    else P.push(take(S.y1));
    // A contact shadow (the road lies on the surface), a thin edge, the top, the lit stretch (the score) and the dashes;
    // then the far end fades into the haze (the field's own fog), as one gradient cut-out.
    const x = this._xr, dpr = S.dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0); x.globalCompositeOperation = "source-over"; x.clearRect(0, 0, innerWidth, innerHeight);
    if (this._band(x, P, 8, 3)) { x.fillStyle = "rgba(0,0,0,0.42)"; x.fill(); }
    if (this._band(x, P, 5, 2)) { x.fillStyle = "#121418"; x.fill(); }
    if (this._band(x, P, 0, 0)) { x.fillStyle = "#2f343d"; x.fill(); }
    const litLen = S.total * (S.litNow || 0); let li = P.length; if (litLen > 1) while (li > 0 && P[li - 1].l <= litLen) li--;
    if (this._band(x, P, 0, 0, li)) { const y0 = P[P.length - 1].y, g = x.createLinearGradient(0, y0, 0, Math.min(P[li].y, y0 - 1));
      g.addColorStop(0, "#00b5ff"); g.addColorStop(0.5, "#3839ff"); g.addColorStop(1, "#8911ff"); x.fillStyle = g; x.fill(); }
    if (P.length > 1) { x.beginPath(); x.moveTo(P[0].x, P[0].y); for (let i = 1; i < P.length; i++) x.lineTo(P[i].x, P[i].y);
      x.setLineDash([3, 12]); x.lineDashOffset = S.total - this._at(top).l; x.strokeStyle = "rgba(255,255,255,0.10)"; x.lineWidth = 2; x.stroke(); x.setLineDash([]); }
    const e0 = P[0]; if (top <= S.finY + 4 && e0) { x.beginPath(); x.arc(e0.x, e0.y, G.RW * (e0.rs != null ? e0.rs : e0.s) / 2, 0, TAU); x.fillStyle = "#2f343d"; x.fill(); }
    const qf = P.find(q => q.fog >= 0.999) || P[P.length - 1];
    if (P.length && P[0].fog < 0.999) { const g = x.createLinearGradient(0, P[0].y, 0, qf ? Math.max(qf.y, P[0].y + 1) : P[0].y + 1);
      g.addColorStop(0, "rgba(0,0,0," + P[0].fog.toFixed(3) + ")"); g.addColorStop(1, "rgba(0,0,0,1)");
      x.globalCompositeOperation = "destination-in"; x.fillStyle = g; x.fillRect(0, 0, innerWidth, innerHeight); x.globalCompositeOperation = "source-over"; }
    // Medals, labels and plaques ride the same model.
    S.els.forEach(e => {
      const q = this._place(e._ry, e._qo || (e._qo = {}));
      if (q.y < -160 || q.y > innerHeight + 160 || q.p >= 1 || q.fog <= 0.01) { if (e.style.visibility !== "hidden") e.style.visibility = "hidden"; e._q = null;
        if (e._i != null) e.firstChild.tabIndex = -1; return; }
      e.style.visibility = "";
      let tf = "translate3d(" + (q.x - e._w / 2).toFixed(1) + "px," + (q.y - e._ay).toFixed(1) + "px,0)";
      if (e._fin) tf += " scale(" + Math.max(q.s, 0.42).toFixed(3) + ")";                          // the finish stays a landmark, even far away
      else if (e._cap) { /* plaques keep their size (their text is the whole plaque); they fade instead */ }
      else if (q.p === 0 && q.s < 0.999) tf += " scale(" + q.s.toFixed(3) + ")";
      else if (q.p > 0) tf += reduced ? " scale(" + q.s.toFixed(3) + ")" : " perspective(600px) rotateX(" + (48 * E(q.p)).toFixed(1) + "deg) rotateZ(" + (300 * E(q.p)).toFixed(1) + "deg) scale(" + q.s.toFixed(3) + ")";
      e.style.transform = tf;
      const readable = e._i === this._next && q.fog > 0.4 ? 1 : clamp((q.persp - 0.34) / 0.1, 0, 1);   // the next mission always; the collision pass thins the rest
      e._q = q;
      if (e._i != null) { const far = q.p === 0 && q.s < 0.36; if (far !== !!e._far) { e._far = far; e.classList.toggle("far", far); } }
      if (e._fin) { e.style.opacity = (q.fog * (q.p > 0.86 ? 1 - (q.p - 0.86) / 0.14 : 1)).toFixed(3); }
      else if (e._cap) { const u = clamp(((e._ry - (ryLip - G.BEND)) / G.BEND - 0.35) / 0.65, 0, 1), near = clamp((q.persp - 0.55) / 0.12, 0, 1);   // plaques: the near road only
        e.style.opacity = q.p > 0 ? "0" : (q.fog * near * (1 - E(u))).toFixed(3); }
      else { e.style.opacity = (q.fog * (q.p > 0.86 ? 1 - (q.p - 0.86) / 0.14 : 1)).toFixed(3); const to = ((1 - clamp(q.p / 0.3, 0, 1)) * readable).toFixed(3);
        // Labels stay at full size however far the medal is (compensating its scale), so text never drops below 12px.
        const inv = q.p === 0 ? (1 / Math.max(q.persp, 0.3)).toFixed(3) : "1";
        const tsf = inv === "1" ? "" : "scale(" + inv + ")";
        e._txt.forEach(t => { t._o = to; t._t = tsf; });                                           // wanted values; written once, below
        const ti = q.p > 0.3 || q.fog < 0.3 ? -1 : 0; if (e._ti !== ti) { e._ti = ti; e.firstChild.tabIndex = ti; }   // a medal you can see is one you can reach by keyboard
        // A medal shrinking into the vortex loses its text rather than dropping below the 12px floor (gone by 72%).
        const rimS = q.s / Math.max(q.persp, 0.01);
        if (rimS < 0.999) { const keep = clamp((rimS - 0.72) / 0.22, 0, 1); e._txt.forEach(t => t._o = Math.min(+t._o, keep).toFixed(3)); }
        // Text near the start card fades out instead of being cut off by it (the card's top is a fixed line: no layout read).
        if (q.p === 0) { const bottom = q.y + (e._ay + 60) * q.s, under = clamp((bottom - (G.trackTop - 6)) / 14, 0, 1); if (under > 0) e._txt.forEach(t => t._o = Math.min(+t._o, 1 - under).toFixed(3)); }
        const over = q.p === 0 && q.y + e._ay + 60 > G.cy - G.R0 * G.sf; if (over !== !!e._plate) { e._plate = over; e.classList.toggle("plate", over); } }
    });
    this._labels();
    // Flush the labels: only what changed reaches the DOM (a hidden label's moves are never written).
    S.els.forEach(e => { if (!e._txt || !e._txt.length) return; e._txt.forEach(t => {
      if (t._o == null) return; const o = +t._o > 0.004 ? t._o : "0";
      if (t._wo !== o) { t._wo = o; t.style.opacity = o; }
      if (o !== "0" && t._wt !== t._t) { t._wt = t._t; t.style.transform = t._t; if (!t._orig) { t._orig = 1; t.style.transformOrigin = "50% 0"; } } }); });
    const nx = this._next >= 0 && S.els.find(e => e._i === this._next), nq = nx && nx._qo && nx._q ? nx._qo : nx && this._place(nx._ry, this._dirO || (this._dirO = {}));
    // On screen = drawn clear of the bars, the card and the haze (not "near": a long road puts the next mission far back).
    const where = !nq ? "here" : nq.p > 0 || nq.y > G.trackTop - 40 ? "down" : nq.y < G.hdr + 20 || nq.fog < 0.5 || nq.s < 0.3 ? "up" : "here";
    if (S.where !== where) { S.where = where; dispatchEvent(new CustomEvent("vortex-dir", { detail: { where } })); }
  }
  // Labels on the runway: placed nearest-first (the next mission first) below the medal, else beside it on the outside
  // of the bend, else the inside; a label shows only where it clears every label already placed and every medal.
  _labels() {
    const S = this._S, G = S.G;
    const vis = S.els.filter(e => e._i != null && e._q && e.style.visibility !== "hidden" && e._q.p === 0);
    const orbs = vis.map(e => { const r = e._ay * e._q.s; return { e, l: e._q.x - r, r: e._q.x + r, t: e._q.y - r, b: e._q.y + r }; });
    const hit = (a, b) => a.l < b.r && a.r > b.l && a.t < b.b && a.b > b.t, placed = [];
    const ov = (a, b) => Math.max(0, Math.min(a.r, b.r) - Math.max(a.l, b.l)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.t, b.t));
    const cost = (e, b) => (b.l < 4 || b.r > innerWidth - 4 ? 1e6 : 0) + placed.reduce((c, p) => c + ov(p, b) * 10, 0) + orbs.reduce((c, o) => c + (o.e !== e ? ov(o, b) : 0), 0);
    vis.filter(e => +e._txt[0]._o > 0.05).sort((a, b) => (b._i === this._next) - (a._i === this._next) || b._q.persp - a._q.persp).forEach(e => {
      const q = e._q, r = e._ay * q.s, top = q.y + r + 4, out = q.x >= G.cx ? 1 : -1;
      if (e._lw == null) { e._lw = Math.max(...e._txt.map(t => t.offsetWidth)) + 6; e._lh = e._txt.reduce((h, t) => h + t.offsetHeight, 0) + 8; }   // layout size (transforms don't change it)
      const hw = e._lw / 2, lh = e._lh;
      const C = [{ k: 0, dx: 0, dy: 0 }, { k: 1, dx: out * (r + 8 + hw), dy: -(r + 4 + lh / 2) }, { k: 2, dx: -out * (r + 8 + hw), dy: -(r + 4 + lh / 2) }];
      if (e._pick) C.sort((a, b) => (b.k === e._pick) - (a.k === e._pick));
      C.forEach(c => c.cost = cost(e, { l: q.x + c.dx - hw, r: q.x + c.dx + hw, t: top + c.dy, b: top + c.dy + lh }));
      const prev = C.find(c => c.k === e._pick && e._shown && c.cost < 80);                         // a graze of a few px doesn't move a shown label
      let pick = prev || C.find(c => c.cost === 0); if (!pick && e._i === this._next) pick = C.reduce((a, b) => b.cost < a.cost ? b : a);
      e._pick = pick ? pick.k : 0; e._shown = !!pick;
      if (!pick) { e._txt.forEach(t => t._o = "0"); return; }
      placed.push({ l: q.x + pick.dx - hw, r: q.x + pick.dx + hw, t: top + pick.dy, b: top + pick.dy + lh });
      if (pick.dx) { const sc = Math.max(q.s, 0.01), inv = 1 / Math.max(q.persp, 0.3);                // the node is scaled by q.s: shift in its units
        const tf = "translate(" + (pick.dx / sc).toFixed(1) + "px," + (pick.dy / sc).toFixed(1) + "px) scale(" + inv.toFixed(3) + ")"; e._txt.forEach(t => t._t = tf); } });
    // A plaque that would cover a placed label gives way: mission names matter more than section names.
    S.els.forEach(e => { if (!e._cap || !e._q || e.style.visibility === "hidden" || +e.style.opacity <= 0.01) return;
      const b = { l: e._q.x - 110, r: e._q.x + 110, t: e._q.y - 18, b: e._q.y + 18 }; if (placed.some(p => hit(p, b))) e.style.opacity = "0"; });
  }

  // ── The vortex: an ocean whirlpool seen from 35° above, in nexera-hero's field colours ──
  _vxCache() {
    const S = this._S, G = S.G, x = this._xb, N = 64, R = new Float32Array(N + 1), Y = new Float32Array(N + 1), L = new Float32Array(N + 1);
    const ring = f => ({ h: G.HD * Math.pow(f, 1.15), r: G.R0 * (1 - 0.8 * Math.pow(f, 0.72)) });
    for (let i = 0; i <= N; i++) { const q = ring(i / N); R[i] = q.r; Y[i] = q.h * G.cf / G.sf; L[i] = 1.9 * Math.log(G.R0 / q.r); }
    const hero = (f, a, lit) => { const r = 50 + 100 * f, g = 120 - 60 * f, b = 255, Lt = lit || 0;
      return "rgba(" + Math.round(r + (255 - r) * Lt) + "," + Math.round(g + (255 - g) * Lt) + "," + Math.round(b + (255 - b) * Lt) + "," + clamp(a, 0, 1).toFixed(3) + ")"; };
    const grad = (x0, y0, r0, x1, y1, r1, stops) => { const g = x.createRadialGradient(x0, y0, r0, x1, y1, r1); stops.forEach(s => g.addColorStop(s[0], s[1])); return g; };
    // Concentric on the hole, out over the field to 1.8 rims: nothing at an arm's outer tip, full down the wall.
    const fade = (peak, lit) => grad(0, 0, 0, 0, 0, G.R0 * ARM_OUT, [[0, hero(0.9, 0, lit)], [0.2, hero(0.86, peak * 0.6, lit)], [0.4, hero(0.8, peak, lit)],
      [0.58, hero(0.72, peak * 0.75, lit)], [0.8, hero(0.64, peak * 0.2, lit)], [1, hero(0.6, 0, lit)]]);
    const core = x.createRadialGradient(0, 0, 0, 0, 0, G.R0 * 0.36); core.addColorStop(0, "rgba(255,255,255,0.95)"); core.addColorStop(0.3 / 0.72, "rgba(169,200,255,0.9)");
    core.addColorStop(0.58 / 0.72, hero(0.8, 0.33, 0)); core.addColorStop(1, hero(0.8, 0, 0));
    const er = x.createLinearGradient(G.cx - G.R0 * 1.8, 0, G.cx - G.R0 * 0.15, 0); er.addColorStop(0, "rgba(0,0,0,0.92)"); er.addColorStop(0.55, "rgba(0,0,0,0.6)"); er.addColorStop(1, "rgba(0,0,0,0)");
    S.VX = { N, R, Y, L, core, er,
      // The mouth barely darkens on the page's grey ground (a heavy black disc at 0.55; still dark at 0.26).
      hole: grad(0, (G.throatY - G.cy) / G.sf, 0, 0, 0, G.R0, [[0, hero(0.8, 0.28, 0)], [0.45, "rgba(6,7,10,0.12)"], [1, "rgba(6,7,10,0)"]]),
      sheen: grad(0, -G.R0 * 0.62, 0, 0, -G.R0 * 0.62, G.R0 * 0.75, [[0, hero(0.72, 0.12, 0.25)], [1, hero(0.72, 0, 0)]]),
      sheet: fade(0.22, 0), foam: fade(0.7, 0.25), streak: fade(0.55, 0.1) };
  }
  _drawVortex() {
    const S = this._S, G = S.G, xb = this._xb;
    if (!S.VX) this._vxCache();
    const VX = S.VX, spin = S.spin, _p = [0, 0], _q = [0, 0];
    // A point on the flow's log spiral at depth f (0 = rim, 1 = core), and the same spiral carried on over the field.
    const spiralPt = (f, base, out) => { const t = Math.min(1, Math.max(0, f)) * VX.N, i = Math.min(VX.N - 1, t | 0), k = t - i;
      const r = VX.R[i] + (VX.R[i + 1] - VX.R[i]) * k, a = base + VX.L[i] + (VX.L[i + 1] - VX.L[i]) * k;
      out[0] = r * Math.cos(a); out[1] = VX.Y[i] + (VX.Y[i + 1] - VX.Y[i]) * k + r * Math.sin(a); return out; };
    const outsidePt = (o, base, out) => { const rn = 1 + o * (ARM_OUT - 1), r = G.R0 * rn, a = base - 1.9 * Math.log(rn); out[0] = r * Math.cos(a); out[1] = r * Math.sin(a); return out; };
    xb.setTransform(S.dpr, 0, 0, S.dpr, 0, -S.cTop * S.dpr); xb.globalCompositeOperation = "source-over"; xb.globalAlpha = 1; xb.clearRect(0, S.cTop, innerWidth, S.cH);
    xb.save(); xb.translate(G.cx, G.cy); xb.scale(1, G.sf);
    // A hole in the field: the mouth darkens with depth; the far wall catches a pale sheen under the rim.
    xb.fillStyle = VX.hole; xb.beginPath(); xb.arc(0, 0, G.R0, 0, TAU); xb.fill(); xb.fillStyle = VX.sheen; xb.fill();
    xb.globalCompositeOperation = "lighter";
    // Five sheets of water, each its own width and weight, with foam on the leading edge; each is one shape from its
    // tapering tip out in the field down to the core, on the very spiral the field's dots arrive along.
    const OUT = 12;
    for (let b = 0; b < 5; b++) { const base = b * 1.2566 + spin, W = ARM_W[b]; xb.globalAlpha = ARM_L[b] * (0.8 + 0.2 * Math.sin(spin * 0.9 + b * 1.7));
      xb.beginPath();
      for (let k = OUT; k > 0; k--) { outsidePt(k / OUT, base, _p); k === OUT ? xb.moveTo(_p[0], _p[1]) : xb.lineTo(_p[0], _p[1]); }
      for (let k = 0; k <= 30; k++) { spiralPt(k / 30, base, _p); xb.lineTo(_p[0], _p[1]); }
      xb.strokeStyle = VX.foam; xb.lineWidth = 1.5; xb.stroke();
      for (let k = 30; k >= 0; k--) { const f = k / 30; spiralPt(f, base + W * (1 - f * 0.75), _q); xb.lineTo(_q[0], _q[1]); }
      for (let k = 1; k <= OUT; k++) { const o = k / OUT; outsidePt(o, base + W * (1 - E(o)), _q); xb.lineTo(_q[0], _q[1]); }
      xb.closePath(); xb.fillStyle = VX.sheet; xb.fill(); }
    // The water's texture: thin streaks on the same spiral, sliding into the core as the whirl turns.
    const STREAKS = Q >= 3 ? 0 : TIER === "high" ? 30 : TIER === "mid" ? 22 : 14;
    xb.strokeStyle = VX.streak; xb.lineWidth = 1; xb.lineCap = "round";
    for (let k = 0; k < STREAKS; k++) {
      const seed = (k * 0.6180339) % 1, len = 0.25 + 0.35 * ((k * 0.3819) % 1), head = ((seed + spin * 0.09) % 1) * (1 + len) - len, base = k * (TAU / STREAKS) + seed * 0.9 + spin;
      const f0 = Math.max(0.02, head), f1 = Math.min(0.97, head + len); if (f1 - f0 < 0.04) continue;
      xb.globalAlpha = Math.min(1, (f1 - f0) / len * 1.2); xb.beginPath();
      for (let i = 0; i <= 12; i++) { spiralPt(f0 + (f1 - f0) * i / 12, base, _p); i ? xb.lineTo(_p[0], _p[1]) : xb.moveTo(_p[0], _p[1]); }
      xb.stroke(); }
    xb.restore();
    // The outer arms on the left fade away (the companion's corner stays clear); nothing near the core changes.
    xb.save(); xb.globalCompositeOperation = "destination-out"; xb.beginPath(); xb.rect(0, S.cTop, G.cx, S.cH); xb.ellipse(G.cx, G.cy, G.R0 * 0.55, G.R0 * 0.55 * G.sf, 0, 0, TAU); xb.clip("evenodd");
    xb.fillStyle = VX.er; xb.fillRect(0, S.cTop, G.cx, S.cH); xb.restore();
    // The core: a steady light at the bottom of the hole.
    xb.save(); xb.globalAlpha = 1; xb.translate(G.cx, G.throatY); xb.scale(1, G.sf * 1.25); xb.globalCompositeOperation = "lighter";
    xb.fillStyle = VX.core; xb.beginPath(); xb.arc(0, 0, G.R0 * 0.36, 0, TAU); xb.fill(); xb.restore();
  }

  // ── The governor: when frames keep running long (an average over 24ms for ~1.5s) it steps quality down one level
  // and waits 3s before judging again. It never steps back up in a session, so it cannot flicker between levels.
  _govern(dtMs) {
    const g = this._gov; if (reduced || document.hidden) return;
    g.ema += (Math.min(dtMs, 100) - g.ema) * 0.08;
    if (g.calm > 0) { g.calm -= dtMs; return; }
    g.slow = g.ema > 24 ? g.slow + dtMs : 0;
    if (g.slow > 1500 && Q < 3) { Q++; g.slow = 0; g.calm = 3000;
      if (Q === 2) { FIELD.lowRes(true); this._sizeCanvas(); }
      console.info("[vortex-map] quality level " + Q + " (frames averaging " + g.ema.toFixed(1) + "ms)"); }
  }
  // ── One clock ──
  _tick(now) { if (!this._running) return; this._frame(now); if (!reduced) requestAnimationFrame(this._tick); }
  _frame(now) {
    const S = this._S; if (!S.els.length || !FIELD || document.hidden) return;
    const dtMs = now - S.last, dt = Math.min(0.05, Math.max(0, dtMs / 1000)); S.last = now; S.SY = scrollY; this._govern(dtMs);
    // The page's road box can move under us (a side card opens, a note above it changes): follow it (one read, first).
    this._syncBox();
    const moved = S.SY !== S.lastY;
    S.boost = Math.min(1, S.boost * Math.exp(-dt * 1.2) + (S.lastY < 0 ? 0 : Math.abs(S.SY - S.lastY)) * 0.004 + S.poke); S.poke = 0;   // interaction raises the pace; it eases back within ~2s
    if (moved) S.lastY = S.SY;
    // The start card's border turns only with the scroll: 0.09° per pixel, eased so it glides and comes to rest.
    const target = S.SY * 0.09, first = S.borderA == null; if (first) S.borderA = target;
    if (first || Math.abs(target - S.borderA) > 0.02) { S.borderA += (target - S.borderA) * (reduced ? 1 : 1 - Math.exp(-dt * 2.5));
      const a = S.borderA.toFixed(2) + "deg", sel = this.getAttribute("anchor"), el = sel && document.querySelector(sel);
      this.style.setProperty("--a", a); if (el) el.style.setProperty("--a", a); }
    // The lit stretch eases to the score (the page's own 1.3s curve).
    if (S.litNow !== S.litTo && S.litNow != null) { const k = reduced ? 1 : clamp((now - S.litT0) / 1300, 0, 1), e = 1 - Math.pow(1 - k, 3); S.litNow = S.litFrom + (S.litTo - S.litFrom) * e; if (k >= 1) S.litNow = S.litTo; S.roadDirty = true; }
    if (!reduced) S.spin += dt * (0.12 + S.boost * 0.24);                                            // idle: one turn in ~52s
    if (!reduced && Q < 3) S.drift += dt * (0.45 + S.boost * 0.35);                                  // the wave's own slow drift
    // At rest the scene draws at the tier's idle rate: 30fps on strong devices, 20 on modest ones (or once the governor
    // has stepped down twice), 15 on low-end; while you scroll, every frame (every other one once the governor steps in).
    // A skipped frame still honours a pending road change.
    const rest = !moved && S.boost < 0.03, every = rest ? (TIER === "low" ? 4 : TIER === "mid" || Q >= 2 ? 3 : 2) : Q >= 1 ? 2 : 1;
    const halfRate = (S.frame++ % every) !== 0;
    if (halfRate) { if (S.roadDirty) { this._drawRoad(); S.roadDirty = false; S.roadPhase = S.bgPhase; } return; }
    this._drawVortex();
    // The wave: its own drift (0.45 phase units a second, ~1/7 of the hero's pace) plus 0.009 per pixel of scroll, eased.
    const G = S.G, bgTarget = reduced ? 0 : S.SY * 0.009; if (S.bgScroll == null) S.bgScroll = bgTarget;
    if (!S.vortexSet) { FIELD.setVortex(G.cx, G.cy, G.R0, G.R0 * G.sf, { R0: G.R0, sf: G.sf, cf: G.cf, HD: G.HD }); S.vortexSet = true; }
    if (Math.abs(bgTarget - S.bgScroll) > 0.0015) S.bgScroll += (bgTarget - S.bgScroll) * (1 - Math.exp(-dt * 3)); else S.bgScroll = bgTarget;
    S.bgPhase = S.bgScroll + S.drift;
    if (Q < 3 || moved) FIELD.draw(S.bgPhase, 4 + S.spin, S.spin);                                   // +4: the whirl is already drawing the grid in
    const calm = !moved && S.boost < 0.03 && !S.roadDirty; S.roadSkip = calm ? (S.roadSkip || 0) + 1 : 0;
    if (moved || S.roadDirty || (S.bgPhase !== S.roadPhase && (!calm || S.roadSkip % (every >= 3 ? 2 : 3) === 0))) { this._drawRoad(); S.roadDirty = false; S.roadPhase = S.bgPhase; }   // once: the road rides this frame's wave
  }
  // The scrollY that brings a mission to the upper third of the view, clear of the vortex (the first one: onto it).
  _syncBox() { const S = this._S, box = this._roadBox(); if (!box || !S.G) return;
    const br = box.getBoundingClientRect(), top = br.top + scrollY;
    if (Math.abs(top - S.G.top) > 0.5 || Math.abs(br.left - S.G.left) > 0.5) { S.G.top = top; S.G.left = br.left; S.roadDirty = true;
      this._r.col.style.height = Math.ceil(top + S.y1 - S.G.cy + innerHeight) + "px"; } }
  _scrollFor(ry) { this._syncBox(); const S = this._S, G = S.G, max = Math.max(0, document.documentElement.scrollHeight - innerHeight); return clamp(G.top + ry - (G.cy - 260), 0, max); }
  scrollToMission(i, smooth) {
    if (!this.ready) return false; const e = this._S.els.find(x => x._i === i); if (!e) return false;
    scrollTo({ top: this._scrollFor(e._ry), behavior: smooth && !reduced ? "smooth" : "auto" }); return true;
  }
  scrollToFinish(smooth) { if (!this.ready) return false; scrollTo({ top: this._scrollFor(this._S.finY), behavior: smooth && !reduced ? "smooth" : "auto" }); return true; }
  get quality() { return Q; }
}
if (!customElements.get("vortex-map")) customElements.define("vortex-map", VortexMap);
