# -*- coding: utf-8 -*-
"""第四批 51 个知识点：ps-74 ～ ps-124。"""
from voice_bank_senior_b4a import VOICE_POINTS_S_B4A
from voice_bank_senior_b4b import VOICE_POINTS_S_B4B

ORDER = [f"ps-{i}" for i in range(74, 125)]
_MAP = {}
for p in list(VOICE_POINTS_S_B4A) + list(VOICE_POINTS_S_B4B):
    _MAP[p["id"]] = {
        "id": p["id"], "unit": p["unit"], "name": p["name"],
        "steps": [{"label": s[0], "narration": s[1]} for s in p["steps"]],
    }
BATCH4_POINTS = [_MAP[i] for i in ORDER]
assert len(BATCH4_POINTS) == 51
assert all(len(p["steps"]) == 3 for p in BATCH4_POINTS)
