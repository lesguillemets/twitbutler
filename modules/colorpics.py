#!/usr/bin/env python3
import PIL.Image as Image
import numpy as np
from io import BytesIO

def rgb_image(r,g,b,size=50) -> BytesIO :
    dat = np.array([r,g,b]*(size*size), dtype=np.uint8).reshape(
        size,size,3
    )
    
    img = Image.fromarray(dat)
    imgf = BytesIO()
    img.save(imgf, format='png')
    imgf.seek(0)
    return imgf
