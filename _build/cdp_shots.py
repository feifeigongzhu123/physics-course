# -*- coding: utf-8 -*-
"""逐步截图 + 手机布局检查。"""
import base64
import json
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

from cdp_check import WS, wait_http, EDGE

ROOT = Path(r"D:\AI\ZCode\physics")
PORT = 9445


def main():
    ud = tempfile.mkdtemp(prefix="edgeph_shots_")
    proc = subprocess.Popen(
        [EDGE, "--headless", "--disable-gpu", "--no-sandbox",
         "--allow-file-access-from-files", "--autoplay-policy=no-user-gesture-required",
         f"--remote-debugging-port={PORT}", f"--user-data-dir={ud}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        wait_http(f"http://127.0.0.1:{PORT}/json/version")
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list") as r:
            page = next(t for t in json.loads(r.read()) if t["type"] == "page")
        ws = WS(page["webSocketDebuggerUrl"])
        ws.call("Page.enable")
        ws.call("Runtime.enable")
        ws.call("Emulation.setDeviceMetricsOverride",
                {"width": 900, "height": 1450, "deviceScaleFactor": 1, "mobile": False})

        def js(expr):
            r = ws.call("Runtime.evaluate",
                        {"expression": expr, "returnByValue": True, "awaitPromise": True})
            return r.get("result", {}).get("result", {}).get("value")

        for pg, ids in [("junior", ["pj-1", "pj-2", "pj-3"]),
                        ("senior", ["ps-1", "ps-2", "ps-3"])]:
            ws.call("Page.navigate", {"url": (ROOT / f"{pg}.html").as_uri()})
            time.sleep(2.0)
            for pid in ids:
                for st in (0, 1, 2):
                    js(f"window.__PH.open('{pid}', {st})")
                    time.sleep(0.9)
                    cap = js("document.getElementById('caption').textContent")
                    if pid == "pj-2" and st == 2:
                        print("CAPTION pj-2 s3:", cap)
                    shot = ws.call("Page.captureScreenshot", {"format": "png"})
                    (ROOT / "shots" / f"step-{pid}-s{st+1}.png").write_bytes(
                        base64.b64decode(shot["result"]["data"]))

        # 手机 390px：两页各一个点
        ws.call("Emulation.setDeviceMetricsOverride",
                {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True})
        for pg, pid in [("junior", "pj-3"), ("junior", "pj-1"), ("senior", "ps-3")]:
            ws.call("Page.navigate", {"url": (ROOT / f"{pg}.html").as_uri() + "?debug=1"})
            time.sleep(2.0)
            for st in (0, 1, 2):
                js(f"window.__PH.open('{pid}', {st})")
                time.sleep(0.9)
                sw = js("document.body.scrollWidth")
                cw = js("document.documentElement.clientWidth")
                sl = js("document.getElementById('stageBox').scrollLeft")
                print("MOBILE", pg, pid, "step", st + 1, "scrollWidth", sw, "client", cw, "stageScroll", sl)
            shot = ws.call("Page.captureScreenshot", {"format": "png"})
            (ROOT / "shots" / f"mobile-{pid}.png").write_bytes(
                base64.b64decode(shot["result"]["data"]))
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
