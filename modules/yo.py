#!/usr/bin/env python3

import urllib.request as req
from urllib.parse import urlencode
import json
import os

YOURL = "https://api.justyo.co/yo/"

try:
    from .consts import yo_token, yo_username
except ImportError as e:
    yo_token = os.environ['yo_token']
    yo_username = os.environ['yo_username']

def yo(*args,**kwargs):
    queries = {"username" : yo_username,
         "api_token" : yo_token }
    if "link" in kwargs:
        queries['link'] = kwargs['link']
    elif "location" in kwargs:
        queries['location'] = kwargs['location']
    data = urlencode(queries).encode('utf-8')
    
    with req.urlopen(YOURL,data=data) as u:
        response = json.loads(u.read().decode('utf-8'))
    if response.get("success"):
        return "Yo-ed."
    return str(response.get("error"))
