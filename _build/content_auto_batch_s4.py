# -*- coding: utf-8 -*-
"""高中第四批自动生成课程：ps-82 ～ ps-101，共 20 点。"""
from content_auto_ak import POINTS_AUTO_AK
from content_auto_al import POINTS_AUTO_AL
from content_auto_am import POINTS_AUTO_AM
from content_auto_an import POINTS_AUTO_AN

POINTS_AUTO_S4 = list(POINTS_AUTO_AK) + list(POINTS_AUTO_AL) + list(POINTS_AUTO_AM) + list(POINTS_AUTO_AN)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_S4]
    assert len(POINTS_AUTO_S4) == 20, len(POINTS_AUTO_S4)
    assert len(set(ids)) == 20
    print("auto senior batch 4:", len(POINTS_AUTO_S4), ids)
