# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\AI\ZCode\physics\_build\build_full.py")
s = p.read_text(encoding="utf-8")
insert = '''REAL_PATH = ROOT / "data" / "real_questions.json"
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

'''
anchor = "normalize_narration(POINTS)\nnormalize_narration(SENIOR_POINTS)"
if insert not in s:
    s = s.replace(anchor, insert + anchor)
p.write_text(s, encoding="utf-8")
print("build patched")
