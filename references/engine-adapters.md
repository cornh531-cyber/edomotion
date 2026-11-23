# Engine adapters — per-platform build procedures

All engines consume the same `Motion.md` + `timeline.json` (see SKILL.md §3). Pick the
section matching the engine chosen in SKILL.md §1. Everything here is model-agnostic:
plain commands, no vendor-only plugins required.

---

## A. OpenMotion (nexu-io/openmotion)

Full-stack agentic video studio; video source is HTML, direction lives in `Motion.md`,
timing is edited in Studio, export is MP4. Requires Node.js, FFmpeg, a browser.

```bash
# 1. Install the skill into your agent (skills CLI works on 70+ agents)
npx skills add nexu-io/openmotion --skill openmotion
# 2. Ask your agent (then follow its scaffold):
#    "Use OpenMotion to install and connect the local Studio and MCP, then help me make a video."
```

Procedure:
1. Invoke OpenMotion's matching sub-skill:
   - `motion-director` — original video from a brief (our default path).
   - `motion-recreate` — user supplied a reference clip/link (analyze shots, rebuild with
     OUR original story — never the reference's content, per SKILL.md rule 5).
2. Write `Motion.md` (shot order, transitions, text animation, timing, sound cues, brand
   kit section) — OpenMotion treats this as the creative-direction source of truth.
3. Build the composition in HTML/CSS/JS per the scaffold's conventions; one section per
   shot id; numbers imported from `timeline.json`.
4. Generate/collect assets per SKILL.md §4 (SVG characters, VO clips, music).
5. Edit timing/clips in **Studio** if the agent supports it; keep Studio edits in sync with
   `timeline.json` (Studio wins only if the human edited it).
6. Export MP4 through OpenMotion's render/production flow (`motion-production` skill /
   Studio export), then run the QC gate (SKILL.md §6).

Notes: OpenMotion also has `motion-template-to-video` and `motion-video-to-template` — use
the latter to turn a finished part into a reusable template for the next parts.

---

## B. HyperFrames (heygen-com/hyperframes)

HTML is the source of truth: plain `index.html` with `data-*` timing attributes + GSAP
timeline; deterministic render = headless Chrome seeks every frame, FFmpeg encodes. No
React, no build step.

```bash
npx skills add heygen-com/hyperframes     # or: npx hyperframes skills update
npx hyperframes init my-video && cd my-video
```

Procedure:
1. Author `index.html` from the scaffold: standard elements (`div`, `h1`, `video`, `audio`)
   carrying `data-*` timing attributes; register the GSAP timeline per the scaffold's
   convention (the engine seeks `window.__timelines`). Include `data-composition-id`
   (e.g. `story-part1`) and the canvas 1080×1920.
2. One block per shot id; text/caption layers absolutely positioned inside safe zones.
3. Audio: `<audio>` elements positioned at shot starts; VO files from §4.
4. Validate & iterate:
   ```bash
   npx hyperframes lint        # missing composition id, overlapping tracks, unregistered timelines
   npx hyperframes validate    # contrast audit at 5 timestamps
   npx hyperframes inspect     # duration / tracks / dimensions — must match timeline.json
   npx hyperframes preview     # live-reload browser preview (port 3002)
   ```
5. Render:
   ```bash
   npx hyperframes render --quality draft --output draft.mp4   # fast iteration
   npx hyperframes render --quality high --output final.mp4    # delivery
   ```
6. Optional visual audit: `node skills/hyperframes/scripts/animation-map.mjs <composition-dir>`.
7. QC gate (SKILL.md §6) → deliver.

---

## C. Remotion (React + TypeScript)

```bash
npm create video@latest    # pick the "blank"/hello-world TS template
```

3D note (for the blocky toon-chibi look): use `@remotion/three` (`npm i @remotion/three
three @react-three/fiber`) — a `<Three.jsCanvas>` inside `<Sequence>`s, camera/objects
keyframed from `useCurrentFrame()` + timeline.json.

Project layout:

```
src/
  Root.tsx        # <Composition id="Story" .../> registration
  Story.tsx       # reads timeline.json → one <Sequence> per shot
  shots/S01.tsx … # one component per shot id
public/
  vo/vo_S01.mp3 …  music.mp3  sfx/*.mp3
```

`Root.tsx` core:

```tsx
import timeline from './timeline.json'; // or a generated TS constant
const FPS = timeline.fps; // 30
const totalFrames = Math.round(timeline.shots.at(-1).end * FPS);

<Composition id="Story" component={Story} durationInFrames={totalFrames}
  fps={FPS} width={1080} height={1920} />
```

`Story.tsx` core rules:
- Map every shot to `<Sequence from={Math.round(shot.start * FPS)}
  durationInFrames={Math.round((shot.end - shot.start) * FPS)}>` — never hardcode numbers.
- Animation: `const frame = useCurrentFrame();` then
  `interpolate(frame, [0, 10], [0.96, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})`
  for push-ins; `spring({frame, fps, config: {damping: 200}})` for pops.
- Push-in on beats 5–6: scale from 1 → 1.06 across the whole sequence.
- VO: inside each shot's `<Sequence>`, `<Audio src={staticFile('vo/vo_' + id + '.mp3')} />`.
- Music: one `<Audio loop src={staticFile('assets/music.mp3')} volume={(f) =>
  interpolate(f, [0, 30], [0.35, 0.25], {extrapolateRight: 'clamp'})} />` from frame 0.
- Captions: absolutely positioned div at `top: 72%`, `width: 100%`, text-align center,
  inside each shot's Sequence.

QC before render (measure, don't assume):
```bash
npx remotion compositions            # Story must report 1080x1920, correct fps
npx remotion still Story out/qc.png --frame=90   # spot-check a mid frame
npx remotion render Story out/final.mp4 --crf=18
ffprobe -v error -show_entries format=duration -of csv=p=0 out/final.mp4
```

QC gate (SKILL.md §6) → deliver.

---

## D. Motion Canvas (TypeScript scene generators)

```bash
npm create motion-canvas@latest
```

- One scene per beat (7 scenes), each generator awaits `yield* waitFor(seconds)` matching
  the timeline; per-shot generators receive `start/end` from `timeline.json`.
- Characters: SVG layers with `Node` references; animate `rotation/position/scale` via
  tweens; captions as `<Txt>`.
- Render: `npm run render` → MP4; then QC gate.

Use when the user prefers Motion Canvas explicitly; otherwise Remotion/HyperFrames are the
primary Node paths.

---

## E. html-fallback (no engine installed — works for ANY model)

Deliver **one self-contained `index.html`** (no external deps, no CDN — must work offline
and in sandboxed previews). It is both the preview and the render source.

Required structure:

```html
<!doctype html><html><head><meta charset="utf-8">
<style>
  html,body{margin:0;height:100%;background:#000;display:grid;place-items:center}
  #stage{width:1080px;height:1920px;position:relative;overflow:hidden;
         transform-origin:center}
  /* scale stage to viewport via JS; everything inside is absolutely positioned */
  .cap{position:absolute;top:72%;width:100%;text-align:center;
       font:600 52px 'Baloo 2',Poppins,system-ui,sans-serif;color:#fff;
       -webkit-text-stroke:3px #1a1a1a}
</style></head>
<body><div id="stage"><!-- SVG characters, backgrounds, caption divs --></div>
<script>
const SHOTS = [ /* pasted verbatim from timeline.json */ ];
const FPS = 30; // deterministic clock driven by requestAnimationFrame from t=0
// playhead t → find shot → apply transforms/keyframes per shot id
</script>
<script>/* click-to-play overlay: audio elements fire at their shot starts */</script>
</body></html>
```

Rules:
- Fixed 1080×1920 stage scaled by `min(vw/1080, vh/1920)` — layout never reflows.
- One JS section per shot id, all numbers from `SHOTS` (the timeline), CSS keyframes
  paused/seekable (set `animation-delay` negative per elapsed time, or drive transforms from
  the playhead — prefer the playhead: it is deterministic and seekable).
- Audio: `<audio>` per VO clip started at its shot start on first user click (autoplay
  policies); music looped, ducked by lowering its `volume` while any VO clip is active.
- If an AI image tool is available, characters may instead be PNG sprites — keep one sheet
  per character; otherwise inline SVG.

Rendering paths (in order of preference):

1. **Playwright frame-accurate capture** (Node or Python available):
   ```bash
   # after: pip install playwright && playwright install chromium   (or npm i playwright)
   ```
   Python recipe — seek the page's playhead to each frame, screenshot, encode:
   ```python
   # render_frames.py  (concept: exposes window.setPlayhead(t) from the HTML script)
   from playwright.sync_api import sync_playwright
   import subprocess, pathlib, json
   tl = json.load(open('timeline.json')); fps = tl['fps']
   total = int(tl['shots'][-1]['end'] * fps)
   pathlib.Path('frames').mkdir(exist_ok=True)
   with sync_playwright() as p:
       b = p.chromium.launch(); pg = b.new_page(viewport={'width':1080,'height':1920})
       pg.goto(pathlib.Path('index.html').resolve().as_uri())
       for f in range(total):
           pg.evaluate(f'setPlayhead({f / fps})')       # deterministic seek, no wall clock
           pg.screenshot(path=f'frames/f{f:05d}.png', clip={'x':0,'y':0,'width':1080,'height':1920})
       b.close()
   subprocess.run(['ffmpeg','-y','-framerate',str(fps),'-i','frames/f%05d.png',
                   '-i','vo_full.wav','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',
                   '-c:a','aac','-b:a','256k','-shortest','final.mp4'])
   ```
2. **No automation at all (chat mode)**: deliver the HTML + these human steps:
   - Open `index.html` in a desktop browser at fullscreen, press the play overlay,
     screen-record (OBS / Windows Game Bar / macOS ⌘⇧5) at 1080×1920 or 1:1 crop,
     record system audio; trim with any editor.
   - Optional audio pre-mux (exact VO alignment): build the full VO track first:
     ```bash
     ffmpeg -i vo_S01.mp3 -i vo_S02.mp3 -filter_complex \
       "[0]adelay=0|0[a0];[1]adelay=6500|6500[a1];[a0][a1]amix=inputs=2:normalize=0" \
       vo_full.wav   # repeat per clip with its shot.start ms
     ```
3. If a recording was produced by the human, verify with `ffprobe` and finish the QC gate.

Never let fallback mode produce a non-deterministic wall-clock animation: the playhead
seek function (`setPlayhead`) is mandatory — it is what makes renders reproducible and
QC possible.

---

## F. Blender (bpy) — true-3D path (closest to the reference look)

Reference look = blocky toon-chibi, matte shading, soft key light, shallow DOF. Blender
does this natively and is fully scriptable + headless-renderable.

```bash
blender --version                    # 3.6+/4.x with bundled Python
pip install bpy                      # OR use `blender -b -P script.py` (no pip needed)
```

Recipe:
1. **Build** (`scripts/build_scene.py`, run with `blender -b -P`): construct characters
   from primitives — head = UV sphere scaled round, hair = joined cube facets (shade flat),
   hands = spheres, body = rounded cube, eyes = small flattened spheres, brows = thin
   boxes; arms/hands as separate objects parented to empties (named: `head`, `brow.L/R`,
   `mouth`, `arm.L/R`) so animation is transform-driven. One builder function per character
   (fn(raka), fn(abah)…) — reuse for every part.
2. **Materials**: matte diffuse (roughness 0.7–0.9, no specular gloss); skin/hair palette
   from `references/style-guide.md`; backgrounds same (mint walls, wood, tile).
3. **Set**: 2 locations max; corkboard/sticky-notes/desk as simple textured planes.
4. **Camera & light**: 1080×1920 resolution; area key light (soft, warm) + weak fill +
   world ambient; DOF on, focus = speaker head, f-stop ~2.0 (blurred background bokeh +
   blurred foreground figure for over-shoulder shots).
5. **Animate from timeline.json** — read it in Python; per shot: `scene.frame_start =
   round(start*fps)`, move/rotate the named groups with linear/ease keyframes; push-in =
   keyframe camera distance; mouth-flap = scale-Y oscillation while VO active.
6. **Render** (`blender -b project.blend -P render.py`): EEVEE engine (fast, soft look;
   enable AO + bloom subtle), PNG frame sequence `frames/f#####.png`, then:
   ```bash
   ffmpeg -framerate 30 -i frames/f%05d.png -i vo_full.wav -c:v libx264 -crf 18 \
          -pix_fmt yuv420p -c:a aac -b:a 256k -shortest final.mp4
   ```
7. QC gate (SKILL.md §6) → deliver. Keep the .blend + build script so the next part
   reuses the exact same characters (frozen assets).

Tip for agent workflows: everything is deterministic and file-based (timeline.json →
keyframes → frame sequence), so this path passes the same QC gate as the Node engines.
