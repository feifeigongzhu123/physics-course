# -*- coding: utf-8 -*-
"""校验真题 JSON：选项、答案、逐项解析、知识点映射。用法：python validate_real_questions.py real_questions_a.json"""
import json, re, sys
from pathlib import Path

ROOT = Path(r"D:\AI\ZCode\physics")
senior = json.loads((ROOT / "data" / "senior.json").read_text(encoding="utf-8"))
junior = json.loads((ROOT / "data" / "junior.json").read_text(encoding="utf-8"))
POINT_IDS = {p["id"] for p in senior + junior}
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
ok = True
ids = set()
for q in data:
    errs = []
    qid = q.get("id", "?")
    if qid in ids:
        errs.append("id 重复")
    ids.add(qid)
    if q.get("pointId") not in POINT_IDS:
        errs.append(f"pointId 不存在 {q.get('pointId')}")
    if len(q.get("options", [])) != 4 or len(set(q.get("options", []))) != 4:
        errs.append("选项不是 4 个互异")
    ans = q.get("answerIndexes")
    if not isinstance(ans, list) or not ans or any(not isinstance(i, int) or not 0 <= i < 4 for i in ans):
        errs.append("answerIndexes 非法")
        ans = []
    if len(set(ans)) != len(ans):
        errs.append("answerIndexes 重复")
    if bool(q.get("multi")) != (len(ans) > 1):
        errs.append("multi 与答案数量不一致")
    notes = q.get("optionNotes", [])
    if len(notes) != 4:
        errs.append("optionNotes 不是 4 条")
    else:
        for i, n in enumerate(notes):
            if not re.match(r"^[ABCD] [对错]：", n):
                errs.append(f"解析格式 {n[:10]}")
            if not n.startswith("ABCD"[i] + " "):
                errs.append("解析标号错位")
            if (i in ans) != ("对" in n[:4]):
                errs.append(f"{qid} 第 {i} 项对错与答案不符")
    n = len(q.get("explanation", ""))
    if not 40 <= n <= 220:
        errs.append(f"解析长度 {n}")
    for k in ("stem", "source"):
        if not q.get(k):
            errs.append(f"缺少 {k}")
    if errs:
        ok = False
        print("[FAIL]", qid, "；".join(errs))
    else:
        print("[OK]", qid, q.get("pointId"), "answers", "".join("ABCD"[i] for i in ans))
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
