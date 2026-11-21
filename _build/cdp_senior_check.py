# -*- coding: utf-8 -*-
"""高中页验收：23 点、场景、题目、MP3。"""
import base64, json, subprocess, tempfile, time, urllib.request
from pathlib import Path
from cdp_check import WS, wait_http, EDGE

ROOT = Path(r"D:\AI\ZCode\physics")
PORT = 9449
ud = tempfile.mkdtemp(prefix="edgeph_s_")
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
            {"width": 900, "height": 1450, "deviceScaleFactor": 1, "mobile": False})
    ws.call("Page.navigate", {"url": (ROOT / "senior.html").as_uri()})
    time.sleep(2.2)

    def js(expr):
        r = ws.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        return r.get("result", {}).get("result", {}).get("value")

    print("READY", js("document.documentElement.getAttribute('data-ready')"),
          "ERRORS", js("document.documentElement.getAttribute('data-js-errors')"),
          "POINTS", js("window.__PH ? window.__PH.data.length : -1"),
          "SCENES", js("document.querySelectorAll('.scene').length"))
    for pid in ["ps-102", "ps-110", "ps-116", "ps-121", "ps-124"]:
        for st in (0, 1, 2):
            js(f"window.__PH.open('{pid}', {st})")
            time.sleep(0.6)
            print(pid, st + 1,
                  "op", js(f"getComputedStyle(document.getElementById('scene-{pid}')).opacity"),
                  "reads", js("document.querySelectorAll('#readouts .readout').length"))
        print(pid, "questions", js("document.querySelectorAll('#questions .q').length"))
        shot = ws.call("Page.captureScreenshot", {"format": "png"})
        (ROOT / "shots" / f"senior-{pid}.png").write_bytes(base64.b64decode(shot["result"]["data"]))
    js("window.__PH.open('ps-102', 0)")
    time.sleep(0.4)
    js("document.getElementById('play').click()")
    time.sleep(2.2)
    print("AUDIO", js("JSON.stringify(window.__PH.current)"))
finally:
    try:
        proc.terminate(); proc.wait(timeout=5)
    except Exception:
        proc.kill()
