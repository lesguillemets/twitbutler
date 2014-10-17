#!/usr/bin/env python3
"""
 _____          _ _   _           _   _
|_   _|_      _(_) |_| |__  _   _| |_| | ___ _ __
  | | \ \ /\ / / | __| '_ \| | | | __| |/ _ \ '__|
  | |  \ V  V /| | |_| |_) | |_| | |_| |  __/ |
  |_|   \_/\_/ |_|\__|_.__/ \__,_|\__|_|\___|_|

"""
from twython import Twython
from twython import TwythonStreamer
from commands import Commands
from commands import MediaCommands
from commands import MediaResponse
import time
import os

try:
    import consts
except ImportError as e:
    class consts(object):
        keys = {
            'app' : {
                'api_key' : os.environ['twitter_api_key'],
                'api_secret' : os.environ['twitter_api_secret'],
            },
            'user' : {
                'access_token' : os.environ['twitter_access_token'],
                'access_token_secret' : (
                    os.environ['twitter_access_token_secret']
                ),
            },
        }


verb = False
cmd_prefix = "!"

if verb:
    log = print
else:
    log = lambda x: None

class TwitButler(object):
    
    def __init__(self, keys=consts.keys,me='exumbra_insoIem',logging=True):
        auth = [
            keys['app']['api_key'],
            keys['app']['api_secret'],
            keys['user']['access_token'],
            keys['user']['access_token_secret'],
        ]
        self.api = Twython(*auth)
        # self.api.update_status(status="tst3")
        
        self.streamer = TwythonStreamer(*auth)
        self.streamer.on_success = self.on_stream_success
        self.streamer.on_error = self.on_error
        self.me = me
        self.logging = logging
    
    def on_stream_success(self,data):
        if ('in_reply_to_screen_name' in data and
                data['in_reply_to_screen_name'] == self.me):
            try:
                log("____")
                log(data['text'])
                self.respond_to(data)
            except Exception as e:
                log(e)
                pass
    
    def respond_to(self,data):
        try:
            response = parse_command(data)
        except Exception as e:
            self.debug_log_tweet(e)
            return
        if isinstance(response,str):
            # respond with string only!
            self.api.update_status(
                status = (
                    '@' + data['user']['screen_name'] +
                    " " + response
                ),
                in_reply_to_status_id = data['id']
            )
        elif isinstance(response, MediaResponse):
            self.api.update_status_with_media(
                status = (
                    '@' + data['user']['screen_name'] +
                    " " + response.text
                ),
                media = response.media,
                in_reply_to_status_id = data['id']
            )
    
    def on_error(self,status_code,data):
        log(status_code)
    
    def debug_log_tweet(self,data,txt):
        if self.logging:
            self.api.update_status(
                status = (
                    '@' + data['user']['screen_name'] +
                    " Exception: " + txt
                ),
                in_reply_to_status_id = data['id']
            )
        else:
            return

def parse_command(data):
    text = data['text']
    try:
        command = text.split()[1]
        is_cmd = command[0] == cmd_prefix
        command = command[1:]
    except IndexError as e:
        log("index error")
        return None
    
    if is_cmd:
        if command.startswith("__") and command.endswith("__"):
            # Commands.__something__(data) ?
            # That counld be Commands.__delattr__, etc.
            # Well, although it's unlikely to cause any problems...
            return None
        if hasattr(Commands, command):
            # commands that returns string
            log('hasattr!')
            return (getattr(Commands,command)(data))
        
        elif hasattr(MediaCommands, command):
            # commands that uses media
            log('media!')
            return (getattr(MediaCommands,command)(data))
        
        else:
            # command seems to be given,
            # but not recognized
            log("not hasattr")
            return None
    else:
        # not a command!
        return None

def main():
    butler = TwitButler()
    butler.streamer.user()

if __name__ == "__main__":
    main()