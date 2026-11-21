# -*- coding: utf-8 -*-
import json, re, subprocess, sys, io
from pathlib import Path

import imageio_ffmpeg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
root = Path(r"D:\AI\ZCode\physics")


def duration(path: Path) -> float:
    p = subprocess.run([FFMPEG, "-hide_banner", "-i", str(path)],
                       capture_output=True, text=True, errors="replace")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", p.stderr)
    if not m:
        return 0.0
    h, mi, s = m.groups()
    return round(int(h) * 3600 + int(mi) * 60 + float(s), 1)


total = 0
for grade in ("junior", "senior"):
    data = json.loads((root / "data" / f"{grade}.json").read_text(encoding="utf-8"))
    print(grade, "points", len(data))
    for p in data:
        durs = []
        for i, s in enumerate(p["steps"], 1):
            mp3 = root / "audio" / p["id"] / f"step{i}.mp3"
            durs.append(duration(mp3))
            total += mp3.stat().st_size
        print(" ", p["id"], p["name"], "mp3", durs, "questions", len(p["questions"]))
print("audio total MB", round(total / 1048576, 1))
print("files", len(list((root / "audio").rglob("*.mp3"))))
