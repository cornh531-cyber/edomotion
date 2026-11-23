<div align="center">

# 🎬 STORY MOTION VIDEO

**Skill universal pembuat video animasi cerita 9:16 — dikloning persis dari gaya
channel animasi TikTok (@kacaurus · "Angket Cita-Cita")**

*Karakter 3D blocky toon-chibi · Narasi "gue" · Caption · Musik lofi · Cerita berseri*

`v1.1.0` · `License: MIT` · `Format: SKILL.md (agentskills.io)` · `Bahasa: ID + EN`

---

**Dari brief → video MP4 siap upload TikTok / Reels / Shorts.**

Dijalankan oleh **AI apa pun** · Di-build di **platform motion apa pun**

</div>

---

## 📦 Isi paket

```
story-motion-video/
├── SKILL.md                          ← jantung skill: kontrak 7 fase + QC gate
├── README.md                         ← file ini
├── LICENSE                           ← MIT
├── references/
│   ├── style-guide.md                ← spesifikasi gaya presisi (palet TERUKUR dari frame asli!)
│   ├── style-reference-frame.jpg     ← frame ground-truth dari video referensi
│   ├── engine-adapters.md            ← resep per platform (6 engine)
│   └── instant-prompt.md             ← full prompt copy-paste untuk AI chat
├── scripts/
│   └── check_timeline.py             ← validator timing (QC gate otomatis)
└── examples/
    └── timeline.example.json         ← contoh timeline 16 shot yang PASS validator
```

## ✨ Kenapa skill ini beda

| | Skill biasa | Skill ini |
|---|---|---|
| Gaya referensi | deskripsi vagu | 🎯 **palet hex di-sample dari pixel frame asli** + rasio proporsi terukur |
| Platform | 1 engine | 🧩 **6 jalur**: Blender · OpenMotion · HyperFrames · Remotion · Motion Canvas · fallback HTML |
| Model AI | sering vendor-lock | 🌐 **murni Markdown** — jalan di semua LLM besar |
| Timing | "kira-kira" | 📐 `timeline.json` angka pasti + validator otomatis |
| Selesai | AI mengaku done | ✅ **QC gate wajib bukti** (ffprobe, tabel PASS/FAIL) |
| Seri | per-video | 🔁 **frozen assets** — part 2, 3, 4… konsisten karakter & tempo |

## 🎯 Kecocokan dengan video referensi (yang dikloning)

| Aspek | Spec di skill ini |
|---|---|
| Karakter | 3D blocky toon-chibi 2,5–3 kepala; kepala ≈ 45–50% lebar frame; rambut facet low-poly; tangan mitten jumbo |
| Warna | 14 warna terukur langsung dari frame: dinding `#b1ada1`, mint `#90a298`, kayu `#917359`/`#775a48`, kulit `#a57d63`, rambut `#30343d`, dst. |
| Cahaya | matte + key light hangat + AO tipis + vignette ringan |
| Kamera | medium shot statis · over-shoulder ber-DOF (f/2.0) · push-in 1→1.06 di beat emosi |
| Cerita | struktur 7 beat persis channel: Hook paradoks → Konteks (tanam objek) → Turn + gag → Montase → Realisasi (metafora harfiah) → Payoff → Outro |
| Bahasa | narasi orang pertama "gue/abah/mamah", slang natural, 2,2–3,2 kata/detik |
| Seri | kartu "Bagian X dari Y" + cadence 3 slot release + full-version cut |

> ⚖️ **Etika**: yang dikloning 100% adalah *format & gaya* (hal yang tidak dilindungi hak
> cipta). Cerita, dialog, audio, dan desain karakter spesifik channel referensi TIDAK
> disalin — semua konten yang dihasilkan skill ini orisinal. Lihat style-guide §9.

## 🚀 Quickstart

### Jalur A — Agen koding (Claude Code, Codex, Cursor, Gemini CLI, Qwen Code, dll.)

```bash
# 1. Pasang skill (pilih salah satu)
npx skills add <repo-kamu>/story-motion-video
cp -r story-motion-video ~/.claude/skills/        # cara manual Claude Code

# 2. Suruh agent-nya
```
> "Gunakan skill story-motion-video: buat Bagian 1 dari brief ini: [ceritamu]"
```

Skill otomatis mendeteksi engine terbaik yang terpasang (Blender → OpenMotion →
HyperFrames → Remotion) dan mengeksekusi sampai MP4 + tabel QC PASS.

### Jalur B — AI chat (GPT, Gemini web, DeepSeek, Qwen, GLM, Kimi, Grok, MiniMax, dll.)

Salin full prompt dari **`references/instant-prompt.md`** → isi `[BRIEF-KU]` → tempel.
Hasil: file HTML animasi 9:16 siap buka di browser + langkah render/rekam layar.

### Jalur C — Sudah punya OpenMotion / HyperFrames?

Tidak perlu install apa pun — skill mendeteksi dan langsung memakai adapter-nya
(Motion.md untuk OpenMotion, `data-*` + GSAP untuk HyperFrames).

## 🛠 Matriks engine

| Engine | Kecepatan setup | Kemiripan 3D w/ referensi | Catatan |
|---|---|---|---|
| **Blender (bpy)** | ⚙️ sedang | ⭐⭐⭐⭐⭐ paling persis | primitif → EEVEE → ffmpeg |
| **OpenMotion** | ⚙️ sedang | ⭐⭐⭐⭐ | Studio editor + Motion.md, recreasi referensi |
| **HyperFrames** | ⚡ cepat | ⭐⭐⭐⭐ (Three.js) | deterministik, lint→render |
| **Remotion** | ⚡ cepat | ⭐⭐⭐⭐ (@remotion/three) | React + spring/interpolate |
| **Motion Canvas** | ⚡ cepat | ⭐⭐⭐ | TS scene generator |
| **HTML fallback** | 🚀 instan | ⭐⭐⭐ (Three.js lokal) / ⭐⭐ pseudo-2.5D | tanpa install apa pun |

## 🤖 Dukungan model

Murni Markdown + JSON + Python-stdlib → **tanpa API/fitur vendor tertentu**.
Diuji secara desain pada: Claude · GPT · Gemini · Qwen · DeepSeek · Grok · GLM · Kimi ·
MiniMax · Llama · Hunyuan · Step · Nemotron · Mimo · Muse · dan LLM lain.
AI tanpa tool file/shell tetap selesai lewat jalur HTML fallback (aturan degradasi di SKILL.md §0.4).

## ✅ QC gate (6 langkah, wajib PASS)

```bash
python3 scripts/check_timeline.py timeline.json     # rate 2,2–3,2 wps · hook ≤3,5s · gap ≤1,5s
ffprobe -v error -show_entries format=duration -of csv=p=0 final.mp4   # ±1,5s dari plan
```
+ frame math · sinkron caption ±150 ms · zona aman 120/360/140 px · style check 3D ·
konten orisinal. Semua dicetak sebagai **tabel PASS/FAIL** — AI dilarang bilang "selesai"
tanpa bukti.

## 📁 Output per part

```
output/part1/
├── final.mp4        ← 1080×1920 · 30fps · H.264 CRF18 · AAC 256k
├── captions.srt     ← dari timeline (bantu auto-caption platform)
├── thumb.png        ← frame hook + judul besar
├── Motion.md        ← arahan kreatif (dipakai ulang part berikutnya)
└── timeline.json    ← sumber kebenaran timing
```

## ❓ FAQ

**Bisa jalan tanpa internet?** Ya — semua jalur lokal; fallback HTML tanpa CDN.
**Kok bukan AI video generator (Veo/Sora)?** Skill ini membuat AI *memprogram* video
(OpenMotion/HyperFrames/Remotion/Blender) — hasilnya deterministik, bisa diedit ulang
per shot, dan gratis tanpa quota generator.
**Ganti gaya?** Edit `references/style-guide.md` (palet, proporsi) — sisa pipeline sama.
**Tambah part?** Jalankan lagi dengan brief part berikutnya; karakter/palet/tempo FROZEN.

---

<div align="center">

**MIT License** · Referensi gaya: video publik @kacaurus (analisis format, bukan penyalinan konten)
*Dibuat dengan 🦖 energy — "Walaupun kacau, pasti kita urus."*

</div>
