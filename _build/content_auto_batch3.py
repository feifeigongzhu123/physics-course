# -*- coding: utf-8 -*-
"""第三批自动生成课程：pj-44 ～ pj-63，共 20 点。"""
from content_auto_i import POINTS_AUTO_I
from content_auto_j import POINTS_AUTO_J
from content_auto_k import POINTS_AUTO_K
from content_auto_l import POINTS_AUTO_L

POINTS_AUTO_B3 = list(POINTS_AUTO_I) + list(POINTS_AUTO_J) + list(POINTS_AUTO_K) + list(POINTS_AUTO_L)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_B3]
    assert len(POINTS_AUTO_B3) == 20, len(POINTS_AUTO_B3)
    assert len(set(ids)) == 20
    print("auto batch 3:", len(POINTS_AUTO_B3), ids)
