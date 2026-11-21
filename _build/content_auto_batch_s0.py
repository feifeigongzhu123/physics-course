# -*- coding: utf-8 -*-
"""高中必修一自动生成课程：ps-4 ～ ps-21，共 18 点。"""
from content_auto_y import POINTS_AUTO_Y
from content_auto_z import POINTS_AUTO_Z
from content_auto_aa import POINTS_AUTO_AA
from content_auto_ab import POINTS_AUTO_AB

POINTS_AUTO_S0 = list(POINTS_AUTO_Y) + list(POINTS_AUTO_Z) + list(POINTS_AUTO_AA) + list(POINTS_AUTO_AB)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_S0]
    assert len(POINTS_AUTO_S0) == 18, len(POINTS_AUTO_S0)
    assert len(set(ids)) == 18
    print("auto senior batch 0:", len(POINTS_AUTO_S0), ids)
