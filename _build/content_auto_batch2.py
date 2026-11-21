# -*- coding: utf-8 -*-
"""第二批自动生成课程：pj-24 ～ pj-43，共 20 点。"""
from content_auto_e import POINTS_AUTO_E
from content_auto_f import POINTS_AUTO_F
from content_auto_g import POINTS_AUTO_G
from content_auto_h import POINTS_AUTO_H

POINTS_AUTO_B2 = list(POINTS_AUTO_E) + list(POINTS_AUTO_F) + list(POINTS_AUTO_G) + list(POINTS_AUTO_H)

if __name__ == "__main__":
    ids = [p["id"] for p in POINTS_AUTO_B2]
    assert len(POINTS_AUTO_B2) == 20, len(POINTS_AUTO_B2)
    assert len(set(ids)) == 20
    print("auto batch 2:", len(POINTS_AUTO_B2), ids)
