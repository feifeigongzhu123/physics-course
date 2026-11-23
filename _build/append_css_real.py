# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\AI\ZCode\physics\_build\base_app.css")
css = '''
/* ===== 真题加练 / 重做 ===== */
.q-head{flex-wrap:wrap;align-items:center}
#qProgress{margin-left:auto}
.redo-all{border:1px solid #e5e7ef;background:#fff;border-radius:999px;padding:7px 12px;font-size:10.5px;font-weight:800;color:#3a4a63;cursor:pointer}
.redo-all:disabled{cursor:default}
.real-teaser{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px;margin-top:12px;border:1px solid #c7d7f5;background:linear-gradient(135deg,#ffffff,#eef5ff)}
.real-teaser b{display:block;font-size:14px;color:#1e3a8a}
.real-teaser span{display:block;font-size:11px;color:#64748b;margin-top:4px;line-height:1.6}
#openReal{border:0;border-radius:12px;padding:10px 14px;font-size:12px;font-weight:900;color:#fff;background:linear-gradient(135deg,#3b82f6,#1d4ed8);cursor:pointer;white-space:nowrap}
.real-head{margin-top:22px;border-top:1px dashed #dbe6f2;padding-top:16px}
.multi-tip{font-size:10.5px;color:#1d4ed8;background:#eef5ff;border:1px solid #d6e4fb;border-radius:9px;padding:7px 10px;margin:8px 0}
.submit-answer{border:0;border-radius:12px;padding:10px 16px;font-size:12px;font-weight:900;color:#fff;background:linear-gradient(135deg,#3b82f6,#1d4ed8);cursor:pointer;margin:8px 0 2px}
.submit-answer:disabled{opacity:.55;cursor:default}
.opt.selected{border-color:#1d4ed8;background:#eef5ff;box-shadow:inset 0 0 0 1px #1d4ed8}
.opt.selected .letter{background:#1d4ed8;color:#fff}
.q-actions{display:flex;gap:8px;flex-wrap:wrap}
.redo{border:1px solid #d7e2f2;background:#fff;border-radius:999px;padding:7px 13px;font-size:11.5px;font-weight:800;color:#3a4a63;cursor:pointer}
.redo:hover{border-color:#b9cdf0;color:#1e3a8a}
'''
p.write_text(p.read_text(encoding="utf-8") + css, encoding="utf-8")
print("css appended")
