# -*- coding: utf-8 -*-
"""按学段/知识点批量生成 MP3 语音。

用法：
  python gen_audio.py --grade junior              # 初中全部待生成
  python gen_audio.py --grade senior --only ps-4,ps-5
  python gen_audio.py --grade all --dry-run       # 只估算，不生成
已存在的 MP3 默认跳过，可断点续跑；--force 重生成。
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent.parent
BUILD = Path(__file__).resolve().parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
AVG_SECONDS = 31


def load(grade):
    mf = BUILD / f"{grade}_audio_manifest.json"
    if not mf.exists():
        raise SystemExit(f"缺少 {mf}，请先运行 build.py")
    return json.loads(mf.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grade", choices=["junior", "senior", "all"], default="all")
    ap.add_argument("--only", default="", help="逗号分隔的知识点 id，如 pj-4,ps-2")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    grades = ["junior", "senior"] if args.grade == "all" else [args.grade]
    only = [x.strip() for x in args.only.split(",") if x.strip()]
    items = []
    for g in grades:
        for it in load(g):
            if only and not any(f"/{pid}/" in "/" + it["path"] for pid in only):
                continue
            items.append(it)

    todo = []
    for it in items:
        p = ROOT / it["path"]
        if args.force or not (p.exists() and p.stat().st_size > 1000):
            todo.append(it)

    est_mb = len(todo) * AVG_SECONDS * 6000 / 1048576
    print(f"清单 {len(items)} 段，待生成 {len(todo)} 段，已存在跳过 {len(items)-len(todo)} 段")
    print(f"预计时长约 {len(todo)*AVG_SECONDS/60:.0f} 分钟，MP3 约 {est_mb:.1f} MB")
    if args.dry_run or not todo:
        return

    tmp = BUILD / "_tmp_audio_manifest.json"
    tmp.write_text(json.dumps(todo, ensure_ascii=False, indent=1), encoding="utf-8")
    cmd = [
        "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", str(BUILD / "tts.ps1"),
        "-Manifest", str(tmp), "-Root", str(ROOT), "-Ffmpeg", FFMPEG,
    ]
    try:
        subprocess.run(cmd, check=True)
    finally:
        tmp.unlink(missing_ok=True)
    print("完成。建议运行 python build.py 更新时长并重建页面。")


if __name__ == "__main__":
    main()
