# -*- coding: utf-8 -*-
"""用 Edge 无头批量截图 6 个知识点的第 1、3 步，便于目视验收。"""
import subprocess
from pathlib import Path

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ROOT = Path(r"D:\AI\ZCode\physics")
SHOTS = ROOT / "shots"
SHOTS.mkdir(exist_ok=True)

jobs = []
for pid in ["pj-1", "pj-2", "pj-3"]:
    for step in [0, 2]:
        jobs.append((pid, step, "junior"))
for pid in ["ps-1", "ps-2", "ps-3"]:
    for step in [0, 2]:
        jobs.append((pid, step, "senior"))

for pid, step, page in jobs:
    out = SHOTS / f"{pid}-s{step+1}.png"
    url = f"file:///D:/AI/ZCode/physics/{page}.html#{pid}/{step}"
    subprocess.run(
        [
            EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--window-size=900,1500", "--virtual-time-budget=1800",
            f"--screenshot={out}", url,
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
    )
    print(out.name, out.exists(), out.stat().st_size if out.exists() else 0)
