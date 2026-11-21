# -*- coding: utf-8 -*-
"""在局域网内分享物理动画课。

用法：python serve.py [端口]
默认 8000，绑定 0.0.0.0；终端会打印本机与局域网地址。
"""
import os
import socket
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".svg": "image/svg+xml",
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg",
    }

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    os.chdir(ROOT)
    try:
        httpd = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    except OSError as e:
        print(f"端口 {PORT} 无法启动：{e}")
        print(f"可以换一个端口，例如：python serve.py {PORT + 1}")
        return
    ip = lan_ip()
    print("物理动画课已启动")
    print(f"  本机访问：http://127.0.0.1:{PORT}/")
    print(f"  局域网：  http://{ip}:{PORT}/")
    print("手机与电脑连接同一 Wi-Fi，打开局域网地址即可。")
    print("按 Ctrl+C 停止。")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
