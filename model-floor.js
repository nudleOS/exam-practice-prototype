import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

// A transparent three.js canvas holding BOTH the model and the ripple floor, so the two
// share one camera: orbit the object and the rings turn with it, flattening toward edge-on
// as the camera drops — which is what makes the floor read as ground rather than wallpaper.
class ModelFloor extends HTMLElement {
  static get observedAttributes() { return ["src", "floor", "face", "clip", "yaw", "lift", "paused", "fit", "speed"]; }
  connectedCallback() {
    // A copy in a page's raw template (<x-dc>: live markup, not an inert <template>) is never a view. Defining the element
    // upgraded those copies before the runtime rendered and removed them: 3 WebGL contexts and a 3.2 MB download for robots
    // no screen showed (measured 2026-10-06 at 360x687, a phone's question page: the stack ran define -> connectedCallback).
    if (this.closest("x-dc")) return;
    // A move (removed here, added there in the same task) keeps the live renderer: see disconnectedCallback.
    clearTimeout(this._tdT);
    // Self-healing: a live mount is one that still has its canvas. Returning on `_up` alone
    // left the element permanently blank if the canvas was ever lost.
    if (this._up && this.shadowRoot && this.shadowRoot.querySelector("canvas")) return;
    // Defensive: if a prior mount left a teardown behind, run it before building another.
    // Two live renderers on one element is how contexts accumulate past the browser's cap.
    if (this._teardown) { this._teardown(); this._teardown = null; }
    this._up = true;
    // Shadow DOM keeps the canvas invisible to the host page's reconciler, so the element can
    // mount anywhere — mid-stream, inside a loop — without a foreign child breaking a diff.
    const root = this.shadowRoot || this.attachShadow({ mode: "open" });
    root.replaceChildren();
    // Sizing and the fade live INSIDE the shadow root. Writing them to this.style fought the
    // host page's reconciler, which owns the element's style attribute and overwrites it —
    // taking the component's own geometry with it.
    const sheet = document.createElement("style");
    sheet.textContent = ":host { display:block; position:relative }" +
      ".stage { position:absolute; inset:0; opacity:0; transition:opacity 320ms ease }" +
      ".stage.ready { opacity:1 }";
    root.appendChild(sheet);
    const stage = document.createElement("div");
    stage.className = "stage";
    root.appendChild(stage);
    this._stage = stage;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 400);
    // A device with no GPU, or a page already holding its browser's limit of WebGL contexts,
    // throws here. The companion is decoration, so it steps aside rather than taking the
    // page's script down with it.
    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    } catch (e) {
      this.setAttribute("data-avatar", "unavailable");
      stage.classList.add("ready");
      return;
    }
    renderer.setClearAlpha(0);
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.domElement.style.cssText = "display:block; width:100%; height:100%; touch-action:none";
    stage.appendChild(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0xdfe8ff, 0x1a1d24, 1.15));
    const key = new THREE.DirectionalLight(0xffffff, 2.1);
    key.position.set(3, 6, 4);
    scene.add(key);
    const rim = new THREE.DirectionalLight(0x4d7bff, 1.5);
    rim.position.set(-4, 2, -3);
    scene.add(rim);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.enablePan = false;
    controls.minDistance = 1.2;
    controls.maxDistance = 40;
    // Never let the camera drop under the floor the model is standing on.
    controls.maxPolarAngle = Math.PI * 0.495;
    // still: a pose, not a toy: no drag-rotate, no zoom (and the page scrolls through it; see playClip for the pose)
    if (this.hasAttribute("still")) controls.enabled = false;
    this._controls = controls;

    const pivot = new THREE.Group();
    this._yawTarget = parseFloat(this.getAttribute("yaw")) || 0;
    this._liftTarget = parseFloat(this.getAttribute("lift")) || 0;
    pivot.rotation.y = (this.getAttribute("face") === "user" ? 0 : Math.PI) + this._yawTarget;
    scene.add(pivot);

    // The hero's ripple, rebuilt on the ground plane: four rings on a 30s cycle, staggered
    // 7.5s apart, azure and cobalt alternating. Lying flat at y=0 they are genuinely the
    // floor the model stands on, not a backdrop behind it.
    const AZURE = 0x0068f8, COBALT = 0x1e46ff;
    const RING_CYCLE = 30, RING_MAX = 15;

    // The hero ring is not a hairline — it is a bright core with an outer bloom and a dark
    // outline that reads as depth. A radial-gradient texture gives all three in one plane,
    // and gets the soft blur a geometric ring cannot.
    const ringTexture = (() => {
      const S = 512;
      const c = document.createElement("canvas");
      c.width = c.height = S;
      const g = c.getContext("2d");
      const grd = g.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
      grd.addColorStop(0.00, "rgba(255,255,255,0)");
      grd.addColorStop(0.78, "rgba(255,255,255,0)");
      grd.addColorStop(0.86, "rgba(255,255,255,0.10)");
      grd.addColorStop(0.935, "rgba(255,255,255,0.62)");
      grd.addColorStop(0.962, "rgba(255,255,255,1)");
      grd.addColorStop(0.980, "rgba(255,255,255,0.55)");
      grd.addColorStop(1.00, "rgba(255,255,255,0)");
      g.fillStyle = grd;
      g.fillRect(0, 0, S, S);
      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    })();

    const rings = [AZURE, COBALT, COBALT, AZURE].map((col, i) => {
      const mesh = new THREE.Mesh(
        new THREE.PlaneGeometry(2, 2),
        new THREE.MeshBasicMaterial({
          map: ringTexture, color: col, transparent: true, opacity: 0,
          blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
        })
      );
      mesh.rotation.x = -Math.PI / 2;
      mesh.renderOrder = -1;
      scene.add(mesh);
      return { mesh, phase: i / 4 };
    });

    // A soft pool under the feet, so the model sits in the floor's light rather than on
    // top of a hole in it.
    const pool = new THREE.Mesh(
      new THREE.CircleGeometry(3.6, 64),
      new THREE.MeshBasicMaterial({
        color: AZURE, transparent: true, opacity: 0.12,
        blending: THREE.AdditiveBlending, depthWrite: false
      })
    );
    pool.rotation.x = -Math.PI / 2;
    pool.position.y = 0.002;
    pool.renderOrder = -2;
    scene.add(pool);

    // A contact shadow grounds the figure: without it the model floats however well the
    // rings are placed.
    const shadow = new THREE.Mesh(
      new THREE.CircleGeometry(0.85, 48),
      new THREE.MeshBasicMaterial({ color: 0x05070c, transparent: true, opacity: 0.34, depthWrite: false })
    );
    shadow.rotation.x = -Math.PI / 2;
    shadow.position.y = 0.004;
    scene.add(shadow);

    const clock = new THREE.Clock();
    let ringScale = 2.4;
    // The floor is four states, not a flag: the travelling ripple, a single still disc, only its
    // first ring ("ring": for a small box the wide pool would be cut by the edges), or nothing at
    // all when the avatar is furniture beside a question rather than the subject.
    const floorMode = () => this.getAttribute("floor") || "ripple";
    this._applyFloor = () => {
      const mode = floorMode();
      rings.forEach(r => { r.mesh.visible = mode === "ripple"; });
      pool.visible = mode !== "none" && mode !== "ring";
      // No floor, no disc: a shadow with nothing to fall on reads as a hole under the feet.
      shadow.visible = mode !== "none";
      if (mode === "still" || mode === "ring") {
        // One resting ring at the pool's edge reads as a plinth, not a pulse.
        rings[0].mesh.visible = true;
        // "ring" is drawn small enough (radius ~0.96 of the 2.4 figure) to sit inside a narrow box.
        rings[0].mesh.scale.setScalar((mode === "ring" ? 1.0 : 1.55) * (ringScale / 2.4));
        rings[0].mesh.material.opacity = 0.34;
      }
    };

    let lastW = 0, lastH = 0;
    const resize = () => {
      const w = this.clientWidth, h = this.clientHeight;
      if (!w || !h || (w === lastW && h === lastH)) return;
      lastW = w; lastH = h;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    };
    this._ro = new ResizeObserver(resize);
    this._ro.observe(this);
    resize();
    // The pane animates open, so the first laid-out size can arrive a frame or two late.
    requestAnimationFrame(resize);
    this._sizeT = setTimeout(resize, 120);

    const src = this.getAttribute("src");
    // Loading is a function of src, so a bound src that changes after connect reloads rather
    // than leaving the first model on screen.
    this._load = src => {
      while (pivot.children.length) pivot.remove(pivot.children[0]);
      // Swapping src hides the stage again, so the outgoing model does not sit visible
      // through the next load.
      if (this._ready) stage.classList.remove("ready");
      // A new model brings its own clips; the old mixer would animate a scene that is gone.
      this._mixer = null; this._clips = null; this._action = null;
      if (!src) return;
      new GLTFLoader().load(src, gltf => {
        if (this._src !== src) return;   // a newer src won the race
        const obj = gltf.scene;
        const box = new THREE.Box3().setFromObject(obj);
        const size = box.getSize(new THREE.Vector3());
        const mid = box.getCenter(new THREE.Vector3());
        // Stand the model at its real size in metres, so the floor reads as a measured
        // ground plane rather than an abstract one — judging scale is the point of this pane.
        const H = parseFloat(this.getAttribute("height")) || 2.4;
        const k = H / Math.max(size.y || 1, 0.001);
        obj.scale.setScalar(k);
        obj.position.set(-mid.x * k, -box.min.y * k, -mid.z * k);
        pivot.add(obj);

        const clips = gltf.animations || [];
        // inplace (optional): pin the hips' x/z to the first frame, keeping their height, so a clip that walks the body
        // around (measured: the companion robot's greet ends ~1.9 units from where it starts) plays in place. A figure
        // standing in a box then stays centred and turns about itself. Without the attribute, clips play as authored.
        // Pinned to the skeleton's REST hip position, the same for every clip (pinning each clip to its own first frame left
        // clips offset from each other: measured, the robot's run starts 0.34 units off-centre and swung out of its box).
        if (this.hasAttribute("inplace")) clips.forEach(c => c.tracks.forEach(t => {
          if (!/hips\.position$/i.test(t.name)) return;
          const bone = obj.getObjectByName(t.name.replace(/\.position$/, "")), rx = bone ? bone.position.x : t.values[0], rz = bone ? bone.position.z : t.values[2];
          const v = t.values; for (let i = 0; i < v.length; i += 3) { v[i] = rx; v[i + 2] = rz; }
        }));
        if (clips.length) {
          this._mixer = new THREE.AnimationMixer(obj);
          this._clips = clips;
          this._action = null;
          this.playClip(this.getAttribute("clip"));
          // Turn about the figure, not the file's origin. A clip can stand the body well away from where its bind
          // pose was centred (measured: the companion robot's greet stands it 1.95 units forward), so `yaw` swung it
          // round a wide circle, out of its box. The pivot moves under the posed body and the model moves back by the
          // same amount: the picture is unchanged at yaw 0, and turning now happens in place.
          // Measured at the clip's full weight (its fade-in starts at 0, which would measure the bind pose instead).
          if (this._action) this._action.setEffectiveWeight(1);
          this._mixer.update(0); obj.updateMatrixWorld(true);
          const posed = new THREE.Box3().setFromObject(obj, true).getCenter(new THREE.Vector3());
          const local = pivot.worldToLocal(posed.clone());
          obj.position.x -= local.x; obj.position.z -= local.z;
          pivot.position.x = posed.x; pivot.position.z = posed.z;
        }
        this.dispatchEvent(new CustomEvent("loaded", { bubbles: true }));
        // Nothing is shown until there is something to show — otherwise the empty canvas
        // reads as a box that flashes and vanishes before the model appears.
        this._ready = true;
        stage.classList.add("ready");
        this.setAttribute("data-avatar", "ready");
        // The model stands ON the ripple's centre, so the camera aims at the floor point
        // (0,0,0) rather than the figure's mid-height — that puts its feet dead centre and
        // lets it rise into the upper half of the frame.
        // Frame the model to FILL its box: the visible extent is 2·d·tan(fov/2), so the
        // padding factor decides how much of the canvas the figure occupies. 1.35 left it at
        // ~37%; 0.62 fills roughly 80%. `fit` overrides per mount.
        // Framing is re-runnable: a moved figure can be re-framed for its new box without reloading (fit changes).
        this._frame = () => {
        const pad = parseFloat(this.getAttribute("fit")) || 0.62;
        const fov = camera.fov * Math.PI / 180;
        const d = Math.max((H * pad) / Math.tan(fov / 2), H * 1.05);
        // Facing the user is a different framing from the three-quarter studio view: straight
        // down the z axis, so the avatar meets the eye instead of presenting a shoulder.
        const dir = (this.getAttribute("face") === "user"
          ? new THREE.Vector3(0, 0.18, 1)
          : new THREE.Vector3(0.42, 0.46, 0.88)).normalize().multiplyScalar(d);
        camera.position.copy(dir);
        // Aiming at the floor point wastes half the frame below ground and clips the head:
        // the visible span is ±d·tan(fov/2) about the target, so a model standing 0→H needs
        // the target at its mid-height to fit. The studio view keeps the floor as its target,
        // because there the ripple IS the subject and the feet should sit dead centre.
        const aimY = this.getAttribute("floor") === "none" || this.getAttribute("face") === "user" ? H / 2 : 0;
        camera.position.y += aimY;
        controls.target.set(0, aimY, 0);
        controls.update();
        controls.saveState();
        };
        this._frame();
        // The ripple spreads relative to the object, so a hand tool and a haul truck each
        // get a floor at their own scale.
        ringScale = H;
        pool.scale.setScalar(H / 2.4);
        shadow.scale.setScalar((Math.max(size.x, size.z) * k) / 0.85 * 0.6);
        this._applyFloor();
      }, undefined, () => { stage.classList.add("ready"); this.setAttribute("data-avatar", "failed"); this.dispatchEvent(new CustomEvent("failed", { bubbles: true })); });
    };
    this._src = src;
    this._load(src);

    // Connected is not the same as on screen. A pane left open behind another, or a
    // backgrounded preview, kept this loop rendering — so the loop follows visibility.
    let visible = true;
    const wake = () => {
      if (!visible || this._raf || !this._up) return;
      clock.getDelta();
      this._raf = requestAnimationFrame(tick);
    };
    const sleep = () => { if (this._raf) { cancelAnimationFrame(this._raf); this._raf = 0; } };
    this._io = new IntersectionObserver(es => {
      visible = es.some(e => e.isIntersecting);
      if (visible) wake(); else sleep();
    }, { threshold: 0 });
    this._io.observe(this);
    this._onVis = () => { if (document.hidden) sleep(); else wake(); };
    document.addEventListener("visibilitychange", this._onVis);

    const tick = () => {
      this._raf = requestAnimationFrame(tick);
      const base = this.getAttribute("face") === "user" ? 0 : Math.PI;
      const ty = base + (this._yawTarget || 0);
      pivot.rotation.y += (ty - pivot.rotation.y) * 0.08;
      pivot.position.y += ((this._liftTarget || 0) - pivot.position.y) * 0.08;
      if (this.getAttribute("autorotate") !== "off") pivot.rotation.y += 0.0022;

      const t = clock.getElapsedTime();
      // Derived, not clock.getDelta() — that would consume the same tick the rings read.
      if (this._mixer) { this._mixer.update(Math.min(0.1, Math.max(0, t - (this._lastT || t))));
        const a = this._action;
        if (this._holdAt != null && a && !a.paused && (a.timeScale >= 0 ? a.time >= this._holdAt : a.time <= this._holdAt) /* either direction */) { a.time = this._holdAt; a.paused = true; this._mixer.update(0); } }
      this._lastT = t;
      if (floorMode() === "ripple") rings.forEach(r => {
        const p = ((t / RING_CYCLE) + r.phase) % 1;
        // Ease the expansion the way the hero does — quick off the mark, slowing as it
        // widens — rather than the flat linear crawl.
        const e = 1 - Math.pow(1 - p, 1.7);
        r.mesh.scale.setScalar((0.35 + e * RING_MAX) * (ringScale / 2.4));
        const a = p < 0.10 ? p / 0.10 : p > 0.55 ? Math.max(0, Math.pow((1 - p) / 0.45, 1.3)) : 1;
        r.mesh.material.opacity = a * 0.42;
      });

      controls.update();
      renderer.render(scene, camera);
    };
    wake();
    // `renderer.dispose()` alone does NOT return the WebGL context — it frees GL objects and
    // leaves the context live. React remounts this element every time the pane opens, so
    // without an explicit forceContextLoss each open leaks one context; past the browser's
    // ~16-context cap the compositor starts thrashing and the main thread stalls outright.
    this._bindUnload();
    this._teardown = () => {
      this._mixer = null; this._clips = null; this._action = null;
      cancelAnimationFrame(this._raf);
      this._raf = 0;
      clearTimeout(this._sizeT);
      if (this._io) { this._io.disconnect(); this._io = null; }
      if (this._onVis) { document.removeEventListener("visibilitychange", this._onVis); this._onVis = null; }
      if (this._ro) { this._ro.disconnect(); this._ro = null; }
      controls.dispose();
      scene.traverse(o => {
        if (o.geometry) o.geometry.dispose();
        const mats = Array.isArray(o.material) ? o.material : (o.material ? [o.material] : []);
        mats.forEach(m => { if (m.map) m.map.dispose(); m.dispose(); });
      });
      ringTexture.dispose();
      renderer.dispose();
      const ctx = renderer.getContext();
      const ext = ctx && ctx.getExtension("WEBGL_lose_context");
      if (ext) ext.loseContext();
      renderer.forceContextLoss();
      if (renderer.domElement && renderer.domElement.parentNode) renderer.domElement.remove();
      if (this._onHide) { window.removeEventListener("pagehide", this._onHide); this._onHide = null; }
      this._controls = null;
    };
  }
  reset() { if (this._controls) this._controls.reset(); }
  _rate() { const r = parseFloat(this.getAttribute("speed")); return isFinite(r) && r !== 0 ? r : 1; }
  attributeChangedCallback(name, was, now) {
    if (was === now) return;
    if (name === "floor") { if (this._applyFloor) this._applyFloor(); return; }
    if (name === "clip") { this.playClip(now); return; }
    // paused (optional): the figure holds the current frame of its clip until the attribute is removed —
    // e.g. frozen in its first pose while a card spins, moving the instant the card lands.
    if (name === "paused") { if (this._action) this._action.paused = now !== null; return; }
    // speed (optional): playback rate of the clip, e.g. 1.6 to run faster (legs and all), or negative to play it backwards
    // (a fall played backwards reads as getting up). fade (optional, read at play): the crossfade in seconds (default 0.3).
    if (name === "speed") { if (this._action) this._action.timeScale = this._rate(); return; }
    if (name === "yaw") { this._yawTarget = parseFloat(now) || 0; return; }
    if (name === "fit") { if (this._frame) this._frame(); return; }
    if (name === "lift") { this._liftTarget = parseFloat(now) || 0; return; }
    if (name !== "src" || !this._load) return;
    this._src = now;
    this._load(now);
  }
  // A rigged model carries its own performances. Export names vary ("greet_04.001"), so a
  // clip is matched on the word rather than on an exact name the exporter chose.
  playClip(want) {
    if (!this._mixer || !this._clips) return;
    const key = String(want || "").toLowerCase();
    const hit = key && this._clips.filter(c => c.name.toLowerCase().indexOf(key) !== -1)[0];
    if (!hit) { if (this._action) { this._action.fadeOut(0.3); this._action = null; } return; }
    if (this._action && this._action.getClip() === hit) return;
    const next = this._mixer.clipAction(hit);
    // A fall (or the robot's defeat) stays down — it holds its last frame until something else
    // is asked for. Anything else loops, because a greet or a dance that freezes looks like a crash.
    // loop="once" plays any clip one time and holds its last frame (the home greeting must not visibly loop).
    const once = key === "fall" || key === "defeat" || this.getAttribute("loop") === "once";
    next.reset();
    // from="seconds" starts the clip part-way (the finish plays only the dance's best stretch).
    const from = parseFloat(this.getAttribute("from"));
    if (isFinite(from) && from > 0) next.time = Math.min(from, hit.duration);
    next.setLoop(once ? THREE.LoopOnce : THREE.LoopRepeat, once ? 1 : Infinity);
    next.clampWhenFinished = once;
    // hold="seconds" (with loop="once") stops the clip on a chosen frame instead of its last one;
    // with reduced motion the figure starts already in that pose rather than playing into it.
    const hold = once ? parseFloat(this.getAttribute("hold")) : NaN;
    this._holdAt = isFinite(hold) ? Math.min(hold, hit.duration) : null;
    // still (with loop="once" and hold): the figure appears already in the held pose and never moves; no blend in from the bind pose
    const still = this.hasAttribute("still");
    next.timeScale = this._rate(); const fade = still ? 0 : parseFloat(this.getAttribute("fade")) || 0.3;
    next.fadeIn(fade).play();
    if (this.hasAttribute("paused")) next.paused = true;
    if (this._holdAt != null && (still || window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches)) {
      next.time = this._holdAt; next.paused = true; next.setEffectiveWeight(1); }
    if (this._action) this._action.crossFadeTo(next, fade, false);
    this._action = next;
  }
  // A reload does not always fire disconnectedCallback, and the context survives long enough
  // to count against the cap on the next load. pagehide is the one event that reliably fires.
  _bindUnload() {
    this._onHide = () => { if (this._teardown) { this._teardown(); this._teardown = null; this._up = false; } };
    window.addEventListener("pagehide", this._onHide);
  }
  // Teardown waits one task: if the element is re-attached first (moved from one container to another, e.g. the
  // companion jumping from the page into a card), it keeps its renderer, model and clip instead of reloading.
  // Removed for good, it tears down as before and gives its WebGL context back.
  disconnectedCallback() {
    clearTimeout(this._tdT);
    this._tdT = setTimeout(() => {
      if (this.isConnected) return;
      if (this._teardown) { this._teardown(); this._teardown = null; }
      this._up = false;
    }, 0);
  }
}
if (!customElements.get("model-floor")) customElements.define("model-floor", ModelFloor);
