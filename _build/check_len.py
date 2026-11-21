# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, r"D:\AI\ZCode\physics\_build")
from content_junior import POINTS_JUNIOR
from content_senior import POINTS_SENIOR
for p in POINTS_JUNIOR + POINTS_SENIOR:
    for q in p["questions"]:
        n = len(q["explanation"])
        if not (60 <= n <= 110):
            print(p["id"], q["id"], n)
