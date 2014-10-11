#!/usr/bin/env python3
import urllib.request as req
import os
from urllib.parse import quote
import json
try:
    from .consts import yahoo_info
except ImportError as e:
    yahoo_info = {
        'app_id' : os.environ['yahoo_app_id'],
        'secret' : os.environ['yahoo_app_secret'],
    }

geourl = "http://geo.search.olp.yahooapis.jp/OpenLocalPlatform/V1/geoCoder"

def geocode(query):
    para = "?appid={}&output=json&query={}".format(
        yahoo_info['app_id'],
        quote(query)
    )
    with req.urlopen(geourl+para) as u:
        data = json.loads(u.read().decode('utf-8'))
    if 'Feature' in data:
        return data['Feature']
    else:
        return None
