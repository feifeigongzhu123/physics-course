# -*- coding: utf-8 -*-
"""根据 data/voice_bank_junior.json 生成语音试听页 voice-bank.html。"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent.parent
BATCH = sys.argv[1] if len(sys.argv) > 1 else "1"
CFG = {
    "1": {
        "data": "voice_bank_junior.json",
        "out": "voice-bank.html",
        "kicker": "物理语音批 · 第一批",
        "title": "八年级上册 50 个知识点，150 段讲解语音",
        "sub": "覆盖八年级上册第一～六章，按教材顺序排列。语音为 MP3 48 kbps，总时长约 {mins:.1f} 分钟，可逐段试听；动画与题库随后接入课程页。",
    },
    "2": {
        "data": "voice_bank_batch2.json",
        "out": "voice-bank-b2.html",
        "kicker": "物理语音批 · 第二批",
        "title": "第二批 53 个知识点，159 段讲解语音",
        "sub": "初中九年级电与磁、信息与能源 35 点，加高中必修一前 18 点。语音为 MP3 48 kbps，总时长约 {mins:.1f} 分钟；动画与题库随后接入课程页。",
    },
    "3": {
        "data": "voice_bank_batch3.json",
        "out": "voice-bank-b3.html",
        "kicker": "物理语音批 · 第三批",
        "title": "第三批 52 个知识点，156 段讲解语音",
        "sub": "高中必修一最后 1 点、必修二、必修三、选择性必修一前段，共 52 点。语音为 MP3 48 kbps，总时长约 {mins:.1f} 分钟；动画与题库随后接入课程页。",
    },
    "4": {
        "data": "voice_bank_batch4.json",
        "out": "voice-bank-b4.html",
        "kicker": "物理语音批 · 第四批",
        "title": "第四批 51 个知识点，153 段讲解语音",
        "sub": "高中选择性必修一后段、选择性必修二、选择性必修三，共 51 点。语音为 MP3 48 kbps，总时长约 {mins:.1f} 分钟；动画与题库随后接入课程页。",
    },
}[BATCH]
DATA = json.loads((ROOT / "data" / CFG["data"]).read_text(encoding="utf-8"))
TOTAL = sum(len(p["steps"]) for p in DATA)
SIZE = sum(
    (ROOT / "audio" / p["id"] / f"step{i}.mp3").stat().st_size
    for p in DATA for i in range(1, len(p["steps"]) + 1)
) / 1048576
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def duration(path):
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", str(path)],
                       capture_output=True, text=True, errors="replace")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", r.stderr)
    if not m:
        return 0.0
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


TOTAL_SEC = sum(
    duration(ROOT / "audio" / p["id"] / f"step{i}.mp3")
    for p in DATA for i in range(1, len(p["steps"]) + 1)
)

cards = []
for p in DATA:
    rows = []
    for i, s in enumerate(p["steps"], 1):
        rows.append(f"""
        <div class="row">
          <div class="row-head"><span class="num">{i}</span><b>{html.escape(s['label'])}</b></div>
          <p>{html.escape(s['narration'])}</p>
          <audio controls preload="metadata" src="audio/{p['id']}/step{i}.mp3"></audio>
        </div>""")
    cards.append(f"""
    <section class="card point">
      <div class="point-head">
        <span class="unit">{html.escape(p['unit'])}</span>
        <h2>{html.escape(p['name'])}</h2>
        <span class="id">{p['id']}</span>
      </div>
      {''.join(rows)}
    </section>""")

page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>物理语音批 · 第一批</title>
<style>
  *{{box-sizing:border-box}}
  :root{{--ink:#22314a;--muted:#7c8aa3;--line:#dce5f2;--paper:#eef3fb;--blue:#1d4ed8;--blue-dark:#1e3a8a}}
  body{{margin:0;background:radial-gradient(900px 420px at 50% -160px,#eef5ff,rgba(238,245,255,0) 65%),var(--paper);
    color:var(--ink);font-family:"PingFang SC","Microsoft YaHei",system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
  .app{{max-width:900px;margin:0 auto;padding:20px 14px 40px}}
  .card{{background:#fff;border:1px solid var(--line);border-radius:20px;box-shadow:0 12px 34px rgba(40,60,110,.07)}}
  .hero{{padding:20px;background:linear-gradient(155deg,#fff,#f7faff 60%,#f2f7fb)}}
  .kicker{{font-size:10px;font-weight:800;letter-spacing:.7px;color:var(--blue);background:#e8effc;border-radius:999px;padding:5px 10px}}
  h1{{font-size:23px;font-weight:900;margin:12px 0 6px;letter-spacing:-.4px}}
  .sub{{font-size:12px;color:var(--muted);line-height:1.7;margin:0}}
  .stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px}}
  .stat{{background:#f8fafc;border:1px solid #e8eef5;border-radius:13px;padding:10px 8px;text-align:center}}
  .stat b{{display:block;font-size:20px;font-weight:900;color:var(--blue-dark)}}
  .stat span{{display:block;font-size:10px;color:var(--muted);margin-top:2px}}
  .top{{display:flex;justify-content:space-between;align-items:center;gap:10px;margin:0 2px 10px}}
  .back{{font-size:11px;font-weight:800;color:var(--blue-dark);text-decoration:none;background:#fff;border:1px solid #e5e7ef;border-radius:999px;padding:8px 13px}}
  .point{{padding:16px;margin-top:12px}}
  .point-head{{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin-bottom:8px}}
  .unit{{font-size:10px;font-weight:800;color:var(--blue);background:#e8effc;border-radius:999px;padding:4px 8px}}
  .point-head h2{{font-size:16px;margin:0;font-weight:900;flex:1}}
  .id{{font-size:10px;color:var(--muted);font-family:monospace}}
  .row{{border-top:1px dashed #e5e7ef;padding:11px 0 4px}}
  .row-head{{display:flex;align-items:center;gap:8px;font-size:13px;margin-bottom:5px}}
  .num{{width:20px;height:20px;border-radius:50%;background:#e7effc;color:var(--blue-dark);font-size:11px;font-weight:900;
    display:grid;place-items:center;flex:none}}
  .row p{{font-size:12px;line-height:1.75;color:#5b6b82;margin:0 0 8px;padding-left:28px}}
  audio{{width:100%;height:36px;margin-bottom:6px}}
  .note{{margin-top:14px;font-size:10.5px;color:var(--muted);line-height:1.8;text-align:center}}
  @media(max-width:560px){{.app{{padding:12px 10px 28px}}.hero{{padding:15px}}h1{{font-size:19px}}.point{{padding:13px}}}}
</style>
</head>
<body>
<div class="app">
  <div class="top"><a class="back" href="index.html">← 返回总目录</a><a class="back" href="junior.html">初中样例 →</a></div>
  <section class="card hero">
    <span class="kicker">{CFG['kicker']}</span>
    <h1>{CFG['title']}</h1>
    <p class="sub">{CFG['sub'].format(mins=TOTAL_SEC/60)}</p>
    <div class="stats">
      <div class="stat"><b>{len(DATA)}</b><span>知识点</span></div>
      <div class="stat"><b>{TOTAL}</b><span>段语音</span></div>
      <div class="stat"><b>{SIZE:.1f} MB</b><span>MP3 体积</span></div>
    </div>
  </section>
  {''.join(cards)}
  <p class="note">讲解稿同步保存在 data/{CFG['data']} · 语音路径 audio/</p>
</div>
</body>
</html>"""
(ROOT / CFG["out"]).write_text(page, encoding="utf-8")
print(f"{CFG['out']} 已生成：{len(DATA)} 点 / {TOTAL} 段 / {SIZE:.1f} MB")
