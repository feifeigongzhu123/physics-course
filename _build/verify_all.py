# -*- coding: utf-8 -*-
import json, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = Path(r"D:\AI\ZCode\physics")
ids = {}
for name in ["voice_bank_junior.json", "voice_bank_batch2.json", "voice_bank_batch3.json", "voice_bank_batch4.json"]:
    data = json.loads((root / "data" / name).read_text(encoding="utf-8"))
    for p in data:
        ids.setdefault(p["id"], []).append(name)
for grade in ("junior", "senior"):
    data = json.loads((root / "data" / f"{grade}.json").read_text(encoding="utf-8"))
    for p in data:
        if p["id"] not in ids:
            ids[p["id"]] = ["course"]
print("unique points with narration", len(ids), "dupes", [k for k, v in ids.items() if len(v) > 1])
missing = []
for pid in ids:
    for i in (1, 2, 3):
        f = root / "audio" / pid / f"step{i}.mp3"
        if not f.exists() or f.stat().st_size < 1000:
            missing.append((pid, i))
print("missing clips", missing)
files = list((root / "audio").glob("*/step*.mp3"))
print("clips", len(files), "MB", round(sum(f.stat().st_size for f in files) / 1048576, 1))
pj = [f for f in files if f.parent.name.startswith("pj-")]
ps = [f for f in files if f.parent.name.startswith("ps-")]
print("junior clips", len(pj), "senior clips", len(ps))
print("junior points", len({f.parent.name for f in pj}), "senior points", len({f.parent.name for f in ps}))
