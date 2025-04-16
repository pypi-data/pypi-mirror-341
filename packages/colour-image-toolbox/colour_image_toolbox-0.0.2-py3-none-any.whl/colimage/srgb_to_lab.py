import numpy as np


Matrix_sRGB_to_XYZ = np.array(
    [
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ]
)


def srgb_to_lab(RGB):
    # RGB: (3, ), range from 0 to 1
    # convert to linear sRGB
    RGB = np.where(RGB <= 0.04045, RGB / 12.92, ((RGB + 0.055) / 1.055) ** 2.4)
    # convert to XYZ
    XYZ = np.dot(Matrix_sRGB_to_XYZ, RGB)
    XYZ_w = np.dot(Matrix_sRGB_to_XYZ, np.array([1, 1, 1]))
    # convert to CIELAB
    XYZ_ratio = XYZ / XYZ_w
    XYZ_ratio = np.where(
        XYZ_ratio > 0.008856, XYZ_ratio ** (1 / 3), (XYZ_ratio * 7.787) + (16 / 116)
    )
    L = (116 * XYZ_ratio[1]) - 16
    a = 500 * (XYZ_ratio[0] - XYZ_ratio[1])
    b = 200 * (XYZ_ratio[1] - XYZ_ratio[2])
    return np.array([L, a, b])


if __name__ == "__main__":
    # Test the function with an example RGB value
    RGB = np.array([0.5, 0.5, 0.5])  # Example RGB value (normalized to [0, 1])
    lab = srgb_to_lab(RGB)
    print("Lab:", lab)
