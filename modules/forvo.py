#!/usr/bin/env python3

import json
import urllib.parse as par
import urllib.request as req

try:
    from .consts import forvo_key
except ImportError as e:
    import os
    forvo_key = os.environ['forvo_key']

BASE_URL = '/'.join([
    "http://apifree.forvo.com/key",
    forvo_key,
    "format",
    "json",
])

class ForvoRequest(object):
    base_url = BASE_URL
    optional_queries = []
    def __init__(self,word,**kargs):
        self.params = {}
        for opt_query in self.optional_queries:
            q = kargs.get(opt_query)
            if q is not None:
                self.params[opt_query] = q
        self.params['word'] = word
    
    def __repr__(self):
        return str(self.params)
    
    def to_url(self):
        queries = [
            '/'.join([k,par.quote(str(v))]) for (k,v) in self.params.items()
        ]
        return '/'.join([self.base_url] + queries)

class WordPronunciations(ForvoRequest):
    
    optional_queries = [
        'language', 'country',
        'username', 'sex',
        'rate', 'order', 'limit'
    ]
    
    def __init__(self,*arg,**kargs):
        super().__init__(*arg,**kargs)
        self.params['action'] = 'word-pronunciations'

class StandardPronunciation(ForvoRequest):
    
    optional_queries = ['language']
    
    def __init__(self,*arg,**kargs):
        super().__init__(*arg,**kargs)
        self.params['action'] = 'standard-pronunciation'

class Pronunciation(object):
    def __init__(self,data,query,restricted=False):
        self.data = data
        self.query = query
        self.restricted = restricted
    
    def __repr__(self):
        return "\n\t>--".join([
            str(self.data),
            str(self.query),
            "Restricted" if self.restricted else "Success"
        ])
    
    def show(self):
        pass

def best_rated_pronunciation(word,**kwargs):
    q = WordPronunciations(word, **kwargs)
    q.params['order'] = 'rate-desc'
    with req.urlopen(q.to_url()) as s:
        res = s.read().decode('utf-8')
    data = json.loads(res)
    try:
        pron = data['items'][0]
    except (IndexError, KeyError) as e:
        pron = None
    return (q,pron)

def pronunciation(word, **kwargs):
    rest = False
    (q,p) = best_rated_pronunciation(word, **kwargs)
    if p is None:
        rest = True
        (_,p) = best_rated_pronunciation(word)
    return Pronunciation(p,q,rest)

if __name__ == "__main__":
    print(pronunciation("Richard", country="GBR"))
