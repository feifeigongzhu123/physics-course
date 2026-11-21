# -*- coding: utf-8 -*-
"""一次性搭建物理课程骨架：复用化学课的 app.js / app.css / TTS / serve.py。"""
import re
from pathlib import Path

SRC = Path(r"D:\AI\ZCode\chemistry")
DST = Path(r"D:\AI\ZCode\physics")
BUILD = DST / "_build"

for d in [BUILD, BUILD / "scenes", DST / "data", DST / "audio"]:
    d.mkdir(parents=True, exist_ok=True)

# ---- app.js ----
js = (SRC / "_build" / "app.js").read_text(encoding="utf-8")
js = js.replace("APP_VERSION = '1.2.0'", "APP_VERSION = 'v0.1.0'")
js = js.replace("APP_BUILD = '2026-11-19'", "APP_BUILD = '2026-11-19'")
js = js.replace("document.documentElement.setAttribute('data-version', APP_VERSION);",
                "document.documentElement.setAttribute('data-version', APP_VERSION);")
js = js.replace("document.getElementById('junior-data')", "document.getElementById('physics-data')")
js = js.replace("'junior_chem_progress_v1'", "'physics_progress_v1'")
js = js.replace("'chem-audio-v2'", "'physics-audio-v1'")
js = js.replace(
    "var m = (location.hash || '').match(/^#((?:j[123]|s[1-8]|g[23])-(?:[1-9]|1[0-4]))(?:\\/([0-2]))?$/);",
    "var m = (location.hash || '').match(/^#((?:pj|ps)-[1-9])(?:\\/([0-2]))?$/);",
)
js = js.replace("window.__JC", "window.__PH")
js = js.replace("var KEY = 'physics_progress_v1';", "var KEY = 'physics_progress_v1';")
(BUILD / "app.js").write_text(js, encoding="utf-8")

# ---- app.css ----
css = (SRC / "_build" / "app.css").read_text(encoding="utf-8-sig")
start = css.index("/* ===== j1-1 变化与性质 ===== */")
end = css.index("/* ===== 手机端 ===== */")
css = css[:start] + "/*__SCENE_CSS__*/\n\n" + css[end:]

pairs = [
    ("#0e8a7b", "#1d4ed8"),
    ("#0a6b60", "#1e3a8a"),
    ("#e8f7f3", "#e8effc"),
    ("#18a892", "#3b82f6"),
    ("#c9ece4", "#c7d7f5"),
    ("#e7f7f2", "#e7effc"),
    ("#f6fbfa", "#f6f9ff"),
    ("#b9d8d2", "#b9cdf0"),
    ("#f5f1e8", "#eef3fb"),
    ("#fffaf0", "#eef5ff"),
    ("rgba(255,250,240,0)", "rgba(238,245,255,0)"),
    ("#e8e2d6", "#dce5f2"),
]
for a, b in pairs:
    css = css.replace(a, b)
(BUILD / "base_app.css").write_text(css, encoding="utf-8")

# ---- tts / serve ----
(BUILD / "tts.ps1").write_text((SRC / "_build" / "tts.ps1").read_text(encoding="utf-8"), encoding="utf-8")
(DST / "serve.py").write_text((SRC / "serve.py").read_text(encoding="utf-8"), encoding="utf-8")
(DST / "VERSION").write_text("v0.1.0\n", encoding="utf-8")

print("scaffold ok")
print("js len", len(js), "css len", len(css))
print("hash line:", [l for l in js.splitlines() if "location.hash" in l])
