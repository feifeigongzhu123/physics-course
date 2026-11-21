# -*- coding: utf-8 -*-
"""390px 检查新增 20 点场景：页面无横向溢出、动画区可滚动。"""
import base64, json, subprocess, tempfile, time, urllib.request
from pathlib import Path
from cdp_check import WS, wait_http, EDGE

ROOT = Path(r"D:\AI\ZCode\physics")
PORT = 9448
ud = tempfile.mkdtemp(prefix="edgeph_m_")
proc = subprocess.Popen(
    [EDGE, "--headless", "--disable-gpu", "--no-sandbox", "--allow-file-access-from-files",
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
            {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True})
    ws.call("Page.navigate", {"url": (ROOT / "junior.html").as_uri()})
    time.sleep(2.2)

    def js(expr):
        r = ws.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        return r.get("result", {}).get("result", {}).get("value")

    for pid in ["pj-24", "pj-38", "pj-43"]:
        js(f"window.__PH.open('{pid}', 0)")
        time.sleep(0.9)
        print(pid, "body", js("document.body.scrollWidth"), "client", js("document.documentElement.clientWidth"),
              "stageScroll", js("document.getElementById('stageBox').scrollLeft"))
        shot = ws.call("Page.captureScreenshot", {"format": "png"})
        (ROOT / "shots" / f"mobile-auto-{pid}.png").write_bytes(base64.b64decode(shot["result"]["data"]))
finally:
    try:
        proc.terminate(); proc.wait(timeout=5)
    except Exception:
        proc.kill()
