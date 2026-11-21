# -*- coding: utf-8 -*-
"""自动补齐剩余高中语音：第三批、第四批依次生成并构建试听页。"""
import subprocess
import sys
from pathlib import Path

BUILD = Path(__file__).resolve().parent


def run(*args):
    print(">>", " ".join(map(str, args)))
    subprocess.run([sys.executable, *map(str, args)], cwd=BUILD, check=True)


if __name__ == "__main__":
    for batch in ("3", "4"):
        run("gen_voice_bank.py", "--batch", batch)
        run("build_voice_bank.py", batch)
    print("剩余高中语音批次完成")
