# -*- coding: utf-8 -*-
"""高中收尾批次：ps-122 ～ ps-124，共 3 点。"""
from content_auto_as import POINTS_AUTO_AS

POINTS_AUTO_S6 = list(POINTS_AUTO_AS)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_S6]
    assert len(POINTS_AUTO_S6) == 3, len(POINTS_AUTO_S6)
    print("auto senior batch 6:", len(POINTS_AUTO_S6), ids)
