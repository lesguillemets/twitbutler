#!/usr/bin/env python3
import urllib.request as req
from urllib.parse import quote
import json
from .yahoo_geo import geocode
try:
    from .consts import yahoo_info
except ImportError as e:
    yahoo_info = {
        'app_id' : os.environ['yahoo_app_id'],
        'secret' : os.environ['yahoo_app_secret'],
    }

rainurl = "http://weather.olp.yahooapis.jp/v1/place"

def rainfall(query):
    geo = geocode(query)
    if geo is None:
        raise ValueError("Location not found.")
    else:
        geo = geo[0]
    
    coordinates = geo['Geometry']['Coordinates']
    para = "?appid={}&output=json&coordinates={}".format(
        yahoo_info['app_id'],
        coordinates
    )
    with req.urlopen(rainurl+para) as u:
        data = json.loads(u.read().decode('utf-8'))
    
    try:
        raindata = data['Feature'][0]['Property']['WeatherList']['Weather'][0]
    except IndexError as e:
        return None
    
    return (geo, raindata)

if __name__ == "__main__":
    print(rainfall("飛騨"))
