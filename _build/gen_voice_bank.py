# -*- coding: utf-8 -*-
"""生成语音批：讲解稿 -> manifest -> Huihui + ffmpeg -> MP3。"""
import argparse
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent.parent
BUILD = Path(__file__).resolve().parent
DATA = ROOT / "data"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="逗号分隔的知识点 id，如 pj-4,pj-5")
    ap.add_argument("--batch", choices=["1", "2", "3", "4"], default="1")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    only = [x.strip() for x in args.only.split(",") if x.strip()]

    if args.batch == "1":
        from voice_bank_batch1 import BATCH1_POINTS as all_points
    elif args.batch == "2":
        from voice_bank_batch2 import BATCH2_POINTS as all_points
    elif args.batch == "3":
        from voice_bank_batch3 import BATCH3_POINTS as all_points
    else:
        from voice_bank_batch4 import BATCH4_POINTS as all_points
    points = [p for p in all_points if not only or p["id"] in only]
    manifest = []
    for p in points:
        for i, s in enumerate(p["steps"], 1):
            manifest.append({"path": f"audio/{p['id']}/step{i}.mp3", "text": s["narration"]})

    data = [
        {
            "id": p["id"], "unit": p["unit"], "name": p["name"],
            "steps": [{"label": s["label"], "narration": s["narration"]} for s in p["steps"]],
        }
        for p in points
    ]
    DATA.mkdir(exist_ok=True)
    out_json = DATA / {
        "1": "voice_bank_junior.json",
        "2": "voice_bank_batch2.json",
        "3": "voice_bank_batch3.json",
        "4": "voice_bank_batch4.json",
    }[args.batch]
    if not only:
        out_json.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    todo = [it for it in manifest
            if not ((ROOT / it["path"]).exists() and (ROOT / it["path"]).stat().st_size > 1000)]
    print(f"第 {args.batch} 批：知识点 {len(points)} 个，语音 {len(manifest)} 段，待生成 {len(todo)} 段")
    if args.dry_run or not todo:
        return

    tmp = BUILD / "_voice_bank_manifest.json"
    tmp.write_text(json.dumps(todo, ensure_ascii=False, indent=1), encoding="utf-8")
    cmd = [
        "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", str(BUILD / "tts.ps1"),
        "-Manifest", str(tmp), "-Root", str(ROOT), "-Ffmpeg", imageio_ffmpeg.get_ffmpeg_exe(),
    ]
    try:
        subprocess.run(cmd, check=True)
    finally:
        tmp.unlink(missing_ok=True)

    total = sum((ROOT / it["path"]).stat().st_size for it in manifest
                if (ROOT / it["path"]).exists())
    print(f"完成：{len(manifest)} 段，共 {total/1048576:.1f} MB")


if __name__ == "__main__":
    main()
