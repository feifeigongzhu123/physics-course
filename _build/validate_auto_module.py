# -*- coding: utf-8 -*-
"""校验自动生成的 5 点内容模块。用法：python validate_auto_module.py content_auto_a.py"""
import importlib.util
import re
import sys

ANGLES = ["概念辨析", "现象图像", "实验装置", "计算守恒", "易错陷阱"]
path = sys.argv[1]
spec = importlib.util.spec_from_file_location("mod", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
lists = [v for k, v in vars(mod).items() if k.startswith("POINTS_AUTO")]
assert len(lists) == 1, "需要一个 POINTS_AUTO_* 列表"
pts = lists[0]
ok = True
for p in pts:
    pid = p.get("id", "?")
    errs = []
    for k in ("id", "unit", "name", "title", "subtitle", "readoutLabels", "steps", "questions"):
        if not p.get(k):
            errs.append(f"缺少 {k}")
    if len(p.get("readoutLabels", [])) != 3:
        errs.append("readoutLabels 不是 3")
    if len(p.get("steps", [])) != 3:
        errs.append("steps 不是 3")
    for i, s in enumerate(p.get("steps", []), 1):
        for k in ("label", "caption", "narration", "reads", "eq", "eqSub"):
            if not s.get(k):
                errs.append(f"第{i}步缺少 {k}")
        if len(s.get("reads", [])) != 3:
            errs.append(f"第{i}步 reads 不是 3")
        if re.search(r"<(?!/?b>)", s.get("caption", "")):
            errs.append(f"第{i}步 caption 有未转义的 <")
        if len(s.get("narration", "")) < 40:
            errs.append(f"第{i}步 narration 过短")
    qs = p.get("questions", [])
    if len(qs) != 5:
        errs.append("题数不是 5")
    if [q.get("angle") for q in qs] != ANGLES:
        errs.append("题目角度不齐")
    seq = []
    for q in qs:
        qid = q.get("id", "?")
        if q.get("source") not in ("中考真题改编", "高考真题改编"):
            errs.append(f"{qid} 来源错误")
        if len(q.get("options", [])) != 4 or len(set(q.get("options", []))) != 4:
            errs.append(f"{qid} 选项错误")
        ai = q.get("answerIndex")
        if not isinstance(ai, int) or not 0 <= ai < 4:
            errs.append(f"{qid} answerIndex 错误")
            continue
        notes = q.get("optionNotes", [])
        if len(notes) != 4:
            errs.append(f"{qid} 解析不是 4 条")
        else:
            for i, n in enumerate(notes):
                if not re.match(r"^[ABCD] [对错]：", n):
                    errs.append(f"{qid} 解析格式 {n[:10]}")
                if not n.startswith("ABCD"[i] + " "):
                    errs.append(f"{qid} 解析标号错位")
                if (i == ai) != ("对" in n[:4]):
                    errs.append(f"{qid} 对错与答案不符")
        n = len(q.get("explanation", ""))
        if not 60 <= n <= 110:
            errs.append(f"{qid} 解析长度 {n}")
        seq.append(ai)
    for a, b in zip(seq, seq[1:]):
        if a == b:
            errs.append("连续同答案")
    if set(seq) != {0, 1, 2, 3}:
        errs.append(f"答案未覆盖 ABCD {seq}")
    if errs:
        ok = False
        print(f"[FAIL] {pid} {p.get('name')} -> " + "；".join(errs))
    else:
        print(f"[OK] {pid} {p.get('name')} 答案 {seq}")
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
