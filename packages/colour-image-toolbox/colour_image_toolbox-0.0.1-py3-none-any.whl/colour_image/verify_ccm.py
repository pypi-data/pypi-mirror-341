"""
MakerNotes:WB_RGGBLevels: 2485 1024 1024 1651
MakerNotes:ColorMatrix: 954 -10 80 187 969 -132 105 -19 938
"""

import numpy as np


wb = np.array([2485 / 1024, 1, 1651 / 1024])
wb = np.diag(wb)

ccm = np.array([
    [954, -10, 80],
    [187, 969, -132],
    [105, -19, 938]
])
ccm = ccm / 1024

wb_inv = np.linalg.inv(wb)
ccm_inv = np.linalg.inv(ccm)

d65_xyz = np.array([0.95047, 1.00000, 1.08883])

d65_crgb_wb = ccm_inv @ d65_xyz

d65_crgb = wb_inv @ d65_crgb_wb
print(d65_crgb/d65_crgb[1])
