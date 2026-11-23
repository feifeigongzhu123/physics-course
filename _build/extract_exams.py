# -*- coding: utf-8 -*-
import sys, io
from pathlib import Path
import pymupdf

src = Path(r"D:\AI\物理")
out = Path(r"D:\AI\ZCode\physics\_build\exam_text")
out.mkdir(parents=True, exist_ok=True)
for pdf in sorted(src.glob("*.pdf")):
    doc = pymupdf.open(str(pdf))
    text = "\n\n".join(page.get_text("text") for page in doc)
    p = out / (pdf.stem + ".txt")
    p.write_text(text, encoding="utf-8")
    print(p.name, len(text), "chars", doc.page_count, "pages")
print("done")
