# -*- coding: utf-8 -*-
import sys, io, xml.etree.ElementTree as ET
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = Path(r"D:\AI\ZCode\physics\_build\scenes")
bad = []
for i in range(1, 86):
    f = root / f"pj-{i}.svg"
    try:
        text = f.read_text(encoding="utf-8")
        tree = ET.fromstring(text)
        zones = text.count('data-zone=')
        has_style = "<style>" in text
        tag = tree.tag.split('}')[-1]
        ok = tag == "svg" and 'viewBox="0 0 900 620"' in text and zones >= 3 and has_style
        print(f"pj-{i}", "ok" if ok else "WARN", "zones", zones, "style", has_style)
        if not ok:
            bad.append(f"pj-{i}")
    except Exception as e:
        print(f"pj-{i}", "ERROR", e)
        bad.append(f"pj-{i}")
print("BAD", bad)
