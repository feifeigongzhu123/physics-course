# -*- coding: utf-8 -*-
import base64, json, subprocess, tempfile, time, urllib.request
from pathlib import Path
from cdp_check import WS, wait_http, EDGE

ROOT = Path(r"D:\AI\ZCode\physics")
PORT = 9451
ud = tempfile.mkdtemp(prefix="edgeph_rimg_")
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
            {"width": 900, "height": 1600, "deviceScaleFactor": 1, "mobile": False})
    ws.call("Page.navigate", {"url": (ROOT / "senior.html").as_uri()})
    time.sleep(2.2)

    def js(expr):
        r = ws.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        return r.get("result", {}).get("result", {}).get("value")

    print("errors", js("document.documentElement.getAttribute('data-js-errors')"))
    js("window.__PH.open('ps-6',0)")
    time.sleep(0.8)
    print("ps-6 real", js("window.__PH.data.find(p=>p.id==='ps-6').realQuestions.length"))
    js("document.getElementById('openReal').click()")
    time.sleep(0.6)
    print("tag", js("document.querySelector('[data-q=\"ln2021-q3\"] .real-tag').textContent"))
    print("source", js("document.querySelector('[data-q=\"ln2021-q3\"] .source').textContent"))
    print("img", js("(function(){var i=document.querySelector('[data-q=\"ln2021-q3\"] .q-image');return i?i.naturalWidth+'x'+i.naturalHeight:'none'})()"))
    print("opts", js("document.querySelectorAll('[data-q=\"ln2021-q3\"] .opt').length"))
    js("document.querySelector('[data-q=\"ln2021-q3\"] .opt[data-i=\"0\"]').click()")
    time.sleep(0.3)
    print("verdict", js("document.querySelector('[data-q=\"ln2021-q3\"] .verdict').textContent"))
    js("document.getElementById('realBank').scrollIntoView({block:'start'})")
    time.sleep(0.3)
    shot = ws.call("Page.captureScreenshot", {"format": "png"})
    (ROOT / "shots" / "real-image.png").write_bytes(base64.b64decode(shot["result"]["data"]))

    js("window.__PH.open('ps-89',0)")
    time.sleep(0.6)
    print("ps-89 real", js("window.__PH.data.find(p=>p.id==='ps-89').realQuestions.length"))
    js("document.getElementById('openReal').click()")
    time.sleep(0.6)
    print("multi img", js("(function(){var i=document.querySelector('[data-q=\"ln2024-q9\"] .q-image');return i?i.naturalWidth+'x'+i.naturalHeight:'none'})()"))
    js("document.querySelector('[data-q=\"ln2024-q9\"] .opt[data-i=\"0\"]').click()")
    js("document.querySelector('[data-q=\"ln2024-q9\"] .opt[data-i=\"2\"]').click()")
    js("document.querySelector('[data-q=\"ln2024-q9\"] .submit-answer').click()")
    time.sleep(0.3)
    print("multi verdict", js("document.querySelector('[data-q=\"ln2024-q9\"] .verdict').textContent"))
    print("errors_end", js("document.documentElement.getAttribute('data-js-errors')"))
finally:
    try:
        proc.terminate(); proc.wait(timeout=5)
    except Exception:
        proc.kill()
