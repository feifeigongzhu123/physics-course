# -*- coding: utf-8 -*-
"""物理样例课 CDP 验收：JS 错误、深链、场景、题库、音频、截图。"""
import base64
import json
import os
import socket
import struct
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ROOT = Path(r"D:\AI\ZCode\physics")
PORT = 9444


class WS:
    def __init__(self, url):
        rest = url[5:]
        hostport, path = rest.split("/", 1)
        host, port = hostport.split(":")
        self.sock = socket.create_connection((host, int(port)), timeout=15)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\n"
            f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.sock.recv(4096)
        self.buf = b""
        self.nid = 0

    def _rd(self, n):
        out = self.buf
        while len(out) < n:
            chunk = self.sock.recv(n - len(out))
            if not chunk:
                raise EOFError("socket closed")
            out += chunk
        self.buf = out[n:]
        return out[:n]

    def send(self, obj):
        data = json.dumps(obj).encode()
        header = bytearray([0x81])
        n = len(data)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", n)
        mask = os.urandom(4)
        header += mask
        self.sock.sendall(bytes(header) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def recv(self):
        while True:
            h = self._rd(2)
            opcode = h[0] & 0x0F
            ln = h[1] & 0x7F
            if ln == 126:
                ln = struct.unpack(">H", self._rd(2))[0]
            elif ln == 127:
                ln = struct.unpack(">Q", self._rd(8))[0]
            masked = h[1] & 0x80
            mask = self._rd(4) if masked else None
            payload = self._rd(ln)
            if masked:
                payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
            if opcode == 0x9:
                self.send({"pong": True})
                continue
            if opcode == 0x8:
                raise EOFError("ws closed")
            return json.loads(payload.decode("utf-8"))

    def call(self, method, params=None, timeout=20):
        self.nid += 1
        mid = self.nid
        self.send({"id": mid, "method": method, "params": params or {}})
        end = time.time() + timeout
        while time.time() < end:
            msg = self.recv()
            if msg.get("id") == mid:
                return msg
        raise TimeoutError(method)


def wait_http(url, timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                return r.read()
        except Exception:
            time.sleep(0.2)
    raise TimeoutError(url)


def main():
    ud = tempfile.mkdtemp(prefix="edgeph_cdp_")
    proc = subprocess.Popen(
        [
            EDGE, "--headless", "--disable-gpu", "--no-sandbox",
            "--allow-file-access-from-files", "--autoplay-policy=no-user-gesture-required",
            f"--remote-debugging-port={PORT}", f"--user-data-dir={ud}", "about:blank",
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        wait_http(f"http://127.0.0.1:{PORT}/json/version")
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list") as r:
            targets = json.loads(r.read())
        page = next(t for t in targets if t["type"] == "page")
        ws = WS(page["webSocketDebuggerUrl"])
        ws.call("Page.enable")
        ws.call("Runtime.enable")
        ws.call("Log.enable")
        ws.call("Emulation.setDeviceMetricsOverride",
                {"width": 900, "height": 1400, "deviceScaleFactor": 1, "mobile": False})

        def js(expr):
            r = ws.call("Runtime.evaluate",
                        {"expression": expr, "returnByValue": True, "awaitPromise": True})
            return r.get("result", {}).get("result", {}).get("value")

        for pg, ids in [("junior", ["pj-1", "pj-2", "pj-3"]),
                        ("senior", ["ps-1", "ps-2", "ps-3"])]:
            url = (ROOT / f"{pg}.html").as_uri()
            ws.call("Page.navigate", {"url": url})
            time.sleep(2.0)
            print("==", pg, "ready", js("document.documentElement.getAttribute('data-ready')"),
                  "errors", js("document.documentElement.getAttribute('data-js-errors')"),
                  "points", js("window.__PH ? window.__PH.data.length : -1"))
            for pid in ids:
                for st in (0, 1, 2):
                    js(f"window.__PH.open('{pid}', {st})")
                    time.sleep(0.75)
                    op = js(f"getComputedStyle(document.getElementById('scene-{pid}')).opacity")
                    cls = js(f"document.getElementById('scene-{pid}').className")
                    cap = js("document.getElementById('caption').textContent")
                    print(f"{pid} step{st+1} cls={cls} opacity={op} cap={cap[:24]}")
                # 答第一题
                js("document.querySelectorAll('#questions .q .opt')[0].click()")
                time.sleep(0.3)
                verdict = js("document.querySelector('#questions .q .verdict').textContent")
                qs = js("document.querySelectorAll('#questions .q').length")
                print(pid, "questions", qs, "verdict", verdict)
                shot = ws.call("Page.captureScreenshot", {"format": "png"})
                out = ROOT / "shots" / f"cdp-{pid}.png"
                out.write_bytes(base64.b64decode(shot["result"]["data"]))
            # 首页截图
            js("window.__PH.home()")
            time.sleep(0.5)
            shot = ws.call("Page.captureScreenshot", {"format": "png"})
            (ROOT / "shots" / f"cdp-{pg}-home.png").write_bytes(base64.b64decode(shot["result"]["data"]))

        # 音频播放检查（初中 pj-1 第 1 步）
        ws.call("Page.navigate", {"url": (ROOT / "junior.html").as_uri()})
        time.sleep(2.0)
        js("window.__PH.open('pj-1', 0)")
        time.sleep(0.4)
        js("document.getElementById('play').click()")
        time.sleep(3.0)
        print("AUDIO", js("JSON.stringify(window.__PH.current)"))
        print("ACTIVE", js("window.__PH.activeAudios()"))
        print("BANNED", js("document.documentElement.innerHTML.indexOf('离线播放')"))
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
