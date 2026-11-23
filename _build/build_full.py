# -*- coding: utf-8 -*-
"""构建“初中 3 个样例 + 20 个自动生成点”的完整 junior.html。"""
import json
import sys
from pathlib import Path

from build import BUILD, ROOT, prepare, validate, write_data, build_html
from content_junior import POINTS_JUNIOR
from content_auto_batch1 import POINTS_AUTO_B1
from content_auto_batch2 import POINTS_AUTO_B2
from content_auto_batch3 import POINTS_AUTO_B3
from content_auto_batch4 import POINTS_AUTO_B4
from content_auto_batch_s1 import POINTS_AUTO_S1
from content_auto_batch_s0 import POINTS_AUTO_S0
from content_auto_batch_s2 import POINTS_AUTO_S2
from content_auto_batch_s3 import POINTS_AUTO_S3
from content_auto_batch_s4 import POINTS_AUTO_S4
from content_auto_batch_s5 import POINTS_AUTO_S5
from content_auto_batch_s6 import POINTS_AUTO_S6
from content_senior import POINTS_SENIOR

UNIT_FIX = {
    "pj-1": "八年级上册 第四章 光现象",
    "pj-2": "八年级上册 第五章 透镜及其应用",
    "pj-3": "九年级全一册 第十五章 电流和电路",
}
ORDER = [
    "pj-4", "pj-5", "pj-6", "pj-7", "pj-8", "pj-9", "pj-10", "pj-11",
    "pj-12", "pj-13", "pj-14", "pj-15", "pj-16", "pj-1", "pj-17", "pj-18",
    "pj-19", "pj-20", "pj-21", "pj-2", "pj-22", "pj-23",
] + [f"pj-{i}" for i in range(24, 86)] + ["pj-3"]
_MAP = {}
for p in list(POINTS_JUNIOR) + list(POINTS_AUTO_B1) + list(POINTS_AUTO_B2) + list(POINTS_AUTO_B3) + list(POINTS_AUTO_B4):
    p["unit"] = UNIT_FIX.get(p["id"], p["unit"])
    _MAP[p["id"]] = p
POINTS = [_MAP[i] for i in ORDER]

SENIOR_ORDER = (
    [f"ps-{i}" for i in range(4, 22)]
    + ["ps-22", "ps-23", "ps-24", "ps-25", "ps-1"]
    + [f"ps-{i}" for i in range(26, 42)]
    + [f"ps-{i}" for i in range(42, 48)]
    + ["ps-3"]
    + [f"ps-{i}" for i in range(48, 62)]
    + [f"ps-{i}" for i in range(62, 68)]
    + ["ps-2"]
    + [f"ps-{i}" for i in range(68, 125)]
)
_SENIOR_MAP = {}
for p in list(POINTS_SENIOR) + list(POINTS_AUTO_S1) + list(POINTS_AUTO_S0) + list(POINTS_AUTO_S2) + list(POINTS_AUTO_S3) + list(POINTS_AUTO_S4) + list(POINTS_AUTO_S5) + list(POINTS_AUTO_S6):
    _SENIOR_MAP[p["id"]] = p
SENIOR_POINTS = [_SENIOR_MAP[i] for i in SENIOR_ORDER]

VOICE_FILES = [
    "voice_bank_junior.json",
    "voice_bank_batch2.json",
    "voice_bank_batch3.json",
    "voice_bank_batch4.json",
]


def normalize_narration(points):
    """构建时用语音库原文覆盖 narration，确保数据、字幕与已生成音频一致。"""
    voice = {}
    for name in VOICE_FILES:
        path = ROOT / "data" / name
        if not path.exists():
            continue
        for p in json.loads(path.read_text(encoding="utf-8")):
            for i, s in enumerate(p["steps"], 1):
                voice[(p["id"], i)] = s["narration"]
    for p in points:
        for i, s in enumerate(p["steps"], 1):
            if (p["id"], i) in voice:
                s["narration"] = voice[(p["id"], i)]


REAL_PATH = ROOT / "data" / "real_questions.json"
if REAL_PATH.exists():
    _real = json.loads(REAL_PATH.read_text(encoding="utf-8"))
    _by_point = {}
    for _q in _real:
        _q["real"] = True
        _by_point.setdefault(_q.get("pointId"), []).append(_q)
    for _p in SENIOR_POINTS:
        _list = _by_point.get(_p["id"])
        if _list:
            _p["realQuestions"] = _list

normalize_narration(POINTS)
normalize_narration(SENIOR_POINTS)

if __name__ == "__main__":
    prepare(POINTS, "junior")
    validate(POINTS, "junior", 85, "中考真题改编")
    write_data(POINTS, "junior")
    build_html(
        POINTS, "junior", "junior.html",
        [
            ("初中物理 · 动画精讲（样例）", "初中物理 · 动画精讲（85 点）"),
            ("初中物理 · 样例课", "初中物理 · 动画精讲"),
            ("光学与电路 · 9 段动画 · 15 道中考真题改编 · 每题逐项解析",
             "初中 85 个知识点 · 255 段动画 · 425 道中考真题改编 · 每题逐项解析"),
        ],
    )
    print("full junior build ok:", len(POINTS))

    prepare(SENIOR_POINTS, "senior")
    validate(SENIOR_POINTS, "senior", 124, "高考真题改编")
    write_data(SENIOR_POINTS, "senior")
    build_html(
        SENIOR_POINTS, "senior", "senior.html",
        [
            ("初中物理 · 动画精讲（样例）", "高中物理 · 动画精讲（124 点）"),
            ("初中物理 · 样例课", "高中物理 · 动画精讲"),
            ("光学与电路 · 9 段动画 · 15 道中考真题改编 · 每题逐项解析",
             "高中 124 个知识点 · 372 段动画 · 620 道高考真题改编 · 每题逐项解析"),
            ("5 道题 · 中考真题改编", "5 道题 · 高考真题改编"),
            ('<span class="kicker" id="lessonKicker">初中物理</span>',
             '<span class="kicker" id="lessonKicker">高中物理</span>'),
            ("<h1>初中物理 · 动画精讲", "<h1>高中物理 · 动画精讲"),
        ],
    )
    print("full build ok: junior", len(POINTS), "senior", len(SENIOR_POINTS))
