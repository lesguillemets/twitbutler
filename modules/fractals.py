#!/usr/bin/env python3

import numpy as np
import PIL.Image as Image
from io import BytesIO
import colorsys

def julia(sizex:int=200, sizey:int=200,
          c : complex = -1.24 + 0.075j,
          upperleft : (float,float) = (-0.3,-0.3),
          bottomright:(float,float) = (0.3,0.3),
          threshold : float = 4, repeat : int = 300) -> BytesIO:
    
    data = np.zeros(3*sizex*sizey, dtype=np.uint8).reshape(
        sizex, sizey, 3
    )
    dx = (bottomright[0] - upperleft[0]) / sizex
    dy = (bottomright[1] - upperleft[1]) / sizey
    # f = lambda z: z*z + c this is slow.
    
    def julia_val(z):
        for n in range(repeat):
            z = z*z+c # update
            if (z.real**2 + z.imag**2) > threshold:
                # div
                return n
        return -1
    
    for xn in range(sizex):
        for yn in range(sizey):
            x = upperleft[0] + dx*xn
            y = upperleft[1] + dy*yn
            s = julia_val(complex(x,y))
            if s < 0:
                # diversion!
                color =  (0,0,0)
            else:
                h = s/repeat
                rgb = colorsys.hsv_to_rgb(h,1,1)
                color = list(map(lambda x: int(x*256), rgb))
            data[xn][yn] = color
    
    img = Image.fromarray(data)
    imgf = BytesIO()
    img.save(imgf, format='png')
    imgf.seek(0)
    return imgf

if __name__ == "__main__":
    julia()
