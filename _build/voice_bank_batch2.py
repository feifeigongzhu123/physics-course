# -*- coding: utf-8 -*-
"""第二批 53 个知识点的语音清单：初中剩余 35 点 + 高中必修一前 18 点。"""
from content_junior import POINTS_JUNIOR
from voice_bank_junior_b2 import VOICE_POINTS_J_B2
from voice_bank_senior_b2 import VOICE_POINTS_S_B2

UNIT_FIX = {"pj-3": "九年级全一册 第十五章 电流和电路"}
NAME_FIX = {"pj-3": "串联和并联"}

ORDER = [
    "pj-52", "pj-53", "pj-54", "pj-55", "pj-3",
    "pj-56", "pj-57", "pj-58", "pj-59", "pj-60", "pj-61", "pj-62", "pj-63",
    "pj-64", "pj-65", "pj-66", "pj-67", "pj-68", "pj-69", "pj-70", "pj-71",
    "pj-72", "pj-73", "pj-74", "pj-75", "pj-76", "pj-77", "pj-78", "pj-79",
    "pj-80", "pj-81", "pj-82", "pj-83", "pj-84", "pj-85",
    "ps-4", "ps-5", "ps-6", "ps-7", "ps-8", "ps-9", "ps-10", "ps-11",
    "ps-12", "ps-13", "ps-14", "ps-15", "ps-16", "ps-17", "ps-18", "ps-19",
    "ps-20", "ps-21",
]


def _norm(p):
    steps = []
    for s in p["steps"]:
        if isinstance(s, dict):
            steps.append({"label": s["label"], "narration": s["narration"]})
        else:
            steps.append({"label": s[0], "narration": s[1]})
    pid = p["id"]
    return {
        "id": pid,
        "unit": UNIT_FIX.get(pid, p.get("unit", "")),
        "name": NAME_FIX.get(pid, p["name"]),
        "steps": steps,
    }


_MAP = {}
for p in list(POINTS_JUNIOR) + list(VOICE_POINTS_J_B2) + list(VOICE_POINTS_S_B2):
    _MAP[p["id"]] = _norm(p)

BATCH2_POINTS = [_MAP[pid] for pid in ORDER]

assert len(BATCH2_POINTS) == 53, len(BATCH2_POINTS)
assert len({p["id"] for p in BATCH2_POINTS}) == 53
for p in BATCH2_POINTS:
    assert len(p["steps"]) == 3, p["id"]
