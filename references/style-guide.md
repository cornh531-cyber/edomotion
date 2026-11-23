# Style guide — the reference formula (Kacaurus-style animated story)

Reverse-engineered from the reference video: @kacaurus "Angket Cita-Cita" (bagian terakhir),
TikTok, ~120 s, 9:16, Indonesian first-person narration, #animasi #ceritalucu.
This is a **style** spec — clone the format, never the content (see §9).

---

## 1. Format specs

| Property | Value |
|---|---|
| Canvas | 1080 × 1920 (9:16), 30 fps |
| Duration | 60–120 s per part (parts > full-version cut) |
| Codec | H.264 MP4, CRF 18–20, AAC 256 kbps, −14 LUFS |
| Safe zones | 120 px top, 360 px bottom, 140 px right (TikTok/Reels UI) |
| Captions | ~72% frame height, max 2 lines × ~34 chars |
| Language | Indonesian, first person ("gue"), casual Jakarta/Bandung slang |

## 1.5 Palet terukur (disample langsung dari frame referensi — `style-reference-frame.jpg`)

Nilai di bawah adalah **hasil pengukuran pixel** pada frame asli (scene kelas, siang).
Nilai sudah termasuk grading/vignette lembut channel-nya — saat lighting scene-mu lebih
terang, naikkan brightness ±15–20% dengan hue yang sama.

| Elemen | Hex terukur | Catatan |
|---|---|---|
| Dinding atas (cream/greige) | `#b1ada1` | hangat, sedikit abu |
| Wainscot/band dinding (mint sage) | `#90a298` | mint yang kalem, bukan mint terang |
| Papan gabus | `#a89e7e` | tan |
| Sticky notes (pastel) | `#e7c9a9`–`#d9b48f` area | pink/biru kalem di sekitar nilai ini |
| Tanaman (hijau) | `#487856` | hijau sage gelap |
| Lantai tile | `#abaaa8` | abu terang netral |
| Meja (kayu atas) | `#917359` | kayu hangat medium |
| Meja (kayu depan) | `#775a48` | kayu lebih gelap |
| Rambut | `#30343d` | hitam lembut ke biru-abu (bukan hitam pekat) |
| Kulit | `#a57d63` | tan hangat |
| Kertas/buku | `#bfc0c2` | putih redup oleh cahaya |
| Tas/figur depan (blur) | `#6f4654` | maroon |
| Kursi | `#746f91` area | biru-ungu kalem |
| Tempat pensil | `#454954` | abu gelap |

**Skala proporsi terukur**: pada medium shot, lebar kepala karakter ≈ 45–50% lebar
frame; tinggi kepala+rambut ≈ 3,2× tinggi wajah. Mata oval gelap besar dengan highlight
putih kecil, alis tipis ekspresif, blush pipi lembut.

## 2. Visual language (3D — verified from the reference frame, see style-reference-frame.jpg)

**Characters — blocky 3D toon-chibi (the channel's core look):**
- Rendered 3D (Blender/Three.js look), NOT flat 2D: matte soft shading, gentle studio
  lighting (key + ambient, subtle AO), slight vignette.
- Proportions ~2.5–3 heads tall: oversized rounded head, chunky faceted geometric hair
  (low-poly planes, not strands), big oval eyes + thin expressive brows, soft blush,
  tiny nose/mouth; oversized mitten hands, simple rounded limbs (no elbows/knees detail).
- Signature outfit per character (reference frame: white school uniform w/ small chest
  logo; other family members: office shirt+tie, hoodie, home wear).
- Animate via transforms of named rig groups (head-tilt, brow-raise, mouth-flap,
  arm-swing); blink cycle every 3–4 s; idle breathing sway; exaggerate on punchlines.
- Poses stay symmetrical and simple — the charm is in proportions + expression, not detail.

**Backgrounds — simple 3D sets, max 2 locations per part:**
- Recurring home/school set: wooden desk (the "heart" location), classroom, dining table,
  bedroom, street. Muted cozy palette: pale mint walls (#cfe0d8-ish), cream/beige upper
  walls, warm wood (#c08a4e-ish), terracotta/plant accents, tiled floor.
- Set dressing repeats: corkboard with pastel sticky notes, potted plant, pen holder.
- **Shallow depth of field**: blurred foreground figure for over-shoulder shots, soft
  background bokeh — this is what makes it feel cinematic. Warm cream for day, deep
  blue/purple for night, desaturated for flashback.

**Camera (virtual, code-driven):**
- Default: static medium shot per beat; over-shoulder framing with a blurred near figure
  for dialogue.
- Emotional beat (5–6): slow push-in, 4–6 s, ~6% dolly/scale.
- Reveal gag: 2-frame shake or 1.05× pop.
- Time skip: 250 ms fade; scene cut: hard cut (whip only for the turn).

**Continuity rule**: the payoff object (beat 6) must appear planted in beat 2 — same
model/shape, same location in frame.

## 3. The 7-beat structure (with the reference as worked example)

| # | Beat | Sec | Reference moment (style illustration, not copyable text) |
|---|---|---|---|
| 1 | Cold-open hook | 0–6 | Paradox line: "the 4th questionnaire was mine, two years ago" + title card |
| 2 | Context | 6–25 | What the narrator wrote on the questionnaire and why (family planted: dad's job funds everything) |
| 3 | Turn | 25–45 | The belief breaks (dad laid off) + visual gag: necktie morphs → bear head → cooking apron |
| 4 | Rhythm montage | 45–65 | Parallel "everything stayed the same" shots (sister still in college, mom still in her club, house never lacking) |
| 5 | Realization | 65–80 | Quiet push-in: "I only ever copied the tie — without it I can't picture myself" → blank silhouette |
| 6 | Payoff | 80–105 | Letter on the dining table → dad reads → wallet close-up → short dialogue → laugh |
| 7 | Outro | 105–120 | Warm final line ("the image is still blank — but dad is staring off beside me"), part card, hashtags |

**Blank-image device**: when the narrator "can't picture himself", show a literal empty
outline/silhouette — abstract metaphors drawn literally is the channel's signature move.
Use devices like this: draw the metaphor.

**Humor placement**: one visual gag in beat 3, one deadpan dialogue joke in beat 6. Sadness
and jokes alternate; never two gags in a row.

## 4. Narration & dialogue

- Narrator: teen voice, warm, wry, slightly tired — conversational, not "announcer".
- Rate 2.2–3.2 words/s; sentences ≤ 14 words; one idea per sentence.
- Dialogue lines are short (≤ 8 words), quoted, with the character on screen.
- Slang register: "gue/abah/mamah", contractions ("udah", "nggak", "bikin") — natural
  spoken Indonesian, never formal ("saya", "adalah").
- Emotional payoff = understatement ("Nah, itu udah kayak Abah banget.") — no melodrama.

## 5. Captions

- Rounded sans (Baloo 2 → Poppins → system-ui fallback), white, 48–56 px, 3–4 px dark
  stroke or 60% black rounded pill.
- Compress VO to ≤ 2 × 34 chars; keep slang exactly as spoken.
- Appear with the VO word, leave at shot end; never stack two captions.

## 6. Audio

- Music: one lofi/piano bed for the whole part, ducked −6 dB under VO; silence 0.5 s
  before the beat-5 reveal; 3 s tail after outro line.
- SFX set (small): paper rustle, chair scrape, door, clock tick, footsteps, whoosh.
- VO per-shot files `vo_S01.mp3`… so captions and timing stay mechanical.

## 7. Serialization model (from the reference channel)

- One story arc split into parts; each part self-contained but ends on a hook.
- Part card in outro: "Bagian X dari Y" / "Bagian terakhir".
- Cadence: parts released in sequence, "full version" cut after the last part.
- Characters, palette, locations, fonts are **frozen assets** reused across parts — this is
  what makes the channel recognizable; enforce via the asset files in §4 of SKILL.md.

## 8. Thumbnail

- Frame at ~3 s (hook peak), title text ≥ 120 px, character face + hook object.
- High contrast against the palette; no UI-zone text.

## 9. Do-not-copy (ethics/law)

The reference is a format spec only. Never reproduce: the actual story text/transcript,
dialogue, voice tracks, character designs, logo/name, or channel branding of the reference.
All stories, characters and lines must be original works in the same format.
