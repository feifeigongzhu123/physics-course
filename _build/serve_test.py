# -*- coding: utf-8 -*-
import os, sys, threading, urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(r"D:\AI\ZCode\physics")
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
import serve  # noqa: E402

httpd = ThreadingHTTPServer(("127.0.0.1", 8765), serve.Handler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
try:
    for path in ["index.html", "voice-bank.html", "junior.html", "senior.html",
                 "audio/pj-1/step1.mp3", "audio/pj-4/step1.mp3", "data/junior.json"]:
        with urllib.request.urlopen(f"http://127.0.0.1:8765/{path}", timeout=5) as r:
            print(path, r.status, r.headers.get("Content-Type"), len(r.read()))
finally:
    httpd.shutdown()
