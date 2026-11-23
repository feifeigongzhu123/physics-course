# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\AI\ZCode\physics\_build\base_app.css")
css = (
    "\n.real-tag{font-size:10px;font-weight:900;color:#fff;background:#dc2626;"
    "border-radius:999px;padding:4px 8px;letter-spacing:.5px}\n"
    ".q-image{display:block;width:100%;max-width:760px;height:auto;margin:4px auto 12px;"
    "border:1px solid #e3e9f2;border-radius:12px;background:#fff}\n"
)
p.write_text(p.read_text(encoding="utf-8") + css, encoding="utf-8")
print("css ok")
