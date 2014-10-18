#!/usr/bin/env python3
import PIL.Image as Image
import numpy as np
from . import imgloader
import time

def to_monochrome(orig_img, weights=(0.2989, 0.5970, 0.1140)):
    total_w = sum(weights)
    weights = tuple(map(lambda x:x/total_w, weights))
    img_ary = np.array(orig_img, dtype=np.uint8)
    
    for line in img_ary:
        for pixel in line:
            grayscale = sum(
                (pixel[i] * weights[i]) for i in range(3)
            )
            pixel[:] = [grayscale,grayscale,grayscale]
    
    return Image.fromarray(img_ary)
