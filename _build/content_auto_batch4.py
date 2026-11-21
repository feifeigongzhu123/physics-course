# -*- coding: utf-8 -*-
"""第四批自动生成课程：pj-64 ～ pj-85，共 22 点。"""
from content_auto_m import POINTS_AUTO_M
from content_auto_n import POINTS_AUTO_N
from content_auto_o import POINTS_AUTO_O
from content_auto_p import POINTS_AUTO_P

POINTS_AUTO_B4 = list(POINTS_AUTO_M) + list(POINTS_AUTO_N) + list(POINTS_AUTO_O) + list(POINTS_AUTO_P)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_B4]
    assert len(POINTS_AUTO_B4) == 22, len(POINTS_AUTO_B4)
    assert len(set(ids)) == 22
    print("auto batch 4:", len(POINTS_AUTO_B4), ids)
