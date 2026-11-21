# -*- coding: utf-8 -*-
import json, subprocess, wave
from pathlib import Path
import imageio_ffmpeg

root = Path(r"D:\AI\ZCode\physics")
data = json.loads((root / "data" / "voice_bank_junior.json").read_text(encoding="utf-8"))
p = next(x for x in data if x["id"] == "pj-21")
text = p["steps"][0]["narration"]
print("len", len(text))
print(text[:120])
mf = root / "_build" / "_diag_manifest.json"
mf.write_text(json.dumps([{"path": "_diag/test.wav", "text": text}], ensure_ascii=False), encoding="utf-8")
subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-File", str(root / "_build" / "tts.ps1"),
                "-Manifest", str(mf), "-Root", str(root),
                "-Ffmpeg", imageio_ffmpeg.get_ffmpeg_exe()], check=True)
wav = root / "_diag" / "test.wav"
with wave.open(str(wav), "rb") as w:
    print("wav dur", round(w.getnframes() / w.getframerate(), 2), "frames", w.getnframes(), "rate", w.getframerate())
mp3 = root / "_diag" / "test.mp3"
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(wav), "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame", "-b:a", "48k", str(mp3)], check=True)
print("mp3 size", mp3.stat().st_size)
