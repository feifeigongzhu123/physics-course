# -*- coding: utf-8 -*-
"""第一批 50 个知识点的语音清单，按教材顺序排列。"""
from content_junior import POINTS_JUNIOR
from voice_bank_junior import VOICE_POINTS
from voice_bank_junior_b1 import VOICE_POINTS_B1

UNIT_FIX = {
    "pj-1": "八年级上册 第四章 光现象",
    "pj-2": "八年级上册 第五章 透镜及其应用",
}
NAME_FIX = {"pj-2": "凸透镜成像的规律"}

ORDER = [
    "pj-4", "pj-5", "pj-6", "pj-7", "pj-8", "pj-9", "pj-10", "pj-11",
    "pj-12", "pj-13", "pj-14", "pj-15", "pj-16", "pj-1", "pj-17", "pj-18",
    "pj-19", "pj-20", "pj-21", "pj-2", "pj-22", "pj-23", "pj-24", "pj-25",
    "pj-26", "pj-27", "pj-28", "pj-29", "pj-30", "pj-31", "pj-32", "pj-33",
    "pj-34", "pj-35", "pj-36", "pj-37", "pj-38", "pj-39", "pj-40", "pj-41",
    "pj-42", "pj-43", "pj-44", "pj-45", "pj-46", "pj-47", "pj-48", "pj-49",
    "pj-50", "pj-51",
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
for p in list(POINTS_JUNIOR) + list(VOICE_POINTS) + list(VOICE_POINTS_B1):
    _MAP[p["id"]] = _norm(p)

BATCH1_POINTS = [_MAP[pid] for pid in ORDER]

assert len(BATCH1_POINTS) == 50, len(BATCH1_POINTS)
assert len({p["id"] for p in BATCH1_POINTS}) == 50
for p in BATCH1_POINTS:
    assert len(p["steps"]) == 3, p["id"]
