# -*- coding: utf-8 -*-
import json, subprocess, tempfile, time, urllib.request
from pathlib import Path
from cdp_check import WS, wait_http, EDGE

ROOT = Path(r"D:\AI\ZCode\physics")
PORT = 9452
ud = tempfile.mkdtemp(prefix="edgeph_dbg_")
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
    ws.call("Page.navigate", {"url": (ROOT / "senior.html").as_uri()})
    time.sleep(2.0)

    def js(expr):
        r = ws.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        return r.get("result", {}).get("result", {}).get("value")

    js("window.__PH.open('ps-89',0)"); time.sleep(0.5)
    js("document.getElementById('openReal').click()"); time.sleep(0.4)
    print("cards", js("Array.from(document.querySelectorAll('#realQuestions .q')).map(e=>e.getAttribute('data-q')).join(',')"))
    js("document.querySelector('[data-q=\"ln2024-q9\"] .opt[data-i=\"0\"]').click()")
    js("document.querySelector('[data-q=\"ln2024-q9\"] .opt[data-i=\"1\"]').click()")
    print("selected", js("document.querySelectorAll('[data-q=\"ln2024-q9\"] .opt.selected').length"))
    print("store_before", js("JSON.stringify(window.__PH.store.answers['ln2024-q9'])"))
    js("document.querySelector('[data-q=\"ln2024-q9\"] .submit-answer').click()")
    time.sleep(0.2)
    print("store_after", js("JSON.stringify(window.__PH.store.answers['ln2024-q9'])"))
    print("verdict", js("document.querySelector('[data-q=\"ln2024-q9\"] .verdict').textContent"))
finally:
    try:
        proc.terminate(); proc.wait(timeout=5)
    except Exception:
        proc.kill()
