# -*- coding: utf-8 -*-
"""高中第二批自动生成课程：ps-42 ～ ps-61，共 20 点。"""
from content_auto_ac import POINTS_AUTO_AC
from content_auto_ad import POINTS_AUTO_AD
from content_auto_ae import POINTS_AUTO_AE
from content_auto_af import POINTS_AUTO_AF

POINTS_AUTO_S2 = list(POINTS_AUTO_AC) + list(POINTS_AUTO_AD) + list(POINTS_AUTO_AE) + list(POINTS_AUTO_AF)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_S2]
    assert len(POINTS_AUTO_S2) == 20, len(POINTS_AUTO_S2)
    assert len(set(ids)) == 20
    print("auto senior batch 2:", len(POINTS_AUTO_S2), ids)
