# -*- coding: utf-8 -*-
"""实测单段 Huihui 合成 + MP3 转码耗时。"""
import json, subprocess, time, shutil
from pathlib import Path
import imageio_ffmpeg

ROOT = Path(r"D:\AI\ZCode\physics")
BUILD = ROOT / "_build"
items = json.loads((BUILD / "junior_audio_manifest.json").read_text(encoding="utf-8"))
one = [{"path": "_bench/bench.mp3", "text": items[0]["text"]}]
tmp = BUILD / "_bench_manifest.json"
tmp.write_text(json.dumps(one, ensure_ascii=False), encoding="utf-8")
start = time.perf_counter()
subprocess.run([
    "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
    "-File", str(BUILD / "tts.ps1"), "-Manifest", str(tmp), "-Root", str(ROOT),
    "-Ffmpeg", imageio_ffmpeg.get_ffmpeg_exe(),
], check=True, stdout=subprocess.DEVNULL)
elapsed = time.perf_counter() - start
out = ROOT / "_bench" / "bench.mp3"
size = out.stat().st_size
print(f"单段耗时 {elapsed:.1f}s，MP3 {size/1024:.0f} KB")
print(f"627 段估算 {elapsed*627/3600:.1f} 小时（串行）")
shutil.rmtree(ROOT / "_bench", ignore_errors=True)
tmp.unlink(missing_ok=True)
