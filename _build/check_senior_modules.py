# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from voice_bank_senior_b3a import VOICE_POINTS_S_B3A
from voice_bank_senior_b3b import VOICE_POINTS_S_B3B
from voice_bank_senior_b4a import VOICE_POINTS_S_B4A
from voice_bank_senior_b4b import VOICE_POINTS_S_B4B
from voice_bank_batch3 import BATCH3_POINTS
from voice_bank_batch4 import BATCH4_POINTS

for name, pts in [("b3a", VOICE_POINTS_S_B3A), ("b3b", VOICE_POINTS_S_B3B),
                  ("b4a", VOICE_POINTS_S_B4A), ("b4b", VOICE_POINTS_S_B4B)]:
    ids = [p["id"] for p in pts]
    steps = [len(p["steps"]) for p in pts]
    lens = [len(s[1]) for p in pts for s in p["steps"]]
    print(name, "points", len(pts), "steps_ok", all(x == 3 for x in steps),
          "ids", ids[0], "..", ids[-1], "len", min(lens), max(lens))

print("batch3", len(BATCH3_POINTS), [p["id"] for p in BATCH3_POINTS[:2]], BATCH3_POINTS[-1]["id"])
print("batch4", len(BATCH4_POINTS), [p["id"] for p in BATCH4_POINTS[:2]], BATCH4_POINTS[-1]["id"])

allids = [p["id"] for p in BATCH3_POINTS + BATCH4_POINTS]
assert len(allids) == len(set(allids)) == 103
assert len([i for i in allids if i.startswith("ps-")]) == 103
print("unique", len(allids), "OK")
