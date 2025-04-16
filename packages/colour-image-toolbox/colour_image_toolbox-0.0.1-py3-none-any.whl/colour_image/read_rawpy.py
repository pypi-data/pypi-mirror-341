import rawpy
import numpy as np


file_name = r"C:\Users\Jackc\Desktop\镜头\DSC04781.ARW"
# file_name = r"C:\Users\Jackc\Desktop\Canon600D_0001.CR2"
# file_name = r"C:\Users\Jackc\Desktop\DSC05718.ARW"

with rawpy.imread(file_name) as raw:
    cwb = raw.camera_whitebalance
    dwb = raw.daylight_whitebalance
    print(dwb)
    ccm1 = raw.rgb_xyz_matrix

daylight_whitebalance = np.array(dwb[:3])

r_gain = daylight_whitebalance[0] / daylight_whitebalance[1]
g_gain = 1
b_gain = daylight_whitebalance[2] / daylight_whitebalance[1]

wb = np.diag([r_gain, g_gain, b_gain])

ccm = ccm1[0:3, 0:3]
print(ccm)

ccm_all = wb @ ccm

print(f"if_ccm_alL is able to be inverted: {np.linalg.cond(ccm_all) < 1 / np.finfo(float).eps}")

d65_xyz = np.array([0.95047, 1.00000, 1.08883])
d65_rgb = wb @ ccm @ d65_xyz

camera_rgb = np.array([1.0, 1.0, 1.0])

wb_inv = np.linalg.inv(wb)
print(wb)

camera_rgb_cat = wb_inv @ camera_rgb
print(camera_rgb_cat)

ccm_inv = np.linalg.inv(ccm)
print(ccm_inv)

xyz = ccm_inv @ camera_rgb_cat
print(xyz/xyz[1])

