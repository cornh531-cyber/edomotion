#!/usr/bin/env python3
"""Timeline validator for story-motion-video (QC gate step 1).

Usage:  python3 scripts/check_timeline.py path/to/timeline.json
Checks: schema, monotonic non-overlapping shots, speech rate 2.2-3.2 wps,
        hook <= 3.5 s, silent gaps <= 1.5 s, total duration bounds, caption length.
Exit 0 = PASS, exit 1 = FAIL. Prints one PASS/FAIL summary line.
"""
import json, re, sys

RATE_MIN, RATE_MAX = 2.2, 3.2
HOOK_MAX = 3.5
GAP_MAX = 1.5
TOTAL_MIN, TOTAL_MAX = 45.0, 180.0
CAPTION_LINE, CAPTION_LINES = 34, 2


def words(s: str) -> int:
    return len(re.findall(r"\S+", s or ""))


def main(path: str) -> int:
    problems, warnings = [], []
    try:
        tl = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print(f"FAIL: cannot read {path}: {e}")
        return 1

    shots = tl.get("shots") or []
    if not shots:
        problems.append("no shots[]")
    fps = tl.get("fps", 30)
    if fps not in (24, 25, 30, 60):
        warnings.append(f"unusual fps={fps}")
    if (tl.get("width"), tl.get("height")) != (1080, 1920):
        problems.append(f"canvas must be 1080x1920, got {tl.get('width')}x{tl.get('height')}")

    prev_end = 0.0
    for i, s in enumerate(shots):
        sid = s.get("id", f"#{i}")
        try:
            start, end = float(s["start"]), float(s["end"])
        except Exception:
            problems.append(f"{sid}: missing/invalid start/end")
            continue
        if end <= start:
            problems.append(f"{sid}: end {end} <= start {start}")
            continue
        if start < prev_end - 0.05:
            problems.append(f"{sid}: overlaps previous shot (starts {start} < {prev_end})")
        gap = start - prev_end
        if gap > GAP_MAX:
            problems.append(f"{sid}: {gap:.1f}s silent gap before shot (max {GAP_MAX}s)")
        prev_end = max(prev_end, end)

        dur = end - start
        wps = words(s.get("vo", "")) / dur if dur else 0
        if not (RATE_MIN <= wps <= RATE_MAX):
            problems.append(f"{sid}: speech rate {wps:.2f} wps outside {RATE_MIN}-{RATE_MAX}")
        cap = s.get("caption", "") or ""
        lines = [ln for ln in cap.split("\n") if ln]
        if len(lines) > CAPTION_LINES or any(len(ln) > CAPTION_LINE for ln in lines):
            warnings.append(f"{sid}: caption >{CAPTION_LINES}x{CAPTION_LINE} chars (treat as guidance)")
        if s.get("type") == "hook" and i != 0:
            warnings.append(f"{sid}: 'hook' type on non-first shot")
        if not s.get("vo") and not s.get("caption"):
            problems.append(f"{sid}: shot has neither vo nor caption")

    first = shots[0] if shots else {}
    hook_dur = float(first.get("end", 0)) - float(first.get("start", 0))
    if hook_dur > HOOK_MAX:
        problems.append(f"hook shot is {hook_dur:.1f}s (max {HOOK_MAX}s)")

    total = float(shots[-1]["end"]) if shots else 0.0
    if not (TOTAL_MIN <= total <= TOTAL_MAX):
        problems.append(f"total duration {total:.1f}s outside {TOTAL_MIN}-{TOTAL_MAX}s")

    ok = not problems
    print(f"{'PASS' if ok else 'FAIL'}: {len(shots)} shots, {total:.1f}s total, "
          f"fps={fps}, hook={hook_dur:.1f}s")
    for p in problems:
        print(f"  [FAIL] {p}")
    for w in warnings:
        print(f"  [warn] {w}")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
