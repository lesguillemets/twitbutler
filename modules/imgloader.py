#!/usr/bin/env python3
import PIL.Image as Image
from io import BytesIO
import urllib.request as req

def tw_load_img(url : str, maxsize = None) -> Image:
    large_url = url+ ":large"
    ext = url.split('.')[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'gif']:
        raise CantHandleException("Can't handle ext {}.".format(ext))
    img_req = req.Request(
        large_url, headers={
            'Content-Type':'image/{}'.format(ext)
        }
    )
    try:
        with req.urlopen(img_req) as f:
            data = BytesIO(f.read())
            data.seek(0)
    except Exception as e:
        raise CantURLOpenException(e)
    
    try:
        img = Image.open(data)
    except Exception as e:
        raise CantOpenException(e)
    if maxsize:
        longer = max(img.size)
        if longer > maxsize:
            img = img.resize(
                tuple(map(lambda s: int(s*maxsize/longer), img.size))
            )
    return img

class CantHandleException(Exception):
    pass

class CantURLOpenException(Exception):
    pass

class CantOpenException(Exception):
    pass
