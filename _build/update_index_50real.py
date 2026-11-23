# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\AI\ZCode\physics\index.html")
s = p.read_text(encoding="utf-8")
s = s.replace("版本 <b>v1.1.0</b> · 2026-11-21 · 课程页 209 点 / 627 步 / 1045 题 + 20 道高考真题 · 语音 627 段",
              "版本 <b>v1.2.0</b> · 2026-11-21 · 课程页 209 点 / 627 步 / 1045 题 + 50 道高考真题 · 语音 627 段")
s = s.replace('<span class="feature">20 道高考真题加练</span>', '<span class="feature">50 道高考真题加练</span>')
s = s.replace("16 个高中点追加了 20 道 2021–2025 高考真题（含 5 道多选）：做完 5 题可继续做真题，单选/多选都支持重做。",
              "29 个高中点追加了 50 道 2021–2025 高考真题（含 15 道多选）：真题带红色“真题”标和年份来源，带图题显示原题图；做完 5 题可继续做真题，单选/多选都支持重做。")
p.write_text(s, encoding="utf-8")

p = Path(r"D:\AI\ZCode\physics\_build\app.js")
s = p.read_text(encoding="utf-8").replace("var APP_VERSION = 'v1.1.0'", "var APP_VERSION = 'v1.2.0'")
p.write_text(s, encoding="utf-8")
Path(r"D:\AI\ZCode\physics\VERSION").write_text("v1.2.0\n", encoding="utf-8")
print("version/index updated")
