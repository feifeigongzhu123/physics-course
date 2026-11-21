# -*- coding: utf-8 -*-
import json, re, subprocess, sys, io
from pathlib import Path
import imageio_ffmpeg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = Path(r"D:\AI\ZCode\physics")
name = sys.argv[1] if len(sys.argv) > 1 else "voice_bank_junior.json"
data = json.loads((root / "data" / name).read_text(encoding="utf-8"))
ff = imageio_ffmpeg.get_ffmpeg_exe()


def dur(p):
    r = subprocess.run([ff, "-hide_banner", "-i", str(p)], capture_output=True, text=True, errors="replace")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", r.stderr)
    return round(int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3)), 1) if m else 0


durs = []
size = 0
for p in data:
    ds = []
    for i in range(1, len(p["steps"]) + 1):
        f = root / "audio" / p["id"] / f"step{i}.mp3"
        assert f.exists() and f.stat().st_size > 1000, f
        d = dur(f)
        ds.append(d)
        durs.append(d)
        size += f.stat().st_size
    print(p["id"], p["name"], ds)
print("points", len(data), "clips", len(durs), "total_s", sum(durs), "MB", round(size/1048576, 1))
print("min", min(durs), "max", max(durs), "avg", round(sum(durs)/len(durs), 1))
