# -*- coding: utf-8 -*-
"""第一批自动生成课程：pj-4 ～ pj-23，共 20 点。"""
from content_auto_a import POINTS_AUTO_A
from content_auto_b import POINTS_AUTO_B
from content_auto_c import POINTS_AUTO_C
from content_auto_d import POINTS_AUTO_D

POINTS_AUTO_B1 = list(POINTS_AUTO_A) + list(POINTS_AUTO_B) + list(POINTS_AUTO_C) + list(POINTS_AUTO_D)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_B1]
    assert len(POINTS_AUTO_B1) == 20, len(POINTS_AUTO_B1)
    assert len(set(ids)) == 20
    print("auto batch 1:", len(POINTS_AUTO_B1), ids)
