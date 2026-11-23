# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\AI\ZCode\physics\PRODUCTION.md")
s = p.read_text(encoding="utf-8")
anchor = "## 6. 质量门槛（新点交付前逐条过）"
sec = """## 5.12 高考真题加练（v1.2.0）

- 来源：`D:\\AI\\物理` 下 2021–2025 辽宁/黑吉辽蒙 5 套解析卷；每套 10 道选择题，共 50 道（35 单选 + 15 多选）已全部收录。
- 挂载：50 道题分配在 29 个高中知识点；数据在 `data/real_questions.json`，字段含 `id/year/source/pointId/multi/image/stem/options/answerIndexes/optionNotes/explanation`。
- 带图题：30 道题从 PDF 裁出“题干+选项”图（`real/<id>.png`，裁到【答案】之前），页面显示原题图；图像选项用 A/B/C/D 按钮。
- 页面：真题显示红色“真题”徽标和年份来源；基础 5 题答完后出现“继续做真题”；单选直接判、多选勾选后提交；每题显示正确项和每个错误项的原因；支持单题重做、重做全部真题、重做基础 5 题。
- 非选择题（实验/计算）暂未纳入，后续如果要加需要单独的自由作答题型。

"""
if anchor in s and "5.12" not in s:
    s = s.replace(anchor, sec + anchor)
s = s.replace("**完整课程页 209 点已全部完成**（初中 85 + 高中 124，627 步 / 1045 题），没有待补的点。",
              "**完整课程页 209 点已全部完成**（初中 85 + 高中 124，627 步 / 1045 题），另加 50 道高考真题加练；没有待补的点。")
p.write_text(s, encoding="utf-8")
print("production updated")
