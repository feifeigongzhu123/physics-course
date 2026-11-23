# -*- coding: utf-8 -*-
"""从高考真题 PDF 裁出剩余 30 道选择题的题目+选项图（裁到【答案】之前）。"""
import io
import json
import re
from pathlib import Path

import pymupdf
from PIL import Image

SRC = Path(r"D:\AI\物理")
OUT = Path(r"D:\AI\ZCode\physics\real")
OUT.mkdir(parents=True, exist_ok=True)

PDFS = {
    2021: "2021年高考物理试卷（辽宁）（解析卷）.pdf",
    2022: "2022年高考物理试卷（辽宁）（解析卷）.pdf",
    2023: "2023年高考物理试卷（辽宁）（解析卷）.pdf",
    2024: "2024年高考物理试卷（辽宁）（解析卷）.pdf",
    2025: "2025年黑龙江、吉林、辽宁、内蒙古高考物理真题（解析版）.pdf",
}
QNUM = {
    2021: [3, 5, 6, 7, 9, 10],
    2022: [2, 3, 5, 6, 8, 10],
    2023: [1, 3, 4, 5, 6, 7, 9, 10],
    2024: [5, 6, 7, 9, 10],
    2025: [4, 5, 7, 9, 10],
}


def page_image(page, clip=None, zoom=2.0):
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip, alpha=False)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")


def find_q(doc, num):
    pat = re.compile(r"^\s*" + str(num) + r"\s*[.．]\s*")
    start = None
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("blocks"):
            if "一、选择题" in (b[4] or ""):
                start = (pno, b[1])
                break
        if start:
            break
    if not start:
        return None, None, None
    sp, sy = start
    for pno in range(sp, doc.page_count):
        page = doc[pno]
        for b in page.get_text("blocks"):
            text = (b[4] or "").strip()
            if pno == sp and b[1] <= sy + 2:
                continue
            if pat.match(text):
                return pno, b[1], text[:60]
    return None, None, None


def find_answer(doc, start_page, start_y):
    for pno in range(start_page, doc.page_count):
        page = doc[pno]
        for b in page.get_text("blocks"):
            text = (b[4] or "").strip()
            if "【答案】" in text:
                if pno != start_page or b[1] > start_y + 20:
                    return pno, b[1]
    return None, None


manifest = []
for year, pdf_name in PDFS.items():
    doc = pymupdf.open(str(SRC / pdf_name))
    for num in QNUM[year]:
        pno, y, head = find_q(doc, num)
        qid = f"ln{year}-q{num}"
        if pno is None:
            print("NO QUESTION", qid)
            continue
        apno, ay = find_answer(doc, pno, y)
        if apno is None:
            print("NO ANSWER", qid, "page", pno)
            apno, ay = pno, doc[pno].rect.height
        imgs = []
        for p in range(pno, apno + 1):
            page = doc[p]
            if p == pno and p == apno:
                clip = pymupdf.Rect(0, max(0, y - 6), page.rect.width, min(page.rect.height, ay - 2))
            elif p == pno:
                clip = pymupdf.Rect(0, max(0, y - 6), page.rect.width, page.rect.height)
            elif p == apno:
                clip = pymupdf.Rect(0, 0, page.rect.width, min(page.rect.height, ay - 2))
            else:
                clip = page.rect
            if clip.height < 5:
                continue
            imgs.append(page_image(page, clip))
        if not imgs:
            print("EMPTY", qid)
            continue
        w = max(i.width for i in imgs)
        h = sum(i.height for i in imgs) + 10 * (len(imgs) - 1)
        canvas = Image.new("RGB", (w, h), "white")
        yy = 0
        for im in imgs:
            canvas.paste(im, (0, yy))
            yy += im.height + 10
        path = OUT / f"{qid}.png"
        canvas.save(path, optimize=True)
        manifest.append({"id": qid, "image": f"real/{qid}.png", "pages": [pno + 1, apno + 1]})
        print("OK", qid, path.name, canvas.size, "pages", pno + 1, apno + 1)

(Path(r"D:\AI\ZCode\physics\_build\real_images.json")).write_text(
    json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8"
)
print("images", len(manifest))
