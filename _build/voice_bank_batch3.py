# -*- coding: utf-8 -*-
"""第三批 52 个知识点：ps-22 ～ ps-73。"""
from voice_bank_senior_b3a import VOICE_POINTS_S_B3A
from voice_bank_senior_b3b import VOICE_POINTS_S_B3B

ORDER = [f"ps-{i}" for i in range(22, 74)]
_MAP = {}
for p in list(VOICE_POINTS_S_B3A) + list(VOICE_POINTS_S_B3B):
    _MAP[p["id"]] = {
        "id": p["id"], "unit": p["unit"], "name": p["name"],
        "steps": [{"label": s[0], "narration": s[1]} for s in p["steps"]],
    }
BATCH3_POINTS = [_MAP[i] for i in ORDER]
assert len(BATCH3_POINTS) == 52
assert all(len(p["steps"]) == 3 for p in BATCH3_POINTS)
