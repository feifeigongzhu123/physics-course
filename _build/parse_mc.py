# -*- coding: utf-8 -*-
import re, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
root = Path(r"D:\AI\ZCode\physics\_build\exam_text")
for f in sorted(root.glob("*.txt")):
    t = f.read_text(encoding="utf-8")
    m = re.search(r"一、选择题(.*?)(?=\n\s*二、|\Z)", t, re.S)
    if not m:
        print("NO MC", f.name); continue
    body = m.group(1)
    parts = re.split(r"\n\s*(\d{1,2})\.\s", "\n" + body)
    print("=====", f.name, "parts", len(parts)//2)
    for i in range(1, len(parts), 2):
        num = parts[i]; block = parts[i+1]
        ans = re.search(r"【答案】\s*([A-D]+)", block)
        if not ans:
            continue
        stem = block.split("\nA.", 1)[0].strip().replace("\n", " ")
        opts = re.findall(r"\n\s*([A-D])\.\s*(.*?)(?=\n\s*[A-D]\.|\n\s*【答案】)", block, re.S)
        print(f"Q{num} ans={ans.group(1)} stem={stem[:90]}")
        for k, v in opts:
            print("  ", k, re.sub(r"\s+", " ", v).strip()[:100])
