---
name: story-motion-video
description: >
  Create vertical (9:16) narrative motion videos — 3D toon-chibi animated short stories
  (blocky characters, soft studio lighting, shallow depth of field) with voiceover,
  captions and serialized structure, in the style of viral TikTok animation
  channels (reference: Kacaurus "Angket Cita-Cita"). Engine-agnostic: builds with whichever
  motion platform is available — OpenMotion, HyperFrames, Remotion, Motion Canvas, or a
  zero-dependency single-file HTML fallback. Model-agnostic: written so ANY AI agent or chat
  model can execute it (Claude, GPT, Gemini, Qwen, DeepSeek, Grok, GLM, Kimi, MiniMax, Llama,
  Hunyuan, Step, Nemotron, Mimo, Muse, and others), with a degraded-but-working path when
  tools are missing. Use when the user asks for an "animated story video", "video motion
  seperti TikTok animasi", "recreate this animation style", "motion graphics story", or wants
  an MP4 for TikTok / Reels / Shorts from a story brief.
license: MIT
metadata:
  version: 1.0.0
  reference-style: "Kacaurus-style animated story (Indonesian, 9:16, narration-driven)"
  engines: openmotion, hyperframes, remotion, motion-canvas, blender-bpy, html-fallback
  languages: any (story content), English (code/comments)
---

# Story Motion Video — universal skill for animated short-story videos

Produce a vertical animated story video that reads like the reference: a first-person,
narration-driven 3D animation (voiceover + captions + blocky toon-chibi characters) serialized into parts,
exported as MP4 for TikTok/Reels/Shorts.

This skill is a **contract**: it must complete on any AI system. It adapts to whatever engine
and tools exist, and always degrades gracefully instead of stopping.

---

## 0. Non-negotiable rules (apply on every model, every engine)

1. **Style first.** Every deliverable must read as "animated short-story": VO narration,
   on-screen captions, blocky 3D toon-chibi characters (soft light, shallow DOF), warm
   slice-of-life mood, serialized parts. Full style spec: `references/style-guide.md` +
   `references/style-reference-frame.jpg`.
2. **Deterministic timing.** Never animate "roughly". Every shot has numeric `start`/`end`
   seconds in a written shot table before any code is produced. All animation is driven by
   that table (frame math, not vibes).
3. **Measure, then deliver.** Never claim a render you did not run. Never deliver before the
   QC gate (§6) passes. If you cannot render, say exactly what the human must run.
4. **Always a fallback.** Missing engine? Downgrade one level (§1 table) and continue.
   Chat-only model? Use the single-file HTML fallback. Stopping is not allowed.
5. **Style is cloned, content is not.** Recreate the *format* (structure, pacing, visual
   language). Never copy the reference channel's actual story text, audio, logo, or
   characters verbatim — write original stories in the same format.
6. **Language split.** Story content: the user's language (default Indonesian).
   Code, filenames, comments: English.

---

## 1. Detect environment → pick the engine

Check, in order, what is available. Announce your choice in one line.

| Condition | Engine | Entry point |
|---|---|---|
| Blender available or installable, true-3D desired | **blender-bpy** | adapter §F (`python3 scripts/build_scene.py && blender -b -P render.py`) |
| OpenMotion skill/MCP installed or installable | **openmotion** | `npx skills add nexu-io/openmotion --skill openmotion` |
| HyperFrames installed or installable | **hyperframes** | `npx skills add heygen-com/hyperframes` then `npx hyperframes init` |
| Node.js + npm present, no engine yet | **remotion** (or motion-canvas) | `npm create video@latest` |
| Only Python/ffmpeg, no Node | **html-fallback** | single-file HTML + frame capture |
| Chat-only (no shell, no files) | **html-fallback (chat mode)** | output one self-contained HTML file + instructions |

Detailed procedures per engine: `references/engine-adapters.md`. Read the section for the
chosen engine **before** writing code. All engines implement the same `Motion.md` shot table
(§3), so switching engines later only changes the build step, not the plan.

---

## 2. Phase 1 — Story brief

Fill this with the user (ask only for missing fields; invent the rest and show it for a
quick yes/no). Save as `story-brief.md`.

```
TITLE:            (e.g. "Angket Cita-Cita — Bagian 1")
LOGLINE:          one sentence, first person
CHARACTERS:       name / age / look (hair, outfit, 2 props) / voice note  [2–5 chars]
SETTING:          primary location + secondary (keep ≤2 locations per part)
MOOD:             comedy-with-heart default; pick: funny / sad-warm / tense / hopeful
MORAL / PAYOFF:   the emotional line the ending lands on
SERIALIZATION:    total parts, what each part covers, cliffhanger per part
HASHTAGS:         3–5 tags
LANGUAGE:         default id (Indonesian), first-person "gue" narration
```

**Story formula (7 beats).** Map the brief onto these beats — timings for a 100–120 s part;
scale proportionally for 60–90 s:

1. **Cold-open hook (0–6 s)** — a paradox/mystery line in first person + title card.
   The hook must be speakable in ≤ 3.5 s and create one question the viewer wants answered.
2. **Context (6–25 s)** — who, where, what the narrator believed/ wanted.
3. **Turn (25–45 s)** — the event that breaks the belief; land a **visual gag** here.
4. **Rhythm montage (45–65 s)** — 3+ parallel shots with repeated sentence structure.
5. **Realization (65–80 s)** — quiet beat, slow push-in, narrator's decision.
6. **Payoff (80–105 s)** — short dialogue exchange + one close-up of a small physical
   object (letter, wallet, phone). This object was planted in beat 2.
7. **Outro (105–120 s)** — warm final line, part card ("Bagian X dari Y" / "Bagian
   terakhir"), hashtags, 3 s of music tail.

Rule: plant in beat 2 what pays off in beat 6. One plant minimum per part.

---

## 3. Phase 2 — Motion plan (`Motion.md` + `timeline.json`)

Write **both** files at the project root before building anything.

**`Motion.md`** — the creative direction (engines like OpenMotion read this directly):

```markdown
# Motion.md — <TITLE>
## Format
1080x1920 (9:16), 30 fps, target 110 s, H.264 MP4. Language: id. 1 of N parts.
## Style kit
Palette: [scene-mood → 5 hex colors]. Fonts: rounded sans (Baloo 2 / Poppins fallback).
Characters: link to asset list. Camera: mostly static mids; push-in on beats 5–6.
## Shot list
| id  | start | end | shot (visual)                  | camera      | VO                          | caption                       | sfx       |
| S01 | 0.0   | 6.0 | ...                            | static      | "...hook line..."           | "...hook line (short)..."     | paper     |
| ... |
## Audio cues
Music: lofi piano bed, duck -6 dB under VO. VO clips: vo_S01.mp3 ... 
## Assets
characters/*.svg, backgrounds/*.svg, vo/*.mp3, music.mp3, sfx/*.mp3
```

**`timeline.json`** — the machine-readable timing table (one object per shot):

```json
{
  "fps": 30, "width": 1080, "height": 1920,
  "shots": [
    {"id": "S01", "start": 0.0, "end": 6.0, "type": "hook",
     "vo": "Ternyata angket keempat itu dari gue sendiri, dua tahun lalu.",
     "caption": "Angket keempat itu... punya gue sendiri.", "sfx": "paper"}
  ],
  "audio": {"voiceover": "vo/", "music": "assets/music.mp3", "music_duck_db": -6}
}
```

**Timing laws** (validate with `python3 scripts/check_timeline.py timeline.json`):
- Speech rate 2.2–3.2 words/second per shot (Indonesian narration).
- Shot length 3–7 s (montage beats may drop to 2 s).
- Hook VO ≤ 3.5 s. No silent gap > 1.5 s except 0.5 s before beat-5 reveal.
- Total duration = plan ± 0 ; the table is the source of truth.
- Captions ≤ 2 lines × ~34 chars, verbatim from the VO but compressed.

---

## 4. Phase 3 — Assets

**Characters (primary path — code-drawn SVG).** Flat 2D vector characters as SVG or CSS
shapes: semi-chibi proportions (~3.5 heads tall), big expressive eyes/brows, simple outfits
with one signature prop per character. Draw each character once as a reusable symbol with
named parts (head, eyes, brows, mouth, arms) so poses/mouth-flaps are transforms, not
redraws. Consistency beats detail — this is the reference channel's core look.

**Characters (optional path — AI image gen).** If an image tool exists: generate a
character sheet (turnaround, 3 expressions) per character first, lock the style string, then
scene backgrounds. Store prompts in `assets/prompts.md` so every regeneration matches.
Never mix both paths inside one part.

**Voiceover.** Priority order:
1. Agent-native TTS if the runtime offers it → render per-shot clips `vo/vo_S01.mp3`…,
   teen-male warm/wry narrator; pitch-shift ±15% and ±10% speed for other characters.
2. Local TTS: `edge-tts --voice id-ID-ArdiNeural --text "..." --write-media vo_S01.mp3`
   (or any id-ID voice; Abah-type characters: rate="-10%", pitch="-20Hz").
3. No TTS at all → build the video with captions + music only and tell the user to record
   VO over the silent render (the timeline already matches).

**Music & SFX.** One instrumental bed (lofi/piano) for the whole part; keep SFX set small:
paper, chair, door, clock, footsteps, whoosh. If no SFX assets exist, skip SFX — never
synthesize fake assets that don't exist.

**Captions.** Derived from the shot table: white rounded sans, 48–56 px, ≤2 lines, centered
at ~72% frame height (safe zone: 120 px top, 360 px bottom of 1920 px are UI-risk areas).

---

## 5. Phase 4 — Build with the chosen engine

Read the matching section of `references/engine-adapters.md`, then build. Quick reference:

- **OpenMotion** — install the skill, let it scaffold, keep `Motion.md` as the direction
  doc, build the HTML source, adjust timing in Studio, export MP4. Ideal for reference-video
  recreation (`motion-recreate`) and Studio-based editing.
- **HyperFrames** — `npx hyperframes init`; one `index.html` composition: HTML elements +
  `data-*` timing attributes + GSAP timeline; then `lint → inspect → preview → render
  --quality high --output final.mp4`. Deterministic frame-seek rendering via headless Chrome
  + FFmpeg.
- **Remotion** — React + TS: `<Composition id="Story" width={1080} height={1920} fps={30}
  durationInFrames={...}>`; one `<Sequence>` per shot from the timeline; animate with
  `useCurrentFrame()` + `interpolate()` + `spring()`; `<Audio src={staticFile(...)}>` per VO
  clip inside its `<Sequence from={frame}>`; QC frame math before render; `npx remotion
  render Story out/final.mp4`.
- **Motion Canvas** — TS scene generators (`yield* waitFor(s)`), one scene per beat,
  `npm run render`.
- **html-fallback** — one self-contained `index.html`: fixed 1080×1920 stage scaled to
  viewport, declarative shot array in JS, CSS keyframes/WAAPI keyed to the timeline, audio
  elements fired at shot starts behind a click-to-play overlay. Render with Playwright
  frame capture + FFmpeg, or hand off for screen recording (full recipe in the adapter doc).

Whatever the engine: code must be boring and mechanical — one scene/section per shot id
(`S01`, `S02`…), constants imported from the same numbers as `timeline.json`. No improvised
durations in code. If code and timeline disagree, the timeline wins.

---

## 6. Phase 5 — QC gate (all must pass before delivery)

Run in order; fix and re-run until clean:

1. `python3 scripts/check_timeline.py timeline.json` → PASS (rate, gaps, hook, total).
2. **Frame math** (Remotion/HyperFrames/Motion Canvas): computed `durationInFrames` /
   composition length == `round(total_seconds × fps)`. Show the number.
3. **Render exists**: `ffprobe -v error -show_entries format=duration -of csv=p=0 final.mp4`
   → within ±1.5 s of plan. (Fallback mode: HTML runs end-to-end in a browser without
   console errors; state this explicitly instead of pretending.)
4. **Subtitle sync**: each caption's visible window within ±150 ms of its VO clip window.
5. **Safe zones**: no text/critical visual inside 120 px top / 360 px bottom / 140 px right.
6. **Audio levels**: VO clear, music ducked ≈ -6 dB under VO, master ≈ -14 LUFS.
7. **Style check**: blocky 3D toon-chibi characters w/ soft light + DOF, ≤2 locations,
   hook readable at 3 s, payoff object visible, part card + hashtags in outro.
8. **Content check**: nothing copied verbatim from the reference channel.

Print the QC table with PASS/FAIL per row. No SKIP allowed — degrade the plan instead.

---

## 7. Phase 6 — Deliver & serialize

Deliverables, in a folder named after the part (e.g. `output/part1/`):

- `final.mp4` — H.264, 1080×1920, 30 fps, CRF 18–20 (or ~12 Mbps), AAC 192–256 kbps.
- `captions.srt` — from the shot table (helps platform auto-captioning & accessibility).
- `thumb.png` — hook frame (≈3 s) with the title text large.
- `Motion.md`, `timeline.json`, `story-brief.md` — kept so the next part reuses characters,
  palette and pacing (serialization = same files, new beats).
- Metadata block: title, part tag ("Bagian X" / "Bagian terakhir"), hashtags, first comment
  teaser suggestion.

Cadence guidance (from the reference channel's model): split one story into short parts,
release them in sequence, and a "full version" cut when the parts finish.

---

## Red flags — stop and re-read the skill if you catch yourself

- Writing prose *about* the video instead of producing `Motion.md` / `timeline.json` / files.
- Animating without numeric start/end times, or inventing durations inside code.
- Saying "done" with no rendered file (or, in fallback mode, no verified HTML).
- 16:9 layout, 24 fps drift, captions inside bottom 360 px.
- Copying the reference channel's story text, audio, or characters 1:1.
- Installing a heavy engine when the fallback would finish the job faster.

## Verification (evidence to include in your final answer)

1. Timeline validator output line: `PASS: N shots, X s total, avg Y wps`.
2. Rendered file path + ffprobe duration (or explicit fallback instructions + verified HTML).
3. QC table from §6 with every row PASS.
4. One-paragraph "what to review first" for the human.

## Files in this skill

- `references/style-guide.md` — the reverse-engineered reference style: beats, visual
  language (3D toon-chibi spec), VO direction, caption rules, example beat sheet.
- `references/style-reference-frame.jpg` — actual frame from the reference video; the
  visual ground truth for character proportions, lighting and palette.
- `references/engine-adapters.md` — full procedures for OpenMotion, HyperFrames, Remotion,
  Motion Canvas, and the html-fallback (incl. render commands and audio muxing).
- `references/instant-prompt.md` — single copy-paste prompt for chat-only models.
- `scripts/check_timeline.py` — timing validator used by the QC gate.
- `examples/timeline.example.json` — a passing 16-shot / 90 s timeline demonstrating the
  7-beat formula (run the validator on it as a smoke test).
