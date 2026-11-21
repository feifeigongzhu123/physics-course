# -*- coding: utf-8 -*-
"""把 audio/ 下的 WAV 批量转成 MP3（16k / mono / 48kbps），成功后删除 WAV。"""
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = Path(__file__).resolve().parent.parent
BITRATE = "48k"


def duration(path: Path) -> float:
    p = subprocess.run(
        [FFMPEG, "-hide_banner", "-i", str(path)],
        capture_output=True, text=True, errors="replace",
    )
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", p.stderr)
    if not m:
        return 0.0
    h, mi, s = m.groups()
    return round(int(h) * 3600 + int(mi) * 60 + float(s), 2)


def convert(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
         "-i", str(src), "-vn", "-ac", "1", "-ar", "16000",
         "-c:a", "libmp3lame", "-b:a", BITRATE, str(dst)],
        check=True,
    )


def main():
    wavs = sorted((ROOT / "audio").glob("*/*.wav"))
    total_in = total_out = 0
    n = 0
    for src in wavs:
        dst = src.with_suffix(".mp3")
        if dst.exists() and dst.stat().st_size > 1000:
            src.unlink()
            continue
        convert(src, dst)
        if dst.stat().st_size < 1000:
            raise SystemExit(f"转码失败：{src}")
        total_in += src.stat().st_size
        total_out += dst.stat().st_size
        src.unlink()
        n += 1
        print(f"[{n}/{len(wavs)}] {dst.relative_to(ROOT)} {duration(dst)}s")
    print(f"完成 {n} 段；WAV {total_in/1048576:.1f} MB -> MP3 {total_out/1048576:.1f} MB")


if __name__ == "__main__":
    main()
