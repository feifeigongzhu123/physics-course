# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\AI\ZCode\physics\_build\app.js")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "    card.innerHTML =\n      '<div class=\"q-top\"><span class=\"q-idx\">' + esc(tag) + '</span>' +\n      (q.angle",
    "    var realTag = q.real ? '<span class=\"real-tag\">真题</span>' : '';\n    card.innerHTML =\n      '<div class=\"q-top\"><span class=\"q-idx\">' + esc(tag) + '</span>' + realTag +\n      (q.angle",
)
s = s.replace(
    "      '<p class=\"stem\">' + esc(q.stem) + '</p>' +\n      (multi ? '<div class=\"multi-tip\">",
    "      '<p class=\"stem\">' + esc(q.stem) + '</p>' +\n      (q.image ? '<img class=\"q-image\" src=\"' + esc(q.image) + '\" alt=\"原题配图\">' : '') +\n      (multi ? '<div class=\"multi-tip\">",
)
p.write_text(s, encoding="utf-8")
print("app image patched")
