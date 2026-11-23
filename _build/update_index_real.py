# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\AI\ZCode\physics\index.html")
s = p.read_text(encoding="utf-8")
s = s.replace("版本 <b>v1.0.0</b> · 2026-11-21 · 课程页 209 点 / 627 步 / 1045 题 · 语音 209 点 / 627 段",
              "版本 <b>v1.1.0</b> · 2026-11-21 · 课程页 209 点 / 627 步 / 1045 题 + 20 道高考真题 · 语音 627 段")
s = s.replace('<span class="feature">209 点语音已就绪</span>',
              '<span class="feature">209 点语音已就绪</span>\n      <span class="feature">20 道高考真题加练</span>')
s = s.replace("<li>全课程 209 点已全部完成：初中 85 + 高中 124，共 627 步动画、1045 道题；语音层 627 段 MP3（约 86 MB）。</li>",
              "<li>全课程 209 点已全部完成：初中 85 + 高中 124，共 627 步动画、1045 道题；语音层 627 段 MP3（约 86 MB）。</li>\n      <li>16 个高中点追加了 20 道 2021–2025 高考真题（含 5 道多选）：做完 5 题可继续做真题，单选/多选都支持重做。</li>")
p.write_text(s, encoding="utf-8")
print("index updated")
