# -*- coding: utf-8 -*-
"""验收：真题加练、单选/多选、逐项错因、重做。"""
import base64, json, subprocess, tempfile, time, urllib.request
from pathlib import Path
from cdp_check import WS, wait_http, EDGE

ROOT = Path(r"D:\AI\ZCode\physics")
PORT = 9450
ud = tempfile.mkdtemp(prefix="edgeph_real_")
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

    print("READY", js("document.documentElement.getAttribute('data-ready')"),
          "ERRORS", js("document.documentElement.getAttribute('data-js-errors')"))

    js("window.__PH.open('ps-116',0)")
    time.sleep(0.8)
    print("real count", js("window.__PH.data.find(p=>p.id==='ps-116').realQuestions.length"))
    print("teaser", js("document.getElementById('realBank').innerText.slice(0,80)"))
    js("document.getElementById('openReal').click()")
    time.sleep(0.4)
    print("real cards", js("document.querySelectorAll('#realQuestions .q').length"))
    # 多选 ln2024-q8 正确答案 BD
    js("document.querySelector('[data-q=\"ln2024-q8\"] .opt[data-i=\"1\"]').click()")
    js("document.querySelector('[data-q=\"ln2024-q8\"] .opt[data-i=\"3\"]').click()")
    print("selected", js("document.querySelectorAll('[data-q=\"ln2024-q8\"] .opt.selected').length"))
    js("document.querySelector('[data-q=\"ln2024-q8\"] .submit-answer').click()")
    time.sleep(0.3)
    print("multi verdict", js("document.querySelector('[data-q=\"ln2024-q8\"] .verdict').textContent"))
    print("notes ok", js("document.querySelectorAll('[data-q=\"ln2024-q8\"] .notes p.ok').length"),
          "notes total", js("document.querySelectorAll('[data-q=\"ln2024-q8\"] .notes p').length"))
    # 重做该题
    js("document.querySelector('[data-q=\"ln2024-q8\"] .redo').click()")
    time.sleep(0.3)
    print("redo hidden", js("document.querySelector('[data-q=\"ln2024-q8\"] .q-feedback').classList.contains('hidden')"),
          "opts enabled", js("!document.querySelector('[data-q=\"ln2024-q8\"] .opt').disabled"))
    # 单选 ln2021-q2 正确答案 C
    js("document.querySelector('[data-q=\"ln2021-q2\"] .opt[data-i=\"2\"]').click()")
    time.sleep(0.2)
    print("single verdict", js("document.querySelector('[data-q=\"ln2021-q2\"] .verdict').textContent"))
    print("wrong notes", js("document.querySelectorAll('[data-q=\"ln2021-q2\"] .notes p:not(.ok)').length"))
    # 重做基础 5 题
    js("window.__PH.open('ps-24',0)")
    time.sleep(0.5)
    js("document.querySelector('#questions .q .opt').click()")
    time.sleep(0.2)
    js("document.getElementById('redoAll').click()")
    time.sleep(0.3)
    print("base redo hidden", js("document.querySelector('#questions .q .q-feedback').classList.contains('hidden')"))
    print("base opts enabled", js("!document.querySelector('#questions .q .opt').disabled"))
    # 打开真题并截图
    js("if(document.getElementById('openReal')) document.getElementById('openReal').click()")
    time.sleep(0.4)
    js("document.getElementById('realBank').scrollIntoView({block:'start'})")
    time.sleep(0.4)
    shot = ws.call("Page.captureScreenshot", {"format": "png"})
    (ROOT / "shots" / "real-bank.png").write_bytes(base64.b64decode(shot["result"]["data"]))
    print("ERRORS_END", js("document.documentElement.getAttribute('data-js-errors')"))
finally:
    try:
        proc.terminate(); proc.wait(timeout=5)
    except Exception:
        proc.kill()
