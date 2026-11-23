# -*- coding: utf-8 -*-
import json, re, sys
from pathlib import Path

ROOT = Path(r"D:\AI\ZCode\physics")
BUILD = ROOT / "_build"
allq = []
for name in ["real_questions_a.json", "real_questions_b.json", "real_questions_c.json",
             "real_questions_d.json", "real_questions_e.json"]:
    data = json.loads((BUILD / name).read_text(encoding="utf-8"))
    allq.extend(data)
    print(name, len(data))
ids = [q["id"] for q in allq]
assert len(ids) == len(set(ids)) == 50, (len(ids), len(set(ids)))
missing = [q["image"] for q in allq if q.get("image") and not (ROOT / q["image"]).exists()]
print("missing images", missing)
print("with image", sum(1 for q in allq if q.get("image")))
(ROOT / "data" / "real_questions.json").write_text(json.dumps(allq, ensure_ascii=False, indent=1), encoding="utf-8")
print("merged 50")
