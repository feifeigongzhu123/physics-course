# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\AI\ZCode\physics\_build\scenes\ps-1.svg")
s = p.read_text(encoding="utf-8")
s = s.replace('y1="146.2" x2="270" y2="146.2"', 'y1="144.2" x2="270" y2="144.2"')
s = s.replace('y1="196.6" x2="390" y2="196.6"', 'y1="192.6" x2="390" y2="192.6"')
s = s.replace('y1="279.4" x2="510" y2="279.4"', 'y1="273.4" x2="510" y2="273.4"')
s = s.replace('y1="394.6" x2="630" y2="394.6"', 'y1="386.6" x2="630" y2="386.6"')
s = s.replace('cy="146.2"', 'cy="144.2"').replace('cy="196.6"', 'cy="192.6"')
s = s.replace('cy="279.4"', 'cy="273.4"').replace('cy="394.6"', 'cy="386.6"')
s = s.replace('x1="510" y1="279.4"', 'x1="510" y1="273.4"')
s = s.replace('M552 279.4', 'M552 273.4')
p.write_text(s, encoding="utf-8")
print("remaining", s.count("279.4"), s.count("394.6"))
