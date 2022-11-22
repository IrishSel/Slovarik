from collections import defaultdict
import matplotlib.pyplot as plt
from skimage .measure import regionprops, label
import numpy as np
import math

def count_lakes_and_bays(region):
    symbol = ~region.image
    lb = label(symbol)
    regs = regionprops(lb)
    lakes = 0
    bays = 0
    for reg in regionprops(lb):
        flag = True
        for y, x in reg.coords:
            if y == 0 or x == 0 or y == region.image.shape[0] - 1 or x == region.image.shape[1] - 1:
                flag = False
                break
        lakes += int(flag)
        bays += int(not flag)
    return lakes, bays

def has_vline(region):
    return 1. in region.image.mean(0)


def recognize (im_region):
    result = defaultdict(lambda: 0)
    labeled = label(im_region)
    regionss = regionprops(labeled)

    for region in regionss:
        lakes, bays = count_lakes_and_bays(region)
        if lakes == 0:
            if np.all(region.image):
                result["-"] += 1
            elif has_vline(region):
                result["1"] += 1
            elif bays == 2:
                result["/"] += 1
            elif math.floor(region.orientation * 10) == 15:
                result["W"] += 1
            elif region.eccentricity > 0.65:
                result["X"] += 1
            else:
                result["*"] += 1
        elif lakes == 1:
            if bays == 3:
                result["A"] += 1
            elif bays == 4:
                result["0"] += 1
            elif region.eccentricity > 0.65:
                result["P"] += 1
            else:
                result["D"] += 1
        elif lakes == 2:
            if has_vline(region) and bays == 2:
                result["B"] += 1
            else:
                result["8"] += 1
        else:
            result["unknown"] += 1
    return result

im = plt.imread("symbols.png")
im = np.mean(im, 2)
im[im > 0] = 1

lb = label(im)
rec = recognize(im)

for i in rec.keys():
    print(i, rec[i])

plt.show()
