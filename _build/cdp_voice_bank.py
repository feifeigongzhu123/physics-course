# -*- coding: utf-8 -*-
"""语音试听页验收：51 个播放器、首段可播、时长可读。"""
import base64, json, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path

from cdp_check import WS, wait_http, EDGE

ROOT = Path(r"D:\AI\ZCode\physics")
PAGE = sys.argv[1] if len(sys.argv) > 1 else "voice-bank.html"
SHOT = sys.argv[2] if len(sys.argv) > 2 else "voice-bank-cdp.png"
PORT = 9446

ud = tempfile.mkdtemp(prefix="edgeph_vb_")
proc = subprocess.Popen(
    [EDGE, "--headless", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files",
     "--autoplay-policy=no-user-gesture-required",
     f"--remote-debugging-port={PORT}", f"--user-data-dir={ud}", "about:blank"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
try:
    wait_http(f"http://127.0.0.1:{PORT}/json/version")
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list") as r:
        page = next(t for t in json.loads(r.read()) if t["type"] == "page")
    ws = WS(page["webSocketDebuggerUrl"])
    ws.call("Page.enable"); ws.call("Runtime.enable")
    ws.call("Emulation.setDeviceMetricsOverride",
            {"width": 900, "height": 1400, "deviceScaleFactor": 1, "mobile": False})
    ws.call("Page.navigate", {"url": (ROOT / PAGE).as_uri()})
    time.sleep(2.5)

    def js(expr):
        r = ws.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        return r.get("result", {}).get("result", {}).get("value")

    print("audio count", js("document.querySelectorAll('audio').length"))
    print("first duration", js("document.querySelector('audio').duration"))
    print("errors", js("document.documentElement.getAttribute('data-js-errors')"))
    js("document.querySelector('audio').play()")
    time.sleep(2.0)
    print("playing", js("JSON.stringify({paused:document.querySelector('audio').paused,t:document.querySelector('audio').currentTime,d:document.querySelector('audio').duration})"))
    shot = ws.call("Page.captureScreenshot", {"format": "png"})
    (ROOT / "shots" / SHOT).write_bytes(base64.b64decode(shot["result"]["data"]))
finally:
    try:
        proc.terminate(); proc.wait(timeout=5)
    except Exception:
        proc.kill()
