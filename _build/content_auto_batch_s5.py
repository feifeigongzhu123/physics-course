# -*- coding: utf-8 -*-
"""高中第五批自动生成课程：ps-102 ～ ps-121，共 20 点。"""
from content_auto_ao import POINTS_AUTO_AO
from content_auto_ap import POINTS_AUTO_AP
from content_auto_aq import POINTS_AUTO_AQ
from content_auto_ar import POINTS_AUTO_AR

POINTS_AUTO_S5 = list(POINTS_AUTO_AO) + list(POINTS_AUTO_AP) + list(POINTS_AUTO_AQ) + list(POINTS_AUTO_AR)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_S5]
    assert len(POINTS_AUTO_S5) == 20, len(POINTS_AUTO_S5)
    assert len(set(ids)) == 20
    print("auto senior batch 5:", len(POINTS_AUTO_S5), ids)
