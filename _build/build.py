# -*- coding: utf-8 -*-
"""构建物理样例课：junior.html / senior.html / data / 音频清单。"""
import json
import re
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg

from content_junior import POINTS_JUNIOR
from content_senior import POINTS_SENIOR

ROOT = Path(__file__).resolve().parent.parent
BUILD = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
AUDIO_DIR = ROOT / "audio"
ANGLES = ["概念辨析", "现象图像", "实验装置", "计算守恒", "易错陷阱"]
BANNED = ["离线播放"]

SCENES = {
    "pj-1": "平面镜、法线、入射光线、反射光线、角度弧",
    "pj-2": "凸透镜、主光轴、焦点、物体、两条特殊光线、像",
    "pj-3": "串联回路、并联双支路、电池、开关、灯泡",
    "ps-1": "抛出点、抛物线轨迹、等时水平箭头、速度分解",
    "ps-2": "墙、弹簧、振子、平衡位置、x-t 图像、能量条",
    "ps-3": "电子枪、平行板、电场线、偏转轨迹、荧光屏",
}


def audio_duration(path: Path) -> float:
    try:
        if path.suffix == ".wav":
            with wave.open(str(path), "rb") as w:
                return round(w.getnframes() / float(w.getframerate()), 2)
        p = subprocess.run(
            [imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-i", str(path)],
            capture_output=True, text=True, errors="replace",
        )
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", p.stderr)
        if not m:
            return 0.0
        h, mi, s = m.groups()
        return round(int(h) * 3600 + int(mi) * 60 + float(s), 2)
    except Exception:
        return 0.0


def prepare(points, grade):
    for p in points:
        p["grade"] = grade
        p.setdefault("scene", {"type": "physics", "props": SCENES.get(p["id"], p["name"])})
        for i, s in enumerate(p["steps"], 1):
            s["audio"] = f"audio/{p['id']}/step{i}.mp3"
            s["dur"] = audio_duration(AUDIO_DIR / p["id"] / f"step{i}.mp3")


def validate(points, grade, expect, exam):
    assert len(points) == expect, f"{grade} 知识点数量应为 {expect}，实际 {len(points)}"
    ids = [p["id"] for p in points]
    assert len(set(ids)) == expect, f"{grade} id 重复"
    letters = set()
    for p in points:
        assert p.get("grade") == grade, f"{p['id']} grade 错误"
        assert p.get("scene", {}).get("type") == "physics", f"{p['id']} scene.type"
        assert p.get("scene", {}).get("props"), f"{p['id']} scene.props 缺失"
        assert p.get("readoutLabels") and len(p["readoutLabels"]) == 3, f"{p['id']} 读数标签不是 3"
        assert len(p["steps"]) == 3, f"{p['id']} 步数不是 3"
        assert [s.get("label") for s in p["steps"]] == [s["label"] for s in p["steps"]], f"{p['id']} 步骤标签"
        for i, s in enumerate(p["steps"], 1):
            for k in ("label", "caption", "narration", "eq", "eqSub"):
                assert s.get(k), f"{p['id']} 第 {i} 步缺少 {k}"
            assert len(s["reads"]) == 3, f"{p['id']} 第 {i} 步读数不是 3 个"
            assert len(s["narration"]) >= 20, f"{p['id']} 第 {i} 步语音稿过短"
        assert len(p["questions"]) == 5, f"{p['id']} 题数不是 5"
        assert [q["angle"] for q in p["questions"]] == ANGLES, f"{p['id']} 角度不齐"
        seq = []
        for q in p["questions"]:
            assert q["source"] == exam, f"{q['id']} 来源标注错误"
            assert len(q["options"]) == 4 and len(set(q["options"])) == 4, f"{q['id']} 选项"
            assert 0 <= q["answerIndex"] < 4, f"{q['id']} 答案越界"
            assert len(q["optionNotes"]) == 4, f"{q['id']} 逐项解析不是 4 条"
            for i, n in enumerate(q["optionNotes"]):
                assert re.match(r"^[ABCD] [对错]：", n), f"{q['id']} 解析格式：{n[:14]}"
                assert n.startswith("ABCD"[i] + " "), f"{q['id']} 解析标号与选项不符"
            assert 60 <= len(q["explanation"]) <= 110, f"{q['id']} 解析长度 {len(q['explanation'])}"
            letters.add("ABCD"[q["answerIndex"]])
            seq.append(q["answerIndex"])
        for a, b in zip(seq, seq[1:]):
            assert a != b, f"{p['id']} 连续同答案：{seq}"
        assert set(seq) == {0, 1, 2, 3}, f"{p['id']} 答案未覆盖 ABCD：{seq}"
    assert letters == set("ABCD"), f"{grade} 答案字母未覆盖"
    blob = json.dumps(points, ensure_ascii=False)
    for w in BANNED:
        assert w not in blob, f"出现禁用词：{w}"
    print(f"{grade} 校验通过：{len(points)} 点 / {len(points)*3} 步 / {len(points)*5} 题")


def write_data(points, name):
    DATA_DIR.mkdir(exist_ok=True)
    payload = json.dumps(points, ensure_ascii=False, indent=1)
    (DATA_DIR / f"{name}.json").write_text(payload + "\n", encoding="utf-8")
    manifest = []
    for p in points:
        for i, s in enumerate(p["steps"], 1):
            manifest.append({"path": f"audio/{p['id']}/step{i}.mp3", "text": s["narration"]})
    (BUILD / f"{name}_audio_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"已写入 data/{name}.json 与音频清单 {len(manifest)} 段")


def build_html(points, name, out, replacements):
    template = (BUILD / "template.html").read_text(encoding="utf-8")
    css = (BUILD / "base_app.css").read_text(encoding="utf-8").replace(
        "/*__SCENE_CSS__*/", (BUILD / "scenes.css").read_text(encoding="utf-8")
    )
    js = (BUILD / "app.js").read_text(encoding="utf-8")
    scene_files = sorted((BUILD / "scenes").glob(f"{'pj' if name == 'junior' else 'ps'}*.svg"))
    assert len(scene_files) == len(points), f"{name} 场景数 {len(scene_files)} != {len(points)}"
    blocks = []
    for f in scene_files:
        blocks.append(
            f'<div class="scene" data-scene="{f.stem}" id="scene-{f.stem}">\n'
            + f.read_text(encoding="utf-8").strip() + "\n</div>"
        )
    html = template.replace("/*__CSS__*/", css)
    html = html.replace("<!--__SCENES__-->", "\n".join(blocks))
    html = html.replace("__DATA_JSON__", json.dumps(points, ensure_ascii=False, indent=1))
    html = html.replace("/*__APP_JS__*/", js)
    for a, b in replacements:
        html = html.replace(a, b)
    (ROOT / out).write_text(html, encoding="utf-8")
    print(f"已写入 {out}：{len(html)/1024:.1f} KB")


if __name__ == "__main__":
    raise SystemExit("初中已扩到 23 点，请运行 python build_full.py（同时构建初中 23 点和高中 3 点）。")
