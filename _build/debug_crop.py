# -*- coding: utf-8 -*-
import pymupdf, re
d = pymupdf.open(r"D:\AI\物理\2021年高考物理试卷（辽宁）（解析卷）.pdf")
p = d[0]
for b in p.get_text("blocks"):
    t = (b[4] or "").strip().replace("\n", " ")
    if any(k in t for k in ("一、选择题", "3.考试", "1. 1935", "3. 某驾校", "3.某驾校")):
        print(round(b[1], 1), round(b[3], 1), repr(t[:60]))
