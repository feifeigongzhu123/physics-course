# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\AI\ZCode\physics\README.md")
s = p.read_text(encoding="utf-8")
anchor = "## 语音批进度（2026-11-21）"
sec = """## 高考真题加练（v1.2.0）

- 来源：2021–2025 辽宁 / 黑吉辽蒙高考物理 5 套 PDF，共 50 道选择题（35 单选 + 15 多选）全部收录；每套另有实验/计算非选择题，暂未纳入选择题模式。
- 挂载：50 道题分配到 29 个高中知识点；做完基础 5 题后出现“继续做真题”，可展开加练。
- 真题标识：每道真题显示红色“真题”徽标，并标注年份与来源（如“2021年辽宁高考物理”）。
- 带图题：30 道依赖原题图/图像选项的题，已从 PDF 裁出题目与选项图（`real/<id>.png`），页面直接显示；图像选项用 A/B/C/D 按钮选择。
- 交互：单选直接判，多选勾选后提交；正确答案和每个错误选项都给出原因；支持单题重做、重做全部真题、重做基础 5 题。
- 数据：`data/real_questions.json`；题目图：`real/`。

"""
if anchor in s and "高考真题加练" not in s:
    s = s.replace(anchor, sec + anchor)
s = s.replace("scenes/pj-*.svg           # 初中 85 个三步动画场景",
              "real/*.png                # 30 道带图真题的原题图\ndata/real_questions.json   # 50 道高考真题与逐项解析\n  scenes/pj-*.svg           # 初中 85 个三步动画场景")
s = s.replace("python cdp_senior_check.py # 高中 124 点：场景切换、读数、5 题、MP3、截图",
              "python cdp_senior_check.py # 高中 124 点：场景切换、读数、5 题、MP3、截图\npython cdp_real_check.py   # 真题加练、单选/多选、逐项错因、重做\npython cdp_real_image.py   # 真题图、真题徽标、多选提交")
p.write_text(s, encoding="utf-8")
print("readme updated")
