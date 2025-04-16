import numpy as np
import rawpy
import OpenImageIO as oiio
import matplotlib.pyplot as plt


# Rawpy (raw image)
def read_raw(fileName):
    with rawpy.imread(fileName) as raw:
        img_1 = raw.raw_image.copy()
        return img_1
    

# OpenImageIO (tif image)
def read_tif(fileName):
    inp = oiio.ImageInput.open(fileName)
    if inp:
        spec = inp.spec()
        xres = spec.width
        yres = spec.height
        nchannels = spec.nchannels
        pixels = inp.read_image(0, 0, 0, nchannels, "float32")
        inp.close()
        if nchannels == 1:
            return np.array(pixels).reshape(yres, xres)
        else:
            return np.array(pixels).reshape(yres, xres, nchannels)
        
        
def read_img(fileName):
    if fileName.endswith(".tif" or ".tiff"):
        img = read_tif(fileName)
    else:
        img = read_raw(fileName)
    return img
        
        
def main():
    img_1_path = "a7c2无压缩.ARW"
    img_2_path = "a7c2无压缩_CaptureOne.dng"
    crop_flag = True
    crop_index = 0
    
    img_1 = read_img(img_1_path)
    img_2 = read_img(img_2_path)
    
    print(
        f"img_1 shape: {img_1.shape}, dtype: {img_1.dtype}, max: {np.max(img_1)}, min: {np.min(img_1)}"
    )
    print(
        f"img_2 shape: {img_2.shape}, dtype: {img_2.dtype}, max: {np.max(img_2)}, min: {np.min(img_2)}"
    )
    
    # crop raw image
    left = 12
    right = 20
    top = 8
    bottom = 8
    if crop_flag:
        if crop_index == 0:
            img_1 = img_1[top:-bottom, left:-right]
        elif crop_index == 1:  
            img_2 = img_2[top:-bottom, left:-right]


    img_1 = img_1.astype(np.float64)
    img_2 = img_2.astype(np.float64)

    # ratio
    ratio_img = img_2 / img_1
    print(
        f"ratio_img shape: {ratio_img.shape}, dtype: {ratio_img.dtype}, max: {np.max(ratio_img)}, min: {np.min(ratio_img)}, mean: {np.mean(ratio_img)}"
    )

    # difference
    diff_img = img_2 - img_1
    print(
        f"diff_img shape: {diff_img.shape}, dtype: {diff_img.dtype}, max: {np.max(diff_img)}, min: {np.min(diff_img)}, mean: {np.mean(diff_img)}"
    )
    

if __name__ == "__main__":
    main()
