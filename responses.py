#!/usr/bin/env python3

class MediaResponse(object):
    def __init__(self, text:str, media:'BytesIO'):
        self.text = text
        self.media = media

class DeleteResponse(object):
    def __init__(self,data:"twitdata"):
        self.data = data
