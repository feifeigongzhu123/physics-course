# -*- coding: utf-8 -*-
from pathlib import Path
root = Path(r"D:\AI\ZCode\physics\audio")
fs = sorted(root.glob("pj-*/step*.mp3"))
print("files", len(fs), "MB", round(sum(f.stat().st_size for f in fs) / 1048576, 1))
low = high = 0
for f in fs:
    n = int(f.parent.name.split("-")[1])
    if n <= 20:
        low += f.stat().st_size
    else:
        high += f.stat().st_size
print("pj-1..20", round(low / 1048576, 1), "pj-21..51", round(high / 1048576, 1))
