# -*- coding: utf-8 -*-
"""高中第三批自动生成课程：ps-62 ～ ps-81，共 20 点。"""
from content_auto_ag import POINTS_AUTO_AG
from content_auto_ah import POINTS_AUTO_AH
from content_auto_ai import POINTS_AUTO_AI
from content_auto_aj import POINTS_AUTO_AJ

POINTS_AUTO_S3 = list(POINTS_AUTO_AG) + list(POINTS_AUTO_AH) + list(POINTS_AUTO_AI) + list(POINTS_AUTO_AJ)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_S3]
    assert len(POINTS_AUTO_S3) == 20, len(POINTS_AUTO_S3)
    assert len(set(ids)) == 20
    print("auto senior batch 3:", len(POINTS_AUTO_S3), ids)
