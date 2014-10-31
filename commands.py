#!/usr/bin/env python3
import time
from textwrap import dedent
from io import BytesIO
import modules.weather as wt
import modules.yahoo_rain as yahoo_rain
import modules.primes as primes
import modules.colorpics as colorpics
import modules.fractals as frct
import modules.imgloader as imgloader
import modules.imgeffector as imgeffector
import modules.characterise as characterise
from responses import *

def appendtimestamp(f):
    def g(*args,**kwargs):
        return f(*args,**kwargs) + " [{}]".format(
            str(time.time())[-6:])
    return g

class Commands(object):
    prime_handler = None
    
    @staticmethod
    def ping(data):
        """Check if bot is running."""
        return "pong (+{})".format(str(int(time.time()))[-5:])
    
    @staticmethod
    def time(data):
        """returns current time."""
        now = time.time()
        gmt = time.gmtime(now)
        return (
            "{}-{:02}-{:02} {:02}:{:02}:{:02} UTC / " +
            "{} secs since the epoc"
        ).format(
            gmt.tm_year, gmt.tm_mon, gmt.tm_mday,
            gmt.tm_hour, gmt.tm_min, gmt.tm_sec,
            now
        )
    
    @staticmethod
    @appendtimestamp
    def weather(data):
        """
        `!weather cityname`
        
        returns a weather forecast for cities listed here(https://t.co/gmMxzUzSXr).
        """
        # is cityname specified?
        try:
            cityname = data['text'].split()[2]
        except IndexError as e:
            return "city unspecified."
        
        # is the city listed on the forecast?
        try:
            frc = wt.WForecast(cityname)
        except ValueError as e:
            return "city not found."
        
        try:
            return '\n' + frc.forecast()
        except Exception as e:
            return "Error fetching data."
    
    @staticmethod
    @appendtimestamp
    def rain(data):
        """
        `!rain loc [.]`
        
        latest 10-min rainfall specified by loc (any string).
        Trailing .'s are ignored.  Powered by yahoo!.
        """
        # is cityname specified?
        try:
            cityname = data['text'].strip(".").split()[2:]
        except IndexError as e:
            return "city unspecified."
        cityname = " ".join(cityname)
        
        try:
            raindata = yahoo_rain.rainfall(cityname)
        except ValueError as e:
            return "Location {} not found. Try a different query.".format(
                cityname
            )
        
        if raindata is None:
            return (
                "Something went wrong and couldn't get rain info. Sorry. "
            )
        
        # ok, everything went fine.
        return "{} 現在の10分間降雨量: {}mm ({})".format(
            raindata[1]['Date'][-4:],
            raindata[1]['Rainfall'],
            raindata[0]['Name'],
        )
    
    @staticmethod
    def help(data):
        """
        `!help [cmd]`
        
        Help for the command specified.
        If no command is specified, returns list of commands.
        """
        try:
            cmd = data['text'].split()[2]
        except IndexError as e:
            cmd = None
        
        
        if cmd is None:
            # list available commands
            cmds = [c for c in dir(Commands) if not c.startswith('__')]
            res = 'commands: ' + ' '.join(cmds)
            if len(res) > 120:
                return res[:117] + '文字数'
            else:
                return res
        
        else:
            if cmd.startswith('__'):
                # __le__, etc. won't be nice.
                return "Command Invalid."
            
            # now consider 'real' commands.
            try:
                res = trim(getattr(Commands,cmd).__doc__)
            except AttributeError as e:
                res = "Command Not Found."
            try:
                res = trim(getattr(MediaCommands,cmd).__doc__)
            except AttributeError as e:
                res = "Command Not Found."
            
            return res[:120]
    
    @classmethod
    def factorize(cls,data):
        """
        `!factorize n`
        factorize an integer. Uses primes < 1million.
        """
        try:
            number = data['text'].split()[2]
        except IndexError as e:
            return "usage: !factorize number. No number specified."
        try:
            n = int(number)
        except ValueError as e:
            return "Failed to parse {} as an integer.".format(number)
        
        if cls.prime_handler is None:
            cls.prime_handler = primes.PrimeHandler(1000)
        
        try:
            factors = cls.prime_handler.factorise(n)
        except ValueError as e:
            return str(e)
        return_str = [
            "{}^{}".format(p,i) for (p,i) in factors
        ]
        return "*".join(return_str)
    
    @staticmethod
    def charinfo(data):
        """Returns unicode information about the first character given."""
        try:
            char = data['text'].split()[2][0]
        except IndexError as e:
            return "No character specified."
        
        chardata = characterise.char_data(char)
        chardata['hex'] = chardata['hex'][2:].rjust(4,'0').upper()
        
        return "{char} (U+{hex}) : {name}. cat: {cat}".format(**chardata)
    
    @staticmethod
    def emoji(data):
        """returns the emoji of the given name."""
        try:
            name = data['text'].split()[2].strip(':')
        except IndexError as e:
            return "No code specified."
        
        try:
            emoji = characterise.emoji_code(name)
        except KeyError as e:
            return (
                "Emoji with that code ({}) is not found.".format(name)
            )
        
        emojidata = characterise.char_data(emoji)
        emojidata['hex'] = emojidata['hex'][2:].rjust(4,'0').upper()
        
        return "{emoji} (U+{hex}/{name})".format(
            emoji=emoji, hex=emojidata['hex'], name=emojidata['name']
        )
    
    @staticmethod
    def delete(data):
        return DeleteResponse(data)
    

class MediaCommands(object):
    
    @staticmethod
    def rgb(data: "twdata") -> "Left String, Right MediaResponse":
        """returns a small image filled with the specified rgb."""
        try:
            r,g,b = data['text'].split()[2:5]
        except ValueError as e:
            return "Specify r,g and b separated with spaces."
        try:
            r,g,b = map(int,(r,g,b))
        except ValueError as e:
            return "Can only accept integers."
        try:
            assert all(0 <= c <= 255 for c in (r,g,b))
        except AssertionError as e:
            return "All values must be between 0 and 255."
        # phew. That was a lot!
        imgf = colorpics.rgb_image(r,g,b)
        return MediaResponse(
            "color : rgb {},{},{}".format(r,g,b),
            imgf
        )
    
    @staticmethod
    def julia(data: "twdata") -> "Left String, Right MediaResponse":
        """ returns julia. arguments: ReC ImC [x0 y0 x1 y1]"""
        
        failcode = str(time.time())[-6:]
        
        try:
            ReC, ImC = data['text'].split()[2:4]
        except ValueError as e:
            ReC, ImC = -1.24,0.075
        try:
            c = complex(float(ReC), float(ImC))
        except ValueError as e:
            return "can't parse {} and/or {} as floats. [{}]".format(ReC,ImC,failcode)
        
        try:
            grids = data['text'].split()[4:8]
        except ValueError as e:
            grids = [-0.3,-0.3,0.3,0.3]
        if len(grids) != 4:
            grids = [-0.3,-0.3,0.3,0.3]
        
        try:
            x0,y0,x1,y1 = map(float, grids)
        except ValueError as e:
            return "can't parse {} as floats. [{}]".format(grids,failcode)
        
        x0,x1 = min(x0,x1), max(x0,x1)
        y0,y1 = min(y0,y1), max(y0,y1)
        
        # phew!
        time0 = time.time()
        imgf = frct.julia(c=c, upperleft=(x0,y0), bottomright=(x1,y1))
        time1 = time.time()
        
        return_text = dedent(
            """
            julia set at c = {}+{}i, from ({},{}) to ({},{}).
            Took {:2.3f} secs to render.
            """).format(
                c.real, c.imag, x0, y0, x1, y1, time1-time0
            )
        
        return MediaResponse(return_text, imgf)
    
    @staticmethod
    def monochrome(data: "twdata") -> "Left String, Right MediaResponse":
        """
        returns monochrome version of your photo.
        You can specify weights for rgb.
        """
        
        failcode = str(time.time())[-5:]
        
        try:
            target_m = data['entities']['media'][0]
        except (IndexError, KeyError) as e:
            return "Give me an image !"
        
        try:
            img = imgloader.tw_load_img(target_m['media_url'], maxsize=1000)
        except imgloader.CantHandleException as e:
            return "{} [{}]".format(e,failcode)
        except imgloader.CantURLOpenException as e:
            return "{} [{}]".format(e,failcode)
        except imgloader.CantOpenException as e:
            return "{} [{}]".format(e,failcode)
        ext = img.format or 'png'
        
        imgf = BytesIO()
        time0 = time.time()
        mono_img = imgeffector.to_monochrome(img)
        time1 = time.time()
        mono_img.save(imgf, format=ext)
        imgf.seek(0)
        text = "took {:2.3f} secs to process.".format(time1-time0)
        
        return MediaResponse(text,imgf)

def trim(docstring):
    if docstring is None:
        return ''
    doclines = docstring.splitlines()
    
    if not doclines[0]:
        doclines.pop(0)
    if not doclines[-1]:
        doclines.pop(-1)
    
    return ' '.join(
        map(lambda x: x.lstrip() or '\n' , doclines)
    )
