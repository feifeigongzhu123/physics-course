# -*- coding: utf-8 -*-
"""高中第一批自动生成课程：ps-22 ～ ps-41，共 20 点。"""
from content_auto_q import POINTS_AUTO_Q
from content_auto_r import POINTS_AUTO_R
from content_auto_s import POINTS_AUTO_S
from content_auto_t import POINTS_AUTO_T

POINTS_AUTO_S1 = list(POINTS_AUTO_Q) + list(POINTS_AUTO_R) + list(POINTS_AUTO_S) + list(POINTS_AUTO_T)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_S1]
    assert len(POINTS_AUTO_S1) == 20, len(POINTS_AUTO_S1)
    assert len(set(ids)) == 20
    print("auto senior batch 1:", len(POINTS_AUTO_S1), ids)
